import uuid
from datetime import date
from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Depends, Response
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..autenticacao import ContextoDaSessao, exigir_persona
from ..banco import obter_sessao
from ..erros import ErroDeValidacao, NaoEncontrado, TipoEmUso
from ..personas.modelo import Persona
from .modelo import PrecoDeReferencia, TipoDeRecurso, ValorDeReferencia
from .regra import (
    alterar_tipo_de_recurso,
    cadastrar_tipo_de_recurso,
    consultar_precos_de_referencia,
    consultar_valor_de_referencia,
    desativar_tipo_de_recurso,
    excluir_tipo_de_recurso,
    listar_tipos_de_recurso,
    reativar_tipo_de_recurso,
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
    ativo: bool
    valor_em_moedas: Decimal | None
    vigencia_inicio: date | None


def _saida(tipo: TipoDeRecurso, valor: ValorDeReferencia | None) -> TipoDeRecursoSaida:
    return TipoDeRecursoSaida(
        id=tipo.id,
        nome=tipo.nome,
        natureza=tipo.natureza.value,
        unidade=tipo.unidade,
        exige_comprovante=tipo.exige_comprovante,
        ativo=tipo.ativo,
        valor_em_moedas=valor.valor_em_moedas if valor is not None else None,
        vigencia_inicio=valor.vigencia_inicio if valor is not None else None,
    )


def _buscar_tipo(sessao_bd: Session, id_do_tipo: uuid.UUID) -> TipoDeRecurso:
    tipo = sessao_bd.get(TipoDeRecurso, id_do_tipo)
    if tipo is None:
        raise NaoEncontrado(mensagem="Tipo de recurso não encontrado.")
    return tipo


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


class AlterarTipoDeRecursoEntrada(BaseModel):
    """`natureza` existe só para a regra responder que ela não se altera,
    com mensagem própria (design — decisão 2)."""

    model_config = ConfigDict(extra="forbid")

    nome: str | None = None
    unidade: str | None = None
    exige_comprovante: bool | None = None
    natureza: str | None = None


def _saida_vigente(sessao_bd: Session, tipo: TipoDeRecurso) -> TipoDeRecursoSaida:
    return _saida(tipo, consultar_valor_de_referencia(sessao_bd, tipo=tipo, data=date.today()))


@roteador.patch("/tipos-de-recurso/{id_do_tipo}")
def alterar_tipo_de_recurso_rota(
    id_do_tipo: uuid.UUID,
    entrada: AlterarTipoDeRecursoEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> TipoDeRecursoSaida:
    """Restrita ao Admin — nome, unidade e exige comprovante; a natureza é
    recusada (`RF-07-51`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    tipo = _buscar_tipo(sessao_bd, id_do_tipo)
    alterar_tipo_de_recurso(
        sessao_bd,
        tipo,
        operador=operador,
        nome=entrada.nome,
        unidade=entrada.unidade,
        exige_comprovante=entrada.exige_comprovante,
        natureza=entrada.natureza,
    )
    sessao_bd.commit()
    return _saida_vigente(sessao_bd, tipo)


class ValorDeReferenciaSaida(BaseModel):
    id: uuid.UUID
    tipo_de_recurso_id: uuid.UUID
    valor_em_moedas: Decimal
    vigencia_inicio: date
    vigencia_fim: date | None


class RegistrarValorDeReferenciaEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    valor_em_moedas: Decimal
    vigencia_inicio: date


@roteador.post("/tipos-de-recurso/{id_do_tipo}/valores-de-referencia", status_code=201)
def registrar_valor_de_referencia_rota(
    id_do_tipo: uuid.UUID,
    entrada: RegistrarValorDeReferenciaEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> ValorDeReferenciaSaida:
    """Restrita ao Admin — abre vigência nova do valor em moedas e encerra a
    vigente no dia de início da nova (`RF-07-51`, `RF-07-02`, `RN-07-03`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    tipo = _buscar_tipo(sessao_bd, id_do_tipo)
    valor = registrar_valor_de_referencia(
        sessao_bd,
        operador=operador,
        tipo=tipo,
        valor_em_moedas=entrada.valor_em_moedas,
        vigencia_inicio=entrada.vigencia_inicio,
    )
    sessao_bd.commit()
    return ValorDeReferenciaSaida(
        id=valor.id,
        tipo_de_recurso_id=valor.tipo_de_recurso_id,
        valor_em_moedas=valor.valor_em_moedas,
        vigencia_inicio=valor.vigencia_inicio,
        vigencia_fim=valor.vigencia_fim,
    )


@roteador.post("/tipos-de-recurso/{id_do_tipo}/desativacao")
def desativar_tipo_de_recurso_rota(
    id_do_tipo: uuid.UUID,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> TipoDeRecursoSaida:
    """Restrita ao Admin — sai da escolha nova, nada do que existe muda
    (`RF-07-52`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    tipo = _buscar_tipo(sessao_bd, id_do_tipo)
    desativar_tipo_de_recurso(sessao_bd, tipo, operador=operador)
    sessao_bd.commit()
    return _saida_vigente(sessao_bd, tipo)


@roteador.post("/tipos-de-recurso/{id_do_tipo}/reativacao")
def reativar_tipo_de_recurso_rota(
    id_do_tipo: uuid.UUID,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> TipoDeRecursoSaida:
    """Restrita ao Admin (`RF-07-52`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    tipo = _buscar_tipo(sessao_bd, id_do_tipo)
    reativar_tipo_de_recurso(sessao_bd, tipo, operador=operador)
    sessao_bd.commit()
    return _saida_vigente(sessao_bd, tipo)


@roteador.delete("/tipos-de-recurso/{id_do_tipo}", status_code=204)
def excluir_tipo_de_recurso_rota(
    id_do_tipo: uuid.UUID,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> Response:
    """Restrita ao Admin — só o tipo nunca usado; a chave estrangeira que
    chegue entre a conferência e o `DELETE` vira a mesma recusa por uso
    (`RN-07-40`, design — decisão 4)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    tipo = _buscar_tipo(sessao_bd, id_do_tipo)
    try:
        excluir_tipo_de_recurso(sessao_bd, tipo, operador=operador)
        sessao_bd.commit()
    except IntegrityError as exc:
        sessao_bd.rollback()
        raise TipoEmUso(campo="tipo_de_recurso_id") from exc
    return Response(status_code=204)
