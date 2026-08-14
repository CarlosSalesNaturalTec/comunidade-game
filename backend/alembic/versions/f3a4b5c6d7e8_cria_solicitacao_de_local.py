"""cria solicitacao_de_local

Revision ID: f3a4b5c6d7e8
Revises: e1f2a3b4c5d6
Create Date: 2026-08-14 22:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f3a4b5c6d7e8"
down_revision: str | Sequence[str] | None = "e1f2a3b4c5d6"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "solicitacao_de_local",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("solicitante_id", sa.Uuid(), nullable=False),
        sa.Column("comunidade_virtual_id", sa.Uuid(), nullable=False),
        sa.Column("desafio_de_coleta_id", sa.Uuid(), nullable=False),
        sa.Column(
            "nivel_pretendido",
            sa.Enum(
                "comunidade",
                "bairro",
                "rua",
                "condominio",
                "bloco",
                "quadra",
                name="niveldolocal",
                native_enum=False,
                length=16,
            ),
            nullable=False,
        ),
        sa.Column("rotulo", sa.String(length=128), nullable=False),
        sa.Column("justificativa", sa.Text(), nullable=False),
        sa.Column(
            "situacao",
            sa.Enum(
                "recebida",
                "aprovada",
                "recusada",
                name="situacaodasolicitacaodelocal",
                native_enum=False,
                length=16,
            ),
            nullable=False,
        ),
        sa.Column("avaliador_id", sa.Uuid(), nullable=True),
        sa.Column("motivo_da_recusa", sa.Text(), nullable=True),
        sa.Column("local_criado_id", sa.Uuid(), nullable=True),
        sa.Column("avaliado_em", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "registrado_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["avaliador_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["comunidade_virtual_id"], ["comunidade_virtual.id"]),
        sa.ForeignKeyConstraint(["desafio_de_coleta_id"], ["desafio_de_coleta.id"]),
        sa.ForeignKeyConstraint(["local_criado_id"], ["local.id"]),
        sa.ForeignKeyConstraint(["solicitante_id"], ["persona.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("solicitacao_de_local")
