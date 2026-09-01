import uuid
from decimal import Decimal

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from ..aportes.modelo import Aporte, FormaDeAporte
from ..livro_razao.modelo import Lancamento, NaturezaDoLancamento


def poder_sustentador_de(sessao: Session, *, provedor_id: uuid.UUID) -> Decimal:
    """A soma, em moedas, dos créditos ligados aos aportes do provedor mais
    os ajustes que referenciam esses créditos — a cadeia aporte → crédito →
    ajuste, sempre derivada e recontável (`RF-07-10`, `RN-07-15`, design —
    Decisions 1, 5). Provedor sem aporte soma zero."""
    creditos = (
        sessao.query(Lancamento.id)
        .join(Aporte, Aporte.lancamento_id == Lancamento.id)
        .filter(
            Aporte.provedor_id == provedor_id,
            Lancamento.natureza == NaturezaDoLancamento.credito,
        )
        .subquery()
    )
    total = (
        sessao.query(func.coalesce(func.sum(Lancamento.valor_em_moedas), 0))
        .filter(
            or_(
                Lancamento.id.in_(select(creditos.c.id)),
                Lancamento.lancamento_original_id.in_(select(creditos.c.id)),
            )
        )
        .scalar()
    )
    return Decimal(total)


def moedas_acumuladas_de(sessao: Session, *, provedor_id: uuid.UUID) -> Decimal:
    """A soma, em moedas, dos aportes homologados do provedor — direto na
    tabela `Aporte`, sem olhar lançamento de ajuste (`RF-14-14`, `RN-14-11`,
    design — Decisions 1). Não é `poder_sustentador_de`: aquela deriva do
    livro-razão e o ressarcimento pago a derruba; esta mede o piso do
    avatar próprio, um direito que, uma vez alcançado, não regride.
    Provedor sem aporte soma zero."""
    total = (
        sessao.query(func.coalesce(func.sum(Aporte.valor_em_moedas), 0))
        .filter(Aporte.provedor_id == provedor_id)
        .scalar()
    )
    return Decimal(total)


def poder_sustentador_por_provedor(sessao: Session) -> dict[uuid.UUID, Decimal]:
    """A mesma derivação de `poder_sustentador_de`, agregada para todo
    provedor de uma vez — usada tanto pelo movimentado total quanto pelo
    movimentado por provedor da prestação de contas, para que as duas
    leituras não divirjam (`RF-07-16`, `RN-07-15`, design — Decisions 1, 5).
    Provedor sem aporte não entra no dicionário.
    """
    creditos = (
        sessao.query(
            Aporte.provedor_id.label("provedor_id"),
            Lancamento.id.label("lancamento_id"),
            Lancamento.valor_em_moedas.label("valor_em_moedas"),
        )
        .join(Lancamento, Lancamento.id == Aporte.lancamento_id)
        .filter(Lancamento.natureza == NaturezaDoLancamento.credito)
        .subquery()
    )
    ajustes = (
        sessao.query(
            creditos.c.provedor_id.label("provedor_id"),
            Lancamento.valor_em_moedas.label("valor_em_moedas"),
        )
        .join(Lancamento, Lancamento.lancamento_original_id == creditos.c.lancamento_id)
        .filter(Lancamento.natureza == NaturezaDoLancamento.ajuste)
    )
    movimentos = (
        sessao.query(
            creditos.c.provedor_id.label("provedor_id"),
            creditos.c.valor_em_moedas.label("valor_em_moedas"),
        )
        .union_all(ajustes)
        .subquery()
    )
    linhas = (
        sessao.query(movimentos.c.provedor_id, func.sum(movimentos.c.valor_em_moedas))
        .group_by(movimentos.c.provedor_id)
        .all()
    )
    return {provedor_id: Decimal(total) for provedor_id, total in linhas}


def contagem_de_absorcoes_de(sessao: Session, *, provedor_id: uuid.UUID) -> int:
    """Quantas vezes o provedor sustentou atividade sem recurso — os
    aportes dele de forma `absorcao`. Deriva só de `Aporte`, nunca do
    livro-razão, para que ajuste ou estorno não a alterem (`RF-07-26`,
    `RN-07-19`, design — Decisions 2)."""
    return (
        sessao.query(func.count(Aporte.id))
        .filter(Aporte.provedor_id == provedor_id, Aporte.forma == FormaDeAporte.absorcao)
        .scalar()
    )
