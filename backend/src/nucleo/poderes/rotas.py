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
from .modelo import NaturezaDoPoder, PapelDoPoder, Poder, VigenciaDoPoder
from .regra import alterar_poder, cadastrar_poder, desativar_poder

roteador = APIRouter()


class PoderSaida(BaseModel):
    id: uuid.UUID
    nome: str
    descricao: str
    natureza: NaturezaDoPoder
    vigencia: VigenciaDoPoder
    papel: PapelDoPoder | None
    ativo: bool
    tecnico: bool


def _saida(poder: Poder) -> PoderSaida:
    return PoderSaida(
        id=poder.id,
        nome=poder.nome,
        descricao=poder.descricao,
        natureza=poder.natureza,
        vigencia=poder.vigencia,
        papel=poder.papel,
        ativo=poder.ativo,
        tecnico=poder.tecnico,
    )


class CadastrarPoderEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nome: str = Field(min_length=1)
    descricao: str
    natureza: NaturezaDoPoder
    vigencia: VigenciaDoPoder = VigenciaDoPoder.vigente
    papel: PapelDoPoder | None = None
    tecnico: bool = False


@roteador.post("/poderes", status_code=201)
def cadastrar_poder_rota(
    entrada: CadastrarPoderEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> PoderSaida:
    """Restrita ao Admin — a recusa de qualquer outro papel é 403, devolvida
    por `cadastrar_poder` (`RF-02-10`, `RF-01-62`, `RN-01-43`, `RN-01-54`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    poder = cadastrar_poder(
        sessao_bd,
        operador=operador,
        nome=entrada.nome,
        descricao=entrada.descricao,
        natureza=entrada.natureza,
        vigencia=entrada.vigencia,
        papel=entrada.papel,
        tecnico=entrada.tecnico,
    )
    sessao_bd.commit()
    return _saida(poder)


@roteador.get("/poderes", response_model=PaginaDeResultado[PoderSaida])
def listar_poderes_rota(
    parametros: Annotated[ParametrosDeListagem, Depends(contrato_de_listagem())],
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> PaginaDeResultado[PoderSaida]:
    """Aberta a qualquer persona em sessão, sem filtro por comunidade — o
    poder é bem comum da plataforma. Ao contrário da vitrine pública, a
    listagem da gestão inclui o poder inativo (`RF-02-10`, `RF-01-28`)."""
    consulta = sessao_bd.query(Poder)

    if parametros.cursor:
        posicao = decodificar_cursor(parametros.cursor)
        try:
            nome_cursor = posicao["nome"]
            id_cursor = uuid.UUID(posicao["id"])
        except (KeyError, ValueError) as exc:
            raise ErroDeValidacao(mensagem="Cursor de paginação inválido.", campo="cursor") from exc
        consulta = consulta.filter(tuple_(Poder.nome, Poder.id) > (nome_cursor, id_cursor))

    consulta = consulta.order_by(Poder.nome, Poder.id).limit(parametros.tamanho + 1)
    poderes = consulta.all()

    proximo_cursor = None
    if len(poderes) > parametros.tamanho:
        poderes = poderes[: parametros.tamanho]
        ultimo = poderes[-1]
        proximo_cursor = codificar_cursor({"nome": ultimo.nome, "id": str(ultimo.id)})

    return PaginaDeResultado(
        itens=[_saida(poder) for poder in poderes],
        proximo_cursor=proximo_cursor,
    )


class AlterarPoderEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nome: str | None = None
    descricao: str | None = None
    vigencia: VigenciaDoPoder | None = None
    tecnico: bool | None = None


@roteador.put("/poderes/{id_do_poder}")
def alterar_poder_rota(
    id_do_poder: uuid.UUID,
    entrada: AlterarPoderEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> PoderSaida:
    """Restrita ao Admin — natureza e papel ficam fora do corpo, porque
    `alterar_poder` não os admite; a marca de técnico entra (`RF-02-10`,
    `RN-01-43`, `RN-01-54`, `RN-09-34`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    poder = sessao_bd.get(Poder, id_do_poder)
    poder = alterar_poder(
        sessao_bd,
        poder,
        operador=operador,
        nome=entrada.nome,
        descricao=entrada.descricao,
        vigencia=entrada.vigencia,
        tecnico=entrada.tecnico,
    )
    sessao_bd.commit()
    return _saida(poder)


@roteador.post("/poderes/{id_do_poder}/desativacao")
def desativar_poder_rota(
    id_do_poder: uuid.UUID,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> PoderSaida:
    """Restrita ao Admin — retira o poder da escolha de novas trilhas e da
    leitura pública, sem desfazer o vínculo das trilhas já criadas
    (`RF-02-10`, `RF-01-62`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    poder = sessao_bd.get(Poder, id_do_poder)
    poder = desativar_poder(sessao_bd, poder, operador=operador)
    sessao_bd.commit()
    return _saida(poder)
