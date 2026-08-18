import uuid
from decimal import Decimal

from sqlalchemy import func
from sqlalchemy.orm import Session

from ..aulas.modelo import Aula, RecursoDeclaradoDaAula, SituacaoDaAula
from ..erros import ErroDeValidacao
from ..livro_razao.modelo import Lancamento
from ..livro_razao.regra import lancar_debito, saldo_de
from ..personas.modelo import Persona
from ..pontos_de_apoio.modelo import PontoDeApoio
from ..recursos.modelo import TipoDeRecurso
from ..recursos.regra import consultar_valor_de_referencia
from ..tempo import agora
from .modelo import EstadoDaReserva, Reserva


def quantidade_reservada(
    sessao: Session, *, tipo_de_recurso_id: uuid.UUID, ponto_de_apoio_id: uuid.UUID
) -> Decimal:
    """Agregação sobre as reservas no estado **reservada**, como o saldo é
    agregação sobre `lancamento` — nenhum número guardado, recontar devolve
    o mesmo resultado (`RF-07-07`, design — Decisions 2)."""
    total = (
        sessao.query(func.coalesce(func.sum(Reserva.quantidade), 0))
        .filter(
            Reserva.tipo_de_recurso_id == tipo_de_recurso_id,
            Reserva.ponto_de_apoio_id == ponto_de_apoio_id,
            Reserva.estado == EstadoDaReserva.reservada,
        )
        .scalar()
    )
    return Decimal(total)


def disponivel_de(
    sessao: Session, *, tipo_de_recurso_id: uuid.UUID, ponto_de_apoio_id: uuid.UUID
) -> Decimal:
    """O saldo derivado menos o reservado — é contra ela, nunca contra o
    saldo total, que toda decisão de reservar é tomada (`RF-07-07`,
    `RF-07-08`, design — Decisions 2)."""
    saldo = saldo_de(
        sessao, tipo_de_recurso_id=tipo_de_recurso_id, ponto_de_apoio_id=ponto_de_apoio_id
    )
    reservado = quantidade_reservada(
        sessao, tipo_de_recurso_id=tipo_de_recurso_id, ponto_de_apoio_id=ponto_de_apoio_id
    )
    return saldo - reservado


def _bloquear_par(
    sessao: Session, *, tipo_de_recurso_id: uuid.UUID, ponto_de_apoio_id: uuid.UUID
) -> None:
    """`SELECT ... FOR UPDATE` sobre as linhas do par tipo/ponto de apoio em
    `lancamento` e `reserva`, para que dois agendamentos concorrentes não
    reservem o mesmo saldo disponível (design — Decisions 4, Risks)."""
    sessao.query(Lancamento.id).filter(
        Lancamento.tipo_de_recurso_id == tipo_de_recurso_id,
        Lancamento.ponto_de_apoio_id == ponto_de_apoio_id,
    ).with_for_update().all()
    sessao.query(Reserva.id).filter(
        Reserva.tipo_de_recurso_id == tipo_de_recurso_id,
        Reserva.ponto_de_apoio_id == ponto_de_apoio_id,
    ).with_for_update().all()


def tentar_reservar_recursos(sessao: Session, *, aula: Aula, operador: Persona) -> bool:
    """Avalia a disponível de cada recurso que a aula declara e, havendo
    para **todos**, grava uma `Reserva` por recurso; faltando qualquer
    parcela, não reserva nada — nem a dos tipos que tinham saldo. Devolve se
    reservou (`RF-07-08`, `RN-07-01`, design — Decisions 1, 4).
    """
    declarados = sessao.query(RecursoDeclaradoDaAula).filter_by(aula_id=aula.id).all()
    if not declarados:
        return True

    for declarado in declarados:
        _bloquear_par(
            sessao,
            tipo_de_recurso_id=declarado.tipo_de_recurso_id,
            ponto_de_apoio_id=aula.ponto_de_apoio_id,
        )

    for declarado in declarados:
        disponivel = disponivel_de(
            sessao,
            tipo_de_recurso_id=declarado.tipo_de_recurso_id,
            ponto_de_apoio_id=aula.ponto_de_apoio_id,
        )
        if disponivel < declarado.quantidade:
            return False

    for declarado in declarados:
        sessao.add(
            Reserva(
                aula_id=aula.id,
                tipo_de_recurso_id=declarado.tipo_de_recurso_id,
                ponto_de_apoio_id=aula.ponto_de_apoio_id,
                quantidade=declarado.quantidade,
                estado=EstadoDaReserva.reservada,
                autor_id=operador.id,
                papel_do_autor=operador.papel.value,
            )
        )
    sessao.flush()
    return True


def confirmar_aulas_pendentes(
    sessao: Session, *, tipo: TipoDeRecurso, ponto_de_apoio: PontoDeApoio, operador: Persona
) -> list[Aula]:
    """Varre as aulas pendentes de lastro daquele ponto de apoio que
    declaram o tipo recém-creditado, da mais próxima para a mais distante
    pelo horário inicial, e confirma — com a reserva efetivada no mesmo ato
    — as que couberem (`RN-07-37`, design — Decisions 5)."""
    candidatas = (
        sessao.query(Aula)
        .join(RecursoDeclaradoDaAula, RecursoDeclaradoDaAula.aula_id == Aula.id)
        .filter(
            Aula.situacao == SituacaoDaAula.pendente_de_lastro,
            Aula.ponto_de_apoio_id == ponto_de_apoio.id,
            RecursoDeclaradoDaAula.tipo_de_recurso_id == tipo.id,
        )
        .order_by(Aula.inicio_em.asc())
        .distinct()
        .all()
    )

    confirmadas = []
    for aula in candidatas:
        if tentar_reservar_recursos(sessao, aula=aula, operador=operador):
            aula.situacao = SituacaoDaAula.confirmada
            sessao.flush()
            confirmadas.append(aula)
    return confirmadas


def _valorar_debito(sessao: Session, *, tipo: TipoDeRecurso, quantidade: Decimal) -> Decimal:
    """A baixa é valorada pela vigência do valor de referência no dia do
    lançamento da atividade, no mesmo mecanismo que já valora o crédito do
    aporte (`RN-07-04`, aportes.regra._valorar_em_moedas)."""
    referencia = consultar_valor_de_referencia(sessao, tipo=tipo, data=agora().date())
    if referencia is None:
        raise ErroDeValidacao(
            mensagem="Nenhuma vigência do valor de referência cobre a data do débito.",
            campo="tipo_de_recurso_id",
        )
    return (quantidade * referencia.valor_em_moedas).quantize(Decimal("0.01"))


def consumir_reservas_da_aula(
    sessao: Session, *, aula: Aula, operador: Persona
) -> list[Lancamento]:
    """Converte cada reserva ainda reservada da aula em baixa: um débito por
    reserva, no ponto de apoio da aula, e a reserva passa a **consumida**
    (`RF-07-09`, `RN-07-36`, design — Decisions 7)."""
    reservas = (
        sessao.query(Reserva).filter_by(aula_id=aula.id, estado=EstadoDaReserva.reservada).all()
    )

    lancamentos = []
    for reserva in reservas:
        tipo = sessao.get(TipoDeRecurso, reserva.tipo_de_recurso_id)
        valor_em_moedas = _valorar_debito(sessao, tipo=tipo, quantidade=reserva.quantidade)
        lancamento = lancar_debito(
            sessao,
            tipo_de_recurso_id=reserva.tipo_de_recurso_id,
            ponto_de_apoio_id=reserva.ponto_de_apoio_id,
            quantidade=reserva.quantidade,
            valor_em_moedas=valor_em_moedas,
            operador=operador,
            aula_id=aula.id,
        )
        reserva.estado = EstadoDaReserva.consumida
        lancamentos.append(lancamento)
    sessao.flush()
    return lancamentos


def liberar_reservas_da_aula(sessao: Session, *, aula: Aula) -> None:
    """O cancelamento leva as reservas ainda reservadas a **liberada**,
    devolvendo as quantidades à disponível (`RF-07-09`, spec
    `reserva-de-recurso`)."""
    reservas = (
        sessao.query(Reserva).filter_by(aula_id=aula.id, estado=EstadoDaReserva.reservada).all()
    )
    for reserva in reservas:
        reserva.estado = EstadoDaReserva.liberada
    sessao.flush()
