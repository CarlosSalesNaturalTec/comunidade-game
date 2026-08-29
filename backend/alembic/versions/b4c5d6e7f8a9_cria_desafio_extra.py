"""cria desafio_extra

Revision ID: b4c5d6e7f8a9
Revises: da7ae0cdb737
Create Date: 2026-08-29 12:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b4c5d6e7f8a9"
down_revision: str | Sequence[str] | None = "da7ae0cdb737"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # O desafio que o Apoiador propõe sobre uma trilha em andamento
    # (PRD-14 §8). A recompensa é uma quantidade de um tipo de recurso num
    # ponto de apoio, no mesmo desenho do item do catálogo avulso; o nick
    # do destinatário é texto puro, sem chave estrangeira, para que a
    # aplicação nunca confirme se ele existe (`RF-14-29` a `RF-14-39`,
    # `RF-14-74` a `RF-14-76`, `RN-14-13` a `RN-14-20`, `RN-14-41`).
    op.create_table(
        "desafio_extra",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("trilha_id", sa.Uuid(), nullable=False),
        sa.Column("missao_id", sa.Uuid(), nullable=True),
        sa.Column(
            "modalidade",
            sa.Enum("aberto", "direcionado", name="modalidade", native_enum=False, length=16),
            nullable=False,
        ),
        sa.Column("nick_do_destinatario", sa.Text(), nullable=True),
        sa.Column("justificativa_do_vinculo", sa.Text(), nullable=True),
        sa.Column("tipo_de_recurso_id", sa.Uuid(), nullable=False),
        sa.Column("ponto_de_apoio_id", sa.Uuid(), nullable=False),
        sa.Column("quantidade_disponivel", sa.Integer(), nullable=False),
        sa.Column("criterio_de_atribuicao", sa.Text(), nullable=False),
        sa.Column("pontos_extras", sa.Integer(), nullable=False),
        sa.Column(
            "formato",
            sa.Enum(
                "presencial",
                "on_line",
                name="formatododesafioextra",
                native_enum=False,
                length=16,
            ),
            nullable=False,
        ),
        sa.Column(
            "custeio",
            sa.Enum(
                "aporte_do_proponente",
                "saldo_de_recurso",
                name="custeiododesafioextra",
                native_enum=False,
                length=24,
            ),
            nullable=False,
        ),
        sa.Column("aporte_id", sa.Uuid(), nullable=True),
        sa.Column("vigencia_inicio", sa.Date(), nullable=False),
        sa.Column("vigencia_fim", sa.Date(), nullable=False),
        sa.Column("mestre_validador_id", sa.Uuid(), nullable=True),
        sa.Column("admin_aprovador_id", sa.Uuid(), nullable=True),
        sa.Column(
            "situacao",
            sa.Enum(
                "em_validacao_do_mestre",
                "em_aprovacao_do_admin",
                "publicado",
                "recusado",
                name="situacaododesafioextra",
                native_enum=False,
                length=24,
            ),
            nullable=False,
        ),
        sa.Column("motivo_da_recusa", sa.Text(), nullable=True),
        sa.Column("autor_id", sa.Uuid(), nullable=False),
        sa.Column("papel_do_autor", sa.String(length=32), nullable=False),
        sa.Column(
            "registrado_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "pontos_extras >= 1 AND pontos_extras <= 10",
            name="ck_desafio_extra_pontos_extras_teto_10",
        ),
        sa.CheckConstraint(
            "(modalidade = 'direcionado' AND nick_do_destinatario IS NOT NULL "
            "AND justificativa_do_vinculo IS NOT NULL) OR "
            "(modalidade = 'aberto' AND nick_do_destinatario IS NULL "
            "AND justificativa_do_vinculo IS NULL)",
            name="ck_desafio_extra_direcionado_exige_nick_e_justificativa",
        ),
        sa.CheckConstraint(
            "vigencia_fim >= vigencia_inicio",
            name="ck_desafio_extra_fim_apos_ou_igual_ao_inicio",
        ),
        sa.ForeignKeyConstraint(["admin_aprovador_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["aporte_id"], ["aporte.id"]),
        sa.ForeignKeyConstraint(["autor_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["mestre_validador_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["missao_id"], ["missao.id"]),
        sa.ForeignKeyConstraint(["ponto_de_apoio_id"], ["ponto_de_apoio.id"]),
        sa.ForeignKeyConstraint(["tipo_de_recurso_id"], ["tipo_de_recurso.id"]),
        sa.ForeignKeyConstraint(["trilha_id"], ["trilha.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("desafio_extra")
