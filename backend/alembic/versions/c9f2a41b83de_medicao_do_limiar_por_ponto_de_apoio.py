"""medição do limiar por ponto de apoio

Revision ID: c9f2a41b83de
Revises: a7c31d5e90b2
Create Date: 2026-09-18 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c9f2a41b83de"
down_revision: str | Sequence[str] | None = "a7c31d5e90b2"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # A medição é a unidade gravada, e o limiar vigente de um ponto de apoio é
    # o da medição mais recente dele — sem um segundo registro "vigente" para
    # sair de sincronia com o histórico (`RF-01-73`, `RF-04-66`, `RN-04-35`,
    # design — decisão 4). Guarda distâncias, nunca descritor.
    op.create_table(
        "medicao_do_limiar",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("ponto_de_apoio_id", sa.Uuid(), nullable=False),
        sa.Column("limiar", sa.Float(), nullable=False),
        sa.Column("distancias_do_piso", postgresql.ARRAY(sa.Float()), nullable=False),
        sa.Column("distancias_do_teto", postgresql.ARRAY(sa.Float()), nullable=False),
        sa.Column("pessoas_no_teto", sa.Integer(), nullable=False),
        sa.Column("autor_id", sa.Uuid(), nullable=False),
        sa.Column("papel_do_autor", sa.String(length=32), nullable=False),
        sa.Column(
            "registrado_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["autor_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["ponto_de_apoio_id"], ["ponto_de_apoio.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    # A leitura quente é "a mais recente daquele ponto de apoio", em toda
    # comparação de entrada por nick e imagem (`RF-01-73`).
    op.create_index(
        "ix_medicao_do_limiar_ponto_de_apoio_id",
        "medicao_do_limiar",
        ["ponto_de_apoio_id"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("ix_medicao_do_limiar_ponto_de_apoio_id", table_name="medicao_do_limiar")
    op.drop_table("medicao_do_limiar")
