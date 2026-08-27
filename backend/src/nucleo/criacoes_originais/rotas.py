import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from ..armazenamento.fabrica import dependencia_de_armazenamento
from ..armazenamento.porta import PortaDeArmazenamento
from ..autenticacao import ContextoDaSessao, exigir_persona
from ..banco import obter_sessao
from ..consentimentos.regra import condicao_de_autorizacao_vigente
from ..culminancias.modelo import Culminancia
from ..equipes.modelo import Equipe, IntegranteDaEquipe
from ..erros import NaoEncontrado, PermissaoNegada
from ..permissoes import Operacao, exigir_permissao
from ..personas.modelo import Papel, Persona
from ..trilhas.modelo import Trilha
from ..vitrine.publico import AvatarENickSaida, buscar_avatares_e_nicks
from .modelo import CriacaoOriginal, SituacaoDaCriacaoOriginal, TipoDeProducaoDaCriacaoOriginal
from .regra import (
    abrir_envio_da_criacao,
    confirmar_envio_da_criacao,
    consultar_criacao_original_do_guerreiro_na_trilha,
    consultar_fila_do_mestre_autor,
    consultar_portfolio_do_guerreiro,
    devolver_criacao_original,
    entregar_criacao_original,
    validar_criacao_original,
)

roteador = APIRouter()


class CriacaoOriginalSaida(BaseModel):
    id: uuid.UUID
    trilha_id: uuid.UUID
    equipe_id: uuid.UUID | None
    guerreiro_id: uuid.UUID | None
    tipo: TipoDeProducaoDaCriacaoOriginal
    producao: str | None
    referencia: str | None
    tamanho: int | None
    situacao: SituacaoDaCriacaoOriginal
    motivo_da_devolucao: str | None


def _saida(criacao: CriacaoOriginal) -> CriacaoOriginalSaida:
    return CriacaoOriginalSaida(
        id=criacao.id,
        trilha_id=criacao.trilha_id,
        equipe_id=criacao.equipe_id,
        guerreiro_id=criacao.guerreiro_id,
        tipo=criacao.tipo,
        producao=criacao.producao,
        referencia=criacao.referencia,
        tamanho=criacao.tamanho,
        situacao=criacao.situacao,
        motivo_da_devolucao=criacao.motivo_da_devolucao,
    )


def _obter_criacao(sessao_bd: Session, id_da_criacao: uuid.UUID) -> CriacaoOriginal:
    criacao = sessao_bd.get(CriacaoOriginal, id_da_criacao)
    if criacao is None:
        raise NaoEncontrado(mensagem="Criação original não encontrada.")
    return criacao


class EntregarCriacaoEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    equipe_id: uuid.UUID | None = None
    tipo: str | None = None
    producao: str | None = None


@roteador.post("/culminancias/{id_da_culminancia}/criacoes", status_code=201)
def entregar_criacao_original_rota(
    id_da_culminancia: uuid.UUID,
    entrada: EntregarCriacaoEntrada,
    contexto: Annotated[
        ContextoDaSessao, Depends(exigir_permissao(Operacao.suas_criacoes, "escreve"))
    ],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> CriacaoOriginalSaida:
    """`RF-05-40`, `RF-05-41`: a entrega é endereçada pela culminância — o
    núcleo resolve a trilha por ela (design — decisão 1). A modalidade, a
    coerência do tipo e a substituição antes da validação já são de
    `entregar_criacao_original`."""
    guerreiro = sessao_bd.get(Persona, contexto.persona_id)
    culminancia = sessao_bd.get(Culminancia, id_da_culminancia)
    if culminancia is None:
        raise NaoEncontrado(mensagem="Culminância não encontrada.")
    trilha = sessao_bd.get(Trilha, culminancia.trilha_id)
    equipe = sessao_bd.get(Equipe, entrada.equipe_id) if entrada.equipe_id is not None else None

    criacao = entregar_criacao_original(
        sessao_bd,
        guerreiro=guerreiro,
        trilha=trilha,
        equipe=equipe,
        tipo=entrada.tipo,
        producao=entrada.producao,
    )
    sessao_bd.commit()
    return _saida(criacao)


@roteador.get("/eu/trilhas/{id_da_trilha}/criacao")
def obter_minha_criacao_da_trilha_rota(
    id_da_trilha: uuid.UUID,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> CriacaoOriginalSaida:
    """A própria entrega do Guerreiro(a) naquela trilha, em qualquer
    situação — sustenta a tela de entrega e a de devolução ao reabrir a
    aplicação, com o motivo e o caminho de reenvio (`RF-05-40`,
    `RF-05-42`)."""
    if contexto.papel != Papel.guerreiro:
        raise PermissaoNegada(mensagem="Só o Guerreiro(a) tem criação original própria.")
    criacao = consultar_criacao_original_do_guerreiro_na_trilha(
        sessao_bd, guerreiro_id=contexto.persona_id, trilha_id=id_da_trilha
    )
    if criacao is None:
        raise NaoEncontrado(mensagem="Nenhuma criação original entregue nesta trilha.")
    return _saida(criacao)


class AbrirEnvioEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tipo_mime: str
    tamanho_declarado: int


class AbrirEnvioSaida(BaseModel):
    endereco_da_sessao: str


@roteador.post("/criacoes/{id_da_criacao}/arquivo", status_code=201)
def abrir_envio_rota(
    id_da_criacao: uuid.UUID,
    entrada: AbrirEnvioEntrada,
    contexto: Annotated[
        ContextoDaSessao, Depends(exigir_permissao(Operacao.suas_criacoes, "escreve"))
    ],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    armazenamento: Annotated[PortaDeArmazenamento, Depends(dependencia_de_armazenamento)],
) -> AbrirEnvioSaida:
    """`RF-05-40`: abre a sessão retomável de envio, espelhando
    `conteudos/rotas.py` (design — decisão 4)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    criacao = _obter_criacao(sessao_bd, id_da_criacao)
    endereco = abrir_envio_da_criacao(
        sessao_bd,
        criacao,
        operador=operador,
        tipo_mime=entrada.tipo_mime,
        tamanho_declarado=entrada.tamanho_declarado,
        armazenamento=armazenamento,
    )
    sessao_bd.commit()
    return AbrirEnvioSaida(endereco_da_sessao=endereco)


@roteador.patch("/criacoes/{id_da_criacao}/arquivo")
def confirmar_envio_rota(
    id_da_criacao: uuid.UUID,
    contexto: Annotated[
        ContextoDaSessao, Depends(exigir_permissao(Operacao.suas_criacoes, "escreve"))
    ],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    armazenamento: Annotated[PortaDeArmazenamento, Depends(dependencia_de_armazenamento)],
) -> CriacaoOriginalSaida:
    """Confirma o envio encerrado pelo cliente — só agora a criação passa a
    servir bytes (`RF-05-40`, design — decisão 4)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    criacao = _obter_criacao(sessao_bd, id_da_criacao)
    criacao = confirmar_envio_da_criacao(
        sessao_bd, criacao, operador=operador, armazenamento=armazenamento
    )
    sessao_bd.commit()
    return _saida(criacao)


class CreditadoNoPortfolioSaida(AvatarENickSaida):
    pass


class ItemDoPortfolioSaida(BaseModel):
    id: uuid.UUID
    trilha_id: uuid.UUID
    tipo: TipoDeProducaoDaCriacaoOriginal
    producao: str | None
    referencia: str | None
    validado_em: datetime | None
    autores: list[CreditadoNoPortfolioSaida]
    publica: bool


def _situacao_de_exposicao(sessao_bd: Session, criacao: CriacaoOriginal) -> bool:
    """A mesma condição que a vitrine usa, estendida ao autor individual —
    um só primitivo, dois consumidores (design — decisão 7)."""
    if criacao.guerreiro_id is not None:
        return (
            sessao_bd.query(CriacaoOriginal)
            .filter(
                CriacaoOriginal.id == criacao.id,
                condicao_de_autorizacao_vigente(sessao_bd, CriacaoOriginal.guerreiro_id),
            )
            .first()
            is not None
        )
    tem_integrante_sem_autorizacao = (
        sessao_bd.query(IntegranteDaEquipe.id)
        .filter(IntegranteDaEquipe.equipe_id == criacao.equipe_id)
        .filter(~condicao_de_autorizacao_vigente(sessao_bd, IntegranteDaEquipe.persona_id))
        .first()
        is not None
    )
    return not tem_integrante_sem_autorizacao


def _autores_creditados(
    sessao_bd: Session, criacao: CriacaoOriginal
) -> list[CreditadoNoPortfolioSaida]:
    if criacao.guerreiro_id is not None:
        ids = [criacao.guerreiro_id]
    else:
        ids = [
            integrante.persona_id
            for integrante in sessao_bd.query(IntegranteDaEquipe)
            .filter_by(equipe_id=criacao.equipe_id)
            .all()
        ]
    avatares_e_nicks = buscar_avatares_e_nicks(sessao_bd, ids)
    return [avatares_e_nicks[persona_id] for persona_id in ids if persona_id in avatares_e_nicks]


@roteador.get("/eu/portfolio")
def obter_portfolio_rota(
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> list[ItemDoPortfolioSaida]:
    """`RF-05-43`, `RF-05-44`, `RN-05-21`: as criações validadas do
    Guerreiro(a) em sessão, com a situação de exposição pública derivada da
    mesma condição que a vitrine usa."""
    if contexto.papel != Papel.guerreiro:
        raise PermissaoNegada(mensagem="Só o Guerreiro(a) tem portfólio.")
    criacoes = consultar_portfolio_do_guerreiro(sessao_bd, guerreiro_id=contexto.persona_id)
    return [
        ItemDoPortfolioSaida(
            id=criacao.id,
            trilha_id=criacao.trilha_id,
            tipo=criacao.tipo,
            producao=criacao.producao,
            referencia=criacao.referencia,
            validado_em=criacao.validado_em,
            autores=_autores_creditados(sessao_bd, criacao),
            publica=_situacao_de_exposicao(sessao_bd, criacao),
        )
        for criacao in criacoes
    ]


class AutorNaFilaSaida(CreditadoNoPortfolioSaida):
    # `None` na modalidade individual — só a equipe tem papel por
    # integrante, fixado na homologação (`RN-01-44`, `RF-09-32`).
    papel: str | None


def _autores_da_fila(sessao_bd: Session, criacao: CriacaoOriginal) -> list[AutorNaFilaSaida]:
    if criacao.guerreiro_id is not None:
        avatares_e_nicks = buscar_avatares_e_nicks(sessao_bd, [criacao.guerreiro_id])
        creditado = avatares_e_nicks.get(criacao.guerreiro_id)
        if creditado is None:
            return []
        return [AutorNaFilaSaida(avatar=creditado.avatar, nick=creditado.nick, papel=None)]

    integrantes = sessao_bd.query(IntegranteDaEquipe).filter_by(equipe_id=criacao.equipe_id).all()
    avatares_e_nicks = buscar_avatares_e_nicks(
        sessao_bd, [integrante.persona_id for integrante in integrantes]
    )
    return [
        AutorNaFilaSaida(
            avatar=avatares_e_nicks[integrante.persona_id].avatar,
            nick=avatares_e_nicks[integrante.persona_id].nick,
            papel=integrante.papel,
        )
        for integrante in integrantes
        if integrante.persona_id in avatares_e_nicks
    ]


class CriacaoNaFilaSaida(BaseModel):
    id: uuid.UUID
    trilha_id: uuid.UUID
    trilha_nome: str
    criterio_de_validacao: str
    tipo: TipoDeProducaoDaCriacaoOriginal
    producao: str | None
    referencia: str | None
    autores: list[AutorNaFilaSaida]


@roteador.get("/criacoes/fila")
def listar_fila_de_criacoes_rota(
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> list[CriacaoNaFilaSaida]:
    """`RF-09-31`, `RF-09-32`: as criações entregues das trilhas de que o
    Mestre em sessão é autor, com a trilha, o critério que ele mesmo
    declarou na culminância e a autoria — cada integrante com o papel que
    teve, na modalidade em equipe. Admin lê a fila inteira."""
    if contexto.papel not in (Papel.mestre, Papel.admin):
        raise PermissaoNegada(mensagem="Só Mestre ou Admin leem a fila de criações.")
    operador = sessao_bd.get(Persona, contexto.persona_id)
    criacoes = consultar_fila_do_mestre_autor(sessao_bd, operador=operador)
    saida = []
    for criacao in criacoes:
        trilha = sessao_bd.get(Trilha, criacao.trilha_id)
        culminancia = sessao_bd.query(Culminancia).filter_by(trilha_id=trilha.id).first()
        saida.append(
            CriacaoNaFilaSaida(
                id=criacao.id,
                trilha_id=criacao.trilha_id,
                trilha_nome=trilha.nome,
                criterio_de_validacao=culminancia.criterio_de_validacao
                if culminancia is not None
                else "",
                tipo=criacao.tipo,
                producao=criacao.producao,
                referencia=criacao.referencia,
                autores=_autores_da_fila(sessao_bd, criacao),
            )
        )
    return saida


@roteador.post("/criacoes/{id_da_criacao}/validacao")
def validar_criacao_original_rota(
    id_da_criacao: uuid.UUID,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> CriacaoOriginalSaida:
    """`RF-09-31`: só o Mestre autor da trilha ou o Admin decidem — a posse
    já é de `validar_criacao_original`."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    criacao = _obter_criacao(sessao_bd, id_da_criacao)
    criacao = validar_criacao_original(sessao_bd, operador=operador, criacao=criacao)
    sessao_bd.commit()
    return _saida(criacao)


class DevolverCriacaoEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    motivo: str | None = None


@roteador.post("/criacoes/{id_da_criacao}/devolucao")
def devolver_criacao_original_rota(
    id_da_criacao: uuid.UUID,
    entrada: DevolverCriacaoEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> CriacaoOriginalSaida:
    """`RF-05-42`, `RF-09-34`: exige o motivo, escrito pelo Mestre em
    linguagem simples; a autoria nunca muda (`RN-09-04`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    criacao = _obter_criacao(sessao_bd, id_da_criacao)
    criacao = devolver_criacao_original(
        sessao_bd, operador=operador, criacao=criacao, motivo=entrada.motivo
    )
    sessao_bd.commit()
    return _saida(criacao)
