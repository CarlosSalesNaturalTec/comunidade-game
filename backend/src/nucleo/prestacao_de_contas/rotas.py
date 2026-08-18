import uuid
from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..banco import obter_sessao
from .regra import consumo_por_aula_e_comunidade, movimentado_total_e_por_provedor

roteador = APIRouter()


class MovimentadoPorProvedorSaida(BaseModel):
    provedor_id: uuid.UUID
    movimentado_em_moedas: Decimal


class PrestacaoDeContasSaida(BaseModel):
    movimentado_total_em_moedas: Decimal
    por_provedor: list[MovimentadoPorProvedorSaida]


@roteador.get("/prestacao-de-contas")
def prestacao_de_contas(
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> PrestacaoDeContasSaida:
    """Pública, sem `exigir_persona`: o movimentado total e por provedor,
    derivado dos lançamentos no momento da leitura, sem fechamento
    periódico (`RF-07-16`, `RN-07-05`, `RN-07-31`, PRD-07 §9)."""
    total, por_provedor = movimentado_total_e_por_provedor(sessao_bd)
    return PrestacaoDeContasSaida(
        movimentado_total_em_moedas=total,
        por_provedor=[
            MovimentadoPorProvedorSaida(
                provedor_id=linha.provedor_id, movimentado_em_moedas=linha.movimentado_em_moedas
            )
            for linha in por_provedor
        ],
    )


class ConsumoDaAulaSaida(BaseModel):
    aula_id: uuid.UUID
    comunidade_virtual_id: uuid.UUID
    consumo_em_moedas: Decimal


class ConsumoDaComunidadeSaida(BaseModel):
    comunidade_virtual_id: uuid.UUID
    consumo_em_moedas: Decimal


class PrestacaoDeContasDasAulasSaida(BaseModel):
    aulas: list[ConsumoDaAulaSaida]
    por_comunidade: list[ConsumoDaComunidadeSaida]


@roteador.get("/prestacao-de-contas/aulas")
def prestacao_de_contas_das_aulas(
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> PrestacaoDeContasDasAulasSaida:
    """Pública, sem `exigir_persona`: o consumo por aula e por comunidade,
    pelo valor que cada débito gravou no ato — aula sem baixa não aparece
    (`RF-07-16`, `RN-07-05`, `RN-07-33`, `RN-07-36`, PRD-07 §9)."""
    aulas, comunidades = consumo_por_aula_e_comunidade(sessao_bd)
    return PrestacaoDeContasDasAulasSaida(
        aulas=[
            ConsumoDaAulaSaida(
                aula_id=linha.aula_id,
                comunidade_virtual_id=linha.comunidade_virtual_id,
                consumo_em_moedas=linha.consumo_em_moedas,
            )
            for linha in aulas
        ],
        por_comunidade=[
            ConsumoDaComunidadeSaida(
                comunidade_virtual_id=linha.comunidade_virtual_id,
                consumo_em_moedas=linha.consumo_em_moedas,
            )
            for linha in comunidades
        ],
    )
