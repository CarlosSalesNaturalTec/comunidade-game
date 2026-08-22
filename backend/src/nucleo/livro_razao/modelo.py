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


class DestinacaoDoAporte(enum.StrEnum):
    """O que separa o que vira lastro do que não vira: a destinação
    `ressarcimento` credita reconhecimento sem creditar estoque
    (`RF-07-23`, `RN-07-38`, PRD-07 §8)."""

    lastro = "lastro"
    ressarcimento = "ressarcimento"


class Lancamento(Base, ComAutoria):
    """A unidade do livro-razão: cada entrada e cada saída de recurso, por
    tipo e ponto de apoio, em `NUMERIC(12, 2)` exato (`RF-07-19`, `RN-07-04`,
    `RN-07-36`). Somente inserção — os _listeners_ abaixo recusam `UPDATE`
    e `DELETE` também dentro do ORM, além do _trigger_ da migração
    (`RN-07-15`, design — Decisions 3).

    `lancamento_original_id` e `motivo_do_ajuste` só existem no lançamento
    de natureza `ajuste`: a correção referencia o original, sem alterá-lo
    (design — Decisions 9). `aula_id` só existe no débito emitido pela
    baixa da reserva — crédito e ajuste não a declaram, e débito gravado
    antes desta coluna fica sem aula, por ser somente inserção
    (`RF-07-16`, `RN-07-15`, design — Decisions 3, 4).

    `lancamento_relacionado_id` só existe no par de uma **transferência**
    entre pontos de apoio: o débito na origem e o crédito no destino se
    referenciam mutuamente, cada um já sabendo o `id` do outro desde a
    criação — a coluna é `DEFERRABLE INITIALLY DEFERRED` porque os dois só
    existem, um para o outro, dentro da mesma operação, e `lancamento` é
    somente inserção (`RF-07-19`, `RN-07-15`, design — Decisions 1).

    `destinacao` herda a do aporte que gerou o crédito, e o ajuste herda a
    do lançamento que referencia — é a coluna local que `saldo_de` filtra,
    sem junção com `aporte` (`RF-07-23`, `RN-07-38`, design — Decisions 2).
    O ajuste que reverte um ressarcimento grava **quantidade zero**: reverte
    moedas sem desfazer um consumo que já aconteceu (`RF-07-25`, design —
    Decisions 1).
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
    lancamento_relacionado_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid,
        ForeignKey("lancamento.id", deferrable=True, initially="DEFERRED"),
        nullable=True,
    )
    aula_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, ForeignKey("aula.id"), nullable=True)
    destinacao: Mapped[DestinacaoDoAporte] = mapped_column(
        Enum(DestinacaoDoAporte, native_enum=False, length=16),
        nullable=False,
        default=DestinacaoDoAporte.lastro,
        server_default=DestinacaoDoAporte.lastro.value,
    )

    __table_args__ = (
        Index(
            "ix_lancamento_tipo_de_recurso_ponto_de_apoio",
            "tipo_de_recurso_id",
            "ponto_de_apoio_id",
        ),
        Index("ix_lancamento_aula_id", "aula_id"),
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
