import uuid
from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from ..autenticacao import ContextoDaSessao, exigir_persona
from ..banco import obter_sessao
from ..erros import NaoEncontrado, PermissaoNegada
from ..personas.modelo import Papel, Persona
from ..pontos_de_apoio.modelo import PontoDeApoio
from ..recursos.modelo import TipoDeRecurso
from .modelo import Lancamento
from .regra import lancar_ajuste, saldos_por_ponto_de_apoio, transferir_saldo

roteador = APIRouter()


class LancamentoSaida(BaseModel):
    id: uuid.UUID
    natureza: str
    tipo_de_recurso_id: uuid.UUID
    ponto_de_apoio_id: uuid.UUID
    quantidade: Decimal
    valor_em_moedas: Decimal
    lancamento_original_id: uuid.UUID | None
    motivo_do_ajuste: str | None
    lancamento_relacionado_id: uuid.UUID | None


def _saida(lancamento: Lancamento) -> LancamentoSaida:
    return LancamentoSaida(
        id=lancamento.id,
        natureza=lancamento.natureza.value,
        tipo_de_recurso_id=lancamento.tipo_de_recurso_id,
        ponto_de_apoio_id=lancamento.ponto_de_apoio_id,
        quantidade=lancamento.quantidade,
        valor_em_moedas=lancamento.valor_em_moedas,
        lancamento_original_id=lancamento.lancamento_original_id,
        motivo_do_ajuste=lancamento.motivo_do_ajuste,
        lancamento_relacionado_id=lancamento.lancamento_relacionado_id,
    )


class LancarAjusteEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    quantidade: Decimal
    valor_em_moedas: Decimal
    motivo: str = Field(min_length=1)


@roteador.post("/lancamentos/{id_do_lancamento}/ajuste", status_code=201)
def lancar_ajuste_rota(
    id_do_lancamento: uuid.UUID,
    entrada: LancarAjusteEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> LancamentoSaida:
    """Restrita ao Admin — a única via de correção de um lançamento errado,
    que nunca é alterado nem removido (`RF-07-19`, `RN-07-15`, PRD-07 §9).
    Não há `PUT` nem `PATCH` declarados sobre `lancamento`: o FastAPI
    responde 405 a método não previsto (design — Decisions 4)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    lancamento_original = sessao_bd.get(Lancamento, id_do_lancamento)
    ajuste = lancar_ajuste(
        sessao_bd,
        operador=operador,
        lancamento_original=lancamento_original,
        quantidade=entrada.quantidade,
        valor_em_moedas=entrada.valor_em_moedas,
        motivo=entrada.motivo,
    )
    sessao_bd.commit()
    return _saida(ajuste)


class TransferirSaldoEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tipo_de_recurso_id: uuid.UUID
    ponto_de_apoio_origem_id: uuid.UUID
    ponto_de_apoio_destino_id: uuid.UUID
    quantidade: Decimal
    motivo: str = Field(min_length=1)


class TransferenciaSaida(BaseModel):
    debito: LancamentoSaida
    credito: LancamentoSaida


@roteador.post("/lancamentos/transferencia", status_code=201)
def transferir_saldo_rota(
    entrada: TransferirSaldoEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> TransferenciaSaida:
    """Restrita ao Admin — o par de lançamentos que esvazia o saldo de um
    ponto de apoio para outro, sem usar `ajuste` (`RF-07-19`, `RN-07-15`,
    design — Decisions 1)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    tipo_de_recurso = sessao_bd.get(TipoDeRecurso, entrada.tipo_de_recurso_id)
    ponto_de_apoio_origem = sessao_bd.get(PontoDeApoio, entrada.ponto_de_apoio_origem_id)
    ponto_de_apoio_destino = sessao_bd.get(PontoDeApoio, entrada.ponto_de_apoio_destino_id)
    debito, credito = transferir_saldo(
        sessao_bd,
        operador=operador,
        tipo_de_recurso=tipo_de_recurso,
        ponto_de_apoio_origem=ponto_de_apoio_origem,
        ponto_de_apoio_destino=ponto_de_apoio_destino,
        quantidade=entrada.quantidade,
        motivo=entrada.motivo,
    )
    sessao_bd.commit()
    return TransferenciaSaida(debito=_saida(debito), credito=_saida(credito))


class SaldoDoTipoDeRecursoSaida(BaseModel):
    tipo_de_recurso_id: uuid.UUID
    nome: str
    saldo: Decimal


@roteador.get("/pontos-de-apoio/{id_do_ponto_de_apoio}/saldos")
def listar_saldos_do_ponto_de_apoio_rota(
    id_do_ponto_de_apoio: uuid.UUID,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> list[SaldoDoTipoDeRecursoSaida]:
    """Restrita ao Admin — a tela de transferência mostra o saldo disponível
    na origem antes de confirmar (`RF-07-19`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    if operador.papel != Papel.admin:
        raise PermissaoNegada(mensagem="Só o Admin consulta o saldo de um ponto de apoio.")
    ponto_de_apoio = sessao_bd.get(PontoDeApoio, id_do_ponto_de_apoio)
    if ponto_de_apoio is None:
        raise NaoEncontrado(mensagem="Ponto de apoio não encontrado.")

    saldos = saldos_por_ponto_de_apoio(sessao_bd, ponto_de_apoio_id=ponto_de_apoio.id)
    return [
        SaldoDoTipoDeRecursoSaida(
            tipo_de_recurso_id=tipo_de_recurso_id,
            nome=sessao_bd.get(TipoDeRecurso, tipo_de_recurso_id).nome,
            saldo=saldo,
        )
        for tipo_de_recurso_id, saldo in saldos
    ]
