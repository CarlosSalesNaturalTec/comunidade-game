import enum
import uuid
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Boolean, Date, DateTime, Enum, ForeignKey, Integer, Numeric, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from ..autoria import ComAutoria
from ..banco import Base
from ..livro_razao.modelo import DestinacaoDoAporte


class FormaDeAporte(enum.StrEnum):
    """As quatro formas do PRD-07 §8."""

    financeira = "financeira"
    material = "material"
    servico = "servico"
    absorcao = "absorcao"


class OrigemDoRegistro(enum.StrEnum):
    """`app_08` é a declaração do Apoiador homologada pelo Admin, apontando
    `aporte_declarado_id` (`RF-14-25` a `RF-14-27`, design — Decisions 1)."""

    gestao = "gestao"
    pre_cadastro = "pre_cadastro"
    app_08 = "app_08"


class OrigemDaEscolhaDoAporte(enum.StrEnum):
    """A partir de que o Apoiador declarou o valor (`RF-14-25`, design —
    Decisions 3). `missao` aponta `missao_do_apoiador_id` (`RF-14-63`,
    design — Migration Plan)."""

    missao = "missao"
    necessidade = "necessidade"
    valor_sugerido = "valor_sugerido"
    valor_livre = "valor_livre"


class SituacaoDaDeclaracao(enum.StrEnum):
    pendente = "pendente"
    homologada = "homologada"
    recusada = "recusada"


class SituacaoDeRessarcimento(enum.StrEnum):
    """`ressarcido` é gravado pela capacidade `ressarcimento`, na fatia que
    a alcança (`RF-07-22`, `RF-07-25`)."""

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

    `destinacao` separa o que vira lastro do que não vira (`RF-07-23`,
    `RN-07-38`). `aula_id` só existe na forma absorção, quando o aporte
    declara qual necessidade publicada atende (`RF-07-28`).

    `aporte_declarado_id` é único: a mesma declaração da App 08 não credita
    duas vezes, no mesmo desenho de `solicitacao_de_participacao_id`
    (`RF-14-26`, `RN-14-07`, design — Decisions 2).
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
    destinacao: Mapped[DestinacaoDoAporte] = mapped_column(
        Enum(DestinacaoDoAporte, native_enum=False, length=16),
        nullable=False,
        default=DestinacaoDoAporte.lastro,
        server_default=DestinacaoDoAporte.lastro.value,
    )
    aula_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, ForeignKey("aula.id"), nullable=True)
    aporte_declarado_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("aporte_declarado.id"), unique=True, nullable=True
    )


class AporteDeclarado(Base, ComAutoria):
    """A declaração do Apoiador em sessão de que transferiu dinheiro, à
    espera de homologação (`RF-14-25` a `RF-14-27`, PRD-14 §6.3, design —
    Decisions 1). Nunca gera lançamento, credita saldo ou compõe o Poder
    Sustentador enquanto `pendente` — só `registrar_aporte()`, apontando
    esta declaração como origem, credita (`RN-14-07`).

    `aula_id` e `tipo_de_recurso_id` só existem na origem `necessidade`: o
    par que identifica a necessidade escolhida, sem vínculo — ela é
    derivada e pode deixar de existir até a homologação (design —
    Decisions 3). `motivo_da_recusa`, `resolvido_por_id` e `resolvido_em`
    só existem depois do desfecho, homologação ou recusa.

    `missao_do_apoiador_id` só existe na origem `missao` (`RF-14-63`,
    `RN-14-32`, design — Decisions 1).
    """

    __tablename__ = "aporte_declarado"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    provedor_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("persona.id"), nullable=False)
    valor_declarado: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    origem_da_escolha: Mapped[OrigemDaEscolhaDoAporte] = mapped_column(
        Enum(OrigemDaEscolhaDoAporte, native_enum=False, length=16), nullable=False
    )
    aula_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, ForeignKey("aula.id"), nullable=True)
    tipo_de_recurso_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("tipo_de_recurso.id"), nullable=True
    )
    missao_do_apoiador_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("missao_do_apoiador.id"), nullable=True
    )
    comprovante_referencia: Mapped[str | None] = mapped_column(String(512), nullable=True)
    comprovante_nome_original: Mapped[str | None] = mapped_column(String(256), nullable=True)
    comprovante_tipo: Mapped[str | None] = mapped_column(String(128), nullable=True)
    comprovante_tamanho: Mapped[int | None] = mapped_column(Integer, nullable=True)
    situacao: Mapped[SituacaoDaDeclaracao] = mapped_column(
        Enum(SituacaoDaDeclaracao, native_enum=False, length=16),
        nullable=False,
        default=SituacaoDaDeclaracao.pendente,
    )
    motivo_da_recusa: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    resolvido_por_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("persona.id"), nullable=True
    )
    resolvido_em: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
