"""acrescenta persona.avatar

Revision ID: a1c2e3f4b5d6
Revises: d7a99bc76819
Create Date: 2026-08-13 22:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a1c2e3f4b5d6"
down_revision: str | Sequence[str] | None = "d7a99bc76819"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # Aceita nulo: personas existentes não têm avatar, e quem não tem
    # simplesmente não aparece em público, por já não ter autorização de
    # divulgação (design — Migration Plan). A rota que grava é do PRD-04.
    op.add_column("persona", sa.Column("avatar", sa.Text(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("persona", "avatar")
