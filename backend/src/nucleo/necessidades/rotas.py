import uuid
from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..autenticacao import ContextoDaSessao, exigir_persona
from ..banco import obter_sessao
from ..personas.modelo import Persona
from ..tempo import DataHoraComFuso
from .regra import (
    NecessidadeDeRecurso,
    consultar_necessidades_do_mestre,
    consultar_necessidades_publicas,
)

roteador = APIRouter()


class NecessidadeDeRecursoSaida(BaseModel):
    aula_id: uuid.UUID
    tipo_de_recurso_id: uuid.UUID
    quantidade_faltante: Decimal
    valor_em_moedas: Decimal | None
    comunidade_virtual_id: uuid.UUID
    ponto_de_apoio_id: uuid.UUID
    inicio_em: DataHoraComFuso
    fim_em: DataHoraComFuso


def _saida(necessidade: NecessidadeDeRecurso) -> NecessidadeDeRecursoSaida:
    return NecessidadeDeRecursoSaida(
        aula_id=necessidade.aula_id,
        tipo_de_recurso_id=necessidade.tipo_de_recurso_id,
        quantidade_faltante=necessidade.quantidade_faltante,
        valor_em_moedas=necessidade.valor_em_moedas,
        comunidade_virtual_id=necessidade.comunidade_virtual_id,
        ponto_de_apoio_id=necessidade.ponto_de_apoio_id,
        inicio_em=necessidade.inicio_em,
        fim_em=necessidade.fim_em,
    )


@roteador.get("/vitrine/necessidades", response_model=list[NecessidadeDeRecursoSaida])
def listar_necessidades_publicas_rota(
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> list[NecessidadeDeRecursoSaida]:
    """Pública, sem credencial de persona e sob chave de aplicação, como
    toda leitura do prefixo `/vitrine` (`RF-07-27`, `RF-03-47`, `RF-01-02`,
    `RF-01-16`)."""
    necessidades = consultar_necessidades_publicas(sessao_bd)
    return [_saida(necessidade) for necessidade in necessidades]


@roteador.get("/necessidades/minhas", response_model=list[NecessidadeDeRecursoSaida])
def listar_necessidades_do_mestre_rota(
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> list[NecessidadeDeRecursoSaida]:
    """Restrita ao Mestre em sessão, filtrada pela comunidade a que ele está
    vinculado — fora do prefixo `/vitrine`, que o núcleo reserva à leitura
    sem persona (`RF-07-27`, design — Decisions 5)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    necessidades = consultar_necessidades_do_mestre(sessao_bd, operador=operador)
    return [_saida(necessidade) for necessidade in necessidades]
