"""cria producao da missao

Revision ID: a7c9a9c847e8
Revises: 8134f16e4d7a
Create Date: 2026-08-30 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a7c9a9c847e8"
down_revision: str | Sequence[str] | None = "8134f16e4d7a"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "producao_da_missao",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("equipe_id", sa.Uuid(), nullable=True),
        sa.Column("guerreiro_id", sa.Uuid(), nullable=True),
        sa.Column("missao_id", sa.Uuid(), nullable=False),
        sa.Column("atividade_id", sa.Uuid(), nullable=False),
        sa.Column(
            "forma",
            sa.Enum(
                "texto",
                "audio",
                "foto",
                name="formadeentregadaproducao",
                native_enum=False,
                length=16,
            ),
            nullable=False,
        ),
        sa.Column("transcricao", sa.Text(), nullable=False),
        sa.Column("devolutiva", sa.Text(), nullable=True),
        sa.Column("autor_id", sa.Uuid(), nullable=False),
        sa.Column("papel_do_autor", sa.String(length=32), nullable=False),
        sa.Column(
            "registrado_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["atividade_id"], ["atividade.id"]),
        sa.ForeignKeyConstraint(["autor_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["equipe_id"], ["equipe.id"]),
        sa.ForeignKeyConstraint(["guerreiro_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["missao_id"], ["missao.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.CheckConstraint(
            "(equipe_id IS NOT NULL AND guerreiro_id IS NULL) OR "
            "(equipe_id IS NULL AND guerreiro_id IS NOT NULL)",
            name="ck_producao_da_missao_equipe_ou_guerreiro",
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("producao_da_missao")
