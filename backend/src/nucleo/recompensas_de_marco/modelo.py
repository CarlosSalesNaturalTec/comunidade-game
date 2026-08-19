import uuid
from decimal import Decimal

from sqlalchemy import ForeignKey, Index, Numeric, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from ..autoria import ComAutoria
from ..banco import Base


class RecompensaDeMarco(Base, ComAutoria):
    """A recompensa que o Mestre autor declara para um marco da própria
    trilha — o livro, a camisa e o kit em MDF, entregues sem custo ao
    Guerreiro(a) que o alcança (`RF-09-71`, PRD-09 §8). O marco aceito é
    sempre uma **missão** da própria trilha: é o único marco que o núcleo
    hoje verifica alcançado (design — Decisions).

    Sem ponto de apoio nem comunidade: a trilha é bem comum e alcança todas
    as comunidades, então o lastro só se confere no ato da entrega
    (`RF-09-72`, `RN-09-27`). `quantidade` é o teto declarado, nunca
    decrementado — a terceira recusa da entrega compara com a **contagem**
    de `EntregaDeRecompensa` desta recompensa, e é também a quantidade do
    tipo de recurso debitada em cada entrega (design — Decisions).
    """

    __tablename__ = "recompensa_de_marco"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    trilha_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("trilha.id"), nullable=False)
    missao_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("missao.id"), nullable=False)
    tipo_de_recurso_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("tipo_de_recurso.id"), nullable=False
    )
    quantidade: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)

    __table_args__ = (Index("ix_recompensa_de_marco_trilha_id", "trilha_id"),)


class EntregaDeRecompensa(Base, ComAutoria):
    """A baixa definitiva de uma `RecompensaDeMarco` a um Guerreiro(a) —
    uma por Guerreiro(a) que alcança o marco, sem situação própria na
    recompensa (`RF-07-13`, `RF-09-76`, PRD-07 §8). O ponto de apoio é
    escolhido no ato, porque a trilha não tem um (design — Decisions).
    `lancamento_id` é o débito emitido na mesma operação; `ComAutoria` já
    grava o Mestre que entregou, o papel e a data e hora com fuso, o mesmo
    precedente de `trocas.modelo.Troca`.
    """

    __tablename__ = "entrega_de_recompensa"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    recompensa_de_marco_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("recompensa_de_marco.id"), nullable=False
    )
    guerreiro_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("persona.id"), nullable=False)
    ponto_de_apoio_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("ponto_de_apoio.id"), nullable=False
    )
    lancamento_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("lancamento.id"), nullable=False
    )

    __table_args__ = (
        Index("ix_entrega_de_recompensa_recompensa_de_marco_id", "recompensa_de_marco_id"),
        Index("ix_entrega_de_recompensa_guerreiro_id", "guerreiro_id"),
    )
