import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from ..autenticacao import ContextoDaSessao
from ..banco import obter_sessao
from ..erros import NaoEncontrado
from ..permissoes import Operacao, exigir_permissao
from ..personas.modelo import Papel, Persona
from .modelo import OrigemDoFimDeVinculo
from .regra import encerrar_vinculo

roteador = APIRouter()


class EncerrarVinculoEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    motivo: str = Field(min_length=1)


class FimDeVinculoSaida(BaseModel):
    id: uuid.UUID
    guerreiro_id: uuid.UUID
    origem: OrigemDoFimDeVinculo
    encerrado_por: uuid.UUID | None
    motivo: str
    momento: datetime


@roteador.post("/guerreiros/{id}/fim-de-vinculo", status_code=201)
def encerrar_vinculo_rota(
    id: uuid.UUID,
    entrada: EncerrarVinculoEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_permissao(Operacao.tudo, "escreve"))],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> FimDeVinculoSaida:
    """Restrita ao Admin por `Operacao.tudo` — nenhuma outra persona tem a
    operação na matriz, e a negação por padrão devolve 403 (`RF-13-44`).
    """
    guerreiro = sessao_bd.get(Persona, id)
    if guerreiro is None or guerreiro.papel != Papel.guerreiro:
        raise NaoEncontrado(mensagem="Guerreiro(a) não encontrado.", campo="id")

    admin = sessao_bd.get(Persona, contexto.persona_id)
    fim = encerrar_vinculo(
        sessao_bd, guerreiro=guerreiro, encerrado_por=admin, motivo=entrada.motivo
    )
    sessao_bd.commit()
    return FimDeVinculoSaida(
        id=fim.id,
        guerreiro_id=fim.guerreiro_id,
        origem=fim.origem,
        encerrado_por=fim.encerrado_por,
        motivo=fim.motivo,
        momento=fim.momento,
    )
