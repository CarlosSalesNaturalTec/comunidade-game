import uuid

from sqlalchemy.orm import Session

from ..erros import ErroDeValidacao
from ..resultados.modelo import DesfechoDoResultado, Resultado
from .modelo import PontoExtra

# Documento 11 §5: os dois desfechos de fonte dupla creditam o mesmo
# adicional no regular e no extra.
ADICIONAL_DE_MERITO = 5
ADICIONAL_DE_MERITO_EXTRA_POR_AUXILIO = 10


def creditar_ponto_extra(sessao: Session, *, guerreiro_id: uuid.UUID, valor: int) -> PontoExtra:
    """Credita `valor` no acumulado e no saldo disponível na mesma operação
    — as duas contas só recebem crédito nesta fatia (`RF-01-56`,
    `RN-01-39`, `RN-01-40`)."""
    if valor <= 0:
        raise ErroDeValidacao(
            mensagem="Crédito de ponto extra exige valor positivo.", campo="valor"
        )

    conta = sessao.query(PontoExtra).filter_by(guerreiro_id=guerreiro_id).first()
    if conta is None:
        conta = PontoExtra(guerreiro_id=guerreiro_id, acumulado=valor, saldo_disponivel=valor)
        sessao.add(conta)
    else:
        conta.acumulado += valor
        conta.saldo_disponivel += valor
    sessao.flush()
    return conta


def debitar_ponto_extra(sessao: Session, *, guerreiro_id: uuid.UUID, valor: int) -> PontoExtra:
    """Debita `valor` do saldo disponível, sem tocar o acumulado — o único
    débito previsto no Ciclo 01, pela troca por recompensa avulsa
    (`RF-01-56`, `RN-01-39`, `RN-01-40`). Recusado, com o motivo nomeado,
    quando deixaria o saldo negativo — antes de a `CheckConstraint` do
    modelo recusar sem dizer por quê."""
    if valor <= 0:
        raise ErroDeValidacao(mensagem="Débito de ponto extra exige valor positivo.", campo="valor")

    conta = sessao.query(PontoExtra).filter_by(guerreiro_id=guerreiro_id).first()
    if conta is None or conta.saldo_disponivel < valor:
        raise ErroDeValidacao(
            mensagem="Saldo disponível de pontos extras insuficiente.", campo="valor"
        )

    conta.saldo_disponivel -= valor
    sessao.flush()
    return conta


def creditar_ponto_extra_do_resultado(sessao: Session, *, resultado: Resultado) -> None:
    """Fonte dupla do documento 11 §5: só `realizada_com_merito` e
    `merito_extra_por_auxilio` creditam ponto extra, junto do regular
    (`RF-01-56`)."""
    if resultado.desfecho == DesfechoDoResultado.realizada_com_merito:
        creditar_ponto_extra(sessao, guerreiro_id=resultado.guerreiro_id, valor=ADICIONAL_DE_MERITO)
    elif resultado.desfecho == DesfechoDoResultado.merito_extra_por_auxilio:
        creditar_ponto_extra(
            sessao,
            guerreiro_id=resultado.guerreiro_id,
            valor=ADICIONAL_DE_MERITO_EXTRA_POR_AUXILIO,
        )
