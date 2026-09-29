import uuid
from collections.abc import Iterable
from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel
from sqlalchemy import and_, func, tuple_
from sqlalchemy.orm import Session, aliased

from ..aportes.modelo import Aporte
from ..comunidades.regra import filtrar_personas_por_comunidade
from ..consentimentos.regra import condicao_de_autorizacao_vigente
from ..criacoes_originais.modelo import CriacaoOriginal, SituacaoDaCriacaoOriginal
from ..desafios_extras.modelo import (
    ConclusaoDeDesafioExtra,
    DesafioExtra,
    Modalidade,
    SituacaoDoDesafioExtra,
)
from ..equipes.modelo import IntegranteDaEquipe
from ..erros import ErroDeValidacao
from ..paginacao import PaginaDeResultado, codificar_cursor, decodificar_cursor
from ..personas.modelo import ArtefatoComprobatorio, Nick, Papel, Persona
from ..personas.regra import PISO_DE_MOEDAS_DO_AVATAR_PROPRIO
from ..poder_sustentador.regra import contagem_de_absorcoes_de, moedas_acumuladas_de
from ..poderes.modelo import Poder
from ..pontuacao.modelo import Badge, Nivel
from ..pontuacao.regra import consulta_de_ranking
from ..selos_do_apoiador.regra import derivar_sustento, listar_selos
from ..trilhas.modelo import SituacaoDaTrilha, Trilha


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


# ---------------------------------------------------------------------------
# Mestre e Apoiador em público — as duas variantes da carta do documento 11
# §8.2 que a vitrine não publicava (`RF-03-02`, `RF-03-07`).
# ---------------------------------------------------------------------------

# O piso do avatar próprio do Apoiador, em moedas acumuladas (`RF-03-66`,
# `RN-14-11`, documento 11 §8.2). É o mesmo de `personas/regra.py`, importado
# de lá para que a vitrine e a App 08 nunca discordem.


class IdentificacaoPublicaSaida(BaseModel):
    """Quem é o adulto em público, **e o que o valor é**. O nick é opcional
    para Mestre e Apoiador, e a carta das duas variantes o exige: não havendo
    nick, sai o nome, declarado como nome, para que superfície alguma o
    apresente no lugar reservado ao nick (`RF-03-79`, `RN-03-36`, documento 11
    §8.2, decisão do fundador de 2026-09-29).

    NUNCA vale para Guerreiro(a): nome civil de criança não vai a público em
    hipótese alguma (invariantes 9 e 12 do documento 99 §6) — por isso a
    projeção do Guerreiro(a) segue sendo `AvatarENickSaida`, que só tem nick.
    """

    valor: str
    tipo: str  # "nick" ou "nome"


class ArtefatoPublicoSaida(BaseModel):
    """A prova pública do adulto: link declarado com o rótulo do que aponta
    (`RF-03-07`). O artefato não tem tipo no modelo — currículo, portfólio e
    rede social são o mesmo registro, distinguidos pelo rótulo de quem o
    declarou (`RN-02-01`, documento 02 §1)."""

    endereco: str
    rotulo: str


class TrilhaPublicaDeAutoriaSaida(BaseModel):
    id: uuid.UUID
    nome: str
    area_do_conhecimento: str


class MestreResponsavelSaida(BaseModel):
    """O Mestre responsável por um poder, na seção de poderes: o bastante
    para o card e o **identificador** que leva à página individual dele
    (`RF-03-02`, documento 11 §8.2)."""

    id: uuid.UUID
    avatar: str | None
    avatar_padrao: bool
    identificacao: IdentificacaoPublicaSaida


class CartaPublicaDeMestreSaida(BaseModel):
    """A variante **Mestre** do documento 11 §8.2, inteira: a mesma projeção
    serve o card e a página individual, como a carta do Guerreiro(a) já faz
    (`RF-03-02`, `RF-03-03`, `RF-03-07`).

    Nada de contato: e-mail, WhatsApp e afins ficam fora da rota pública
    (`RN-03-01`).
    """

    id: uuid.UUID
    avatar: str | None
    avatar_padrao: bool
    identificacao: IdentificacaoPublicaSaida
    areas_de_habilidade: list[str]
    artefatos: list[ArtefatoPublicoSaida]
    trilhas_de_autoria: list[TrilhaPublicaDeAutoriaSaida]
    absorcoes: int


class SeloPublicoSaida(BaseModel):
    familia: str
    nome: str


class DesafioPublicoDoApoiadorSaida(BaseModel):
    """A efetividade **agregada** do `RF-03-80`: trilha, período e quantos
    concluíram. Nunca quem concluiu — nem nick, nem avatar, nem contagem que
    identifique alguém —, e o direcionado sai só como "houve conclusão"
    (`RN-03-37`, decisão do fundador de 2026-09-29). O painel detalhado segue
    sendo do próprio Apoiador, na App 08 (`efetividade-do-apoio`)."""

    trilha: str
    periodo_inicio: date
    periodo_fim: date
    concluiram: int
    direcionado: bool


class CartaPublicaDeApoiadorSaida(BaseModel):
    """A variante **Apoiador** do documento 11 §8.2, inteira. O total sai em
    moedas e nunca em reais (`RF-03-10`, `RN-03-18`), e o avatar já vem
    resolvido pelo piso (`RF-03-66`)."""

    id: uuid.UUID
    avatar: str | None
    avatar_padrao: bool
    identificacao: IdentificacaoPublicaSaida
    total_em_moedas: Decimal
    nivel_de_sustento: int
    nome_do_nivel: str
    selos: list[SeloPublicoSaida]
    desafios_propostos: list[DesafioPublicoDoApoiadorSaida]
    artefatos: list[ArtefatoPublicoSaida]


def _identificacoes_publicas(
    sessao: Session, personas: list[Persona]
) -> dict[uuid.UUID, IdentificacaoPublicaSaida]:
    """Nick quando há, nome quando não — num só round-trip para toda a
    página (`RF-03-79`)."""
    if not personas:
        return {}
    nicks = dict(
        sessao.query(Nick.persona_id, Nick.valor)
        .filter(Nick.persona_id.in_([p.id for p in personas]))
        .all()
    )
    saida: dict[uuid.UUID, IdentificacaoPublicaSaida] = {}
    for persona in personas:
        nick = nicks.get(persona.id)
        if nick:
            saida[persona.id] = IdentificacaoPublicaSaida(valor=nick, tipo="nick")
        else:
            saida[persona.id] = IdentificacaoPublicaSaida(valor=persona.nome or "", tipo="nome")
    return saida


def _artefatos_publicos(
    sessao: Session, personas_ids: list[uuid.UUID]
) -> dict[uuid.UUID, list[ArtefatoPublicoSaida]]:
    if not personas_ids:
        return {}
    linhas = (
        sessao.query(ArtefatoComprobatorio)
        .filter(ArtefatoComprobatorio.persona_id.in_(personas_ids))
        .order_by(ArtefatoComprobatorio.criado_em)
        .all()
    )
    saida: dict[uuid.UUID, list[ArtefatoPublicoSaida]] = {}
    for artefato in linhas:
        saida.setdefault(artefato.persona_id, []).append(
            ArtefatoPublicoSaida(endereco=artefato.endereco, rotulo=artefato.rotulo)
        )
    return saida


def _trilhas_de_autoria(
    sessao: Session, mestres_ids: list[uuid.UUID]
) -> dict[uuid.UUID, list[TrilhaPublicaDeAutoriaSaida]]:
    """Só trilha **publicada**: rascunho e trilha retirada não são prova
    pública de nada (`RF-03-07`)."""
    if not mestres_ids:
        return {}
    linhas = (
        sessao.query(Trilha)
        .filter(
            Trilha.autor_id.in_(mestres_ids),
            Trilha.situacao == SituacaoDaTrilha.publicada,
        )
        .order_by(Trilha.nome)
        .all()
    )
    saida: dict[uuid.UUID, list[TrilhaPublicaDeAutoriaSaida]] = {}
    for trilha in linhas:
        saida.setdefault(trilha.autor_id, []).append(
            TrilhaPublicaDeAutoriaSaida(
                id=trilha.id,
                nome=trilha.nome,
                area_do_conhecimento=trilha.area_do_conhecimento,
            )
        )
    return saida


def montar_cartas_de_mestre(
    sessao: Session, personas: list[Persona]
) -> list[CartaPublicaDeMestreSaida]:
    """A carta inteira de cada Mestre da página, na mesma resposta — montar
    uma a uma custaria uma consulta por card, o mesmo cuidado que a carta do
    Guerreiro(a) já toma (`RF-03-02`, `RF-03-07`).

    As **áreas de habilidade** do documento 11 §8.2 não têm campo na persona:
    derivam da área do conhecimento das trilhas publicadas de autoria do
    Mestre (decisão do fundador de 2026-09-29).
    """
    ids = [persona.id for persona in personas]
    identificacoes = _identificacoes_publicas(sessao, personas)
    artefatos = _artefatos_publicos(sessao, ids)
    trilhas = _trilhas_de_autoria(sessao, ids)

    cartas: list[CartaPublicaDeMestreSaida] = []
    for persona in personas:
        trilhas_do_mestre = trilhas.get(persona.id, [])
        areas = sorted({trilha.area_do_conhecimento for trilha in trilhas_do_mestre})
        cartas.append(
            CartaPublicaDeMestreSaida(
                id=persona.id,
                avatar=persona.avatar,
                # O avatar padrão do projeto ocupa o lugar de qualquer avatar
                # que falte (documento 15 §7.3).
                avatar_padrao=persona.avatar is None,
                identificacao=identificacoes[persona.id],
                areas_de_habilidade=areas,
                artefatos=artefatos.get(persona.id, []),
                trilhas_de_autoria=trilhas_do_mestre,
                absorcoes=contagem_de_absorcoes_de(sessao, provedor_id=persona.id),
            )
        )
    return cartas


def _desafios_publicos_do_apoiador(
    sessao: Session, apoiador_id: uuid.UUID
) -> list[DesafioPublicoDoApoiadorSaida]:
    """Só o que está **publicado** — proposta em validação ou recusada não é
    fato público —, com a contagem de conclusões agregada numa consulta só
    (`RF-03-80`, `RN-03-37`)."""
    desafios = (
        sessao.query(DesafioExtra, Trilha.nome)
        .join(Trilha, Trilha.id == DesafioExtra.trilha_id)
        .filter(
            DesafioExtra.autor_id == apoiador_id,
            DesafioExtra.situacao == SituacaoDoDesafioExtra.publicado,
        )
        .order_by(DesafioExtra.vigencia_inicio.desc())
        .all()
    )
    if not desafios:
        return []

    conclusoes = dict(
        sessao.query(
            ConclusaoDeDesafioExtra.desafio_id,
            func.count(ConclusaoDeDesafioExtra.id),
        )
        .filter(ConclusaoDeDesafioExtra.desafio_id.in_([d.id for d, _ in desafios]))
        .group_by(ConclusaoDeDesafioExtra.desafio_id)
        .all()
    )
    return [
        DesafioPublicoDoApoiadorSaida(
            trilha=nome_da_trilha,
            periodo_inicio=desafio.vigencia_inicio,
            periodo_fim=desafio.vigencia_fim,
            concluiram=conclusoes.get(desafio.id, 0),
            direcionado=desafio.modalidade == Modalidade.direcionado,
        )
        for desafio, nome_da_trilha in desafios
    ]


def montar_cartas_de_apoiador(
    sessao: Session, personas: list[Persona]
) -> list[CartaPublicaDeApoiadorSaida]:
    """A carta inteira de cada Apoiador da página. O total é o **acumulado em
    aportes homologados** (`moedas_acumuladas_de`), não o Poder Sustentador:
    o `RF-03-66` e o `RN-14-11` falam de um direito que não regride, e o
    ressarcimento pago derruba o Poder Sustentador (`RF-03-10`, `RF-03-55`,
    `RN-03-18`)."""
    ids = [persona.id for persona in personas]
    identificacoes = _identificacoes_publicas(sessao, personas)
    artefatos = _artefatos_publicos(sessao, ids)

    cartas: list[CartaPublicaDeApoiadorSaida] = []
    for persona in personas:
        acumulado = moedas_acumuladas_de(sessao, provedor_id=persona.id)
        # O piso decide no núcleo, não na tela: abaixo dele a resposta nem
        # chega a carregar o avatar próprio (`RF-03-66`, documento 11 §8.2).
        liberado = acumulado >= PISO_DE_MOEDAS_DO_AVATAR_PROPRIO
        sustento = derivar_sustento(sessao, apoiador_id=persona.id)
        selos_por_familia = listar_selos(sessao, apoiador_id=persona.id)
        cartas.append(
            CartaPublicaDeApoiadorSaida(
                id=persona.id,
                avatar=persona.avatar if liberado else None,
                avatar_padrao=not liberado or persona.avatar is None,
                identificacao=identificacoes[persona.id],
                total_em_moedas=acumulado,
                nivel_de_sustento=sustento.nivel,
                nome_do_nivel=sustento.nome_do_nivel,
                # `frente_que_falta` fica fora: é orientação ao próprio
                # Apoiador, na App 08, não fato público.
                selos=[
                    SeloPublicoSaida(familia=str(familia), nome=selo.selo_nome)
                    for familia, selos in selos_por_familia.items()
                    for selo in selos
                ],
                desafios_propostos=_desafios_publicos_do_apoiador(sessao, persona.id),
                artefatos=artefatos.get(persona.id, []),
            )
        )
    return cartas


def _paginar_adultos_publicos(
    sessao: Session,
    *,
    papel: Papel,
    apenas_com_aporte: bool,
    cursor: str | None,
    tamanho: int,
) -> tuple[list[Persona], str | None]:
    """Paginação por cursor sobre `(criada_em, id)`, no mesmo contrato das
    demais listagens (`RF-01-28`). A ordem de apresentação é da tela: aqui a
    ordem é a estável do cursor, e **nunca** por valor aportado — pódio de
    apoiador é proibido (`RN-14-38`).

    `apenas_com_aporte` é o portão do `RF-03-57`: aplicado **antes** de
    paginar, para que a página não fique curta por exclusão. Linha em
    `Aporte` é aporte já creditado — a declaração pendente vive em
    `AporteDeclarado` e não cria nenhuma —, e a absorção conta mesmo sem
    homologador, que ela credita sem homologação (`RN-07-35`). É o mesmo
    portão que `derivar_sustento` usa para o nível 1.
    """
    consulta = sessao.query(Persona).filter(Persona.papel == papel)
    if apenas_com_aporte:
        consulta = consulta.filter(
            sessao.query(Aporte.id).filter(Aporte.provedor_id == Persona.id).exists()
        )

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

    linhas = consulta.order_by(Persona.criada_em, Persona.id).limit(tamanho + 1).all()

    proximo_cursor = None
    if len(linhas) > tamanho:
        linhas = linhas[:tamanho]
        proximo_cursor = codificar_cursor(
            {"criada_em": linhas[-1].criada_em.isoformat(), "id": str(linhas[-1].id)}
        )
    return linhas, proximo_cursor


def paginar_mestres_publicos(
    sessao: Session, *, cursor: str | None, tamanho: int
) -> PaginaDeResultado[CartaPublicaDeMestreSaida]:
    linhas, proximo_cursor = _paginar_adultos_publicos(
        sessao, papel=Papel.mestre, apenas_com_aporte=False, cursor=cursor, tamanho=tamanho
    )
    return PaginaDeResultado(
        itens=montar_cartas_de_mestre(sessao, linhas), proximo_cursor=proximo_cursor
    )


def paginar_apoiadores_publicos(
    sessao: Session, *, cursor: str | None, tamanho: int
) -> PaginaDeResultado[CartaPublicaDeApoiadorSaida]:
    linhas, proximo_cursor = _paginar_adultos_publicos(
        sessao, papel=Papel.apoiador, apenas_com_aporte=True, cursor=cursor, tamanho=tamanho
    )
    return PaginaDeResultado(
        itens=montar_cartas_de_apoiador(sessao, linhas), proximo_cursor=proximo_cursor
    )


def buscar_adulto_publico(
    sessao: Session, *, persona_id: uuid.UUID, papel: Papel, apenas_com_aporte: bool
) -> Persona | None:
    """Papel e portão resolvidos **na mesma consulta**: não há desvio no
    código que possa vazar a diferença entre identificador inexistente,
    persona de outro papel e Apoiador sem aporte — os três recebem o mesmo
    404 (`RF-03-57`, `RN-03-01`, o mesmo desenho de
    `buscar_persona_guerreiro_publica_por_nick`)."""
    consulta = sessao.query(Persona).filter(Persona.id == persona_id, Persona.papel == papel)
    if apenas_com_aporte:
        consulta = consulta.filter(
            sessao.query(Aporte.id).filter(Aporte.provedor_id == Persona.id).exists()
        )
    return consulta.first()


def mestres_responsaveis_por_poder(
    sessao: Session, poderes_ids: list[uuid.UUID]
) -> dict[uuid.UUID, list[MestreResponsavelSaida]]:
    """Os Mestres responsáveis do documento 11 §8.2: os autores das trilhas
    **publicadas** de cada poder, deduplicados, num só round-trip para todo o
    catálogo. Poder sem trilha publicada não entra no dicionário, e a rota o
    devolve com a lista vazia (`RF-03-02`, decisão do fundador de
    2026-09-29)."""
    if not poderes_ids:
        return {}
    linhas = (
        sessao.query(Trilha.poder_id, Persona)
        .join(Persona, Persona.id == Trilha.autor_id)
        .filter(
            Trilha.poder_id.in_(poderes_ids),
            Trilha.situacao == SituacaoDaTrilha.publicada,
            Persona.papel == Papel.mestre,
        )
        .all()
    )
    personas = {persona.id: persona for _, persona in linhas}
    identificacoes = _identificacoes_publicas(sessao, list(personas.values()))

    saida: dict[uuid.UUID, list[MestreResponsavelSaida]] = {}
    vistos: dict[uuid.UUID, set[uuid.UUID]] = {}
    for poder_id, persona in linhas:
        if persona.id in vistos.setdefault(poder_id, set()):
            continue
        vistos[poder_id].add(persona.id)
        saida.setdefault(poder_id, []).append(
            MestreResponsavelSaida(
                id=persona.id,
                avatar=persona.avatar,
                avatar_padrao=persona.avatar is None,
                identificacao=identificacoes[persona.id],
            )
        )
    for lista in saida.values():
        lista.sort(key=lambda mestre: mestre.identificacao.valor)
    return saida
