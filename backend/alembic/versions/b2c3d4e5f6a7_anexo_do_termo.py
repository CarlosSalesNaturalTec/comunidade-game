"""anexo_do_termo

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f6
Create Date: 2026-08-25 19:05:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b2c3d4e5f6a7"
down_revision: str | Sequence[str] | None = "a1b2c3d4e5f6"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # Registro próprio, à parte do consentimento — que segue de somente
    # inserção —, único por consentimento (`RF-02-68`, `RN-01-12`).
    op.create_table(
        "anexo_do_termo",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("consentimento_id", sa.Uuid(), nullable=False),
        sa.Column("digitalizacao_referencia", sa.String(length=512), nullable=False),
        sa.Column("digitalizacao_nome_original", sa.String(length=256), nullable=True),
        sa.Column("digitalizacao_tipo", sa.String(length=128), nullable=False),
        sa.Column("digitalizacao_tamanho", sa.Integer(), nullable=False),
        sa.Column("autor_id", sa.Uuid(), nullable=False),
        sa.Column("papel_do_autor", sa.String(length=32), nullable=False),
        sa.Column(
            "registrado_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["autor_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["consentimento_id"], ["consentimento.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("consentimento_id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("anexo_do_termo")
