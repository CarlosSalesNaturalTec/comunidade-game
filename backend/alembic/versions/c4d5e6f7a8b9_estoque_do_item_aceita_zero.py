"""estoque do item de catalogo avulso aceita zero

Revision ID: c4d5e6f7a8b9
Revises: b3c4d5e6f7a8
Create Date: 2026-08-19 00:05:00.000000

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c4d5e6f7a8b9"
down_revision: str | Sequence[str] | None = "b3c4d5e6f7a8"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # O piso de gestão continua sendo 1, aplicado em `catalogo_avulso.regra`; a
    # trava de banco passa a só impedir negativo, porque a troca decrementa o
    # estoque até zero sem passar pelo caminho de gestão (`RF-07-36`, `RN-07-27`).
    op.drop_constraint(
        "ck_item_de_catalogo_avulso_estoque_minimo", "item_de_catalogo_avulso", type_="check"
    )
    op.create_check_constraint(
        "ck_item_de_catalogo_avulso_estoque_nao_negativo", "item_de_catalogo_avulso", "estoque >= 0"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "ck_item_de_catalogo_avulso_estoque_nao_negativo",
        "item_de_catalogo_avulso",
        type_="check",
    )
    op.create_check_constraint(
        "ck_item_de_catalogo_avulso_estoque_minimo", "item_de_catalogo_avulso", "estoque >= 1"
    )
