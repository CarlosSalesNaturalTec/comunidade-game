import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Integer, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from ..autoria import ComAutoria
from ..banco import Base

OBJETIVO_ODS_MINIMO = 1
OBJETIVO_ODS_MAXIMO = 18


class EtiquetaOds(Base, ComAutoria):
    """Rótulo descritivo que liga trilha ou missão a um Objetivo de
    Desenvolvimento Sustentável (documento 11 §2.1) — nunca as duas ao
    mesmo tempo, nem nenhuma das duas: a restrição abaixo torna a regra
    impossível de violar por qualquer caminho de escrita (`RF-01-40`,
    `RF-01-45`, design — decisões). Não pontua e não é poder (`RN-01-23`).
    """

    __tablename__ = "etiqueta_ods"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    objetivo: Mapped[int] = mapped_column(Integer, nullable=False)
    meta: Mapped[str | None] = mapped_column(String(32), nullable=True)
    trilha_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("trilha.id"), nullable=True
    )
    missao_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("missao.id"), nullable=True
    )

    __table_args__ = (
        CheckConstraint(
            f"objetivo >= {OBJETIVO_ODS_MINIMO} AND objetivo <= {OBJETIVO_ODS_MAXIMO}",
            name="ck_etiqueta_ods_objetivo_entre_1_e_18",
        ),
        CheckConstraint(
            "(trilha_id IS NOT NULL AND missao_id IS NULL) OR "
            "(trilha_id IS NULL AND missao_id IS NOT NULL)",
            name="ck_etiqueta_ods_trilha_ou_missao",
        ),
    )
