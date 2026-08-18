"""cria ponto_de_apoio, tipo_de_recurso e valor_de_referencia; aula ganha ponto_de_apoio_id

Revision ID: b8c9d0e1f2a3
Revises: a7b8c9d0e1f2
Create Date: 2026-08-18 09:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b8c9d0e1f2a3"
down_revision: str | Sequence[str] | None = "a7b8c9d0e1f2"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # Nasce sem responsável — quem responde pelo acervo é designado depois,
    # em operação própria (`RF-07-47`, `RF-07-49`). `ativo` nasce verdadeiro
    # e nenhuma operação o muda nesta fatia (design — Decisions 6, Risks).
    op.create_table(
        "ponto_de_apoio",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("nome", sa.String(length=128), nullable=False),
        sa.Column("comunidade_virtual_id", sa.Uuid(), nullable=False),
        sa.Column("responsavel_id", sa.Uuid(), nullable=True),
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
        sa.ForeignKeyConstraint(["comunidade_virtual_id"], ["comunidade_virtual.id"]),
        sa.ForeignKeyConstraint(["responsavel_id"], ["persona.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    # O valor de referência não é coluna daqui: vive em `valor_de_referencia`,
    # versionado por vigência (`RF-07-01`, `RF-07-02`).
    op.create_table(
        "tipo_de_recurso",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("nome", sa.String(length=128), nullable=False),
        sa.Column(
            "natureza",
            sa.Enum(
                "consumivel",
                "duravel",
                "servico",
                "financeiro",
                name="naturezadorecurso",
                native_enum=False,
                length=16,
            ),
            nullable=False,
        ),
        sa.Column("unidade", sa.String(length=32), nullable=False),
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

    # Vigência semiaberta `inicio <= data < fim`; `fim` nula é a vigência
    # aberta. `NUMERIC(12, 2)` é decimal exato — soma e comparação não
    # derivam (`RN-07-04`, design — Decisions 1 e 2).
    op.create_table(
        "valor_de_referencia",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("tipo_de_recurso_id", sa.Uuid(), nullable=False),
        sa.Column("valor_em_moedas", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("vigencia_inicio", sa.Date(), nullable=False),
        sa.Column("vigencia_fim", sa.Date(), nullable=True),
        sa.Column("autor_id", sa.Uuid(), nullable=False),
        sa.Column("papel_do_autor", sa.String(length=32), nullable=False),
        sa.Column(
            "registrado_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "valor_em_moedas >= 0", name="ck_valor_de_referencia_valor_nao_negativo"
        ),
        sa.CheckConstraint(
            "vigencia_fim IS NULL OR vigencia_fim >= vigencia_inicio",
            name="ck_valor_de_referencia_fim_apos_ou_igual_ao_inicio",
        ),
        sa.ForeignKeyConstraint(["autor_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["tipo_de_recurso_id"], ["tipo_de_recurso.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    # `NOT NULL` direto: não há retrocompatibilidade a preservar — a
    # plataforma não está implantada e não há valor de backfill defensável
    # (design — Decisions 3). Esta migração FALHA em base com aulas já
    # gravadas: quem operar precisa cadastrar o ponto de apoio antes e
    # decidir a qual aula cada um pertence — decisão de gestão, não de
    # migration. Não afrouxe a coluna para anulável como remédio.
    op.add_column("aula", sa.Column("ponto_de_apoio_id", sa.Uuid(), nullable=False))
    op.create_foreign_key(
        "fk_aula_ponto_de_apoio_id_ponto_de_apoio",
        "aula",
        "ponto_de_apoio",
        ["ponto_de_apoio_id"],
        ["id"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("fk_aula_ponto_de_apoio_id_ponto_de_apoio", "aula", type_="foreignkey")
    op.drop_column("aula", "ponto_de_apoio_id")
    op.drop_table("valor_de_referencia")
    op.drop_table("tipo_de_recurso")
    op.drop_table("ponto_de_apoio")
