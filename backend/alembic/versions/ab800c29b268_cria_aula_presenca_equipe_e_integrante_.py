"""cria aula presenca equipe e integrante_da_equipe

Revision ID: ab800c29b268
Revises: bfa7ba04387f
Create Date: 2026-08-12 21:15:23.366258

"""

import uuid
from collections.abc import Sequence
from datetime import UTC, datetime

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "ab800c29b268"
down_revision: str | Sequence[str] | None = "bfa7ba04387f"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "aula",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("comunidade_virtual_id", sa.Uuid(), nullable=False),
        sa.Column("inicio_em", sa.DateTime(timezone=True), nullable=False),
        sa.Column("fim_em", sa.DateTime(timezone=True), nullable=False),
        sa.Column("autor_id", sa.Uuid(), nullable=False),
        sa.Column("papel_do_autor", sa.String(length=32), nullable=False),
        sa.Column(
            "registrado_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint("fim_em > inicio_em", name="ck_aula_fim_em_apos_inicio_em"),
        sa.ForeignKeyConstraint(["autor_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["comunidade_virtual_id"], ["comunidade_virtual.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "presenca",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("aula_id", sa.Uuid(), nullable=False),
        sa.Column("guerreiro_id", sa.Uuid(), nullable=False),
        sa.Column(
            "modo",
            sa.Enum(
                "reconhecimento",
                "confirmacao",
                name="mododecomprovacao",
                native_enum=False,
                length=16,
            ),
            nullable=False,
        ),
        sa.Column("confirmador_id", sa.Uuid(), nullable=True),
        sa.Column("momento_do_fato", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "momento_do_registro",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
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
        sa.ForeignKeyConstraint(["aula_id"], ["aula.id"]),
        sa.ForeignKeyConstraint(["autor_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["confirmador_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["guerreiro_id"], ["persona.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("aula_id", "guerreiro_id", name="uq_presenca_aula_id_guerreiro_id"),
    )

    # Vínculo com a aula ou com a trilha, nunca os dois — restrição de
    # banco, não só de regra, no mesmo padrão de `etiqueta_ods` (design —
    # decisões).
    op.create_table(
        "equipe",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("aula_id", sa.Uuid(), nullable=True),
        sa.Column("trilha_id", sa.Uuid(), nullable=True),
        sa.Column("homologado_por_id", sa.Uuid(), nullable=True),
        sa.Column("homologado_em", sa.DateTime(timezone=True), nullable=True),
        sa.Column("autor_id", sa.Uuid(), nullable=False),
        sa.Column("papel_do_autor", sa.String(length=32), nullable=False),
        sa.Column(
            "registrado_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "(aula_id IS NOT NULL AND trilha_id IS NULL) OR "
            "(aula_id IS NULL AND trilha_id IS NOT NULL)",
            name="ck_equipe_aula_ou_trilha",
        ),
        sa.ForeignKeyConstraint(["aula_id"], ["aula.id"]),
        sa.ForeignKeyConstraint(["autor_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["homologado_por_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["trilha_id"], ["trilha.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "integrante_da_equipe",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("equipe_id", sa.Uuid(), nullable=False),
        sa.Column("persona_id", sa.Uuid(), nullable=False),
        sa.Column("papel", sa.String(length=64), nullable=True),
        sa.Column(
            "entrou_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["equipe_id"], ["equipe.id"]),
        sa.ForeignKeyConstraint(["persona_id"], ["persona.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "equipe_id", "persona_id", name="uq_integrante_da_equipe_equipe_id_persona_id"
        ),
    )

    # `equipe_id` nasce anulável para o backfill abaixo poder rodar; vira
    # obrigatória só depois de toda criação original existente apontar
    # para uma equipe (design — Migration Plan).
    op.add_column("criacao_original", sa.Column("equipe_id", sa.Uuid(), nullable=True))

    conexao = op.get_bind()
    metadados = sa.MetaData()
    criacao_original = sa.Table("criacao_original", metadados, autoload_with=conexao)
    equipe = sa.Table("equipe", metadados, autoload_with=conexao)
    integrante_da_equipe = sa.Table("integrante_da_equipe", metadados, autoload_with=conexao)

    momento = datetime.now(UTC)
    linhas = conexao.execute(
        sa.select(
            criacao_original.c.id,
            criacao_original.c.trilha_id,
            criacao_original.c.autor_id,
            criacao_original.c.papel_do_autor,
        )
    ).fetchall()
    for linha in linhas:
        # Cada criação original existente vira uma equipe da trilha já
        # homologada, de um único integrante — o próprio autor. Nenhuma
        # autoria se perde, e o registro migrado continua respondendo
        # "quem criou isto" com a mesma pessoa (`RN-01-13`, design —
        # Migration Plan).
        equipe_id = uuid.uuid4()
        conexao.execute(
            equipe.insert().values(
                id=equipe_id,
                trilha_id=linha.trilha_id,
                homologado_por_id=linha.autor_id,
                homologado_em=momento,
                autor_id=linha.autor_id,
                papel_do_autor=linha.papel_do_autor,
                registrado_em=momento,
            )
        )
        conexao.execute(
            integrante_da_equipe.insert().values(
                id=uuid.uuid4(),
                equipe_id=equipe_id,
                persona_id=linha.autor_id,
                entrou_em=momento,
            )
        )
        conexao.execute(
            criacao_original.update()
            .where(criacao_original.c.id == linha.id)
            .values(equipe_id=equipe_id)
        )

    op.alter_column("criacao_original", "equipe_id", nullable=False)
    op.drop_constraint("uq_criacao_original_autor_id_trilha_id", "criacao_original", type_="unique")
    op.create_unique_constraint("uq_criacao_original_equipe_id", "criacao_original", ["equipe_id"])
    op.create_foreign_key(
        "fk_criacao_original_equipe_id_equipe",
        "criacao_original",
        "equipe",
        ["equipe_id"],
        ["id"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    # A ordem inversa devolve a unicidade antiga sem perda, porque o
    # `autor_id` de cada criação original nunca deixou de existir; as
    # equipes criadas no backfill ficam órfãs de uso e somem junto com a
    # coluna (design — Migration Plan).
    op.drop_constraint(
        "fk_criacao_original_equipe_id_equipe", "criacao_original", type_="foreignkey"
    )
    op.drop_constraint("uq_criacao_original_equipe_id", "criacao_original", type_="unique")
    op.create_unique_constraint(
        "uq_criacao_original_autor_id_trilha_id",
        "criacao_original",
        ["autor_id", "trilha_id"],
    )
    op.drop_column("criacao_original", "equipe_id")

    op.drop_table("integrante_da_equipe")
    op.drop_table("equipe")
    op.drop_table("presenca")
    op.drop_table("aula")
