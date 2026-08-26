"""valor_debitado e encerrada_em da ocorrencia de conduta

Revision ID: c3d4e5f6a7b8
Revises: b2c3d4e5f6a7
Create Date: 2026-08-25 20:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c3d4e5f6a7b8"
down_revision: str | Sequence[str] | None = "b2c3d4e5f6a7"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_FUNCAO_ANTIGA = """
CREATE FUNCTION recusar_alteracao_de_ocorrencia_de_conduta() RETURNS trigger AS $$
BEGIN
    RAISE EXCEPTION
        'ocorrencia_de_conduta é somente inserção: UPDATE e DELETE não são permitidos';
END;
$$ LANGUAGE plpgsql;
"""


def upgrade() -> None:
    """Upgrade schema."""
    # `valor_debitado` nasce preenchido com o nominal (`valor`) — é o que
    # havia para gravar antes desta migração; a decisão do fundador de
    # 2026-08-25 (o ranking devolve o debitado, não o nominal) alcança só
    # quem existir depois dela (design — Migration Plan, riscos).
    # `encerrada_em` nasce vazio em tudo — nenhum ciclo foi encerrado ainda.
    op.add_column("ocorrencia_de_conduta", sa.Column("valor_debitado", sa.Integer(), nullable=True))
    op.add_column(
        "ocorrencia_de_conduta",
        sa.Column("encerrada_em", sa.DateTime(timezone=True), nullable=True),
    )
    op.execute("UPDATE ocorrencia_de_conduta SET valor_debitado = valor")
    op.alter_column("ocorrencia_de_conduta", "valor_debitado", nullable=False)

    # O _trigger_ passa a admitir exatamente o `UPDATE` do expurgo do fim de
    # ciclo — anula `motivo`, carimba `encerrada_em`, e nenhuma outra coluna
    # muda junto; todo o resto continua recusado, `DELETE` incluído (design
    # — decisão 2, `RF-02-100`).
    op.execute(
        """
        DROP TRIGGER trg_ocorrencia_de_conduta_somente_insercao ON ocorrencia_de_conduta;
        DROP FUNCTION recusar_alteracao_de_ocorrencia_de_conduta();

        CREATE FUNCTION recusar_alteracao_de_ocorrencia_de_conduta() RETURNS trigger AS $$
        BEGIN
            IF TG_OP = 'UPDATE'
                AND OLD.motivo IS NOT NULL AND NEW.motivo IS NULL
                AND OLD.encerrada_em IS NULL AND NEW.encerrada_em IS NOT NULL
                AND NEW.valor IS NOT DISTINCT FROM OLD.valor
                AND NEW.valor_debitado IS NOT DISTINCT FROM OLD.valor_debitado
                AND NEW.guerreiro_id IS NOT DISTINCT FROM OLD.guerreiro_id
                AND NEW.aula_id IS NOT DISTINCT FROM OLD.aula_id
                AND NEW.atividade_id IS NOT DISTINCT FROM OLD.atividade_id
                AND NEW.autor_id IS NOT DISTINCT FROM OLD.autor_id
                AND NEW.papel_do_autor IS NOT DISTINCT FROM OLD.papel_do_autor
                AND NEW.momento_do_fato IS NOT DISTINCT FROM OLD.momento_do_fato
                AND NEW.momento_do_registro IS NOT DISTINCT FROM OLD.momento_do_registro
            THEN
                RETURN NEW;
            END IF;
            RAISE EXCEPTION
                'ocorrencia_de_conduta é somente inserção: só o expurgo do fim de ciclo altera '
                'motivo e encerrada_em, e nenhuma outra coluna junto';
        END;
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER trg_ocorrencia_de_conduta_somente_insercao
        BEFORE UPDATE OR DELETE ON ocorrencia_de_conduta
        FOR EACH ROW EXECUTE FUNCTION recusar_alteracao_de_ocorrencia_de_conduta();
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Segura só enquanto nenhum ciclo foi encerrado: depois dela, o motivo
    # expurgado não volta, por desenho (design — Migration Plan).
    op.execute(
        f"""
        DROP TRIGGER trg_ocorrencia_de_conduta_somente_insercao ON ocorrencia_de_conduta;
        DROP FUNCTION recusar_alteracao_de_ocorrencia_de_conduta();
        {_FUNCAO_ANTIGA}
        CREATE TRIGGER trg_ocorrencia_de_conduta_somente_insercao
        BEFORE UPDATE OR DELETE ON ocorrencia_de_conduta
        FOR EACH ROW EXECUTE FUNCTION recusar_alteracao_de_ocorrencia_de_conduta();
        """
    )
    op.drop_column("ocorrencia_de_conduta", "encerrada_em")
    op.drop_column("ocorrencia_de_conduta", "valor_debitado")
