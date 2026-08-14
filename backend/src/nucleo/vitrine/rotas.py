import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import func, tuple_
from sqlalchemy.orm import Session

from ..banco import obter_sessao
from ..configuracao import Configuracao, obter_configuracao
from ..consentimentos.regra import condicao_de_autorizacao_vigente
from ..criacoes_originais.modelo import CriacaoOriginal, SituacaoDaCriacaoOriginal
from ..equipes.modelo import IntegranteDaEquipe
from ..erros import ErroDeValidacao, NaoEncontrado
from ..ods.regra import cobertura_por_comunidade, comunidades_com_cobertura
from ..paginacao import (
    PaginaDeResultado,
    ParametrosDeListagem,
    codificar_cursor,
    contrato_de_listagem,
    decodificar_cursor,
)
from ..personas.modelo import ComunidadeVirtual, Nick, Papel, Persona
from ..poderes.modelo import Poder
from ..pontuacao.modelo import Badge, Nivel, PontoRegular
from ..protecao.freio import exigir_freio_por_origem
from ..trilhas.modelo import SituacaoDaTrilha, Trilha
from .publico import (
    AvatarENickSaida,
    buscar_avatares_e_nicks,
    buscar_persona_guerreiro_publica_por_nick,
    paginar_guerreiros_publicos,
)

roteador = APIRouter()


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


@roteador.get("/vitrine/guerreiros", response_model=PaginaDeResultado[AvatarENickSaida])
def listar_guerreiros_publicos(
    parametros: Annotated[ParametrosDeListagem, Depends(contrato_de_listagem())],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> PaginaDeResultado[AvatarENickSaida]:
    """Cards de quem tem autorização vigente, paginado e filtrável por
    comunidade (`RF-01-02`, `RF-01-28`, `RN-01-10`, `RN-01-11`)."""
    comunidade_id = _analisar_comunidade(parametros.filtros.get("comunidade"))
    return paginar_guerreiros_publicos(
        sessao_bd,
        comunidade_id=comunidade_id,
        cursor=parametros.cursor,
        tamanho=parametros.tamanho,
    )


class NivelPublicoSaida(BaseModel):
    trilha_id: uuid.UUID
    valor: int


class BadgePublicoSaida(BaseModel):
    tipo: str
    trilha_id: uuid.UUID | None
    poder_id: uuid.UUID | None


class PerfilPublicoDeGuerreiroSaida(AvatarENickSaida):
    pontos_regulares: int
    niveis: list[NivelPublicoSaida]
    badges: list[BadgePublicoSaida]


@roteador.get(
    "/vitrine/guerreiros/{nick}",
    response_model=PerfilPublicoDeGuerreiroSaida,
    dependencies=[Depends(exigir_freio_por_origem("consulta_por_nick"))],
)
def perfil_publico_de_guerreiro(
    nick: str,
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> PerfilPublicoDeGuerreiroSaida:
    """Perfil por nick exato; nick inexistente e nick sem autorização
    devolvem o mesmo 404, resolvidos na mesma consulta (`RF-01-33`,
    `RF-01-34`, `RN-01-22`, `RF-01-65`)."""
    persona = buscar_persona_guerreiro_publica_por_nick(sessao_bd, nick)
    if persona is None:
        raise NaoEncontrado(mensagem="Guerreiro(a) não encontrado(a).")

    total_pontos = (
        sessao_bd.query(func.coalesce(func.sum(PontoRegular.total), 0))
        .filter(PontoRegular.guerreiro_id == persona.id)
        .scalar()
    )
    niveis = sessao_bd.query(Nivel).filter_by(guerreiro_id=persona.id).all()
    badges = sessao_bd.query(Badge).filter_by(guerreiro_id=persona.id).all()

    return PerfilPublicoDeGuerreiroSaida(
        avatar=persona.avatar,
        nick=nick,
        pontos_regulares=total_pontos,
        niveis=[
            NivelPublicoSaida(trilha_id=nivel.trilha_id, valor=nivel.valor) for nivel in niveis
        ],
        badges=[
            BadgePublicoSaida(
                tipo=badge.tipo.value, trilha_id=badge.trilha_id, poder_id=badge.poder_id
            )
            for badge in badges
        ],
    )


class ItemDeRankingSaida(AvatarENickSaida):
    pontos_regulares: int
    posicao: int


@roteador.get("/vitrine/rankings", response_model=PaginaDeResultado[ItemDeRankingSaida])
def ranking_publico(
    parametros: Annotated[ParametrosDeListagem, Depends(contrato_de_listagem())],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> PaginaDeResultado[ItemDeRankingSaida]:
    """Ordena por ponto regular; a posição é calculada sobre o conjunto já
    filtrado pelo portão da divulgação, de modo que quem não autorizou não
    abre buraco na numeração (`RF-01-21`, `RF-01-28`, `RN-01-10`)."""
    comunidade_id = _analisar_comunidade(parametros.filtros.get("comunidade"))

    totais = (
        sessao_bd.query(
            PontoRegular.guerreiro_id.label("guerreiro_id"),
            func.sum(PontoRegular.total).label("total"),
        )
        .group_by(PontoRegular.guerreiro_id)
        .subquery()
    )
    total_expr = func.coalesce(totais.c.total, 0)
    posicao_expr = func.row_number().over(order_by=[total_expr.desc(), Persona.id]).label("posicao")

    base = (
        sessao_bd.query(
            Persona.id.label("persona_id"),
            Persona.avatar.label("avatar"),
            Nick.valor.label("nick"),
            total_expr.label("total"),
            posicao_expr,
        )
        .join(Nick, Nick.persona_id == Persona.id)
        .outerjoin(totais, totais.c.guerreiro_id == Persona.id)
        .filter(
            Persona.papel == Papel.guerreiro,
            condicao_de_autorizacao_vigente(sessao_bd, Persona.id),
        )
    )
    if comunidade_id is not None:
        base = base.filter(Persona.comunidade_virtual_id == comunidade_id)

    subquery = base.subquery()
    consulta = sessao_bd.query(*subquery.c).order_by(subquery.c.posicao)

    if parametros.cursor:
        posicao_do_cursor = decodificar_cursor(parametros.cursor)
        try:
            ultima_posicao = int(posicao_do_cursor["posicao"])
        except (KeyError, ValueError) as exc:
            raise ErroDeValidacao(mensagem="Cursor de paginação inválido.", campo="cursor") from exc
        consulta = consulta.filter(subquery.c.posicao > ultima_posicao)

    linhas = consulta.limit(parametros.tamanho + 1).all()

    proximo_cursor = None
    if len(linhas) > parametros.tamanho:
        linhas = linhas[: parametros.tamanho]
        proximo_cursor = codificar_cursor({"posicao": linhas[-1].posicao})

    itens = [
        ItemDeRankingSaida(
            avatar=linha.avatar,
            nick=linha.nick,
            pontos_regulares=linha.total,
            posicao=linha.posicao,
        )
        for linha in linhas
    ]
    return PaginaDeResultado(itens=itens, proximo_cursor=proximo_cursor)


class TrilhaPublicaSaida(BaseModel):
    id: uuid.UUID
    nome: str


class PoderPublicoSaida(BaseModel):
    id: uuid.UUID
    nome: str
    descricao: str
    trilhas: list[TrilhaPublicaSaida]


@roteador.get("/vitrine/poderes", response_model=list[PoderPublicoSaida])
def listar_poderes_publicos(
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> list[PoderPublicoSaida]:
    """Poderes ativos com as trilhas publicadas vinculadas a cada um; a
    trilha nunca é filtrada por comunidade, bem comum da plataforma
    (`RF-01-62`, `RN-01-42`)."""
    poderes = sessao_bd.query(Poder).filter_by(ativo=True).order_by(Poder.nome).all()
    saida: list[PoderPublicoSaida] = []
    for poder in poderes:
        trilhas = (
            sessao_bd.query(Trilha)
            .filter_by(poder_id=poder.id, situacao=SituacaoDaTrilha.publicada)
            .order_by(Trilha.nome)
            .all()
        )
        saida.append(
            PoderPublicoSaida(
                id=poder.id,
                nome=poder.nome,
                descricao=poder.descricao,
                trilhas=[TrilhaPublicaSaida(id=trilha.id, nome=trilha.nome) for trilha in trilhas],
            )
        )
    return saida


class CriacaoPublicaSaida(BaseModel):
    trilha_id: uuid.UUID
    producao: str
    autores: list[AvatarENickSaida]


@roteador.get("/vitrine/criacoes", response_model=PaginaDeResultado[CriacaoPublicaSaida])
def listar_criacoes_publicas(
    parametros: Annotated[ParametrosDeListagem, Depends(contrato_de_listagem())],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> PaginaDeResultado[CriacaoPublicaSaida]:
    """Portfólio de criações validadas, exibidas só quando todos os
    creditados têm autorização vigente (`RF-01-26`, `RN-01-13`,
    `RN-01-10`)."""
    tem_integrante_nao_autorizado = (
        sessao_bd.query(IntegranteDaEquipe.id)
        .filter(IntegranteDaEquipe.equipe_id == CriacaoOriginal.equipe_id)
        .filter(~condicao_de_autorizacao_vigente(sessao_bd, IntegranteDaEquipe.persona_id))
        .exists()
    )
    consulta = (
        sessao_bd.query(CriacaoOriginal)
        .filter(CriacaoOriginal.situacao == SituacaoDaCriacaoOriginal.validada)
        .filter(~tem_integrante_nao_autorizado)
    )

    if parametros.cursor:
        posicao = decodificar_cursor(parametros.cursor)
        try:
            validado_em_cursor = datetime.fromisoformat(posicao["validado_em"])
            id_cursor = uuid.UUID(posicao["id"])
        except (KeyError, ValueError) as exc:
            raise ErroDeValidacao(mensagem="Cursor de paginação inválido.", campo="cursor") from exc
        consulta = consulta.filter(
            tuple_(CriacaoOriginal.validado_em, CriacaoOriginal.id)
            > (validado_em_cursor, id_cursor)
        )

    consulta = consulta.order_by(CriacaoOriginal.validado_em, CriacaoOriginal.id).limit(
        parametros.tamanho + 1
    )
    criacoes = consulta.all()

    proximo_cursor = None
    if len(criacoes) > parametros.tamanho:
        criacoes = criacoes[: parametros.tamanho]
        ultima = criacoes[-1]
        proximo_cursor = codificar_cursor(
            {"validado_em": ultima.validado_em.isoformat(), "id": str(ultima.id)}
        )

    equipe_ids = [criacao.equipe_id for criacao in criacoes]
    integrantes_por_equipe: dict[uuid.UUID, list[uuid.UUID]] = {}
    if equipe_ids:
        for integrante in sessao_bd.query(IntegranteDaEquipe).filter(
            IntegranteDaEquipe.equipe_id.in_(equipe_ids)
        ):
            integrantes_por_equipe.setdefault(integrante.equipe_id, []).append(
                integrante.persona_id
            )

    todas_as_personas_ids = {
        persona_id for ids in integrantes_por_equipe.values() for persona_id in ids
    }
    avatares_e_nicks = buscar_avatares_e_nicks(sessao_bd, todas_as_personas_ids)

    itens = [
        CriacaoPublicaSaida(
            trilha_id=criacao.trilha_id,
            producao=criacao.producao,
            autores=[
                avatares_e_nicks[persona_id]
                for persona_id in integrantes_por_equipe.get(criacao.equipe_id, [])
                if persona_id in avatares_e_nicks
            ],
        )
        for criacao in criacoes
    ]
    return PaginaDeResultado(itens=itens, proximo_cursor=proximo_cursor)


class CoberturaPublicaSaida(BaseModel):
    comunidade_id: uuid.UUID
    comunidade_nome: str
    objetivos: list[int]
    ciclo: str


@roteador.get("/vitrine/ods/cobertura", response_model=list[CoberturaPublicaSaida])
def cobertura_publica_de_ods(
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    configuracao: Annotated[Configuracao, Depends(obter_configuracao)],
) -> list[CoberturaPublicaSaida]:
    """Cobertura agregada por comunidade e ciclo; nenhum recorte por
    Guerreiro(a) existe nesta rota (`RF-01-43`, `RN-01-24`)."""
    saida: list[CoberturaPublicaSaida] = []
    for comunidade_id in comunidades_com_cobertura(sessao_bd):
        comunidade = sessao_bd.get(ComunidadeVirtual, comunidade_id)
        objetivos = cobertura_por_comunidade(sessao_bd, comunidade_id)
        saida.append(
            CoberturaPublicaSaida(
                comunidade_id=comunidade_id,
                comunidade_nome=comunidade.nome,
                objetivos=sorted(objetivos),
                ciclo=configuracao.ciclo_rotulo,
            )
        )
    return saida
