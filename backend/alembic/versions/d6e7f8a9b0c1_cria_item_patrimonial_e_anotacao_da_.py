"""cria item patrimonial e anotacao da ficha de vida

Revision ID: d6e7f8a9b0c1
Revises: c4d5e6f7a8b9
Create Date: 2026-08-19 02:30:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d6e7f8a9b0c1"
down_revision: str | Sequence[str] | None = "c4d5e6f7a8b9"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # O exemplar permanente tombado num ponto de apoio — o responsável não é
    # coluna aqui, deriva de `PontoDeApoio.responsavel_id` por junção
    # (`RF-07-11`, `RN-07-10`, design — Decisions 4).
    op.create_table(
        "item_patrimonial",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("aporte_de_origem_id", sa.Uuid(), nullable=True),
        sa.Column("titulo", sa.String(length=256), nullable=False),
        sa.Column("numero_de_tombo", sa.String(length=64), nullable=False),
        sa.Column("ponto_de_apoio_id", sa.Uuid(), nullable=False),
        sa.Column("estado_de_conservacao", sa.String(length=128), nullable=False),
        sa.Column("autor_id", sa.Uuid(), nullable=False),
        sa.Column("papel_do_autor", sa.String(length=32), nullable=False),
        sa.Column(
            "registrado_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["aporte_de_origem_id"], ["aporte.id"]),
        sa.ForeignKeyConstraint(["autor_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["ponto_de_apoio_id"], ["ponto_de_apoio.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "ponto_de_apoio_id",
            "numero_de_tombo",
            name="uq_item_patrimonial_ponto_de_apoio_numero_de_tombo",
        ),
    )
    op.create_index(
        "ix_item_patrimonial_ponto_de_apoio_id", "item_patrimonial", ["ponto_de_apoio_id"]
    )

    # A ficha de vida — histórico de somente inserção, no mesmo padrão de
    # `lancamento` e `auditoria` (`RF-07-11`, `RF-07-48`, design — Decisions
    # 2, Migration Plan).
    op.create_table(
        "anotacao_da_ficha_de_vida",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("item_patrimonial_id", sa.Uuid(), nullable=False),
        sa.Column(
            "teor",
            sa.Enum(
                "cuidado", "perda", "dano", name="teordaanotacao", native_enum=False, length=16
            ),
            nullable=False,
        ),
        sa.Column("estado_de_conservacao", sa.String(length=128), nullable=False),
        sa.Column("autor_id", sa.Uuid(), nullable=False),
        sa.Column("papel_do_autor", sa.String(length=32), nullable=False),
        sa.Column(
            "registrado_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["autor_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["item_patrimonial_id"], ["item_patrimonial.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_anotacao_da_ficha_de_vida_item_patrimonial_id",
        "anotacao_da_ficha_de_vida",
        ["item_patrimonial_id"],
    )
    op.execute(
        """
        CREATE FUNCTION recusar_alteracao_de_anotacao_da_ficha_de_vida() RETURNS trigger AS $$
        BEGIN
            RAISE EXCEPTION
                'anotação da ficha de vida é somente inserção: UPDATE e DELETE não são permitidos';
        END;
        $$ LANGUAGE plpgsql;
        """
    )
    op.execute(
        """
        CREATE TRIGGER trg_anotacao_da_ficha_de_vida_somente_insercao
        BEFORE UPDATE OR DELETE ON anotacao_da_ficha_de_vida
        FOR EACH ROW EXECUTE FUNCTION recusar_alteracao_de_anotacao_da_ficha_de_vida();
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        "DROP TRIGGER trg_anotacao_da_ficha_de_vida_somente_insercao ON anotacao_da_ficha_de_vida"
    )
    op.execute("DROP FUNCTION recusar_alteracao_de_anotacao_da_ficha_de_vida()")
    op.drop_index(
        "ix_anotacao_da_ficha_de_vida_item_patrimonial_id",
        table_name="anotacao_da_ficha_de_vida",
    )
    op.drop_table("anotacao_da_ficha_de_vida")
    op.drop_index("ix_item_patrimonial_ponto_de_apoio_id", table_name="item_patrimonial")
    op.drop_table("item_patrimonial")
