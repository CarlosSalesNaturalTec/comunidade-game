"""cria disciplina conteudo e etiqueta_ods

Revision ID: bfa7ba04387f
Revises: b6fa81f28651
Create Date: 2026-08-12 18:31:55.144671

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "bfa7ba04387f"
down_revision: str | Sequence[str] | None = "b6fa81f28651"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "disciplina",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("nome", sa.String(length=128), nullable=False),
        sa.Column("nome_normalizado", sa.String(length=128), nullable=False),
        sa.Column("autor_id", sa.Uuid(), nullable=False),
        sa.Column("papel_do_autor", sa.String(length=32), nullable=False),
        sa.Column(
            "registrado_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["autor_id"], ["persona.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("nome_normalizado", name="uq_disciplina_nome_normalizado"),
    )

    # Nasce publicado; os três campos abaixo só são preenchidos quando o
    # Admin despublica, sem exigir a posse do Mestre autor (design —
    # decisões).
    op.create_table(
        "conteudo",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("disciplina_id", sa.Uuid(), nullable=False),
        sa.Column("material", sa.Text(), nullable=False),
        sa.Column("despublicado_em", sa.DateTime(timezone=True), nullable=True),
        sa.Column("despublicado_por_id", sa.Uuid(), nullable=True),
        sa.Column("motivo_da_despublicacao", sa.String(length=512), nullable=True),
        sa.Column("autor_id", sa.Uuid(), nullable=False),
        sa.Column("papel_do_autor", sa.String(length=32), nullable=False),
        sa.Column(
            "registrado_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["autor_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["despublicado_por_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["disciplina_id"], ["disciplina.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    # Exatamente uma trilha ou uma missão, nunca as duas nem nenhuma —
    # restrição de banco, não só de regra (RF-01-40, RF-01-45, design —
    # decisões).
    op.create_table(
        "etiqueta_ods",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("objetivo", sa.Integer(), nullable=False),
        sa.Column("meta", sa.String(length=32), nullable=True),
        sa.Column("trilha_id", sa.Uuid(), nullable=True),
        sa.Column("missao_id", sa.Uuid(), nullable=True),
        sa.Column("autor_id", sa.Uuid(), nullable=False),
        sa.Column("papel_do_autor", sa.String(length=32), nullable=False),
        sa.Column(
            "registrado_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "objetivo >= 1 AND objetivo <= 18",
            name="ck_etiqueta_ods_objetivo_entre_1_e_18",
        ),
        sa.CheckConstraint(
            "(trilha_id IS NOT NULL AND missao_id IS NULL) OR "
            "(trilha_id IS NULL AND missao_id IS NOT NULL)",
            name="ck_etiqueta_ods_trilha_ou_missao",
        ),
        sa.ForeignKeyConstraint(["autor_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["missao_id"], ["missao.id"]),
        sa.ForeignKeyConstraint(["trilha_id"], ["trilha.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("etiqueta_ods")
    op.drop_table("conteudo")
    op.drop_table("disciplina")
