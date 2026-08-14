"""credencial de dispositivo do sensor

Revision ID: e1f2a3b4c5d6
Revises: a4b5c6d7e8f9
Create Date: 2026-08-14 19:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e1f2a3b4c5d6"
down_revision: str | Sequence[str] | None = "a4b5c6d7e8f9"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # RN-01-53: o índice de hoje sobre (tipo, identificador) impediria o
    # mesmo aparelho em duas séries — passa a excluir o tipo `dispositivo`.
    op.drop_index("uq_credencial_identificador_por_tipo_ativa", table_name="credencial")

    op.add_column("credencial", sa.Column("serie_de_coleta_id", sa.Uuid(), nullable=True))
    op.add_column("credencial", sa.Column("trilha_id", sa.Uuid(), nullable=True))
    op.add_column("credencial", sa.Column("revogada_por", sa.String(length=128), nullable=True))
    op.add_column(
        "credencial", sa.Column("motivo_da_revogacao", sa.String(length=512), nullable=True)
    )
    op.add_column("credencial", sa.Column("revogada_em", sa.DateTime(timezone=True), nullable=True))
    op.create_foreign_key(
        "fk_credencial_serie_de_coleta_id_serie_de_coleta",
        "credencial",
        "serie_de_coleta",
        ["serie_de_coleta_id"],
        ["id"],
    )
    op.create_foreign_key(
        "fk_credencial_trilha_id_trilha", "credencial", "trilha", ["trilha_id"], ["id"]
    )

    op.create_index(
        "uq_credencial_identificador_por_tipo_ativa",
        "credencial",
        ["tipo", "identificador"],
        unique=True,
        postgresql_where=sa.text("ativa AND tipo != 'dispositivo'"),
    )
    op.create_index(
        "uq_credencial_dispositivo_serie_ativa",
        "credencial",
        ["serie_de_coleta_id"],
        unique=True,
        postgresql_where=sa.text("ativa AND tipo = 'dispositivo'"),
    )

    # O atributo `dispositivo` do PRD-08 §8 (`RF-08-14`). `ADD COLUMN`
    # anulável em tabela particionada propaga às partições sem reescrever
    # dado.
    op.add_column("registro_de_coleta", sa.Column("credencial_id", sa.Uuid(), nullable=True))
    op.create_foreign_key(
        "fk_registro_de_coleta_credencial_id_credencial",
        "registro_de_coleta",
        "credencial",
        ["credencial_id"],
        ["id"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "fk_registro_de_coleta_credencial_id_credencial", "registro_de_coleta", type_="foreignkey"
    )
    op.drop_column("registro_de_coleta", "credencial_id")

    op.drop_index("uq_credencial_dispositivo_serie_ativa", table_name="credencial")
    op.drop_index("uq_credencial_identificador_por_tipo_ativa", table_name="credencial")

    op.drop_constraint("fk_credencial_trilha_id_trilha", "credencial", type_="foreignkey")
    op.drop_constraint(
        "fk_credencial_serie_de_coleta_id_serie_de_coleta", "credencial", type_="foreignkey"
    )

    op.drop_column("credencial", "revogada_em")
    op.drop_column("credencial", "motivo_da_revogacao")
    op.drop_column("credencial", "revogada_por")
    op.drop_column("credencial", "trilha_id")
    op.drop_column("credencial", "serie_de_coleta_id")

    op.create_index(
        "uq_credencial_identificador_por_tipo_ativa",
        "credencial",
        ["tipo", "identificador"],
        unique=True,
        postgresql_where=sa.text("ativa"),
    )
