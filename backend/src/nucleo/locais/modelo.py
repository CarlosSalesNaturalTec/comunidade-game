import enum
import uuid
from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKey,
    ForeignKeyConstraint,
    String,
    Text,
    UniqueConstraint,
    Uuid,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from ..banco import Base


class NivelDoLocal(enum.StrEnum):
    """Seis níveis, nessa ordem de contenção — cada um dentro do anterior
    (`RF-08-04`, PRD-08 §8)."""

    comunidade = "comunidade"
    bairro = "bairro"
    rua = "rua"
    condominio = "condominio"
    bloco = "bloco"
    quadra = "quadra"


# A ordem de contenção — "o pai é do nível imediatamente acima" (`RF-08-04`)
# é lido daqui por `locais/regra.py`.
ORDEM_DOS_NIVEIS: tuple[NivelDoLocal, ...] = (
    NivelDoLocal.comunidade,
    NivelDoLocal.bairro,
    NivelDoLocal.rua,
    NivelDoLocal.condominio,
    NivelDoLocal.bloco,
    NivelDoLocal.quadra,
)


class Local(Base):
    """Um nó da hierarquia territorial da comunidade, com duas origens: o
    cadastro direto por Admin e a aprovação de `SolicitacaoDeLocal` por
    Admin ou pelo Mestre autor da trilha do desafio de origem — as duas sob
    as mesmas regras de hierarquia (`RF-08-04`, `RF-08-22`, `RN-08-18`).

    `UNIQUE (id, comunidade_id)` existe só para sustentar a chave
    estrangeira composta do pai: com ela, o próprio banco recusa um pai de
    outra comunidade, sem que nenhuma regra precise conferir (design —
    Decisions). O nível do pai — imediatamente acima — não cabe em chave
    estrangeira e é validado em `locais/regra.py`.
    """

    __tablename__ = "local"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    comunidade_virtual_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("comunidade_virtual.id"), nullable=False
    )
    nivel: Mapped[NivelDoLocal] = mapped_column(
        Enum(NivelDoLocal, native_enum=False, length=16), nullable=False
    )
    rotulo: Mapped[str] = mapped_column(String(128), nullable=False)
    local_pai_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, nullable=True)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        UniqueConstraint("id", "comunidade_virtual_id", name="uq_local_id_comunidade_virtual_id"),
        ForeignKeyConstraint(
            ["local_pai_id", "comunidade_virtual_id"],
            ["local.id", "local.comunidade_virtual_id"],
            name="fk_local_local_pai_id_comunidade_virtual_id",
        ),
        CheckConstraint(
            "(nivel = 'comunidade') = (local_pai_id IS NULL)",
            name="ck_local_pai_so_vazio_no_nivel_comunidade",
        ),
    )


class SituacaoDaSolicitacaoDeLocal(enum.StrEnum):
    """Só `recebida` admite transição, e apenas para `aprovada` ou
    `recusada` — desfecho irreversível, sem reabertura (`RN-08-18`,
    design — Decisions)."""

    recebida = "recebida"
    aprovada = "aprovada"
    recusada = "recusada"


class SolicitacaoDeLocal(Base):
    """Pedido do Guerreiro(a) por um local ausente na hierarquia, preso à
    sua comunidade vigente e ao desafio de coleta que o alcança até a
    trilha do avaliador (`RF-08-22`, PRD-08 §8). Sem prazo de resposta e
    sem marca de atraso: fica fora do ciclo da fila única de avaliação, que
    proíbe em toda situação o que a aprovação daqui faz — criar cadastro
    (proposal — Por que não é a quinta natureza da fila de avaliação).

    O pedido em si NEVER cria local — só a aprovação, e `local_criado_id`
    guarda o local que ela criou, para que a auditoria e o teste confiram
    que a aprovação criou um local e um só (`RN-08-18`, design —
    Decisions). O local pai da aprovação não é atributo daqui: vem do
    corpo do próprio ato de avaliar (design — Decisions).
    """

    __tablename__ = "solicitacao_de_local"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    solicitante_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("persona.id"), nullable=False
    )
    comunidade_virtual_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("comunidade_virtual.id"), nullable=False
    )
    desafio_de_coleta_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("desafio_de_coleta.id"), nullable=False
    )
    nivel_pretendido: Mapped[NivelDoLocal] = mapped_column(
        Enum(NivelDoLocal, native_enum=False, length=16), nullable=False
    )
    rotulo: Mapped[str] = mapped_column(String(128), nullable=False)
    justificativa: Mapped[str] = mapped_column(Text, nullable=False)
    situacao: Mapped[SituacaoDaSolicitacaoDeLocal] = mapped_column(
        Enum(SituacaoDaSolicitacaoDeLocal, native_enum=False, length=16),
        nullable=False,
        default=SituacaoDaSolicitacaoDeLocal.recebida,
    )
    avaliador_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("persona.id"), nullable=True
    )
    motivo_da_recusa: Mapped[str | None] = mapped_column(Text, nullable=True)
    local_criado_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("local.id"), nullable=True
    )
    avaliado_em: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    registrado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
