"""remoção do template da missão

Decisão do fundador de 2026-11-16 (documento 09 §1, change
`remocao-do-template-da-missao`): o template sai da App 09, e com ele a tabela
`sugestao_de_estrutura` e a marca de técnico do catálogo de poderes, que só o
template lia. Os registros apagados não voltam: o `downgrade` recria as duas
estruturas vazias, com a coluna em falso (design — decisão 1).

Revision ID: b7d9f1a3c5e8
Revises: a3c5e7f9b1d2
Create Date: 2026-11-16 12:00:00

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "b7d9f1a3c5e8"
down_revision: str | Sequence[str] | None = "a3c5e7f9b1d2"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_index("ix_sugestao_de_estrutura_missao_id", table_name="sugestao_de_estrutura")
    op.drop_table("sugestao_de_estrutura")
    op.drop_column("poder", "tecnico")


def downgrade() -> None:
    """Downgrade schema."""
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
