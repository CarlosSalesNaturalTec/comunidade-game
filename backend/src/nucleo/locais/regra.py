import uuid
from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import tuple_
from sqlalchemy.orm import Session

from ..erros import ErroDeValidacao, PermissaoNegada
from ..paginacao import PaginaDeResultado, codificar_cursor, decodificar_cursor
from ..personas.modelo import Papel, Persona
from .modelo import ORDEM_DOS_NIVEIS, Local, NivelDoLocal


class LocalSaida(BaseModel):
    id: uuid.UUID
    comunidade_virtual_id: uuid.UUID
    nivel: str
    rotulo: str
    local_pai_id: uuid.UUID | None


def cadastrar_local(
    sessao: Session,
    *,
    operador: Persona,
    comunidade_id: uuid.UUID | None,
    nivel: str | None,
    rotulo: str | None,
    local_pai_id: uuid.UUID | None,
) -> Local:
    """Só Admin cadastra local, a única origem nesta entrega (`RF-08-04`,
    `RN-08-18`). O pai precisa ser do nível imediatamente acima e da mesma
    comunidade; só o nível `comunidade` dispensa pai.
    """
    if operador.papel != Papel.admin:
        raise PermissaoNegada(mensagem="Só o Admin cadastra local.")
    if comunidade_id is None:
        raise ErroDeValidacao(mensagem="Local exige uma comunidade.", campo="comunidade_id")
    if not rotulo or not rotulo.strip():
        raise ErroDeValidacao(mensagem="Local exige rótulo.", campo="rotulo")

    try:
        nivel_valido = NivelDoLocal(nivel)
    except ValueError as exc:
        raise ErroDeValidacao(mensagem="Nível fora dos valores previstos.", campo="nivel") from exc

    indice = ORDEM_DOS_NIVEIS.index(nivel_valido)
    if nivel_valido == NivelDoLocal.comunidade:
        if local_pai_id is not None:
            raise ErroDeValidacao(
                mensagem="O nível 'comunidade' não tem local pai.", campo="local_pai_id"
            )
    else:
        if local_pai_id is None:
            raise ErroDeValidacao(mensagem="Local exige o local pai.", campo="local_pai_id")

        pai = sessao.get(Local, local_pai_id)
        if pai is None:
            raise ErroDeValidacao(mensagem="Local pai não encontrado.", campo="local_pai_id")
        if pai.comunidade_virtual_id != comunidade_id:
            raise ErroDeValidacao(
                mensagem="Local pai precisa ser da mesma comunidade.", campo="local_pai_id"
            )
        nivel_esperado_do_pai = ORDEM_DOS_NIVEIS[indice - 1]
        if pai.nivel != nivel_esperado_do_pai:
            raise ErroDeValidacao(
                mensagem=f"O nível imediatamente acima de '{nivel_valido.value}' é "
                f"'{nivel_esperado_do_pai.value}'.",
                campo="local_pai_id",
            )

    local = Local(
        comunidade_virtual_id=comunidade_id,
        nivel=nivel_valido,
        rotulo=rotulo,
        local_pai_id=local_pai_id,
    )
    sessao.add(local)
    sessao.flush()
    return local


def paginar_locais(
    sessao: Session,
    *,
    comunidade_id: uuid.UUID,
    cursor: str | None,
    tamanho: int,
) -> PaginaDeResultado[LocalSaida]:
    """Listagem paginada, sempre filtrada por comunidade (`RF-01-18`,
    `RF-01-28`) — nenhum local de outra comunidade entra na página."""
    consulta = sessao.query(Local).filter(Local.comunidade_virtual_id == comunidade_id)

    if cursor:
        posicao = decodificar_cursor(cursor)
        try:
            criado_em_cursor = datetime.fromisoformat(posicao["criado_em"])
            id_cursor = uuid.UUID(posicao["id"])
        except (KeyError, ValueError) as exc:
            raise ErroDeValidacao(mensagem="Cursor de paginação inválido.", campo="cursor") from exc
        consulta = consulta.filter(
            tuple_(Local.criado_em, Local.id) > (criado_em_cursor, id_cursor)
        )

    consulta = consulta.order_by(Local.criado_em, Local.id).limit(tamanho + 1)
    locais = consulta.all()

    proximo_cursor = None
    if len(locais) > tamanho:
        locais = locais[:tamanho]
        ultimo = locais[-1]
        proximo_cursor = codificar_cursor(
            {"criado_em": ultimo.criado_em.isoformat(), "id": str(ultimo.id)}
        )

    itens = [
        LocalSaida(
            id=local.id,
            comunidade_virtual_id=local.comunidade_virtual_id,
            nivel=local.nivel.value,
            rotulo=local.rotulo,
            local_pai_id=local.local_pai_id,
        )
        for local in locais
    ]
    return PaginaDeResultado(itens=itens, proximo_cursor=proximo_cursor)
