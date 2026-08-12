"""cria nick e acesso_ao_template

Revision ID: 4692973e3186
Revises: df890afdfe89
Create Date: 2026-08-12 10:29:16.490319

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "4692973e3186"
down_revision: str | Sequence[str] | None = "df890afdfe89"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "nick",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("persona_id", sa.Uuid(), nullable=False),
        sa.Column("valor", sa.String(length=64), nullable=False),
        sa.Column(
            "criado_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["persona_id"], ["persona.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("uq_nick_valor", "nick", ["valor"], unique=True)
    op.create_index("uq_nick_persona_id", "nick", ["persona_id"], unique=True)

    op.create_table(
        "acesso_ao_template",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("guerreiro_id", sa.Uuid(), nullable=False),
        sa.Column("acessado_por", sa.Uuid(), nullable=True),
        sa.Column(
            "natureza",
            sa.Enum(
                "gravacao",
                "recadastro",
                "comparacao_de_login",
                name="naturezadoacesso",
                native_enum=False,
                length=32,
            ),
            nullable=False,
        ),
        sa.Column(
            "desfecho",
            sa.Enum(
                "sucesso",
                "recusa",
                name="desfechodoacesso",
                native_enum=False,
                length=16,
            ),
            nullable=False,
        ),
        sa.Column(
            "momento",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["acessado_por"], ["persona.id"]),
        sa.ForeignKeyConstraint(["guerreiro_id"], ["persona.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    # Somente inserção (RN-01-14, design — decisões): o listener de mapeador
    # recusa dentro do ORM, e este trigger recusa também fora dele.
    op.execute(
        """
        CREATE FUNCTION recusar_alteracao_de_acesso_ao_template() RETURNS trigger AS $$
        BEGIN
            RAISE EXCEPTION
                'acesso_ao_template é somente inserção: UPDATE e DELETE não são permitidos';
        END;
        $$ LANGUAGE plpgsql;
        """
    )
    op.execute(
        """
        CREATE TRIGGER trg_acesso_ao_template_somente_insercao
        BEFORE UPDATE OR DELETE ON acesso_ao_template
        FOR EACH ROW EXECUTE FUNCTION recusar_alteracao_de_acesso_ao_template();
        """
    )

    # Cabe o descritor cifrado e codificado, maior que o hash de senha que o
    # limite anterior foi dimensionado para caber (design — decisões).
    op.alter_column(
        "credencial",
        "segredo",
        existing_type=sa.VARCHAR(length=512),
        type_=sa.Text(),
        existing_nullable=True,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "credencial",
        "segredo",
        existing_type=sa.Text(),
        type_=sa.VARCHAR(length=512),
        existing_nullable=True,
    )
    op.execute("DROP TRIGGER trg_acesso_ao_template_somente_insercao ON acesso_ao_template")
    op.execute("DROP FUNCTION recusar_alteracao_de_acesso_ao_template()")
    op.drop_table("acesso_ao_template")
    op.drop_index("uq_nick_persona_id", table_name="nick")
    op.drop_index("uq_nick_valor", table_name="nick")
    op.drop_table("nick")
