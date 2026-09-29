import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from ..banco import Base


class SecaoInstitucional(enum.StrEnum):
    """As três seções fixas do conteúdo institucional da vitrine, na ordem em
    que a leitura pública as devolve (`RF-03-45`, `RF-02-80`)."""

    quem_somos = "quem-somos"
    contatos = "contatos"
    como_apoiar = "como-apoiar"


class ConteudoInstitucional(Base):
    """Versão vigente de cada seção institucional — uma linha por seção, que
    nasce na primeira publicação ou semeadura (design — decisão 1). O histórico
    de quem publicou o quê vive na trilha de auditoria, não aqui.

    `autor_id` é nulo quando quem gravou foi a semeadura da implantação, que
    não tem persona. `video_url` só existe em "Quem somos" (`RF-03-49`).
    """

    __tablename__ = "conteudo_institucional"

    secao: Mapped[SecaoInstitucional] = mapped_column(
        Enum(SecaoInstitucional, native_enum=False, length=32), primary_key=True
    )
    texto: Mapped[str | None] = mapped_column(Text, nullable=True)
    video_url: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    autor_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("persona.id"), nullable=True
    )
    publicado_em: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
