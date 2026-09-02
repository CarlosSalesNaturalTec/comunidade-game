"""cria favorito

Revision ID: 6ef2d53a10d7
Revises: b1fabae4dbda
Create Date: 2026-09-02 02:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "6ef2d53a10d7"
down_revision: str | Sequence[str] | None = "b1fabae4dbda"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # A preferência de leitura do Apoiador sobre um Guerreiro(a) ou um
    # Mestre — nunca canal, nunca lastro (PRD-14 §8, design — decisão 3).
    op.create_table(
        "favorito",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("apoiador_id", sa.Uuid(), nullable=False),
        sa.Column("guerreiro_id", sa.Uuid(), nullable=True),
        sa.Column("mestre_id", sa.Uuid(), nullable=True),
        sa.Column(
            "incluido_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "(guerreiro_id IS NOT NULL AND mestre_id IS NULL) OR "
            "(guerreiro_id IS NULL AND mestre_id IS NOT NULL)",
            name="ck_favorito_guerreiro_ou_mestre",
        ),
        sa.ForeignKeyConstraint(["apoiador_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["guerreiro_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["mestre_id"], ["persona.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "uq_favorito_apoiador_id_guerreiro_id",
        "favorito",
        ["apoiador_id", "guerreiro_id"],
        unique=True,
        postgresql_where=sa.text("guerreiro_id IS NOT NULL"),
    )
    op.create_index(
        "uq_favorito_apoiador_id_mestre_id",
        "favorito",
        ["apoiador_id", "mestre_id"],
        unique=True,
        postgresql_where=sa.text("mestre_id IS NOT NULL"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("uq_favorito_apoiador_id_mestre_id", table_name="favorito")
    op.drop_index("uq_favorito_apoiador_id_guerreiro_id", table_name="favorito")
    op.drop_table("favorito")
