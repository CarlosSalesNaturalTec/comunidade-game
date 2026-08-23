"""cria ocorrencia de conduta

Revision ID: 40a07b5f3ebd
Revises: 5c60068d9f47
Create Date: 2026-08-23 21:52:27.207825

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "40a07b5f3ebd"
down_revision: str | Sequence[str] | None = "5c60068d9f47"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # Somente inserção, no padrão de `lancamento` e `consentimento`:
    # `motivo` anulável para o expurgo futuro sem tocar o lançamento
    # (`RF-09-46`, `RN-01-52`, design — Decisions 3).
    op.create_table(
        "ocorrencia_de_conduta",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("guerreiro_id", sa.Uuid(), nullable=False),
        sa.Column("aula_id", sa.Uuid(), nullable=False),
        sa.Column("atividade_id", sa.Uuid(), nullable=False),
        sa.Column("valor", sa.Integer(), nullable=False),
        sa.Column("motivo", sa.Text(), nullable=True),
        sa.Column("momento_do_fato", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "momento_do_registro",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
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
        sa.ForeignKeyConstraint(["atividade_id"], ["atividade.id"]),
        sa.ForeignKeyConstraint(["aula_id"], ["aula.id"]),
        sa.ForeignKeyConstraint(["autor_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["guerreiro_id"], ["persona.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.execute(
        """
        CREATE FUNCTION recusar_alteracao_de_ocorrencia_de_conduta() RETURNS trigger AS $$
        BEGIN
            RAISE EXCEPTION
                'ocorrencia_de_conduta é somente inserção: UPDATE e DELETE não são permitidos';
        END;
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER trg_ocorrencia_de_conduta_somente_insercao
        BEFORE UPDATE OR DELETE ON ocorrencia_de_conduta
        FOR EACH ROW EXECUTE FUNCTION recusar_alteracao_de_ocorrencia_de_conduta();
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        """
        DROP TRIGGER trg_ocorrencia_de_conduta_somente_insercao ON ocorrencia_de_conduta;
        DROP FUNCTION recusar_alteracao_de_ocorrencia_de_conduta();
        """
    )
    op.drop_table("ocorrencia_de_conduta")
