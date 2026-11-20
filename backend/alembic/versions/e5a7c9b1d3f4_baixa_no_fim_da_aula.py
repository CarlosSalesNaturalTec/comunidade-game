"""baixa no fim da aula: transição das aulas já terminadas

Decisão do fundador de 2026-11-20 (change `baixa-no-fim-da-aula`): a aula não tem
fechamento, e a reserva é baixada pelo sistema no fim do horário. A aula que já
terminou antes desta implantação, ainda sem desfecho, tem a reserva **liberada**,
sem débito — as entregas de recompensa já debitaram o que saiu —, e passa a
realizada, ou a realizada sem lastro se estava pendente (`RF-07-56`, design —
decisão 7). A coluna `situacao` já comporta o valor novo: é texto de 20.

Revision ID: e5a7c9b1d3f4
Revises: d4f6a8c0e2b3
Create Date: 2026-11-20 18:00:00

"""

from collections.abc import Sequence

from alembic import op

revision: str = "e5a7c9b1d3f4"
down_revision: str | Sequence[str] | None = "d4f6a8c0e2b3"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
        UPDATE reserva SET estado = 'liberada'
         WHERE estado = 'reservada'
           AND aula_id IN (
               SELECT id FROM aula
                WHERE fim_em < now()
                  AND situacao IN ('prevista', 'confirmada', 'pendente_de_lastro')
           )
        """
    )
    op.execute(
        """
        UPDATE aula
           SET situacao = CASE situacao
                              WHEN 'pendente_de_lastro' THEN 'realizada_sem_lastro'
                              ELSE 'realizada'
                          END
         WHERE fim_em < now()
           AND situacao IN ('prevista', 'confirmada', 'pendente_de_lastro')
        """
    )


def downgrade() -> None:
    """Downgrade schema: a transição é fato consumado — a reserva liberada já
    voltou à disponível e pode ter sido usada —, e nada se desfaz."""
