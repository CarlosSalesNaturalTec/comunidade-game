import enum
import uuid
from decimal import Decimal

from sqlalchemy import DDL, Enum, ForeignKey, Index, Numeric, Text, Uuid, event
from sqlalchemy.orm import Mapped, mapped_column

from ..autoria import ComAutoria
from ..banco import Base
from ..erros import LancamentoImutavel


class NaturezaDoLancamento(enum.StrEnum):
    """As três naturezas do movimento de recurso (`RF-07-19`, PRD-07 §8)."""

    credito = "credito"
    debito = "debito"
    ajuste = "ajuste"


class Lancamento(Base, ComAutoria):
    """A unidade do livro-razão: cada entrada e cada saída de recurso, por
    tipo e ponto de apoio, em `NUMERIC(12, 2)` exato (`RF-07-19`, `RN-07-04`,
    `RN-07-36`). Somente inserção — os _listeners_ abaixo recusam `UPDATE`
    e `DELETE` também dentro do ORM, além do _trigger_ da migração
    (`RN-07-15`, design — Decisions 3).

    `lancamento_original_id` e `motivo_do_ajuste` só existem no lançamento
    de natureza `ajuste`: a correção referencia o original, sem alterá-lo
    (design — Decisions 9).
    """

    __tablename__ = "lancamento"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    natureza: Mapped[NaturezaDoLancamento] = mapped_column(
        Enum(NaturezaDoLancamento, native_enum=False, length=16), nullable=False
    )
    tipo_de_recurso_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("tipo_de_recurso.id"), nullable=False
    )
    ponto_de_apoio_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("ponto_de_apoio.id"), nullable=False
    )
    quantidade: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    valor_em_moedas: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    lancamento_original_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("lancamento.id"), nullable=True
    )
    motivo_do_ajuste: Mapped[str | None] = mapped_column(Text, nullable=True)

    __table_args__ = (
        Index(
            "ix_lancamento_tipo_de_recurso_ponto_de_apoio",
            "tipo_de_recurso_id",
            "ponto_de_apoio_id",
        ),
    )


def _recusar_alteracao(mapper, connection, target) -> None:
    raise LancamentoImutavel()


event.listen(Lancamento, "before_update", _recusar_alteracao)
event.listen(Lancamento, "before_delete", _recusar_alteracao)

# O mesmo trigger da migração, preso à criação/remoção da tabela: garante que
# `Base.metadata.create_all()` — caminho que os testes usam, fora do Alembic —
# também recusa `UPDATE` e `DELETE` fora do ORM (mesmo padrão de
# `consentimentos/modelo.py`). A migração mantém a cópia dela própria porque
# uma migração é histórico congelado, e não deve mudar se este arquivo mudar.
event.listen(
    Lancamento.__table__,
    "after_create",
    DDL(
        """
        CREATE FUNCTION recusar_alteracao_de_lancamento() RETURNS trigger AS $$
        BEGIN
            RAISE EXCEPTION
                'lancamento é somente inserção: UPDATE e DELETE não são permitidos';
        END;
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER trg_lancamento_somente_insercao
        BEFORE UPDATE OR DELETE ON lancamento
        FOR EACH ROW EXECUTE FUNCTION recusar_alteracao_de_lancamento();
        """
    ),
)
event.listen(
    Lancamento.__table__,
    "before_drop",
    DDL(
        """
        DROP TRIGGER trg_lancamento_somente_insercao ON lancamento;
        DROP FUNCTION recusar_alteracao_de_lancamento();
        """
    ),
)
