import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..banco import obter_sessao
from ..erros import ErroDeValidacao, NaoEncontrado
from ..paginacao import PaginaDeResultado, ParametrosDeListagem, contrato_de_listagem
from ..poderes.modelo import Poder
from ..ponto_extra.modelo import PontoExtra
from ..pontuacao.modelo import Badge, Nivel, PontoRegular
from ..protecao.freio import exigir_freio_por_origem
from ..trilhas.modelo import Trilha
from ..vitrine.publico import (
    AvatarENickSaida,
    buscar_persona_guerreiro_publica_por_nick,
    paginar_guerreiros_publicos,
)

roteador = APIRouter()

# `RF-01-22`, `RN-01-06`: nenhuma rota deste módulo escreve. O contrato dos
# jogos é leitura, ponto — a mesma projeção pública da vitrine (invariante 8
# do documento 99 §6), sem credencial de persona (`RF-01-02`).


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


@roteador.get("/jogos/elenco", response_model=PaginaDeResultado[AvatarENickSaida])
def elenco_do_jogo(
    parametros: Annotated[ParametrosDeListagem, Depends(contrato_de_listagem())],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> PaginaDeResultado[AvatarENickSaida]:
    """O elenco é estritamente quem tem autorização de divulgação vigente —
    o mesmo portão da vitrine (`RN-01-10`, invariante 8 do documento 99
    §6)."""
    comunidade_id = _analisar_comunidade(parametros.filtros.get("comunidade"))
    return paginar_guerreiros_publicos(
        sessao_bd,
        comunidade_id=comunidade_id,
        cursor=parametros.cursor,
        tamanho=parametros.tamanho,
    )


class NivelDoPersonagemSaida(BaseModel):
    trilha_id: uuid.UUID
    valor: int


class BadgeDoPersonagemSaida(BaseModel):
    tipo: str
    trilha_id: uuid.UUID | None
    poder_id: uuid.UUID | None


class PoderDoPersonagemSaida(BaseModel):
    id: uuid.UUID
    nome: str


class PersonagemSaida(AvatarENickSaida):
    """A estrutura nunca carrega o saldo disponível de ponto extra — só o
    acumulado, que nunca decresce (`RF-01-59`, `RN-01-41`, design —
    Decisions): a ausência é da estrutura, não da serialização."""

    pontos_regulares: int
    pontos_extra_acumulado: int
    niveis: list[NivelDoPersonagemSaida]
    badges: list[BadgeDoPersonagemSaida]
    poderes: list[PoderDoPersonagemSaida]


@roteador.get(
    "/jogos/personagens/{nick}",
    response_model=PersonagemSaida,
    dependencies=[Depends(exigir_freio_por_origem("consulta_por_nick"))],
)
def progresso_do_personagem(
    nick: str,
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> PersonagemSaida:
    """O progresso para montar o personagem: pontos regulares, acumulado de
    pontos extras, poderes, badges e níveis — nunca o saldo disponível
    (`RF-01-22`, `RF-01-59`, `RN-01-10`). Quem não autorizou não é
    alcançável, nem por consulta direta (`RN-01-10`)."""
    persona = buscar_persona_guerreiro_publica_por_nick(sessao_bd, nick)
    if persona is None:
        raise NaoEncontrado(mensagem="Guerreiro(a) não encontrado(a).")

    total_pontos = (
        sessao_bd.query(func.coalesce(func.sum(PontoRegular.total), 0))
        .filter(PontoRegular.guerreiro_id == persona.id)
        .scalar()
    )
    # Só a coluna do acumulado é lida — o saldo disponível nunca entra na
    # consulta, e portanto não há como vazá-lo por engano (`RN-01-41`).
    acumulado_extra = (
        sessao_bd.query(PontoExtra.acumulado).filter(PontoExtra.guerreiro_id == persona.id).scalar()
    ) or 0

    niveis = sessao_bd.query(Nivel).filter_by(guerreiro_id=persona.id).all()
    badges = sessao_bd.query(Badge).filter_by(guerreiro_id=persona.id).all()

    poder_ids = {
        poder_id
        for (poder_id,) in sessao_bd.query(Trilha.poder_id)
        .join(Nivel, Nivel.trilha_id == Trilha.id)
        .filter(Nivel.guerreiro_id == persona.id)
        .distinct()
    }
    poderes = sessao_bd.query(Poder).filter(Poder.id.in_(poder_ids)).all() if poder_ids else []

    return PersonagemSaida(
        avatar=persona.avatar,
        nick=nick,
        pontos_regulares=total_pontos,
        pontos_extra_acumulado=acumulado_extra,
        niveis=[
            NivelDoPersonagemSaida(trilha_id=nivel.trilha_id, valor=nivel.valor) for nivel in niveis
        ],
        badges=[
            BadgeDoPersonagemSaida(
                tipo=badge.tipo.value, trilha_id=badge.trilha_id, poder_id=badge.poder_id
            )
            for badge in badges
        ],
        poderes=[PoderDoPersonagemSaida(id=poder.id, nome=poder.nome) for poder in poderes],
    )
