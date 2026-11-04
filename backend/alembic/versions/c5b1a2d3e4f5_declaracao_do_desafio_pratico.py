"""declaracao do desafio pratico: forma, criterio e titulo curto

O desafio de desbloqueio **prático** passa a declarar, ao lado do enunciado
que já tinha, a **forma de comprovação aceita** — uma das seis formas de
entrega do Guerreiro(a) (`RF-09-129`) —, o **critério de aceite** em texto
livre (`RF-09-130`) e um **título curto**, que é o que a vitrine exibe ao lado
do nick (`RF-09-131`).

As três colunas são da própria `missao`, como `tipo_do_desafio_de_desbloqueio`
e `desafio_de_desbloqueio_enunciado` já são: são uma por missão, e só as
perguntas do quiz viraram tabela, porque são muitas.

Todas _nullable_ e **sem _backfill_**: o prático declarado antes desta
exigência segue valendo e fica incompleto até o Mestre autor redeclará-lo
(`RN-09-50`, decisão do fundador de 2026-11-04). Inventar critério e título em
nome dele seria texto que a vitrine exibiria. O teto de 60 caracteres do título
é da coluna **e** da regra (`RN-09-51`).

Revision ID: c5b1a2d3e4f5
Revises: b4a99997fa70
Create Date: 2026-11-04

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "c5b1a2d3e4f5"
down_revision: str | None = "b4a99997fa70"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "missao",
        sa.Column("desafio_pratico_forma_de_comprovacao", sa.String(length=16), nullable=True),
    )
    op.add_column(
        "missao", sa.Column("desafio_pratico_criterio_de_aceite", sa.Text(), nullable=True)
    )
    op.add_column(
        "missao", sa.Column("desafio_pratico_titulo_curto", sa.String(length=60), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("missao", "desafio_pratico_titulo_curto")
    op.drop_column("missao", "desafio_pratico_criterio_de_aceite")
    op.drop_column("missao", "desafio_pratico_forma_de_comprovacao")
