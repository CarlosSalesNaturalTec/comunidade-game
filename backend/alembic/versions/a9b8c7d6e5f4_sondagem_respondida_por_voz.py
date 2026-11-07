"""a sondagem aceita resposta falada, sem alternativa

Decisão do fundador de 2026-11-07 (documento 09 §1).

`resposta_da_submissao.alternativa_escolhida` passa a nulável e nasce
`resposta_falada`: na sondagem, a fala que não se ligou a nenhuma
alternativa segue como transcrição literal, gravada como não acertada
(`RF-05-98`, `RN-05-55`). O `CHECK` garante uma forma só por linha. As linhas
existentes têm alternativa e passam no `CHECK`.

O `downgrade` apaga as respostas faladas antes de voltar o `NOT NULL`.

Revision ID: a9b8c7d6e5f4
Revises: f8e4d5a6b7c8
Create Date: 2026-11-07

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "a9b8c7d6e5f4"
down_revision: str | None = "f8e4d5a6b7c8"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("resposta_da_submissao", sa.Column("resposta_falada", sa.Text(), nullable=True))
    op.alter_column("resposta_da_submissao", "alternativa_escolhida", nullable=True)
    op.create_check_constraint(
        "ck_resposta_da_submissao_forma_unica",
        "resposta_da_submissao",
        "(alternativa_escolhida IS NULL) <> (resposta_falada IS NULL)",
    )


def downgrade() -> None:
    op.drop_constraint(
        "ck_resposta_da_submissao_forma_unica", "resposta_da_submissao", type_="check"
    )
    op.execute("DELETE FROM resposta_da_submissao WHERE alternativa_escolhida IS NULL")
    op.alter_column("resposta_da_submissao", "alternativa_escolhida", nullable=False)
    op.drop_column("resposta_da_submissao", "resposta_falada")
