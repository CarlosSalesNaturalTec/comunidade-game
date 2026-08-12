"""cria resultado, ponto_regular, nivel, badge e ponto_extra

Revision ID: 215dc282710b
Revises: fdfe17ea361e
Create Date: 2026-08-12 15:38:54.061666

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "215dc282710b"
down_revision: str | Sequence[str] | None = "fdfe17ea361e"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "resultado",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("guerreiro_id", sa.Uuid(), nullable=False),
        sa.Column("atividade_id", sa.Uuid(), nullable=False),
        sa.Column("producao", sa.Text(), nullable=False),
        sa.Column(
            "desfecho",
            sa.Enum(
                "realizada",
                "realizada_com_merito",
                "merito_extra_por_auxilio",
                name="desfechodoresultado",
                native_enum=False,
                length=32,
            ),
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
        sa.Column("momento_do_fato", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "momento_do_registro",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["atividade_id"], ["atividade.id"]),
        sa.ForeignKeyConstraint(["autor_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["guerreiro_id"], ["persona.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "ponto_regular",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("guerreiro_id", sa.Uuid(), nullable=False),
        sa.Column("trilha_id", sa.Uuid(), nullable=False),
        sa.Column("total", sa.Integer(), nullable=False),
        sa.CheckConstraint("total >= 0", name="ck_ponto_regular_total_nao_negativo"),
        sa.ForeignKeyConstraint(["guerreiro_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["trilha_id"], ["trilha.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "guerreiro_id", "trilha_id", name="uq_ponto_regular_guerreiro_id_trilha_id"
        ),
    )
    # Nunca debitado, em nenhuma operação (RF-01-57, RN-01-38): o listener de
    # mapeador recusa dentro do ORM, e este gatilho recusa também fora dele —
    # script, migração futura ou psql direto (mesmo padrão de RN-01-12).
    op.execute(
        """
        CREATE FUNCTION recusar_debito_de_ponto_regular() RETURNS trigger AS $$
        BEGIN
            IF (TG_OP = 'DELETE') THEN
                RAISE EXCEPTION
                    'ponto regular nunca é debitado: DELETE não é permitido';
            END IF;
            IF NEW.total < OLD.total THEN
                RAISE EXCEPTION
                    'ponto regular nunca é debitado: total não pode diminuir';
            END IF;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        """
    )
    op.execute(
        """
        CREATE TRIGGER trg_ponto_regular_nunca_debita
        BEFORE UPDATE OR DELETE ON ponto_regular
        FOR EACH ROW EXECUTE FUNCTION recusar_debito_de_ponto_regular();
        """
    )

    op.create_table(
        "nivel",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("guerreiro_id", sa.Uuid(), nullable=False),
        sa.Column("trilha_id", sa.Uuid(), nullable=False),
        sa.Column("valor", sa.Integer(), nullable=False),
        sa.Column(
            "certificado_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["guerreiro_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["trilha_id"], ["trilha.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "guerreiro_id",
            "trilha_id",
            "valor",
            name="uq_nivel_guerreiro_id_trilha_id_valor",
        ),
    )

    op.create_table(
        "badge",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("guerreiro_id", sa.Uuid(), nullable=False),
        sa.Column("trilha_id", sa.Uuid(), nullable=True),
        sa.Column("poder_id", sa.Uuid(), nullable=True),
        sa.Column(
            "tipo",
            sa.Enum(
                "de_nivel",
                "de_valores_e_causas",
                name="tipodebadge",
                native_enum=False,
                length=32,
            ),
            nullable=False,
        ),
        sa.Column(
            "certificado_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "(trilha_id IS NOT NULL) != (poder_id IS NOT NULL)",
            name="ck_badge_trilha_ou_poder",
        ),
        sa.ForeignKeyConstraint(["guerreiro_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["poder_id"], ["poder.id"]),
        sa.ForeignKeyConstraint(["trilha_id"], ["trilha.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "ponto_extra",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("guerreiro_id", sa.Uuid(), nullable=False),
        sa.Column("acumulado", sa.Integer(), nullable=False),
        sa.Column("saldo_disponivel", sa.Integer(), nullable=False),
        sa.CheckConstraint("acumulado >= 0", name="ck_ponto_extra_acumulado_nao_negativo"),
        sa.CheckConstraint("saldo_disponivel >= 0", name="ck_ponto_extra_saldo_nao_negativo"),
        sa.ForeignKeyConstraint(["guerreiro_id"], ["persona.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("guerreiro_id"),
    )
    # O acumulado só cresce (RN-01-39, RN-01-40); o saldo nunca negativo já é
    # a CheckConstraint acima, válida em qualquer via.
    op.execute(
        """
        CREATE FUNCTION recusar_debito_de_ponto_extra() RETURNS trigger AS $$
        BEGIN
            IF (TG_OP = 'DELETE') THEN
                RAISE EXCEPTION
                    'ponto extra nunca é debitado nesta fatia: DELETE não é permitido';
            END IF;
            IF NEW.acumulado < OLD.acumulado THEN
                RAISE EXCEPTION
                    'o acumulado de ponto extra só cresce: não pode diminuir';
            END IF;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        """
    )
    op.execute(
        """
        CREATE TRIGGER trg_ponto_extra_acumulado_so_cresce
        BEFORE UPDATE OR DELETE ON ponto_extra
        FOR EACH ROW EXECUTE FUNCTION recusar_debito_de_ponto_extra();
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TRIGGER trg_ponto_extra_acumulado_so_cresce ON ponto_extra")
    op.execute("DROP FUNCTION recusar_debito_de_ponto_extra()")
    op.drop_table("ponto_extra")
    op.drop_table("badge")
    op.drop_table("nivel")
    op.execute("DROP TRIGGER trg_ponto_regular_nunca_debita ON ponto_regular")
    op.execute("DROP FUNCTION recusar_debito_de_ponto_regular()")
    op.drop_table("ponto_regular")
    op.drop_table("resultado")
