"""declaracao de aporte da app 08

Revision ID: c3d2e6f970c9
Revises: f4a5b6c7d8e9
Create Date: 2026-09-01 20:05:49.583909

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c3d2e6f970c9"
down_revision: str | Sequence[str] | None = "f4a5b6c7d8e9"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # A declaração do Apoiador em sessão, pendente até a homologação ou a
    # recusa do Admin (`RF-14-25` a `RF-14-27`, design — Migration Plan).
    op.create_table(
        "aporte_declarado",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("provedor_id", sa.Uuid(), nullable=False),
        sa.Column("valor_declarado", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column(
            "origem_da_escolha",
            sa.Enum(
                "necessidade",
                "valor_sugerido",
                "valor_livre",
                name="origemdaescolhadoaporte",
                native_enum=False,
                length=16,
            ),
            nullable=False,
        ),
        sa.Column("aula_id", sa.Uuid(), nullable=True),
        sa.Column("tipo_de_recurso_id", sa.Uuid(), nullable=True),
        sa.Column("comprovante_referencia", sa.String(length=512), nullable=True),
        sa.Column("comprovante_nome_original", sa.String(length=256), nullable=True),
        sa.Column("comprovante_tipo", sa.String(length=128), nullable=True),
        sa.Column("comprovante_tamanho", sa.Integer(), nullable=True),
        sa.Column(
            "situacao",
            sa.Enum(
                "pendente",
                "homologada",
                "recusada",
                name="situacaodadeclaracao",
                native_enum=False,
                length=16,
            ),
            nullable=False,
        ),
        sa.Column("motivo_da_recusa", sa.String(length=1024), nullable=True),
        sa.Column("resolvido_por_id", sa.Uuid(), nullable=True),
        sa.Column("resolvido_em", sa.DateTime(timezone=True), nullable=True),
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
        sa.ForeignKeyConstraint(["provedor_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["resolvido_por_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["tipo_de_recurso_id"], ["tipo_de_recurso.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    # Único e anulável: a mesma declaração não credita duas vezes
    # (`RF-14-26`, `RN-14-07`, design — Decisions 2).
    op.add_column("aporte", sa.Column("aporte_declarado_id", sa.Uuid(), nullable=True))
    op.create_unique_constraint("uq_aporte_aporte_declarado_id", "aporte", ["aporte_declarado_id"])
    op.create_foreign_key(
        "fk_aporte_aporte_declarado_id_aporte_declarado",
        "aporte",
        "aporte_declarado",
        ["aporte_declarado_id"],
        ["id"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "fk_aporte_aporte_declarado_id_aporte_declarado", "aporte", type_="foreignkey"
    )
    op.drop_constraint("uq_aporte_aporte_declarado_id", "aporte", type_="unique")
    op.drop_column("aporte", "aporte_declarado_id")
    op.drop_table("aporte_declarado")
