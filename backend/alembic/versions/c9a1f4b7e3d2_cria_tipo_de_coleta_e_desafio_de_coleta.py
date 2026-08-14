"""cria tipo_de_coleta e desafio_de_coleta

Revision ID: c9a1f4b7e3d2
Revises: 9637d98fa3e4
Create Date: 2026-08-14 14:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c9a1f4b7e3d2"
down_revision: str | Sequence[str] | None = "9637d98fa3e4"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # Unidade e faixa esperada só existem no tipo que se mede por número
    # (RF-08-05, RF-08-12, design — Decisions).
    op.create_table(
        "tipo_de_coleta",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("nome", sa.String(length=128), nullable=False),
        sa.Column(
            "forma_de_registro",
            sa.Enum(
                "numero",
                "foto",
                "video",
                name="formaderegistro",
                native_enum=False,
                length=16,
            ),
            nullable=False,
        ),
        sa.Column("unidade", sa.String(length=32), nullable=True),
        sa.Column("faixa_minima", sa.Float(), nullable=True),
        sa.Column("faixa_maxima", sa.Float(), nullable=True),
        sa.Column("ativo", sa.Boolean(), nullable=False),
        sa.Column("autor_id", sa.Uuid(), nullable=False),
        sa.Column("papel_do_autor", sa.String(length=32), nullable=False),
        sa.Column(
            "registrado_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "(forma_de_registro = 'numero' AND unidade IS NOT NULL AND "
            "faixa_minima IS NOT NULL AND faixa_maxima IS NOT NULL) OR "
            "(forma_de_registro != 'numero' AND unidade IS NULL AND "
            "faixa_minima IS NULL AND faixa_maxima IS NULL)",
            name="ck_tipo_de_coleta_unidade_e_faixa_so_no_tipo_numero",
        ),
        sa.CheckConstraint(
            "faixa_minima IS NULL OR faixa_maxima IS NULL OR faixa_minima <= faixa_maxima",
            name="ck_tipo_de_coleta_faixa_minima_menor_ou_igual_a_maxima",
        ),
        sa.ForeignKeyConstraint(["autor_id"], ["persona.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    # Sem coluna de trilha nem de etiqueta ODS: ambas são derivadas, nunca
    # copiadas (design — Decisions).
    op.create_table(
        "desafio_de_coleta",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("missao_id", sa.Uuid(), nullable=False),
        sa.Column("tipo_de_coleta_id", sa.Uuid(), nullable=False),
        sa.Column(
            "cadencia",
            sa.Enum(
                "diaria",
                "semanal",
                "mensal",
                name="cadencia",
                native_enum=False,
                length=16,
            ),
            nullable=False,
        ),
        sa.Column("vigencia_inicio", sa.DateTime(timezone=True), nullable=False),
        sa.Column("vigencia_fim", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "granularidade_exigida",
            sa.Enum(
                "comunidade",
                "bairro",
                "rua",
                "condominio",
                "bloco",
                "quadra",
                name="niveldolocal",
                native_enum=False,
                length=16,
            ),
            nullable=False,
        ),
        sa.Column("registros_que_pontuam_por_periodo", sa.Integer(), nullable=False),
        sa.Column("autor_id", sa.Uuid(), nullable=False),
        sa.Column("papel_do_autor", sa.String(length=32), nullable=False),
        sa.Column(
            "registrado_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "vigencia_fim >= vigencia_inicio",
            name="ck_desafio_de_coleta_vigencia_fim_nao_precede_inicio",
        ),
        sa.CheckConstraint(
            "registros_que_pontuam_por_periodo >= 1",
            name="ck_desafio_de_coleta_registros_que_pontuam_maior_ou_igual_a_1",
        ),
        sa.ForeignKeyConstraint(["autor_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["missao_id"], ["missao.id"]),
        sa.ForeignKeyConstraint(["tipo_de_coleta_id"], ["tipo_de_coleta.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("desafio_de_coleta")
    op.drop_table("tipo_de_coleta")
