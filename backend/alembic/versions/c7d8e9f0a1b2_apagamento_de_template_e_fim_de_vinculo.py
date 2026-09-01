"""apagamento de template e fim de vinculo

Revision ID: c7d8e9f0a1b2
Revises: ed3658419470
Create Date: 2026-09-01 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c7d8e9f0a1b2"
down_revision: str | Sequence[str] | None = "ed3658419470"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "apagamento_de_template",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("guerreiro_id", sa.Uuid(), nullable=False),
        sa.Column(
            "gatilho",
            sa.Enum(
                "exclusao_deferida",
                "recusa_biometria",
                "fim_do_vinculo",
                name="gatilhodeapagamento",
                native_enum=False,
                length=32,
            ),
            nullable=False,
        ),
        sa.Column("apagar_em", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "criado_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["guerreiro_id"], ["persona.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("guerreiro_id", name="uq_apagamento_de_template_guerreiro_id"),
    )

    op.create_table(
        "fim_de_vinculo",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("guerreiro_id", sa.Uuid(), nullable=False),
        sa.Column(
            "origem",
            sa.Enum(
                "admin",
                "varredura",
                name="origemdofimdevinculo",
                native_enum=False,
                length=16,
            ),
            nullable=False,
        ),
        sa.Column("encerrado_por", sa.Uuid(), nullable=True),
        sa.Column("motivo", sa.Text(), nullable=False),
        sa.Column(
            "momento",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["encerrado_por"], ["persona.id"]),
        sa.ForeignKeyConstraint(["guerreiro_id"], ["persona.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("guerreiro_id", name="uq_fim_de_vinculo_guerreiro_id"),
    )
    # Somente inserção (design — decisão 3): o listener de mapeador recusa
    # dentro do ORM, e este trigger recusa também fora dele.
    op.execute(
        """
        CREATE FUNCTION recusar_alteracao_de_fim_de_vinculo() RETURNS trigger AS $$
        BEGIN
            RAISE EXCEPTION
                'fim_de_vinculo é somente inserção: UPDATE e DELETE não são permitidos';
        END;
        $$ LANGUAGE plpgsql;
        """
    )
    op.execute(
        """
        CREATE TRIGGER trg_fim_de_vinculo_somente_insercao
        BEFORE UPDATE OR DELETE ON fim_de_vinculo
        FOR EACH ROW EXECUTE FUNCTION recusar_alteracao_de_fim_de_vinculo();
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TRIGGER trg_fim_de_vinculo_somente_insercao ON fim_de_vinculo")
    op.execute("DROP FUNCTION recusar_alteracao_de_fim_de_vinculo()")
    op.drop_table("fim_de_vinculo")
    op.drop_table("apagamento_de_template")
