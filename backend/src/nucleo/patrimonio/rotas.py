import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from ..aportes.modelo import Aporte
from ..autenticacao import ContextoDaSessao, exigir_persona
from ..banco import obter_sessao
from ..personas.modelo import Persona
from ..pontos_de_apoio.modelo import PontoDeApoio
from ..tempo import DataHoraComFuso
from .modelo import AnotacaoDaFichaDeVida, ItemPatrimonial
from .regra import anotar_ficha_de_vida, listar_acervo, listar_ficha_de_vida, tombar_item

roteador = APIRouter()


class AnotacaoDaFichaDeVidaSaida(BaseModel):
    id: uuid.UUID
    teor: str
    estado_de_conservacao: str
    autor_id: uuid.UUID
    registrado_em: DataHoraComFuso


def _saida_da_anotacao(anotacao: AnotacaoDaFichaDeVida) -> AnotacaoDaFichaDeVidaSaida:
    return AnotacaoDaFichaDeVidaSaida(
        id=anotacao.id,
        teor=anotacao.teor.value,
        estado_de_conservacao=anotacao.estado_de_conservacao,
        autor_id=anotacao.autor_id,
        registrado_em=anotacao.registrado_em,
    )


class ItemPatrimonialSaida(BaseModel):
    id: uuid.UUID
    aporte_de_origem_id: uuid.UUID | None
    titulo: str
    numero_de_tombo: str
    ponto_de_apoio_id: uuid.UUID
    estado_de_conservacao: str
    responsavel_id: uuid.UUID | None
    ficha_de_vida: list[AnotacaoDaFichaDeVidaSaida]
    autor_id: uuid.UUID
    registrado_em: DataHoraComFuso


def _saida(sessao: Session, item: ItemPatrimonial) -> ItemPatrimonialSaida:
    ponto_de_apoio = sessao.get(PontoDeApoio, item.ponto_de_apoio_id)
    ficha = listar_ficha_de_vida(sessao, item_patrimonial_id=item.id)
    return ItemPatrimonialSaida(
        id=item.id,
        aporte_de_origem_id=item.aporte_de_origem_id,
        titulo=item.titulo,
        numero_de_tombo=item.numero_de_tombo,
        ponto_de_apoio_id=item.ponto_de_apoio_id,
        estado_de_conservacao=item.estado_de_conservacao,
        responsavel_id=ponto_de_apoio.responsavel_id if ponto_de_apoio is not None else None,
        ficha_de_vida=[_saida_da_anotacao(anotacao) for anotacao in ficha],
        autor_id=item.autor_id,
        registrado_em=item.registrado_em,
    )


class TombarItemEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    titulo: str = Field(min_length=1)
    numero_de_tombo: str = Field(min_length=1)
    ponto_de_apoio_id: uuid.UUID
    estado_de_conservacao: str = Field(min_length=1)
    aporte_de_origem_id: uuid.UUID | None = None


@roteador.post("/itens-patrimoniais", status_code=201)
def tombar_item_rota(
    entrada: TombarItemEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> ItemPatrimonialSaida:
    """Restrita ao Admin — o aporte de origem, quando declarado, precisa
    ser de tipo durável e não pode exceder a quantidade aportada
    (`RF-07-11`, `RN-07-07`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    ponto_de_apoio = sessao_bd.get(PontoDeApoio, entrada.ponto_de_apoio_id)
    aporte_de_origem = (
        sessao_bd.get(Aporte, entrada.aporte_de_origem_id)
        if entrada.aporte_de_origem_id is not None
        else None
    )
    item = tombar_item(
        sessao_bd,
        operador=operador,
        titulo=entrada.titulo,
        numero_de_tombo=entrada.numero_de_tombo,
        ponto_de_apoio=ponto_de_apoio,
        estado_de_conservacao=entrada.estado_de_conservacao,
        aporte_de_origem=aporte_de_origem,
    )
    sessao_bd.commit()
    return _saida(sessao_bd, item)


@roteador.get("/itens-patrimoniais")
def listar_acervo_rota(
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    comunidade_virtual_id: uuid.UUID | None = None,
) -> list[ItemPatrimonialSaida]:
    """Restrita à gestão — Admin lê qualquer comunidade, sempre declarada;
    o Mestre lê só a do seu vínculo vigente (`RF-07-11`, `RF-01-16`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    itens = listar_acervo(sessao_bd, operador=operador, comunidade_virtual_id=comunidade_virtual_id)
    return [_saida(sessao_bd, item) for item in itens]


class AnotarFichaDeVidaEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    teor: str
    estado_de_conservacao: str = Field(min_length=1)


@roteador.post("/itens-patrimoniais/{id_do_item}/ficha-de-vida", status_code=201)
def anotar_ficha_de_vida_rota(
    id_do_item: uuid.UUID,
    entrada: AnotarFichaDeVidaEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> ItemPatrimonialSaida:
    """Restrita a Admin ou Mestre — grava a anotação e reescreve o estado
    de conservação corrente do item (`RF-07-48`, `RN-07-09`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    item = sessao_bd.get(ItemPatrimonial, id_do_item)
    anotar_ficha_de_vida(
        sessao_bd,
        operador=operador,
        item=item,
        teor=entrada.teor,
        estado_de_conservacao=entrada.estado_de_conservacao,
    )
    sessao_bd.commit()
    return _saida(sessao_bd, item)
