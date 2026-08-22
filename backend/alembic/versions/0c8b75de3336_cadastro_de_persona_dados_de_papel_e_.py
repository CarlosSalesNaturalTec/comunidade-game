"""cadastro de persona: dados de papel e artefato comprobatorio

Revision ID: 0c8b75de3336
Revises: e2f3a4b5c6d7
Create Date: 2026-08-21 22:39:48.653058

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0c8b75de3336"
down_revision: str | Sequence[str] | None = "e2f3a4b5c6d7"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # Aditiva: nenhuma persona existente muda de estado (design — Migration
    # Plan). Nulas porque a semeadura e as personas anteriores a esta fatia
    # não as carregam.
    op.add_column("persona", sa.Column("nome", sa.String(length=256), nullable=True))
    op.add_column("persona", sa.Column("nascimento", sa.Date(), nullable=True))
    op.add_column("persona", sa.Column("email", sa.String(length=256), nullable=True))
    op.add_column("persona", sa.Column("whatsapp", sa.String(length=32), nullable=True))

    op.create_table(
        "artefato_comprobatorio",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("persona_id", sa.Uuid(), nullable=False),
        sa.Column("endereco", sa.String(length=512), nullable=False),
        sa.Column("rotulo", sa.String(length=256), nullable=False),
        sa.Column(
            "criado_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["persona_id"], ["persona.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("artefato_comprobatorio")
    op.drop_column("persona", "whatsapp")
    op.drop_column("persona", "email")
    op.drop_column("persona", "nascimento")
    op.drop_column("persona", "nome")
