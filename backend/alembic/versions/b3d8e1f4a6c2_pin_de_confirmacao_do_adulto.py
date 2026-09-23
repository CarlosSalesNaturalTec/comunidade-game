"""PIN de confirmação do adulto

Revision ID: b3d8e1f4a6c2
Revises: c9f2a41b83de
Create Date: 2026-09-23 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b3d8e1f4a6c2"
down_revision: str | Sequence[str] | None = "c9f2a41b83de"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # Nulo: ninguém tem PIN antes de cadastrá-lo na App 09 ou na App 03
    # (`RF-01-75`, design — Migration Plan).
    op.add_column("persona", sa.Column("pin_verificador", sa.JSON(), nullable=True))
    op.add_column(
        "sessao",
        sa.Column("erros_de_pin_seguidos", sa.Integer(), server_default="0", nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("sessao", "erros_de_pin_seguidos")
    op.drop_column("persona", "pin_verificador")
