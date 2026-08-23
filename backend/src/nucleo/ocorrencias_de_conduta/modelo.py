import uuid

from sqlalchemy import DDL, ForeignKey, Integer, Text, Uuid, event
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

    Somente inserção, no padrão de `Lancamento`: os _listeners_ abaixo
    recusam `UPDATE` e `DELETE` também dentro do ORM, além do _trigger_ da
    migração.
    """

    __tablename__ = "ocorrencia_de_conduta"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    guerreiro_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("persona.id"), nullable=False)
    aula_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("aula.id"), nullable=False)
    atividade_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("atividade.id"), nullable=False
    )
    valor: Mapped[int] = mapped_column(Integer, nullable=False)
    motivo: Mapped[str | None] = mapped_column(Text, nullable=True)


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
            RAISE EXCEPTION
                'ocorrencia_de_conduta é somente inserção: UPDATE e DELETE não são permitidos';
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
