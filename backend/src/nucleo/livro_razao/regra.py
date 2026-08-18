from decimal import Decimal

from sqlalchemy import case, func
from sqlalchemy.orm import Session

from ..erros import ErroDeValidacao, PermissaoNegada
from ..personas.modelo import Papel, Persona
from .modelo import Lancamento, NaturezaDoLancamento


def lancar_credito(
    sessao: Session,
    *,
    tipo_de_recurso_id,
    ponto_de_apoio_id,
    quantidade: Decimal,
    valor_em_moedas: Decimal,
    operador: Persona,
) -> Lancamento:
    """O lançamento de crédito que todo aporte homologado gera, um por
    aporte, no ponto de apoio declarado (`RF-07-04`, `RF-07-07`, `RN-07-36`,
    design — Decisions 9)."""
    lancamento = Lancamento(
        natureza=NaturezaDoLancamento.credito,
        tipo_de_recurso_id=tipo_de_recurso_id,
        ponto_de_apoio_id=ponto_de_apoio_id,
        quantidade=quantidade,
        valor_em_moedas=valor_em_moedas,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(lancamento)
    sessao.flush()
    return lancamento


def lancar_debito(
    sessao: Session,
    *,
    tipo_de_recurso_id,
    ponto_de_apoio_id,
    quantidade: Decimal,
    valor_em_moedas: Decimal,
    operador: Persona,
) -> Lancamento:
    """O lançamento de débito que a baixa de uma reserva gera, um por
    reserva consumida, no ponto de apoio da aula que a consumiu (`RF-07-09`,
    `RN-07-36`, design — Decisions 7)."""
    lancamento = Lancamento(
        natureza=NaturezaDoLancamento.debito,
        tipo_de_recurso_id=tipo_de_recurso_id,
        ponto_de_apoio_id=ponto_de_apoio_id,
        quantidade=quantidade,
        valor_em_moedas=valor_em_moedas,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(lancamento)
    sessao.flush()
    return lancamento


def lancar_ajuste(
    sessao: Session,
    *,
    operador: Persona,
    lancamento_original: Lancamento | None,
    quantidade: Decimal | None,
    valor_em_moedas: Decimal | None,
    motivo: str | None,
) -> Lancamento:
    """Só Admin corrige lançamento, e só por lançamento novo que referencia
    o original sem alterá-lo (`RF-07-19`, `RN-07-15`). Herda tipo de recurso
    e ponto de apoio do original, para que a correção entre na mesma conta
    de saldo (design — Decisions 9)."""
    if operador.papel != Papel.admin:
        raise PermissaoNegada(mensagem="Só o Admin lança ajuste.")
    if lancamento_original is None:
        raise ErroDeValidacao(
            mensagem="Lançamento original não encontrado.", campo="lancamento_original_id"
        )
    if not motivo or not motivo.strip():
        raise ErroDeValidacao(mensagem="Ajuste exige motivo.", campo="motivo")
    if quantidade is None:
        raise ErroDeValidacao(mensagem="Ajuste exige quantidade.", campo="quantidade")
    if valor_em_moedas is None:
        raise ErroDeValidacao(mensagem="Ajuste exige valor em moedas.", campo="valor_em_moedas")

    ajuste = Lancamento(
        natureza=NaturezaDoLancamento.ajuste,
        tipo_de_recurso_id=lancamento_original.tipo_de_recurso_id,
        ponto_de_apoio_id=lancamento_original.ponto_de_apoio_id,
        quantidade=quantidade,
        valor_em_moedas=valor_em_moedas,
        lancamento_original_id=lancamento_original.id,
        motivo_do_ajuste=motivo,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(ajuste)
    sessao.flush()
    return ajuste


def saldo_de(sessao: Session, *, tipo_de_recurso_id, ponto_de_apoio_id) -> Decimal:
    """O saldo é sempre agregado sobre `lancamento`, nunca um número
    editável: recontar devolve o mesmo número (`RF-07-07`, `RN-07-36`,
    design — Decisions 1). Crédito soma, débito subtrai, ajuste entra pelo
    sinal que a própria quantidade já carrega."""
    contribuicao = case(
        (Lancamento.natureza == NaturezaDoLancamento.debito, -Lancamento.quantidade),
        else_=Lancamento.quantidade,
    )
    total = (
        sessao.query(func.coalesce(func.sum(contribuicao), 0))
        .filter(
            Lancamento.tipo_de_recurso_id == tipo_de_recurso_id,
            Lancamento.ponto_de_apoio_id == ponto_de_apoio_id,
        )
        .scalar()
    )
    return Decimal(total)
