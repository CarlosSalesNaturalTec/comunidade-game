import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from ..autenticacao import ContextoDaSessao, exigir_persona
from ..banco import obter_sessao
from ..erros import ErroDeValidacao, NaoEncontrado, PermissaoNegada
from ..fila.modelo import SituacaoDaSolicitacao
from ..fila.rotas import SolicitacaoSaida
from ..permissoes import Operacao, exigir_permissao
from ..personas.modelo import Nick, Papel, Persona
from .modelo import SolicitacaoDoResponsavel, TipoDeSolicitacaoDoResponsavel
from .regra import (
    abrir_solicitacao,
    esta_em_atraso,
    listar_fila_do_admin,
    listar_minhas_solicitacoes,
    registrar_tratamento,
)

roteador = APIRouter()


def _nick_de(sessao: Session, persona_id: uuid.UUID) -> str | None:
    registro = sessao.query(Nick).filter_by(persona_id=persona_id).first()
    return registro.valor if registro is not None else None


class AbrirSolicitacaoEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    guerreiro_id: uuid.UUID
    tipo: TipoDeSolicitacaoDoResponsavel
    texto: str = Field(min_length=1)


@roteador.post("/solicitacoes", status_code=201)
def abrir_solicitacao_rota(
    entrada: AbrirSolicitacaoEntrada,
    contexto: Annotated[
        ContextoDaSessao, Depends(exigir_permissao(Operacao.solicitacoes_e_propostas, "escreve"))
    ],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> SolicitacaoSaida:
    """Restrita ao responsável (`RF-13-22`, `RF-13-24`). A resposta traz só
    o protocolo — o próprio identificador do registro — e o prazo, nada
    mais (design — decisão 4)."""
    responsavel = sessao_bd.get(Persona, contexto.persona_id)
    solicitacao = abrir_solicitacao(
        sessao_bd,
        responsavel=responsavel,
        guerreiro_id=entrada.guerreiro_id,
        tipo=entrada.tipo,
        texto=entrada.texto,
    )
    sessao_bd.commit()
    return SolicitacaoSaida(id=solicitacao.id, prazo=solicitacao.prazo)


class MinhaSolicitacaoSaida(BaseModel):
    id: uuid.UUID
    guerreiro_id: uuid.UUID
    tipo: TipoDeSolicitacaoDoResponsavel
    texto: str
    situacao: SituacaoDaSolicitacao
    prazo: datetime
    em_atraso: bool
    desfecho: str | None
    tratado_em: datetime | None


def _saida_para_responsavel(solicitacao: SolicitacaoDoResponsavel) -> MinhaSolicitacaoSaida:
    return MinhaSolicitacaoSaida(
        id=solicitacao.id,
        guerreiro_id=solicitacao.guerreiro_id,
        tipo=solicitacao.tipo,
        texto=solicitacao.texto,
        situacao=solicitacao.situacao,
        prazo=solicitacao.prazo,
        em_atraso=esta_em_atraso(solicitacao),
        desfecho=solicitacao.desfecho,
        tratado_em=solicitacao.tratado_em,
    )


@roteador.get("/eu/solicitacoes")
def minhas_solicitacoes_rota(
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> list[MinhaSolicitacaoSaida]:
    """Restrita ao responsável — só as próprias (`RF-13-25`, `RF-13-26`,
    `RN-13-13`), no mesmo molde de `/eu/recompensas`."""
    if contexto.papel != Papel.responsavel:
        raise PermissaoNegada(mensagem="Só o responsável lê as próprias solicitações.")

    solicitacoes = listar_minhas_solicitacoes(sessao_bd, responsavel_id=contexto.persona_id)
    return [_saida_para_responsavel(solicitacao) for solicitacao in solicitacoes]


class AdminSolicitacaoSaida(BaseModel):
    """A fila do Admin traz também o nick do responsável e o do
    Guerreiro(a), porque a gestão não tem rota que liste responsáveis
    (design — decisão 7)."""

    id: uuid.UUID
    responsavel_id: uuid.UUID
    nick_do_responsavel: str | None
    guerreiro_id: uuid.UUID
    nick_do_guerreiro: str | None
    tipo: TipoDeSolicitacaoDoResponsavel
    texto: str
    situacao: SituacaoDaSolicitacao
    prazo: datetime
    em_atraso: bool
    tratado_por_id: uuid.UUID | None
    desfecho: str | None
    tratado_em: datetime | None


def _saida_para_admin(
    sessao: Session, solicitacao: SolicitacaoDoResponsavel
) -> AdminSolicitacaoSaida:
    return AdminSolicitacaoSaida(
        id=solicitacao.id,
        responsavel_id=solicitacao.responsavel_id,
        nick_do_responsavel=_nick_de(sessao, solicitacao.responsavel_id),
        guerreiro_id=solicitacao.guerreiro_id,
        nick_do_guerreiro=_nick_de(sessao, solicitacao.guerreiro_id),
        tipo=solicitacao.tipo,
        texto=solicitacao.texto,
        situacao=solicitacao.situacao,
        prazo=solicitacao.prazo,
        em_atraso=esta_em_atraso(solicitacao),
        tratado_por_id=solicitacao.tratado_por_id,
        desfecho=solicitacao.desfecho,
        tratado_em=solicitacao.tratado_em,
    )


@roteador.get("/solicitacoes-do-responsavel")
def listar_fila_do_admin_rota(
    contexto: Annotated[ContextoDaSessao, Depends(exigir_permissao(Operacao.tudo, "le"))],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> list[AdminSolicitacaoSaida]:
    """Restrita a Admin (`RF-02-23`, `RF-01-16`), da mais antiga para a mais
    recente."""
    solicitacoes = listar_fila_do_admin(sessao_bd)
    return [_saida_para_admin(sessao_bd, solicitacao) for solicitacao in solicitacoes]


class TratarSolicitacaoEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    situacao: str = Field(min_length=1)
    desfecho: str | None = None


@roteador.post("/solicitacoes-do-responsavel/{id_da_solicitacao}/tratamento")
def registrar_tratamento_rota(
    id_da_solicitacao: uuid.UUID,
    entrada: TratarSolicitacaoEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_permissao(Operacao.tudo, "escreve"))],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> AdminSolicitacaoSaida:
    """Restrita a Admin (`RF-02-24`, `RF-01-16`). Grava quem tratou e
    quando; a guarda de segundo desfecho está na regra (`RN-13-14`)."""
    solicitacao = sessao_bd.get(SolicitacaoDoResponsavel, id_da_solicitacao)
    if solicitacao is None:
        raise NaoEncontrado(mensagem="Solicitação do responsável não encontrada.")

    try:
        situacao_valida = SituacaoDaSolicitacao(entrada.situacao)
    except ValueError as exc:
        raise ErroDeValidacao(
            mensagem="Desfecho precisa ser aceita ou recusada.", campo="situacao"
        ) from exc

    tratado_por = sessao_bd.get(Persona, contexto.persona_id)
    solicitacao = registrar_tratamento(
        sessao_bd,
        solicitacao,
        situacao=situacao_valida,
        tratado_por=tratado_por,
        desfecho=entrada.desfecho,
    )
    sessao_bd.commit()
    return _saida_para_admin(sessao_bd, solicitacao)
