"""cria conclusao_de_desafio_extra

Revision ID: b1fabae4dbda
Revises: 02239f525269
Create Date: 2026-09-02 01:38:58.344301

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b1fabae4dbda"
down_revision: str | Sequence[str] | None = "02239f525269"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # O registro da conclusão de um DesafioExtra por um Guerreiro(a) — só a
    # entidade e a leitura nesta fatia; o ato de registrá-la é do PRD-09,
    # ainda sem fatia (`RF-14-42`, `RF-14-37`, design — Context, decisão 1).
    op.create_table(
        "conclusao_de_desafio_extra",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("desafio_id", sa.Uuid(), nullable=False),
        sa.Column("guerreiro_id", sa.Uuid(), nullable=False),
        sa.Column("recompensa_entregue", sa.Boolean(), nullable=False),
        sa.Column("pontos_extras_creditados", sa.Integer(), nullable=False),
        sa.Column("momento_do_fato", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "momento_do_registro",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["desafio_id"], ["desafio_extra.id"]),
        sa.ForeignKeyConstraint(["guerreiro_id"], ["persona.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "desafio_id", "guerreiro_id", name="uq_conclusao_de_desafio_extra_desafio_guerreiro"
        ),
    )
    # Somente inserção (design — decisão 2): o listener de mapeador recusa
    # dentro do ORM, e este trigger recusa também fora dele — script,
    # migração futura ou psql direto.
    op.execute(
        """
        CREATE FUNCTION recusar_alteracao_de_conclusao_de_desafio_extra() RETURNS trigger AS $$
        BEGIN
            RAISE EXCEPTION
                'conclusão de desafio extra é somente inserção: '
                'UPDATE e DELETE não são permitidos';
        END;
        $$ LANGUAGE plpgsql;
        """
    )
    op.execute(
        """
        CREATE TRIGGER trg_conclusao_de_desafio_extra_somente_insercao
        BEFORE UPDATE OR DELETE ON conclusao_de_desafio_extra
        FOR EACH ROW EXECUTE FUNCTION recusar_alteracao_de_conclusao_de_desafio_extra();
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        "DROP TRIGGER trg_conclusao_de_desafio_extra_somente_insercao ON conclusao_de_desafio_extra"
    )
    op.execute("DROP FUNCTION recusar_alteracao_de_conclusao_de_desafio_extra()")
    op.drop_table("conclusao_de_desafio_extra")
