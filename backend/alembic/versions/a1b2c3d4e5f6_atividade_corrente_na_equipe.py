"""atividade_corrente na equipe

Revision ID: a1b2c3d4e5f6
Revises: 9c48158e1fdd
Create Date: 2026-08-25 19:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a1b2c3d4e5f6"
down_revision: str | Sequence[str] | None = "9c48158e1fdd"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # Anulável: a equipe da trilha nunca a recebe, e a equipe da aula nasce
    # sem escolha declarada (`RF-02-42`, `RF-04-35`, design — Decisions).
    op.add_column("equipe", sa.Column("atividade_corrente_id", sa.Uuid(), nullable=True))
    op.create_foreign_key(
        "fk_equipe_atividade_corrente_id_atividade",
        "equipe",
        "atividade",
        ["atividade_corrente_id"],
        ["id"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("fk_equipe_atividade_corrente_id_atividade", "equipe", type_="foreignkey")
    op.drop_column("equipe", "atividade_corrente_id")
