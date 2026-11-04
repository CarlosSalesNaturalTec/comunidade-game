"""os dois vereditos do julgamento do desafio pratico

O julgamento do desafio **prático** deixa de ser um booleano e passa a **dois
vereditos** (`RF-09-133`): `aprovado` é renomeado para `cumpriu` — o que abre a
missão seguinte e credita os 5 pontos regulares do documento 11 §5 — e nasce
`publicavel`, que diz se aquela entrega vai à **vitrine pública**. Com um campo
só, o Mestre teria de reprovar quem cumpriu e enquadrou mal, ou publicar o
rosto da criança (design — decisão 1).

`motivo_do_julgamento` guarda o motivo em **linguagem simples**, exigido em todo
veredito negativo (`RF-09-134`, `RN-09-53`). Ele só serve se a criança o ler, e
por isso a reprovação **para de apagar** a linha: ela permanece com o veredito e
o motivo, e entregar de novo reabre a mesma declaração (`RN-09-54`, design —
decisão 2).

`julgado_em` é o que separa o julgado por esta regra do julgado **antes** dela:
a linha antiga tem `cumpriu` verdadeiro com `julgado_em` nulo, e por isso não
recebe crédito retroativo nem se rejulga (`RN-09-55`, design — decisão 3).

O rename preserva o dado: `cumpriu` nulo segue sendo "declarado e não julgado",
que é o que o percurso e a bancada já leem. As três colunas novas são
_nullable_ e **sem _backfill_** — a migração não credita ponto, não apaga linha
e não mexe em saldo nenhum.

Revision ID: e7d3c4f5a6b7
Revises: d6c2b3e4f5a6
Create Date: 2026-11-04

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "e7d3c4f5a6b7"
down_revision: str | None = "d6c2b3e4f5a6"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.alter_column("desbloqueio_da_missao", "aprovado", new_column_name="cumpriu")
    op.add_column("desbloqueio_da_missao", sa.Column("publicavel", sa.Boolean(), nullable=True))
    op.add_column(
        "desbloqueio_da_missao", sa.Column("motivo_do_julgamento", sa.Text(), nullable=True)
    )
    op.add_column(
        "desbloqueio_da_missao",
        sa.Column("julgado_em", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("desbloqueio_da_missao", "julgado_em")
    op.drop_column("desbloqueio_da_missao", "motivo_do_julgamento")
    op.drop_column("desbloqueio_da_missao", "publicavel")
    op.alter_column("desbloqueio_da_missao", "cumpriu", new_column_name="aprovado")
