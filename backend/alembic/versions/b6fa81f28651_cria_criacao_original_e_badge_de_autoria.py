"""cria criacao_original e badge de_autoria

Revision ID: b6fa81f28651
Revises: 215dc282710b
Create Date: 2026-08-12 17:36:39.916038

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b6fa81f28651"
down_revision: str | Sequence[str] | None = "215dc282710b"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # `TipoDeBadge.de_autoria` não exige DDL: a coluna `badge.tipo` é
    # `native_enum=False` — VARCHAR(32) sem CHECK constraint —, então o
    # novo valor já cabe sem tocar a tabela das fatias anteriores.
    op.create_table(
        "criacao_original",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("trilha_id", sa.Uuid(), nullable=False),
        sa.Column("producao", sa.Text(), nullable=False),
        sa.Column(
            "situacao",
            sa.Enum(
                "entregue",
                "validada",
                "devolvida",
                name="situacaodacriacaooriginal",
                native_enum=False,
                length=16,
            ),
            nullable=False,
        ),
        sa.Column("validado_por_id", sa.Uuid(), nullable=True),
        sa.Column("validado_em", sa.DateTime(timezone=True), nullable=True),
        sa.Column("autor_id", sa.Uuid(), nullable=False),
        sa.Column("papel_do_autor", sa.String(length=32), nullable=False),
        sa.Column(
            "registrado_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["autor_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["trilha_id"], ["trilha.id"]),
        sa.ForeignKeyConstraint(["validado_por_id"], ["persona.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("autor_id", "trilha_id", name="uq_criacao_original_autor_id_trilha_id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("criacao_original")
