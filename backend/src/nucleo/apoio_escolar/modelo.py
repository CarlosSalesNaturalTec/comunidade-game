import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from ..autoria import ComAutoria
from ..banco import Base


class Disciplina(Base, ComAutoria):
    """Catálogo aberto do apoio escolar (documento 03 §7): qualquer Mestre
    cadastra, sem posse — é taxonomia compartilhada, não conteúdo pessoal
    (`RF-01-35`, design — decisões). `nome_normalizado` evita duplicar
    "Matemática" e "matemática" como disciplinas diferentes, no mesmo
    padrão de `trilhas.regra._normalizar_natureza`.
    """

    __tablename__ = "disciplina"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    nome: Mapped[str] = mapped_column(String(128), nullable=False)
    nome_normalizado: Mapped[str] = mapped_column(String(128), nullable=False)

    __table_args__ = (UniqueConstraint("nome_normalizado", name="uq_disciplina_nome_normalizado"),)


class Conteudo(Base, ComAutoria):
    """Conteúdo do corpus fechado, autoral como trilha e missão: só o
    Mestre autor altera o próprio (`conferir_posse_do_conteudo`). Nasce
    publicado — o Mestre não passa por rascunho, ao contrário da trilha
    (design — decisões) — e o Admin o tira de circulação preenchendo os
    três campos de despublicação, sem precisar da posse.
    """

    __tablename__ = "conteudo"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    disciplina_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("disciplina.id"), nullable=False
    )
    material: Mapped[str] = mapped_column(Text, nullable=False)
    despublicado_em: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    despublicado_por_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("persona.id"), nullable=True
    )
    motivo_da_despublicacao: Mapped[str | None] = mapped_column(String(512), nullable=True)
