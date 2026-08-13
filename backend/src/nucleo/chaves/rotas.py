import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import tuple_
from sqlalchemy.orm import Session

from ..autenticacao import ContextoDaSessao
from ..banco import obter_sessao
from ..configuracao import Configuracao, obter_configuracao
from ..erros import ErroDeValidacao, NaoEncontrado
from ..fila.modelo import SolicitacaoDeChave
from ..paginacao import (
    PaginaDeResultado,
    ParametrosDeListagem,
    codificar_cursor,
    contrato_de_listagem,
    decodificar_cursor,
)
from ..permissoes import Operacao, exigir_permissao
from .modelo import ChaveDeAplicacao
from .regra import aplicar_decurso_se_vencido, apresentar_url, emitir_chave_de_terceiro, revogar

roteador = APIRouter()


class EmitirChaveEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    solicitacao_id: uuid.UUID


class ChaveEmitidaSaida(BaseModel):
    """O segredo — a chave completa, pronta para o cabeçalho
    `X-Chave-Aplicacao` — sai uma única vez, aqui (`RN-01-35`)."""

    id: uuid.UUID
    segredo: str


@roteador.post("/chaves", status_code=201)
def emitir_chave_rota(
    entrada: EmitirChaveEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_permissao(Operacao.tudo, "escreve"))],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    configuracao: Annotated[Configuracao, Depends(obter_configuracao)],
) -> ChaveEmitidaSaida:
    """Restrita a Admin, sobre solicitação aprovada (`RF-01-50`)."""
    solicitacao = sessao_bd.get(SolicitacaoDeChave, entrada.solicitacao_id)
    if solicitacao is None:
        raise NaoEncontrado(mensagem="Solicitação de chave não encontrada.")

    chave, segredo = emitir_chave_de_terceiro(
        sessao_bd,
        solicitacao,
        emitida_por=str(contexto.persona_id),
        configuracao=configuracao,
    )
    sessao_bd.commit()
    return ChaveEmitidaSaida(id=chave.id, segredo=segredo)


class ApresentarUrlEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    url: str = Field(min_length=1)


@roteador.post("/chaves/{id_da_chave}/url", status_code=204)
def apresentar_url_rota(
    id_da_chave: uuid.UUID,
    entrada: ApresentarUrlEntrada,
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> None:
    """Pública, sem credencial de persona (`RF-01-51`, `RN-01-33`): quem
    prova a titularidade é o identificador da chave, entregue só na
    emissão."""
    apresentar_url(sessao_bd, id_da_chave, entrada.url)
    sessao_bd.commit()


class RevogarChaveEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    motivo: str = Field(min_length=1)


@roteador.delete("/chaves/{id_da_chave}", status_code=204)
def revogar_chave_rota(
    id_da_chave: uuid.UUID,
    entrada: RevogarChaveEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_permissao(Operacao.tudo, "escreve"))],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> None:
    """Restrita a Admin, a qualquer tempo, com motivo e autoria
    (`RF-01-53`). Não desfaz nada — a chave só lê (`RN-01-36`)."""
    chave = sessao_bd.get(ChaveDeAplicacao, id_da_chave)
    if chave is None:
        raise NaoEncontrado(mensagem="Chave de aplicação não encontrada.")

    revogar(sessao_bd, chave, motivo=entrada.motivo, revogada_por=str(contexto.persona_id))
    sessao_bd.commit()


class ChaveDeAplicacaoSaida(BaseModel):
    """Nunca traz o segredo nem o resumo criptográfico (`RN-01-35`)."""

    id: uuid.UUID
    aplicacao: str
    natureza: str
    ambiente: str
    prazo_de_apresentacao: datetime | None
    url_apresentada: str | None
    situacao: str


@roteador.get("/chaves", response_model=PaginaDeResultado[ChaveDeAplicacaoSaida])
def listar_chaves_rota(
    parametros: Annotated[ParametrosDeListagem, Depends(contrato_de_listagem())],
    contexto: Annotated[ContextoDaSessao, Depends(exigir_permissao(Operacao.tudo, "le"))],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> PaginaDeResultado[ChaveDeAplicacaoSaida]:
    """Restrita a Admin (`RF-01-16`). O vencimento se aplica também aqui, para
    que a chave vencida apareça revogada mesmo que nunca mais chame o núcleo
    (`RF-01-52`, design — Decisions)."""
    consulta = sessao_bd.query(ChaveDeAplicacao)

    if parametros.cursor:
        posicao = decodificar_cursor(parametros.cursor)
        try:
            emitida_em_cursor = datetime.fromisoformat(posicao["emitida_em"])
            id_cursor = uuid.UUID(posicao["id"])
        except (KeyError, ValueError) as exc:
            raise ErroDeValidacao(mensagem="Cursor de paginação inválido.", campo="cursor") from exc
        consulta = consulta.filter(
            tuple_(ChaveDeAplicacao.emitida_em, ChaveDeAplicacao.id)
            > (emitida_em_cursor, id_cursor)
        )

    consulta = consulta.order_by(ChaveDeAplicacao.emitida_em, ChaveDeAplicacao.id)
    registros = consulta.limit(parametros.tamanho + 1).all()

    proximo_cursor = None
    if len(registros) > parametros.tamanho:
        registros = registros[: parametros.tamanho]
        ultimo = registros[-1]
        proximo_cursor = codificar_cursor(
            {"emitida_em": ultimo.emitida_em.isoformat(), "id": str(ultimo.id)}
        )

    houve_transicao = False
    for registro in registros:
        if aplicar_decurso_se_vencido(registro):
            houve_transicao = True
    if houve_transicao:
        sessao_bd.commit()

    return PaginaDeResultado(
        itens=[
            ChaveDeAplicacaoSaida(
                id=registro.id,
                aplicacao=registro.aplicacao,
                natureza=registro.natureza.value,
                ambiente=registro.ambiente,
                prazo_de_apresentacao=registro.prazo_de_apresentacao,
                url_apresentada=registro.url_apresentada,
                situacao=registro.situacao.value,
            )
            for registro in registros
        ],
        proximo_cursor=proximo_cursor,
    )
