"""renumera a ordem do conteúdo da missão

Revision ID: c4e81b2a9d60
Revises: b2d7e5f1c893
Create Date: 2026-10-28 00:00:00.000000

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c4e81b2a9d60"
down_revision: str | Sequence[str] | None = "b2d7e5f1c893"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


# A ordem do conteúdo nasceu declarada pelo cliente, e o cliente declarava
# sempre 1: todo conteúdo de uma missão empatava, e a sequência que o
# Guerreiro(a) lê ficava a cargo do desempate do banco (`RF-09-126`, design —
# decisão 4). Renumera por missão, na sequência de criação — `registrado_em`,
# com desempate por `id` para o resultado ser determinístico quando duas
# linhas nascem no mesmo instante. Constante, e não literal embutido, para
# que `tests/test_conteudo.py` exercite **este** SQL e não uma cópia dele.
SQL_RENUMERA_A_ORDEM = """
    WITH renumerado AS (
        SELECT
            id,
            ROW_NUMBER() OVER (
                PARTITION BY missao_id ORDER BY registrado_em, id
            ) AS nova_ordem
        FROM conteudo_da_missao
    )
    UPDATE conteudo_da_missao AS c
    SET ordem = r.nova_ordem
    FROM renumerado AS r
    WHERE c.id = r.id AND c.ordem <> r.nova_ordem
"""


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(SQL_RENUMERA_A_ORDEM)


def downgrade() -> None:
    """Downgrade schema."""
    # Sem volta útil: desfazer a renumeração devolveria todo conteúdo a
    # `ordem = 1`, que é exatamente o defeito que esta revisão corrige. O
    # esquema não muda, então nada há para reverter.
