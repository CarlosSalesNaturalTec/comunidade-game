"""cria termo, leitura_de_termo e acesso_ao_dado_do_guerreiro

Revision ID: d3e4f5a6b7c8
Revises: c7d8e9f0a1b2
Create Date: 2026-09-01 00:00:00.000001

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d3e4f5a6b7c8"
down_revision: str | Sequence[str] | None = "c7d8e9f0a1b2"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "termo",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column(
            "tipo",
            sa.Enum(
                "autorizacao_de_divulgacao",
                "biometria",
                name="tipodeconsentimento",
                native_enum=False,
                length=64,
            ),
            nullable=False,
        ),
        sa.Column("versao", sa.String(length=32), nullable=False),
        sa.Column("texto", sa.Text(), nullable=False),
        sa.Column("vigente_desde", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "criado_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("tipo", "versao", name="uq_termo_tipo_versao"),
    )
    op.create_index("ix_termo_tipo_vigente_desde", "termo", ["tipo", "vigente_desde"])

    op.create_table(
        "leitura_de_termo",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("responsavel_id", sa.Uuid(), nullable=False),
        sa.Column("versao", sa.String(length=32), nullable=False),
        sa.Column(
            "lida_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["responsavel_id"], ["persona.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "responsavel_id", "versao", name="uq_leitura_de_termo_responsavel_versao"
        ),
    )

    op.create_table(
        "acesso_ao_dado_do_guerreiro",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("auditoria_id", sa.Uuid(), nullable=False),
        sa.Column("guerreiro_id", sa.Uuid(), nullable=False),
        sa.Column(
            "momento",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["auditoria_id"], ["auditoria.id"]),
        sa.ForeignKeyConstraint(["guerreiro_id"], ["persona.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_acesso_ao_dado_do_guerreiro_guerreiro_id",
        "acesso_ao_dado_do_guerreiro",
        ["guerreiro_id"],
    )
    op.create_index(
        "ix_acesso_ao_dado_do_guerreiro_momento", "acesso_ao_dado_do_guerreiro", ["momento"]
    )
    # Somente inserção (design.md — decisão 1, mesmo padrão de `auditoria`):
    # o listener de mapeador recusa dentro do ORM, e este trigger recusa
    # também fora dele.
    op.execute(
        """
        CREATE FUNCTION recusar_alteracao_de_acesso_ao_dado_do_guerreiro() RETURNS trigger AS $$
        BEGIN
            RAISE EXCEPTION
                'acesso_ao_dado_do_guerreiro é somente inserção: sem UPDATE nem DELETE';
        END;
        $$ LANGUAGE plpgsql;
        """
    )
    op.execute(
        """
        CREATE TRIGGER trg_acesso_ao_dado_do_guerreiro_somente_insercao
        BEFORE UPDATE OR DELETE ON acesso_ao_dado_do_guerreiro
        FOR EACH ROW EXECUTE FUNCTION recusar_alteracao_de_acesso_ao_dado_do_guerreiro();
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        "DROP TRIGGER trg_acesso_ao_dado_do_guerreiro_somente_insercao "
        "ON acesso_ao_dado_do_guerreiro"
    )
    op.execute("DROP FUNCTION recusar_alteracao_de_acesso_ao_dado_do_guerreiro()")
    op.drop_index(
        "ix_acesso_ao_dado_do_guerreiro_momento", table_name="acesso_ao_dado_do_guerreiro"
    )
    op.drop_index(
        "ix_acesso_ao_dado_do_guerreiro_guerreiro_id", table_name="acesso_ao_dado_do_guerreiro"
    )
    op.drop_table("acesso_ao_dado_do_guerreiro")
    op.drop_table("leitura_de_termo")
    op.drop_index("ix_termo_tipo_vigente_desde", table_name="termo")
    op.drop_table("termo")
