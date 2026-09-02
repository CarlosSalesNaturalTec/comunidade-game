import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, Uuid, func, text
from sqlalchemy.orm import Mapped, mapped_column

from ..banco import Base


class Favorito(Base):
    """Preferência de leitura do Apoiador sobre um Guerreiro(a) ou um
    Mestre — nunca canal, nunca lastro (PRD-14 §8, design — decisão 3).
    Exatamente um entre `guerreiro_id` e `mestre_id` é preenchido, e o
    índice único parcial por alvo garante um só favorito por par.
    """

    __tablename__ = "favorito"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    apoiador_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("persona.id"), nullable=False)
    guerreiro_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("persona.id"), nullable=True
    )
    mestre_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("persona.id"), nullable=True
    )
    incluido_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        CheckConstraint(
            "(guerreiro_id IS NOT NULL AND mestre_id IS NULL) OR "
            "(guerreiro_id IS NULL AND mestre_id IS NOT NULL)",
            name="ck_favorito_guerreiro_ou_mestre",
        ),
        Index(
            "uq_favorito_apoiador_id_guerreiro_id",
            "apoiador_id",
            "guerreiro_id",
            unique=True,
            postgresql_where=text("guerreiro_id IS NOT NULL"),
        ),
        Index(
            "uq_favorito_apoiador_id_mestre_id",
            "apoiador_id",
            "mestre_id",
            unique=True,
            postgresql_where=text("mestre_id IS NOT NULL"),
        ),
    )
