import uuid
from datetime import datetime

from sqlalchemy import DDL, DateTime, ForeignKey, Integer, Text, Uuid, event
from sqlalchemy.orm import Mapped, mapped_column

from ..autoria import ComAutoria
from ..banco import Base
from ..erros import OcorrenciaDeCondutaImutavel
from ..tempo import ComMomentoDoFato


class OcorrenciaDeConduta(Base, ComAutoria, ComMomentoDoFato):
    """Registro do fato de má conduta lançado pelo Mestre autor da atividade
    ou pelo Admin — a segunda causa de débito de ponto regular, ao lado do
    estorno de coleta invalidada (`RF-09-46`, `RF-01-57`, 11 §5).

    `valor` é gravado a partir da constante da regra em vez de derivado na
    leitura: o `RN-01-52` exige que o lançamento sobreviva com valor, data e
    autor depois de o motivo sumir, e uma tabela de valores que mude de
    vigência não pode reescrever o passado (design — Decisions 3). `motivo`
    nasce anulável para que o expurgo, quando vier, seja um `UPDATE` para
    `NULL` sem tocar o lançamento — a nulidade existe só para o expurgo
    futuro, e a regra exige o motivo na criação (design — riscos).

    `valor_debitado` grava o que o débito tirou de fato do saldo depois do
    aparo em zero — `valor` é sempre o nominal do documento 11 §5, e os dois
    divergem quando o saldo da trilha era menor que 5 (design — decisão 3).
    `encerrada_em` marca a saída do ranking pelo fim de ciclo — efeito de
    jogo, distinto da guarda do motivo, que é LGPD (design — decisão 4).

    Somente inserção, no padrão de `Lancamento`: os _listeners_ abaixo
    recusam `UPDATE` e `DELETE` também dentro do ORM, além do _trigger_ da
    migração. O expurgo do fim de ciclo passa ao largo do ORM — é um
    `UPDATE` de Core, que não dispara evento de mapper —, e o _trigger_ do
    Postgres é quem admite exatamente essa forma de alteração (design —
    decisão 2).
    """

    __tablename__ = "ocorrencia_de_conduta"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    guerreiro_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("persona.id"), nullable=False)
    aula_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("aula.id"), nullable=False)
    atividade_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("atividade.id"), nullable=False
    )
    valor: Mapped[int] = mapped_column(Integer, nullable=False)
    valor_debitado: Mapped[int] = mapped_column(Integer, nullable=False)
    motivo: Mapped[str | None] = mapped_column(Text, nullable=True)
    encerrada_em: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


def _recusar_alteracao(mapper, connection, target) -> None:
    raise OcorrenciaDeCondutaImutavel()


event.listen(OcorrenciaDeConduta, "before_update", _recusar_alteracao)
event.listen(OcorrenciaDeConduta, "before_delete", _recusar_alteracao)

# O mesmo trigger da migração, preso à criação/remoção da tabela: garante que
# `Base.metadata.create_all()` — caminho que os testes usam, fora do Alembic —
# também recusa `UPDATE` e `DELETE` fora do ORM (mesmo padrão de
# `livro_razao/modelo.py`). A migração mantém a cópia dela própria porque uma
# migração é histórico congelado, e não deve mudar se este arquivo mudar.
event.listen(
    OcorrenciaDeConduta.__table__,
    "after_create",
    DDL(
        """
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
    ),
)
event.listen(
    OcorrenciaDeConduta.__table__,
    "before_drop",
    DDL(
        """
        DROP TRIGGER trg_ocorrencia_de_conduta_somente_insercao ON ocorrencia_de_conduta;
        DROP FUNCTION recusar_alteracao_de_ocorrencia_de_conduta();
        """
    ),
)
