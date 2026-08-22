"""culminancia e publicacao da trilha

Revision ID: 5c60068d9f47
Revises: 08bd6438e436
Create Date: 2026-08-22 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "5c60068d9f47"
down_revision: str | Sequence[str] | None = "08bd6438e436"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "culminancia",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("trilha_id", sa.Uuid(), nullable=False),
        sa.Column("descricao", sa.Text(), nullable=False),
        sa.Column(
            "modalidade",
            sa.Enum(
                "individual",
                "em_equipe",
                name="modalidadedaculminancia",
                native_enum=False,
                length=16,
            ),
            nullable=False,
        ),
        sa.Column("criterio_de_validacao", sa.Text(), nullable=False),
        sa.Column("autor_id", sa.Uuid(), nullable=False),
        sa.Column("papel_do_autor", sa.String(length=32), nullable=False),
        sa.Column(
            "registrado_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["autor_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["trilha_id"], ["trilha.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("trilha_id", name="uq_culminancia_trilha_id"),
    )

    # `despublicada` em `SituacaoDaTrilha.situacao` não exige DDL: a coluna
    # é `native_enum=False` — VARCHAR(16) sem CHECK constraint —, então o
    # valor novo já cabe sem tocar a tabela (mesmo padrão de
    # `b6fa81f28651_cria_criacao_original_e_badge_de_autoria`). Nenhuma
    # trilha existente muda de valor.
    op.add_column("trilha", sa.Column("motivo_da_situacao", sa.Text(), nullable=True))
    op.add_column("trilha", sa.Column("autor_da_situacao_id", sa.Uuid(), nullable=True))
    op.add_column(
        "trilha", sa.Column("papel_do_autor_da_situacao", sa.String(length=32), nullable=True)
    )
    op.add_column(
        "trilha", sa.Column("situacao_alterada_em", sa.DateTime(timezone=True), nullable=True)
    )
    op.create_foreign_key(
        "fk_trilha_autor_da_situacao_id_persona",
        "trilha",
        "persona",
        ["autor_da_situacao_id"],
        ["id"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("fk_trilha_autor_da_situacao_id_persona", "trilha", type_="foreignkey")
    op.drop_column("trilha", "situacao_alterada_em")
    op.drop_column("trilha", "papel_do_autor_da_situacao")
    op.drop_column("trilha", "autor_da_situacao_id")
    op.drop_column("trilha", "motivo_da_situacao")

    op.drop_table("culminancia")
