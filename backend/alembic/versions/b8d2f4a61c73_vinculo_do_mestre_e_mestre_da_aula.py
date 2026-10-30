"""vinculo do mestre e mestre da aula

Revision ID: b8d2f4a61c73
Revises: a7c3d9e1f250
Create Date: 2026-10-30 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b8d2f4a61c73"
down_revision: str | Sequence[str] | None = "a7c3d9e1f250"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # As duas tabelas nascem **vazias**: o Mestre nunca teve vínculo de
    # comunidade, então não há dado a transportar, e as aulas da fase de
    # testes foram canceladas (decisão do fundador de 2026-10-30). Quem
    # povoa é o primeiro agendamento com Mestre escalado.
    op.create_table(
        "vinculo_do_mestre",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("mestre_id", sa.Uuid(), nullable=False),
        sa.Column("comunidade_virtual_id", sa.Uuid(), nullable=False),
        sa.Column(
            "data_inicio",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["comunidade_virtual_id"], ["comunidade_virtual.id"]),
        sa.ForeignKeyConstraint(["mestre_id"], ["persona.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    # Sem `data_fim`, o par é único e basta: o vínculo do Mestre não tem
    # vigência a conferir, porque nunca encerra no Ciclo 01.
    op.create_index(
        "uq_vinculo_do_mestre",
        "vinculo_do_mestre",
        ["mestre_id", "comunidade_virtual_id"],
        unique=True,
    )

    op.create_table(
        "mestre_da_aula",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("aula_id", sa.Uuid(), nullable=False),
        sa.Column("mestre_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(["aula_id"], ["aula.id"]),
        sa.ForeignKeyConstraint(["mestre_id"], ["persona.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("uq_mestre_da_aula", "mestre_da_aula", ["aula_id", "mestre_id"], unique=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("uq_mestre_da_aula", table_name="mestre_da_aula")
    op.drop_table("mestre_da_aula")
    op.drop_index("uq_vinculo_do_mestre", table_name="vinculo_do_mestre")
    op.drop_table("vinculo_do_mestre")
