"""comprovacao do desafio pratico entregue pelo guerreiro

A declaração de que cumpriu o desafio **prático** deixa de ser nua e passa a
carregar a **comprovação** na forma que o Mestre autor declarou aceitar
(`RF-05-91`). As colunas são da própria `desbloqueio_da_missao`, não de tabela
nova: a linha já é **uma por par** `(guerreiro_id, missao_id)`, já nasce com a
declaração e já é **apagada** quando o julgamento não passa — de modo que a
comprovação morre com ela sem código de limpeza próprio (`RN-05-52`, design —
decisão 1).

`comprovacao` guarda o corpo do tipo texto ou o endereço do tipo link externo;
`comprovacao_referencia`, `comprovacao_tamanho` e `comprovacao_tipo_do_arquivo`
guardam o arquivo dos quatro tipos de mídia, preenchidos só quando o envio
conclui, espelhando `criacao_original` (design — decisão 4).

`entrega_presencial` é a alternativa de quem recusa a câmera, não tem aparelho
que grave ou não consegue enviar: a declaração é gravada sem mídia e nunca faz
perder a missão (`RN-05-51`, `RF-05-78`). É coluna **própria** porque sem ela
"não entregou" e "vai entregar no encontro" ficariam indistinguíveis, e a
bancada do Mestre não teria como dizer o que esperar (design — decisão 3).

Todas _nullable_ e **sem _backfill_**: o desbloqueio prático gravado antes
desta regra segue valendo sem comprovação, como a revisão anterior fixou para
os três campos do Mestre, e a leitura dos bytes dele responde 404 (design —
decisão 7).

Revision ID: d6c2b3e4f5a6
Revises: c5b1a2d3e4f5
Create Date: 2026-11-04

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "d6c2b3e4f5a6"
down_revision: str | None = "c5b1a2d3e4f5"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("desbloqueio_da_missao", sa.Column("comprovacao", sa.Text(), nullable=True))
    op.add_column(
        "desbloqueio_da_missao",
        sa.Column("comprovacao_referencia", sa.String(length=512), nullable=True),
    )
    op.add_column(
        "desbloqueio_da_missao", sa.Column("comprovacao_tamanho", sa.Integer(), nullable=True)
    )
    op.add_column(
        "desbloqueio_da_missao",
        sa.Column("comprovacao_tipo_do_arquivo", sa.String(length=255), nullable=True),
    )
    op.add_column(
        "desbloqueio_da_missao", sa.Column("entrega_presencial", sa.Boolean(), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("desbloqueio_da_missao", "entrega_presencial")
    op.drop_column("desbloqueio_da_missao", "comprovacao_tipo_do_arquivo")
    op.drop_column("desbloqueio_da_missao", "comprovacao_tamanho")
    op.drop_column("desbloqueio_da_missao", "comprovacao_referencia")
    op.drop_column("desbloqueio_da_missao", "comprovacao")
