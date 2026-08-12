import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column

from ..autoria import ComAutoria
from ..banco import Base


class VinculoResponsavel(Base, ComAutoria):
    """Atributos do PRD-01 §8. `ComAutoria` cobre "cadastrado por" (Admin ou
    Mestre); `fim` nulo é o que a contagem do teto de três trata como
    vigente (RN-01-19, design — decisões).
    """

    __tablename__ = "vinculo_responsavel"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    responsavel_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("persona.id"), nullable=False
    )
    guerreiro_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("persona.id"), nullable=False)
    grau_de_parentesco: Mapped[str] = mapped_column(String(64), nullable=False)
    inicio: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    fim: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
