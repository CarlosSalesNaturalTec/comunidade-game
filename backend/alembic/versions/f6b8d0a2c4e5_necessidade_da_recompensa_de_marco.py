"""necessidade da recompensa de marco: comunidade e trilha no lugar da aula

Change `necessidade-da-recompensa-de-marco` (fatia 14 do PRD-07): a necessidade da
recompensa de marco é identificada por comunidade + trilha + tipo de recurso. A
absorção, a declaração do Apoiador e a missão do Apoiador passam a apontá-la, e a
missão deixa de exigir aula (`RF-07-28`, `RF-07-54`, `RF-02-102`, `RF-14-25`, design —
decisões 3, 5).

Revision ID: f6b8d0a2c4e5
Revises: e5a7c9b1d3f4
Create Date: 2026-11-21 12:00:00

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "f6b8d0a2c4e5"
down_revision: str | Sequence[str] | None = "e5a7c9b1d3f4"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_TABELAS = ("aporte", "aporte_declarado", "missao_do_apoiador")


def upgrade() -> None:
    """Upgrade schema."""
    for tabela in _TABELAS:
        op.add_column(tabela, sa.Column("comunidade_virtual_id", sa.Uuid(), nullable=True))
        op.add_column(tabela, sa.Column("trilha_id", sa.Uuid(), nullable=True))
        op.create_foreign_key(
            f"{tabela}_comunidade_virtual_id_fkey",
            tabela,
            "comunidade_virtual",
            ["comunidade_virtual_id"],
            ["id"],
        )
        op.create_foreign_key(f"{tabela}_trilha_id_fkey", tabela, "trilha", ["trilha_id"], ["id"])
    op.alter_column("missao_do_apoiador", "aula_id", existing_type=sa.Uuid(), nullable=True)
    op.create_check_constraint(
        "ck_missao_do_apoiador_aula_ou_trilha",
        "missao_do_apoiador",
        "(aula_id IS NOT NULL AND comunidade_virtual_id IS NULL AND trilha_id IS NULL) OR "
        "(aula_id IS NULL AND comunidade_virtual_id IS NOT NULL AND trilha_id IS NOT NULL)",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("ck_missao_do_apoiador_aula_ou_trilha", "missao_do_apoiador", "check")
    op.alter_column("missao_do_apoiador", "aula_id", existing_type=sa.Uuid(), nullable=False)
    for tabela in _TABELAS:
        op.drop_constraint(f"{tabela}_trilha_id_fkey", tabela, "foreignkey")
        op.drop_constraint(f"{tabela}_comunidade_virtual_id_fkey", tabela, "foreignkey")
        op.drop_column(tabela, "trilha_id")
        op.drop_column(tabela, "comunidade_virtual_id")
