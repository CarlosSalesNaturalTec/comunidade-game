import uuid

from sqlalchemy.orm import Session

from .modelo import ContaDoLancamento, LancamentoDePontuacao, OrigemDoLancamento


def lancar_movimento_regular(
    sessao: Session,
    *,
    guerreiro_id: uuid.UUID,
    trilha_id: uuid.UUID | None,
    poder_id: uuid.UUID | None,
    valor: int,
    origem: OrigemDoLancamento,
    referencia_id: uuid.UUID | None,
    detalhe: str | None,
) -> LancamentoDePontuacao:
    """Grava o movimento da conta regular na mesma transação dele, com o
    valor que de fato moveu o total — o débito que para em zero registra só
    o que debitou (`RF-01-88`, `RN-01-67`)."""
    lancamento = LancamentoDePontuacao(
        guerreiro_id=guerreiro_id,
        conta=ContaDoLancamento.regular,
        trilha_id=trilha_id,
        poder_id=poder_id,
        valor=valor,
        origem=origem,
        referencia_id=referencia_id,
        detalhe=_aparar(detalhe),
    )
    sessao.add(lancamento)
    sessao.flush()
    return lancamento


def lancar_movimento_extra(
    sessao: Session,
    *,
    guerreiro_id: uuid.UUID,
    valor: int,
    valor_no_acumulado: int,
    origem: OrigemDoLancamento,
    referencia_id: uuid.UUID | None,
    detalhe: str | None,
) -> LancamentoDePontuacao:
    """Grava o movimento da conta extra: `valor` no saldo disponível e
    `valor_no_acumulado` no acumulado, separados — a troca move só o saldo
    (`RF-01-88`, `RN-01-67`)."""
    lancamento = LancamentoDePontuacao(
        guerreiro_id=guerreiro_id,
        conta=ContaDoLancamento.extra,
        valor=valor,
        valor_no_acumulado=valor_no_acumulado,
        origem=origem,
        referencia_id=referencia_id,
        detalhe=_aparar(detalhe),
    )
    sessao.add(lancamento)
    sessao.flush()
    return lancamento


def _aparar(detalhe: str | None) -> str | None:
    if detalhe is None:
        return None
    return detalhe[:256]
