import uuid

from sqlalchemy import ForeignKey, Index, Integer, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from ..autoria import ComAutoria
from ..banco import Base


class Troca(Base, ComAutoria):
    """A entrega de um item do catálogo avulso por pontos extras — o único
    débito de ponto extra do Ciclo 01 (`RF-07-35`, `RF-07-36`, PRD-07 §8).
    `preco_cobrado` é a vigência corrente do preço de referência **na data
    da troca**, gravada aqui para que mudança posterior da tabela não
    reescreva o histórico (`RF-07-46`, `RN-07-29`).

    O encontro é a `Aula` do PRD-01 (documento 02 §8.2, decisão 1): o
    núcleo não verifica o estado dela nem a presença do Guerreiro(a).
    `ComAutoria` já grava o Mestre que entregou, o papel e a data e hora
    com fuso — não há coluna própria para isso (design — Decisions 1).
    """

    __tablename__ = "troca"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    item_de_catalogo_avulso_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("item_de_catalogo_avulso.id"), nullable=False
    )
    guerreiro_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("persona.id"), nullable=False)
    preco_cobrado: Mapped[int] = mapped_column(Integer, nullable=False)
    aula_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("aula.id"), nullable=False)

    __table_args__ = (
        Index("ix_troca_guerreiro_id", "guerreiro_id"),
        Index("ix_troca_aula_id", "aula_id"),
    )
