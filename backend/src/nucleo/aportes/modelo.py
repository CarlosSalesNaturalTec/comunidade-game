import enum
import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy import Boolean, Date, Enum, ForeignKey, Integer, Numeric, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from ..autoria import ComAutoria
from ..banco import Base


class FormaDeAporte(enum.StrEnum):
    """As quatro formas do PRD-07 §8."""

    financeira = "financeira"
    material = "material"
    servico = "servico"
    absorcao = "absorcao"


class OrigemDoRegistro(enum.StrEnum):
    """Nasce com as duas origens que esta fatia alcança; a terceira do
    PRD-07 §8 — App 08 — é de fatia futura (design — Decisions 6)."""

    gestao = "gestao"
    pre_cadastro = "pre_cadastro"


class SituacaoDeRessarcimento(enum.StrEnum):
    """Nasce com `ressarcido` ainda inalcançável nesta fatia, no precedente
    do `ativo` do ponto de apoio (design — Decisions 6)."""

    nao_se_aplica = "nao_se_aplica"
    em_aberto = "em_aberto"
    ressarcido = "ressarcido"


class Aporte(Base, ComAutoria):
    """O registro do que entra, em nome de quem proveu, valorado em moedas
    pela vigência da tabela **na data do aporte** (`RF-07-04`, `RF-07-05`,
    PRD-07 §8). `valor_em_moedas` é gravado no ato e nunca recalculado —
    mudar o valor de referência depois não reescreve aporte já registrado
    (`RN-07-03`, design — Decisions 8). `valor_de_origem` é a segunda face
    do valor — reais, nunca exibida em rota pública (PRD-07 §8).

    `admin_homologador_id` fica vazio na absorção, que credita sem
    homologação (`RN-07-35`). `solicitacao_de_participacao_id` é único: a
    mesma declaração do pré-cadastro não credita duas vezes (`RN-07-21`,
    design — Decisions 10).
    """

    __tablename__ = "aporte"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    provedor_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("persona.id"), nullable=False)
    tipo_de_recurso_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("tipo_de_recurso.id"), nullable=False
    )
    quantidade: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    ponto_de_apoio_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("ponto_de_apoio.id"), nullable=False
    )
    valor_em_moedas: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    valor_de_origem: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    forma: Mapped[FormaDeAporte] = mapped_column(
        Enum(FormaDeAporte, native_enum=False, length=16), nullable=False
    )
    origem_do_registro: Mapped[OrigemDoRegistro] = mapped_column(
        Enum(OrigemDoRegistro, native_enum=False, length=16), nullable=False
    )
    solicitacao_de_participacao_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("solicitacao_de_participacao.id"), unique=True, nullable=True
    )
    ressarcivel: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    situacao_de_ressarcimento: Mapped[SituacaoDeRessarcimento] = mapped_column(
        Enum(SituacaoDeRessarcimento, native_enum=False, length=16), nullable=False
    )
    periodo_apurado: Mapped[date | None] = mapped_column(Date, nullable=True)
    comprovante_referencia: Mapped[str | None] = mapped_column(String(512), nullable=True)
    comprovante_nome_original: Mapped[str | None] = mapped_column(String(256), nullable=True)
    comprovante_tipo: Mapped[str | None] = mapped_column(String(128), nullable=True)
    comprovante_tamanho: Mapped[int | None] = mapped_column(Integer, nullable=True)
    admin_homologador_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("persona.id"), nullable=True
    )
    lancamento_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("lancamento.id"), nullable=False
    )
    data_do_aporte: Mapped[date] = mapped_column(Date, nullable=False)
