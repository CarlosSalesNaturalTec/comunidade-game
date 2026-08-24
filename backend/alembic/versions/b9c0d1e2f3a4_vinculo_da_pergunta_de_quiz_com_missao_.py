"""vinculo da pergunta de quiz com missao e trilha

Revision ID: b9c0d1e2f3a4
Revises: 40a07b5f3ebd
Create Date: 2026-08-23 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b9c0d1e2f3a4"
down_revision: str | Sequence[str] | None = "40a07b5f3ebd"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # `pergunta_de_quiz` nunca teve rota: a tabela está vazia em todo
    # ambiente, e por isso as duas colunas nascem `NOT NULL` direto, sem
    # backfill (`RF-09-39`, design — Migration Plan).
    op.add_column("pergunta_de_quiz", sa.Column("missao_id", sa.Uuid(), nullable=False))
    op.add_column("pergunta_de_quiz", sa.Column("trilha_id", sa.Uuid(), nullable=False))
    op.create_foreign_key(
        "fk_pergunta_de_quiz_missao_id_missao",
        "pergunta_de_quiz",
        "missao",
        ["missao_id"],
        ["id"],
    )
    op.create_foreign_key(
        "fk_pergunta_de_quiz_trilha_id_trilha",
        "pergunta_de_quiz",
        "trilha",
        ["trilha_id"],
        ["id"],
    )
    op.create_index("ix_pergunta_de_quiz_missao_id", "pergunta_de_quiz", ["missao_id"])
    op.create_index("ix_pergunta_de_quiz_trilha_id", "pergunta_de_quiz", ["trilha_id"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("ix_pergunta_de_quiz_trilha_id", table_name="pergunta_de_quiz")
    op.drop_index("ix_pergunta_de_quiz_missao_id", table_name="pergunta_de_quiz")
    op.drop_constraint(
        "fk_pergunta_de_quiz_trilha_id_trilha", "pergunta_de_quiz", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_pergunta_de_quiz_missao_id_missao", "pergunta_de_quiz", type_="foreignkey"
    )
    op.drop_column("pergunta_de_quiz", "trilha_id")
    op.drop_column("pergunta_de_quiz", "missao_id")
