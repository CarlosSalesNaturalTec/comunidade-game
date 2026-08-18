import uuid
from datetime import date
from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from ..autenticacao import ContextoDaSessao, exigir_persona
from ..banco import obter_sessao
from ..personas.modelo import Persona
from .modelo import TipoDeRecurso, ValorDeReferencia
from .regra import cadastrar_tipo_de_recurso, registrar_valor_de_referencia

roteador = APIRouter()


class TipoDeRecursoSaida(BaseModel):
    id: uuid.UUID
    nome: str
    natureza: str
    unidade: str
    exige_comprovante: bool
    valor_em_moedas: Decimal
    vigencia_inicio: date


def _saida(tipo: TipoDeRecurso, valor: ValorDeReferencia) -> TipoDeRecursoSaida:
    return TipoDeRecursoSaida(
        id=tipo.id,
        nome=tipo.nome,
        natureza=tipo.natureza.value,
        unidade=tipo.unidade,
        exige_comprovante=tipo.exige_comprovante,
        valor_em_moedas=valor.valor_em_moedas,
        vigencia_inicio=valor.vigencia_inicio,
    )


class CadastrarTipoDeRecursoEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nome: str = Field(min_length=1)
    natureza: str = Field(min_length=1)
    unidade: str = Field(min_length=1)
    valor_em_moedas: Decimal
    vigencia_inicio: date
    exige_comprovante: bool = False


@roteador.post("/tipos-de-recurso", status_code=201)
def cadastrar_tipo_de_recurso_rota(
    entrada: CadastrarTipoDeRecursoEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> TipoDeRecursoSaida:
    """Restrita ao Admin — cadastra o tipo e abre a primeira vigência do
    valor de referência num único ato (`RF-07-01`, `RF-07-02`, PRD-07 §9)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    tipo = cadastrar_tipo_de_recurso(
        sessao_bd,
        operador=operador,
        nome=entrada.nome,
        natureza=entrada.natureza,
        unidade=entrada.unidade,
        exige_comprovante=entrada.exige_comprovante,
    )
    valor = registrar_valor_de_referencia(
        sessao_bd,
        operador=operador,
        tipo=tipo,
        valor_em_moedas=entrada.valor_em_moedas,
        vigencia_inicio=entrada.vigencia_inicio,
    )
    sessao_bd.commit()
    return _saida(tipo, valor)
