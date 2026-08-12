import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from ..autenticacao import ContextoDaSessao
from ..banco import obter_sessao
from ..erros import NaoEncontrado
from ..permissoes import Operacao, exigir_permissao
from ..personas.modelo import Papel, Persona
from .regra import cadastrar_responsavel, criar_vinculo

roteador = APIRouter()


class ResponsavelSaida(BaseModel):
    id: uuid.UUID


@roteador.post("/responsaveis", status_code=201)
def cadastrar_responsavel_rota(
    contexto: Annotated[
        ContextoDaSessao, Depends(exigir_permissao(Operacao.cadastro_de_responsavel, "escreve"))
    ],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> ResponsavelSaida:
    """Restrita a Admin e Mestre pela matriz (`RF-01-13`, `RF-01-16`)."""
    criado_por = sessao_bd.get(Persona, contexto.persona_id)
    responsavel = cadastrar_responsavel(sessao_bd, criado_por=criado_por)
    sessao_bd.commit()
    return ResponsavelSaida(id=responsavel.id)


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
