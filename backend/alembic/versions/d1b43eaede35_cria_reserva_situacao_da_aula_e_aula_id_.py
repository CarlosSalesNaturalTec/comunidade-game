"""cria reserva, situação da aula e aula_id do resultado

Revision ID: d1b43eaede35
Revises: c2d3e4f5a6b7
Create Date: 2026-08-18 12:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d1b43eaede35"
down_revision: str | Sequence[str] | None = "c2d3e4f5a6b7"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # O que a aula precisa, declarado no agendamento — separado da reserva
    # porque a aula pendente de lastro precisa lembrar o que lhe falta
    # (`RF-07-08`, design — Decisions 1).
    op.create_table(
        "recurso_declarado_da_aula",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("aula_id", sa.Uuid(), nullable=False),
        sa.Column("tipo_de_recurso_id", sa.Uuid(), nullable=False),
        sa.Column("quantidade", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.ForeignKeyConstraint(["aula_id"], ["aula.id"]),
        sa.ForeignKeyConstraint(["tipo_de_recurso_id"], ["tipo_de_recurso.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    # O compromisso de saldo que a aula assume ao reservar — nunca um
    # lançamento do livro-razão (`RF-07-08`, `RN-07-01`, design — Decisions
    # 3). O índice composto é o que `disponivel_de` e o `FOR UPDATE` do
    # agendamento concorrente percorrem (design — Decisions 2, 4).
    op.create_table(
        "reserva",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("aula_id", sa.Uuid(), nullable=False),
        sa.Column("tipo_de_recurso_id", sa.Uuid(), nullable=False),
        sa.Column("ponto_de_apoio_id", sa.Uuid(), nullable=False),
        sa.Column("quantidade", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column(
            "estado",
            sa.Enum(
                "reservada",
                "consumida",
                "liberada",
                name="estadodareserva",
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
        sa.ForeignKeyConstraint(["aula_id"], ["aula.id"]),
        sa.ForeignKeyConstraint(["autor_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["ponto_de_apoio_id"], ["ponto_de_apoio.id"]),
        sa.ForeignKeyConstraint(["tipo_de_recurso_id"], ["tipo_de_recurso.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_reserva_tipo_de_recurso_ponto_de_apoio_estado",
        "reserva",
        ["tipo_de_recurso_id", "ponto_de_apoio_id", "estado"],
    )

    # `situacao` nasce confirmada para as linhas existentes — aula sem
    # recurso declarado é aula confirmada (design — Decisions 4, Migration
    # Plan) — e o `server_default` sai depois do preenchimento, que aqui é
    # trivial: o Ciclo 01 ainda não entrou no ar e não há linha em `aula`.
    op.add_column(
        "aula",
        sa.Column(
            "situacao",
            sa.Enum(
                "prevista",
                "pendente_de_lastro",
                "confirmada",
                "realizada",
                "cancelada",
                name="situacaodaaula",
                native_enum=False,
                length=20,
            ),
            nullable=False,
            server_default="confirmada",
        ),
    )
    op.alter_column("aula", "situacao", server_default=None)
    op.add_column("aula", sa.Column("cancelamento_motivo", sa.Text(), nullable=True))

    # `resultado.aula_id` nasce obrigatório, sem etapa de preenchimento: a
    # tabela não tem linha em ambiente algum além dos testes — o núcleo
    # nunca expôs rota que a escrevesse (`RF-07-09`, design — Decisions 8).
    op.add_column("resultado", sa.Column("aula_id", sa.Uuid(), nullable=False))
    op.create_foreign_key("fk_resultado_aula_id_aula", "resultado", "aula", ["aula_id"], ["id"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("fk_resultado_aula_id_aula", "resultado", type_="foreignkey")
    op.drop_column("resultado", "aula_id")
    op.drop_column("aula", "cancelamento_motivo")
    op.drop_column("aula", "situacao")
    op.drop_index("ix_reserva_tipo_de_recurso_ponto_de_apoio_estado", table_name="reserva")
    op.drop_table("reserva")
    op.drop_table("recurso_declarado_da_aula")
