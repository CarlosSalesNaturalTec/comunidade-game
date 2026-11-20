"""finalidade do tipo de recurso

Decisão do fundador de 2026-11-20 (change `finalidade-do-tipo-de-recurso`): todo tipo
de recurso não durável tem uma finalidade — consumo do encontro ou recompensa —, e o
durável não tem nenhuma. Os tipos já cadastrados nascem recompensa, e o Admin corrige
depois os de consumo do encontro (`RF-07-53`, `RN-07-41`, design — decisão 4).

Revision ID: d4f6a8c0e2b3
Revises: c2e4a6b8d0f1
Create Date: 2026-11-20 12:00:00

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "d4f6a8c0e2b3"
down_revision: str | Sequence[str] | None = "c2e4a6b8d0f1"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_TRAVA = "ck_tipo_de_recurso_finalidade_so_no_nao_duravel"


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("tipo_de_recurso", sa.Column("finalidade", sa.String(24), nullable=True))
    op.execute("UPDATE tipo_de_recurso SET finalidade = 'recompensa' WHERE natureza <> 'duravel'")
    op.create_check_constraint(
        _TRAVA, "tipo_de_recurso", "(natureza = 'duravel') = (finalidade IS NULL)"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(_TRAVA, "tipo_de_recurso", type_="check")
    op.drop_column("tipo_de_recurso", "finalidade")
