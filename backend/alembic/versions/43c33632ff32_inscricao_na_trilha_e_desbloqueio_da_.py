"""inscricao na trilha e desbloqueio da missao

Revision ID: 43c33632ff32
Revises: c3d4e5f6a7b8
Create Date: 2026-08-27 01:29:33.310439

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "43c33632ff32"
down_revision: str | Sequence[str] | None = "c3d4e5f6a7b8"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "inscricao_na_trilha",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("guerreiro_id", sa.Uuid(), nullable=False),
        sa.Column("trilha_id", sa.Uuid(), nullable=False),
        sa.Column(
            "momento", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.ForeignKeyConstraint(["guerreiro_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["trilha_id"], ["trilha.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "guerreiro_id", "trilha_id", name="uq_inscricao_na_trilha_guerreiro_id_trilha_id"
        ),
    )

    op.add_column(
        "missao",
        sa.Column(
            "tipo_do_desafio_de_desbloqueio",
            sa.Enum(
                "quiz", "pratico", name="tipodedesafiodedesbloqueio", native_enum=False, length=16
            ),
            nullable=True,
        ),
    )
    op.add_column("missao", sa.Column("desafio_de_desbloqueio_enunciado", sa.Text(), nullable=True))
    op.add_column(
        "missao", sa.Column("desafio_de_desbloqueio_alternativa_1", sa.Text(), nullable=True)
    )
    op.add_column(
        "missao", sa.Column("desafio_de_desbloqueio_alternativa_2", sa.Text(), nullable=True)
    )
    op.add_column(
        "missao", sa.Column("desafio_de_desbloqueio_alternativa_3", sa.Text(), nullable=True)
    )
    op.add_column(
        "missao", sa.Column("desafio_de_desbloqueio_alternativa_4", sa.Text(), nullable=True)
    )
    op.add_column(
        "missao",
        sa.Column("desafio_de_desbloqueio_alternativa_correta", sa.Integer(), nullable=True),
    )

    op.create_table(
        "desbloqueio_da_missao",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("guerreiro_id", sa.Uuid(), nullable=False),
        sa.Column("missao_id", sa.Uuid(), nullable=False),
        sa.Column(
            "momento", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column("aprovado", sa.Boolean(), nullable=True),
        sa.Column("julgado_por_id", sa.Uuid(), nullable=True),
        sa.ForeignKeyConstraint(["guerreiro_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["missao_id"], ["missao.id"]),
        sa.ForeignKeyConstraint(["julgado_por_id"], ["persona.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "guerreiro_id", "missao_id", name="uq_desbloqueio_da_missao_guerreiro_id_missao_id"
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("desbloqueio_da_missao")
    op.drop_column("missao", "desafio_de_desbloqueio_alternativa_correta")
    op.drop_column("missao", "desafio_de_desbloqueio_alternativa_4")
    op.drop_column("missao", "desafio_de_desbloqueio_alternativa_3")
    op.drop_column("missao", "desafio_de_desbloqueio_alternativa_2")
    op.drop_column("missao", "desafio_de_desbloqueio_alternativa_1")
    op.drop_column("missao", "desafio_de_desbloqueio_enunciado")
    op.drop_column("missao", "tipo_do_desafio_de_desbloqueio")
    op.drop_table("inscricao_na_trilha")
