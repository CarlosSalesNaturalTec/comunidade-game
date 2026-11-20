import logging
import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import func
from sqlalchemy.orm import Session

from ..aulas.modelo import Aula, RecursoDeclaradoDaAula, SituacaoDaAula
from ..desafios_extras.modelo import DesafioExtra
from ..erros import ErroDeValidacao
from ..livro_razao.modelo import Lancamento
from ..livro_razao.regra import lancar_debito, saldo_de
from ..personas.modelo import Persona
from ..pontos_de_apoio.modelo import PontoDeApoio
from ..recursos.modelo import NaturezaDoRecurso, TipoDeRecurso
from ..recursos.regra import consultar_valor_de_referencia
from ..tempo import agora
from .modelo import EstadoDaReserva, Reserva

_registro = logging.getLogger(__name__)


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


PAPEL_DO_SISTEMA = "sistema"

_SITUACOES_SEM_DESFECHO = (
    SituacaoDaAula.prevista,
    SituacaoDaAula.confirmada,
    SituacaoDaAula.pendente_de_lastro,
)


class _AulaSemValoracao(Exception):
    """Tipo reservado sem vigência do valor de referência no dia do fim da
    aula: a aula fica para a próxima varredura (design — decisão 3)."""


def consumir_reservas_da_aula(sessao: Session, *, aula: Aula) -> list[Lancamento]:
    """Converte cada reserva ainda reservada da aula em baixa: um débito por
    reserva, no ponto de apoio da aula, e a reserva passa a **consumida**.
    É ato do **sistema** no fim do horário — o autor da aula com o papel
    `sistema` —, valorado pela vigência do dia do fim da aula (`RF-07-09`,
    `RN-07-36`, `RN-07-43`, design — decisões 2 e 3)."""
    reservas = (
        sessao.query(Reserva).filter_by(aula_id=aula.id, estado=EstadoDaReserva.reservada).all()
    )
    dia_do_fim = aula.fim_em.date()

    valores = []
    for reserva in reservas:
        tipo = sessao.get(TipoDeRecurso, reserva.tipo_de_recurso_id)
        referencia = consultar_valor_de_referencia(sessao, tipo=tipo, data=dia_do_fim)
        if referencia is None:
            raise _AulaSemValoracao(tipo.nome)
        valores.append((reserva.quantidade * referencia.valor_em_moedas).quantize(Decimal("0.01")))

    lancamentos = []
    for reserva, valor_em_moedas in zip(reservas, valores, strict=True):
        lancamento = lancar_debito(
            sessao,
            tipo_de_recurso_id=reserva.tipo_de_recurso_id,
            ponto_de_apoio_id=reserva.ponto_de_apoio_id,
            quantidade=reserva.quantidade,
            valor_em_moedas=valor_em_moedas,
            aula_id=aula.id,
            autoria=(aula.autor_id, PAPEL_DO_SISTEMA),
        )
        reserva.estado = EstadoDaReserva.consumida
        lancamentos.append(lancamento)
    sessao.flush()
    return lancamentos


def encerrar_aulas_vencidas(sessao: Session, *, momento: datetime | None = None) -> int:
    """A aula não tem fechamento: passado o `fim_em`, a confirmada (ou a
    prevista) tem as reservas baixadas e passa a **realizada**, e a pendente
    de lastro passa a **realizada sem lastro**, sem baixa. `SKIP LOCKED`
    impede duas varreduras de pegar a mesma aula; a aula que não se pode
    valorar fica para a próxima. Devolve quantas aulas encerrou (`RF-07-09`,
    `RF-07-55`, `RF-01-91`, `RN-07-43`, design — decisão 1)."""
    momento = momento or agora()
    vencidas = (
        sessao.query(Aula)
        .filter(Aula.fim_em <= momento, Aula.situacao.in_(_SITUACOES_SEM_DESFECHO))
        .order_by(Aula.fim_em.asc())
        .with_for_update(skip_locked=True)
        .all()
    )

    encerradas = 0
    for aula in vencidas:
        if aula.situacao == SituacaoDaAula.pendente_de_lastro:
            aula.situacao = SituacaoDaAula.realizada_sem_lastro
        else:
            ponto_de_restauracao = sessao.begin_nested()
            try:
                consumir_reservas_da_aula(sessao, aula=aula)
            except _AulaSemValoracao as exc:
                ponto_de_restauracao.rollback()
                _registro.warning(
                    "Aula %s ficou para a próxima varredura: %s sem valor de referência "
                    "vigente no dia do fim.",
                    aula.id,
                    exc,
                )
                continue
            ponto_de_restauracao.commit()
            aula.situacao = SituacaoDaAula.realizada
        encerradas += 1
    sessao.flush()
    return encerradas


def varrer_aulas_vencidas(sessao: Session) -> None:
    """O disparo sob demanda: roda a varredura e a grava antes da operação
    que depende da situação da aula, do saldo ou da necessidade (decisão do
    fundador de 2026-11-20, design — decisão 4)."""
    encerrar_aulas_vencidas(sessao)
    sessao.commit()


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


def reservar_recompensa_do_desafio(
    sessao: Session, *, desafio: DesafioExtra, operador: Persona
) -> Reserva:
    """A publicação do desafio extra reserva, no mesmo ato, a quantidade
    disponível declarada — a recompensa é aquela quantidade do tipo de
    recurso no ponto de apoio da proposta, o mesmo par que `lastro_provido`
    já consulta no custeio por saldo (`RF-07-39`, design — Decisions 5).
    Bloqueia o par antes de conferir a disponível, o mesmo caminho do
    agendamento concorrente (design — Decisions 3), recusa tipo de recurso
    de natureza durável e recusa sem disponível suficiente — nos dois
    casos, sem gravar reserva alguma (`RN-07-01`, `RN-07-07`)."""
    _bloquear_par(
        sessao,
        tipo_de_recurso_id=desafio.tipo_de_recurso_id,
        ponto_de_apoio_id=desafio.ponto_de_apoio_id,
    )
    tipo = sessao.get(TipoDeRecurso, desafio.tipo_de_recurso_id)
    if tipo.natureza == NaturezaDoRecurso.duravel:
        raise ErroDeValidacao(
            mensagem=(
                "Tipo de recurso de natureza durável não é reservável: o saldo é "
                "patrimônio, não insumo de atividade."
            ),
            campo="tipo_de_recurso_id",
        )

    quantidade = Decimal(desafio.quantidade_disponivel)
    disponivel = disponivel_de(
        sessao,
        tipo_de_recurso_id=desafio.tipo_de_recurso_id,
        ponto_de_apoio_id=desafio.ponto_de_apoio_id,
    )
    if disponivel < quantidade:
        raise ErroDeValidacao(
            mensagem="A recompensa não cabe na quantidade disponível daquele ponto de apoio.",
            campo="quantidade_disponivel",
        )

    reserva = Reserva(
        desafio_extra_id=desafio.id,
        tipo_de_recurso_id=desafio.tipo_de_recurso_id,
        ponto_de_apoio_id=desafio.ponto_de_apoio_id,
        quantidade=quantidade,
        estado=EstadoDaReserva.reservada,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(reserva)
    sessao.flush()
    return reserva


def liberar_reservas_do_desafio(sessao: Session, *, desafio: DesafioExtra) -> None:
    """O encerramento do desafio pelo Admin leva a **liberada** toda
    reserva daquele desafio ainda **reservada**, devolvendo a quantidade à
    disponível (`RF-07-40`, spec `reserva-de-recurso`)."""
    reservas = (
        sessao.query(Reserva)
        .filter_by(desafio_extra_id=desafio.id, estado=EstadoDaReserva.reservada)
        .all()
    )
    for reserva in reservas:
        reserva.estado = EstadoDaReserva.liberada
    sessao.flush()
