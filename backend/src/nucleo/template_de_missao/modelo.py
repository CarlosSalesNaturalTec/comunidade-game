import enum
import uuid

from sqlalchemy import JSON, Enum, ForeignKey, Index, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from ..autoria import ComAutoria
from ..banco import Base


class SituacaoDaSugestaoDeEstrutura(enum.StrEnum):
    proposta = "proposta"
    aceita = "aceita"
    recusada = "recusada"
    alterada = "alterada"


class SugestaoDeEstrutura(Base, ComAutoria):
    """Registro de um pedido de estrutura ao template da missão — nunca
    estado da missão (`RF-09-85`, PRD-09 §8, design — decisão 4). Pedir de
    novo grava uma linha nova; a situação só muda quando o Mestre autor
    aceita, recusa ou altera, e nada aqui grava conteúdo, atividade,
    retomada ou etiqueta na missão — quem grava são as rotas de autoria que
    já existem (`RF-09-89`, `RN-09-33`).

    `estrutura_proposta` e `lacunas` são JSON: a primeira é o que o modelo
    propôs (ou vazio, sem credencial ou indisponível), a segunda é o que o
    núcleo apurou sozinho a partir do que está gravado — nunca do que o
    modelo respondeu (`RF-09-86`). Sem coluna de custo: o `RF-09-90` e a
    `RN-09-07` proíbem medir consumo do modelo por ato.
    """

    __tablename__ = "sugestao_de_estrutura"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    missao_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("missao.id"), nullable=False)
    topico: Mapped[str] = mapped_column(Text, nullable=False)
    estrutura_proposta: Mapped[dict] = mapped_column(JSON, nullable=False)
    lacunas: Mapped[list] = mapped_column(JSON, nullable=False)
    situacao: Mapped[SituacaoDaSugestaoDeEstrutura] = mapped_column(
        Enum(SituacaoDaSugestaoDeEstrutura, native_enum=False, length=16),
        nullable=False,
        default=SituacaoDaSugestaoDeEstrutura.proposta,
    )

    __table_args__ = (Index("ix_sugestao_de_estrutura_missao_id", "missao_id"),)
