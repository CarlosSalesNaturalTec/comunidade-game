import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from ..autenticacao import ContextoDaSessao, exigir_persona
from ..banco import obter_sessao
from ..personas.modelo import Persona
from .modelo import PontoDeApoio
from .regra import cadastrar_ponto_de_apoio, designar_responsavel

roteador = APIRouter()


class PontoDeApoioSaida(BaseModel):
    id: uuid.UUID
    nome: str
    comunidade_virtual_id: uuid.UUID
    responsavel_id: uuid.UUID | None
    ativo: bool


def _saida(ponto_de_apoio: PontoDeApoio) -> PontoDeApoioSaida:
    return PontoDeApoioSaida(
        id=ponto_de_apoio.id,
        nome=ponto_de_apoio.nome,
        comunidade_virtual_id=ponto_de_apoio.comunidade_virtual_id,
        responsavel_id=ponto_de_apoio.responsavel_id,
        ativo=ponto_de_apoio.ativo,
    )


class CadastrarPontoDeApoioEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nome: str = Field(min_length=1)
    comunidade_id: uuid.UUID


@roteador.post("/pontos-de-apoio", status_code=201)
def cadastrar_ponto_de_apoio_rota(
    entrada: CadastrarPontoDeApoioEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> PontoDeApoioSaida:
    """Restrita ao Admin — a recusa de qualquer outro papel é 403, devolvida
    por `cadastrar_ponto_de_apoio` (`RF-07-47`, `RN-07-33`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    ponto_de_apoio = cadastrar_ponto_de_apoio(
        sessao_bd,
        operador=operador,
        nome=entrada.nome,
        comunidade_id=entrada.comunidade_id,
    )
    sessao_bd.commit()
    return _saida(ponto_de_apoio)


class DesignarResponsavelEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    responsavel_id: uuid.UUID


@roteador.put("/pontos-de-apoio/{id_do_ponto_de_apoio}/responsavel")
def designar_responsavel_rota(
    id_do_ponto_de_apoio: uuid.UUID,
    entrada: DesignarResponsavelEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> PontoDeApoioSaida:
    """Restrita ao Admin — designa ou troca o responsável pelo acervo, a
    qualquer tempo, com 422 para papel fora de Admin, Mestre ou Apoiador
    (`RF-07-49`, `RN-07-34`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    ponto_de_apoio = sessao_bd.get(PontoDeApoio, id_do_ponto_de_apoio)
    responsavel = sessao_bd.get(Persona, entrada.responsavel_id)
    ponto_de_apoio = designar_responsavel(
        sessao_bd,
        ponto_de_apoio,
        operador=operador,
        responsavel=responsavel,
    )
    sessao_bd.commit()
    return _saida(ponto_de_apoio)
