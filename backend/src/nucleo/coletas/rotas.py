import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, Request, UploadFile
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from ..armazenamento.fabrica import dependencia_de_armazenamento
from ..armazenamento.porta import PortaDeArmazenamento
from ..autenticacao import (
    NOME_DO_CABECALHO_DE_DISPOSITIVO,
    ContextoDaSessao,
    exigir_credencial_de_dispositivo,
    exigir_persona,
)
from ..banco import obter_sessao
from ..erros import PermissaoNegada
from ..permissoes import Operacao, conferir_permissao, exigir_permissao
from ..personas.modelo import Credencial, Persona
from ..tempo import DataHoraComFuso
from ..trilhas.modelo import Missao
from .modelo import DesafioDeColeta, SerieDeColeta
from .regra import (
    abrir_serie_de_coleta,
    cadastrar_tipo_de_coleta,
    criar_desafio_de_coleta,
    emitir_credencial_de_dispositivo,
    gravar_registro_de_coleta,
    revogar_credencial_de_dispositivo,
)

roteador = APIRouter()


class CriarTipoDeColetaEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nome: str = Field(min_length=1)
    forma_de_registro: str = Field(min_length=1)
    unidade: str | None = None
    faixa_minima: float | None = None
    faixa_maxima: float | None = None


class TipoDeColetaSaida(BaseModel):
    id: uuid.UUID
    nome: str
    forma_de_registro: str
    unidade: str | None
    faixa_minima: float | None
    faixa_maxima: float | None
    ativo: bool


@roteador.post("/tipos-de-coleta", status_code=201)
def cadastrar_tipo_de_coleta_rota(
    entrada: CriarTipoDeColetaEntrada,
    contexto: Annotated[
        ContextoDaSessao,
        Depends(exigir_permissao(Operacao.catalogo_de_tipos_de_coleta, "escreve")),
    ],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> TipoDeColetaSaida:
    """Restrita ao Admin — a recusa de qualquer outro papel, inclusive o
    Mestre, é 403 pela matriz de permissões (`RF-08-05`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    tipo = cadastrar_tipo_de_coleta(
        sessao_bd,
        operador=operador,
        nome=entrada.nome,
        forma_de_registro=entrada.forma_de_registro,
        unidade=entrada.unidade,
        faixa_minima=entrada.faixa_minima,
        faixa_maxima=entrada.faixa_maxima,
    )
    sessao_bd.commit()
    return TipoDeColetaSaida(
        id=tipo.id,
        nome=tipo.nome,
        forma_de_registro=tipo.forma_de_registro.value,
        unidade=tipo.unidade,
        faixa_minima=tipo.faixa_minima,
        faixa_maxima=tipo.faixa_maxima,
        ativo=tipo.ativo,
    )


class CriarDesafioDeColetaEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    missao_id: uuid.UUID
    tipo_de_coleta_id: uuid.UUID
    cadencia: str = Field(min_length=1)
    vigencia_inicio: DataHoraComFuso
    vigencia_fim: DataHoraComFuso
    granularidade_exigida: str = Field(min_length=1)
    registros_que_pontuam_por_periodo: int


class DesafioDeColetaSaida(BaseModel):
    id: uuid.UUID
    missao_id: uuid.UUID
    tipo_de_coleta_id: uuid.UUID
    cadencia: str
    vigencia_inicio: datetime
    vigencia_fim: datetime
    granularidade_exigida: str
    registros_que_pontuam_por_periodo: int


@roteador.post("/desafios-de-coleta", status_code=201)
def criar_desafio_de_coleta_rota(
    entrada: CriarDesafioDeColetaEntrada,
    contexto: Annotated[
        ContextoDaSessao, Depends(exigir_permissao(Operacao.suas_trilhas_e_conteudos, "escreve"))
    ],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> DesafioDeColetaSaida:
    """Restrita ao Mestre autor da trilha da missão e ao Admin — a posse é
    conferida em `criar_desafio_de_coleta`, pela trilha alcançada a partir
    da missão (`RF-08-06`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    missao = sessao_bd.get(Missao, entrada.missao_id)
    desafio = criar_desafio_de_coleta(
        sessao_bd,
        operador=operador,
        missao=missao,
        tipo_de_coleta_id=entrada.tipo_de_coleta_id,
        cadencia=entrada.cadencia,
        vigencia_inicio=entrada.vigencia_inicio,
        vigencia_fim=entrada.vigencia_fim,
        granularidade_exigida=entrada.granularidade_exigida,
        registros_que_pontuam_por_periodo=entrada.registros_que_pontuam_por_periodo,
    )
    sessao_bd.commit()
    return DesafioDeColetaSaida(
        id=desafio.id,
        missao_id=desafio.missao_id,
        tipo_de_coleta_id=desafio.tipo_de_coleta_id,
        cadencia=desafio.cadencia.value,
        vigencia_inicio=desafio.vigencia_inicio,
        vigencia_fim=desafio.vigencia_fim,
        granularidade_exigida=desafio.granularidade_exigida.value,
        registros_que_pontuam_por_periodo=desafio.registros_que_pontuam_por_periodo,
    )


class AbrirSerieDeColetaEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    desafio_de_coleta_id: uuid.UUID
    local_id: uuid.UUID
    # Aceito e sempre ignorado: a série é sempre do Guerreiro(a) da sessão,
    # nunca do que vier no corpo (`RN-08-04`).
    coletor_id: uuid.UUID | None = None


class SerieDeColetaSaida(BaseModel):
    id: uuid.UUID
    desafio_de_coleta_id: uuid.UUID
    coletor_id: uuid.UUID
    local_id: uuid.UUID
    cadencia: str
    estado: str
    aberta_em: datetime
    ultima_medicao_valida_em: datetime | None


@roteador.post("/series-de-coleta", status_code=201)
def abrir_serie_de_coleta_rota(
    entrada: AbrirSerieDeColetaEntrada,
    contexto: Annotated[
        ContextoDaSessao, Depends(exigir_permissao(Operacao.seus_registros_de_coleta, "escreve"))
    ],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> SerieDeColetaSaida:
    """Restrita ao Guerreiro(a) — a recusa de qualquer outro papel é 403,
    devolvida por `abrir_serie_de_coleta` (`RF-08-07`, `RN-08-04`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    desafio = sessao_bd.get(DesafioDeColeta, entrada.desafio_de_coleta_id)
    serie = abrir_serie_de_coleta(
        sessao_bd,
        operador=operador,
        desafio=desafio,
        local_id=entrada.local_id,
    )
    sessao_bd.commit()
    return SerieDeColetaSaida(
        id=serie.id,
        desafio_de_coleta_id=serie.desafio_de_coleta_id,
        coletor_id=serie.coletor_id,
        local_id=serie.local_id,
        cadencia=serie.cadencia.value,
        estado=serie.estado.value,
        aberta_em=serie.aberta_em,
        ultima_medicao_valida_em=serie.ultima_medicao_valida_em,
    )


class EmitirCredencialDeDispositivoEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    serie_de_coleta_id: uuid.UUID
    identificador: str = Field(min_length=1)
    trilha_id: uuid.UUID


class CredencialDeDispositivoEmitidaSaida(BaseModel):
    """O segredo sai uma única vez, aqui (`RN-01-35`)."""

    id: uuid.UUID
    identificador: str
    segredo: str


@roteador.post("/credenciais/dispositivo", status_code=201)
def emitir_credencial_de_dispositivo_rota(
    entrada: EmitirCredencialDeDispositivoEntrada,
    contexto: Annotated[
        ContextoDaSessao,
        Depends(exigir_permissao(Operacao.credencial_de_dispositivo_dos_seus_desafios, "escreve")),
    ],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> CredencialDeDispositivoEmitidaSaida:
    """Restrita a Admin e ao Mestre autor do desafio da série — a posse é
    conferida em `emitir_credencial_de_dispositivo` (`RF-01-67`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    serie = sessao_bd.get(SerieDeColeta, entrada.serie_de_coleta_id)
    credencial, segredo = emitir_credencial_de_dispositivo(
        sessao_bd,
        operador=operador,
        serie=serie,
        identificador=entrada.identificador,
        trilha_id=entrada.trilha_id,
    )
    sessao_bd.commit()
    return CredencialDeDispositivoEmitidaSaida(
        id=credencial.id, identificador=credencial.identificador, segredo=segredo
    )


class RevogarCredencialDeDispositivoEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    motivo: str = Field(min_length=1)


@roteador.delete("/credenciais/dispositivo/{id_da_credencial}", status_code=204)
def revogar_credencial_de_dispositivo_rota(
    id_da_credencial: uuid.UUID,
    entrada: RevogarCredencialDeDispositivoEntrada,
    contexto: Annotated[
        ContextoDaSessao,
        Depends(exigir_permissao(Operacao.credencial_de_dispositivo_dos_seus_desafios, "escreve")),
    ],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> None:
    """Restrita a Admin e ao Mestre autor do desafio da série, a qualquer
    tempo, com motivo e autoria (`RF-01-68`). Não desfaz nada — a
    credencial só autentica (`RN-08-10`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    credencial = sessao_bd.get(Credencial, id_da_credencial)
    revogar_credencial_de_dispositivo(
        sessao_bd, credencial, operador=operador, motivo=entrada.motivo
    )
    sessao_bd.commit()


class RegistroDeColetaSaida(BaseModel):
    id: uuid.UUID
    serie_de_coleta_id: uuid.UUID
    valor: float | None
    unidade: str | None
    origem: str
    situacao: str
    a_conferir: bool
    comunidade_virtual_id: uuid.UUID
    pontos_creditados: int
    pontuou: bool
    momento_do_fato: datetime
    momento_do_registro: datetime


@dataclass(frozen=True)
class ContextoDoRegistro:
    coletor_id: uuid.UUID
    credencial_id: uuid.UUID | None


def _resolver_autenticacao_do_registro(
    request: Request,
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    serie_de_coleta_id: Annotated[uuid.UUID, Form()],
) -> ContextoDoRegistro:
    """Uma rota só, com dois autenticadores (PRD-08 §9): a credencial de
    dispositivo, quando o cabeçalho vem preenchido, ou a sessão de persona,
    como já era. Nunca os dois — o cabeçalho decide (`RN-08-23`)."""
    if request.headers.get(NOME_DO_CABECALHO_DE_DISPOSITIVO):
        contexto_dispositivo = exigir_credencial_de_dispositivo(
            request, sessao_bd, serie_de_coleta_id
        )
        return ContextoDoRegistro(
            coletor_id=contexto_dispositivo.coletor_id,
            credencial_id=contexto_dispositivo.credencial_id,
        )

    contexto_da_sessao = exigir_persona(request, sessao_bd)
    if not conferir_permissao(
        contexto_da_sessao.papel, "escreve", Operacao.seus_registros_de_coleta
    ):
        raise PermissaoNegada()
    return ContextoDoRegistro(coletor_id=contexto_da_sessao.persona_id, credencial_id=None)


@roteador.post("/registros-de-coleta", status_code=201)
def gravar_registro_de_coleta_rota(
    contexto: Annotated[ContextoDoRegistro, Depends(_resolver_autenticacao_do_registro)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    armazenamento: Annotated[PortaDeArmazenamento, Depends(dependencia_de_armazenamento)],
    serie_de_coleta_id: Annotated[uuid.UUID, Form()],
    momento_do_fato: Annotated[DataHoraComFuso, Form()],
    origem: Annotated[str, Form()],
    valor: Annotated[float | None, Form()] = None,
    unidade: Annotated[str | None, Form()] = None,
    midia: Annotated[UploadFile | None, File()] = None,
) -> RegistroDeColetaSaida:
    """Restrita ao coletor da série (`RF-08-08`), pela sessão dele ou pela
    credencial de dispositivo da série (`RF-08-14`); mídia entra por
    _multipart_ porque o tipo `foto`/`video` a exige como o próprio
    registro (`RF-08-21`)."""
    operador = sessao_bd.get(Persona, contexto.coletor_id)
    serie = sessao_bd.get(SerieDeColeta, serie_de_coleta_id)
    conteudo = midia.file.read() if midia is not None else None
    registro = gravar_registro_de_coleta(
        sessao_bd,
        operador=operador,
        serie=serie,
        momento_do_fato=momento_do_fato,
        origem=origem,
        credencial_de_dispositivo_id=contexto.credencial_id,
        valor=valor,
        unidade=unidade,
        midia_conteudo=conteudo,
        armazenamento=armazenamento,
    )
    sessao_bd.commit()
    return RegistroDeColetaSaida(
        id=registro.id,
        serie_de_coleta_id=registro.serie_de_coleta_id,
        valor=registro.valor,
        unidade=registro.unidade,
        origem=registro.origem.value,
        situacao=registro.situacao.value,
        a_conferir=registro.a_conferir,
        comunidade_virtual_id=registro.comunidade_virtual_id,
        pontos_creditados=registro.pontos_creditados,
        pontuou=registro.pontos_creditados > 0,
        momento_do_fato=registro.momento_do_fato,
        momento_do_registro=registro.momento_do_registro,
    )
