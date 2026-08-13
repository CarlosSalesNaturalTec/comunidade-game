"""cria auditoria

Revision ID: 92e50a17f93e
Revises: c47a1e9f5b30
Create Date: 2026-08-13 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "92e50a17f93e"
down_revision: str | Sequence[str] | None = "c47a1e9f5b30"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "auditoria",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("autor_id", sa.Uuid(), nullable=False),
        sa.Column("papel_do_autor", sa.String(length=32), nullable=False),
        sa.Column("acao", sa.String(length=256), nullable=False),
        sa.Column("entidade_afetada", sa.String(length=128), nullable=False),
        sa.Column(
            "momento",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("origem", sa.String(length=64), nullable=False),
        sa.ForeignKeyConstraint(["autor_id"], ["persona.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_auditoria_autor_id", "auditoria", ["autor_id"])
    op.create_index("ix_auditoria_momento", "auditoria", ["momento"])
    # Somente inserção (PRD-01 §8, "Imutabilidade"): o listener de mapeador
    # recusa dentro do ORM, e este trigger recusa também fora dele — script,
    # migração futura ou psql direto.
    op.execute(
        """
        CREATE FUNCTION recusar_alteracao_de_auditoria() RETURNS trigger AS $$
        BEGIN
            RAISE EXCEPTION
                'auditoria é somente inserção: UPDATE e DELETE não são permitidos';
        END;
        $$ LANGUAGE plpgsql;
        """
    )
    op.execute(
        """
        CREATE TRIGGER trg_auditoria_somente_insercao
        BEFORE UPDATE OR DELETE ON auditoria
        FOR EACH ROW EXECUTE FUNCTION recusar_alteracao_de_auditoria();
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TRIGGER trg_auditoria_somente_insercao ON auditoria")
    op.execute("DROP FUNCTION recusar_alteracao_de_auditoria()")
    op.drop_index("ix_auditoria_momento", table_name="auditoria")
    op.drop_index("ix_auditoria_autor_id", table_name="auditoria")
    op.drop_table("auditoria")
