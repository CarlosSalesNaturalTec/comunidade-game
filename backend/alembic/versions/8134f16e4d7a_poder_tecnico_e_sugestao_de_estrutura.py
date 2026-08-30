"""poder tecnico e sugestao de estrutura

Revision ID: 8134f16e4d7a
Revises: c5d6e7f8a9b0
Create Date: 2026-08-29 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "8134f16e4d7a"
down_revision: str | Sequence[str] | None = "c5d6e7f8a9b0"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # Aditiva: `tecnico` nasce falso para todo poder existente, e nenhuma
    # trilha muda de comportamento até um Admin marcar o poder pela gestão
    # (`RF-01-62`, `RN-01-54`, design — Migration Plan).
    op.add_column(
        "poder", sa.Column("tecnico", sa.Boolean(), nullable=False, server_default=sa.false())
    )

    op.create_table(
        "sugestao_de_estrutura",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("missao_id", sa.Uuid(), nullable=False),
        sa.Column("topico", sa.Text(), nullable=False),
        sa.Column("estrutura_proposta", sa.JSON(), nullable=False),
        sa.Column("lacunas", sa.JSON(), nullable=False),
        sa.Column(
            "situacao",
            sa.Enum(
                "proposta",
                "aceita",
                "recusada",
                "alterada",
                name="situacaodasugestaodeestrutura",
                native_enum=False,
                length=16,
            ),
            nullable=False,
            server_default="proposta",
        ),
        sa.Column("autor_id", sa.Uuid(), nullable=False),
        sa.Column("papel_do_autor", sa.String(length=32), nullable=False),
        sa.Column(
            "registrado_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["autor_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["missao_id"], ["missao.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_sugestao_de_estrutura_missao_id", "sugestao_de_estrutura", ["missao_id"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("ix_sugestao_de_estrutura_missao_id", table_name="sugestao_de_estrutura")
    op.drop_table("sugestao_de_estrutura")
    op.drop_column("poder", "tecnico")
