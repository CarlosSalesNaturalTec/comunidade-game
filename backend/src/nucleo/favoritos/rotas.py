import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from ..autenticacao import ContextoDaSessao, exigir_persona
from ..banco import obter_sessao
from ..erros import ErroDeValidacao, PermissaoNegada
from ..personas.modelo import Papel, Persona
from ..protecao.freio import exigir_freio_por_origem
from ..vitrine.publico import buscar_avatares_e_nicks
from .regra import (
    FavoritoDeGuerreiro,
    FavoritoDeMestre,
    Novidade,
    favoritar,
    listar_favoritos,
    montar_novidades,
    remover_favorito,
)

roteador = APIRouter()


class NovidadeSaida(BaseModel):
    tipo: str
    data: datetime
    trilha_id: uuid.UUID | None
    trilha_nome: str | None
    badge_tipo: str | None
    nivel_valor: int | None


def _saida_da_novidade(novidade: Novidade) -> NovidadeSaida:
    return NovidadeSaida(
        tipo=novidade.tipo,
        data=novidade.data,
        trilha_id=novidade.trilha_id,
        trilha_nome=novidade.trilha_nome,
        badge_tipo=novidade.badge_tipo,
        nivel_valor=novidade.nivel_valor,
    )


class FavoritoDeGuerreiroSaida(BaseModel):
    id: uuid.UUID
    avatar: str | None
    nick: str
    novidades: list[NovidadeSaida]


class FavoritoDeMestreSaida(BaseModel):
    id: uuid.UUID
    avatar: str | None
    nome: str | None
    novidades: list[NovidadeSaida]


class FavoritosSaida(BaseModel):
    guerreiros: list[FavoritoDeGuerreiroSaida]
    mestres: list[FavoritoDeMestreSaida]


def _saida_de_guerreiro(favorito: FavoritoDeGuerreiro) -> FavoritoDeGuerreiroSaida:
    return FavoritoDeGuerreiroSaida(
        id=favorito.favorito_id,
        avatar=favorito.avatar,
        nick=favorito.nick,
        novidades=[_saida_da_novidade(n) for n in favorito.novidades],
    )


def _saida_de_mestre(favorito: FavoritoDeMestre) -> FavoritoDeMestreSaida:
    return FavoritoDeMestreSaida(
        id=favorito.favorito_id,
        avatar=favorito.avatar,
        nome=favorito.nome,
        novidades=[_saida_da_novidade(n) for n in favorito.novidades],
    )


def _exigir_apoiador(contexto: ContextoDaSessao) -> None:
    if contexto.papel != Papel.apoiador:
        raise PermissaoNegada(mensagem="Só o Apoiador gerencia os próprios favoritos.")


@roteador.get("/eu/favoritos")
def listar_meus_favoritos_rota(
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> FavoritosSaida:
    """Só os próprios favoritos, com as novidades dos últimos 30 dias
    (`RF-14-48`, `RF-14-52`, `RF-14-53`)."""
    _exigir_apoiador(contexto)
    favoritos = listar_favoritos(sessao_bd, apoiador_id=contexto.persona_id)
    return FavoritosSaida(
        guerreiros=[_saida_de_guerreiro(g) for g in favoritos.guerreiros],
        mestres=[_saida_de_mestre(m) for m in favoritos.mestres],
    )


class FavoritarEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nick: str | None = None
    mestre_id: uuid.UUID | None = None


@roteador.post(
    "/eu/favoritos",
    status_code=201,
    dependencies=[Depends(exigir_freio_por_origem("consulta_por_nick"))],
)
def favoritar_rota(
    entrada: FavoritarEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> FavoritoDeGuerreiroSaida | FavoritoDeMestreSaida:
    """Alvo por nick exato de Guerreiro(a) ou por persona de Mestre —
    exatamente um dos dois (`RF-14-49`, `RF-14-51`, `RF-14-52`)."""
    _exigir_apoiador(contexto)
    if (entrada.nick is None) == (entrada.mestre_id is None):
        raise ErroDeValidacao(
            mensagem="Informe o nick do Guerreiro(a) ou o mestre_id, nunca os dois nem nenhum."
        )

    favorito = favoritar(
        sessao_bd, apoiador_id=contexto.persona_id, nick=entrada.nick, mestre_id=entrada.mestre_id
    )
    sessao_bd.commit()

    if favorito.guerreiro_id is not None:
        avatar_e_nick = buscar_avatares_e_nicks(sessao_bd, [favorito.guerreiro_id])[
            favorito.guerreiro_id
        ]
        novidades = montar_novidades(
            sessao_bd, guerreiro_ids=[favorito.guerreiro_id], mestre_ids=[]
        )
        return FavoritoDeGuerreiroSaida(
            id=favorito.id,
            avatar=avatar_e_nick.avatar,
            nick=avatar_e_nick.nick,
            novidades=[_saida_da_novidade(n) for n in novidades.get(favorito.guerreiro_id, [])],
        )

    mestre = sessao_bd.get(Persona, favorito.mestre_id)
    novidades_do_mestre = montar_novidades(
        sessao_bd, guerreiro_ids=[], mestre_ids=[favorito.mestre_id]
    )
    return FavoritoDeMestreSaida(
        id=favorito.id,
        avatar=mestre.avatar,
        nome=mestre.nome,
        novidades=[_saida_da_novidade(n) for n in novidades_do_mestre.get(favorito.mestre_id, [])],
    )


@roteador.delete("/eu/favoritos/{favorito_id}", status_code=204)
def remover_meu_favorito_rota(
    favorito_id: uuid.UUID,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> None:
    """Remove a qualquer tempo; favorito de outro Apoiador e favorito
    inexistente recebem o mesmo 404 (`RF-14-55`)."""
    _exigir_apoiador(contexto)
    remover_favorito(sessao_bd, apoiador_id=contexto.persona_id, favorito_id=favorito_id)
    sessao_bd.commit()
