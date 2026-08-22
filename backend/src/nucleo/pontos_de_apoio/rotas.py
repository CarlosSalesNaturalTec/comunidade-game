import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import tuple_
from sqlalchemy.orm import Session

from ..autenticacao import ContextoDaSessao, exigir_persona
from ..banco import obter_sessao
from ..erros import ErroDeValidacao
from ..paginacao import (
    PaginaDeResultado,
    ParametrosDeListagem,
    codificar_cursor,
    contrato_de_listagem,
    decodificar_cursor,
)
from ..personas.modelo import Persona
from .modelo import PontoDeApoio
from .regra import (
    cadastrar_ponto_de_apoio,
    desativar_ponto_de_apoio,
    designar_responsavel,
    escopo_de_comunidade_da_leitura,
    reativar_ponto_de_apoio,
)

roteador = APIRouter()


class PontoDeApoioSaida(BaseModel):
    id: uuid.UUID
    nome: str
    comunidade_virtual_id: uuid.UUID
    responsavel_id: uuid.UUID | None
    ativo: bool


def _saida(ponto_de_apoio: PontoDeApoio) -> PontoDeApoioSaida:
    return PontoDeApoioSaida(
        id=ponto_de_apoio.id,
        nome=ponto_de_apoio.nome,
        comunidade_virtual_id=ponto_de_apoio.comunidade_virtual_id,
        responsavel_id=ponto_de_apoio.responsavel_id,
        ativo=ponto_de_apoio.ativo,
    )


class CadastrarPontoDeApoioEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nome: str = Field(min_length=1)
    comunidade_id: uuid.UUID


@roteador.post("/pontos-de-apoio", status_code=201)
def cadastrar_ponto_de_apoio_rota(
    entrada: CadastrarPontoDeApoioEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> PontoDeApoioSaida:
    """Restrita ao Admin — a recusa de qualquer outro papel é 403, devolvida
    por `cadastrar_ponto_de_apoio` (`RF-07-47`, `RN-07-33`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    ponto_de_apoio = cadastrar_ponto_de_apoio(
        sessao_bd,
        operador=operador,
        nome=entrada.nome,
        comunidade_id=entrada.comunidade_id,
    )
    sessao_bd.commit()
    return _saida(ponto_de_apoio)


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


@roteador.get("/pontos-de-apoio", response_model=PaginaDeResultado[PontoDeApoioSaida])
def listar_pontos_de_apoio_rota(
    parametros: Annotated[ParametrosDeListagem, Depends(contrato_de_listagem())],
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> PaginaDeResultado[PontoDeApoioSaida]:
    """Restrita à gestão — Admin lê qualquer comunidade, sempre declarada; o
    Mestre lê só a do seu vínculo vigente, e sem vínculo lê lista vazia
    (`RF-07-47`, `RF-01-28`, `RF-01-18`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    comunidade_id = _analisar_comunidade(parametros.filtros.get("comunidade"))
    alvo_id = escopo_de_comunidade_da_leitura(
        operador=operador, comunidade_virtual_id=comunidade_id
    )
    if alvo_id is None:
        return PaginaDeResultado(itens=[], proximo_cursor=None)

    consulta = sessao_bd.query(PontoDeApoio).filter(PontoDeApoio.comunidade_virtual_id == alvo_id)

    if parametros.cursor:
        posicao = decodificar_cursor(parametros.cursor)
        try:
            nome_cursor = posicao["nome"]
            id_cursor = uuid.UUID(posicao["id"])
        except (KeyError, ValueError) as exc:
            raise ErroDeValidacao(mensagem="Cursor de paginação inválido.", campo="cursor") from exc
        consulta = consulta.filter(
            tuple_(PontoDeApoio.nome, PontoDeApoio.id) > (nome_cursor, id_cursor)
        )

    consulta = consulta.order_by(PontoDeApoio.nome, PontoDeApoio.id).limit(parametros.tamanho + 1)
    pontos_de_apoio = consulta.all()

    proximo_cursor = None
    if len(pontos_de_apoio) > parametros.tamanho:
        pontos_de_apoio = pontos_de_apoio[: parametros.tamanho]
        ultimo = pontos_de_apoio[-1]
        proximo_cursor = codificar_cursor({"nome": ultimo.nome, "id": str(ultimo.id)})

    return PaginaDeResultado(
        itens=[_saida(ponto_de_apoio) for ponto_de_apoio in pontos_de_apoio],
        proximo_cursor=proximo_cursor,
    )


class DesignarResponsavelEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    responsavel_id: uuid.UUID


@roteador.put("/pontos-de-apoio/{id_do_ponto_de_apoio}/responsavel")
def designar_responsavel_rota(
    id_do_ponto_de_apoio: uuid.UUID,
    entrada: DesignarResponsavelEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> PontoDeApoioSaida:
    """Restrita ao Admin — designa ou troca o responsável pelo acervo, a
    qualquer tempo, com 422 para papel fora de Admin, Mestre ou Apoiador
    (`RF-07-49`, `RN-07-34`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    ponto_de_apoio = sessao_bd.get(PontoDeApoio, id_do_ponto_de_apoio)
    responsavel = sessao_bd.get(Persona, entrada.responsavel_id)
    ponto_de_apoio = designar_responsavel(
        sessao_bd,
        ponto_de_apoio,
        operador=operador,
        responsavel=responsavel,
    )
    sessao_bd.commit()
    return _saida(ponto_de_apoio)


class MudarSituacaoDoPontoDeApoioEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    motivo: str = Field(min_length=1)


@roteador.post("/pontos-de-apoio/{id_do_ponto_de_apoio}/desativacao")
def desativar_ponto_de_apoio_rota(
    id_do_ponto_de_apoio: uuid.UUID,
    entrada: MudarSituacaoDoPontoDeApoioEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> PontoDeApoioSaida:
    """Restrita ao Admin — bloqueada por aula futura e por saldo
    remanescente, cada bloqueio dizendo o que prende o espaço (`RF-07-47`,
    `RN-07-01`, `RN-07-15`, `RN-07-33`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    ponto_de_apoio = sessao_bd.get(PontoDeApoio, id_do_ponto_de_apoio)
    ponto_de_apoio = desativar_ponto_de_apoio(
        sessao_bd, ponto_de_apoio, operador=operador, motivo=entrada.motivo
    )
    sessao_bd.commit()
    return _saida(ponto_de_apoio)


@roteador.post("/pontos-de-apoio/{id_do_ponto_de_apoio}/reativacao")
def reativar_ponto_de_apoio_rota(
    id_do_ponto_de_apoio: uuid.UUID,
    entrada: MudarSituacaoDoPontoDeApoioEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> PontoDeApoioSaida:
    """Restrita ao Admin (`RF-07-47`, `RN-07-33`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    ponto_de_apoio = sessao_bd.get(PontoDeApoio, id_do_ponto_de_apoio)
    ponto_de_apoio = reativar_ponto_de_apoio(
        sessao_bd, ponto_de_apoio, operador=operador, motivo=entrada.motivo
    )
    sessao_bd.commit()
    return _saida(ponto_de_apoio)
