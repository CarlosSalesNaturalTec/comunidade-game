"""marca de ativo do tipo de recurso

Revision ID: 12b4e8984d37
Revises: beba078c9152
Create Date: 2026-11-13 00:00:00

O tipo de recurso ganha a marca de ativo; desativado, sai só da escolha nova
(`RF-07-52`). Nasce verdadeira, e todo tipo já cadastrado fica ativo — sem
retroação (design — decisão 7).
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "12b4e8984d37"
down_revision: str | Sequence[str] | None = "beba078c9152"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "tipo_de_recurso",
        sa.Column("ativo", sa.Boolean(), nullable=False, server_default=sa.true()),
    )


def downgrade() -> None:
    op.drop_column("tipo_de_recurso", "ativo")
