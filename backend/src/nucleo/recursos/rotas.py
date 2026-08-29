import uuid
from datetime import date
from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from ..autenticacao import ContextoDaSessao, exigir_persona
from ..banco import obter_sessao
from ..erros import ErroDeValidacao
from ..personas.modelo import Persona
from .modelo import PrecoDeReferencia, TipoDeRecurso, ValorDeReferencia
from .regra import (
    cadastrar_tipo_de_recurso,
    consultar_precos_de_referencia,
    consultar_valor_de_referencia,
    listar_tipos_de_recurso,
    registrar_preco_de_referencia,
    registrar_valor_de_referencia,
)

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


@roteador.get("/tipos-de-recurso", response_model=list[TipoDeRecursoSaida])
def listar_tipos_de_recurso_rota(
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> list[TipoDeRecursoSaida]:
    """Admin e Mestre leem; a escrita segue privativa do Admin. Serve o
    seletor de tipo de recurso da gestão — entre outros, o da homologação
    do aporte — e, para o Mestre, o ato de absorção da necessidade
    (`RF-07-01`, `RF-02-84`, `RF-09-56`, `RF-09-57`, PRD-02 §6.2)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    tipos = listar_tipos_de_recurso(sessao_bd, operador=operador)
    saida: list[TipoDeRecursoSaida] = []
    for tipo in tipos:
        valor = consultar_valor_de_referencia(sessao_bd, tipo=tipo, data=date.today())
        if valor is not None:
            saida.append(_saida(tipo, valor))
    return saida


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


class PrecoDeReferenciaSaida(BaseModel):
    id: uuid.UUID
    tipo_de_recurso_id: uuid.UUID
    preco_em_pontos_extras: int
    vigencia_inicio: date
    vigencia_fim: date | None


def _saida_preco(preco: PrecoDeReferencia) -> PrecoDeReferenciaSaida:
    return PrecoDeReferenciaSaida(
        id=preco.id,
        tipo_de_recurso_id=preco.tipo_de_recurso_id,
        preco_em_pontos_extras=preco.preco_em_pontos_extras,
        vigencia_inicio=preco.vigencia_inicio,
        vigencia_fim=preco.vigencia_fim,
    )


class RegistrarPrecoDeReferenciaEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    preco_em_pontos_extras: int
    vigencia_inicio: date


@roteador.post("/tipos-de-recurso/{id_do_tipo}/precos-de-referencia", status_code=201)
def registrar_preco_de_referencia_rota(
    id_do_tipo: uuid.UUID,
    entrada: RegistrarPrecoDeReferenciaEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> PrecoDeReferenciaSaida:
    """Restrita ao Admin — abre a vigência do preço em pontos extras, régua
    independente do valor em moedas do mesmo tipo (`RF-07-42`, `RF-07-43`,
    `RN-07-24`, `RN-07-25`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    tipo = sessao_bd.get(TipoDeRecurso, id_do_tipo)
    if tipo is None:
        raise ErroDeValidacao(
            mensagem="Tipo de recurso não encontrado.", campo="tipo_de_recurso_id"
        )
    preco = registrar_preco_de_referencia(
        sessao_bd,
        operador=operador,
        tipo=tipo,
        preco_em_pontos_extras=entrada.preco_em_pontos_extras,
        vigencia_inicio=entrada.vigencia_inicio,
    )
    sessao_bd.commit()
    return _saida_preco(preco)


@roteador.get("/tipos-de-recurso/{id_do_tipo}/precos-de-referencia")
def listar_precos_de_referencia_rota(
    id_do_tipo: uuid.UUID,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> list[PrecoDeReferenciaSaida]:
    """Restrita ao Admin — o histórico de vigências do preço em pontos
    extras de um tipo, da mais recente para a mais antiga (`RF-07-43`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    tipo = sessao_bd.get(TipoDeRecurso, id_do_tipo)
    if tipo is None:
        raise ErroDeValidacao(
            mensagem="Tipo de recurso não encontrado.", campo="tipo_de_recurso_id"
        )
    precos = consultar_precos_de_referencia(sessao_bd, operador=operador, tipo=tipo)
    return [_saida_preco(preco) for preco in precos]
