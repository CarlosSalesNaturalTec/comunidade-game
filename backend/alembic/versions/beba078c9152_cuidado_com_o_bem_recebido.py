"""cuidado com o bem recebido: kit do prático, customização e pontuação do bem

Revision ID: beba078c9152
Revises: b1c2d3e4f5a6
Create Date: 2026-11-12 00:00:00

O prático declara, opcional, o kit que apresenta (`RF-09-141`). O registro de
customização do kit recebido e a pontuação do bem por encontro — conservação
ou customização, uma vez só (`RF-01-84` a `RF-01-87`, `RN-01-66`). Sem
backfill: prático já declarado segue sem kit.
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "beba078c9152"
down_revision: str | Sequence[str] | None = "b1c2d3e4f5a6"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _colunas_de_autoria() -> list[sa.Column]:
    return [
        sa.Column("autor_id", sa.Uuid(), sa.ForeignKey("persona.id"), nullable=False),
        sa.Column("papel_do_autor", sa.String(length=32), nullable=False),
        sa.Column(
            "registrado_em",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    ]


def upgrade() -> None:
    op.add_column("missao", sa.Column("desafio_pratico_kit_id", sa.Uuid(), nullable=True))
    op.create_foreign_key(
        "fk_missao_desafio_pratico_kit_id",
        "missao",
        "recompensa_de_marco",
        ["desafio_pratico_kit_id"],
        ["id"],
    )

    op.create_table(
        "registro_de_customizacao",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "entrega_de_recompensa_id",
            sa.Uuid(),
            sa.ForeignKey("entrega_de_recompensa.id"),
            nullable=False,
        ),
        sa.Column("guerreiro_id", sa.Uuid(), sa.ForeignKey("persona.id"), nullable=False),
        sa.Column("descricao", sa.Text(), nullable=False),
        sa.Column(
            "situacao",
            sa.Enum(
                "pendente",
                "aprovado",
                "reprovado",
                "cancelado",
                "expirado",
                name="situacaodoregistrodecustomizacao",
                native_enum=False,
                length=16,
            ),
            nullable=False,
        ),
        sa.Column("midia_referencia", sa.String(length=512), nullable=True),
        sa.Column("midia_tamanho", sa.Integer(), nullable=True),
        sa.Column("midia_tipo_do_arquivo", sa.String(length=255), nullable=True),
        sa.Column("motivo_do_julgamento", sa.Text(), nullable=True),
        sa.Column("aula_id", sa.Uuid(), sa.ForeignKey("aula.id"), nullable=True),
        sa.Column("julgado_por_id", sa.Uuid(), sa.ForeignKey("persona.id"), nullable=True),
        sa.Column("julgado_em", sa.DateTime(timezone=True), nullable=True),
        *_colunas_de_autoria(),
    )
    op.create_index(
        "uq_registro_de_customizacao_pendente_por_entrega",
        "registro_de_customizacao",
        ["entrega_de_recompensa_id"],
        unique=True,
        postgresql_where=sa.text("situacao = 'pendente'"),
    )
    op.create_index(
        "ix_registro_de_customizacao_guerreiro_id", "registro_de_customizacao", ["guerreiro_id"]
    )

    op.create_table(
        "pontuacao_do_bem",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("aula_id", sa.Uuid(), sa.ForeignKey("aula.id"), nullable=False),
        sa.Column(
            "entrega_de_recompensa_id",
            sa.Uuid(),
            sa.ForeignKey("entrega_de_recompensa.id"),
            nullable=False,
        ),
        sa.Column("guerreiro_id", sa.Uuid(), sa.ForeignKey("persona.id"), nullable=False),
        sa.Column(
            "fonte",
            sa.Enum(
                "conservacao",
                "customizacao",
                name="fontedapontuacaodobem",
                native_enum=False,
                length=16,
            ),
            nullable=False,
        ),
        sa.Column(
            "registro_de_customizacao_id",
            sa.Uuid(),
            sa.ForeignKey("registro_de_customizacao.id"),
            nullable=True,
        ),
        *_colunas_de_autoria(),
        sa.UniqueConstraint(
            "aula_id", "entrega_de_recompensa_id", name="uq_pontuacao_do_bem_aula_entrega"
        ),
    )
    op.create_index("ix_pontuacao_do_bem_guerreiro_id", "pontuacao_do_bem", ["guerreiro_id"])


def downgrade() -> None:
    op.drop_index("ix_pontuacao_do_bem_guerreiro_id", table_name="pontuacao_do_bem")
    op.drop_table("pontuacao_do_bem")
    op.drop_index("ix_registro_de_customizacao_guerreiro_id", table_name="registro_de_customizacao")
    op.drop_index(
        "uq_registro_de_customizacao_pendente_por_entrega",
        table_name="registro_de_customizacao",
    )
    op.drop_table("registro_de_customizacao")
    op.drop_constraint("fk_missao_desafio_pratico_kit_id", "missao", type_="foreignkey")
    op.drop_column("missao", "desafio_pratico_kit_id")
