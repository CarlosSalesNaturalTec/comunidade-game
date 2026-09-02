"""parecer do mestre no desafio extra

Revision ID: d4e5f6a7b8c9
Revises: c06ef985f8cd
Create Date: 2026-09-02 15:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d4e5f6a7b8c9"
down_revision: str | Sequence[str] | None = "c06ef985f8cd"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # A recusa reaproveita `motivo_da_recusa`; só a validação guarda texto
    # próprio, que a recusa não tem (design — decisão 1).
    op.add_column("desafio_extra", sa.Column("parecer_do_mestre", sa.Text(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("desafio_extra", "parecer_do_mestre")
