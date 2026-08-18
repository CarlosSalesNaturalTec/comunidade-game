import uuid
from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from ..autenticacao import ContextoDaSessao, exigir_persona
from ..banco import obter_sessao
from ..personas.modelo import Persona
from .modelo import Lancamento
from .regra import lancar_ajuste

roteador = APIRouter()


class LancamentoSaida(BaseModel):
    id: uuid.UUID
    natureza: str
    tipo_de_recurso_id: uuid.UUID
    ponto_de_apoio_id: uuid.UUID
    quantidade: Decimal
    valor_em_moedas: Decimal
    lancamento_original_id: uuid.UUID | None
    motivo_do_ajuste: str | None


def _saida(lancamento: Lancamento) -> LancamentoSaida:
    return LancamentoSaida(
        id=lancamento.id,
        natureza=lancamento.natureza.value,
        tipo_de_recurso_id=lancamento.tipo_de_recurso_id,
        ponto_de_apoio_id=lancamento.ponto_de_apoio_id,
        quantidade=lancamento.quantidade,
        valor_em_moedas=lancamento.valor_em_moedas,
        lancamento_original_id=lancamento.lancamento_original_id,
        motivo_do_ajuste=lancamento.motivo_do_ajuste,
    )


class LancarAjusteEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    quantidade: Decimal
    valor_em_moedas: Decimal
    motivo: str = Field(min_length=1)


@roteador.post("/lancamentos/{id_do_lancamento}/ajuste", status_code=201)
def lancar_ajuste_rota(
    id_do_lancamento: uuid.UUID,
    entrada: LancarAjusteEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> LancamentoSaida:
    """Restrita ao Admin — a única via de correção de um lançamento errado,
    que nunca é alterado nem removido (`RF-07-19`, `RN-07-15`, PRD-07 §9).
    Não há `PUT` nem `PATCH` declarados sobre `lancamento`: o FastAPI
    responde 405 a método não previsto (design — Decisions 4)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    lancamento_original = sessao_bd.get(Lancamento, id_do_lancamento)
    ajuste = lancar_ajuste(
        sessao_bd,
        operador=operador,
        lancamento_original=lancamento_original,
        quantidade=entrada.quantidade,
        valor_em_moedas=entrada.valor_em_moedas,
        motivo=entrada.motivo,
    )
    sessao_bd.commit()
    return _saida(ajuste)
