"""encerramento do desafio extra

Revision ID: c06ef985f8cd
Revises: 1f47b0e735c9
Create Date: 2026-09-02 12:05:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c06ef985f8cd"
down_revision: str | Sequence[str] | None = "1f47b0e735c9"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # O encerramento é fato gravado no desafio, não um quinto valor do
    # enum de situação (`RF-02-106`, `RF-07-40`, design — Decisions 1).
    op.add_column("desafio_extra", sa.Column("admin_encerrador_id", sa.Uuid(), nullable=True))
    op.add_column(
        "desafio_extra",
        sa.Column("encerrado_em", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_foreign_key(
        "fk_desafio_extra_admin_encerrador_id_persona",
        "desafio_extra",
        "persona",
        ["admin_encerrador_id"],
        ["id"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "fk_desafio_extra_admin_encerrador_id_persona", "desafio_extra", type_="foreignkey"
    )
    op.drop_column("desafio_extra", "encerrado_em")
    op.drop_column("desafio_extra", "admin_encerrador_id")
