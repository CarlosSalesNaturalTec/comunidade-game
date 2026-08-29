"""cria solicitacao do responsavel

Revision ID: da7ae0cdb737
Revises: 31bdcf718fdb
Create Date: 2026-08-29 13:21:24.801047

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "da7ae0cdb737"
down_revision: str | Sequence[str] | None = "31bdcf718fdb"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "solicitacao_do_responsavel",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("responsavel_id", sa.Uuid(), nullable=False),
        sa.Column("guerreiro_id", sa.Uuid(), nullable=False),
        sa.Column(
            "tipo",
            sa.Enum(
                "acesso",
                "correcao",
                "exclusao",
                "esclarecimento",
                name="tipodesolicitacaodoresponsavel",
                native_enum=False,
                length=16,
            ),
            nullable=False,
        ),
        sa.Column("texto", sa.Text(), nullable=False),
        sa.Column(
            "situacao",
            sa.Enum(
                "recebida",
                "em_avaliacao",
                "aceita",
                "recusada",
                name="situacaodasolicitacao",
                native_enum=False,
                length=16,
            ),
            nullable=False,
            server_default="recebida",
        ),
        sa.Column(
            "registrado_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("prazo", sa.DateTime(timezone=True), nullable=False),
        sa.Column("tratado_por_id", sa.Uuid(), nullable=True),
        sa.Column("desfecho", sa.Text(), nullable=True),
        sa.Column("tratado_em", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["guerreiro_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["responsavel_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["tratado_por_id"], ["persona.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_solicitacao_do_responsavel_responsavel_id",
        "solicitacao_do_responsavel",
        ["responsavel_id"],
    )
    op.create_index(
        "ix_solicitacao_do_responsavel_guerreiro_id",
        "solicitacao_do_responsavel",
        ["guerreiro_id"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(
        "ix_solicitacao_do_responsavel_guerreiro_id", table_name="solicitacao_do_responsavel"
    )
    op.drop_index(
        "ix_solicitacao_do_responsavel_responsavel_id", table_name="solicitacao_do_responsavel"
    )
    op.drop_table("solicitacao_do_responsavel")
