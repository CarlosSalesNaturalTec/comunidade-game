"""original do artefato do cadastro

Revision ID: 4fe4a2883b8c
Revises: d4e5f6a7b8c9
Create Date: 2026-09-07 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "4fe4a2883b8c"
down_revision: str | Sequence[str] | None = "d4e5f6a7b8c9"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # Três colunas nulas, sem reescrever linha alguma: artefato nunca
    # editado permanece com as três vazias, e é assim que a leitura o
    # reconhece como não mexido (`RN-09-14`, design — decisão 3, Migration
    # Plan).
    op.add_column(
        "artefato_comprobatorio", sa.Column("endereco_original", sa.String(512), nullable=True)
    )
    op.add_column(
        "artefato_comprobatorio", sa.Column("rotulo_original", sa.String(256), nullable=True)
    )
    op.add_column(
        "artefato_comprobatorio",
        sa.Column("editado_em", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("artefato_comprobatorio", "editado_em")
    op.drop_column("artefato_comprobatorio", "rotulo_original")
    op.drop_column("artefato_comprobatorio", "endereco_original")
