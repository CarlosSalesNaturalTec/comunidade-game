import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy import Date, ForeignKey, Integer, Numeric, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from ..autoria import ComAutoria
from ..banco import Base


class Ressarcimento(Base, ComAutoria):
    """O pagamento que devolve, a quem absorveu, o que a plataforma
    absorveu em seu nome — só quando há **receita destinada** que o cubra
    (`RF-07-22`, `RF-07-25`, `RN-07-17`, PRD-07 §8). `aporte_id` é único:
    um aporte tem no máximo um ressarcimento. `receita_destinada_id`
    referencia o aporte de destinação `ressarcimento` que financia o
    pagamento — o teto é o valor de origem dele menos o que já foi pago
    contra ele (design — Decisions 3).

    O comprovante é **exigido**, ao contrário do de `Aporte`: sem ele o
    registro é recusado. Segue o mesmo regime de acesso restrito à gestão
    (`RF-07-22`, PRD-07 §11).
    """

    __tablename__ = "ressarcimento"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    aporte_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("aporte.id"), unique=True, nullable=False
    )
    receita_destinada_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("aporte.id"), nullable=False
    )
    valor_em_reais: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    admin_pagador_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("persona.id"), nullable=False
    )
    data: Mapped[date] = mapped_column(Date, nullable=False)
    comprovante_referencia: Mapped[str] = mapped_column(String(512), nullable=False)
    comprovante_nome_original: Mapped[str | None] = mapped_column(String(256), nullable=True)
    comprovante_tipo: Mapped[str] = mapped_column(String(128), nullable=False)
    comprovante_tamanho: Mapped[int] = mapped_column(Integer, nullable=False)
