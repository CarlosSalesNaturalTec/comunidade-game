import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from ..aulas.modelo import Aula
from ..autenticacao import ContextoDaSessao, exigir_persona
from ..banco import obter_sessao
from ..catalogo_avulso.modelo import ItemDeCatalogoAvulso
from ..personas.modelo import Persona
from ..tempo import DataHoraComFuso
from .modelo import Troca
from .regra import listar_trocas, registrar_troca

roteador = APIRouter()


class TrocaSaida(BaseModel):
    id: uuid.UUID
    item_de_catalogo_avulso_id: uuid.UUID
    guerreiro_id: uuid.UUID
    preco_cobrado: int
    aula_id: uuid.UUID
    autor_id: uuid.UUID
    registrado_em: DataHoraComFuso


def _saida(troca: Troca) -> TrocaSaida:
    return TrocaSaida(
        id=troca.id,
        item_de_catalogo_avulso_id=troca.item_de_catalogo_avulso_id,
        guerreiro_id=troca.guerreiro_id,
        preco_cobrado=troca.preco_cobrado,
        aula_id=troca.aula_id,
        autor_id=troca.autor_id,
        registrado_em=troca.registrado_em,
    )


class RegistrarTrocaEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    item_de_catalogo_avulso_id: uuid.UUID
    guerreiro_id: uuid.UUID


@roteador.post("/aulas/{id_da_aula}/trocas", status_code=201)
def registrar_troca_rota(
    id_da_aula: uuid.UUID,
    entrada: RegistrarTrocaEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> TrocaSaida:
    """Restrita ao Mestre vinculado à comunidade da aula — a entrega, numa
    operação só: grava a troca, debita o saldo disponível, decrementa o
    estoque e emite o débito no livro-razão (`RF-07-35`, `RF-07-36`,
    `RN-07-27`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    aula = sessao_bd.get(Aula, id_da_aula)
    item = sessao_bd.get(ItemDeCatalogoAvulso, entrada.item_de_catalogo_avulso_id)
    guerreiro = sessao_bd.get(Persona, entrada.guerreiro_id)
    troca = registrar_troca(sessao_bd, operador=operador, aula=aula, item=item, guerreiro=guerreiro)
    sessao_bd.commit()
    return _saida(troca)


@roteador.get("/trocas")
def listar_trocas_rota(
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> list[TrocaSaida]:
    """O histórico de trocas, filtrado por persona: Guerreiro(a) só as
    próprias, Mestre as das suas comunidades, Admin todas (`RF-07-35`,
    `RN-07-24`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    trocas = listar_trocas(sessao_bd, operador=operador)
    return [_saida(troca) for troca in trocas]
