import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, Index, String, Uuid, func, text
from sqlalchemy.orm import Mapped, mapped_column

from ..banco import Base


class NaturezaDaChave(enum.StrEnum):
    do_projeto = "do_projeto"
    de_terceiro = "de_terceiro"


class SituacaoDaChave(enum.StrEnum):
    vigente = "vigente"
    revogada = "revogada"


class ChaveDeAplicacao(Base):
    """Identifica a aplicação que chama o núcleo — nunca a pessoa (RN-01-33).

    Guarda apenas o resumo criptográfico do segredo (RN-01-35): não há coluna
    que receba o segredo em claro.
    """

    __tablename__ = "chave_de_aplicacao"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    aplicacao: Mapped[str] = mapped_column(String(64), nullable=False)
    ambiente: Mapped[str] = mapped_column(String(32), nullable=False)
    natureza: Mapped[NaturezaDaChave] = mapped_column(
        Enum(NaturezaDaChave, native_enum=False, length=32), nullable=False
    )
    resumo_do_segredo: Mapped[str] = mapped_column(String(64), nullable=False)
    emitida_por: Mapped[str | None] = mapped_column(String(128), nullable=True)
    emitida_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    prazo_de_apresentacao: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    url_apresentada: Mapped[str | None] = mapped_column(String(512), nullable=True)
    situacao: Mapped[SituacaoDaChave] = mapped_column(
        Enum(SituacaoDaChave, native_enum=False, length=32),
        nullable=False,
        default=SituacaoDaChave.vigente,
    )
    revogada_por: Mapped[str | None] = mapped_column(String(128), nullable=True)
    motivo_da_revogacao: Mapped[str | None] = mapped_column(String(512), nullable=True)
    revogada_em: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        Index(
            "uq_chave_vigente_por_aplicacao_e_ambiente",
            "aplicacao",
            "ambiente",
            unique=True,
            postgresql_where=text("situacao = 'vigente'"),
        ),
    )
