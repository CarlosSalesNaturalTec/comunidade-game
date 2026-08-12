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
    """Registro de que a equipe da trilha entregou, ao final dela, o que
    produziu a partir do que aprendeu — a Culminância do documento 11 §2.
    `equipe_id` é a equipe da trilha que assina o registro (`RF-01-64`);
    `ComAutoria.autor_id` continua a gravar quem entregou pela equipe —
    mesmo sentido de sempre, e nunca muda, nem na devolução (`RN-01-13`).
    `validado_por_id` e `validado_em` guardam o Mestre autor ou o Admin
    que decide, preenchidos só na transição (design — decisões). A
    unicidade passa a ser por equipe: como cada Guerreiro(a) tem uma só
    equipe por trilha (`RN-01-44`), a equipe segue entregando no máximo
    uma criação original por trilha.
    """

    __tablename__ = "criacao_original"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    trilha_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("trilha.id"), nullable=False)
    equipe_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("equipe.id"), nullable=False)
    producao: Mapped[str] = mapped_column(Text, nullable=False)
    situacao: Mapped[SituacaoDaCriacaoOriginal] = mapped_column(
        Enum(SituacaoDaCriacaoOriginal, native_enum=False, length=16), nullable=False
    )
    validado_por_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("persona.id"), nullable=True
    )
    validado_em: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (UniqueConstraint("equipe_id", name="uq_criacao_original_equipe_id"),)
