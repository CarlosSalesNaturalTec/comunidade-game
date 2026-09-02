import uuid
from collections.abc import Iterable
from dataclasses import dataclass, field
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from ..consentimentos.regra import condicao_de_autorizacao_vigente
from ..criacoes_originais.modelo import CriacaoOriginal, SituacaoDaCriacaoOriginal
from ..equipes.modelo import IntegranteDaEquipe
from ..erros import NaoEncontrado
from ..personas.modelo import Papel, Persona
from ..pontuacao.modelo import Badge, Nivel
from ..tempo import agora
from ..trilhas.modelo import SituacaoDaTrilha, Trilha
from ..vitrine.publico import (
    AvatarENickSaida,
    buscar_avatares_e_nicks,
    buscar_persona_guerreiro_publica_por_nick,
)
from .modelo import Favorito

JANELA_DE_NOVIDADE_EM_DIAS = 30


@dataclass(frozen=True)
class Novidade:
    """Um dos quatro fatos disponíveis nesta fatia — o quinto, resultado de
    batalha, entra com o PRD-10 (`RF-14-53`, `RN-14-25`)."""

    tipo: str
    data: datetime
    trilha_id: uuid.UUID | None = None
    trilha_nome: str | None = None
    badge_tipo: str | None = None
    nivel_valor: int | None = None


@dataclass(frozen=True)
class FavoritoDeGuerreiro:
    favorito_id: uuid.UUID
    avatar: str | None
    nick: str
    novidades: list[Novidade] = field(default_factory=list)


@dataclass(frozen=True)
class FavoritoDeMestre:
    favorito_id: uuid.UUID
    avatar: str | None
    nome: str | None
    novidades: list[Novidade] = field(default_factory=list)


@dataclass(frozen=True)
class FavoritosDoApoiador:
    guerreiros: list[FavoritoDeGuerreiro]
    mestres: list[FavoritoDeMestre]


def favoritar(
    sessao: Session,
    *,
    apoiador_id: uuid.UUID,
    nick: str | None,
    mestre_id: uuid.UUID | None,
) -> Favorito:
    """Favorita por nick exato de Guerreiro(a) ou por persona de Mestre —
    nick inexistente e nick sem autorização vigente caem no mesmo
    `NaoEncontrado`, sem desvio no código (`RF-14-49`, `RF-14-51`,
    `RF-14-52`, `RN-14-23`). Favoritar de novo devolve o favorito
    existente, com o mesmo corpo — nunca 409 (design — decisões 4 e 5).
    """
    if nick is not None:
        guerreiro = buscar_persona_guerreiro_publica_por_nick(sessao, nick)
        if guerreiro is None:
            raise NaoEncontrado(mensagem="Guerreiro(a) não encontrado(a).")
        existente = (
            sessao.query(Favorito)
            .filter(Favorito.apoiador_id == apoiador_id, Favorito.guerreiro_id == guerreiro.id)
            .first()
        )
        if existente is not None:
            return existente
        favorito = Favorito(apoiador_id=apoiador_id, guerreiro_id=guerreiro.id)
    else:
        mestre = sessao.get(Persona, mestre_id)
        if mestre is None or mestre.papel != Papel.mestre:
            raise NaoEncontrado(mensagem="Mestre não encontrado.")
        existente = (
            sessao.query(Favorito)
            .filter(Favorito.apoiador_id == apoiador_id, Favorito.mestre_id == mestre_id)
            .first()
        )
        if existente is not None:
            return existente
        favorito = Favorito(apoiador_id=apoiador_id, mestre_id=mestre_id)

    sessao.add(favorito)
    sessao.flush()
    return favorito


def remover_favorito(sessao: Session, *, apoiador_id: uuid.UUID, favorito_id: uuid.UUID) -> None:
    """Apaga a linha por `(id, apoiador_id)` numa consulta só — favorito
    inexistente e favorito de outro Apoiador no mesmo 404 (`RF-14-55`,
    design — decisão 5)."""
    apagados = (
        sessao.query(Favorito)
        .filter(Favorito.id == favorito_id, Favorito.apoiador_id == apoiador_id)
        .delete()
    )
    if apagados == 0:
        raise NaoEncontrado(mensagem="Favorito não encontrado.")


def montar_novidades(
    sessao: Session,
    *,
    guerreiro_ids: Iterable[uuid.UUID],
    mestre_ids: Iterable[uuid.UUID],
) -> dict[uuid.UUID, list[Novidade]]:
    """Uma consulta por tipo de fato, sobre o conjunto de alvos, com janela
    de 30 dias a contar da data do fato (`RF-14-53`, `RN-14-25`, design —
    decisão 6). A criação original de equipe alcança o favoritado pela
    participação dele, e passa pelo mesmo portão de
    `vitrine.rotas.listar_criacoes_publicas`: só entra quando todos os
    creditados têm autorização vigente."""
    ids_de_guerreiro = set(guerreiro_ids)
    ids_de_mestre = set(mestre_ids)
    limite = agora() - timedelta(days=JANELA_DE_NOVIDADE_EM_DIAS)
    novidades: dict[uuid.UUID, list[Novidade]] = {}

    if ids_de_guerreiro:
        criacoes_individuais = (
            sessao.query(CriacaoOriginal)
            .filter(
                CriacaoOriginal.guerreiro_id.in_(ids_de_guerreiro),
                CriacaoOriginal.situacao == SituacaoDaCriacaoOriginal.validada,
                CriacaoOriginal.validado_em >= limite,
            )
            .all()
        )
        for criacao in criacoes_individuais:
            novidades.setdefault(criacao.guerreiro_id, []).append(
                Novidade(
                    tipo="criacao_original", data=criacao.validado_em, trilha_id=criacao.trilha_id
                )
            )

        equipe_ids_dos_favoritados = {
            linha[0]
            for linha in sessao.query(IntegranteDaEquipe.equipe_id)
            .filter(IntegranteDaEquipe.persona_id.in_(ids_de_guerreiro))
            .all()
        }
        if equipe_ids_dos_favoritados:
            criacoes_de_equipe = (
                sessao.query(CriacaoOriginal)
                .filter(
                    CriacaoOriginal.equipe_id.in_(equipe_ids_dos_favoritados),
                    CriacaoOriginal.situacao == SituacaoDaCriacaoOriginal.validada,
                    CriacaoOriginal.validado_em >= limite,
                )
                .all()
            )
            if criacoes_de_equipe:
                equipe_ids_com_criacao = {c.equipe_id for c in criacoes_de_equipe}
                integrantes_por_equipe: dict[uuid.UUID, list[uuid.UUID]] = {}
                for integrante in (
                    sessao.query(IntegranteDaEquipe)
                    .filter(IntegranteDaEquipe.equipe_id.in_(equipe_ids_com_criacao))
                    .all()
                ):
                    integrantes_por_equipe.setdefault(integrante.equipe_id, []).append(
                        integrante.persona_id
                    )
                todos_os_integrantes_ids = {
                    persona_id for ids in integrantes_por_equipe.values() for persona_id in ids
                }
                ids_nao_autorizados = {
                    linha[0]
                    for linha in sessao.query(Persona.id)
                    .filter(
                        Persona.id.in_(todos_os_integrantes_ids),
                        ~condicao_de_autorizacao_vigente(sessao, Persona.id),
                    )
                    .all()
                }
                for criacao in criacoes_de_equipe:
                    membros = integrantes_por_equipe.get(criacao.equipe_id, [])
                    if any(membro in ids_nao_autorizados for membro in membros):
                        continue
                    for membro in membros:
                        if membro in ids_de_guerreiro:
                            novidades.setdefault(membro, []).append(
                                Novidade(
                                    tipo="criacao_original",
                                    data=criacao.validado_em,
                                    trilha_id=criacao.trilha_id,
                                )
                            )

        for badge in (
            sessao.query(Badge)
            .filter(Badge.guerreiro_id.in_(ids_de_guerreiro), Badge.certificado_em >= limite)
            .all()
        ):
            novidades.setdefault(badge.guerreiro_id, []).append(
                Novidade(
                    tipo="badge",
                    data=badge.certificado_em,
                    trilha_id=badge.trilha_id,
                    badge_tipo=badge.tipo.value,
                )
            )

        for nivel in (
            sessao.query(Nivel)
            .filter(Nivel.guerreiro_id.in_(ids_de_guerreiro), Nivel.certificado_em >= limite)
            .all()
        ):
            novidades.setdefault(nivel.guerreiro_id, []).append(
                Novidade(
                    tipo="nivel",
                    data=nivel.certificado_em,
                    trilha_id=nivel.trilha_id,
                    nivel_valor=nivel.valor,
                )
            )

    if ids_de_mestre:
        for trilha in (
            sessao.query(Trilha)
            .filter(
                Trilha.autor_id.in_(ids_de_mestre),
                Trilha.situacao == SituacaoDaTrilha.publicada,
                Trilha.situacao_alterada_em.is_not(None),
                Trilha.situacao_alterada_em >= limite,
            )
            .all()
        ):
            novidades.setdefault(trilha.autor_id, []).append(
                Novidade(
                    tipo="trilha",
                    data=trilha.situacao_alterada_em,
                    trilha_id=trilha.id,
                    trilha_nome=trilha.nome,
                )
            )

    return novidades


def listar_favoritos(sessao: Session, *, apoiador_id: uuid.UUID) -> FavoritosDoApoiador:
    """Guerreiro(a) por avatar e nick sob o portão da divulgação dentro da
    consulta, e Mestre por nome e avatar (`RF-14-48`, `RF-14-52`,
    `RN-14-24`, design — decisão 7). Quem perdeu a autorização some sem
    lacuna nem contagem, e o registro do favorito permanece."""
    favoritos = sessao.query(Favorito).filter(Favorito.apoiador_id == apoiador_id).all()
    favoritos_de_guerreiro = {f.guerreiro_id: f for f in favoritos if f.guerreiro_id is not None}
    favoritos_de_mestre = {f.mestre_id: f for f in favoritos if f.mestre_id is not None}

    ids_de_guerreiro_vigentes: set[uuid.UUID] = set()
    if favoritos_de_guerreiro:
        ids_de_guerreiro_vigentes = {
            linha[0]
            for linha in sessao.query(Persona.id)
            .filter(
                Persona.id.in_(favoritos_de_guerreiro.keys()),
                condicao_de_autorizacao_vigente(sessao, Persona.id),
            )
            .all()
        }

    avatares_e_nicks: dict[uuid.UUID, AvatarENickSaida] = buscar_avatares_e_nicks(
        sessao, ids_de_guerreiro_vigentes
    )
    novidades_por_alvo = montar_novidades(
        sessao,
        guerreiro_ids=ids_de_guerreiro_vigentes,
        mestre_ids=favoritos_de_mestre.keys(),
    )

    guerreiros = [
        FavoritoDeGuerreiro(
            favorito_id=favoritos_de_guerreiro[guerreiro_id].id,
            avatar=avatares_e_nicks[guerreiro_id].avatar,
            nick=avatares_e_nicks[guerreiro_id].nick,
            novidades=novidades_por_alvo.get(guerreiro_id, []),
        )
        for guerreiro_id in ids_de_guerreiro_vigentes
        if guerreiro_id in avatares_e_nicks
    ]

    mestres: list[FavoritoDeMestre] = []
    if favoritos_de_mestre:
        personas_de_mestre = (
            sessao.query(Persona).filter(Persona.id.in_(favoritos_de_mestre.keys())).all()
        )
        mestres = [
            FavoritoDeMestre(
                favorito_id=favoritos_de_mestre[persona.id].id,
                avatar=persona.avatar,
                nome=persona.nome,
                novidades=novidades_por_alvo.get(persona.id, []),
            )
            for persona in personas_de_mestre
        ]

    return FavoritosDoApoiador(guerreiros=guerreiros, mestres=mestres)
