"""papel do poder, serie_de_coleta e registro_de_coleta (particionado)

Revision ID: a4b5c6d7e8f9
Revises: c9a1f4b7e3d2
Create Date: 2026-08-14 16:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a4b5c6d7e8f9"
down_revision: str | Sequence[str] | None = "c9a1f4b7e3d2"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # O papel é opcional — a maioria dos poderes não exerce papel algum — e
    # o índice único parcial garante no máximo um poder com o papel do
    # Território (RN-01-54).
    op.add_column(
        "poder",
        sa.Column(
            "papel",
            sa.Enum("territorio", name="papeldopoder", native_enum=False, length=16),
            nullable=True,
        ),
    )
    op.create_index(
        "uq_poder_papel_territorio",
        "poder",
        ["papel"],
        unique=True,
        postgresql_where=sa.text("papel = 'territorio'"),
    )

    # O ponto regular nasceu só por trilha; a coleta credita direto ao Poder
    # do Território, nunca à trilha em que o desafio nasceu (RN-08-15) — o
    # mesmo par de referências que `badge` já tem (RF-08-09, design —
    # decisões, serie-registro-e-pontuacao-da-coleta).
    op.add_column("ponto_regular", sa.Column("poder_id", sa.Uuid(), nullable=True))
    op.alter_column("ponto_regular", "trilha_id", nullable=True)
    op.create_foreign_key(
        "fk_ponto_regular_poder_id_poder", "ponto_regular", "poder", ["poder_id"], ["id"]
    )
    op.create_unique_constraint(
        "uq_ponto_regular_guerreiro_id_poder_id", "ponto_regular", ["guerreiro_id", "poder_id"]
    )
    op.create_check_constraint(
        "ck_ponto_regular_trilha_ou_poder",
        "ponto_regular",
        "(trilha_id IS NOT NULL) != (poder_id IS NOT NULL)",
    )

    # Nasce ativa e nesta fatia não transita: a interrupção e o encerramento
    # são RF-08-10 e RF-08-11, de entrega posterior (proposal.md).
    op.create_table(
        "serie_de_coleta",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("desafio_de_coleta_id", sa.Uuid(), nullable=False),
        sa.Column("coletor_id", sa.Uuid(), nullable=False),
        sa.Column("local_id", sa.Uuid(), nullable=False),
        sa.Column(
            "cadencia",
            sa.Enum("diaria", "semanal", "mensal", name="cadencia", native_enum=False, length=16),
            nullable=False,
        ),
        sa.Column(
            "estado",
            sa.Enum("ativa", name="estadodaserie", native_enum=False, length=16),
            nullable=False,
        ),
        sa.Column(
            "aberta_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("ultima_medicao_valida_em", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["coletor_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["desafio_de_coleta_id"], ["desafio_de_coleta.id"]),
        sa.ForeignKeyConstraint(["local_id"], ["local.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "coletor_id",
            "desafio_de_coleta_id",
            "local_id",
            name="uq_serie_de_coleta_coletor_desafio_local",
        ),
    )

    # Particionada por RANGE em `momento_do_fato` (documento 03 §1): a chave
    # de particionamento precisa integrar a chave primária, daí o par
    # (id, momento_do_fato) em vez de `id` sozinho (design — decisões).
    op.create_table(
        "registro_de_coleta",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("momento_do_fato", sa.DateTime(timezone=True), nullable=False),
        sa.Column("serie_de_coleta_id", sa.Uuid(), nullable=False),
        sa.Column("valor", sa.Float(), nullable=True),
        sa.Column("unidade", sa.String(length=32), nullable=True),
        sa.Column("midia_referencia", sa.Text(), nullable=True),
        sa.Column(
            "origem",
            sa.Enum(
                "manual", "voz", "sensor", name="origemdoregistro", native_enum=False, length=16
            ),
            nullable=False,
        ),
        sa.Column(
            "situacao",
            sa.Enum("valida", name="situacaodoregistro", native_enum=False, length=16),
            nullable=False,
        ),
        sa.Column("a_conferir", sa.Boolean(), nullable=False),
        sa.Column("comunidade_virtual_id", sa.Uuid(), nullable=False),
        sa.Column("pontos_creditados", sa.Integer(), nullable=False),
        sa.Column("autor_id", sa.Uuid(), nullable=False),
        sa.Column("papel_do_autor", sa.String(length=32), nullable=False),
        sa.Column(
            "registrado_em",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "momento_do_registro",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["autor_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["comunidade_virtual_id"], ["comunidade_virtual.id"]),
        sa.ForeignKeyConstraint(["serie_de_coleta_id"], ["serie_de_coleta.id"]),
        sa.PrimaryKeyConstraint("id", "momento_do_fato"),
        postgresql_partition_by="RANGE (momento_do_fato)",
    )
    # Anos do Ciclo 01 (ago–dez/2026) mais a partição padrão, que recebe o
    # que cair fora deles — guardar em partição pior é melhor que recusar a
    # medição (design — riscos).
    op.execute(
        """
        CREATE TABLE registro_de_coleta_2026 PARTITION OF registro_de_coleta
            FOR VALUES FROM ('2026-01-01 00:00:00+00') TO ('2027-01-01 00:00:00+00');
        """
    )
    op.execute("CREATE TABLE registro_de_coleta_default PARTITION OF registro_de_coleta DEFAULT;")


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("registro_de_coleta")
    op.drop_table("serie_de_coleta")

    op.drop_constraint("ck_ponto_regular_trilha_ou_poder", "ponto_regular", type_="check")
    op.drop_constraint("uq_ponto_regular_guerreiro_id_poder_id", "ponto_regular", type_="unique")
    op.drop_constraint("fk_ponto_regular_poder_id_poder", "ponto_regular", type_="foreignkey")
    op.alter_column("ponto_regular", "trilha_id", nullable=False)
    op.drop_column("ponto_regular", "poder_id")

    op.drop_index("uq_poder_papel_territorio", table_name="poder")
    op.drop_column("poder", "papel")
