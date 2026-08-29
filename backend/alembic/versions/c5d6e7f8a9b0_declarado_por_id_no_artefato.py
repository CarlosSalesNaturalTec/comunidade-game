"""declarado_por_id no artefato

Revision ID: c5d6e7f8a9b0
Revises: b4c5d6e7f8a9
Create Date: 2026-08-29 19:30:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c5d6e7f8a9b0"
down_revision: str | Sequence[str] | None = "b4c5d6e7f8a9"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # Anulável: a linha antiga nasceu sem autor e nulo vale como "do
    # cadastro" (`RN-09-14`, decisão do fundador, 2026-08-29, documento 09
    # §1, design — decisão 2). Sem backfill.
    op.add_column("artefato_comprobatorio", sa.Column("declarado_por_id", sa.Uuid(), nullable=True))
    op.create_foreign_key(
        "fk_artefato_comprobatorio_declarado_por_id_persona",
        "artefato_comprobatorio",
        "persona",
        ["declarado_por_id"],
        ["id"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "fk_artefato_comprobatorio_declarado_por_id_persona",
        "artefato_comprobatorio",
        type_="foreignkey",
    )
    op.drop_column("artefato_comprobatorio", "declarado_por_id")
