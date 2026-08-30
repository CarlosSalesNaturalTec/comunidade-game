import enum
import uuid

from sqlalchemy import CheckConstraint, Enum, ForeignKey, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from ..autoria import ComAutoria
from ..banco import Base


class FormaDeEntregaDaProducao(enum.StrEnum):
    texto = "texto"
    audio = "audio"
    foto = "foto"


class ProducaoDaMissao(Base, ComAutoria):
    """O que a equipe entrega depois de trabalhar a atividade do encontro —
    texto, fala ou foto do manuscrito — e a devolutiva construtiva que a
    plataforma lê de volta (`RF-04-45` a `RF-04-47`, PRD-05 §8). Nasce só
    pela equipe do App 01 nesta fatia; `guerreiro_id` fica reservado à porta
    individual da fatia 7 do PRD-05, sem migração nova (design — decisão 2).

    Sem coluna de foto, de áudio nem de custo: as duas mídias são
    descartadas na leitura (`RF-04-46`, documento 03 §12.2) e o consumo do
    modelo nunca é medido por ato (`RF-09-90`). `ComAutoria` grava quem
    entregou de fato — o integrante em sessão —, separado de `equipe_id`,
    a quem a produção pertence.
    """

    __tablename__ = "producao_da_missao"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    equipe_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("equipe.id"), nullable=True
    )
    guerreiro_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("persona.id"), nullable=True
    )
    missao_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("missao.id"), nullable=False)
    atividade_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("atividade.id"), nullable=False
    )
    forma: Mapped[FormaDeEntregaDaProducao] = mapped_column(
        Enum(FormaDeEntregaDaProducao, native_enum=False, length=16), nullable=False
    )
    transcricao: Mapped[str] = mapped_column(Text, nullable=False)
    devolutiva: Mapped[str | None] = mapped_column(Text, nullable=True)

    __table_args__ = (
        CheckConstraint(
            "(equipe_id IS NOT NULL AND guerreiro_id IS NULL) OR "
            "(equipe_id IS NULL AND guerreiro_id IS NOT NULL)",
            name="ck_producao_da_missao_equipe_ou_guerreiro",
        ),
    )
