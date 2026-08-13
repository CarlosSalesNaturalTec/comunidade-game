import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, UploadFile
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from ..armazenamento.fabrica import dependencia_de_armazenamento
from ..armazenamento.porta import PortaDeArmazenamento
from ..autenticacao import ContextoDaSessao
from ..banco import obter_sessao
from ..permissoes import Operacao, exigir_qualquer_permissao
from ..personas.modelo import Persona
from ..protecao.freio import exigir_freio_por_origem
from .modelo import PretensaoDeParticipacao, TipoDeAlvo
from .regra import (
    registrar_solicitacao_de_chave,
    registrar_solicitacao_de_dados,
    registrar_solicitacao_de_participacao,
    registrar_sugestao,
)

roteador = APIRouter()

# `RF-01-25`: as três operações de proposta das personas — todas levam à
# mesma rota de sugestão e proposta.
_OPERACOES_DE_SUGESTAO = frozenset(
    {
        Operacao.suas_sugestoes,
        Operacao.solicitacoes_e_propostas,
        Operacao.propostas_de_evolucao,
    }
)


class SolicitacaoSaida(BaseModel):
    """As três rotas de envio devolvem só o registro e o prazo — nunca
    dado, arquivo, chave ou acesso (`RN-01-03`, `RN-01-25`, `RN-01-37`)."""

    id: uuid.UUID
    prazo: datetime


@roteador.post("/solicitacoes-de-participacao", status_code=201)
def registrar_solicitacao_de_participacao_rota(
    nome_ou_razao_social: Annotated[str, Form()],
    email: Annotated[str, Form()],
    whatsapp: Annotated[str, Form()],
    pretensao: Annotated[PretensaoDeParticipacao, Form()],
    apresentacao: Annotated[str, Form()],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    armazenamento: Annotated[PortaDeArmazenamento, Depends(dependencia_de_armazenamento)],
    _freio: Annotated[None, Depends(exigir_freio_por_origem("formulario_participacao"))],
    instituicao: Annotated[str | None, Form()] = None,
    links: Annotated[str | None, Form()] = None,
    aporte_declarado: Annotated[str | None, Form()] = None,
    comprovante: Annotated[UploadFile | None, File()] = None,
) -> SolicitacaoSaida:
    """Pública, sem credencial de persona (`RF-01-25`, design — Decisions).
    O pré-cadastro do Apoiador entra aqui, com aporte declarado e
    comprovante; nenhum caminho cria cadastro (`RN-01-03`, `RN-01-28`)."""
    conteudo = comprovante.file.read() if comprovante is not None else None
    solicitacao = registrar_solicitacao_de_participacao(
        sessao_bd,
        nome_ou_razao_social=nome_ou_razao_social,
        email=email,
        whatsapp=whatsapp,
        pretensao=pretensao,
        apresentacao=apresentacao,
        instituicao=instituicao,
        links=links,
        aporte_declarado=aporte_declarado,
        comprovante_conteudo=conteudo,
        comprovante_nome_original=comprovante.filename if comprovante is not None else None,
        comprovante_tipo=comprovante.content_type if comprovante is not None else None,
        armazenamento=armazenamento,
    )
    sessao_bd.commit()
    return SolicitacaoSaida(id=solicitacao.id, prazo=solicitacao.prazo)


class SolicitacaoDeDadosEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    solicitante: str = Field(min_length=1)
    instituicao: str = Field(min_length=1)
    email: str = Field(min_length=1)
    finalidade_declarada: str = Field(min_length=1)
    recorte_pedido: str = Field(min_length=1)


@roteador.post("/solicitacoes-de-dados", status_code=201)
def registrar_solicitacao_de_dados_rota(
    entrada: SolicitacaoDeDadosEntrada,
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    _freio: Annotated[None, Depends(exigir_freio_por_origem("formulario_dados"))],
) -> SolicitacaoSaida:
    """Pública, sem credencial de persona (`RF-01-46`). Sem finalidade
    declarada, o núcleo recusa o registro."""
    solicitacao = registrar_solicitacao_de_dados(
        sessao_bd,
        solicitante=entrada.solicitante,
        instituicao=entrada.instituicao,
        email=entrada.email,
        finalidade_declarada=entrada.finalidade_declarada,
        recorte_pedido=entrada.recorte_pedido,
    )
    sessao_bd.commit()
    return SolicitacaoSaida(id=solicitacao.id, prazo=solicitacao.prazo)


class SolicitacaoDeChaveEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    solicitante: str = Field(min_length=1)
    contato: str = Field(min_length=1)
    o_que_pretende_construir: str = Field(min_length=1)
    instituicao: str | None = None


@roteador.post("/solicitacoes-de-chave", status_code=201)
def registrar_solicitacao_de_chave_rota(
    entrada: SolicitacaoDeChaveEntrada,
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> SolicitacaoSaida:
    """Pública, sem credencial de persona (`RF-01-49`). Sem freio por
    origem — nova solicitação é sempre possível (`RN-01-46`) —, protegida
    só pela cota da chave da aplicação que chama."""
    solicitacao = registrar_solicitacao_de_chave(
        sessao_bd,
        solicitante=entrada.solicitante,
        contato=entrada.contato,
        o_que_pretende_construir=entrada.o_que_pretende_construir,
        instituicao=entrada.instituicao,
    )
    sessao_bd.commit()
    return SolicitacaoSaida(id=solicitacao.id, prazo=solicitacao.prazo)


class SugestaoEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    alvo_tipo: TipoDeAlvo
    texto: str = Field(min_length=1)
    alvo_id: uuid.UUID | None = None


@roteador.post("/sugestoes", status_code=201)
def registrar_sugestao_rota(
    entrada: SugestaoEntrada,
    contexto: Annotated[
        ContextoDaSessao, Depends(exigir_qualquer_permissao(_OPERACOES_DE_SUGESTAO, "escreve"))
    ],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> SolicitacaoSaida:
    """Autenticada — recusa com 401 quem não tem credencial de persona
    (`RF-01-03`). Só texto: não há campo de áudio (03 §12.2)."""
    autor = sessao_bd.get(Persona, contexto.persona_id)
    sugestao = registrar_sugestao(
        sessao_bd,
        autor=autor,
        alvo_tipo=entrada.alvo_tipo,
        texto=entrada.texto,
        alvo_id=entrada.alvo_id,
    )
    sessao_bd.commit()
    return SolicitacaoSaida(id=sugestao.id, prazo=sugestao.prazo)
