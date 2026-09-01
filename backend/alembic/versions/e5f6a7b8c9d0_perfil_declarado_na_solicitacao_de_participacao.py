"""perfil declarado na solicitacao de participacao

Revision ID: e5f6a7b8c9d0
Revises: d3e4f5a6b7c8
Create Date: 2026-09-01 00:00:00.000002

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e5f6a7b8c9d0"
down_revision: str | Sequence[str] | None = "d3e4f5a6b7c8"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # O perfil só existe no pré-cadastro do Apoiador; as solicitações já
    # registradas ficam sem perfil, que é o correto — elas não o declararam
    # (`RF-14-01`, `RN-14-39`, design — Migration Plan).
    op.add_column(
        "solicitacao_de_participacao",
        sa.Column(
            "perfil",
            sa.Enum(
                "pessoa_fisica",
                "pessoa_juridica",
                name="perfildeapoiador",
                native_enum=False,
                length=16,
            ),
            nullable=True,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("solicitacao_de_participacao", "perfil")
