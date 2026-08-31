"""cria consulta ao assistente

Revision ID: f41e6a76385a
Revises: a7c9a9c847e8
Create Date: 2026-08-30 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f41e6a76385a"
down_revision: str | Sequence[str] | None = "a7c9a9c847e8"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "consulta_ao_assistente",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("equipe_id", sa.Uuid(), nullable=True),
        sa.Column("guerreiro_id", sa.Uuid(), nullable=True),
        sa.Column(
            "assistente",
            sa.Enum(
                "trilhas",
                "apoio_escolar",
                name="tipodeassistente",
                native_enum=False,
                length=16,
            ),
            nullable=False,
        ),
        sa.Column(
            "desfecho",
            sa.Enum(
                "respondida",
                "fora_do_corpus",
                "tarefa_escolar",
                name="desfechodaconsulta",
                native_enum=False,
                length=16,
            ),
            nullable=False,
        ),
        sa.Column("pergunta", sa.Text(), nullable=False),
        sa.Column("resposta", sa.Text(), nullable=False),
        sa.Column("autor_id", sa.Uuid(), nullable=False),
        sa.Column("papel_do_autor", sa.String(length=32), nullable=False),
        sa.Column(
            "registrado_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["autor_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["equipe_id"], ["equipe.id"]),
        sa.ForeignKeyConstraint(["guerreiro_id"], ["persona.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.CheckConstraint(
            "(equipe_id IS NOT NULL AND guerreiro_id IS NULL) OR "
            "(equipe_id IS NULL AND guerreiro_id IS NOT NULL)",
            name="ck_consulta_ao_assistente_equipe_ou_guerreiro",
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("consulta_ao_assistente")
