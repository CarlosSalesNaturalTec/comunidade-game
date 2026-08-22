"""desativacao do ponto de apoio

Revision ID: f219b904100a
Revises: 0c8b75de3336
Create Date: 2026-08-21 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f219b904100a"
down_revision: str | Sequence[str] | None = "0c8b75de3336"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # Aditiva: `ativo` já existe e nenhum ponto de apoio muda de valor; as
    # colunas novas só entram na trilha de auditoria a partir da primeira
    # desativação ou reativação (`RF-07-47`, design — Migration Plan).
    op.add_column("ponto_de_apoio", sa.Column("motivo_da_situacao", sa.Text(), nullable=True))
    op.add_column("ponto_de_apoio", sa.Column("autor_da_situacao_id", sa.Uuid(), nullable=True))
    op.add_column(
        "ponto_de_apoio",
        sa.Column("papel_do_autor_da_situacao", sa.String(length=32), nullable=True),
    )
    op.add_column(
        "ponto_de_apoio",
        sa.Column("situacao_alterada_em", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_foreign_key(
        "fk_ponto_de_apoio_autor_da_situacao_id_persona",
        "ponto_de_apoio",
        "persona",
        ["autor_da_situacao_id"],
        ["id"],
    )

    # A referência mútua do par de uma transferência: nenhum lançamento
    # existente a declara, e é `DEFERRABLE INITIALLY DEFERRED` porque os
    # dois lançamentos do par só existem, um para o outro, dentro da mesma
    # operação (`RF-07-19`, `RN-07-15`, design — Decisions 1).
    op.add_column("lancamento", sa.Column("lancamento_relacionado_id", sa.Uuid(), nullable=True))
    op.create_foreign_key(
        "fk_lancamento_lancamento_relacionado_id_lancamento",
        "lancamento",
        "lancamento",
        ["lancamento_relacionado_id"],
        ["id"],
        deferrable=True,
        initially="DEFERRED",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "fk_lancamento_lancamento_relacionado_id_lancamento", "lancamento", type_="foreignkey"
    )
    op.drop_column("lancamento", "lancamento_relacionado_id")

    op.drop_constraint(
        "fk_ponto_de_apoio_autor_da_situacao_id_persona", "ponto_de_apoio", type_="foreignkey"
    )
    op.drop_column("ponto_de_apoio", "situacao_alterada_em")
    op.drop_column("ponto_de_apoio", "papel_do_autor_da_situacao")
    op.drop_column("ponto_de_apoio", "autor_da_situacao_id")
    op.drop_column("ponto_de_apoio", "motivo_da_situacao")
