"""comprovante do resultado: a produção vira comprovante em seis formas

Change `lancamento-com-comprovante-e-julgamento-do-pratico` (fatia 41 do PRD-09): o
Resultado ganha a forma do comprovante e as colunas da mídia, e `producao` passa a
guardar só o texto ou o endereço. As linhas existentes recebem a forma **texto** — o
que gravaram é texto —, e a coluna fica obrigatória em seguida (`RF-09-149`,
`RN-09-64`, design — decisão 1).

Revision ID: a7c9e1b3d5f7
Revises: f6b8d0a2c4e5
Create Date: 2026-11-27 12:00:00

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "a7c9e1b3d5f7"
down_revision: str | Sequence[str] | None = "f6b8d0a2c4e5"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("resultado", sa.Column("comprovante_tipo", sa.String(length=32), nullable=True))
    op.execute("UPDATE resultado SET comprovante_tipo = 'texto'")
    op.alter_column("resultado", "comprovante_tipo", nullable=False)
    op.add_column(
        "resultado", sa.Column("comprovante_referencia", sa.String(length=512), nullable=True)
    )
    op.create_unique_constraint(
        "resultado_comprovante_referencia_key", "resultado", ["comprovante_referencia"]
    )
    op.add_column("resultado", sa.Column("comprovante_tamanho", sa.Integer(), nullable=True))
    op.add_column(
        "resultado",
        sa.Column("comprovante_tipo_do_arquivo", sa.String(length=255), nullable=True),
    )
    op.alter_column("resultado", "producao", existing_type=sa.Text(), nullable=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("UPDATE resultado SET producao = '' WHERE producao IS NULL")
    op.alter_column("resultado", "producao", existing_type=sa.Text(), nullable=False)
    op.drop_column("resultado", "comprovante_tipo_do_arquivo")
    op.drop_column("resultado", "comprovante_tamanho")
    op.drop_constraint("resultado_comprovante_referencia_key", "resultado", type_="unique")
    op.drop_column("resultado", "comprovante_referencia")
    op.drop_column("resultado", "comprovante_tipo")
