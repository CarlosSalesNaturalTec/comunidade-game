"""materiais da missão

Revision ID: b1c2d3e4f5a6
Revises: a9b8c7d6e5f4
Create Date: 2026-11-10 00:00:00

A missão declara os materiais da aula como lista de nomes (`RF-09-140`,
`RN-09-61`). As missões já gravadas ficam com a lista vazia, sem backfill.
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "b1c2d3e4f5a6"
down_revision: str | Sequence[str] | None = "a9b8c7d6e5f4"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "missao",
        sa.Column(
            "materiais",
            sa.ARRAY(sa.Text()),
            server_default=sa.text("'{}'"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_column("missao", "materiais")
