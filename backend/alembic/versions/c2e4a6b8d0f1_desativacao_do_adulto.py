"""desativação do adulto pela gestão

Decisão do fundador de 2026-11-17 (change `edicao-e-exclusao-de-mestre-e-apoiador`):
Mestre e Apoiador já usados não se excluem, se desativam. A marca nasce nula
para todas as personas existentes — sem retroação (design — decisão 6).

Revision ID: c2e4a6b8d0f1
Revises: b7d9f1a3c5e8
Create Date: 2026-11-17 12:00:00

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "c2e4a6b8d0f1"
down_revision: str | Sequence[str] | None = "b7d9f1a3c5e8"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("persona", sa.Column("desativada_em", sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("persona", "desativada_em")
