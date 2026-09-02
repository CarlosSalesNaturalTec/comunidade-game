"""missoes do apoiador, sustento e selos

Revision ID: 02239f525269
Revises: c3d2e6f970c9
Create Date: 2026-09-01 22:10:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "02239f525269"
down_revision: str | Sequence[str] | None = "c3d2e6f970c9"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # O chamado que a gestão publica a partir de uma necessidade de recurso
    # publicada (`RF-02-102`, `RN-14-31`, design — Migration Plan).
    op.create_table(
        "missao_do_apoiador",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("aula_id", sa.Uuid(), nullable=False),
        sa.Column("tipo_de_recurso_id", sa.Uuid(), nullable=False),
        sa.Column(
            "nivel_de_necessidade",
            sa.Enum(
                "existir",
                "acontecer",
                "reconhecer",
                "permanecer",
                name="niveldenecessidade",
                native_enum=False,
                length=16,
            ),
            nullable=False,
        ),
        sa.Column("titulo", sa.String(length=128), nullable=False),
        sa.Column("o_que_se_pede", sa.String(length=512), nullable=False),
        sa.Column("quantidade", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("prazo", sa.Date(), nullable=False),
        sa.Column("selo_nome", sa.String(length=128), nullable=False),
        sa.Column(
            "selo_familia",
            sa.Enum(
                "frente",
                "modalidade",
                "ato",
                "multiplicacao",
                name="familiadeselo",
                native_enum=False,
                length=16,
            ),
            nullable=False,
        ),
        sa.Column(
            "situacao",
            sa.Enum(
                "aberta",
                "concluida",
                "despublicada",
                name="situacaodamissao",
                native_enum=False,
                length=16,
            ),
            nullable=False,
        ),
        sa.Column("autor_id", sa.Uuid(), nullable=False),
        sa.Column("papel_do_autor", sa.String(length=32), nullable=False),
        sa.Column(
            "registrado_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["aula_id"], ["aula.id"]),
        sa.ForeignKeyConstraint(["autor_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["tipo_de_recurso_id"], ["tipo_de_recurso.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    # Somente inserção, sem rota de remoção (`RF-14-66`, `RN-14-36`, design
    # — Decisions 6). O índice único impede o crédito duplo.
    op.create_table(
        "selo_do_apoiador",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("apoiador_id", sa.Uuid(), nullable=False),
        sa.Column(
            "familia",
            sa.Enum(
                "frente",
                "modalidade",
                "ato",
                "multiplicacao",
                name="familiadeselo",
                native_enum=False,
                length=16,
            ),
            nullable=False,
        ),
        sa.Column("selo_nome", sa.String(length=128), nullable=False),
        sa.Column("missao_do_apoiador_id", sa.Uuid(), nullable=False),
        sa.Column(
            "creditado_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["apoiador_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["missao_do_apoiador_id"], ["missao_do_apoiador.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "apoiador_id",
            "missao_do_apoiador_id",
            "selo_nome",
            name="uq_selo_do_apoiador_apoiador_missao_selo",
        ),
    )

    # A origem `missao` do aporte declarado (`RF-14-63`, design — Migration
    # Plan): a declaração aponta a missão escolhida, sem abater nada até a
    # homologação.
    op.add_column("aporte_declarado", sa.Column("missao_do_apoiador_id", sa.Uuid(), nullable=True))
    op.create_foreign_key(
        "fk_aporte_declarado_missao_do_apoiador_id_missao_do_apoiador",
        "aporte_declarado",
        "missao_do_apoiador",
        ["missao_do_apoiador_id"],
        ["id"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "fk_aporte_declarado_missao_do_apoiador_id_missao_do_apoiador",
        "aporte_declarado",
        type_="foreignkey",
    )
    op.drop_column("aporte_declarado", "missao_do_apoiador_id")

    op.drop_table("selo_do_apoiador")
    op.drop_table("missao_do_apoiador")
