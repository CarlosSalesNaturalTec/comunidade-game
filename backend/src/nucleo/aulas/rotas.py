import uuid
from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from ..autenticacao import ContextoDaSessao, exigir_persona
from ..banco import obter_sessao
from ..comunidades.modelo import ComunidadeVirtual
from ..personas.modelo import Persona
from ..pontos_de_apoio.modelo import PontoDeApoio
from ..recursos.modelo import TipoDeRecurso
from ..reservas.regra import disponivel_de
from ..resultados.regra import ResultadoDeclarado
from ..resultados.regra import lancar_atividade_realizada as _lancar_atividade_realizada
from ..tempo import DataHoraComFuso
from ..trilhas.modelo import Atividade
from .modelo import Aula, RecursoDeclaradoDaAula, SituacaoDaAula
from .regra import (
    RecursoDeclaradoEntrada,
    agendar_aula,
    cancelar_aula,
    tentar_reservar_aula_pendente,
)

roteador = APIRouter()


class RecursoDeclaradoCorpo(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tipo_de_recurso_id: uuid.UUID
    quantidade: Decimal


class RecursoFaltanteSaida(BaseModel):
    tipo_de_recurso_id: uuid.UUID
    quantidade_declarada: Decimal
    quantidade_disponivel: Decimal


class AulaSaida(BaseModel):
    id: uuid.UUID
    comunidade_virtual_id: uuid.UUID
    ponto_de_apoio_id: uuid.UUID
    inicio_em: DataHoraComFuso
    fim_em: DataHoraComFuso
    situacao: str
    cancelamento_motivo: str | None
    recursos_faltantes: list[RecursoFaltanteSaida]


def _recursos_faltantes(sessao: Session, aula: Aula) -> list[RecursoFaltanteSaida]:
    """Só a aula pendente de lastro tem o que faltar a mostrar — as demais
    devolvem lista vazia (`RF-07-08`, PRD-07 §5.3)."""
    if aula.situacao != SituacaoDaAula.pendente_de_lastro:
        return []

    declarados = sessao.query(RecursoDeclaradoDaAula).filter_by(aula_id=aula.id).all()
    faltantes = []
    for declarado in declarados:
        disponivel = disponivel_de(
            sessao,
            tipo_de_recurso_id=declarado.tipo_de_recurso_id,
            ponto_de_apoio_id=aula.ponto_de_apoio_id,
        )
        if disponivel < declarado.quantidade:
            faltantes.append(
                RecursoFaltanteSaida(
                    tipo_de_recurso_id=declarado.tipo_de_recurso_id,
                    quantidade_declarada=declarado.quantidade,
                    quantidade_disponivel=disponivel,
                )
            )
    return faltantes


def _saida(sessao: Session, aula: Aula) -> AulaSaida:
    return AulaSaida(
        id=aula.id,
        comunidade_virtual_id=aula.comunidade_virtual_id,
        ponto_de_apoio_id=aula.ponto_de_apoio_id,
        inicio_em=aula.inicio_em,
        fim_em=aula.fim_em,
        situacao=aula.situacao.value,
        cancelamento_motivo=aula.cancelamento_motivo,
        recursos_faltantes=_recursos_faltantes(sessao, aula),
    )


class AgendarAulaEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    comunidade_virtual_id: uuid.UUID
    ponto_de_apoio_id: uuid.UUID
    inicio_em: DataHoraComFuso
    fim_em: DataHoraComFuso
    recursos_declarados: list[RecursoDeclaradoCorpo] = Field(default_factory=list)


@roteador.post("/aulas", status_code=201)
def agendar_aula_rota(
    entrada: AgendarAulaEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> AulaSaida:
    """Restrita ao Admin — agenda e dispara a reserva dos recursos
    declarados (`RF-07-08`, `RF-02-31`, `RF-01-16`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    comunidade = sessao_bd.get(ComunidadeVirtual, entrada.comunidade_virtual_id)
    ponto_de_apoio = sessao_bd.get(PontoDeApoio, entrada.ponto_de_apoio_id)
    recursos_declarados = [
        RecursoDeclaradoEntrada(
            tipo=sessao_bd.get(TipoDeRecurso, item.tipo_de_recurso_id),
            quantidade=item.quantidade,
        )
        for item in entrada.recursos_declarados
    ]

    aula = agendar_aula(
        sessao_bd,
        operador=operador,
        comunidade=comunidade,
        ponto_de_apoio=ponto_de_apoio,
        inicio_em=entrada.inicio_em,
        fim_em=entrada.fim_em,
        recursos_declarados=recursos_declarados,
    )
    sessao_bd.commit()
    return _saida(sessao_bd, aula)


@roteador.post("/aulas/{id_da_aula}/reservas")
def tentar_reservar_aula_pendente_rota(
    id_da_aula: uuid.UUID,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> AulaSaida:
    """Caminho explícito e idempotente da PRD-07 §9: tenta de novo a reserva
    de uma aula pendente de lastro; aula já confirmada devolve o estado
    corrente sem duplicar reserva (design — Decisions 6)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    aula = sessao_bd.get(Aula, id_da_aula)
    aula = tentar_reservar_aula_pendente(sessao_bd, operador=operador, aula=aula)
    sessao_bd.commit()
    return _saida(sessao_bd, aula)


class ResultadoDeclaradoCorpo(BaseModel):
    model_config = ConfigDict(extra="forbid")

    guerreiro_id: uuid.UUID
    atividade_id: uuid.UUID
    momento_do_fato: DataHoraComFuso
    producao: str = Field(min_length=1)
    desfecho: str


class LancarAtividadeRealizadaEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    resultados: list[ResultadoDeclaradoCorpo] = Field(default_factory=list)


@roteador.post("/aulas/{id_da_aula}/lancamentos", status_code=201)
def lancar_atividade_realizada_rota(
    id_da_aula: uuid.UUID,
    entrada: LancarAtividadeRealizadaEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> AulaSaida:
    """Restrita ao Admin — grava os Resultados de todos os participantes e
    converte cada reserva da aula em débito, na mesma operação (`RF-07-09`,
    `RF-02-35`, `RN-07-36`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    aula = sessao_bd.get(Aula, id_da_aula)
    resultados = [
        ResultadoDeclarado(
            guerreiro_id=item.guerreiro_id,
            atividade=sessao_bd.get(Atividade, item.atividade_id),
            momento_do_fato=item.momento_do_fato,
            producao=item.producao,
            desfecho=item.desfecho,
        )
        for item in entrada.resultados
    ]

    aula, _ = _lancar_atividade_realizada(
        sessao_bd, operador=operador, aula=aula, resultados=resultados
    )
    sessao_bd.commit()
    return _saida(sessao_bd, aula)


class CancelarAulaEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    motivo: str = Field(min_length=1)


@roteador.post("/aulas/{id_da_aula}/cancelamento")
def cancelar_aula_rota(
    id_da_aula: uuid.UUID,
    entrada: CancelarAulaEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> AulaSaida:
    """Admin ou Mestre da comunidade cancelam, sempre com motivo — libera as
    reservas da aula (`RF-01-72`, `RF-01-17`, `RF-02-95`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    aula = sessao_bd.get(Aula, id_da_aula)
    aula = cancelar_aula(sessao_bd, operador=operador, aula=aula, motivo=entrada.motivo)
    sessao_bd.commit()
    return _saida(sessao_bd, aula)
