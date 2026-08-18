import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy import func
from sqlalchemy.orm import Session

from ..aportes.modelo import Aporte, FormaDeAporte, SituacaoDeRessarcimento
from ..armazenamento.porta import PortaDeArmazenamento
from ..erros import ErroDeValidacao, PermissaoNegada
from ..livro_razao.modelo import DestinacaoDoAporte, Lancamento
from ..livro_razao.regra import lancar_ajuste
from ..personas.modelo import Papel, Persona
from .modelo import Ressarcimento

_FORMATOS_DE_COMPROVANTE_ACEITOS = frozenset({"application/pdf", "image/jpeg", "image/png"})


def listar_ressarciveis(sessao: Session, *, operador: Persona) -> list[Aporte]:
    """A fila por antiguidade — absorções em aberto, do mais antigo ao mais
    novo —, restrita ao Admin (`RF-07-24`, `RN-07-17`, PRD-07 §§9, 12)."""
    if operador.papel != Papel.admin:
        raise PermissaoNegada(mensagem="Só o Admin lê a fila de ressarcimento.")

    return (
        sessao.query(Aporte)
        .filter(
            Aporte.forma == FormaDeAporte.absorcao,
            Aporte.situacao_de_ressarcimento == SituacaoDeRessarcimento.em_aberto,
        )
        .order_by(Aporte.data_do_aporte.asc())
        .all()
    )


def saldo_em_aberto_da_receita(sessao: Session, *, receita_destinada: Aporte) -> Decimal:
    """O valor em reais da receita destinada menos os ressarcimentos já
    pagos contra ela — sem valor de origem declarado, a receita não cobre
    pagamento algum (`RN-07-17`, design — Decisions 3)."""
    pago = (
        sessao.query(func.coalesce(func.sum(Ressarcimento.valor_em_reais), 0))
        .filter(Ressarcimento.receita_destinada_id == receita_destinada.id)
        .scalar()
    )
    origem = (
        receita_destinada.valor_de_origem
        if receita_destinada.valor_de_origem is not None
        else Decimal("0")
    )
    return origem - Decimal(pago)


def _processar_comprovante_obrigatorio(
    *,
    conteudo: bytes | None,
    nome_original: str | None,
    tipo_mime: str | None,
    armazenamento: PortaDeArmazenamento | None,
) -> tuple[str, str | None, str, int]:
    """PDF, JPG ou PNG — ao contrário do comprovante do aporte, aqui é
    sempre exigido (`RF-07-22`)."""
    if conteudo is None:
        raise ErroDeValidacao(
            mensagem="Ressarcimento exige comprovante anexado.", campo="comprovante"
        )
    if tipo_mime not in _FORMATOS_DE_COMPROVANTE_ACEITOS:
        raise ErroDeValidacao(
            mensagem="Comprovante aceito apenas em PDF, JPG ou PNG.", campo="comprovante"
        )
    if armazenamento is None:
        raise ErroDeValidacao(mensagem="Porta de armazenamento não disponível.")

    referencia = f"ressarcimentos/{uuid.uuid4()}"
    armazenamento.gravar(referencia=referencia, conteudo=conteudo)
    return referencia, nome_original, tipo_mime, len(conteudo)


def registrar_ressarcimento(
    sessao: Session,
    *,
    operador: Persona,
    aporte: Aporte | None,
    receita_destinada: Aporte | None,
    data: date | None,
    comprovante_conteudo: bytes | None,
    comprovante_nome_original: str | None,
    comprovante_tipo: str | None,
    armazenamento: PortaDeArmazenamento | None,
) -> Ressarcimento:
    """Só Admin, e só sobre absorção ainda em aberto, financiada por uma
    receita destinada que a cubra (`RF-07-22`, `RF-07-25`, `RN-07-17`,
    PRD-07 §§9, 11, 12). Emite, na mesma transação, o ajuste de
    **quantidade zero** que reverte as moedas do crédito original — o
    saldo de recurso e a contagem de absorções não se movem (`RN-07-18`,
    `RN-07-15`, design — Decisions 1, 4)."""
    if operador.papel != Papel.admin:
        raise PermissaoNegada(mensagem="Só o Admin registra ressarcimento.")
    if aporte is None:
        raise ErroDeValidacao(mensagem="Aporte não encontrado.", campo="aporte_id")
    if (
        not aporte.ressarcivel
        or aporte.situacao_de_ressarcimento != SituacaoDeRessarcimento.em_aberto
    ):
        raise ErroDeValidacao(
            mensagem="Este aporte não está em aberto para ressarcimento.", campo="aporte_id"
        )
    receita_valida = (
        receita_destinada is not None
        and receita_destinada.destinacao == DestinacaoDoAporte.ressarcimento
    )
    if not receita_valida:
        raise ErroDeValidacao(
            mensagem="Receita destinada não encontrada, ou não é de destinação ressarcimento.",
            campo="receita_destinada_id",
        )
    if data is None:
        raise ErroDeValidacao(mensagem="Ressarcimento exige a data.", campo="data")

    valor_em_reais = aporte.valor_de_origem if aporte.valor_de_origem is not None else Decimal("0")

    # Trava o aporte da receita destinada: dois Admins ressarcindo contra a
    # mesma receita ao mesmo tempo não estouram o teto (design — Decisions
    # 3, Risks).
    sessao.query(Aporte.id).filter(Aporte.id == receita_destinada.id).with_for_update().all()

    saldo_em_aberto = saldo_em_aberto_da_receita(sessao, receita_destinada=receita_destinada)
    if valor_em_reais > saldo_em_aberto:
        raise ErroDeValidacao(
            mensagem="A receita destinada não cobre este valor.", campo="receita_destinada_id"
        )

    referencia, nome_original, tipo_mime, tamanho = _processar_comprovante_obrigatorio(
        conteudo=comprovante_conteudo,
        nome_original=comprovante_nome_original,
        tipo_mime=comprovante_tipo,
        armazenamento=armazenamento,
    )

    lancamento_original = sessao.get(Lancamento, aporte.lancamento_id)
    lancar_ajuste(
        sessao,
        operador=operador,
        lancamento_original=lancamento_original,
        quantidade=Decimal("0"),
        valor_em_moedas=-lancamento_original.valor_em_moedas,
        motivo=f"Ressarcimento do aporte {aporte.id}",
    )

    aporte.situacao_de_ressarcimento = SituacaoDeRessarcimento.ressarcido

    ressarcimento = Ressarcimento(
        aporte_id=aporte.id,
        receita_destinada_id=receita_destinada.id,
        valor_em_reais=valor_em_reais,
        admin_pagador_id=operador.id,
        data=data,
        comprovante_referencia=referencia,
        comprovante_nome_original=nome_original,
        comprovante_tipo=tipo_mime,
        comprovante_tamanho=tamanho,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(ressarcimento)
    sessao.flush()
    return ressarcimento


def total_de_receita_destinada_em_aberto(sessao: Session) -> Decimal:
    """A soma do que toda receita destinada ainda cobre — o valor de
    origem de cada aporte de destinação ressarcimento menos todo o já
    pago —, exibida ao lado da fila para a decisão do Admin (`RF-07-24`,
    `RN-07-17`)."""
    total_origem = (
        sessao.query(func.coalesce(func.sum(Aporte.valor_de_origem), 0))
        .filter(Aporte.destinacao == DestinacaoDoAporte.ressarcimento)
        .scalar()
    )
    total_pago = sessao.query(func.coalesce(func.sum(Ressarcimento.valor_em_reais), 0)).scalar()
    return Decimal(total_origem) - Decimal(total_pago)


def listar_absorcoes_do_provedor(sessao: Session, *, operador: Persona) -> list[Aporte]:
    """A situação de ressarcimento dos aportes que o próprio provedor
    absorveu — Mestre ou Admin, somente leitura (`RF-07-24`, `RN-07-17`,
    PRD-07 §§4, 9)."""
    if operador.papel not in (Papel.mestre, Papel.admin):
        raise PermissaoNegada(mensagem="Só Mestre ou Admin acompanham as próprias absorções.")

    return (
        sessao.query(Aporte)
        .filter(Aporte.forma == FormaDeAporte.absorcao, Aporte.provedor_id == operador.id)
        .order_by(Aporte.data_do_aporte.desc())
        .all()
    )
