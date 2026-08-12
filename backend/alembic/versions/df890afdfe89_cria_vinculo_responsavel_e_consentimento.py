"""cria vinculo_responsavel e consentimento

Revision ID: df890afdfe89
Revises: 06d3d81b962a
Create Date: 2026-08-12 01:35:29.468585

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "df890afdfe89"
down_revision: str | Sequence[str] | None = "06d3d81b962a"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "consentimento",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("responsavel_id", sa.Uuid(), nullable=False),
        sa.Column("guerreiro_id", sa.Uuid(), nullable=False),
        sa.Column("tipo", sa.String(length=64), nullable=False),
        sa.Column("versao_do_termo", sa.String(length=32), nullable=False),
        sa.Column(
            "decisao",
            sa.Enum(
                "concede",
                "nega",
                name="decisaodeconsentimento",
                native_enum=False,
                length=16,
            ),
            nullable=False,
        ),
        sa.Column(
            "origem",
            sa.Enum(
                "propria",
                "assistida",
                "impressa",
                name="origemdoconsentimento",
                native_enum=False,
                length=16,
            ),
            nullable=False,
        ),
        sa.Column("testemunha_id", sa.Uuid(), nullable=True),
        sa.Column("anexo", sa.String(length=512), nullable=True),
        sa.Column("autor_id", sa.Uuid(), nullable=False),
        sa.Column("papel_do_autor", sa.String(length=32), nullable=False),
        sa.Column(
            "registrado_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["autor_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["guerreiro_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["responsavel_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["testemunha_id"], ["persona.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    # Somente inserção (RN-01-12, design — decisões): o listener de mapeador
    # recusa dentro do ORM, e este trigger recusa também fora dele — script,
    # migração futura ou psql direto.
    op.execute(
        """
        CREATE FUNCTION recusar_alteracao_de_consentimento() RETURNS trigger AS $$
        BEGIN
            RAISE EXCEPTION
                'consentimento é somente inserção: UPDATE e DELETE não são permitidos';
        END;
        $$ LANGUAGE plpgsql;
        """
    )
    op.execute(
        """
        CREATE TRIGGER trg_consentimento_somente_insercao
        BEFORE UPDATE OR DELETE ON consentimento
        FOR EACH ROW EXECUTE FUNCTION recusar_alteracao_de_consentimento();
        """
    )
    op.create_table(
        "vinculo_responsavel",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("responsavel_id", sa.Uuid(), nullable=False),
        sa.Column("guerreiro_id", sa.Uuid(), nullable=False),
        sa.Column("grau_de_parentesco", sa.String(length=64), nullable=False),
        sa.Column(
            "inicio",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("fim", sa.DateTime(timezone=True), nullable=True),
        sa.Column("autor_id", sa.Uuid(), nullable=False),
        sa.Column("papel_do_autor", sa.String(length=32), nullable=False),
        sa.Column(
            "registrado_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["autor_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["guerreiro_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["responsavel_id"], ["persona.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("vinculo_responsavel")
    op.execute("DROP TRIGGER trg_consentimento_somente_insercao ON consentimento")
    op.execute("DROP FUNCTION recusar_alteracao_de_consentimento()")
    op.drop_table("consentimento")
