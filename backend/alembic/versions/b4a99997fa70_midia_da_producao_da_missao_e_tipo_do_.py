"""midia da producao da missao e tipo do arquivo da criacao

A produção da missão passa a **guardar** a foto e o áudio (`RF-01-79`): até
2026-11-03 a foto era lida e descartada e o áudio nunca chegava ao núcleo, e a
tabela não tinha onde guardar nenhum dos dois. Entram `referencia`, `tamanho` e
`tipo_do_arquivo`, no mesmo vocabulário de mídia que `criacao_original` e
`conteudo_da_missao` já usam.

A `criacao_original` ganha `tipo_do_arquivo` (`RF-01-78`): ela guardava
`referencia` e `tamanho` e **não** o tipo MIME, que ia só para a sessão de
envio — sem ele a rota de leitura nova devolveria sempre
`application/octet-stream` e nenhum navegador renderizaria a mídia.

Todas as colunas são _nullable_: nada existente precisa de valor, e produção
gravada antes desta migração segue sem mídia, porque o arquivo nunca foi
gravado — não há _backfill_ possível.

Revision ID: b4a99997fa70
Revises: b8d2f4a61c73
Create Date: 2026-11-04

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "b4a99997fa70"
down_revision: str | None = "b8d2f4a61c73"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "producao_da_missao", sa.Column("referencia", sa.String(length=512), nullable=True)
    )
    op.add_column("producao_da_missao", sa.Column("tamanho", sa.Integer(), nullable=True))
    op.add_column(
        "producao_da_missao", sa.Column("tipo_do_arquivo", sa.String(length=255), nullable=True)
    )
    op.add_column(
        "criacao_original", sa.Column("tipo_do_arquivo", sa.String(length=255), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("criacao_original", "tipo_do_arquivo")
    op.drop_column("producao_da_missao", "tipo_do_arquivo")
    op.drop_column("producao_da_missao", "tamanho")
    op.drop_column("producao_da_missao", "referencia")
