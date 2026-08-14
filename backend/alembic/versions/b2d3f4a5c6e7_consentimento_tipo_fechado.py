"""fecha o conjunto de consentimento.tipo

Revision ID: b2d3f4a5c6e7
Revises: a1c2e3f4b5d6
Create Date: 2026-08-13 22:05:00.000000

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b2d3f4a5c6e7"
down_revision: str | Sequence[str] | None = "a1c2e3f4b5d6"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # Falha alto diante de valor existente fora do conjunto: o Postgres
    # valida as linhas já gravadas ao criar a CHECK CONSTRAINT, e recusa a
    # migração se alguma delas não for `autorizacao_de_divulgacao` nem
    # `biometria` — não há mapeamento silencioso para um valor padrão
    # (design — Risks).
    op.create_check_constraint(
        "ck_consentimento_tipo_valido",
        "consentimento",
        "tipo IN ('autorizacao_de_divulgacao', 'biometria')",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("ck_consentimento_tipo_valido", "consentimento", type_="check")
