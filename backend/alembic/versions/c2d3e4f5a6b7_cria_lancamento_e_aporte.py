"""cria lancamento e aporte; tipo_de_recurso ganha exige_comprovante

Revision ID: c2d3e4f5a6b7
Revises: b8c9d0e1f2a3
Create Date: 2026-08-18 10:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c2d3e4f5a6b7"
down_revision: str | Sequence[str] | None = "b8c9d0e1f2a3"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # Coluna nova, com `server_default` falso: nenhum tipo já cadastrado
    # passa a exigir comprovante de surpresa (`RN-07-22`, design — Migration
    # Plan).
    op.add_column(
        "tipo_de_recurso",
        sa.Column("exige_comprovante", sa.Boolean(), nullable=False, server_default=sa.false()),
    )

    # A unidade do livro-razão: somente inserção, com o mesmo par de
    # gatilhos de `consentimento` (`RF-07-19`, `RN-07-15`, design —
    # Decisions 3). `lancamento_original_id` e `motivo_do_ajuste` só se
    # preenchem no lançamento de natureza `ajuste`.
    op.create_table(
        "lancamento",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column(
            "natureza",
            sa.Enum(
                "credito",
                "debito",
                "ajuste",
                name="naturezadolancamento",
                native_enum=False,
                length=16,
            ),
            nullable=False,
        ),
        sa.Column("tipo_de_recurso_id", sa.Uuid(), nullable=False),
        sa.Column("ponto_de_apoio_id", sa.Uuid(), nullable=False),
        sa.Column("quantidade", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("valor_em_moedas", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("lancamento_original_id", sa.Uuid(), nullable=True),
        sa.Column("motivo_do_ajuste", sa.Text(), nullable=True),
        sa.Column("autor_id", sa.Uuid(), nullable=False),
        sa.Column("papel_do_autor", sa.String(length=32), nullable=False),
        sa.Column(
            "registrado_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["autor_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["lancamento_original_id"], ["lancamento.id"]),
        sa.ForeignKeyConstraint(["ponto_de_apoio_id"], ["ponto_de_apoio.id"]),
        sa.ForeignKeyConstraint(["tipo_de_recurso_id"], ["tipo_de_recurso.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_lancamento_tipo_de_recurso_ponto_de_apoio",
        "lancamento",
        ["tipo_de_recurso_id", "ponto_de_apoio_id"],
    )
    op.execute(
        """
        CREATE FUNCTION recusar_alteracao_de_lancamento() RETURNS trigger AS $$
        BEGIN
            RAISE EXCEPTION
                'lancamento é somente inserção: UPDATE e DELETE não são permitidos';
        END;
        $$ LANGUAGE plpgsql;
        """
    )
    op.execute(
        """
        CREATE TRIGGER trg_lancamento_somente_insercao
        BEFORE UPDATE OR DELETE ON lancamento
        FOR EACH ROW EXECUTE FUNCTION recusar_alteracao_de_lancamento();
        """
    )

    # O registro do que entra, valorado em moedas pela vigência na data do
    # aporte (`RF-07-04`, `RF-07-05`, PRD-07 §8). A unicidade de
    # `solicitacao_de_participacao_id` impede a mesma declaração do
    # pré-cadastro creditar duas vezes (`RN-07-21`, design — Decisions 10).
    op.create_table(
        "aporte",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("provedor_id", sa.Uuid(), nullable=False),
        sa.Column("tipo_de_recurso_id", sa.Uuid(), nullable=False),
        sa.Column("quantidade", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("ponto_de_apoio_id", sa.Uuid(), nullable=False),
        sa.Column("valor_em_moedas", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("valor_de_origem", sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column(
            "forma",
            sa.Enum(
                "financeira",
                "material",
                "servico",
                "absorcao",
                name="formadeaporte",
                native_enum=False,
                length=16,
            ),
            nullable=False,
        ),
        sa.Column(
            "origem_do_registro",
            sa.Enum(
                "gestao",
                "pre_cadastro",
                name="origemdoregistro",
                native_enum=False,
                length=16,
            ),
            nullable=False,
        ),
        sa.Column("solicitacao_de_participacao_id", sa.Uuid(), nullable=True),
        sa.Column("ressarcivel", sa.Boolean(), nullable=False),
        sa.Column(
            "situacao_de_ressarcimento",
            sa.Enum(
                "nao_se_aplica",
                "em_aberto",
                "ressarcido",
                name="situacaoderessarcimento",
                native_enum=False,
                length=16,
            ),
            nullable=False,
        ),
        sa.Column("periodo_apurado", sa.Date(), nullable=True),
        sa.Column("comprovante_referencia", sa.String(length=512), nullable=True),
        sa.Column("comprovante_nome_original", sa.String(length=256), nullable=True),
        sa.Column("comprovante_tipo", sa.String(length=128), nullable=True),
        sa.Column("comprovante_tamanho", sa.Integer(), nullable=True),
        sa.Column("admin_homologador_id", sa.Uuid(), nullable=True),
        sa.Column("lancamento_id", sa.Uuid(), nullable=False),
        sa.Column("data_do_aporte", sa.Date(), nullable=False),
        sa.Column("autor_id", sa.Uuid(), nullable=False),
        sa.Column("papel_do_autor", sa.String(length=32), nullable=False),
        sa.Column(
            "registrado_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["admin_homologador_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["autor_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["lancamento_id"], ["lancamento.id"]),
        sa.ForeignKeyConstraint(["ponto_de_apoio_id"], ["ponto_de_apoio.id"]),
        sa.ForeignKeyConstraint(["provedor_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(
            ["solicitacao_de_participacao_id"], ["solicitacao_de_participacao.id"]
        ),
        sa.ForeignKeyConstraint(["tipo_de_recurso_id"], ["tipo_de_recurso.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "solicitacao_de_participacao_id", name="uq_aporte_solicitacao_de_participacao_id"
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("aporte")
    op.execute("DROP TRIGGER trg_lancamento_somente_insercao ON lancamento")
    op.execute("DROP FUNCTION recusar_alteracao_de_lancamento()")
    op.drop_index("ix_lancamento_tipo_de_recurso_ponto_de_apoio", table_name="lancamento")
    op.drop_table("lancamento")
    op.drop_column("tipo_de_recurso", "exige_comprovante")
