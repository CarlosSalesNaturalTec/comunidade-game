"""imagem da pergunta do desbloqueio e substituição que não apaga

Revision ID: 534a9c580412
Revises: d1e2f3a4b5c6
Create Date: 2026-09-11 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "534a9c580412"
down_revision: str | Sequence[str] | None = "d1e2f3a4b5c6"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # As quatro colunas da fatia 19 do PRD-09 (`RF-09-119`, `RN-05-47`),
    # todas nulas: as perguntas existentes nascem sem imagem e vigentes,
    # e não há dado a transportar (design — Migration Plan).
    op.add_column(
        "pergunta_do_desbloqueio",
        sa.Column("imagem_referencia", sa.String(length=512), nullable=True),
    )
    op.add_column(
        "pergunta_do_desbloqueio", sa.Column("imagem_tipo", sa.String(length=128), nullable=True)
    )
    op.add_column(
        "pergunta_do_desbloqueio", sa.Column("imagem_tamanho", sa.Integer(), nullable=True)
    )
    op.add_column(
        "pergunta_do_desbloqueio",
        sa.Column("substituida_em", sa.DateTime(timezone=True), nullable=True),
    )

    # A unicidade de (missão, ordem) passa a valer só entre as perguntas
    # **vigentes**: a substituída permanece na tabela, e duas gerações da
    # mesma ordem colidiriam sob a restrição antiga (design — decisão 4).
    op.drop_constraint(
        "uq_pergunta_do_desbloqueio_missao_id_ordem",
        "pergunta_do_desbloqueio",
        type_="unique",
    )
    op.create_index(
        "uq_pergunta_do_desbloqueio_missao_id_ordem",
        "pergunta_do_desbloqueio",
        ["missao_id", "ordem"],
        unique=True,
        postgresql_where=sa.text("substituida_em IS NULL"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    # A restrição antiga não admite duas gerações da mesma ordem: as
    # perguntas já substituídas saem, o que é inerente a desfazer esta
    # fatia — é o estado em que a fatia 18 as deixava.
    op.execute(
        """
        DELETE FROM resposta_da_submissao
        WHERE pergunta_id IN (
            SELECT id FROM pergunta_do_desbloqueio WHERE substituida_em IS NOT NULL
        )
        """
    )
    op.execute("DELETE FROM pergunta_do_desbloqueio WHERE substituida_em IS NOT NULL")

    op.drop_index(
        "uq_pergunta_do_desbloqueio_missao_id_ordem", table_name="pergunta_do_desbloqueio"
    )
    op.create_unique_constraint(
        "uq_pergunta_do_desbloqueio_missao_id_ordem",
        "pergunta_do_desbloqueio",
        ["missao_id", "ordem"],
    )

    op.drop_column("pergunta_do_desbloqueio", "substituida_em")
    op.drop_column("pergunta_do_desbloqueio", "imagem_tamanho")
    op.drop_column("pergunta_do_desbloqueio", "imagem_tipo")
    op.drop_column("pergunta_do_desbloqueio", "imagem_referencia")
