"""aula_id no lancamento

Revision ID: e017b352da40
Revises: d1b43eaede35
Create Date: 2026-08-18 18:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e017b352da40"
down_revision: str | Sequence[str] | None = "d1b43eaede35"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # Anulável: crédito e ajuste não declaram aula, e a baixa é somente
    # inserção — não há como preencher débito já gravado sem ferir a
    # imutabilidade (`RF-07-16`, `RN-07-15`, design — Decisions 3, 4).
    op.add_column("lancamento", sa.Column("aula_id", sa.Uuid(), nullable=True))
    op.create_foreign_key("fk_lancamento_aula_id_aula", "lancamento", "aula", ["aula_id"], ["id"])
    op.create_index("ix_lancamento_aula_id", "lancamento", ["aula_id"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("ix_lancamento_aula_id", table_name="lancamento")
    op.drop_constraint("fk_lancamento_aula_id_aula", "lancamento", type_="foreignkey")
    op.drop_column("lancamento", "aula_id")
