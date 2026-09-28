import uuid
from collections.abc import Iterable
from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import and_, tuple_
from sqlalchemy.orm import Session, aliased

from ..comunidades.regra import filtrar_personas_por_comunidade
from ..consentimentos.regra import condicao_de_autorizacao_vigente
from ..criacoes_originais.modelo import CriacaoOriginal, SituacaoDaCriacaoOriginal
from ..equipes.modelo import IntegranteDaEquipe
from ..erros import ErroDeValidacao
from ..paginacao import PaginaDeResultado, codificar_cursor, decodificar_cursor
from ..personas.modelo import Nick, Papel, Persona
from ..poderes.modelo import Poder
from ..pontuacao.modelo import Badge, Nivel
from ..pontuacao.regra import consulta_de_ranking
from ..trilhas.modelo import Trilha


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


def _paginar_personas_publicas(
    sessao: Session,
    *,
    comunidade_id: uuid.UUID | None,
    cursor: str | None,
    tamanho: int,
) -> tuple[list[tuple[Persona, str]], str | None]:
    """Paginação por cursor sobre `(criada_em, id)`, no mesmo contrato das
    demais listagens (`RF-01-28`) — o portão da divulgação já filtrou o
    conjunto antes de paginar, de modo que a página nunca fica curta por
    exclusão de quem não autorizou (design — Decisions). Devolve as linhas
    cruas para que cada superfície projete o que lhe cabe: o elenco dos
    jogos, avatar e nick; a vitrine, a carta inteira."""
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

    return linhas, proximo_cursor


def paginar_guerreiros_publicos(
    sessao: Session,
    *,
    comunidade_id: uuid.UUID | None,
    cursor: str | None,
    tamanho: int,
) -> PaginaDeResultado[AvatarENickSaida]:
    """A projeção **mínima** — avatar e nick —, que o elenco dos jogos usa e
    que esta change não muda (invariante 8 do documento 99 §6)."""
    linhas, proximo_cursor = _paginar_personas_publicas(
        sessao, comunidade_id=comunidade_id, cursor=cursor, tamanho=tamanho
    )
    itens = [AvatarENickSaida(avatar=persona.avatar, nick=nick) for persona, nick in linhas]
    return PaginaDeResultado(itens=itens, proximo_cursor=proximo_cursor)


class BadgeNaCartaSaida(BaseModel):
    """A família do badge e o poder a que ele pertence, **já resolvidos**: a
    carta não devolve `trilha_id` cru para o cliente cruzar com o catálogo
    de poderes (design — decisão 2)."""

    familia: str
    poder: str | None


class PoderComNivelSaida(BaseModel):
    poder: str
    nivel: int


class CriacaoNaCartaSaida(BaseModel):
    trilha: str
    validada_em: datetime


class CartaPublicaDeGuerreiroSaida(AvatarENickSaida):
    """A variante Guerreiro(a) do documento 11 §8.2 inteira — avatar, nick,
    badges, poderes com níveis, desempenho e criações originais —, a mesma
    no card e na página, e sem nada de pessoal (`RF-03-03`, `RF-03-05`,
    `RF-03-06`, `RN-01-10`, `RN-01-11`, decisão do fundador, 2026-09-28).
    """

    badges: list[BadgeNaCartaSaida]
    poderes: list[PoderComNivelSaida]
    pontos_regulares: int
    posicao_no_ranking: int
    criacoes: list[CriacaoNaCartaSaida]


def condicoes_de_criacao_publica(sessao: Session):
    """O portão da criação original em público: validada e com **todos** os
    creditados autorizados (`RN-01-13`, `RN-03-02`). Uma regra só para o
    portfólio e para a carta (design — decisão 4)."""
    tem_integrante_nao_autorizado = (
        sessao.query(IntegranteDaEquipe.id)
        .filter(IntegranteDaEquipe.equipe_id == CriacaoOriginal.equipe_id)
        .filter(~condicao_de_autorizacao_vigente(sessao, IntegranteDaEquipe.persona_id))
        .exists()
    )
    guerreiro_individual_nao_autorizado = and_(
        CriacaoOriginal.guerreiro_id.is_not(None),
        ~condicao_de_autorizacao_vigente(sessao, CriacaoOriginal.guerreiro_id),
    )
    return (
        CriacaoOriginal.situacao == SituacaoDaCriacaoOriginal.validada,
        ~tem_integrante_nao_autorizado,
        ~guerreiro_individual_nao_autorizado,
    )


def nomes_de_trilha(sessao: Session, trilha_ids: Iterable[uuid.UUID]) -> dict[uuid.UUID, str]:
    """Um só round-trip para o nome das trilhas de um conjunto — o portfólio
    público exibe a trilha, não o identificador dela (`RF-03-08`)."""
    ids = list(trilha_ids)
    if not ids:
        return {}
    return dict(sessao.query(Trilha.id, Trilha.nome).filter(Trilha.id.in_(ids)).all())


def _nomes_de_poder(
    sessao: Session,
    *,
    trilha_ids: Iterable[uuid.UUID],
    poder_ids: Iterable[uuid.UUID],
) -> tuple[dict[uuid.UUID, str], dict[uuid.UUID, str]]:
    """O nome do poder por trilha e por poder, em duas consultas, para que
    nível e badge saiam nomeados da própria projeção (design — decisão 2)."""
    por_trilha: dict[uuid.UUID, str] = {}
    trilhas = list(trilha_ids)
    if trilhas:
        por_trilha = dict(
            sessao.query(Trilha.id, Poder.nome)
            .join(Poder, Poder.id == Trilha.poder_id)
            .filter(Trilha.id.in_(trilhas))
            .all()
        )
    por_poder: dict[uuid.UUID, str] = {}
    poderes = list(poder_ids)
    if poderes:
        por_poder = dict(sessao.query(Poder.id, Poder.nome).filter(Poder.id.in_(poderes)).all())
    return por_trilha, por_poder


def _desempenho_publico(
    sessao: Session,
    personas_ids: Iterable[uuid.UUID],
    *,
    comunidade_id: uuid.UUID | None,
) -> dict[uuid.UUID, tuple[int, int]]:
    """Pontos regulares e posição, da **mesma** derivação que o
    `/vitrine/rankings` usa, para que carta e ranking nunca discordem
    (`RF-03-05`, `RF-03-09`, design — decisão 3). A posição é calculada
    sobre o ranking inteiro e só depois recortada pelos identificadores da
    página."""
    ids = list(personas_ids)
    if not ids:
        return {}
    ranking = consulta_de_ranking(
        sessao, exigir_divulgacao=True, comunidade_id=comunidade_id
    ).subquery()
    linhas = (
        sessao.query(ranking.c.persona_id, ranking.c.total, ranking.c.posicao)
        .filter(ranking.c.persona_id.in_(ids))
        .all()
    )
    return {persona_id: (int(total), int(posicao)) for persona_id, total, posicao in linhas}


def _criacoes_na_carta(
    sessao: Session, personas_ids: Iterable[uuid.UUID]
) -> dict[uuid.UUID, list[CriacaoNaCartaSaida]]:
    """As criações originais públicas creditadas a cada Guerreiro(a) da
    página, individuais e em equipe, em duas consultas."""
    ids = list(personas_ids)
    if not ids:
        return {}
    condicoes = condicoes_de_criacao_publica(sessao)

    creditos: list[tuple[uuid.UUID, CriacaoOriginal]] = [
        (criacao.guerreiro_id, criacao)
        for criacao in sessao.query(CriacaoOriginal)
        .filter(*condicoes, CriacaoOriginal.guerreiro_id.in_(ids))
        .all()
    ]
    # O portão já consulta `IntegranteDaEquipe`; juntar a tabela de novo sem
    # apelido faria o SQLAlchemy correlacionar a subconsulta e a deixar sem
    # `FROM`. O apelido mantém as duas leituras independentes.
    integrante = aliased(IntegranteDaEquipe)
    creditos += [
        (persona_id, criacao)
        for criacao, persona_id in sessao.query(CriacaoOriginal, integrante.persona_id)
        .join(integrante, integrante.equipe_id == CriacaoOriginal.equipe_id)
        .filter(*condicoes, integrante.persona_id.in_(ids))
        .all()
    ]

    trilhas = nomes_de_trilha(sessao, {criacao.trilha_id for _, criacao in creditos})
    por_guerreiro: dict[uuid.UUID, list[CriacaoNaCartaSaida]] = {}
    for persona_id, criacao in creditos:
        if criacao.validado_em is None:
            continue
        por_guerreiro.setdefault(persona_id, []).append(
            CriacaoNaCartaSaida(
                trilha=trilhas.get(criacao.trilha_id, ""), validada_em=criacao.validado_em
            )
        )
    for criacoes in por_guerreiro.values():
        criacoes.sort(key=lambda criacao: criacao.validada_em)
    return por_guerreiro


def montar_cartas_publicas(
    sessao: Session,
    linhas: list[tuple[Persona, str]],
    *,
    comunidade_id: uuid.UUID | None = None,
) -> list[CartaPublicaDeGuerreiroSaida]:
    """Monta a carta de **todos** os Guerreiros e Guerreiras de uma página em
    consultas por conjunto de identificadores — nunca uma por item, que
    seria N+1 no núcleo e, do lado do cliente, cairia no freio da consulta
    por nick (`RF-01-65`, design — decisão 1)."""
    ids = [persona.id for persona, _ in linhas]
    niveis = sessao.query(Nivel).filter(Nivel.guerreiro_id.in_(ids)).all() if ids else []
    badges = sessao.query(Badge).filter(Badge.guerreiro_id.in_(ids)).all() if ids else []

    trilha_ids = {nivel.trilha_id for nivel in niveis}
    trilha_ids |= {badge.trilha_id for badge in badges if badge.trilha_id is not None}
    poder_ids = {badge.poder_id for badge in badges if badge.poder_id is not None}
    poder_por_trilha, poder_por_id = _nomes_de_poder(
        sessao, trilha_ids=trilha_ids, poder_ids=poder_ids
    )

    desempenho = _desempenho_publico(sessao, ids, comunidade_id=comunidade_id)
    criacoes = _criacoes_na_carta(sessao, ids)

    # Nível por poder: o mesmo poder reúne várias trilhas, e o que a carta
    # exibe é o nível mais alto alcançado nele (documento 11 §§6, 8.2).
    nivel_por_poder: dict[uuid.UUID, dict[str, int]] = {}
    for nivel in niveis:
        poder = poder_por_trilha.get(nivel.trilha_id)
        if poder is None:
            continue
        do_guerreiro = nivel_por_poder.setdefault(nivel.guerreiro_id, {})
        do_guerreiro[poder] = max(do_guerreiro.get(poder, 0), nivel.valor)

    badges_por_guerreiro: dict[uuid.UUID, list[BadgeNaCartaSaida]] = {}
    for badge in badges:
        poder = (
            poder_por_id.get(badge.poder_id)
            if badge.poder_id is not None
            else poder_por_trilha.get(badge.trilha_id)
        )
        badges_por_guerreiro.setdefault(badge.guerreiro_id, []).append(
            BadgeNaCartaSaida(familia=badge.tipo.value, poder=poder)
        )

    cartas: list[CartaPublicaDeGuerreiroSaida] = []
    for persona, nick in linhas:
        pontos, posicao = desempenho.get(persona.id, (0, 0))
        cartas.append(
            CartaPublicaDeGuerreiroSaida(
                avatar=persona.avatar,
                nick=nick,
                badges=badges_por_guerreiro.get(persona.id, []),
                poderes=[
                    PoderComNivelSaida(poder=poder, nivel=nivel)
                    for poder, nivel in sorted(nivel_por_poder.get(persona.id, {}).items())
                ],
                pontos_regulares=pontos,
                posicao_no_ranking=posicao,
                criacoes=criacoes.get(persona.id, []),
            )
        )
    return cartas


def paginar_cartas_publicas(
    sessao: Session,
    *,
    comunidade_id: uuid.UUID | None,
    cursor: str | None,
    tamanho: int,
) -> PaginaDeResultado[CartaPublicaDeGuerreiroSaida]:
    """A listagem da vitrine: a carta inteira de cada Guerreiro(a) da página,
    na mesma resposta (`RF-03-02`, `RF-03-04`, `RF-03-05`)."""
    linhas, proximo_cursor = _paginar_personas_publicas(
        sessao, comunidade_id=comunidade_id, cursor=cursor, tamanho=tamanho
    )
    itens = montar_cartas_publicas(sessao, linhas, comunidade_id=comunidade_id)
    return PaginaDeResultado(itens=itens, proximo_cursor=proximo_cursor)
