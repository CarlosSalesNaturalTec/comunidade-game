import uuid

from sqlalchemy import Boolean, ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from ..autoria import ComAutoria
from ..banco import Base


class PontoDeApoio(Base, ComAutoria):
    """O espaço físico onde o recurso fica guardado e onde a aula acontece,
    cadastrado por Admin e pertencente a uma comunidade (`RF-07-47`,
    `RN-07-33`). Nasce sem responsável — quem responde pelo acervo é
    designado depois, em operação própria (`RF-07-49`).

    `ativo` nasce verdadeiro e hoje NENHUMA operação o muda: a desativação
    é pendência de produto, aberta no documento 09 — o campo existe para
    não fechar a porta ao esquema, mas nenhuma regra o lê ainda
    (design — Decisions, Risks).
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
