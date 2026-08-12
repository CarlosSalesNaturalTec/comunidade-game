"""cria poder trilha missao e atividade

Revision ID: fdfe17ea361e
Revises: 4692973e3186
Create Date: 2026-08-12 12:05:36.116067

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "fdfe17ea361e"
down_revision: str | Sequence[str] | None = "4692973e3186"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "poder",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("nome", sa.String(length=128), nullable=False),
        sa.Column("descricao", sa.Text(), nullable=False),
        sa.Column(
            "natureza",
            sa.Enum(
                "de_guerreiro",
                "derivado_do_aporte",
                name="naturezadopoder",
                native_enum=False,
                length=32,
            ),
            nullable=False,
        ),
        sa.Column(
            "vigencia",
            sa.Enum(
                "vigente",
                "ciclo_futuro",
                name="vigenciadopoder",
                native_enum=False,
                length=16,
            ),
            nullable=False,
        ),
        sa.Column("ativo", sa.Boolean(), nullable=False),
        sa.Column("autor_id", sa.Uuid(), nullable=False),
        sa.Column("papel_do_autor", sa.String(length=32), nullable=False),
        sa.Column(
            "registrado_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["autor_id"], ["persona.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    # Bem comum da plataforma (RN-01-42, design — decisões): nenhuma coluna
    # de comunidade nesta tabela, ao contrário do hábito das fatias
    # anteriores.
    op.create_table(
        "trilha",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("nome", sa.String(length=128), nullable=False),
        sa.Column("objetivo", sa.Text(), nullable=False),
        sa.Column("area_do_conhecimento", sa.String(length=128), nullable=False),
        sa.Column("poder_id", sa.Uuid(), nullable=False),
        sa.Column(
            "situacao",
            sa.Enum(
                "rascunho",
                "publicada",
                name="situacaodatrilha",
                native_enum=False,
                length=16,
            ),
            nullable=False,
        ),
        sa.Column("autor_id", sa.Uuid(), nullable=False),
        sa.Column("papel_do_autor", sa.String(length=32), nullable=False),
        sa.Column(
            "registrado_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["autor_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["poder_id"], ["poder.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "missao",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("trilha_id", sa.Uuid(), nullable=False),
        sa.Column("posicao", sa.Integer(), nullable=False),
        sa.Column("nivel_de_dificuldade", sa.Integer(), nullable=False),
        sa.Column("obrigatoria", sa.Boolean(), nullable=False),
        sa.Column("e_sondagem", sa.Boolean(), nullable=False),
        sa.Column("autor_id", sa.Uuid(), nullable=False),
        sa.Column("papel_do_autor", sa.String(length=32), nullable=False),
        sa.Column(
            "registrado_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["autor_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["trilha_id"], ["trilha.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    # Adiável: reordenar missões (RF-09-02) troca posições e passa por um
    # estado intermediário em que duas dividem a mesma posição; a
    # restrição só é conferida ao fim da transação (design — decisões).
    op.create_unique_constraint(
        "uq_missao_trilha_id_posicao",
        "missao",
        ["trilha_id", "posicao"],
        deferrable=True,
        initially="IMMEDIATE",
    )
    # No máximo uma sondagem por trilha; a primeira posição é conferida na
    # regra (documento 99 §6 invariante 5).
    op.create_index(
        "uq_missao_sondagem_por_trilha",
        "missao",
        ["trilha_id"],
        unique=True,
        postgresql_where=sa.text("e_sondagem"),
    )

    op.create_table(
        "atividade",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("missao_id", sa.Uuid(), nullable=False),
        sa.Column(
            "modalidade",
            sa.Enum(
                "individual",
                "em_equipe",
                "em_equipe_com_familiar",
                name="modalidadedeatividade",
                native_enum=False,
                length=32,
            ),
            nullable=False,
        ),
        sa.Column(
            "formato",
            sa.Enum(
                "presencial",
                "on_line_assincrona",
                name="formatodeatividade",
                native_enum=False,
                length=32,
            ),
            nullable=False,
        ),
        sa.Column("natureza", sa.String(length=64), nullable=False),
        sa.Column("producao_esperada", sa.Text(), nullable=False),
        sa.Column("autor_id", sa.Uuid(), nullable=False),
        sa.Column("papel_do_autor", sa.String(length=32), nullable=False),
        sa.Column(
            "registrado_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["autor_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["missao_id"], ["missao.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("atividade")
    op.drop_index("uq_missao_sondagem_por_trilha", table_name="missao")
    op.drop_constraint("uq_missao_trilha_id_posicao", "missao", type_="unique")
    op.drop_table("missao")
    op.drop_table("trilha")
    op.drop_table("poder")
