"""cria persona sessao credencial e comunidade virtual

Revision ID: 06d3d81b962a
Revises: 40d7e4ba7213
Create Date: 2026-08-12 00:25:51.305546

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "06d3d81b962a"
down_revision: str | Sequence[str] | None = "40d7e4ba7213"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # `comunidade_virtual` e `persona` têm FK cruzada (admin_criador_id e
    # comunidade_virtual_id) — as duas tabelas nascem sem essas colunas
    # referenciarem a outra ainda inexistente, e as FKs entram depois, por
    # ALTER TABLE, quando ambas já existem.
    op.create_table(
        "comunidade_virtual",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("nome", sa.String(length=128), nullable=False),
        sa.Column("localizacao", sa.String(length=256), nullable=False),
        sa.Column("granularidade_maxima", sa.String(length=32), nullable=False),
        sa.Column("admin_criador_id", sa.Uuid(), nullable=True),
        sa.Column(
            "criada_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "persona",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column(
            "papel",
            sa.Enum(
                "admin",
                "mestre",
                "guerreiro",
                "responsavel",
                "apoiador",
                name="papel",
                native_enum=False,
                length=32,
            ),
            nullable=False,
        ),
        sa.Column("comunidade_virtual_id", sa.Uuid(), nullable=True),
        sa.Column("criada_por", sa.Uuid(), nullable=True),
        sa.Column(
            "criada_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "papel != 'guerreiro' OR comunidade_virtual_id IS NOT NULL",
            name="ck_persona_guerreiro_tem_comunidade",
        ),
        sa.ForeignKeyConstraint(["criada_por"], ["persona.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_foreign_key(
        "fk_comunidade_virtual_admin_criador_id_persona",
        "comunidade_virtual",
        "persona",
        ["admin_criador_id"],
        ["id"],
    )
    op.create_foreign_key(
        "fk_persona_comunidade_virtual_id_comunidade_virtual",
        "persona",
        "comunidade_virtual",
        ["comunidade_virtual_id"],
        ["id"],
    )
    op.create_table(
        "credencial",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("persona_id", sa.Uuid(), nullable=False),
        sa.Column(
            "tipo",
            sa.Enum(
                "biometria",
                "login_social",
                "usuario_e_senha",
                name="tipodecredencial",
                native_enum=False,
                length=32,
            ),
            nullable=False,
        ),
        sa.Column("identificador", sa.String(length=256), nullable=False),
        sa.Column("segredo", sa.String(length=512), nullable=True),
        sa.Column("criada_por", sa.Uuid(), nullable=True),
        sa.Column(
            "criada_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("troca_pendente", sa.Boolean(), nullable=False),
        sa.Column("ativa", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["criada_por"], ["persona.id"]),
        sa.ForeignKeyConstraint(["persona_id"], ["persona.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "uq_credencial_identificador_por_tipo_ativa",
        "credencial",
        ["tipo", "identificador"],
        unique=True,
        postgresql_where=sa.text("ativa"),
    )
    op.create_table(
        "sessao",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("persona_id", sa.Uuid(), nullable=False),
        sa.Column("resumo_do_token", sa.String(length=64), nullable=False),
        sa.Column(
            "iniciada_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("expira_em", sa.DateTime(timezone=True), nullable=False),
        sa.Column("origem", sa.String(length=64), nullable=False),
        sa.Column(
            "como_autenticou",
            sa.Enum(
                "biometria",
                "confirmacao_humana",
                "social",
                "credencial",
                name="comoautenticou",
                native_enum=False,
                length=32,
            ),
            nullable=False,
        ),
        sa.Column("quem_confirmou", sa.Uuid(), nullable=True),
        sa.Column("encerrada_em", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["persona_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["quem_confirmou"], ["persona.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("uq_sessao_resumo_do_token", "sessao", ["resumo_do_token"], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("uq_sessao_resumo_do_token", table_name="sessao")
    op.drop_table("sessao")
    op.drop_index(
        "uq_credencial_identificador_por_tipo_ativa",
        table_name="credencial",
        postgresql_where=sa.text("ativa"),
    )
    op.drop_table("credencial")
    op.drop_constraint(
        "fk_persona_comunidade_virtual_id_comunidade_virtual", "persona", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_comunidade_virtual_admin_criador_id_persona",
        "comunidade_virtual",
        type_="foreignkey",
    )
    op.drop_table("persona")
    op.drop_table("comunidade_virtual")
    # ### end Alembic commands ###
