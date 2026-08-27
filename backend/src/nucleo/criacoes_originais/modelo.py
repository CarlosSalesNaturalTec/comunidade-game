import enum
import uuid
from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    Uuid,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from ..autoria import ComAutoria
from ..banco import Base


class SituacaoDaCriacaoOriginal(enum.StrEnum):
    entregue = "entregue"
    validada = "validada"
    devolvida = "devolvida"


class TipoDeProducaoDaCriacaoOriginal(enum.StrEnum):
    """Os cinco valores que `conteudos.modelo.TipoDeConteudo` já firma,
    replicados aqui porque a criação original é entrega do Guerreiro(a), não
    conteúdo do Mestre — os dois nunca compartilham a mesma tabela (design —
    decisão 4). Texto e link externo trazem o que lhes cabe em `producao`
    no ato da entrega; imagem, vídeo e arquivo nascem sem bytes e os
    recebem depois, pela sessão de envio de `criacoes_originais.regra`.
    """

    texto = "texto"
    imagem = "imagem"
    link_externo = "link_externo"
    video = "video"
    arquivo = "arquivo"


class CriacaoOriginal(Base, ComAutoria):
    """Registro de que a equipe da trilha, ou o próprio Guerreiro(a) na
    modalidade individual, entregou, ao final dela, o que produziu a partir
    do que aprendeu — a Culminância do documento 11 §2. Exatamente um entre
    `equipe_id` e `guerreiro_id` é preenchido, conforme a modalidade
    declarada na culminância da trilha (design — decisão 2); `ComAutoria.
    autor_id` continua a gravar quem entregou — o integrante, na equipe, ou
    o próprio Guerreiro(a), na individual —, e nunca muda, nem na devolução
    nem no reenvio (`RN-01-13`, `RN-05-13`). `producao` guarda o corpo do
    tipo texto ou o endereço do tipo link externo; `referencia` e `tamanho`
    guardam o arquivo dos três tipos de mídia, preenchidos só quando o envio
    conclui (design — decisão 4). `motivo_da_devolucao` é gravado só na
    devolução, e o reenvio não o apaga (design — decisão 6).

    A unicidade é por autor: `equipe_id`, porque cada equipe pertence a uma
    só trilha (`RN-01-44`), e o par `(guerreiro_id, trilha_id)`, porque o
    mesmo Guerreiro(a) participa de várias trilhas (design — decisão 3). A
    nova entrega, antes da validação, substitui a produção existente em vez
    de criar um segundo registro; depois de validada, é recusada.
    """

    __tablename__ = "criacao_original"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    trilha_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("trilha.id"), nullable=False)
    equipe_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("equipe.id"), nullable=True
    )
    guerreiro_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("persona.id"), nullable=True
    )
    tipo: Mapped[TipoDeProducaoDaCriacaoOriginal] = mapped_column(
        Enum(TipoDeProducaoDaCriacaoOriginal, native_enum=False, length=16), nullable=False
    )
    producao: Mapped[str | None] = mapped_column(Text, nullable=True)
    referencia: Mapped[str | None] = mapped_column(String(512), nullable=True)
    tamanho: Mapped[int | None] = mapped_column(Integer, nullable=True)
    situacao: Mapped[SituacaoDaCriacaoOriginal] = mapped_column(
        Enum(SituacaoDaCriacaoOriginal, native_enum=False, length=16), nullable=False
    )
    motivo_da_devolucao: Mapped[str | None] = mapped_column(Text, nullable=True)
    validado_por_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("persona.id"), nullable=True
    )
    validado_em: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        CheckConstraint(
            "(equipe_id IS NOT NULL AND guerreiro_id IS NULL) OR "
            "(equipe_id IS NULL AND guerreiro_id IS NOT NULL)",
            name="ck_criacao_original_equipe_ou_guerreiro",
        ),
        Index(
            "uq_criacao_original_equipe_id",
            "equipe_id",
            unique=True,
            postgresql_where=text("equipe_id IS NOT NULL"),
        ),
        Index(
            "uq_criacao_original_guerreiro_id_trilha_id",
            "guerreiro_id",
            "trilha_id",
            unique=True,
            postgresql_where=text("guerreiro_id IS NOT NULL"),
        ),
    )
