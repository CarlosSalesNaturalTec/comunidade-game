import enum
import uuid

from sqlalchemy import CheckConstraint, Enum, ForeignKey, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from ..autoria import ComAutoria
from ..banco import Base


class TipoDeAssistente(enum.StrEnum):
    trilhas = "trilhas"
    apoio_escolar = "apoio_escolar"


class DesfechoDaConsulta(enum.StrEnum):
    respondida = "respondida"
    fora_do_corpus = "fora_do_corpus"
    tarefa_escolar = "tarefa_escolar"


class ConsultaAoAssistente(Base, ComAutoria):
    """A conversa da equipe — ou, na porta individual da App 05, do
    Guerreiro(a) — com o assistente (PRD-04 §8). Nasce só pelo assistente de
    **trilhas**, pela equipe, nesta fatia; a porta individual do apoio
    escolar preenche `guerreiro_id` depois, sem migração nova (design —
    decisão 6). Guarda só as duas transcrições — o áudio da pergunta nunca
    chega aqui (`RF-04-40`, `RN-04-21`).
    """

    __tablename__ = "consulta_ao_assistente"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    equipe_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("equipe.id"), nullable=True
    )
    guerreiro_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("persona.id"), nullable=True
    )
    assistente: Mapped[TipoDeAssistente] = mapped_column(
        Enum(TipoDeAssistente, native_enum=False, length=16), nullable=False
    )
    desfecho: Mapped[DesfechoDaConsulta] = mapped_column(
        Enum(DesfechoDaConsulta, native_enum=False, length=16), nullable=False
    )
    pergunta: Mapped[str] = mapped_column(Text, nullable=False)
    resposta: Mapped[str] = mapped_column(Text, nullable=False)

    __table_args__ = (
        CheckConstraint(
            "(equipe_id IS NOT NULL AND guerreiro_id IS NULL) OR "
            "(equipe_id IS NULL AND guerreiro_id IS NOT NULL)",
            name="ck_consulta_ao_assistente_equipe_ou_guerreiro",
        ),
    )
