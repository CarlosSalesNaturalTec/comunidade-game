"""resultado único por guerreiro e atividade

Revision ID: a7c1d4e9b305
Revises: d5f1a8c3b7e2
Create Date: 2026-10-11 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a7c1d4e9b305"
down_revision: str | Sequence[str] | None = "d5f1a8c3b7e2"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    conexao = op.get_bind()

    # `RN-02-33`: o par (Guerreiro(a), atividade) passa a ser único. Se já
    # houver Resultado repetido, a criação falharia a meio — então a
    # conferência vem antes e para aqui. Resultado não se apaga
    # (`RF-09-47`), então a limpeza é decisão do fundador, nunca da
    # migração (design — Risks).
    duplicatas = conexao.execute(
        sa.text(
            "SELECT guerreiro_id, atividade_id, count(*) AS quantidade "
            "FROM resultado GROUP BY guerreiro_id, atividade_id HAVING count(*) > 1"
        )
    ).fetchall()
    if duplicatas:
        raise RuntimeError(
            "Há Resultado repetido do mesmo par (Guerreiro(a), atividade): "
            f"{len(duplicatas)} par(es). Resultado não se apaga — leve os pares ao "
            "fundador antes de aplicar esta migração."
        )

    # Atividade avulsa já gravada sem aula fica inválida pela regra nova e
    # não se consegue lançar. Atribuir aula a elas é decisão do fundador,
    # então aqui só se conta e se relata (design — Risks).
    avulsas_sem_aula = conexao.execute(
        sa.text("SELECT count(*) FROM atividade WHERE missao_id IS NULL AND aula_id IS NULL")
    ).scalar_one()
    if avulsas_sem_aula:
        print(
            f"[atenção] {avulsas_sem_aula} atividade(s) avulsa(s) sem aula declarada — "
            "o lançamento delas exige que o fundador decida a qual encontro pertencem "
            "(`RF-02-29`)."
        )

    op.create_unique_constraint(
        "uq_resultado_guerreiro_id_atividade_id", "resultado", ["guerreiro_id", "atividade_id"]
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("uq_resultado_guerreiro_id_atividade_id", "resultado", type_="unique")
