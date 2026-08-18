import enum
import uuid
from decimal import Decimal

from sqlalchemy import Enum, ForeignKey, Index, Numeric, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from ..autoria import ComAutoria
from ..banco import Base


class EstadoDaReserva(enum.StrEnum):
    """Os três estados do PRD-07 §8 — sem um quarto valor para "pendente":
    a aula sem lastro simplesmente não tem reserva alguma até que ela caiba
    (design — Decisions 1)."""

    reservada = "reservada"
    consumida = "consumida"
    liberada = "liberada"


class Reserva(Base, ComAutoria):
    """O compromisso de saldo que a aula assume ao ser agendada — nunca um
    lançamento do livro-razão, e por isso sem efeito sobre o saldo derivado
    enquanto está reservada (`RF-07-08`, `RN-07-01`, design — Decisions 3).
    `ComAutoria` grava quem reservou e quando; a saída — baixa ou liberação
    — é o próprio `estado` mudando, sob a autoria que a trilha de auditoria
    já grava para toda escrita (design — Migration Plan).

    O índice composto é o que `reservas.regra.disponivel_de` e o
    `SELECT ... FOR UPDATE` do agendamento concorrente percorrem
    (design — Decisions 2, 4).
    """

    __tablename__ = "reserva"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    aula_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("aula.id"), nullable=False)
    tipo_de_recurso_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("tipo_de_recurso.id"), nullable=False
    )
    ponto_de_apoio_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("ponto_de_apoio.id"), nullable=False
    )
    quantidade: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    estado: Mapped[EstadoDaReserva] = mapped_column(
        Enum(EstadoDaReserva, native_enum=False, length=16),
        nullable=False,
        default=EstadoDaReserva.reservada,
    )

    __table_args__ = (
        Index(
            "ix_reserva_tipo_de_recurso_ponto_de_apoio_estado",
            "tipo_de_recurso_id",
            "ponto_de_apoio_id",
            "estado",
        ),
    )
