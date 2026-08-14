import uuid
from collections.abc import Iterable
from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import tuple_
from sqlalchemy.orm import Session

from ..comunidades.regra import filtrar_personas_por_comunidade
from ..consentimentos.regra import condicao_de_autorizacao_vigente
from ..erros import ErroDeValidacao
from ..paginacao import PaginaDeResultado, codificar_cursor, decodificar_cursor
from ..personas.modelo import Nick, Papel, Persona


class AvatarENickSaida(BaseModel):
    """A projeção pública, única: avatar e nick, e nada de pessoal
    (`RN-01-10`, `RN-01-11`, design — Decisions). Toda saída pública desta
    change — vitrine e jogos — passa por aqui, nunca por seleção de campos
    montada rota a rota.
    """

    avatar: str | None
    nick: str


def buscar_avatares_e_nicks(
    sessao: Session, personas_ids: Iterable[uuid.UUID]
) -> dict[uuid.UUID, AvatarENickSaida]:
    """Um só round-trip para um conjunto de personas — evita N+1 ao montar a
    autoria creditada de uma listagem (design — Decisions)."""
    ids = list(personas_ids)
    if not ids:
        return {}
    linhas = (
        sessao.query(Persona.id, Persona.avatar, Nick.valor)
        .join(Nick, Nick.persona_id == Persona.id)
        .filter(Persona.id.in_(ids))
        .all()
    )
    return {
        persona_id: AvatarENickSaida(avatar=avatar, nick=nick)
        for persona_id, avatar, nick in linhas
    }


def buscar_persona_guerreiro_publica_por_nick(sessao: Session, nick: str) -> Persona | None:
    """Resolve nick e vigência de autorização **na mesma consulta**: não há
    desvio no código que possa vazar a diferença entre nick inexistente e
    nick sem autorização (`RF-01-33`, `RF-01-34`, `RN-01-22`, design —
    Decisions). Reaproveitado pela vitrine e pelo contrato dos jogos —
    mesmo portão (invariante 8 do documento 99 §6).
    """
    return (
        sessao.query(Persona)
        .join(Nick, Nick.persona_id == Persona.id)
        .filter(
            Nick.valor == nick,
            Persona.papel == Papel.guerreiro,
            condicao_de_autorizacao_vigente(sessao, Persona.id),
        )
        .first()
    )


def _consulta_de_guerreiros_publicos(sessao: Session, *, comunidade_id: uuid.UUID | None):
    """A base comum de toda listagem de Guerreiros e Guerreiras em público —
    vitrine e elenco dos jogos (invariante 8 do documento 99 §6): o portão
    da divulgação entra na consulta, não em pós-filtro (design —
    Decisions)."""
    consulta = (
        sessao.query(Persona, Nick.valor)
        .join(Nick, Nick.persona_id == Persona.id)
        .filter(
            Persona.papel == Papel.guerreiro,
            condicao_de_autorizacao_vigente(sessao, Persona.id),
        )
    )
    if comunidade_id is not None:
        consulta = filtrar_personas_por_comunidade(consulta, comunidade_id)
    return consulta


def paginar_guerreiros_publicos(
    sessao: Session,
    *,
    comunidade_id: uuid.UUID | None,
    cursor: str | None,
    tamanho: int,
) -> PaginaDeResultado[AvatarENickSaida]:
    """Paginação por cursor sobre `(criada_em, id)`, no mesmo contrato das
    demais listagens (`RF-01-28`) — o portão da divulgação já filtrou o
    conjunto antes de paginar, de modo que a página nunca fica curta por
    exclusão de quem não autorizou (design — Decisions)."""
    consulta = _consulta_de_guerreiros_publicos(sessao, comunidade_id=comunidade_id)

    if cursor:
        posicao = decodificar_cursor(cursor)
        try:
            criada_em_cursor = datetime.fromisoformat(posicao["criada_em"])
            id_cursor = uuid.UUID(posicao["id"])
        except (KeyError, ValueError) as exc:
            raise ErroDeValidacao(mensagem="Cursor de paginação inválido.", campo="cursor") from exc
        consulta = consulta.filter(
            tuple_(Persona.criada_em, Persona.id) > (criada_em_cursor, id_cursor)
        )

    consulta = consulta.order_by(Persona.criada_em, Persona.id).limit(tamanho + 1)
    linhas = consulta.all()

    proximo_cursor = None
    if len(linhas) > tamanho:
        linhas = linhas[:tamanho]
        ultima_persona, _ = linhas[-1]
        proximo_cursor = codificar_cursor(
            {"criada_em": ultima_persona.criada_em.isoformat(), "id": str(ultima_persona.id)}
        )

    itens = [AvatarENickSaida(avatar=persona.avatar, nick=nick) for persona, nick in linhas]
    return PaginaDeResultado(itens=itens, proximo_cursor=proximo_cursor)
