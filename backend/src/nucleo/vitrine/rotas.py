import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import tuple_
from sqlalchemy.orm import Session

from ..banco import obter_sessao
from ..comunidades.modelo import ComunidadeVirtual
from ..configuracao import Configuracao, obter_configuracao
from ..criacoes_originais.modelo import CriacaoOriginal
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
from ..poderes.modelo import Poder
from ..pontuacao.regra import consulta_de_ranking
from ..protecao.freio import exigir_freio_por_origem
from ..trilhas.modelo import SituacaoDaTrilha, Trilha
from .publico import (
    AvatarENickSaida,
    CartaPublicaDeGuerreiroSaida,
    buscar_avatares_e_nicks,
    buscar_persona_guerreiro_publica_por_nick,
    condicoes_de_criacao_publica,
    montar_cartas_publicas,
    nomes_de_trilha,
    paginar_cartas_publicas,
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


@roteador.get("/vitrine/guerreiros", response_model=PaginaDeResultado[CartaPublicaDeGuerreiroSaida])
def listar_guerreiros_publicos(
    parametros: Annotated[ParametrosDeListagem, Depends(contrato_de_listagem())],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> PaginaDeResultado[CartaPublicaDeGuerreiroSaida]:
    """Cards de quem tem autorização vigente, cada um com a **carta inteira**
    do documento 11 §8.2, paginado e filtrável por comunidade (`RF-01-02`,
    `RF-01-28`, `RF-03-02`, `RF-03-04`, `RF-03-05`, `RN-01-10`, `RN-01-11`).
    A composição sai na própria listagem: montá-la com uma consulta por nick
    para cada card cairia no freio por origem (`RF-01-65`)."""
    comunidade_id = _analisar_comunidade(parametros.filtros.get("comunidade"))
    return paginar_cartas_publicas(
        sessao_bd,
        comunidade_id=comunidade_id,
        cursor=parametros.cursor,
        tamanho=parametros.tamanho,
    )


@roteador.get(
    "/vitrine/guerreiros/{nick}",
    response_model=CartaPublicaDeGuerreiroSaida,
    dependencies=[Depends(exigir_freio_por_origem("consulta_por_nick"))],
)
def perfil_publico_de_guerreiro(
    nick: str,
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> CartaPublicaDeGuerreiroSaida:
    """Perfil por nick exato, na **mesma** composição do card (`RF-03-03`,
    `RF-03-05`); nick inexistente e nick sem autorização devolvem o mesmo
    404, resolvidos na mesma consulta (`RF-01-33`, `RF-01-34`, `RN-01-22`,
    `RF-01-65`)."""
    persona = buscar_persona_guerreiro_publica_por_nick(sessao_bd, nick)
    if persona is None:
        raise NaoEncontrado(mensagem="Guerreiro(a) não encontrado(a).")

    return montar_cartas_publicas(sessao_bd, [(persona, nick)])[0]


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
    abre buraco na numeração (`RF-01-21`, `RF-01-28`, `RN-01-10`). A
    derivação é a mesma que `pontuacao.regra.consulta_de_ranking` usa para o
    ranking logado da turma — este ranking sempre exige o portão da
    divulgação (design — Decisions)."""
    comunidade_id = _analisar_comunidade(parametros.filtros.get("comunidade"))

    base = consulta_de_ranking(sessao_bd, exigir_divulgacao=True, comunidade_id=comunidade_id)

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
    """O portfólio público do `RF-03-08`: trilha, data e autoria por nick.
    **Sem título** — a criação original não tem esse campo no modelo, e
    inventá-lo seria decisão nova (decisão do fundador, 2026-09-28)."""

    trilha_id: uuid.UUID
    trilha: str
    validada_em: datetime
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
    consulta = sessao_bd.query(CriacaoOriginal).filter(*condicoes_de_criacao_publica(sessao_bd))

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

    equipe_ids = [criacao.equipe_id for criacao in criacoes if criacao.equipe_id is not None]
    integrantes_por_equipe: dict[uuid.UUID, list[uuid.UUID]] = {}
    if equipe_ids:
        for integrante in sessao_bd.query(IntegranteDaEquipe).filter(
            IntegranteDaEquipe.equipe_id.in_(equipe_ids)
        ):
            integrantes_por_equipe.setdefault(integrante.equipe_id, []).append(
                integrante.persona_id
            )

    guerreiro_ids = {
        criacao.guerreiro_id for criacao in criacoes if criacao.guerreiro_id is not None
    }
    todas_as_personas_ids = {
        persona_id for ids in integrantes_por_equipe.values() for persona_id in ids
    } | guerreiro_ids
    avatares_e_nicks = buscar_avatares_e_nicks(sessao_bd, todas_as_personas_ids)

    def _autores_da_criacao(criacao: CriacaoOriginal) -> list[AvatarENickSaida]:
        if criacao.guerreiro_id is not None:
            return (
                [avatares_e_nicks[criacao.guerreiro_id]]
                if criacao.guerreiro_id in avatares_e_nicks
                else []
            )
        return [
            avatares_e_nicks[persona_id]
            for persona_id in integrantes_por_equipe.get(criacao.equipe_id, [])
            if persona_id in avatares_e_nicks
        ]

    trilhas = nomes_de_trilha(sessao_bd, {criacao.trilha_id for criacao in criacoes})

    itens = [
        CriacaoPublicaSaida(
            trilha_id=criacao.trilha_id,
            trilha=trilhas.get(criacao.trilha_id, ""),
            validada_em=criacao.validado_em,
            producao=criacao.producao,
            autores=_autores_da_criacao(criacao),
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
