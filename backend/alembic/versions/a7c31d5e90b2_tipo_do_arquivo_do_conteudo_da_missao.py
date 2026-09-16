"""tipo do arquivo do conteúdo da missão

Revision ID: a7c31d5e90b2
Revises: 534a9c580412
Create Date: 2026-09-16 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a7c31d5e90b2"
down_revision: str | Sequence[str] | None = "534a9c580412"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # O tipo real do arquivo, apurado no armazenamento na confirmação do
    # envio (`RF-09-16`, `RF-09-17`, `RF-05-11`). Nula, e sem
    # retrocarregamento: conteúdo já gravado segue legível e sai como tipo
    # indeterminado — o tipo é adiante (design — decisão 2).
    op.add_column(
        "conteudo_da_missao",
        sa.Column("tipo_do_arquivo", sa.String(length=255), nullable=True),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("conteudo_da_missao", "tipo_do_arquivo")
