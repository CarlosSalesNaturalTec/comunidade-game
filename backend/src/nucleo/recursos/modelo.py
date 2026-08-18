import enum
import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy import CheckConstraint, Date, Enum, ForeignKey, Numeric, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from ..autoria import ComAutoria
from ..banco import Base


class NaturezaDoRecurso(enum.StrEnum):
    """As quatro naturezas do vocabulário do que a plataforma consome e
    recebe (`RF-07-01`, PRD-07 §8)."""

    consumivel = "consumivel"
    duravel = "duravel"
    servico = "servico"
    financeiro = "financeiro"


class TipoDeRecurso(Base, ComAutoria):
    """O catálogo do que se consome e se recebe — hora-aula, lanche, insumo,
    kit, cloud e afins —, cadastrado por Admin (`RF-07-01`). O valor de
    referência em moedas não é coluna daqui: vive em `ValorDeReferencia`,
    versionado por vigência (`RF-07-02`).
    """

    __tablename__ = "tipo_de_recurso"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    nome: Mapped[str] = mapped_column(String(128), nullable=False)
    natureza: Mapped[NaturezaDoRecurso] = mapped_column(
        Enum(NaturezaDoRecurso, native_enum=False, length=16), nullable=False
    )
    unidade: Mapped[str] = mapped_column(String(32), nullable=False)


class ValorDeReferencia(Base, ComAutoria):
    """O valor em moedas de um tipo de recurso, versionado por vigência
    semiaberta: `vigencia_inicio <= data < vigencia_fim` (`RF-07-02`,
    `RN-07-03`, design — Decisions 2). Abrir vigência nova encerra a
    vigente no dia de início da nova — nunca reescreve nem apaga a
    anterior. `vigencia_fim` nula é a vigência aberta.

    `NUMERIC(12, 2)` é decimal exato: soma e comparação não derivam, e o
    teto de 12 dígitos comporta dez ordens de grandeza acima do Ciclo 01
    (`RN-07-04`, design — Decisions 1).
    """

    __tablename__ = "valor_de_referencia"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    tipo_de_recurso_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("tipo_de_recurso.id"), nullable=False
    )
    valor_em_moedas: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    vigencia_inicio: Mapped[date] = mapped_column(Date, nullable=False)
    vigencia_fim: Mapped[date | None] = mapped_column(Date, nullable=True)

    __table_args__ = (
        CheckConstraint("valor_em_moedas >= 0", name="ck_valor_de_referencia_valor_nao_negativo"),
        CheckConstraint(
            "vigencia_fim IS NULL OR vigencia_fim >= vigencia_inicio",
            name="ck_valor_de_referencia_fim_apos_ou_igual_ao_inicio",
        ),
    )
