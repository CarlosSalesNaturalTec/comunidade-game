import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Index, String, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column

from ..banco import Base


class ComoAutenticou(enum.StrEnum):
    """As quatro formas do PRD-01 §8. Esta fatia só abre sessão por `social`
    e por `credencial`; `biometria` e `confirmacao_humana` são do Guerreiro(a),
    de fatia futura — o valor já nasce aqui para não migrar a coluna depois.
    """

    biometria = "biometria"
    confirmacao_humana = "confirmacao_humana"
    social = "social"
    credencial = "credencial"


class Sessao(Base):
    """Atributos do PRD-01 §8. O token em si nunca é gravado — só o resumo
    (design — token opaco), como já vale para o segredo da chave.
    """

    __tablename__ = "sessao"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    persona_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("persona.id"), nullable=False)
    resumo_do_token: Mapped[str] = mapped_column(String(64), nullable=False)
    iniciada_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    expira_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    origem: Mapped[str] = mapped_column(String(64), nullable=False)
    como_autenticou: Mapped[ComoAutenticou] = mapped_column(
        Enum(ComoAutenticou, native_enum=False, length=32), nullable=False
    )
    quem_confirmou: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("persona.id"), nullable=True
    )
    encerrada_em: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (Index("uq_sessao_resumo_do_token", "resumo_do_token", unique=True),)
