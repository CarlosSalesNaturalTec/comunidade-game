import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from ..armazenamento.fabrica import dependencia_de_armazenamento
from ..armazenamento.porta import PortaDeArmazenamento
from ..autenticacao import ContextoDaSessao, exigir_persona
from ..banco import obter_sessao
from ..erros import PermissaoNegada
from ..personas.modelo import Papel, Persona
from ..vitrine.publico import AvatarENickSaida, buscar_avatares_e_nicks
from .modelo import (
    FonteDaPontuacaoDoBem,
    PontuacaoDoBem,
    RegistroDeCustomizacao,
    SituacaoDoRegistroDeCustomizacao,
)
from .regra import (
    BemRecebido,
    UltimoRegistroAprovado,
    abrir_envio_da_customizacao,
    bens_recebidos,
    cancelar_customizacao,
    confirmar_envio_da_customizacao,
    fila_do_cuidado,
    julgar_customizacao,
    ler_arquivo_da_customizacao,
    registrar_customizacao,
    registros_do_guerreiro,
    validar_conservacao,
)

roteador = APIRouter(tags=["cuidado com o bem recebido"])


# ---------------------------------------------------------------------------
# Saídas
# ---------------------------------------------------------------------------


class RegistroDeCustomizacaoSaida(BaseModel):
    id: uuid.UUID
    entrega_de_recompensa_id: uuid.UUID
    descricao: str
    situacao: SituacaoDoRegistroDeCustomizacao
    tem_midia: bool
    tipo_do_arquivo: str | None = None
    motivo_do_julgamento: str | None = None
    aula_id: uuid.UUID | None = None
    julgado_em: datetime | None = None
    registrado_em: datetime


def _saida_do_registro(registro: RegistroDeCustomizacao) -> RegistroDeCustomizacaoSaida:
    return RegistroDeCustomizacaoSaida(
        id=registro.id,
        entrega_de_recompensa_id=registro.entrega_de_recompensa_id,
        descricao=registro.descricao,
        situacao=registro.situacao,
        tem_midia=registro.midia_referencia is not None,
        tipo_do_arquivo=registro.midia_tipo_do_arquivo,
        motivo_do_julgamento=registro.motivo_do_julgamento,
        aula_id=registro.aula_id,
        julgado_em=registro.julgado_em,
        registrado_em=registro.registrado_em,
    )


class UltimoRegistroAprovadoSaida(BaseModel):
    """O "antes" do kit: `fonte` diz por qual rota de bytes ele sai — a da
    customização ou a da comprovação do prático."""

    fonte: str
    id: uuid.UUID
    descricao: str | None = None
    tipo_do_arquivo: str | None = None
    aprovado_em: datetime | None = None


def _saida_do_ultimo(ultimo: UltimoRegistroAprovado | None) -> UltimoRegistroAprovadoSaida | None:
    if ultimo is None:
        return None
    return UltimoRegistroAprovadoSaida(
        fonte=ultimo.fonte,
        id=ultimo.id,
        descricao=ultimo.descricao,
        tipo_do_arquivo=ultimo.tipo_do_arquivo,
        aprovado_em=ultimo.aprovado_em,
    )


class BemRecebidoSaida(BaseModel):
    entrega_de_recompensa_id: uuid.UUID
    recompensa_de_marco_id: uuid.UUID
    tipo_de_recurso_nome: str
    trilha_id: uuid.UUID
    trilha_nome: str
    customizacao_aberta: bool
    ultimo_aprovado: UltimoRegistroAprovadoSaida | None = None
    pendente: RegistroDeCustomizacaoSaida | None = None
    pontuado_na_aula: FonteDaPontuacaoDoBem | None = None


def _saida_do_bem(bem: BemRecebido) -> BemRecebidoSaida:
    return BemRecebidoSaida(
        entrega_de_recompensa_id=bem.entrega.id,
        recompensa_de_marco_id=bem.recompensa.id,
        tipo_de_recurso_nome=bem.tipo_de_recurso_nome,
        trilha_id=bem.trilha_id,
        trilha_nome=bem.trilha_nome,
        customizacao_aberta=bem.customizacao_aberta,
        ultimo_aprovado=_saida_do_ultimo(bem.ultimo_aprovado),
        pendente=_saida_do_registro(bem.pendente) if bem.pendente is not None else None,
        pontuado_na_aula=bem.pontuado_na_aula,
    )


class MinhasCustomizacoesSaida(BaseModel):
    kits_abertos: list[BemRecebidoSaida]
    registros: list[RegistroDeCustomizacaoSaida]


class PresenteNaFilaSaida(BaseModel):
    guerreiro_id: uuid.UUID
    guerreiro: AvatarENickSaida | None
    bens: list[BemRecebidoSaida]


class PontuacaoDoBemSaida(BaseModel):
    id: uuid.UUID
    aula_id: uuid.UUID
    entrega_de_recompensa_id: uuid.UUID
    guerreiro_id: uuid.UUID
    fonte: FonteDaPontuacaoDoBem


def _saida_da_pontuacao(pontuacao: PontuacaoDoBem) -> PontuacaoDoBemSaida:
    return PontuacaoDoBemSaida(
        id=pontuacao.id,
        aula_id=pontuacao.aula_id,
        entrega_de_recompensa_id=pontuacao.entrega_de_recompensa_id,
        guerreiro_id=pontuacao.guerreiro_id,
        fonte=pontuacao.fonte,
    )


# ---------------------------------------------------------------------------
# Entradas
# ---------------------------------------------------------------------------


class RegistrarCustomizacaoEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    entrega_de_recompensa_id: uuid.UUID
    descricao: str | None = None


class CapturarCustomizacaoEntrada(RegistrarCustomizacaoEntrada):
    guerreiro_id: uuid.UUID


class AbrirEnvioEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tipo_mime: str
    tamanho_declarado: int


class AbrirEnvioSaida(BaseModel):
    endereco_da_sessao: str


class JulgarCustomizacaoEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    aula_id: uuid.UUID
    aprovado: bool | None = None
    motivo: str | None = None


class ValidarConservacaoEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    guerreiro_id: uuid.UUID
    entrega_de_recompensa_id: uuid.UUID


# ---------------------------------------------------------------------------
# Rotas
# ---------------------------------------------------------------------------


def _operador(sessao_bd: Session, contexto: ContextoDaSessao) -> Persona:
    return sessao_bd.get(Persona, contexto.persona_id)


@roteador.get("/eu/customizacoes")
def minhas_customizacoes_rota(
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> MinhasCustomizacoesSaida:
    """`RF-05-103`: os kits abertos, com o último aprovado, e os registros do
    Guerreiro(a) em sessão — sem identificador de persona na rota."""
    if contexto.papel != Papel.guerreiro:
        raise PermissaoNegada(mensagem="Só o Guerreiro(a) lê as próprias customizações.")
    bens = bens_recebidos(sessao_bd, contexto.persona_id)
    return MinhasCustomizacoesSaida(
        kits_abertos=[_saida_do_bem(bem) for bem in bens if bem.customizacao_aberta],
        registros=[
            _saida_do_registro(registro)
            for registro in registros_do_guerreiro(sessao_bd, contexto.persona_id)
        ],
    )


@roteador.post("/eu/customizacoes", status_code=201)
def registrar_customizacao_rota(
    entrada: RegistrarCustomizacaoEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> RegistroDeCustomizacaoSaida:
    """`RF-05-102`, `RF-04-80`: o Guerreiro(a) registra a customização."""
    operador = _operador(sessao_bd, contexto)
    if operador.papel != Papel.guerreiro:
        raise PermissaoNegada(mensagem="Esta rota é do próprio Guerreiro(a).")
    registro = registrar_customizacao(
        sessao_bd,
        operador=operador,
        entrega_de_recompensa_id=entrada.entrega_de_recompensa_id,
        descricao=entrada.descricao,
    )
    sessao_bd.commit()
    return _saida_do_registro(registro)


@roteador.post("/aulas/{id_da_aula}/customizacoes", status_code=201)
def capturar_customizacao_rota(
    id_da_aula: uuid.UUID,
    entrada: CapturarCustomizacaoEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> RegistroDeCustomizacaoSaida:
    """`RF-04-82`: o Mestre da aula captura o registro na hora, em nome do
    Guerreiro(a) presente."""
    operador = _operador(sessao_bd, contexto)
    if operador.papel != Papel.mestre:
        raise PermissaoNegada(mensagem="Só o Mestre da aula captura o registro no encontro.")
    registro = registrar_customizacao(
        sessao_bd,
        operador=operador,
        entrega_de_recompensa_id=entrada.entrega_de_recompensa_id,
        descricao=entrada.descricao,
        guerreiro_id=entrada.guerreiro_id,
        aula_id=id_da_aula,
    )
    sessao_bd.commit()
    return _saida_do_registro(registro)


@roteador.post("/customizacoes/{id_do_registro}/envios", status_code=201)
def abrir_envio_da_customizacao_rota(
    id_do_registro: uuid.UUID,
    entrada: AbrirEnvioEntrada,
    requisicao: Request,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    armazenamento: Annotated[PortaDeArmazenamento, Depends(dependencia_de_armazenamento)],
) -> AbrirEnvioSaida:
    """`RF-01-84`: abre a sessão retomável da foto ou do vídeo do kit."""
    endereco = abrir_envio_da_customizacao(
        sessao_bd,
        sessao_bd.get(RegistroDeCustomizacao, id_do_registro),
        operador=_operador(sessao_bd, contexto),
        tipo_mime=entrada.tipo_mime,
        tamanho_declarado=entrada.tamanho_declarado,
        armazenamento=armazenamento,
        origem=requisicao.headers.get("Origin"),
    )
    sessao_bd.commit()
    return AbrirEnvioSaida(endereco_da_sessao=endereco)


@roteador.post("/customizacoes/{id_do_registro}/envios/confirmacao")
def confirmar_envio_da_customizacao_rota(
    id_do_registro: uuid.UUID,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    armazenamento: Annotated[PortaDeArmazenamento, Depends(dependencia_de_armazenamento)],
) -> RegistroDeCustomizacaoSaida:
    """Só agora o registro tem mídia e pode ser julgado."""
    registro = confirmar_envio_da_customizacao(
        sessao_bd,
        sessao_bd.get(RegistroDeCustomizacao, id_do_registro),
        operador=_operador(sessao_bd, contexto),
        armazenamento=armazenamento,
    )
    sessao_bd.commit()
    return _saida_do_registro(registro)


@roteador.get("/customizacoes/{id_do_registro}/arquivo")
def ler_arquivo_da_customizacao_rota(
    id_do_registro: uuid.UUID,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    armazenamento: Annotated[PortaDeArmazenamento, Depends(dependencia_de_armazenamento)],
) -> Response:
    """Os bytes ao Guerreiro(a) dono e ao Mestre da comunidade dele."""
    arquivo = ler_arquivo_da_customizacao(
        sessao_bd,
        sessao_bd.get(RegistroDeCustomizacao, id_do_registro),
        operador=_operador(sessao_bd, contexto),
        armazenamento=armazenamento,
    )
    return Response(content=arquivo.bytes_do_arquivo, media_type=arquivo.tipo_mime)


@roteador.post("/customizacoes/{id_do_registro}/cancelamento")
def cancelar_customizacao_rota(
    id_do_registro: uuid.UUID,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> RegistroDeCustomizacaoSaida:
    """`RF-05-103`, `RF-01-86`: o Guerreiro(a) cancela o próprio pendente."""
    registro = cancelar_customizacao(
        sessao_bd,
        sessao_bd.get(RegistroDeCustomizacao, id_do_registro),
        operador=_operador(sessao_bd, contexto),
    )
    sessao_bd.commit()
    return _saida_do_registro(registro)


@roteador.post("/customizacoes/{id_do_registro}/julgamento")
def julgar_customizacao_rota(
    id_do_registro: uuid.UUID,
    entrada: JulgarCustomizacaoEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> RegistroDeCustomizacaoSaida:
    """`RF-01-85`, `RF-04-82`, `RF-04-83`: o Mestre da aula julga ao vivo."""
    registro = julgar_customizacao(
        sessao_bd,
        sessao_bd.get(RegistroDeCustomizacao, id_do_registro),
        operador=_operador(sessao_bd, contexto),
        aula_id=entrada.aula_id,
        aprovado=entrada.aprovado,
        motivo=entrada.motivo,
    )
    sessao_bd.commit()
    return _saida_do_registro(registro)


@roteador.post("/aulas/{id_da_aula}/conservacoes", status_code=201)
def validar_conservacao_rota(
    id_da_aula: uuid.UUID,
    entrada: ValidarConservacaoEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> PontuacaoDoBemSaida:
    """`RF-01-87`, `RF-09-113`, `RF-04-84`: o Mestre da aula valida a
    conservação do bem recebido."""
    pontuacao = validar_conservacao(
        sessao_bd,
        operador=_operador(sessao_bd, contexto),
        aula_id=id_da_aula,
        guerreiro_id=entrada.guerreiro_id,
        entrega_de_recompensa_id=entrada.entrega_de_recompensa_id,
    )
    sessao_bd.commit()
    return _saida_da_pontuacao(pontuacao)


@roteador.get("/aulas/{id_da_aula}/fila-do-cuidado")
def fila_do_cuidado_rota(
    id_da_aula: uuid.UUID,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> list[PresenteNaFilaSaida]:
    """`RF-04-81`, `RF-04-84`: a fila do encontro, só com quem tem presença."""
    _, fila = fila_do_cuidado(
        sessao_bd, operador=_operador(sessao_bd, contexto), aula_id=id_da_aula
    )
    avatares = buscar_avatares_e_nicks(sessao_bd, {item.guerreiro.id for item in fila})
    return [
        PresenteNaFilaSaida(
            guerreiro_id=item.guerreiro.id,
            guerreiro=avatares.get(item.guerreiro.id),
            bens=[_saida_do_bem(bem) for bem in item.bens],
        )
        for item in fila
    ]
