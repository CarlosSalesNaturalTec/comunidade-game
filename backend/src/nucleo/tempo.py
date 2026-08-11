from datetime import datetime

from pydantic import AwareDatetime
from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

# Toda data e hora de entrada e saída exige fuso explícito (PRD-01 §9).
DataHoraComFuso = AwareDatetime


class ComMomentoDoFato:
    """Mixin de modelo para entidades cujo fato pode chegar depois de acontecer.

    `momento_do_fato` é informado por quem registra; `momento_do_registro` é
    sempre o instante em que o núcleo recebeu o registro. A data do fato nunca é
    substituída pela data do registro (PRD-01 §9).
    """

    momento_do_fato: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    momento_do_registro: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
