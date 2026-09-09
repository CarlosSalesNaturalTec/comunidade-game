"""quiz do desbloqueio com várias perguntas

Revision ID: c9d0e1f2a3b4
Revises: 4fe4a2883b8c
Create Date: 2026-09-09 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c9d0e1f2a3b4"
down_revision: str | Sequence[str] | None = "4fe4a2883b8c"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # Em três passos, nesta ordem: cria as tabelas, transporta cada quiz de
    # pergunta única existente como a primeira pergunta da sua missão e só
    # então derruba as seis colunas (design — Migration Plan).
    op.create_table(
        "pergunta_do_desbloqueio",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("missao_id", sa.Uuid(), nullable=False),
        sa.Column("ordem", sa.Integer(), nullable=False),
        sa.Column("enunciado", sa.Text(), nullable=False),
        sa.Column("alternativa_1", sa.Text(), nullable=False),
        sa.Column("alternativa_2", sa.Text(), nullable=False),
        sa.Column("alternativa_3", sa.Text(), nullable=False),
        sa.Column("alternativa_4", sa.Text(), nullable=False),
        sa.Column("alternativa_correta", sa.Integer(), nullable=False),
        sa.CheckConstraint(
            "alternativa_correta BETWEEN 1 AND 4",
            name="ck_pergunta_do_desbloqueio_alternativa_correta",
        ),
        sa.ForeignKeyConstraint(["missao_id"], ["missao.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "missao_id", "ordem", name="uq_pergunta_do_desbloqueio_missao_id_ordem"
        ),
    )
    op.create_index(
        "ix_pergunta_do_desbloqueio_missao_id", "pergunta_do_desbloqueio", ["missao_id"]
    )

    op.create_table(
        "submissao_do_desbloqueio",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("guerreiro_id", sa.Uuid(), nullable=False),
        sa.Column("missao_id", sa.Uuid(), nullable=False),
        sa.Column(
            "momento", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column("acertos", sa.Integer(), nullable=False),
        sa.Column("total", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["guerreiro_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["missao_id"], ["missao.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_submissao_do_desbloqueio_guerreiro_id_missao_id",
        "submissao_do_desbloqueio",
        ["guerreiro_id", "missao_id"],
    )

    op.create_table(
        "resposta_da_submissao",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("submissao_id", sa.Uuid(), nullable=False),
        sa.Column("pergunta_id", sa.Uuid(), nullable=False),
        sa.Column("alternativa_escolhida", sa.Integer(), nullable=False),
        sa.Column("acertou", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["submissao_id"], ["submissao_do_desbloqueio.id"]),
        sa.ForeignKeyConstraint(["pergunta_id"], ["pergunta_do_desbloqueio.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "submissao_id", "pergunta_id", name="uq_resposta_da_submissao_submissao_id_pergunta_id"
        ),
    )
    op.create_index(
        "ix_resposta_da_submissao_submissao_id", "resposta_da_submissao", ["submissao_id"]
    )

    # O desafio de quiz que já existe vira a primeira e única pergunta da
    # missão; o prático não tem pergunta e mantém o enunciado onde está.
    op.execute(
        """
        INSERT INTO pergunta_do_desbloqueio (
            id, missao_id, ordem, enunciado,
            alternativa_1, alternativa_2, alternativa_3, alternativa_4, alternativa_correta
        )
        SELECT
            gen_random_uuid(), id, 1, desafio_de_desbloqueio_enunciado,
            desafio_de_desbloqueio_alternativa_1, desafio_de_desbloqueio_alternativa_2,
            desafio_de_desbloqueio_alternativa_3, desafio_de_desbloqueio_alternativa_4,
            desafio_de_desbloqueio_alternativa_correta
        FROM missao
        WHERE tipo_do_desafio_de_desbloqueio = 'quiz'
          AND desafio_de_desbloqueio_enunciado IS NOT NULL
          AND desafio_de_desbloqueio_alternativa_correta IS NOT NULL
        """
    )
    # No quiz o enunciado desce para a pergunta e a missão fica sem o dela
    # (design — decisão 2).
    op.execute(
        "UPDATE missao SET desafio_de_desbloqueio_enunciado = NULL "
        "WHERE tipo_do_desafio_de_desbloqueio = 'quiz'"
    )

    for coluna in (
        "desafio_de_desbloqueio_alternativa_1",
        "desafio_de_desbloqueio_alternativa_2",
        "desafio_de_desbloqueio_alternativa_3",
        "desafio_de_desbloqueio_alternativa_4",
        "desafio_de_desbloqueio_alternativa_correta",
    ):
        op.drop_column("missao", coluna)


def downgrade() -> None:
    """Downgrade schema."""
    # Volta ao modelo de pergunta única pela pergunta de menor ordem: as
    # demais se perdem, o que é inerente a desfazer esta fatia (design —
    # Migration Plan).
    op.add_column(
        "missao", sa.Column("desafio_de_desbloqueio_alternativa_1", sa.Text(), nullable=True)
    )
    op.add_column(
        "missao", sa.Column("desafio_de_desbloqueio_alternativa_2", sa.Text(), nullable=True)
    )
    op.add_column(
        "missao", sa.Column("desafio_de_desbloqueio_alternativa_3", sa.Text(), nullable=True)
    )
    op.add_column(
        "missao", sa.Column("desafio_de_desbloqueio_alternativa_4", sa.Text(), nullable=True)
    )
    op.add_column(
        "missao",
        sa.Column("desafio_de_desbloqueio_alternativa_correta", sa.Integer(), nullable=True),
    )
    op.execute(
        """
        UPDATE missao SET
            desafio_de_desbloqueio_enunciado = primeira.enunciado,
            desafio_de_desbloqueio_alternativa_1 = primeira.alternativa_1,
            desafio_de_desbloqueio_alternativa_2 = primeira.alternativa_2,
            desafio_de_desbloqueio_alternativa_3 = primeira.alternativa_3,
            desafio_de_desbloqueio_alternativa_4 = primeira.alternativa_4,
            desafio_de_desbloqueio_alternativa_correta = primeira.alternativa_correta
        FROM (
            SELECT DISTINCT ON (missao_id) *
            FROM pergunta_do_desbloqueio
            ORDER BY missao_id, ordem
        ) AS primeira
        WHERE missao.id = primeira.missao_id
        """
    )

    op.drop_index("ix_resposta_da_submissao_submissao_id", table_name="resposta_da_submissao")
    op.drop_table("resposta_da_submissao")
    op.drop_index(
        "ix_submissao_do_desbloqueio_guerreiro_id_missao_id", table_name="submissao_do_desbloqueio"
    )
    op.drop_table("submissao_do_desbloqueio")
    op.drop_index("ix_pergunta_do_desbloqueio_missao_id", table_name="pergunta_do_desbloqueio")
    op.drop_table("pergunta_do_desbloqueio")
