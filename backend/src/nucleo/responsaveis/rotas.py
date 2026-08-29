import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from ..autenticacao import ContextoDaSessao
from ..banco import obter_sessao
from ..erros import NaoEncontrado
from ..paginacao import PaginaDeResultado, ParametrosDeListagem, contrato_de_listagem
from ..permissoes import Operacao, exigir_permissao
from ..personas.modelo import Nick, Papel, Persona
from .regra import cadastrar_responsavel, criar_vinculo, guerreiros_vinculaveis

roteador = APIRouter()


class GuerreiroVinculavelSaida(BaseModel):
    id: uuid.UUID
    nick: str
    avatar: str


def _saida_do_guerreiro_vinculavel(
    persona: Persona, sessao_bd: Session
) -> GuerreiroVinculavelSaida:
    nick = sessao_bd.query(Nick).filter_by(persona_id=persona.id).first()
    return GuerreiroVinculavelSaida(
        id=persona.id,
        nick=nick.valor if nick is not None else "",
        avatar=persona.avatar or "",
    )


@roteador.get("/guerreiros/vinculaveis", response_model=PaginaDeResultado[GuerreiroVinculavelSaida])
def listar_guerreiros_vinculaveis_rota(
    parametros: Annotated[ParametrosDeListagem, Depends(contrato_de_listagem())],
    contexto: Annotated[
        ContextoDaSessao,
        Depends(exigir_permissao(Operacao.vinculo_com_guerreiros_e_guerreiras, "le")),
    ],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> PaginaDeResultado[GuerreiroVinculavelSaida]:
    """Restrita ao Mestre pela matriz — nick e avatar dos Guerreiros e
    Guerreiras ativos da comunidade do seu vínculo vigente, nunca imagem
    real, nome civil ou contato (`RF-09-62`, `RN-01-20`, `RN-09-18`)."""
    mestre = sessao_bd.get(Persona, contexto.persona_id)
    personas, proximo_cursor = guerreiros_vinculaveis(
        sessao_bd, mestre=mestre, parametros=parametros
    )
    return PaginaDeResultado(
        itens=[_saida_do_guerreiro_vinculavel(persona, sessao_bd) for persona in personas],
        proximo_cursor=proximo_cursor,
    )


class CadastrarResponsavelEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nome: str = Field(min_length=1)


class ResponsavelSaida(BaseModel):
    id: uuid.UUID
    nome: str


@roteador.post("/responsaveis", status_code=201)
def cadastrar_responsavel_rota(
    entrada: CadastrarResponsavelEntrada,
    contexto: Annotated[
        ContextoDaSessao, Depends(exigir_permissao(Operacao.cadastro_de_responsavel, "escreve"))
    ],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> ResponsavelSaida:
    """Restrita a Admin e Mestre pela matriz (`RF-01-13`, `RF-01-16`). O
    nome é o conteúdo mínimo do responsável (`RF-04-60`, design —
    decisão 1)."""
    criado_por = sessao_bd.get(Persona, contexto.persona_id)
    responsavel = cadastrar_responsavel(sessao_bd, criado_por=criado_por, nome=entrada.nome)
    sessao_bd.commit()
    return ResponsavelSaida(id=responsavel.id, nome=responsavel.nome or "")


class CriarVinculoEntrada(BaseModel):
    guerreiro_id: uuid.UUID
    grau_de_parentesco: str = Field(min_length=1)


class VinculoSaida(BaseModel):
    id: uuid.UUID
    responsavel_id: uuid.UUID
    guerreiro_id: uuid.UUID
    grau_de_parentesco: str
    inicio: datetime


@roteador.post("/responsaveis/{id}/vinculos", status_code=201)
def criar_vinculo_rota(
    id: uuid.UUID,
    entrada: CriarVinculoEntrada,
    contexto: Annotated[
        ContextoDaSessao,
        Depends(exigir_permissao(Operacao.vinculo_com_guerreiros_e_guerreiras, "escreve")),
    ],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> VinculoSaida:
    """Restrita a Admin e Mestre pela matriz (`RF-01-13`, `RF-01-16`). O
    vínculo só alcança Guerreiro(a) já cadastrado — nenhuma persona nasce
    aqui (`RN-01-20`).
    """
    responsavel = sessao_bd.get(Persona, id)
    if responsavel is None or responsavel.papel != Papel.responsavel:
        raise NaoEncontrado(mensagem="Responsável não encontrado.", campo="id")

    cadastrado_por = sessao_bd.get(Persona, contexto.persona_id)
    vinculo = criar_vinculo(
        sessao_bd,
        responsavel=responsavel,
        guerreiro_id=entrada.guerreiro_id,
        grau_de_parentesco=entrada.grau_de_parentesco,
        cadastrado_por=cadastrado_por,
    )
    sessao_bd.commit()
    return VinculoSaida(
        id=vinculo.id,
        responsavel_id=vinculo.responsavel_id,
        guerreiro_id=vinculo.guerreiro_id,
        grau_de_parentesco=vinculo.grau_de_parentesco,
        inicio=vinculo.inicio,
    )
