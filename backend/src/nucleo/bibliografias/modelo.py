import uuid

from sqlalchemy import ForeignKey, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from ..autoria import ComAutoria
from ..banco import Base


class BibliografiaDaMissao(Base, ComAutoria):
    """O vínculo entre a missão e o acervo (documento 05 §3, PRD-09 §8).
    `item_patrimonial_id` é **anulável** — o vínculo com o exemplar tombado
    é opcional, decisão do fundador de 2026-08-25 (`RF-09-21`).
    Disponibilidade e crédito ao Apoiador **não são coluna**: derivam a
    cada leitura do exemplar tombado e do aporte de origem dele
    (`RF-09-22`, `RF-09-23`, design — decisão 3).
    """

    __tablename__ = "bibliografia_da_missao"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    missao_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("missao.id"), nullable=False)
    titulo: Mapped[str] = mapped_column(String(256), nullable=False)
    capitulo: Mapped[str] = mapped_column(Text, nullable=False)
    item_patrimonial_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("item_patrimonial.id"), nullable=True
    )
