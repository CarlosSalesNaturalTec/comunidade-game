"""modalidade individual e midia da criacao original

Revision ID: d52e3c70c0f4
Revises: 43c33632ff32
Create Date: 2026-08-27 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d52e3c70c0f4"
down_revision: str | Sequence[str] | None = "43c33632ff32"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # Aditiva, na ordem do plano de migração (design.md — Migration Plan):
    # acrescenta as colunas novas com padrão, relaxa as restrições antigas
    # e só então cria os índices parciais. Toda linha existente é de
    # equipe, com tipo texto — o backfill é determinístico.
    op.add_column("criacao_original", sa.Column("guerreiro_id", sa.Uuid(), nullable=True))
    op.add_column(
        "criacao_original",
        sa.Column(
            "tipo",
            sa.Enum(
                "texto",
                "imagem",
                "link_externo",
                "video",
                "arquivo",
                name="tipodeproducaodacriacaooriginal",
                native_enum=False,
                length=16,
            ),
            nullable=True,
        ),
    )
    op.add_column("criacao_original", sa.Column("referencia", sa.String(length=512), nullable=True))
    op.add_column("criacao_original", sa.Column("tamanho", sa.Integer(), nullable=True))
    op.add_column("criacao_original", sa.Column("motivo_da_devolucao", sa.Text(), nullable=True))
    op.execute("UPDATE criacao_original SET tipo = 'texto' WHERE tipo IS NULL")
    op.alter_column("criacao_original", "tipo", nullable=False)

    op.alter_column("criacao_original", "equipe_id", nullable=True)
    op.alter_column("criacao_original", "producao", nullable=True)

    op.drop_constraint("uq_criacao_original_equipe_id", "criacao_original", type_="unique")
    op.create_check_constraint(
        "ck_criacao_original_equipe_ou_guerreiro",
        "criacao_original",
        "(equipe_id IS NOT NULL AND guerreiro_id IS NULL) OR "
        "(equipe_id IS NULL AND guerreiro_id IS NOT NULL)",
    )
    op.create_index(
        "uq_criacao_original_equipe_id",
        "criacao_original",
        ["equipe_id"],
        unique=True,
        postgresql_where=sa.text("equipe_id IS NOT NULL"),
    )
    op.create_index(
        "uq_criacao_original_guerreiro_id_trilha_id",
        "criacao_original",
        ["guerreiro_id", "trilha_id"],
        unique=True,
        postgresql_where=sa.text("guerreiro_id IS NOT NULL"),
    )
    op.create_foreign_key(
        "fk_criacao_original_guerreiro_id_persona",
        "criacao_original",
        "persona",
        ["guerreiro_id"],
        ["id"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "fk_criacao_original_guerreiro_id_persona", "criacao_original", type_="foreignkey"
    )
    op.drop_index("uq_criacao_original_guerreiro_id_trilha_id", table_name="criacao_original")
    op.drop_index("uq_criacao_original_equipe_id", table_name="criacao_original")
    op.drop_constraint("ck_criacao_original_equipe_ou_guerreiro", "criacao_original", type_="check")
    op.create_unique_constraint("uq_criacao_original_equipe_id", "criacao_original", ["equipe_id"])

    op.alter_column("criacao_original", "producao", nullable=False)
    op.alter_column("criacao_original", "equipe_id", nullable=False)

    op.drop_column("criacao_original", "motivo_da_devolucao")
    op.drop_column("criacao_original", "tamanho")
    op.drop_column("criacao_original", "referencia")
    op.drop_column("criacao_original", "tipo")
    op.drop_column("criacao_original", "guerreiro_id")
