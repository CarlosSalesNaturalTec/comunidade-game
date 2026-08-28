"""poder na atividade avulsa

Revision ID: 31bdcf718fdb
Revises: 628a65a05ddc
Create Date: 2026-08-28 02:42:24.886739

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "31bdcf718fdb"
down_revision: str | Sequence[str] | None = "628a65a05ddc"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # `missao_id` passa a admitir nulo — a atividade avulsa não pertence a
    # nenhuma (design — decisões 1, 2). Nenhuma `Atividade` existente perde
    # a missão, então nenhum dado precisa migrar.
    op.alter_column("atividade", "missao_id", existing_type=sa.Uuid(), nullable=True)
    op.add_column("atividade", sa.Column("poder_id", sa.Uuid(), nullable=True))
    op.create_foreign_key("fk_atividade_poder_id_poder", "atividade", "poder", ["poder_id"], ["id"])
    op.create_check_constraint(
        "ck_atividade_missao_id_ou_poder_id",
        "atividade",
        "(missao_id IS NULL) != (poder_id IS NULL)",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("ck_atividade_missao_id_ou_poder_id", "atividade", type_="check")
    op.drop_constraint("fk_atividade_poder_id_poder", "atividade", type_="foreignkey")
    op.drop_column("atividade", "poder_id")
    op.alter_column("atividade", "missao_id", existing_type=sa.Uuid(), nullable=False)
