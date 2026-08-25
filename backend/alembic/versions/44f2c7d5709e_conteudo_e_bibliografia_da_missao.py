"""conteudo e bibliografia da missao

Revision ID: 44f2c7d5709e
Revises: b9c0d1e2f3a4
Create Date: 2026-08-25 02:22:20.196698

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "44f2c7d5709e"
down_revision: str | Sequence[str] | None = "b9c0d1e2f3a4"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "conteudo_da_missao",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("missao_id", sa.Uuid(), nullable=False),
        sa.Column("ordem", sa.Integer(), nullable=False),
        sa.Column(
            "tipo",
            sa.Enum(
                "texto",
                "imagem",
                "link_externo",
                "video",
                "arquivo",
                name="tipodeconteudo",
                native_enum=False,
                length=16,
            ),
            nullable=False,
        ),
        sa.Column("corpo", sa.Text(), nullable=True),
        sa.Column("endereco", sa.String(length=2048), nullable=True),
        sa.Column("referencia", sa.String(length=512), nullable=True),
        sa.Column("tamanho", sa.Integer(), nullable=True),
        sa.Column(
            "autoria",
            sa.Enum("propria", "terceiro", name="autoriadoconteudo", native_enum=False, length=16),
            nullable=False,
        ),
        sa.Column("fonte", sa.Text(), nullable=True),
        sa.Column("autor_id", sa.Uuid(), nullable=False),
        sa.Column("papel_do_autor", sa.String(length=32), nullable=False),
        sa.Column(
            "registrado_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["autor_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["missao_id"], ["missao.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "bibliografia_da_missao",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("missao_id", sa.Uuid(), nullable=False),
        sa.Column("titulo", sa.String(length=256), nullable=False),
        sa.Column("capitulo", sa.Text(), nullable=False),
        sa.Column("item_patrimonial_id", sa.Uuid(), nullable=True),
        sa.Column("autor_id", sa.Uuid(), nullable=False),
        sa.Column("papel_do_autor", sa.String(length=32), nullable=False),
        sa.Column(
            "registrado_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["autor_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["item_patrimonial_id"], ["item_patrimonial.id"]),
        sa.ForeignKeyConstraint(["missao_id"], ["missao.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("bibliografia_da_missao")
    op.drop_table("conteudo_da_missao")
