"""titulo, etapa e cadência de retomada da missão e da atividade

Revision ID: 08bd6438e436
Revises: f219b904100a
Create Date: 2026-08-22 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "08bd6438e436"
down_revision: str | Sequence[str] | None = "f219b904100a"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # `titulo` e `etapa_do_ciclo` são `NOT NULL` em tabelas que já existem
    # (`RF-09-03`, `RF-09-69`, PRD-09 §8, design — decisões 8): entram
    # anuláveis, recebem o preenchimento e só então a trava. O preenchimento
    # de `titulo` é o identificador da própria linha — legível e único; o de
    # `etapa_do_ciclo` é "desenvolvimento", a etapa mais genérica do
    # documento 11 §2.4. `descricao` e `cadencia_de_retomada` entram
    # anuláveis e ficam assim.
    op.add_column("missao", sa.Column("titulo", sa.String(length=128), nullable=True))
    op.execute("UPDATE missao SET titulo = id::text WHERE titulo IS NULL")
    op.alter_column("missao", "titulo", nullable=False)

    op.add_column(
        "missao",
        sa.Column(
            "etapa_do_ciclo",
            sa.Enum(
                "abertura",
                "desenvolvimento",
                "marcos",
                "fechamento",
                name="etapadociclo",
                native_enum=False,
                length=16,
            ),
            nullable=True,
        ),
    )
    op.execute("UPDATE missao SET etapa_do_ciclo = 'desenvolvimento' WHERE etapa_do_ciclo IS NULL")
    op.alter_column("missao", "etapa_do_ciclo", nullable=False)

    op.add_column(
        "missao", sa.Column("cadencia_de_retomada", sa.ARRAY(sa.Integer()), nullable=True)
    )

    op.add_column("atividade", sa.Column("titulo", sa.String(length=128), nullable=True))
    op.execute("UPDATE atividade SET titulo = id::text WHERE titulo IS NULL")
    op.alter_column("atividade", "titulo", nullable=False)

    op.add_column("atividade", sa.Column("descricao", sa.Text(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("atividade", "descricao")
    op.drop_column("atividade", "titulo")
    op.drop_column("missao", "cadencia_de_retomada")
    op.drop_column("missao", "etapa_do_ciclo")
    op.drop_column("missao", "titulo")
