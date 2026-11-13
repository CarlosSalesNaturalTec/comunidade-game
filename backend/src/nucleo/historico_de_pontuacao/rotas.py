import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..autenticacao import ContextoDaSessao, exigir_persona
from ..banco import obter_sessao
from ..erros import PermissaoNegada
from ..paginacao import ParametrosDeListagem, contrato_de_listagem
from ..personas.modelo import Papel, Persona
from .modelo import ContaDoLancamento, OrigemDoLancamento
from .regra import autorizar_leitura_do_historico, listar_lancamentos, saldos_do_guerreiro

roteador = APIRouter()


class SaldoRegularSaida(BaseModel):
    trilha_id: uuid.UUID | None
    poder_id: uuid.UUID | None
    nome: str
    total: int


class SaldoExtraSaida(BaseModel):
    acumulado: int
    saldo_disponivel: int


class SaldosSaida(BaseModel):
    regular: list[SaldoRegularSaida]
    extra: SaldoExtraSaida


class LancamentoSaida(BaseModel):
    id: uuid.UUID
    registrado_em: datetime
    conta: ContaDoLancamento
    origem: OrigemDoLancamento
    valor: int
    valor_no_acumulado: int | None
    trilha_id: uuid.UUID | None
    poder_id: uuid.UUID | None
    nome_da_trilha_ou_poder: str | None
    detalhe: str | None
    motivo: str | None


class HistoricoDePontuacaoSaida(BaseModel):
    saldos: SaldosSaida
    itens: list[LancamentoSaida]
    proximo_cursor: str | None = None


def _historico(
    sessao_bd: Session, *, guerreiro_id: uuid.UUID, parametros: ParametrosDeListagem
) -> HistoricoDePontuacaoSaida:
    itens, proximo_cursor = listar_lancamentos(
        sessao_bd, guerreiro_id=guerreiro_id, parametros=parametros
    )
    return HistoricoDePontuacaoSaida(
        saldos=SaldosSaida(**saldos_do_guerreiro(sessao_bd, guerreiro_id=guerreiro_id)),
        itens=[LancamentoSaida(**item) for item in itens],
        proximo_cursor=proximo_cursor,
    )


@roteador.get("/eu/historico-de-pontuacao", response_model=HistoricoDePontuacaoSaida)
def meu_historico_de_pontuacao(
    parametros: Annotated[ParametrosDeListagem, Depends(contrato_de_listagem())],
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> HistoricoDePontuacaoSaida:
    """O histórico do próprio Guerreiro(a) em sessão, sem identificador de
    persona — não há como apontá-lo para outro (`RF-01-89`, `RF-05-104`,
    `RN-01-68`)."""
    if contexto.papel != Papel.guerreiro:
        raise PermissaoNegada(mensagem="Só o Guerreiro(a) lê o próprio histórico por aqui.")
    return _historico(sessao_bd, guerreiro_id=contexto.persona_id, parametros=parametros)


@roteador.get(
    "/guerreiros/{guerreiro_id}/historico-de-pontuacao",
    response_model=HistoricoDePontuacaoSaida,
)
def historico_de_pontuacao_do_guerreiro(
    guerreiro_id: uuid.UUID,
    parametros: Annotated[ParametrosDeListagem, Depends(contrato_de_listagem())],
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> HistoricoDePontuacaoSaida:
    """O histórico de um Guerreiro(a) ao Admin e ao Mestre com vínculo
    vigente na comunidade dele, com o saldo disponível (`RF-01-89`,
    `RF-09-144`, `RF-02-116`, `RN-01-68`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    guerreiro = autorizar_leitura_do_historico(
        sessao_bd, operador=operador, guerreiro_id=guerreiro_id
    )
    return _historico(sessao_bd, guerreiro_id=guerreiro.id, parametros=parametros)
