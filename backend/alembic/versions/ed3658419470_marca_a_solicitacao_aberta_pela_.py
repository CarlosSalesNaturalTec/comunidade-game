"""marca a solicitacao aberta pela suspensao por divergencia

Revision ID: ed3658419470
Revises: f41e6a76385a
Create Date: 2026-08-31 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "ed3658419470"
down_revision: str | Sequence[str] | None = "f41e6a76385a"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "solicitacao_do_responsavel",
        sa.Column("aberta_pela_suspensao", sa.Boolean(), nullable=False, server_default=sa.false()),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("solicitacao_do_responsavel", "aberta_pela_suspensao")
