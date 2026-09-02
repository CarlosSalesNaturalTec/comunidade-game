"""reserva serve aula ou desafio extra

Revision ID: 1f47b0e735c9
Revises: 6ef2d53a10d7
Create Date: 2026-09-02 12:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "1f47b0e735c9"
down_revision: str | Sequence[str] | None = "6ef2d53a10d7"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # A reserva passa a servir aula ou desafio extra — exatamente um dos
    # dois —, como o PRD-07 §8 já descreve a entidade (`RF-07-39`, design —
    # Decisions 2). Nenhuma linha existente muda de valor: `aula_id` só
    # deixa de ser obrigatório, e o `CHECK` de exclusividade mantém a
    # garantia que o `NOT NULL` dava às reservas de aula.
    op.alter_column("reserva", "aula_id", nullable=True)
    op.add_column("reserva", sa.Column("desafio_extra_id", sa.Uuid(), nullable=True))
    op.create_foreign_key(
        "fk_reserva_desafio_extra_id_desafio_extra",
        "reserva",
        "desafio_extra",
        ["desafio_extra_id"],
        ["id"],
    )
    op.create_index("ix_reserva_desafio_extra_id", "reserva", ["desafio_extra_id"])
    op.create_check_constraint(
        "ck_reserva_aula_ou_desafio_extra",
        "reserva",
        "(aula_id IS NOT NULL AND desafio_extra_id IS NULL) OR "
        "(aula_id IS NULL AND desafio_extra_id IS NOT NULL)",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("ck_reserva_aula_ou_desafio_extra", "reserva", type_="check")
    op.drop_index("ix_reserva_desafio_extra_id", table_name="reserva")
    op.drop_constraint("fk_reserva_desafio_extra_id_desafio_extra", "reserva", type_="foreignkey")
    op.drop_column("reserva", "desafio_extra_id")
    op.alter_column("reserva", "aula_id", nullable=False)
