import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, UniqueConstraint, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column

from ..autoria import ComAutoria
from ..banco import Base


class Equipe(Base, ComAutoria):
    """Grupo livre de até cinco pessoas formado pelos Guerreiros e
    Guerreiras, em dois tempos de vida — o vínculo declara qual: a equipe
    da aula, que encerra com ela, ou a da trilha, fixa depois de homologada
    pelo Mestre (`RF-01-37`, `RF-01-63`, documento 02 §5). `ComAutoria`
    grava quem criou. `homologado_por_id` e `homologado_em`, anuláveis, no
    padrão de `CriacaoOriginal.validado_por_id`/`validado_em`: a fixidez é
    derivada de `homologado_em` não ser nulo, nunca de uma enumeração de
    situação (design — decisões).
    """

    __tablename__ = "equipe"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    aula_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, ForeignKey("aula.id"), nullable=True)
    trilha_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("trilha.id"), nullable=True
    )
    homologado_por_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("persona.id"), nullable=True
    )
    homologado_em: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        CheckConstraint(
            "(aula_id IS NOT NULL AND trilha_id IS NULL) OR "
            "(aula_id IS NULL AND trilha_id IS NOT NULL)",
            name="ck_equipe_aula_ou_trilha",
        ),
    )


class IntegranteDaEquipe(Base):
    """Vínculo entre a equipe e cada persona que a integra, com o papel que
    ela teve — texto livre e opcional, sem efeito sobre pontuação nem
    composição (`RF-01-64`, documento 02 §§4, 5).
    """

    __tablename__ = "integrante_da_equipe"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    equipe_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("equipe.id"), nullable=False)
    persona_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("persona.id"), nullable=False)
    papel: Mapped[str | None] = mapped_column(String(64), nullable=True)
    entrou_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        UniqueConstraint(
            "equipe_id", "persona_id", name="uq_integrante_da_equipe_equipe_id_persona_id"
        ),
    )
