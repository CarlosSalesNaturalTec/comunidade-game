import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..autenticacao import ContextoDaSessao, exigir_persona
from ..banco import obter_sessao
from ..erros import NaoEncontrado
from ..personas.modelo import Persona
from ..trilhas.modelo import Missao
from .modelo import BibliografiaDaMissao
from .regra import criar_bibliografia

roteador = APIRouter()


class BibliografiaSaida(BaseModel):
    id: uuid.UUID
    missao_id: uuid.UUID
    titulo: str
    capitulo: str
    item_patrimonial_id: uuid.UUID | None


def saida_da_bibliografia(bibliografia: BibliografiaDaMissao) -> BibliografiaSaida:
    return BibliografiaSaida(
        id=bibliografia.id,
        missao_id=bibliografia.missao_id,
        titulo=bibliografia.titulo,
        capitulo=bibliografia.capitulo,
        item_patrimonial_id=bibliografia.item_patrimonial_id,
    )


def _obter_missao(sessao_bd: Session, id_da_missao: uuid.UUID) -> Missao:
    missao = sessao_bd.get(Missao, id_da_missao)
    if missao is None:
        raise NaoEncontrado(mensagem="Missão não encontrada.")
    return missao


class CriarBibliografiaEntrada(BaseModel):
    # Sem `extra="forbid"`, ao contrário das demais entradas do núcleo: o
    # cliente pode enviar `apoiador` e o núcleo o ignora — o crédito nunca é
    # digitado, só derivado na leitura (`RF-09-23`, PRD-09 §8).

    titulo: str
    capitulo: str
    item_patrimonial_id: uuid.UUID | None = None


@roteador.post("/missoes/{id_da_missao}/bibliografia", status_code=201)
def criar_bibliografia_rota(
    id_da_missao: uuid.UUID,
    entrada: CriarBibliografiaEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> BibliografiaSaida:
    """`RF-09-21`: a autoria estrita, a exigência de título e capítulo e o
    exemplar opcional já são de `criar_bibliografia`."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    missao = _obter_missao(sessao_bd, id_da_missao)
    bibliografia = criar_bibliografia(
        sessao_bd,
        operador=operador,
        missao=missao,
        titulo=entrada.titulo,
        capitulo=entrada.capitulo,
        item_patrimonial_id=entrada.item_patrimonial_id,
    )
    sessao_bd.commit()
    return saida_da_bibliografia(bibliografia)
