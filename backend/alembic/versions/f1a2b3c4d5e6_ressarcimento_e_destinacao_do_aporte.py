"""ressarcimento e destinação do aporte

Revision ID: f1a2b3c4d5e6
Revises: e017b352da40
Create Date: 2026-08-18 20:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f1a2b3c4d5e6"
down_revision: str | Sequence[str] | None = "e017b352da40"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # A destinação separa o que vira lastro do que não vira (`RF-07-23`,
    # `RN-07-38`, design — Decisions 2, 5). `server_default` "lastro" é
    # verdade para todo aporte e todo lançamento já gravados: nenhum aporte
    # de destinação ressarcimento existe antes desta fatia.
    op.add_column(
        "lancamento",
        sa.Column(
            "destinacao",
            sa.Enum(
                "lastro", "ressarcimento", name="destinacaodoaporte", native_enum=False, length=16
            ),
            nullable=False,
            server_default="lastro",
        ),
    )
    op.add_column(
        "aporte",
        sa.Column(
            "destinacao",
            sa.Enum(
                "lastro", "ressarcimento", name="destinacaodoaporte", native_enum=False, length=16
            ),
            nullable=False,
            server_default="lastro",
        ),
    )

    # A absorção assumida a partir da necessidade publicada declara qual
    # aula atende (`RF-07-28`, design — Decisions 5). Anulável: absorção
    # gravada antes desta fatia não declarou necessidade e não há como
    # inferi-la.
    op.add_column("aporte", sa.Column("aula_id", sa.Uuid(), nullable=True))
    op.create_foreign_key("fk_aporte_aula_id_aula", "aporte", "aula", ["aula_id"], ["id"])

    # A absorção de natureza serviço não é ressarcível — decisão nova desta
    # fatia (documento 04 §1), aplicada às absorções já gravadas: quem
    # absorveu tempo não tem valor em reais a devolver (`RF-07-21`,
    # `RN-07-39`, design — Decisions 6).
    op.execute(
        """
        UPDATE aporte
        SET situacao_de_ressarcimento = 'nao_se_aplica'
        WHERE forma = 'absorcao'
          AND tipo_de_recurso_id IN (
              SELECT id FROM tipo_de_recurso WHERE natureza = 'servico'
          )
        """
    )

    # O pagamento que devolve as moedas do aporte por absorção, contra o
    # que a receita destinada declarada ainda cobre (`RF-07-22`, `RF-07-25`,
    # `RN-07-17`, design — Decisions 3, 4). `aporte_id` é único: um aporte
    # tem no máximo um ressarcimento. O comprovante é exigido, ao contrário
    # do de `aporte`.
    op.create_table(
        "ressarcimento",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("aporte_id", sa.Uuid(), nullable=False),
        sa.Column("receita_destinada_id", sa.Uuid(), nullable=False),
        sa.Column("valor_em_reais", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("admin_pagador_id", sa.Uuid(), nullable=False),
        sa.Column("data", sa.Date(), nullable=False),
        sa.Column("comprovante_referencia", sa.String(length=512), nullable=False),
        sa.Column("comprovante_nome_original", sa.String(length=256), nullable=True),
        sa.Column("comprovante_tipo", sa.String(length=128), nullable=False),
        sa.Column("comprovante_tamanho", sa.Integer(), nullable=False),
        sa.Column("autor_id", sa.Uuid(), nullable=False),
        sa.Column("papel_do_autor", sa.String(length=32), nullable=False),
        sa.Column(
            "registrado_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["admin_pagador_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["aporte_id"], ["aporte.id"]),
        sa.ForeignKeyConstraint(["autor_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["receita_destinada_id"], ["aporte.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("aporte_id", name="uq_ressarcimento_aporte_id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("ressarcimento")
    op.drop_constraint("fk_aporte_aula_id_aula", "aporte", type_="foreignkey")
    op.drop_column("aporte", "aula_id")
    op.drop_column("aporte", "destinacao")
    op.drop_column("lancamento", "destinacao")
