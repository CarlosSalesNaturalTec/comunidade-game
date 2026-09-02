import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String, UniqueConstraint, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column

from ..banco import Base


class FamiliaDeSelo(enum.StrEnum):
    """As quatro famílias do documento 14 §8 (`RN-14-33`, design — Decisions
    8). Os selos de código ficam de fora: dependem da modalidade de apoio em
    código, ainda `[Proposta]`."""

    frente = "frente"
    modalidade = "modalidade"
    ato = "ato"
    multiplicacao = "multiplicacao"


class SeloDoApoiador(Base):
    """O selo creditado a um participante da missão na homologação que a
    conclui — somente inserção, sem rota de remoção (`RF-14-66`, `RN-14-33`,
    `RN-14-36`, design — Decisions 6). O índice único por (Apoiador, missão,
    selo) impede o crédito duplo se a homologação for repetida. O selo de
    mutirão (`RN-14-34`) é gravado pelo núcleo, com `selo_nome` fixo e
    `familia = ato`, não declarado pelo Admin."""

    __tablename__ = "selo_do_apoiador"
    __table_args__ = (
        UniqueConstraint(
            "apoiador_id",
            "missao_do_apoiador_id",
            "selo_nome",
            name="uq_selo_do_apoiador_apoiador_missao_selo",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    apoiador_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("persona.id"), nullable=False)
    familia: Mapped[FamiliaDeSelo] = mapped_column(
        Enum(FamiliaDeSelo, native_enum=False, length=16), nullable=False
    )
    selo_nome: Mapped[str] = mapped_column(String(128), nullable=False)
    missao_do_apoiador_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("missao_do_apoiador.id"), nullable=False
    )
    creditado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
