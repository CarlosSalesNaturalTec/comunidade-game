"""auditoria e estorno da coleta

Revision ID: a7b8c9d0e1f2
Revises: f3a4b5c6d7e8
Create Date: 2026-08-17 16:38:40.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a7b8c9d0e1f2"
down_revision: str | Sequence[str] | None = "f3a4b5c6d7e8"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # A auditoria do Mestre (`RF-08-13`, `RF-08-29`): colunas nulas — o
    # registro já gravado nasce não auditado. `ADD COLUMN` anulável em
    # tabela particionada propaga às partições sem reescrever dado, o mesmo
    # padrão de `credencial_id` na migração anterior. `situacao` já é
    # `VARCHAR` sem `CHECK` — `native_enum=False` não cria um —, então o
    # valor novo `invalidada` não exige alterar restrição alguma.
    op.add_column(
        "registro_de_coleta", sa.Column("auditado_em", sa.DateTime(timezone=True), nullable=True)
    )
    op.add_column("registro_de_coleta", sa.Column("auditado_por_id", sa.Uuid(), nullable=True))
    op.add_column(
        "registro_de_coleta",
        sa.Column("motivo_da_invalidacao", sa.String(length=512), nullable=True),
    )
    op.create_foreign_key(
        "fk_registro_de_coleta_auditado_por_id_persona",
        "registro_de_coleta",
        "persona",
        ["auditado_por_id"],
        ["id"],
    )

    # A trava estreita: recusa só o total negativo — o piso em zero de
    # `RN-01-55` —, não mais toda redução; o débito por fato desfeito passa
    # a ser aceito (`RF-01-57`, `RF-01-69`, design — decisão 2). O gatilho
    # não precisa ser recriado, porque aponta para a função pelo nome.
    op.execute(
        """
        CREATE OR REPLACE FUNCTION recusar_debito_de_ponto_regular() RETURNS trigger AS $$
        BEGIN
            IF (TG_OP = 'DELETE') THEN
                RAISE EXCEPTION
                    'ponto regular nunca é debitado: DELETE não é permitido';
            END IF;
            IF NEW.total < 0 THEN
                RAISE EXCEPTION
                    'ponto regular nunca é debitado: total não pode ficar negativo';
            END IF;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Sem retrocompatibilidade a preservar (design — Migration Plan):
    # registro invalidado entre a subida e o rollback perde a marca.
    op.execute(
        """
        CREATE OR REPLACE FUNCTION recusar_debito_de_ponto_regular() RETURNS trigger AS $$
        BEGIN
            IF (TG_OP = 'DELETE') THEN
                RAISE EXCEPTION
                    'ponto regular nunca é debitado: DELETE não é permitido';
            END IF;
            IF NEW.total < OLD.total THEN
                RAISE EXCEPTION
                    'ponto regular nunca é debitado: total não pode diminuir';
            END IF;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        """
    )

    op.drop_constraint(
        "fk_registro_de_coleta_auditado_por_id_persona", "registro_de_coleta", type_="foreignkey"
    )
    op.drop_column("registro_de_coleta", "motivo_da_invalidacao")
    op.drop_column("registro_de_coleta", "auditado_por_id")
    op.drop_column("registro_de_coleta", "auditado_em")
