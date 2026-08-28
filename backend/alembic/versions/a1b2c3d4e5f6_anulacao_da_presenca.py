"""anulacao da presenca

Revision ID: a1b2c3d4e5f6
Revises: d52e3c70c0f4
Create Date: 2026-08-27 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a1b2c3d4e5f6"
down_revision: str | Sequence[str] | None = "d52e3c70c0f4"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # Aditiva: nenhuma presença existente tem `anulada_em` preenchido, e a
    # unicidade por (aula, guerreiro) passa a valer só entre as não
    # anuladas — o índice parcial substitui a constraint antiga sem exigir
    # dado novo em linha alguma (`RF-02-36`, `RN-02-12`, design — decisão 4).
    op.add_column("presenca", sa.Column("anulada_em", sa.DateTime(timezone=True), nullable=True))
    op.add_column("presenca", sa.Column("anulada_por_id", sa.Uuid(), nullable=True))
    op.add_column("presenca", sa.Column("motivo_da_anulacao", sa.Text(), nullable=True))
    op.create_foreign_key(
        "fk_presenca_anulada_por_id_persona",
        "presenca",
        "persona",
        ["anulada_por_id"],
        ["id"],
    )

    op.drop_constraint("uq_presenca_aula_id_guerreiro_id", "presenca", type_="unique")
    op.create_index(
        "uq_presenca_aula_id_guerreiro_id_nao_anulada",
        "presenca",
        ["aula_id", "guerreiro_id"],
        unique=True,
        postgresql_where=sa.text("anulada_em IS NULL"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("uq_presenca_aula_id_guerreiro_id_nao_anulada", table_name="presenca")
    op.create_unique_constraint(
        "uq_presenca_aula_id_guerreiro_id", "presenca", ["aula_id", "guerreiro_id"]
    )

    op.drop_constraint("fk_presenca_anulada_por_id_persona", "presenca", type_="foreignkey")
    op.drop_column("presenca", "motivo_da_anulacao")
    op.drop_column("presenca", "anulada_por_id")
    op.drop_column("presenca", "anulada_em")
