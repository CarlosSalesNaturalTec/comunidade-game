"""nick insensível a caixa e nick da solicitação de participação

Revision ID: e2f3a4b5c6d7
Revises: d6e7f8a9b0c1
Create Date: 2026-08-21 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e2f3a4b5c6d7"
down_revision: str | Sequence[str] | None = "d6e7f8a9b0c1"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # `RN-01-30`: "Zeferina" e "zeferina" passam a colidir. Se dois nicks já
    # existentes diferem só na caixa, este índice falha ao subir — conferir
    # antes de aplicar em produção (design — Migration Plan).
    op.drop_index("uq_nick_valor", table_name="nick")
    op.create_index("uq_nick_valor", "nick", [sa.text("lower(valor)")], unique=True)

    # Nula: nem toda solicitação declara nick — só a de Apoiador (`RF-01-25`).
    op.add_column(
        "solicitacao_de_participacao", sa.Column("nick", sa.String(length=64), nullable=True)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("solicitacao_de_participacao", "nick")
    op.drop_index("uq_nick_valor", table_name="nick")
    op.create_index("uq_nick_valor", "nick", ["valor"], unique=True)
