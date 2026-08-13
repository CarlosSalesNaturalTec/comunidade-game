"""ciclo de vida da chave de terceiro

Revision ID: d7a99bc76819
Revises: 158b8d6287f5
Create Date: 2026-08-13 21:05:57.774012

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d7a99bc76819"
down_revision: str | Sequence[str] | None = "158b8d6287f5"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "chave_de_aplicacao", sa.Column("solicitacao_de_chave_id", sa.Uuid(), nullable=True)
    )
    op.create_unique_constraint(
        "uq_chave_de_aplicacao_solicitacao_de_chave_id",
        "chave_de_aplicacao",
        ["solicitacao_de_chave_id"],
    )
    op.create_foreign_key(
        "fk_chave_de_aplicacao_solicitacao_de_chave_id",
        "chave_de_aplicacao",
        "solicitacao_de_chave",
        ["solicitacao_de_chave_id"],
        ["id"],
    )

    op.add_column("solicitacao_de_chave", sa.Column("chave_id", sa.Uuid(), nullable=True))
    op.create_unique_constraint(
        "uq_solicitacao_de_chave_chave_id", "solicitacao_de_chave", ["chave_id"]
    )
    op.create_foreign_key(
        "fk_solicitacao_de_chave_chave_id_chave_de_aplicacao",
        "solicitacao_de_chave",
        "chave_de_aplicacao",
        ["chave_id"],
        ["id"],
    )

    # A unicidade por aplicação e ambiente passa a valer só para as chaves do
    # projeto (RN-01-51): a chave de terceiro se identifica pela solicitação
    # que a originou, não pelo nome da aplicação declarada.
    op.drop_index(
        "uq_chave_vigente_por_aplicacao_e_ambiente",
        table_name="chave_de_aplicacao",
        postgresql_where=sa.text("situacao = 'vigente'"),
    )
    op.create_index(
        "uq_chave_vigente_por_aplicacao_e_ambiente",
        "chave_de_aplicacao",
        ["aplicacao", "ambiente"],
        unique=True,
        postgresql_where=sa.text("situacao = 'vigente' AND natureza = 'do_projeto'"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(
        "uq_chave_vigente_por_aplicacao_e_ambiente",
        table_name="chave_de_aplicacao",
        postgresql_where=sa.text("situacao = 'vigente' AND natureza = 'do_projeto'"),
    )
    op.create_index(
        "uq_chave_vigente_por_aplicacao_e_ambiente",
        "chave_de_aplicacao",
        ["aplicacao", "ambiente"],
        unique=True,
        postgresql_where=sa.text("situacao = 'vigente'"),
    )

    op.drop_constraint(
        "fk_solicitacao_de_chave_chave_id_chave_de_aplicacao",
        "solicitacao_de_chave",
        type_="foreignkey",
    )
    op.drop_constraint("uq_solicitacao_de_chave_chave_id", "solicitacao_de_chave", type_="unique")
    op.drop_column("solicitacao_de_chave", "chave_id")

    op.drop_constraint(
        "fk_chave_de_aplicacao_solicitacao_de_chave_id",
        "chave_de_aplicacao",
        type_="foreignkey",
    )
    op.drop_constraint(
        "uq_chave_de_aplicacao_solicitacao_de_chave_id", "chave_de_aplicacao", type_="unique"
    )
    op.drop_column("chave_de_aplicacao", "solicitacao_de_chave_id")
