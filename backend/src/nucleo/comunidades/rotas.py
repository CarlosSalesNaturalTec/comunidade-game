import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from ..autenticacao import ContextoDaSessao, exigir_persona
from ..banco import obter_sessao
from ..personas.modelo import Persona
from .regra import criar_comunidade

roteador = APIRouter()


class CriarComunidadeEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nome: str = Field(min_length=1)
    localizacao: str = Field(min_length=1)
    granularidade_maxima: str = Field(min_length=1)


class ComunidadeSaida(BaseModel):
    id: uuid.UUID
    nome: str
    localizacao: str
    granularidade_maxima: str
    admin_criador_id: uuid.UUID | None
    criada_em: datetime


@roteador.post("/comunidades", status_code=201)
def criar_comunidade_rota(
    entrada: CriarComunidadeEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> ComunidadeSaida:
    """Restrita ao Admin — a recusa de qualquer outro papel é 403,
    devolvida por `criar_comunidade` (`RF-08-01`, `RN-08-01`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    comunidade = criar_comunidade(
        sessao_bd,
        operador=operador,
        nome=entrada.nome,
        localizacao=entrada.localizacao,
        granularidade_maxima=entrada.granularidade_maxima,
    )
    sessao_bd.commit()
    return ComunidadeSaida(
        id=comunidade.id,
        nome=comunidade.nome,
        localizacao=comunidade.localizacao,
        granularidade_maxima=comunidade.granularidade_maxima,
        admin_criador_id=comunidade.admin_criador_id,
        criada_em=comunidade.criada_em,
    )
