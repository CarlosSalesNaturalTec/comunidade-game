import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from ..autenticacao import ContextoDaSessao, exigir_persona
from ..banco import obter_sessao
from ..erros import NaoEncontrado
from ..personas.modelo import Persona
from ..trilhas.modelo import Missao, Trilha
from .modelo import EtiquetaOds
from .regra import (
    EtiquetaDeclarada,
    substituir_etiquetas_da_missao,
    substituir_etiquetas_da_trilha,
)

roteador = APIRouter()


class EtiquetaOdsSaida(BaseModel):
    id: uuid.UUID
    objetivo: int
    meta: str | None
    trilha_id: uuid.UUID | None
    missao_id: uuid.UUID | None


def saida_da_etiqueta(etiqueta: EtiquetaOds) -> EtiquetaOdsSaida:
    return EtiquetaOdsSaida(
        id=etiqueta.id,
        objetivo=etiqueta.objetivo,
        meta=etiqueta.meta,
        trilha_id=etiqueta.trilha_id,
        missao_id=etiqueta.missao_id,
    )


class EtiquetaEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    # Sem faixa declarada aqui de propósito: quem recusa o objetivo fora de
    # 1 a 18 é a regra, para que a recusa valha em todo caminho de escrita e
    # não só nesta porta (design — decisão 4).
    objetivo: int | None = None
    meta: str | None = None


class SubstituirEtiquetasEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    etiquetas: list[EtiquetaEntrada]


def _declaradas(entrada: SubstituirEtiquetasEntrada) -> list[EtiquetaDeclarada]:
    return [
        EtiquetaDeclarada(objetivo=etiqueta.objetivo, meta=etiqueta.meta)
        for etiqueta in entrada.etiquetas
    ]


@roteador.post("/trilhas/{id_da_trilha}/ods")
def substituir_etiquetas_da_trilha_rota(
    id_da_trilha: uuid.UUID,
    entrada: SubstituirEtiquetasEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> list[EtiquetaOdsSaida]:
    """`RF-09-92`: recebe a lista completa de etiquetas da trilha e
    substitui por ela o conjunto que havia, devolvendo o resultante. Uma
    rota só para declarar e para alterar, idempotente; lista vazia deixa a
    trilha sem etiqueta, situação legal no Ciclo 01 (`RF-09-93`). A autoria
    estrita e a recusa de objetivo fora de 1 a 18 já são da regra (design —
    decisões 2, 3 e 4)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    trilha = sessao_bd.get(Trilha, id_da_trilha)
    if trilha is None:
        raise NaoEncontrado(mensagem="Trilha não encontrada.")
    etiquetas = substituir_etiquetas_da_trilha(
        sessao_bd, operador=operador, trilha=trilha, etiquetas=_declaradas(entrada)
    )
    sessao_bd.commit()
    return [saida_da_etiqueta(etiqueta) for etiqueta in etiquetas]


@roteador.post("/missoes/{id_da_missao}/ods")
def substituir_etiquetas_da_missao_rota(
    id_da_missao: uuid.UUID,
    entrada: SubstituirEtiquetasEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> list[EtiquetaOdsSaida]:
    """`RF-09-98`: o mesmo da trilha, escopado à missão — a substituição
    aqui nunca alcança as etiquetas da trilha, o que preserva a precedência
    da etiqueta própria da missão (`RF-01-45`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    missao = sessao_bd.get(Missao, id_da_missao)
    if missao is None:
        raise NaoEncontrado(mensagem="Missão não encontrada.")
    etiquetas = substituir_etiquetas_da_missao(
        sessao_bd, operador=operador, missao=missao, etiquetas=_declaradas(entrada)
    )
    sessao_bd.commit()
    return [saida_da_etiqueta(etiqueta) for etiqueta in etiquetas]
