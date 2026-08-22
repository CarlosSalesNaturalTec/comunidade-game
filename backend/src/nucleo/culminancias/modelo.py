import enum
import uuid

from sqlalchemy import Enum, ForeignKey, Text, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from ..autoria import ComAutoria
from ..banco import Base


class ModalidadeDaCulminancia(enum.StrEnum):
    individual = "individual"
    em_equipe = "em_equipe"


class Culminancia(Base, ComAutoria):
    """O que a criação original de uma trilha precisa ser — a especificação
    da produção final que o Mestre autor declara, no máximo uma por trilha
    (`RF-09-29`, `RF-09-30`, PRD-09 §8). Índice único em `trilha_id`: a
    segunda declaração substitui a linha existente, nunca cria uma segunda
    (design — decisões 1). `criacao_original` resolve a culminância
    aplicável pelo `trilha_id` que já tem, sem referência própria à
    culminância (design — decisões 2).
    """

    __tablename__ = "culminancia"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    trilha_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("trilha.id"), nullable=False)
    descricao: Mapped[str] = mapped_column(Text, nullable=False)
    modalidade: Mapped[ModalidadeDaCulminancia] = mapped_column(
        Enum(ModalidadeDaCulminancia, native_enum=False, length=16), nullable=False
    )
    criterio_de_validacao: Mapped[str] = mapped_column(Text, nullable=False)

    __table_args__ = (UniqueConstraint("trilha_id", name="uq_culminancia_trilha_id"),)
