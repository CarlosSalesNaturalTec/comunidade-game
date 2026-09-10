"""recompensa de marco e entrega de recompensa

Revision ID: d1e2f3a4b5c6
Revises: c9d0e1f2a3b4
Create Date: 2026-09-10 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d1e2f3a4b5c6"
down_revision: str | Sequence[str] | None = "c9d0e1f2a3b4"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # As duas tabelas da fatia 13 do PRD-09 (`RF-09-71`, `RF-09-72`,
    # `RF-09-76`, `RN-09-27`, `RF-07-13`), que subiram como modelo e sem
    # migração. Nascem vazias: não há dado a transportar. `recompensa_de_marco`
    # vem primeiro, porque `entrega_de_recompensa` a referencia.
    op.create_table(
        "recompensa_de_marco",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("trilha_id", sa.Uuid(), nullable=False),
        sa.Column("missao_id", sa.Uuid(), nullable=False),
        sa.Column("tipo_de_recurso_id", sa.Uuid(), nullable=False),
        sa.Column("quantidade", sa.Numeric(precision=12, scale=2), nullable=False),
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
        sa.ForeignKeyConstraint(["tipo_de_recurso_id"], ["tipo_de_recurso.id"]),
        sa.ForeignKeyConstraint(["trilha_id"], ["trilha.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_recompensa_de_marco_trilha_id", "recompensa_de_marco", ["trilha_id"], unique=False
    )

    op.create_table(
        "entrega_de_recompensa",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("recompensa_de_marco_id", sa.Uuid(), nullable=False),
        sa.Column("guerreiro_id", sa.Uuid(), nullable=False),
        sa.Column("ponto_de_apoio_id", sa.Uuid(), nullable=False),
        sa.Column("lancamento_id", sa.Uuid(), nullable=False),
        sa.Column("autor_id", sa.Uuid(), nullable=False),
        sa.Column("papel_do_autor", sa.String(length=32), nullable=False),
        sa.Column(
            "registrado_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["autor_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["guerreiro_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["lancamento_id"], ["lancamento.id"]),
        sa.ForeignKeyConstraint(["ponto_de_apoio_id"], ["ponto_de_apoio.id"]),
        sa.ForeignKeyConstraint(["recompensa_de_marco_id"], ["recompensa_de_marco.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_entrega_de_recompensa_guerreiro_id",
        "entrega_de_recompensa",
        ["guerreiro_id"],
        unique=False,
    )
    op.create_index(
        "ix_entrega_de_recompensa_recompensa_de_marco_id",
        "entrega_de_recompensa",
        ["recompensa_de_marco_id"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("ix_entrega_de_recompensa_recompensa_de_marco_id", "entrega_de_recompensa")
    op.drop_index("ix_entrega_de_recompensa_guerreiro_id", "entrega_de_recompensa")
    op.drop_table("entrega_de_recompensa")
    op.drop_index("ix_recompensa_de_marco_trilha_id", "recompensa_de_marco")
    op.drop_table("recompensa_de_marco")
