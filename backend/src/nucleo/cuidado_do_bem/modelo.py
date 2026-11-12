import enum
import uuid
from datetime import datetime

from sqlalchemy import (
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    Uuid,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from ..autoria import ComAutoria
from ..banco import Base


class SituacaoDoRegistroDeCustomizacao(enum.StrEnum):
    pendente = "pendente"
    aprovado = "aprovado"
    reprovado = "reprovado"
    cancelado = "cancelado"
    expirado = "expirado"


class RegistroDeCustomizacao(Base, ComAutoria):
    """A nova customização de um kit recebido, registrada pelo próprio
    Guerreiro(a) ou capturada pelo Mestre da aula, e julgada ao vivo no
    encontro (`RF-01-84`, `RF-01-85`, `RF-01-86`, documento 11 §5).

    O bem é a **entrega** — o par Guerreiro(a) × recompensa de marco —, não a
    recompensa: é ela que a criança tem nas mãos (design — decisão 2). A mídia
    entra pela sessão de envio e só é gravada depois de confirmada; sem ela o
    registro não é julgado. `ComAutoria` grava quem registrou — o
    Guerreiro(a) ou o Mestre que capturou. Um só pendente por entrega, também
    no banco, pelo índice único parcial (design — decisão 3).
    """

    __tablename__ = "registro_de_customizacao"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    entrega_de_recompensa_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("entrega_de_recompensa.id"), nullable=False
    )
    guerreiro_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("persona.id"), nullable=False)
    descricao: Mapped[str] = mapped_column(Text, nullable=False)
    situacao: Mapped[SituacaoDoRegistroDeCustomizacao] = mapped_column(
        Enum(SituacaoDoRegistroDeCustomizacao, native_enum=False, length=16),
        nullable=False,
        default=SituacaoDoRegistroDeCustomizacao.pendente,
    )
    midia_referencia: Mapped[str | None] = mapped_column(String(512), nullable=True)
    midia_tamanho: Mapped[int | None] = mapped_column(Integer, nullable=True)
    midia_tipo_do_arquivo: Mapped[str | None] = mapped_column(String(255), nullable=True)
    motivo_do_julgamento: Mapped[str | None] = mapped_column(Text, nullable=True)
    aula_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, ForeignKey("aula.id"), nullable=True)
    julgado_por_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("persona.id"), nullable=True
    )
    julgado_em: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        Index(
            "uq_registro_de_customizacao_pendente_por_entrega",
            "entrega_de_recompensa_id",
            unique=True,
            postgresql_where=text("situacao = 'pendente'"),
        ),
        Index("ix_registro_de_customizacao_guerreiro_id", "guerreiro_id"),
    )


class FonteDaPontuacaoDoBem(enum.StrEnum):
    conservacao = "conservacao"
    customizacao = "customizacao"


class PontuacaoDoBem(Base, ComAutoria):
    """O ponto extra que um bem recebido rendeu num encontro, pela conservação
    ou pela customização. A unicidade em (aula, entrega) é a `RN-01-66` no
    banco: o mesmo bem pontua no máximo uma vez por encontro, por um caminho
    só, em qualquer via (design — decisão 3). `ComAutoria` grava o Mestre da
    aula que validou ou aprovou.
    """

    __tablename__ = "pontuacao_do_bem"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    aula_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("aula.id"), nullable=False)
    entrega_de_recompensa_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("entrega_de_recompensa.id"), nullable=False
    )
    guerreiro_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("persona.id"), nullable=False)
    fonte: Mapped[FonteDaPontuacaoDoBem] = mapped_column(
        Enum(FonteDaPontuacaoDoBem, native_enum=False, length=16), nullable=False
    )
    registro_de_customizacao_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("registro_de_customizacao.id"), nullable=True
    )

    __table_args__ = (
        UniqueConstraint(
            "aula_id", "entrega_de_recompensa_id", name="uq_pontuacao_do_bem_aula_entrega"
        ),
        Index("ix_pontuacao_do_bem_guerreiro_id", "guerreiro_id"),
    )
