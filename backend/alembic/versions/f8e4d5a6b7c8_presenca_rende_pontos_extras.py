"""a presenca rende 5 pontos extras, e o piso do catalogo sobe a 25

Decisão do fundador de 2026-11-06 (documento 09 §1).

`presenca.pontos_extras_creditados` guarda o que cada presença creditou, e é
o que a anulação estorna (`RF-01-82`, `RF-01-83`). As presenças existentes
ficam em **0**: não há crédito retroativo, e a anulação delas não toca o ponto
extra (`RN-01-65`, design — decisão 1).

O gatilho do ponto extra passa a admitir a redução do acumulado **só** sob o
marcador local à transação `cg.estorno_de_presenca`, que a regra do estorno
liga; o `DELETE` segue recusado sempre (`RN-01-64`, design — decisão 4).

O piso do preço de referência sobe de 20 para 25 (`RF-07-44`, `RN-07-30`).
Antes de trocar o `CHECK`, toda vigência **aberta** abaixo de 25 é encerrada
hoje — ou no próprio início, se ainda não começou — e ganha sucessora de 25,
com o autor da anterior e `papel_do_autor = 'migracao'` (`RF-07-50`, design —
decisão 5). O `CHECK` novo entra `NOT VALID`:
as vigências encerradas de 20 a 24 ficam no histórico, e nenhuma rota as
altera.

Revision ID: f8e4d5a6b7c8
Revises: e7d3c4f5a6b7
Create Date: 2026-11-06

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "f8e4d5a6b7c8"
down_revision: str | None = "e7d3c4f5a6b7"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_FUNCAO_COM_ESTORNO = """
CREATE OR REPLACE FUNCTION recusar_debito_de_ponto_extra() RETURNS trigger AS $$
BEGIN
    IF (TG_OP = 'DELETE') THEN
        RAISE EXCEPTION
            'ponto extra nunca é removido: DELETE não é permitido';
    END IF;
    IF NEW.acumulado < OLD.acumulado
       AND coalesce(current_setting('cg.estorno_de_presenca', true), '') <> 'on' THEN
        RAISE EXCEPTION
            'o acumulado de ponto extra só cresce: não pode diminuir';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
"""

_FUNCAO_ANTERIOR = """
CREATE OR REPLACE FUNCTION recusar_debito_de_ponto_extra() RETURNS trigger AS $$
BEGIN
    IF (TG_OP = 'DELETE') THEN
        RAISE EXCEPTION
            'ponto extra nunca é debitado nesta fatia: DELETE não é permitido';
    END IF;
    IF NEW.acumulado < OLD.acumulado THEN
        RAISE EXCEPTION
            'o acumulado de ponto extra só cresce: não pode diminuir';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
"""


def upgrade() -> None:
    op.add_column(
        "presenca",
        sa.Column("pontos_extras_creditados", sa.Integer(), nullable=False, server_default="0"),
    )

    op.execute(_FUNCAO_COM_ESTORNO)

    op.execute(
        """
        WITH elevadas AS (
            UPDATE preco_de_referencia
               SET vigencia_fim = GREATEST(CURRENT_DATE, vigencia_inicio)
             WHERE vigencia_fim IS NULL
               AND preco_em_pontos_extras < 25
         RETURNING tipo_de_recurso_id, autor_id, vigencia_fim
        )
        INSERT INTO preco_de_referencia (
            id, tipo_de_recurso_id, preco_em_pontos_extras, vigencia_inicio,
            vigencia_fim, autor_id, papel_do_autor
        )
        SELECT gen_random_uuid(), tipo_de_recurso_id, 25, vigencia_fim, NULL,
               autor_id, 'migracao'
          FROM elevadas;
        """
    )
    op.drop_constraint("ck_preco_de_referencia_piso_minimo", "preco_de_referencia", "check")
    op.execute(
        "ALTER TABLE preco_de_referencia ADD CONSTRAINT ck_preco_de_referencia_piso_minimo "
        "CHECK (preco_em_pontos_extras >= 25) NOT VALID"
    )


def downgrade() -> None:
    # As vigências de 25 abertas pela subida ficam: desfazê-las reescreveria
    # o preço que trocas posteriores já cobraram (`RF-07-46`).
    op.drop_constraint("ck_preco_de_referencia_piso_minimo", "preco_de_referencia", "check")
    op.execute(
        "ALTER TABLE preco_de_referencia ADD CONSTRAINT ck_preco_de_referencia_piso_minimo "
        "CHECK (preco_em_pontos_extras >= 20) NOT VALID"
    )
    op.execute(_FUNCAO_ANTERIOR)
    op.drop_column("presenca", "pontos_extras_creditados")
