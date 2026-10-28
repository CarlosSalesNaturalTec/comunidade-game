"""carimbo da atividade de trilha removida

Revision ID: a7c3d9e1f250
Revises: c4e81b2a9d60
Create Date: 2026-10-28 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a7c3d9e1f250"
down_revision: str | Sequence[str] | None = "c4e81b2a9d60"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # A única coluna da fatia 25 do PRD-09 (`RF-09-128`, `RN-09-47`), nula:
    # as atividades existentes nascem vigentes e não há dado a transportar.
    # Sem índice novo — `removida_em` nunca filtra sozinha, entra sempre ao
    # lado de `missao_id` ou de `aula_id`, e `ix_atividade_aula_id` já existe
    # (design — decisão 8).
    op.add_column(
        "atividade",
        sa.Column("removida_em", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    """Downgrade schema."""
    # A coluna é a única memória do carimbo: sem ela a atividade removida
    # voltaria a aparecer como vigente nas leituras de autoria e de execução,
    # o que é pior que perdê-la. Apaga-se o que foi carimbado antes de dropar,
    # como a revisão da imagem da pergunta já faz com as substituídas. Os
    # fatos que apontam a atividade impedem o `DELETE` por chave estrangeira
    # — é o aviso de que este `downgrade` não é operação de rotina.
    op.execute("DELETE FROM atividade WHERE removida_em IS NOT NULL")
    op.drop_column("atividade", "removida_em")
