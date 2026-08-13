"""cria pergunta partida e resposta de quiz

Revision ID: c47a1e9f5b30
Revises: ab800c29b268
Create Date: 2026-08-13 01:40:11.204517

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c47a1e9f5b30"
down_revision: str | Sequence[str] | None = "ab800c29b268"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # Migração aditiva: nenhuma tabela existente é alterada, e por isso a
    # reversão não perde crédito já concedido (design — Migration Plan).
    op.create_table(
        "pergunta_de_quiz",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("enunciado", sa.Text(), nullable=False),
        sa.Column("alternativa_1", sa.Text(), nullable=False),
        sa.Column("alternativa_2", sa.Text(), nullable=False),
        sa.Column("alternativa_3", sa.Text(), nullable=False),
        sa.Column("alternativa_4", sa.Text(), nullable=False),
        sa.Column("alternativa_correta", sa.Integer(), nullable=False),
        sa.Column("autor_id", sa.Uuid(), nullable=False),
        sa.Column("papel_do_autor", sa.String(length=32), nullable=False),
        sa.Column(
            "registrado_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "alternativa_correta BETWEEN 1 AND 4",
            name="ck_pergunta_de_quiz_alternativa_correta",
        ),
        sa.ForeignKeyConstraint(["autor_id"], ["persona.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "partida_de_quiz",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("aula_id", sa.Uuid(), nullable=False),
        sa.Column("atividade_id", sa.Uuid(), nullable=False),
        sa.Column(
            "situacao",
            sa.Enum(
                "aberta",
                "encerrada",
                name="situacaodapartida",
                native_enum=False,
                length=16,
            ),
            nullable=False,
        ),
        sa.Column("encerrada_por_id", sa.Uuid(), nullable=True),
        sa.Column("encerrada_em", sa.DateTime(timezone=True), nullable=True),
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
        sa.ForeignKeyConstraint(["encerrada_por_id"], ["persona.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "equipe_na_partida",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("partida_id", sa.Uuid(), nullable=False),
        sa.Column("equipe_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(["equipe_id"], ["equipe.id"]),
        sa.ForeignKeyConstraint(["partida_id"], ["partida_de_quiz.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "partida_id", "equipe_id", name="uq_equipe_na_partida_partida_id_equipe_id"
        ),
    )

    op.create_table(
        "pergunta_anulada_na_partida",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("partida_id", sa.Uuid(), nullable=False),
        sa.Column("pergunta_id", sa.Uuid(), nullable=False),
        sa.Column("autor_id", sa.Uuid(), nullable=False),
        sa.Column("papel_do_autor", sa.String(length=32), nullable=False),
        sa.Column(
            "registrado_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["autor_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["partida_id"], ["partida_de_quiz.id"]),
        sa.ForeignKeyConstraint(["pergunta_id"], ["pergunta_de_quiz.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "partida_id",
            "pergunta_id",
            name="uq_pergunta_anulada_na_partida_partida_id_pergunta_id",
        ),
    )

    # A unicidade por (partida, pergunta, equipe) é o que torna o reenvio
    # com a rede instável inofensivo (design — Migration Plan).
    op.create_table(
        "resposta_de_quiz",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("partida_id", sa.Uuid(), nullable=False),
        sa.Column("pergunta_id", sa.Uuid(), nullable=False),
        sa.Column("equipe_id", sa.Uuid(), nullable=False),
        sa.Column("alternativa_escolhida", sa.Integer(), nullable=False),
        sa.Column("momento_de_chegada", sa.DateTime(timezone=True), nullable=False),
        sa.Column("anulada_em", sa.DateTime(timezone=True), nullable=True),
        sa.Column("autor_id", sa.Uuid(), nullable=False),
        sa.Column("papel_do_autor", sa.String(length=32), nullable=False),
        sa.Column(
            "registrado_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "alternativa_escolhida BETWEEN 1 AND 4",
            name="ck_resposta_de_quiz_alternativa_escolhida",
        ),
        sa.ForeignKeyConstraint(["autor_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["equipe_id"], ["equipe.id"]),
        sa.ForeignKeyConstraint(["partida_id"], ["partida_de_quiz.id"]),
        sa.ForeignKeyConstraint(["pergunta_id"], ["pergunta_de_quiz.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "partida_id",
            "pergunta_id",
            "equipe_id",
            name="uq_resposta_de_quiz_partida_id_pergunta_id_equipe_id",
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("resposta_de_quiz")
    op.drop_table("pergunta_anulada_na_partida")
    op.drop_table("equipe_na_partida")
    op.drop_table("partida_de_quiz")
    op.drop_table("pergunta_de_quiz")
