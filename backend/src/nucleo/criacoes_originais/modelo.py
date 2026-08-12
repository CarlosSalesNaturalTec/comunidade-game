import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Text, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from ..autoria import ComAutoria
from ..banco import Base


class SituacaoDaCriacaoOriginal(enum.StrEnum):
    entregue = "entregue"
    validada = "validada"
    devolvida = "devolvida"


class CriacaoOriginal(Base, ComAutoria):
    """Registro de que um Guerreiro(a) entregou, ao final da trilha, o que
    produziu a partir do que aprendeu — a Culminância do documento 11 §2.
    `ComAutoria.autor_id` grava o próprio Guerreiro(a) que entrega, a
    mesma permissão que o PRD-01 §4 já lista ("Guerreiro(a) escreve...
    suas criações"), e nunca muda, nem na devolução (`RN-01-13`).
    `validado_por_id` e `validado_em` guardam o Mestre autor ou o Admin
    que decide, preenchidos só na transição (design — decisões). A
    unicidade por (autor, trilha) evita mais de uma entrega por trilha e,
    com ela, crédito duplicado de pontos e do badge de autoria.
    """

    __tablename__ = "criacao_original"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    trilha_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("trilha.id"), nullable=False)
    producao: Mapped[str] = mapped_column(Text, nullable=False)
    situacao: Mapped[SituacaoDaCriacaoOriginal] = mapped_column(
        Enum(SituacaoDaCriacaoOriginal, native_enum=False, length=16), nullable=False
    )
    validado_por_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("persona.id"), nullable=True
    )
    validado_em: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        UniqueConstraint("autor_id", "trilha_id", name="uq_criacao_original_autor_id_trilha_id"),
    )
