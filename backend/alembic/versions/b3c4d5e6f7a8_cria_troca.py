"""cria troca

Revision ID: b3c4d5e6f7a8
Revises: a2b3c4d5e6f7
Create Date: 2026-08-19 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b3c4d5e6f7a8"
down_revision: str | Sequence[str] | None = "a2b3c4d5e6f7"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # A entrega de um item do catálogo avulso por pontos extras — o único
    # débito de ponto extra do Ciclo 01 (`RF-07-35`, `RF-07-36`). O encontro
    # é a `Aula` do PRD-01, sem verificação de estado nem presença
    # (documento 02 §8.2). `preco_cobrado` congela a vigência corrente do
    # preço de referência na data da troca (`RF-07-46`, `RN-07-29`).
    # `ComAutoria` grava o Mestre que entregou, o papel e a data e hora com
    # fuso.
    op.create_table(
        "troca",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("item_de_catalogo_avulso_id", sa.Uuid(), nullable=False),
        sa.Column("guerreiro_id", sa.Uuid(), nullable=False),
        sa.Column("preco_cobrado", sa.Integer(), nullable=False),
        sa.Column("aula_id", sa.Uuid(), nullable=False),
        sa.Column("autor_id", sa.Uuid(), nullable=False),
        sa.Column("papel_do_autor", sa.String(length=32), nullable=False),
        sa.Column(
            "registrado_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["aula_id"], ["aula.id"]),
        sa.ForeignKeyConstraint(["autor_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["item_de_catalogo_avulso_id"], ["item_de_catalogo_avulso.id"]),
        sa.ForeignKeyConstraint(["guerreiro_id"], ["persona.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_troca_guerreiro_id", "troca", ["guerreiro_id"])
    op.create_index("ix_troca_aula_id", "troca", ["aula_id"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("ix_troca_aula_id", table_name="troca")
    op.drop_index("ix_troca_guerreiro_id", table_name="troca")
    op.drop_table("troca")
