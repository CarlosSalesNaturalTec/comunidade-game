import uuid
from datetime import datetime
from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import tuple_
from sqlalchemy.orm import Session

from ..autenticacao import ContextoDaSessao, exigir_persona
from ..banco import obter_sessao
from ..comunidades.modelo import ComunidadeVirtual
from ..erros import ErroDeValidacao, PermissaoNegada
from ..paginacao import (
    PaginaDeResultado,
    ParametrosDeListagem,
    codificar_cursor,
    contrato_de_listagem,
    decodificar_cursor,
)
from ..permissoes import Operacao, exigir_permissao
from ..personas.modelo import Papel, Persona
from ..pontos_de_apoio.modelo import PontoDeApoio
from ..recursos.modelo import TipoDeRecurso
from ..reservas.regra import disponivel_de
from ..resultados.regra import ResultadoDeclarado
from ..resultados.regra import lancar_atividade_realizada as _lancar_atividade_realizada
from ..tempo import DataHoraComFuso
from ..trilhas.modelo import Atividade, FormatoDeAtividade, Missao, Trilha
from .modelo import Aula, ModoDeComprovacao, Presenca, RecursoDeclaradoDaAula, SituacaoDaAula
from .regra import (
    RecursoDeclaradoEntrada,
    agendar_aula,
    aulas_vigentes,
    cancelar_aula,
    escopo_de_comunidade_da_leitura,
    registrar_presenca,
    tentar_reservar_aula_pendente,
)

roteador = APIRouter()


class RecursoDeclaradoCorpo(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tipo_de_recurso_id: uuid.UUID
    quantidade: Decimal


class RecursoFaltanteSaida(BaseModel):
    tipo_de_recurso_id: uuid.UUID
    quantidade_declarada: Decimal
    quantidade_disponivel: Decimal


class AulaSaida(BaseModel):
    id: uuid.UUID
    comunidade_virtual_id: uuid.UUID
    ponto_de_apoio_id: uuid.UUID
    inicio_em: DataHoraComFuso
    fim_em: DataHoraComFuso
    situacao: str
    cancelamento_motivo: str | None
    recursos_faltantes: list[RecursoFaltanteSaida]


def _recursos_faltantes(sessao: Session, aula: Aula) -> list[RecursoFaltanteSaida]:
    """Só a aula pendente de lastro tem o que faltar a mostrar — as demais
    devolvem lista vazia (`RF-07-08`, PRD-07 §5.3)."""
    if aula.situacao != SituacaoDaAula.pendente_de_lastro:
        return []

    declarados = sessao.query(RecursoDeclaradoDaAula).filter_by(aula_id=aula.id).all()
    faltantes = []
    for declarado in declarados:
        disponivel = disponivel_de(
            sessao,
            tipo_de_recurso_id=declarado.tipo_de_recurso_id,
            ponto_de_apoio_id=aula.ponto_de_apoio_id,
        )
        if disponivel < declarado.quantidade:
            faltantes.append(
                RecursoFaltanteSaida(
                    tipo_de_recurso_id=declarado.tipo_de_recurso_id,
                    quantidade_declarada=declarado.quantidade,
                    quantidade_disponivel=disponivel,
                )
            )
    return faltantes


def _saida(sessao: Session, aula: Aula) -> AulaSaida:
    return AulaSaida(
        id=aula.id,
        comunidade_virtual_id=aula.comunidade_virtual_id,
        ponto_de_apoio_id=aula.ponto_de_apoio_id,
        inicio_em=aula.inicio_em,
        fim_em=aula.fim_em,
        situacao=aula.situacao.value,
        cancelamento_motivo=aula.cancelamento_motivo,
        recursos_faltantes=_recursos_faltantes(sessao, aula),
    )


class AgendarAulaEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    comunidade_virtual_id: uuid.UUID
    ponto_de_apoio_id: uuid.UUID
    inicio_em: DataHoraComFuso
    fim_em: DataHoraComFuso
    recursos_declarados: list[RecursoDeclaradoCorpo] = Field(default_factory=list)


@roteador.post("/aulas", status_code=201)
def agendar_aula_rota(
    entrada: AgendarAulaEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> AulaSaida:
    """Restrita ao Admin — agenda e dispara a reserva dos recursos
    declarados (`RF-07-08`, `RF-02-31`, `RF-01-16`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    comunidade = sessao_bd.get(ComunidadeVirtual, entrada.comunidade_virtual_id)
    ponto_de_apoio = sessao_bd.get(PontoDeApoio, entrada.ponto_de_apoio_id)
    recursos_declarados = [
        RecursoDeclaradoEntrada(
            tipo=sessao_bd.get(TipoDeRecurso, item.tipo_de_recurso_id),
            quantidade=item.quantidade,
        )
        for item in entrada.recursos_declarados
    ]

    aula = agendar_aula(
        sessao_bd,
        operador=operador,
        comunidade=comunidade,
        ponto_de_apoio=ponto_de_apoio,
        inicio_em=entrada.inicio_em,
        fim_em=entrada.fim_em,
        recursos_declarados=recursos_declarados,
    )
    sessao_bd.commit()
    return _saida(sessao_bd, aula)


def _analisar_comunidade(valor: str | None) -> uuid.UUID | None:
    if not valor:
        return None
    try:
        return uuid.UUID(valor)
    except ValueError as exc:
        raise ErroDeValidacao(
            mensagem="Filtro 'comunidade' precisa ser um identificador válido.",
            campo="comunidade",
        ) from exc


def _analisar_momento(bruto: str, campo: str) -> datetime:
    """Mesma régua de `auditoria/rotas.py`: toda data e hora de filtro exige
    fuso explícito (PRD-01 §9)."""
    try:
        valor = datetime.fromisoformat(bruto)
    except ValueError as exc:
        raise ErroDeValidacao(
            mensagem=f"Filtro '{campo}' precisa ser uma data e hora ISO 8601.", campo=campo
        ) from exc
    if valor.tzinfo is None:
        raise ErroDeValidacao(mensagem=f"Filtro '{campo}' exige fuso explícito.", campo=campo)
    return valor


@roteador.get("/aulas", response_model=PaginaDeResultado[AulaSaida])
def listar_agenda_rota(
    parametros: Annotated[ParametrosDeListagem, Depends(contrato_de_listagem())],
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> PaginaDeResultado[AulaSaida]:
    """Restrita à gestão — Admin lê qualquer comunidade, sempre declarada; o
    Mestre lê só a do seu vínculo vigente, e sem vínculo lê lista vazia. O
    filtro de período recorta pelo horário inicial da aula (`RF-02-12`,
    `RF-01-28`, `RF-01-18`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    comunidade_id = _analisar_comunidade(parametros.filtros.get("comunidade"))
    alvo_id = escopo_de_comunidade_da_leitura(
        operador=operador, comunidade_virtual_id=comunidade_id
    )
    if alvo_id is None:
        return PaginaDeResultado(itens=[], proximo_cursor=None)

    consulta = sessao_bd.query(Aula).filter(Aula.comunidade_virtual_id == alvo_id)

    periodo_inicio = parametros.filtros.get("periodo_inicio")
    if periodo_inicio:
        consulta = consulta.filter(
            Aula.inicio_em >= _analisar_momento(periodo_inicio, "periodo_inicio")
        )
    periodo_fim = parametros.filtros.get("periodo_fim")
    if periodo_fim:
        consulta = consulta.filter(Aula.inicio_em <= _analisar_momento(periodo_fim, "periodo_fim"))

    if parametros.cursor:
        posicao = decodificar_cursor(parametros.cursor)
        try:
            inicio_em_cursor = datetime.fromisoformat(posicao["inicio_em"])
            id_cursor = uuid.UUID(posicao["id"])
        except (KeyError, ValueError) as exc:
            raise ErroDeValidacao(mensagem="Cursor de paginação inválido.", campo="cursor") from exc
        consulta = consulta.filter(tuple_(Aula.inicio_em, Aula.id) > (inicio_em_cursor, id_cursor))

    consulta = consulta.order_by(Aula.inicio_em, Aula.id).limit(parametros.tamanho + 1)
    aulas = consulta.all()

    proximo_cursor = None
    if len(aulas) > parametros.tamanho:
        aulas = aulas[: parametros.tamanho]
        ultima = aulas[-1]
        proximo_cursor = codificar_cursor(
            {"inicio_em": ultima.inicio_em.isoformat(), "id": str(ultima.id)}
        )

    return PaginaDeResultado(
        itens=[_saida(sessao_bd, aula) for aula in aulas], proximo_cursor=proximo_cursor
    )


@roteador.get("/aulas/vigentes", response_model=PaginaDeResultado[AulaSaida])
def listar_aulas_vigentes_rota(
    parametros: Annotated[ParametrosDeListagem, Depends(contrato_de_listagem())],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> PaginaDeResultado[AulaSaida]:
    """Rota pública — chave de aplicação sim, credencial de persona não —,
    exposta antes de qualquer pessoa se identificar. Consome `aulas_vigentes`
    sem alterá-la; sem aula vigente, responde 200 com conjunto vazio, nunca
    erro (`RF-02-14`, `RF-02-13`, `RF-01-32`, `RF-01-02`, `RN-02-05`)."""
    comunidade_id = _analisar_comunidade(parametros.filtros.get("comunidade"))
    vigentes = aulas_vigentes(sessao_bd)
    if comunidade_id is not None:
        vigentes = [aula for aula in vigentes if aula.comunidade_virtual_id == comunidade_id]
    return PaginaDeResultado(
        itens=[_saida(sessao_bd, aula) for aula in vigentes], proximo_cursor=None
    )


@roteador.post("/aulas/{id_da_aula}/reservas")
def tentar_reservar_aula_pendente_rota(
    id_da_aula: uuid.UUID,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> AulaSaida:
    """Caminho explícito e idempotente da PRD-07 §9: tenta de novo a reserva
    de uma aula pendente de lastro; aula já confirmada devolve o estado
    corrente sem duplicar reserva (design — Decisions 6)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    aula = sessao_bd.get(Aula, id_da_aula)
    aula = tentar_reservar_aula_pendente(sessao_bd, operador=operador, aula=aula)
    sessao_bd.commit()
    return _saida(sessao_bd, aula)


class ResultadoDeclaradoCorpo(BaseModel):
    model_config = ConfigDict(extra="forbid")

    guerreiro_id: uuid.UUID
    atividade_id: uuid.UUID
    momento_do_fato: DataHoraComFuso
    producao: str = Field(min_length=1)
    desfecho: str


class LancarAtividadeRealizadaEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    resultados: list[ResultadoDeclaradoCorpo] = Field(default_factory=list)


@roteador.post("/aulas/{id_da_aula}/lancamentos", status_code=201)
def lancar_atividade_realizada_rota(
    id_da_aula: uuid.UUID,
    entrada: LancarAtividadeRealizadaEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> AulaSaida:
    """Restrita ao Admin — grava os Resultados de todos os participantes e
    converte cada reserva da aula em débito, na mesma operação (`RF-07-09`,
    `RF-02-35`, `RN-07-36`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    aula = sessao_bd.get(Aula, id_da_aula)
    resultados = [
        ResultadoDeclarado(
            guerreiro_id=item.guerreiro_id,
            atividade=sessao_bd.get(Atividade, item.atividade_id),
            momento_do_fato=item.momento_do_fato,
            producao=item.producao,
            desfecho=item.desfecho,
        )
        for item in entrada.resultados
    ]

    aula, _ = _lancar_atividade_realizada(
        sessao_bd, operador=operador, aula=aula, resultados=resultados
    )
    sessao_bd.commit()
    return _saida(sessao_bd, aula)


class CancelarAulaEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    motivo: str = Field(min_length=1)


@roteador.post("/aulas/{id_da_aula}/cancelamento")
def cancelar_aula_rota(
    id_da_aula: uuid.UUID,
    entrada: CancelarAulaEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> AulaSaida:
    """Admin ou Mestre da comunidade cancelam, sempre com motivo — libera as
    reservas da aula (`RF-01-72`, `RF-01-17`, `RF-02-95`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    aula = sessao_bd.get(Aula, id_da_aula)
    aula = cancelar_aula(sessao_bd, operador=operador, aula=aula, motivo=entrada.motivo)
    sessao_bd.commit()
    return _saida(sessao_bd, aula)


class ConfirmarPresencaEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    guerreiro_id: uuid.UUID
    modo: str
    momento_do_fato: DataHoraComFuso


class PresencaSaida(BaseModel):
    id: uuid.UUID
    aula_id: uuid.UUID
    guerreiro_id: uuid.UUID
    modo: str
    confirmador_id: uuid.UUID | None
    momento_do_fato: DataHoraComFuso


def _saida_da_presenca(presenca: Presenca) -> PresencaSaida:
    return PresencaSaida(
        id=presenca.id,
        aula_id=presenca.aula_id,
        guerreiro_id=presenca.guerreiro_id,
        modo=presenca.modo.value,
        confirmador_id=presenca.confirmador_id,
        momento_do_fato=presenca.momento_do_fato,
    )


@roteador.post("/aulas/{id_da_aula}/presencas", status_code=201)
def confirmar_presenca_rota(
    id_da_aula: uuid.UUID,
    entrada: ConfirmarPresencaEntrada,
    contexto: Annotated[
        ContextoDaSessao,
        Depends(exigir_permissao(Operacao.confirmacao_de_identidade_do_guerreiro, "escreve")),
    ],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> PresencaSaida:
    """O Mestre alcança a presença só pela confirmação de identidade do
    Guerreiro(a) — a mesma operação que a matriz já lhe concede; o modo
    reconhecimento continua exclusivo do App 01 e é recusado aqui, antes de
    chamar `registrar_presenca`, que não distingue papel algum (`RF-09-45`,
    `RF-01-20`, `RF-01-17`, design — Decisions 2)."""
    if entrada.modo != ModoDeComprovacao.confirmacao.value:
        raise PermissaoNegada(mensagem="Esta rota só registra presença no modo confirmação.")

    operador = sessao_bd.get(Persona, contexto.persona_id)
    aula = sessao_bd.get(Aula, id_da_aula)
    guerreiro = sessao_bd.get(Persona, entrada.guerreiro_id)

    presenca = registrar_presenca(
        sessao_bd,
        operador=operador,
        aula=aula,
        guerreiro=guerreiro,
        modo=entrada.modo,
        confirmador=operador,
        momento_do_fato=entrada.momento_do_fato,
    )
    sessao_bd.commit()
    return _saida_da_presenca(presenca)


class AtividadeDoMestreSaida(BaseModel):
    id: uuid.UUID
    missao_id: uuid.UUID
    titulo: str
    formato: str
    modalidade: str


class MinhasTurmasSaida(PaginaDeResultado[AulaSaida]):
    atividades_presenciais: list[AtividadeDoMestreSaida] = Field(default_factory=list)
    atividades_on_line: list[AtividadeDoMestreSaida] = Field(default_factory=list)


def _saida_da_atividade(atividade: Atividade) -> AtividadeDoMestreSaida:
    return AtividadeDoMestreSaida(
        id=atividade.id,
        missao_id=atividade.missao_id,
        titulo=atividade.titulo,
        formato=atividade.formato.value,
        modalidade=atividade.modalidade.value,
    )


@roteador.get("/minhas-turmas")
def listar_minhas_turmas_rota(
    parametros: Annotated[ParametrosDeListagem, Depends(contrato_de_listagem())],
    contexto: Annotated[ContextoDaSessao, Depends(exigir_permissao(Operacao.suas_turmas, "le"))],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> MinhasTurmasSaida:
    """Restrita à operação `suas_turmas`: as aulas das comunidades do Mestre
    em sessão, paginadas no padrão da agenda, e as atividades de que ele é
    autor, separadas pelo formato — presencial do encontro e on-line entre
    encontros (`RF-09-42`, `RF-09-73`, `RN-09-08`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    comunidade_id = _analisar_comunidade(parametros.filtros.get("comunidade"))
    alvo_id = escopo_de_comunidade_da_leitura(
        operador=operador, comunidade_virtual_id=comunidade_id
    )
    if alvo_id is None:
        return MinhasTurmasSaida(itens=[], proximo_cursor=None)

    consulta = sessao_bd.query(Aula).filter(Aula.comunidade_virtual_id == alvo_id)
    if parametros.cursor:
        posicao = decodificar_cursor(parametros.cursor)
        try:
            inicio_em_cursor = datetime.fromisoformat(posicao["inicio_em"])
            id_cursor = uuid.UUID(posicao["id"])
        except (KeyError, ValueError) as exc:
            raise ErroDeValidacao(mensagem="Cursor de paginação inválido.", campo="cursor") from exc
        consulta = consulta.filter(tuple_(Aula.inicio_em, Aula.id) > (inicio_em_cursor, id_cursor))
    consulta = consulta.order_by(Aula.inicio_em, Aula.id).limit(parametros.tamanho + 1)
    aulas = consulta.all()

    proximo_cursor = None
    if len(aulas) > parametros.tamanho:
        aulas = aulas[: parametros.tamanho]
        ultima = aulas[-1]
        proximo_cursor = codificar_cursor(
            {"inicio_em": ultima.inicio_em.isoformat(), "id": str(ultima.id)}
        )

    consulta_de_atividades = (
        sessao_bd.query(Atividade)
        .join(Missao, Missao.id == Atividade.missao_id)
        .join(Trilha, Trilha.id == Missao.trilha_id)
    )
    if operador.papel != Papel.admin:
        consulta_de_atividades = consulta_de_atividades.filter(Trilha.autor_id == operador.id)
    atividades = consulta_de_atividades.all()

    return MinhasTurmasSaida(
        itens=[_saida(sessao_bd, aula) for aula in aulas],
        proximo_cursor=proximo_cursor,
        atividades_presenciais=[
            _saida_da_atividade(a) for a in atividades if a.formato == FormatoDeAtividade.presencial
        ],
        atividades_on_line=[
            _saida_da_atividade(a)
            for a in atividades
            if a.formato == FormatoDeAtividade.on_line_assincrona
        ],
    )
