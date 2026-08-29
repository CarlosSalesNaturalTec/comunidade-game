import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Index, Text, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column

from ..banco import Base
from ..fila.modelo import SituacaoDaSolicitacao


class TipoDeSolicitacaoDoResponsavel(enum.StrEnum):
    acesso = "acesso"
    correcao = "correcao"
    exclusao = "exclusao"
    esclarecimento = "esclarecimento"


class SolicitacaoDoResponsavel(Base):
    """A quinta solicitação do PRD-01 §8 — o pedido de direitos do
    responsável sobre o Guerreiro(a) a que está vinculado, nos quatro tipos
    (`RF-13-22`, `RF-13-24`). Vocabulário do PRD-13 — `tratado_por_id`,
    `desfecho`, `tratado_em` — em vez do mixin `EmAvaliacao`: o ato aqui é
    tratamento, não avaliação (design — decisão 2). Reusa
    `SituacaoDaSolicitacao` da fila: o pedido de exclusão é aceito como
    qualquer outro tipo (PRD-13 §9, design — decisão 5).
    """

    __tablename__ = "solicitacao_do_responsavel"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    responsavel_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("persona.id"), nullable=False
    )
    guerreiro_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("persona.id"), nullable=False)
    tipo: Mapped[TipoDeSolicitacaoDoResponsavel] = mapped_column(
        Enum(TipoDeSolicitacaoDoResponsavel, native_enum=False, length=16), nullable=False
    )
    texto: Mapped[str] = mapped_column(Text, nullable=False)
    situacao: Mapped[SituacaoDaSolicitacao] = mapped_column(
        Enum(SituacaoDaSolicitacao, native_enum=False, length=16),
        nullable=False,
        default=SituacaoDaSolicitacao.recebida,
    )
    registrado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    prazo: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    tratado_por_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("persona.id"), nullable=True
    )
    desfecho: Mapped[str | None] = mapped_column(Text, nullable=True)
    tratado_em: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        Index("ix_solicitacao_do_responsavel_responsavel_id", "responsavel_id"),
        Index("ix_solicitacao_do_responsavel_guerreiro_id", "guerreiro_id"),
    )
