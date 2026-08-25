"""cria pergunta na partida

Revision ID: b7f72144a102
Revises: 44f2c7d5709e
Create Date: 2026-08-25 11:30:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b7f72144a102"
down_revision: str | Sequence[str] | None = "44f2c7d5709e"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # Migração aditiva: nenhuma tabela existente é alterada (design —
    # Migration Plan). A tabela nasce vazia — nenhuma partida anterior
    # existe fora de teste.
    op.create_table(
        "pergunta_na_partida",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("partida_id", sa.Uuid(), nullable=False),
        sa.Column("pergunta_id", sa.Uuid(), nullable=False),
        sa.Column("ordem", sa.Integer(), nullable=False),
        sa.Column("liberada_em", sa.DateTime(timezone=True), nullable=True),
        sa.Column("autor_id", sa.Uuid(), nullable=False),
        sa.Column("papel_do_autor", sa.String(length=32), nullable=False),
        sa.Column(
            "registrado_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["autor_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["partida_id"], ["partida_de_quiz.id"]),
        sa.ForeignKeyConstraint(["pergunta_id"], ["pergunta_de_quiz.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "partida_id", "pergunta_id", name="uq_pergunta_na_partida_partida_id_pergunta_id"
        ),
        sa.UniqueConstraint("partida_id", "ordem", name="uq_pergunta_na_partida_partida_id_ordem"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("pergunta_na_partida")
