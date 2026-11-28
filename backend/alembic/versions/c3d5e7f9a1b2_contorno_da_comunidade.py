"""contorno da comunidade: geometria copiada do OSM, origem e data da cópia

Change `2026-11-27-contorno-da-comunidade` (fatia 1 do PRD-08): a
`comunidade_virtual` ganha o contorno em GeoJSON, o elemento de origem no OSM e a
data da cópia, todos anuláveis — a comunidade já criada segue sem contorno até o
Admin gravá-lo (`RF-08-33`, design — decisão 1).

Revision ID: c3d5e7f9a1b2
Revises: a7c9e1b3d5f7
Create Date: 2026-11-27 23:00:00

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "c3d5e7f9a1b2"
down_revision: str | Sequence[str] | None = "a7c9e1b3d5f7"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("comunidade_virtual", sa.Column("contorno", sa.JSON(), nullable=True))
    op.add_column(
        "comunidade_virtual",
        sa.Column("contorno_origem_osm", sa.String(length=32), nullable=True),
    )
    op.add_column(
        "comunidade_virtual",
        sa.Column("contorno_copiado_em", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("comunidade_virtual", "contorno_copiado_em")
    op.drop_column("comunidade_virtual", "contorno_origem_osm")
    op.drop_column("comunidade_virtual", "contorno")
