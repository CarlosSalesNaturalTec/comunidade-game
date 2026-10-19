"""ciencia da recompensa de marco

Revision ID: b2d7e5f1c893
Revises: a7c1d4e9b305
Create Date: 2026-10-19 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b2d7e5f1c893"
down_revision: str | Sequence[str] | None = "a7c1d4e9b305"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # A tabela da ciência da fatia 10 do PRD-05 (`RF-05-45`, `RN-05-50`).
    # Nasce vazia e nenhuma coluna existente muda: recompensa já conquistada
    # antes desta migração entra como **sem ciência**, o que apresenta a tela
    # uma vez a quem já tinha conquistado — o comportamento desejado, já que o
    # aviso nunca aconteceu (design — Migration Plan).
    op.create_table(
        "ciencia_da_recompensa",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("recompensa_de_marco_id", sa.Uuid(), nullable=False),
        sa.Column("guerreiro_id", sa.Uuid(), nullable=False),
        sa.Column("autor_id", sa.Uuid(), nullable=False),
        sa.Column("papel_do_autor", sa.String(length=32), nullable=False),
        sa.Column(
            "registrado_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["autor_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["guerreiro_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["recompensa_de_marco_id"], ["recompensa_de_marco.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "recompensa_de_marco_id", "guerreiro_id", name="uq_ciencia_da_recompensa_par"
        ),
    )
    op.create_index(
        "ix_ciencia_da_recompensa_guerreiro_id",
        "ciencia_da_recompensa",
        ["guerreiro_id"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("ix_ciencia_da_recompensa_guerreiro_id", table_name="ciencia_da_recompensa")
    op.drop_table("ciencia_da_recompensa")
