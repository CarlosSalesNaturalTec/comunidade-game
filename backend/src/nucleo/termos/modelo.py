import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Index, String, Text, UniqueConstraint, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column

from ..banco import Base
from ..consentimentos.modelo import TipoDeConsentimento


class Termo(Base):
    """O texto de cada versão do termo, em linguagem simples — conteúdo
    semeado na implantação, nunca criado ou editado por rota (`RF-13-32`,
    `RF-13-33`, design — decisão 2). `tipo` reaproveita o conjunto fechado
    de `TipoDeConsentimento`: é o mesmo carimbado em `Consentimento.tipo`.
    A vigente continua sendo a que `Configuracao.consentimento_versao_
    vigente_do_termo` carimba; esta tabela só guarda o texto de cada
    (tipo, versão) já carimbada, e é somente leitura por rota.
    """

    __tablename__ = "termo"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    tipo: Mapped[TipoDeConsentimento] = mapped_column(
        Enum(TipoDeConsentimento, native_enum=False, length=64), nullable=False
    )
    versao: Mapped[str] = mapped_column(String(32), nullable=False)
    texto: Mapped[str] = mapped_column(Text, nullable=False)
    vigente_desde: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        UniqueConstraint("tipo", "versao", name="uq_termo_tipo_versao"),
        Index("ix_termo_tipo_vigente_desde", "tipo", "vigente_desde"),
    )


class LeituraDeTermo(Base):
    """Prova de ciência do responsável — um registro por (responsável,
    versão), permanente, sem valer como consentimento (`RF-13-32`, PRD-13
    §§11, 12). Não referencia `tipo`: a versão já identifica o termo lido.
    """

    __tablename__ = "leitura_de_termo"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    responsavel_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("persona.id"), nullable=False
    )
    versao: Mapped[str] = mapped_column(String(32), nullable=False)
    lida_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        UniqueConstraint("responsavel_id", "versao", name="uq_leitura_de_termo_responsavel_versao"),
    )
