import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..autenticacao import ContextoDaSessao, exigir_persona
from ..banco import obter_sessao
from ..comunidades.modelo import VinculoJogador
from ..erros import ErroDeValidacao, PermissaoNegada
from ..paginacao import (
    ParametrosDeListagem,
    codificar_cursor,
    contrato_de_listagem,
    decodificar_cursor,
)
from ..personas.modelo import Papel
from .regra import consulta_de_ranking

roteador = APIRouter()

_FILTROS_DO_RANKING_DA_TURMA = frozenset({"trilha", "poder"})


def _analisar_uuid(valor: str | None, campo: str) -> uuid.UUID | None:
    if not valor:
        return None
    try:
        return uuid.UUID(valor)
    except ValueError as exc:
        raise ErroDeValidacao(
            mensagem=f"Filtro '{campo}' precisa ser um identificador válido.", campo=campo
        ) from exc


class ItemDoRankingDaTurmaSaida(BaseModel):
    avatar: str | None
    nick: str
    posicao: int
    pontos_regulares: int


class RankingDaTurmaSaida(BaseModel):
    itens: list[ItemDoRankingDaTurmaSaida]
    proximo_cursor: str | None
    minha_posicao: ItemDoRankingDaTurmaSaida


@roteador.get("/rankings/{comunidade}")
def ranking_da_turma_rota(
    comunidade: uuid.UUID,
    parametros: Annotated[
        ParametrosDeListagem, Depends(contrato_de_listagem(_FILTROS_DO_RANKING_DA_TURMA))
    ],
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> RankingDaTurmaSaida:
    """Ranking logado da turma inteira, restrito ao Guerreiro(a) da própria
    comunidade — a exceção declarada à divulgação, porque a tela é logada e
    a comunidade do segmento é sempre conferida contra o vínculo vigente de
    quem pergunta (`RF-05-52`, `RF-05-53`, `RF-05-84`, `RN-05-16`,
    `RN-05-21`)."""
    if contexto.papel != Papel.guerreiro:
        raise PermissaoNegada(mensagem="Só o Guerreiro(a) lê o ranking logado da turma.")

    vinculo = (
        sessao_bd.query(VinculoJogador)
        .filter_by(guerreiro_id=contexto.persona_id, data_fim=None)
        .first()
    )
    if vinculo is None or vinculo.comunidade_virtual_id != comunidade:
        raise PermissaoNegada(mensagem="Só a própria comunidade é consultada por esta rota.")

    trilha_id = _analisar_uuid(parametros.filtros.get("trilha"), "trilha")
    poder_id = _analisar_uuid(parametros.filtros.get("poder"), "poder")
    if trilha_id is not None and poder_id is not None:
        raise ErroDeValidacao(
            mensagem="Filtre por trilha ou por poder, nunca os dois.", campo="poder"
        )

    consulta = consulta_de_ranking(
        sessao_bd,
        exigir_divulgacao=False,
        comunidade_id=comunidade,
        trilha_id=trilha_id,
        poder_id=poder_id,
    )
    subquery = consulta.subquery()
    paginada = sessao_bd.query(*subquery.c).order_by(subquery.c.posicao)

    if parametros.cursor:
        posicao_do_cursor = decodificar_cursor(parametros.cursor)
        try:
            ultima_posicao = int(posicao_do_cursor["posicao"])
        except (KeyError, ValueError) as exc:
            raise ErroDeValidacao(mensagem="Cursor de paginação inválido.", campo="cursor") from exc
        paginada = paginada.filter(subquery.c.posicao > ultima_posicao)

    linhas = paginada.limit(parametros.tamanho + 1).all()
    proximo_cursor = None
    if len(linhas) > parametros.tamanho:
        linhas = linhas[: parametros.tamanho]
        proximo_cursor = codificar_cursor({"posicao": linhas[-1].posicao})

    # A própria posição sempre existe: todo Guerreiro(a) em sessão tem nick e
    # vínculo vigente na comunidade que acabou de ser conferida acima
    # (`RN-05-16`).
    minha_linha = (
        sessao_bd.query(*subquery.c).filter(subquery.c.persona_id == contexto.persona_id).first()
    )

    itens = [
        ItemDoRankingDaTurmaSaida(
            avatar=linha.avatar,
            nick=linha.nick,
            posicao=linha.posicao,
            pontos_regulares=linha.total,
        )
        for linha in linhas
    ]
    minha_posicao = ItemDoRankingDaTurmaSaida(
        avatar=minha_linha.avatar,
        nick=minha_linha.nick,
        posicao=minha_linha.posicao,
        pontos_regulares=minha_linha.total,
    )
    return RankingDaTurmaSaida(
        itens=itens, proximo_cursor=proximo_cursor, minha_posicao=minha_posicao
    )
