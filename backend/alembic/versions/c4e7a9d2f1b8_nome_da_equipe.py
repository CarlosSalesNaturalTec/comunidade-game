"""nome da equipe

Revision ID: c4e7a9d2f1b8
Revises: b3d8e1f4a6c2
Create Date: 2026-09-23 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c4e7a9d2f1b8"
down_revision: str | Sequence[str] | None = "b3d8e1f4a6c2"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # `RF-04-69`, `RN-04-39`: a equipe já existente ganha "Equipe N", por ordem
    # de criação dentro da mesma aula ou trilha — nomes que não colidem entre
    # si (design — decisão 6).
    op.add_column("equipe", sa.Column("nome", sa.String(length=20), nullable=True))
    op.execute(
        """
        UPDATE equipe SET nome = numeradas.nome
        FROM (
            SELECT id, 'Equipe ' || row_number() OVER (
                PARTITION BY coalesce(aula_id, trilha_id) ORDER BY registrado_em, id
            ) AS nome
            FROM equipe
        ) AS numeradas
        WHERE equipe.id = numeradas.id
        """
    )
    op.alter_column("equipe", "nome", nullable=False)
    op.create_index(
        "uq_equipe_aula_id_nome",
        "equipe",
        ["aula_id", sa.text("lower(nome)")],
        unique=True,
        postgresql_where=sa.text("aula_id IS NOT NULL"),
    )
    op.create_index(
        "uq_equipe_trilha_id_nome",
        "equipe",
        ["trilha_id", sa.text("lower(nome)")],
        unique=True,
        postgresql_where=sa.text("trilha_id IS NOT NULL"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("uq_equipe_trilha_id_nome", table_name="equipe")
    op.drop_index("uq_equipe_aula_id_nome", table_name="equipe")
    op.drop_column("equipe", "nome")
