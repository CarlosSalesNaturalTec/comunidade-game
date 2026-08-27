import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from ..autenticacao import ContextoDaSessao, exigir_persona
from ..banco import obter_sessao
from ..erros import NaoEncontrado
from ..personas.modelo import Persona
from ..trilhas.modelo import Trilha
from .modelo import Culminancia, ModalidadeDaCulminancia
from .regra import declarar_culminancia

roteador = APIRouter()


class CulminanciaSaida(BaseModel):
    id: uuid.UUID
    trilha_id: uuid.UUID
    descricao: str
    modalidade: ModalidadeDaCulminancia
    criterio_de_validacao: str


def saida_da_culminancia(culminancia: Culminancia) -> CulminanciaSaida:
    return CulminanciaSaida(
        id=culminancia.id,
        trilha_id=culminancia.trilha_id,
        descricao=culminancia.descricao,
        modalidade=culminancia.modalidade,
        criterio_de_validacao=culminancia.criterio_de_validacao,
    )


class DeclararCulminanciaEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    descricao: str | None = None
    modalidade: str | None = None
    criterio_de_validacao: str | None = None


@roteador.post("/trilhas/{id_da_trilha}/culminancia")
def declarar_culminancia_rota(
    id_da_trilha: uuid.UUID,
    entrada: DeclararCulminanciaEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> CulminanciaSaida:
    """`RF-09-29`, `RF-09-30`: privativa do Mestre autor — a posse estrita e
    as recusas de modalidade e critério já são de `declarar_culminancia`; a
    segunda declaração substitui a anterior (design — decisões 1)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    trilha = sessao_bd.get(Trilha, id_da_trilha)
    if trilha is None:
        raise NaoEncontrado(mensagem="Trilha não encontrada.")
    culminancia = declarar_culminancia(
        sessao_bd,
        trilha=trilha,
        operador=operador,
        descricao=entrada.descricao,
        modalidade=entrada.modalidade,
        criterio_de_validacao=entrada.criterio_de_validacao,
    )
    sessao_bd.commit()
    return saida_da_culminancia(culminancia)
