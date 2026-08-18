"""cria preco_de_referencia e item_de_catalogo_avulso

Revision ID: a2b3c4d5e6f7
Revises: f1a2b3c4d5e6
Create Date: 2026-08-18 21:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a2b3c4d5e6f7"
down_revision: str | Sequence[str] | None = "f1a2b3c4d5e6"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # A segunda régua do tipo de recurso, irmã de `valor_de_referencia` —
    # mesma vigência semiaberta, nunca deriva nem altera o valor em moedas
    # (`RF-07-42`, `RF-07-43`, `RN-07-24`, `RN-07-25`). Inteiro, sem casas
    # decimais, e com o piso de 20 reforçado como `CHECK` (`RF-07-44`,
    # `RN-07-30`).
    op.create_table(
        "preco_de_referencia",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("tipo_de_recurso_id", sa.Uuid(), nullable=False),
        sa.Column("preco_em_pontos_extras", sa.Integer(), nullable=False),
        sa.Column("vigencia_inicio", sa.Date(), nullable=False),
        sa.Column("vigencia_fim", sa.Date(), nullable=True),
        sa.Column("autor_id", sa.Uuid(), nullable=False),
        sa.Column("papel_do_autor", sa.String(length=32), nullable=False),
        sa.Column(
            "registrado_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "preco_em_pontos_extras >= 20", name="ck_preco_de_referencia_piso_minimo"
        ),
        sa.CheckConstraint(
            "vigencia_fim IS NULL OR vigencia_fim >= vigencia_inicio",
            name="ck_preco_de_referencia_fim_apos_ou_igual_ao_inicio",
        ),
        sa.ForeignKeyConstraint(["autor_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["tipo_de_recurso_id"], ["tipo_de_recurso.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    # O item do catálogo avulso: não tem preço próprio — o preço é sempre o
    # da vigência corrente de `preco_de_referencia` do seu tipo de recurso
    # (`RF-07-33`, `RF-07-45`, `RN-07-29`). `ponto_de_apoio_id` é decisão
    # nova desta fatia (documento 04 §1): o saldo que lastreia o item é por
    # tipo e ponto de apoio. `ativo` nasce falso e só passa a verdadeiro
    # quando homologação, preço vigente e lastro convergem (`RF-07-34`,
    # `RN-07-26`).
    op.create_table(
        "item_de_catalogo_avulso",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("nome", sa.String(length=128), nullable=False),
        sa.Column("tipo_de_recurso_id", sa.Uuid(), nullable=False),
        sa.Column("estoque", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("comunidade_virtual_id", sa.Uuid(), nullable=False),
        sa.Column("ponto_de_apoio_id", sa.Uuid(), nullable=False),
        sa.Column(
            "origem_do_cadastro",
            sa.Enum(
                "mestre",
                "apoiador",
                name="origemdocadastrodoitem",
                native_enum=False,
                length=16,
            ),
            nullable=False,
        ),
        sa.Column(
            "situacao_de_homologacao",
            sa.Enum(
                "nao_se_aplica",
                "pendente",
                "homologado",
                "recusado",
                name="situacaodehomologacao",
                native_enum=False,
                length=16,
            ),
            nullable=False,
        ),
        sa.Column("homologacao_motivo", sa.Text(), nullable=True),
        sa.Column("ativo", sa.Boolean(), nullable=False),
        sa.Column("autor_id", sa.Uuid(), nullable=False),
        sa.Column("papel_do_autor", sa.String(length=32), nullable=False),
        sa.Column(
            "registrado_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint("estoque >= 1", name="ck_item_de_catalogo_avulso_estoque_minimo"),
        sa.ForeignKeyConstraint(["autor_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["comunidade_virtual_id"], ["comunidade_virtual.id"]),
        sa.ForeignKeyConstraint(["ponto_de_apoio_id"], ["ponto_de_apoio.id"]),
        sa.ForeignKeyConstraint(["tipo_de_recurso_id"], ["tipo_de_recurso.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("item_de_catalogo_avulso")
    op.drop_table("preco_de_referencia")
