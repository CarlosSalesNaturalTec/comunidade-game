from datetime import UTC, datetime

from pydantic import AwareDatetime
from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

# Toda data e hora de entrada e saída exige fuso explícito (PRD-01 §9).
DataHoraComFuso = AwareDatetime


def agora() -> datetime:
    """Momento corrente com fuso — ponto único para o que hoje já se repete
    como `datetime.now(UTC)` pelo núcleo, usado por quem deriva estado a
    partir do relógio (`RF-01-32`)."""
    return datetime.now(UTC)


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
