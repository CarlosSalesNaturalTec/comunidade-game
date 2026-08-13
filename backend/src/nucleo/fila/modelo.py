import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column

from ..banco import Base


class EmAvaliacao:
    """Mixin do ciclo comum às quatro naturezas da fila — prazo, quem
    avaliou, parecer e data do desfecho (`RF-01-25`, design — Decisions).
    `situacao` fica fora do mixin: o desfecho tem vocabulário próprio em
    cada natureza, e cada modelo declara o seu enum.
    """

    registrado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    prazo: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    avaliado_por_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("persona.id"), nullable=True
    )
    parecer: Mapped[str | None] = mapped_column(Text, nullable=True)
    decidido_em: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class SituacaoDaSolicitacao(enum.StrEnum):
    recebida = "recebida"
    em_avaliacao = "em_avaliacao"
    aceita = "aceita"
    recusada = "recusada"


class SituacaoDaSugestao(enum.StrEnum):
    recebida = "recebida"
    em_avaliacao = "em_avaliacao"
    adotada = "adotada"
    nao_adotada = "nao_adotada"


class PretensaoDeParticipacao(enum.StrEnum):
    mestre = "mestre"
    apoiador = "apoiador"


class TipoDeAlvo(enum.StrEnum):
    atividade = "atividade"
    trilha = "trilha"
    plataforma = "plataforma"


class SolicitacaoDeParticipacao(Base, EmAvaliacao):
    """Atributos do PRD-01 §8. O pré-cadastro do Apoiador — aporte declarado
    e comprovante — só se aplica à pretensão `apoiador`; a plataforma nunca
    coleta CPF, CNPJ ou documento de identidade (`RN-01-28`, `RN-01-29`).
    """

    __tablename__ = "solicitacao_de_participacao"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    situacao: Mapped[SituacaoDaSolicitacao] = mapped_column(
        Enum(SituacaoDaSolicitacao, native_enum=False, length=16),
        nullable=False,
        default=SituacaoDaSolicitacao.recebida,
    )
    nome_ou_razao_social: Mapped[str] = mapped_column(String(256), nullable=False)
    email: Mapped[str] = mapped_column(String(256), nullable=False)
    whatsapp: Mapped[str] = mapped_column(String(32), nullable=False)
    pretensao: Mapped[PretensaoDeParticipacao] = mapped_column(
        Enum(PretensaoDeParticipacao, native_enum=False, length=16), nullable=False
    )
    apresentacao: Mapped[str] = mapped_column(Text, nullable=False)
    instituicao: Mapped[str | None] = mapped_column(String(256), nullable=True)
    links: Mapped[str | None] = mapped_column(Text, nullable=True)
    aporte_declarado: Mapped[str | None] = mapped_column(Text, nullable=True)
    comprovante_referencia: Mapped[str | None] = mapped_column(String(512), nullable=True)
    comprovante_nome_original: Mapped[str | None] = mapped_column(String(256), nullable=True)
    comprovante_tipo: Mapped[str | None] = mapped_column(String(128), nullable=True)
    comprovante_tamanho: Mapped[int | None] = mapped_column(Integer, nullable=True)


class SolicitacaoDeDados(Base, EmAvaliacao):
    """Atributos do PRD-01 §8. A entrega do conjunto é guarda desta fatia
    (`RF-01-47`); a geração do arquivo é do PRD-08 (proposal.md)."""

    __tablename__ = "solicitacao_de_dados"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    situacao: Mapped[SituacaoDaSolicitacao] = mapped_column(
        Enum(SituacaoDaSolicitacao, native_enum=False, length=16),
        nullable=False,
        default=SituacaoDaSolicitacao.recebida,
    )
    solicitante: Mapped[str] = mapped_column(String(256), nullable=False)
    instituicao: Mapped[str] = mapped_column(String(256), nullable=False)
    email: Mapped[str] = mapped_column(String(256), nullable=False)
    finalidade_declarada: Mapped[str] = mapped_column(Text, nullable=False)
    recorte_pedido: Mapped[str] = mapped_column(Text, nullable=False)
    entregue: Mapped[str | None] = mapped_column(Text, nullable=True)


class SolicitacaoDeChave(Base, EmAvaliacao):
    """Atributos do PRD-01 §8, na redação de `RF-01-49`. Não emite chave —
    a emissão é `RF-01-50`, de fatia seguinte —, e não tem freio por origem
    (`RN-01-46`)."""

    __tablename__ = "solicitacao_de_chave"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    situacao: Mapped[SituacaoDaSolicitacao] = mapped_column(
        Enum(SituacaoDaSolicitacao, native_enum=False, length=16),
        nullable=False,
        default=SituacaoDaSolicitacao.recebida,
    )
    solicitante: Mapped[str] = mapped_column(String(256), nullable=False)
    contato: Mapped[str] = mapped_column(String(256), nullable=False)
    instituicao: Mapped[str | None] = mapped_column(String(256), nullable=True)
    o_que_pretende_construir: Mapped[str] = mapped_column(Text, nullable=False)


class SugestaoOuProposta(Base, EmAvaliacao):
    """Atributos do PRD-01 §8. Só guarda texto — o áudio é descartado na
    transcrição antes de chegar ao núcleo (03 §12.2). `creditado_em` é a
    marca que torna o crédito da adoção idempotente pela própria linha
    (`RF-01-56`, design — Decisions); `descartar_em` é a data de descarte
    da transcrição não adotada, 90 dias após o retorno (03 §12.2)."""

    __tablename__ = "sugestao_ou_proposta"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    situacao: Mapped[SituacaoDaSugestao] = mapped_column(
        Enum(SituacaoDaSugestao, native_enum=False, length=16),
        nullable=False,
        default=SituacaoDaSugestao.recebida,
    )
    autor_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("persona.id"), nullable=False)
    papel_do_autor: Mapped[str] = mapped_column(String(32), nullable=False)
    alvo_tipo: Mapped[TipoDeAlvo] = mapped_column(
        Enum(TipoDeAlvo, native_enum=False, length=16), nullable=False
    )
    alvo_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, nullable=True)
    texto: Mapped[str] = mapped_column(Text, nullable=False)
    motivo_do_retorno: Mapped[str | None] = mapped_column(Text, nullable=True)
    creditado_em: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    descartar_em: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
