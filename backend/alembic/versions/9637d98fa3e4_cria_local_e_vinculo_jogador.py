"""cria local e vinculo_jogador; move a comunidade do guerreiro para o vínculo

Revision ID: 9637d98fa3e4
Revises: b2d3f4a5c6e7
Create Date: 2026-08-14 10:00:00.000000

"""

import uuid
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9637d98fa3e4"
down_revision: str | Sequence[str] | None = "b2d3f4a5c6e7"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # `comunidade_virtual` já existe — só muda de módulo em Python, sem DDL
    # de renomeação (design — Migration Plan).
    op.create_table(
        "local",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("comunidade_virtual_id", sa.Uuid(), nullable=False),
        sa.Column(
            "nivel",
            sa.Enum(
                "comunidade",
                "bairro",
                "rua",
                "condominio",
                "bloco",
                "quadra",
                name="niveldolocal",
                native_enum=False,
                length=16,
            ),
            nullable=False,
        ),
        sa.Column("rotulo", sa.String(length=128), nullable=False),
        sa.Column("local_pai_id", sa.Uuid(), nullable=True),
        sa.Column(
            "criado_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "(nivel = 'comunidade') = (local_pai_id IS NULL)",
            name="ck_local_pai_so_vazio_no_nivel_comunidade",
        ),
        sa.ForeignKeyConstraint(["comunidade_virtual_id"], ["comunidade_virtual.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "id", "comunidade_virtual_id", name="uq_local_id_comunidade_virtual_id"
        ),
    )
    # Chave composta do pai: com ela o próprio banco recusa um pai de outra
    # comunidade, sem que nenhuma regra precise conferir (design —
    # Decisions).
    op.create_foreign_key(
        "fk_local_local_pai_id_comunidade_virtual_id",
        "local",
        "local",
        ["local_pai_id", "comunidade_virtual_id"],
        ["id", "comunidade_virtual_id"],
    )

    op.create_table(
        "vinculo_jogador",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("guerreiro_id", sa.Uuid(), nullable=False),
        sa.Column("comunidade_virtual_id", sa.Uuid(), nullable=False),
        sa.Column(
            "data_inicio",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("data_fim", sa.DateTime(timezone=True), nullable=True),
        sa.Column("admin_responsavel_id", sa.Uuid(), nullable=True),
        sa.ForeignKeyConstraint(["admin_responsavel_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["comunidade_virtual_id"], ["comunidade_virtual.id"]),
        sa.ForeignKeyConstraint(["guerreiro_id"], ["persona.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    # Copia cada vínculo já gravado como vigente, com a data de início igual
    # à criação da persona — a cópia precede a queda da coluna, então
    # RN-01-05 nunca fica sem lastro numa janela da migração (design —
    # Migration Plan).
    conexao = op.get_bind()
    metadados = sa.MetaData()
    persona = sa.Table("persona", metadados, autoload_with=conexao)
    vinculo_jogador = sa.Table("vinculo_jogador", metadados, autoload_with=conexao)

    linhas = conexao.execute(
        sa.select(persona.c.id, persona.c.comunidade_virtual_id, persona.c.criada_em).where(
            persona.c.comunidade_virtual_id.isnot(None)
        )
    ).fetchall()
    for linha in linhas:
        conexao.execute(
            vinculo_jogador.insert().values(
                id=uuid.uuid4(),
                guerreiro_id=linha.id,
                comunidade_virtual_id=linha.comunidade_virtual_id,
                data_inicio=linha.criada_em,
            )
        )

    op.create_index(
        "uq_vinculo_jogador_vigente",
        "vinculo_jogador",
        ["guerreiro_id"],
        unique=True,
        postgresql_where=sa.text("data_fim IS NULL"),
    )

    op.drop_constraint("ck_persona_guerreiro_tem_comunidade", "persona", type_="check")
    op.drop_constraint(
        "fk_persona_comunidade_virtual_id_comunidade_virtual", "persona", type_="foreignkey"
    )
    op.drop_column("persona", "comunidade_virtual_id")


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column("persona", sa.Column("comunidade_virtual_id", sa.Uuid(), nullable=True))
    op.create_foreign_key(
        "fk_persona_comunidade_virtual_id_comunidade_virtual",
        "persona",
        "comunidade_virtual",
        ["comunidade_virtual_id"],
        ["id"],
    )

    conexao = op.get_bind()
    metadados = sa.MetaData()
    persona = sa.Table("persona", metadados, autoload_with=conexao)
    vinculo_jogador = sa.Table("vinculo_jogador", metadados, autoload_with=conexao)

    linhas = conexao.execute(
        sa.select(vinculo_jogador.c.guerreiro_id, vinculo_jogador.c.comunidade_virtual_id).where(
            vinculo_jogador.c.data_fim.is_(None)
        )
    ).fetchall()
    for linha in linhas:
        conexao.execute(
            persona.update()
            .where(persona.c.id == linha.guerreiro_id)
            .values(comunidade_virtual_id=linha.comunidade_virtual_id)
        )

    op.create_check_constraint(
        "ck_persona_guerreiro_tem_comunidade",
        "persona",
        "papel != 'guerreiro' OR comunidade_virtual_id IS NOT NULL",
    )

    op.drop_index(
        "uq_vinculo_jogador_vigente",
        table_name="vinculo_jogador",
        postgresql_where=sa.text("data_fim IS NULL"),
    )
    op.drop_table("vinculo_jogador")

    op.drop_constraint("fk_local_local_pai_id_comunidade_virtual_id", "local", type_="foreignkey")
    op.drop_table("local")
