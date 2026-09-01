"""anexação do artefato do apoiador

Revision ID: f4a5b6c7d8e9
Revises: e5f6a7b8c9d0
Create Date: 2026-09-01 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f4a5b6c7d8e9"
down_revision: str | Sequence[str] | None = "e5f6a7b8c9d0"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # Nulas, sem reescrever linha alguma: artefato do Mestre e artefato
    # declarado por Admin no cadastro seguem públicos com as colunas vazias
    # (`RF-14-19`, `RN-14-12`, design — decisão 5, Migration Plan).
    op.add_column("artefato_comprobatorio", sa.Column("anexado_por_id", sa.Uuid(), nullable=True))
    op.add_column(
        "artefato_comprobatorio",
        sa.Column("anexado_em", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_foreign_key(
        "fk_artefato_comprobatorio_anexado_por_id_persona",
        "artefato_comprobatorio",
        "persona",
        ["anexado_por_id"],
        ["id"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "fk_artefato_comprobatorio_anexado_por_id_persona",
        "artefato_comprobatorio",
        type_="foreignkey",
    )
    op.drop_column("artefato_comprobatorio", "anexado_em")
    op.drop_column("artefato_comprobatorio", "anexado_por_id")
