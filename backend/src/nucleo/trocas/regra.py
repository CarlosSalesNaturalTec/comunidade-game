from decimal import Decimal

from sqlalchemy.orm import Session

from ..aulas.modelo import Aula
from ..catalogo_avulso.modelo import ItemDeCatalogoAvulso
from ..catalogo_avulso.regra import falta_de_lastro
from ..comunidades.modelo import VinculoJogador
from ..erros import ErroDeValidacao, PermissaoNegada
from ..livro_razao.regra import lancar_debito
from ..personas.modelo import Papel, Persona
from ..ponto_extra.modelo import PontoExtra
from ..ponto_extra.regra import debitar_ponto_extra
from ..recursos.modelo import TipoDeRecurso
from ..recursos.regra import consultar_preco_de_referencia, consultar_valor_de_referencia
from ..tempo import agora
from .modelo import Troca


def _preco_vigente(sessao: Session, *, item: ItemDeCatalogoAvulso) -> int:
    """O preço em pontos extras da vigência corrente do tipo de recurso do
    item — nunca declarado por quem registra a troca (`RF-07-46`,
    `RF-07-38`, `RN-07-29`)."""
    tipo = sessao.get(TipoDeRecurso, item.tipo_de_recurso_id)
    preco = consultar_preco_de_referencia(sessao, tipo=tipo, data=agora().date())
    if preco is None:
        raise ErroDeValidacao(
            mensagem="Este item não tem preço de referência vigente.", campo="item_id"
        )
    return preco.preco_em_pontos_extras


def _valorar_debito(sessao: Session, *, tipo: TipoDeRecurso, quantidade: Decimal) -> Decimal:
    """A baixa da troca é valorada pela vigência do valor de referência no
    dia da entrega, no mesmo mecanismo de `reservas.regra._valorar_debito`
    (design — Decisions 6)."""
    referencia = consultar_valor_de_referencia(sessao, tipo=tipo, data=agora().date())
    if referencia is None:
        raise ErroDeValidacao(
            mensagem="Nenhuma vigência do valor de referência cobre a data da troca.",
            campo="item_id",
        )
    return (quantidade * referencia.valor_em_moedas).quantize(Decimal("0.01"))


def _bloquear_item(sessao: Session, *, item: ItemDeCatalogoAvulso) -> None:
    """`SELECT ... FOR UPDATE` da linha do item, para que duas trocas
    concorrentes do último item não passem as duas pela verificação de
    estoque (design — Risks)."""
    sessao.query(ItemDeCatalogoAvulso.id).filter_by(id=item.id).with_for_update().all()
    sessao.refresh(item)


def _validar_troca(
    sessao: Session, *, item: ItemDeCatalogoAvulso, guerreiro: Persona, preco: int
) -> None:
    """As quatro recusas, na ordem do spec — item/lastro, estoque,
    comunidade, saldo —, cada uma nomeando a condição para a resposta 422,
    antes de qualquer escrita (`RF-07-37`, `RN-07-26`, `RN-01-40`, design —
    Decisions 3, 4)."""
    if not item.ativo or falta_de_lastro(sessao, item=item) > 0:
        raise ErroDeValidacao(
            mensagem="Item inativo ou sem lastro suficiente para a troca.", campo="item_id"
        )
    if item.estoque < 1:
        raise ErroDeValidacao(mensagem="Item sem estoque para a troca.", campo="item_id")

    vinculo: VinculoJogador | None = guerreiro.vinculo_vigente
    if vinculo is None or vinculo.comunidade_virtual_id != item.comunidade_virtual_id:
        raise ErroDeValidacao(
            mensagem="Guerreiro(a) precisa ser da comunidade do item.", campo="guerreiro_id"
        )

    conta = sessao.query(PontoExtra).filter_by(guerreiro_id=guerreiro.id).first()
    saldo = conta.saldo_disponivel if conta is not None else 0
    if saldo < preco:
        raise ErroDeValidacao(
            mensagem="Saldo disponível de pontos extras insuficiente para a troca.",
            campo="guerreiro_id",
        )


def registrar_troca(
    sessao: Session,
    *,
    operador: Persona,
    aula: Aula | None,
    item: ItemDeCatalogoAvulso | None,
    guerreiro: Persona | None,
) -> Troca:
    """Restrita ao Mestre vinculado à comunidade da aula — grava a troca, o
    débito do saldo disponível, o decremento do estoque e o débito no
    livro-razão numa operação só, sem estado intermediário (`RF-07-35`,
    `RF-07-36`, `RN-07-27`, design — Decisions 1, 6, 7). O núcleo não
    verifica o estado da aula nem a presença do Guerreiro(a) nela — garantia
    da App 01 (documento 02 §8.2, decisão 1)."""
    if operador.papel != Papel.mestre:
        raise PermissaoNegada(mensagem="Só o Mestre registra a troca.")
    if aula is None:
        raise ErroDeValidacao(mensagem="Troca exige uma aula.", campo="aula_id")
    vinculo: VinculoJogador | None = operador.vinculo_vigente
    if vinculo is None or vinculo.comunidade_virtual_id != aula.comunidade_virtual_id:
        raise PermissaoNegada(
            mensagem="Só o Mestre vinculado à comunidade da aula registra a troca."
        )
    if item is None:
        raise ErroDeValidacao(mensagem="Troca exige um item do catálogo.", campo="item_id")
    if guerreiro is None:
        raise ErroDeValidacao(mensagem="Troca exige o Guerreiro(a).", campo="guerreiro_id")

    preco = _preco_vigente(sessao, item=item)

    _bloquear_item(sessao, item=item)
    _validar_troca(sessao, item=item, guerreiro=guerreiro, preco=preco)

    troca = Troca(
        item_de_catalogo_avulso_id=item.id,
        guerreiro_id=guerreiro.id,
        preco_cobrado=preco,
        aula_id=aula.id,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(troca)

    debitar_ponto_extra(sessao, guerreiro_id=guerreiro.id, valor=preco)

    item.estoque -= 1

    tipo = sessao.get(TipoDeRecurso, item.tipo_de_recurso_id)
    valor_em_moedas = _valorar_debito(sessao, tipo=tipo, quantidade=Decimal("1"))
    lancar_debito(
        sessao,
        tipo_de_recurso_id=item.tipo_de_recurso_id,
        ponto_de_apoio_id=item.ponto_de_apoio_id,
        quantidade=Decimal("1"),
        valor_em_moedas=valor_em_moedas,
        operador=operador,
        aula_id=None,
    )

    sessao.flush()
    return troca


def listar_trocas(sessao: Session, *, operador: Persona) -> list[Troca]:
    """Guerreiro(a) lê só as próprias; Mestre, as das comunidades a que está
    vinculado; Admin, todas; Apoiador e responsável recebem 403 — sem
    moedas nem reais na saída, o custo real fica no livro-razão (`RF-07-35`,
    `RN-07-24`, `RN-07-13`)."""
    if operador.papel == Papel.guerreiro:
        return (
            sessao.query(Troca)
            .filter_by(guerreiro_id=operador.id)
            .order_by(Troca.registrado_em.desc())
            .all()
        )
    if operador.papel == Papel.mestre:
        vinculo: VinculoJogador | None = operador.vinculo_vigente
        if vinculo is None:
            return []
        return (
            sessao.query(Troca)
            .join(Aula, Aula.id == Troca.aula_id)
            .filter(Aula.comunidade_virtual_id == vinculo.comunidade_virtual_id)
            .order_by(Troca.registrado_em.desc())
            .all()
        )
    if operador.papel == Papel.admin:
        return sessao.query(Troca).order_by(Troca.registrado_em.desc()).all()
    raise PermissaoNegada(mensagem="Persona sem histórico de trocas a consultar.")
