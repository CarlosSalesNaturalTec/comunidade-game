"""histórico de pontuação: lançamento por movimento e linha de saldo anterior

Decisão do fundador de 2026-11-13 (documento 09 §1, documento 11 §5).

Nasce `lancamento_de_pontuacao`, somente inserção, recusada por gatilho
(`RF-01-88`, `RN-01-67`). Cada conta já existente — cada `ponto_regular` por
trilha ou poder e cada `ponto_extra` — ganha a linha de **saldo anterior**,
com o total desta data, contas zeradas inclusive; o passado não se
reconstrói (`RF-01-90`, design — decisão 5).

Revision ID: a3c5e7f9b1d2
Revises: 12b4e8984d37
Create Date: 2026-11-13 12:00:00

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "a3c5e7f9b1d2"
down_revision: str | Sequence[str] | None = "12b4e8984d37"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "lancamento_de_pontuacao",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("guerreiro_id", sa.Uuid(), nullable=False),
        sa.Column("conta", sa.String(length=16), nullable=False),
        sa.Column("trilha_id", sa.Uuid(), nullable=True),
        sa.Column("poder_id", sa.Uuid(), nullable=True),
        sa.Column("origem", sa.String(length=32), nullable=False),
        sa.Column("referencia_id", sa.Uuid(), nullable=True),
        sa.Column("detalhe", sa.String(length=256), nullable=True),
        sa.Column("valor", sa.Integer(), nullable=False),
        sa.Column("valor_no_acumulado", sa.Integer(), nullable=True),
        sa.Column(
            "registrado_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "(conta = 'regular' AND (trilha_id IS NOT NULL) != (poder_id IS NOT NULL)"
            " AND valor_no_acumulado IS NULL)"
            " OR (conta = 'extra' AND trilha_id IS NULL AND poder_id IS NULL"
            " AND valor_no_acumulado IS NOT NULL)",
            name="ck_lancamento_de_pontuacao_conta",
        ),
        sa.ForeignKeyConstraint(["guerreiro_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["trilha_id"], ["trilha.id"]),
        sa.ForeignKeyConstraint(["poder_id"], ["poder.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_lancamento_de_pontuacao_guerreiro_registrado_em",
        "lancamento_de_pontuacao",
        ["guerreiro_id", "registrado_em", "id"],
    )

    op.execute(
        """
        INSERT INTO lancamento_de_pontuacao
            (id, guerreiro_id, conta, trilha_id, poder_id, origem, valor)
        SELECT gen_random_uuid(), guerreiro_id, 'regular', trilha_id, poder_id,
               'saldo_anterior', total
        FROM ponto_regular
        """
    )
    op.execute(
        """
        INSERT INTO lancamento_de_pontuacao
            (id, guerreiro_id, conta, origem, valor, valor_no_acumulado)
        SELECT gen_random_uuid(), guerreiro_id, 'extra', 'saldo_anterior',
               saldo_disponivel, acumulado
        FROM ponto_extra
        """
    )

    op.execute(
        """
        CREATE FUNCTION recusar_alteracao_de_lancamento_de_pontuacao() RETURNS trigger AS $$
        BEGIN
            RAISE EXCEPTION 'lançamento de pontuação é somente inserção';
        END;
        $$ LANGUAGE plpgsql;
        CREATE TRIGGER trg_lancamento_de_pontuacao_somente_insercao
        BEFORE UPDATE OR DELETE ON lancamento_de_pontuacao
        FOR EACH ROW EXECUTE FUNCTION recusar_alteracao_de_lancamento_de_pontuacao();
        """
    )


def downgrade() -> None:
    op.execute(
        """
        DROP TRIGGER trg_lancamento_de_pontuacao_somente_insercao ON lancamento_de_pontuacao;
        DROP FUNCTION recusar_alteracao_de_lancamento_de_pontuacao();
        """
    )
    op.drop_index(
        "ix_lancamento_de_pontuacao_guerreiro_registrado_em",
        table_name="lancamento_de_pontuacao",
    )
    op.drop_table("lancamento_de_pontuacao")
