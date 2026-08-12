import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column


class ComAutoria:
    """Mixin de modelo para toda entidade que nasce de uma escrita autenticada.

    Grava quem escreveu, com que papel e quando — a trilha de auditoria
    consultável (RF-01-29) é rota de outra fatia; aqui só nasce o registro
    (RF-01-03). A data do registro nunca substitui a do fato, quando a
    entidade também usa `ComMomentoDoFato`.
    """

    autor_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("persona.id"), nullable=False)
    papel_do_autor: Mapped[str] = mapped_column(String(32), nullable=False)
    registrado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
