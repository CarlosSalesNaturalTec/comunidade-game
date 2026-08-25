"""aula_id na atividade

Revision ID: 9c48158e1fdd
Revises: b7f72144a102
Create Date: 2026-08-25 17:19:36.545572

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9c48158e1fdd"
down_revision: str | Sequence[str] | None = "b7f72144a102"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # Anulável: atividade on-line ou assíncrona nunca declara aula, e
    # nenhum registro existente é preenchido — atividade anterior à fatia
    # fica sem encontro (`RF-09-69`, `RF-09-73`, design — Migration Plan).
    op.add_column("atividade", sa.Column("aula_id", sa.Uuid(), nullable=True))
    op.create_foreign_key("fk_atividade_aula_id_aula", "atividade", "aula", ["aula_id"], ["id"])
    op.create_index("ix_atividade_aula_id", "atividade", ["aula_id"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("ix_atividade_aula_id", table_name="atividade")
    op.drop_constraint("fk_atividade_aula_id_aula", "atividade", type_="foreignkey")
    op.drop_column("atividade", "aula_id")
