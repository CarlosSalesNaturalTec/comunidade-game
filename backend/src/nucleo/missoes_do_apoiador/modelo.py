import enum
import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy import Date, Enum, ForeignKey, Numeric, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from ..autoria import ComAutoria
from ..banco import Base
from ..selos_do_apoiador.modelo import FamiliaDeSelo


class NivelDeNecessidade(enum.StrEnum):
    """Os quatro níveis do documento 14 §2, ordenados pelo que quebra
    primeiro se faltar (`RF-14-60`, `RF-02-102`)."""

    existir = "existir"
    acontecer = "acontecer"
    reconhecer = "reconhecer"
    permanecer = "permanecer"


class SituacaoDaMissao(enum.StrEnum):
    """Gravada por ato — homologação ou despublicação. Vencida não é
    situação gravada: é `aberta` com o prazo no passado, avaliado na
    leitura (design — Decisions 4)."""

    aberta = "aberta"
    concluida = "concluida"
    despublicada = "despublicada"


class MissaoDoApoiador(Base, ComAutoria):
    """O chamado que a gestão publica a partir de uma necessidade de recurso
    já publicada (`RF-02-102`, `RF-02-103`, `RN-02-31`, `RN-14-31`, design —
    Decisions 1). Aponta o par `aula_id` + `tipo_de_recurso_id` da
    necessidade de origem, o mesmo par que `AporteDeclarado` já guarda, sem
    chave estrangeira para uma necessidade que não existe como registro —
    ela é derivada e pode deixar de estar entre as necessidades depois da
    publicação, sem nada a corrigir (design — Decisions 1, 3).

    `quantidade` é sempre em moedas: o quanto falta é derivado dos aportes
    homologados que apontam esta missão, nunca gravado (`RF-14-61`, design —
    Decisions 2). `autor_id`/`papel_do_autor`, de `ComAutoria`, são o Admin
    que publicou (`RF-02-102`)."""

    __tablename__ = "missao_do_apoiador"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    aula_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("aula.id"), nullable=False)
    tipo_de_recurso_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("tipo_de_recurso.id"), nullable=False
    )
    nivel_de_necessidade: Mapped[NivelDeNecessidade] = mapped_column(
        Enum(NivelDeNecessidade, native_enum=False, length=16), nullable=False
    )
    titulo: Mapped[str] = mapped_column(String(128), nullable=False)
    o_que_se_pede: Mapped[str] = mapped_column(String(512), nullable=False)
    quantidade: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    prazo: Mapped[date] = mapped_column(Date, nullable=False)
    selo_nome: Mapped[str] = mapped_column(String(128), nullable=False)
    selo_familia: Mapped[FamiliaDeSelo] = mapped_column(
        Enum(FamiliaDeSelo, native_enum=False, length=16), nullable=False
    )
    situacao: Mapped[SituacaoDaMissao] = mapped_column(
        Enum(SituacaoDaMissao, native_enum=False, length=16),
        nullable=False,
        default=SituacaoDaMissao.aberta,
    )
