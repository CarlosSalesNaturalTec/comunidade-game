import enum
import uuid
from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKey,
    ForeignKeyConstraint,
    String,
    UniqueConstraint,
    Uuid,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from ..banco import Base


class NivelDoLocal(enum.StrEnum):
    """Seis níveis, nessa ordem de contenção — cada um dentro do anterior
    (`RF-08-04`, PRD-08 §8)."""

    comunidade = "comunidade"
    bairro = "bairro"
    rua = "rua"
    condominio = "condominio"
    bloco = "bloco"
    quadra = "quadra"


# A ordem de contenção — "o pai é do nível imediatamente acima" (`RF-08-04`)
# é lido daqui por `locais/regra.py`.
ORDEM_DOS_NIVEIS: tuple[NivelDoLocal, ...] = (
    NivelDoLocal.comunidade,
    NivelDoLocal.bairro,
    NivelDoLocal.rua,
    NivelDoLocal.condominio,
    NivelDoLocal.bloco,
    NivelDoLocal.quadra,
)


class Local(Base):
    """Um nó da hierarquia territorial da comunidade, cadastrado por Admin
    nesta entrega — a única origem de local aqui (`RF-08-04`, `RN-08-18`).

    `UNIQUE (id, comunidade_id)` existe só para sustentar a chave
    estrangeira composta do pai: com ela, o próprio banco recusa um pai de
    outra comunidade, sem que nenhuma regra precise conferir (design —
    Decisions). O nível do pai — imediatamente acima — não cabe em chave
    estrangeira e é validado em `locais/regra.py`.
    """

    __tablename__ = "local"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    comunidade_virtual_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("comunidade_virtual.id"), nullable=False
    )
    nivel: Mapped[NivelDoLocal] = mapped_column(
        Enum(NivelDoLocal, native_enum=False, length=16), nullable=False
    )
    rotulo: Mapped[str] = mapped_column(String(128), nullable=False)
    local_pai_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, nullable=True)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        UniqueConstraint("id", "comunidade_virtual_id", name="uq_local_id_comunidade_virtual_id"),
        ForeignKeyConstraint(
            ["local_pai_id", "comunidade_virtual_id"],
            ["local.id", "local.comunidade_virtual_id"],
            name="fk_local_local_pai_id_comunidade_virtual_id",
        ),
        CheckConstraint(
            "(nivel = 'comunidade') = (local_pai_id IS NULL)",
            name="ck_local_pai_so_vazio_no_nivel_comunidade",
        ),
    )
