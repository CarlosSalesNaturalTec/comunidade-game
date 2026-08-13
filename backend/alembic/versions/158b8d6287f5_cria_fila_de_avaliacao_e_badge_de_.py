"""cria fila de avaliacao e badge de protagonismo

Revision ID: 158b8d6287f5
Revises: 92e50a17f93e
Create Date: 2026-08-13 18:44:39.916008

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "158b8d6287f5"
down_revision: str | Sequence[str] | None = "92e50a17f93e"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_COLUNAS_DO_CICLO_COMUM = [
    sa.Column(
        "registrado_em",
        sa.DateTime(timezone=True),
        server_default=sa.text("now()"),
        nullable=False,
    ),
    sa.Column("prazo", sa.DateTime(timezone=True), nullable=False),
    sa.Column("avaliado_por_id", sa.Uuid(), nullable=True),
    sa.Column("parecer", sa.Text(), nullable=True),
    sa.Column("decidido_em", sa.DateTime(timezone=True), nullable=True),
]

_ENUM_SITUACAO_DA_SOLICITACAO = sa.Enum(
    "recebida",
    "em_avaliacao",
    "aceita",
    "recusada",
    name="situacaodasolicitacao",
    native_enum=False,
    length=16,
)


def upgrade() -> None:
    """Upgrade schema."""
    # `TipoDeBadge.de_protagonismo` não exige DDL própria: a coluna
    # `badge.tipo` é `native_enum=False` — VARCHAR(32) sem CHECK de valor —,
    # o mesmo padrão de `de_autoria` (b6fa81f28651). Só a restrição de
    # trilha-ou-poder precisa mudar, porque o badge de protagonismo é a
    # única exceção global (`RN-01-50`).
    op.drop_constraint("ck_badge_trilha_ou_poder", "badge", type_="check")
    op.create_check_constraint(
        "ck_badge_trilha_ou_poder",
        "badge",
        "(tipo = 'de_protagonismo' AND trilha_id IS NULL AND poder_id IS NULL) "
        "OR (tipo != 'de_protagonismo' AND (trilha_id IS NOT NULL) != (poder_id IS NOT NULL))",
    )

    op.create_table(
        "solicitacao_de_participacao",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column(
            "situacao", _ENUM_SITUACAO_DA_SOLICITACAO, nullable=False, server_default="recebida"
        ),
        sa.Column("nome_ou_razao_social", sa.String(length=256), nullable=False),
        sa.Column("email", sa.String(length=256), nullable=False),
        sa.Column("whatsapp", sa.String(length=32), nullable=False),
        sa.Column(
            "pretensao",
            sa.Enum(
                "mestre", "apoiador", name="pretensaodeparticipacao", native_enum=False, length=16
            ),
            nullable=False,
        ),
        sa.Column("apresentacao", sa.Text(), nullable=False),
        sa.Column("instituicao", sa.String(length=256), nullable=True),
        sa.Column("links", sa.Text(), nullable=True),
        sa.Column("aporte_declarado", sa.Text(), nullable=True),
        sa.Column("comprovante_referencia", sa.String(length=512), nullable=True),
        sa.Column("comprovante_nome_original", sa.String(length=256), nullable=True),
        sa.Column("comprovante_tipo", sa.String(length=128), nullable=True),
        sa.Column("comprovante_tamanho", sa.Integer(), nullable=True),
        *_COLUNAS_DO_CICLO_COMUM,
        sa.ForeignKeyConstraint(["avaliado_por_id"], ["persona.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "solicitacao_de_dados",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column(
            "situacao", _ENUM_SITUACAO_DA_SOLICITACAO, nullable=False, server_default="recebida"
        ),
        sa.Column("solicitante", sa.String(length=256), nullable=False),
        sa.Column("instituicao", sa.String(length=256), nullable=False),
        sa.Column("email", sa.String(length=256), nullable=False),
        sa.Column("finalidade_declarada", sa.Text(), nullable=False),
        sa.Column("recorte_pedido", sa.Text(), nullable=False),
        sa.Column("entregue", sa.Text(), nullable=True),
        *_COLUNAS_DO_CICLO_COMUM,
        sa.ForeignKeyConstraint(["avaliado_por_id"], ["persona.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "solicitacao_de_chave",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column(
            "situacao", _ENUM_SITUACAO_DA_SOLICITACAO, nullable=False, server_default="recebida"
        ),
        sa.Column("solicitante", sa.String(length=256), nullable=False),
        sa.Column("contato", sa.String(length=256), nullable=False),
        sa.Column("instituicao", sa.String(length=256), nullable=True),
        sa.Column("o_que_pretende_construir", sa.Text(), nullable=False),
        *_COLUNAS_DO_CICLO_COMUM,
        sa.ForeignKeyConstraint(["avaliado_por_id"], ["persona.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "sugestao_ou_proposta",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column(
            "situacao",
            sa.Enum(
                "recebida",
                "em_avaliacao",
                "adotada",
                "nao_adotada",
                name="situacaodasugestao",
                native_enum=False,
                length=16,
            ),
            nullable=False,
            server_default="recebida",
        ),
        sa.Column("autor_id", sa.Uuid(), nullable=False),
        sa.Column("papel_do_autor", sa.String(length=32), nullable=False),
        sa.Column(
            "alvo_tipo",
            sa.Enum(
                "atividade", "trilha", "plataforma", name="tipodealvo", native_enum=False, length=16
            ),
            nullable=False,
        ),
        sa.Column("alvo_id", sa.Uuid(), nullable=True),
        sa.Column("texto", sa.Text(), nullable=False),
        sa.Column("motivo_do_retorno", sa.Text(), nullable=True),
        sa.Column("creditado_em", sa.DateTime(timezone=True), nullable=True),
        sa.Column("descartar_em", sa.DateTime(timezone=True), nullable=True),
        *_COLUNAS_DO_CICLO_COMUM,
        sa.ForeignKeyConstraint(["autor_id"], ["persona.id"]),
        sa.ForeignKeyConstraint(["avaliado_por_id"], ["persona.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("sugestao_ou_proposta")
    op.drop_table("solicitacao_de_chave")
    op.drop_table("solicitacao_de_dados")
    op.drop_table("solicitacao_de_participacao")

    op.drop_constraint("ck_badge_trilha_ou_poder", "badge", type_="check")
    op.create_check_constraint(
        "ck_badge_trilha_ou_poder",
        "badge",
        "(trilha_id IS NOT NULL) != (poder_id IS NOT NULL)",
    )
