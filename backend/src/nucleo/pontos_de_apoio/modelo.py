import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from ..autoria import ComAutoria
from ..banco import Base


class PontoDeApoio(Base, ComAutoria):
    """O espaço físico onde o recurso fica guardado e onde a aula acontece,
    cadastrado por Admin e pertencente a uma comunidade (`RF-07-47`,
    `RN-07-33`). Nasce sem responsável — quem responde pelo acervo é
    designado depois, em operação própria (`RF-07-49`).

    `ativo` nasce verdadeiro; o Admin desativa e reativa, bloqueado por
    aula futura e por saldo remanescente (`RF-07-47`, `RN-07-01`,
    `RN-07-33`). `motivo_da_situacao`, `autor_da_situacao_id`,
    `papel_do_autor_da_situacao` e `situacao_alterada_em` guardam a
    autoria da última mudança de estado, separada da autoria do cadastro
    já gravada por `ComAutoria` (design — Migration Plan).
    """

    __tablename__ = "ponto_de_apoio"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    nome: Mapped[str] = mapped_column(String(128), nullable=False)
    comunidade_virtual_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("comunidade_virtual.id"), nullable=False
    )
    responsavel_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("persona.id"), nullable=True
    )
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    motivo_da_situacao: Mapped[str | None] = mapped_column(Text, nullable=True)
    autor_da_situacao_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("persona.id"), nullable=True
    )
    papel_do_autor_da_situacao: Mapped[str | None] = mapped_column(String(32), nullable=True)
    situacao_alterada_em: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
