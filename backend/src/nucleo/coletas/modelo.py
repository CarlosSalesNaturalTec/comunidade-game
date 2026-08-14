import enum
import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Uuid,
)
from sqlalchemy.orm import Mapped, mapped_column

from ..autoria import ComAutoria
from ..banco import Base
from ..locais.modelo import NivelDoLocal


class FormaDeRegistro(enum.StrEnum):
    """O que o tipo de coleta exige do registro: um valor numérico ou uma
    evidência de mídia (`RF-08-05`, `RF-08-21`)."""

    numero = "numero"
    foto = "foto"
    video = "video"


class TipoDeColeta(Base, ComAutoria):
    """Catálogo do que se mede no território, cadastrado por Admin — o
    Mestre escolhe entre os tipos cadastrados e nunca cria um novo ao
    escrever o desafio (`RF-08-05`). Unidade e faixa esperada só existem no
    tipo que se mede por número; o `CheckConstraint` torna essa leitura do
    PRD impossível de violar por qualquer caminho de escrita
    (`RF-08-12`, design — Decisions).
    """

    __tablename__ = "tipo_de_coleta"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    nome: Mapped[str] = mapped_column(String(128), nullable=False)
    forma_de_registro: Mapped[FormaDeRegistro] = mapped_column(
        Enum(FormaDeRegistro, native_enum=False, length=16), nullable=False
    )
    unidade: Mapped[str | None] = mapped_column(String(32), nullable=True)
    faixa_minima: Mapped[float | None] = mapped_column(Float, nullable=True)
    faixa_maxima: Mapped[float | None] = mapped_column(Float, nullable=True)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    __table_args__ = (
        CheckConstraint(
            "(forma_de_registro = 'numero' AND unidade IS NOT NULL AND "
            "faixa_minima IS NOT NULL AND faixa_maxima IS NOT NULL) OR "
            "(forma_de_registro != 'numero' AND unidade IS NULL AND "
            "faixa_minima IS NULL AND faixa_maxima IS NULL)",
            name="ck_tipo_de_coleta_unidade_e_faixa_so_no_tipo_numero",
        ),
        CheckConstraint(
            "faixa_minima IS NULL OR faixa_maxima IS NULL OR faixa_minima <= faixa_maxima",
            name="ck_tipo_de_coleta_faixa_minima_menor_ou_igual_a_maxima",
        ),
    )


class Cadencia(enum.StrEnum):
    diaria = "diaria"
    semanal = "semanal"
    mensal = "mensal"


class DesafioDeColeta(Base, ComAutoria):
    """Declarado pelo Mestre autor dentro de uma missão da própria trilha
    (`RF-08-06`). Sem coluna de trilha: a posse é conferida pela trilha
    alcançada a partir de `missao.trilha_id`, o mesmo caminho de
    `criar_etiqueta_ods` (design — Decisions). Também sem coluna de
    etiqueta ODS — ela é derivada da missão ou da trilha a cada leitura,
    nunca copiada (`RF-08-25`, `RN-08-21`, design — Decisions).
    """

    __tablename__ = "desafio_de_coleta"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    missao_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("missao.id"), nullable=False)
    tipo_de_coleta_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("tipo_de_coleta.id"), nullable=False
    )
    cadencia: Mapped[Cadencia] = mapped_column(
        Enum(Cadencia, native_enum=False, length=16), nullable=False
    )
    vigencia_inicio: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    vigencia_fim: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    granularidade_exigida: Mapped[NivelDoLocal] = mapped_column(
        Enum(NivelDoLocal, native_enum=False, length=16), nullable=False
    )
    registros_que_pontuam_por_periodo: Mapped[int] = mapped_column(Integer, nullable=False)

    __table_args__ = (
        CheckConstraint(
            "vigencia_fim >= vigencia_inicio",
            name="ck_desafio_de_coleta_vigencia_fim_nao_precede_inicio",
        ),
        CheckConstraint(
            "registros_que_pontuam_por_periodo >= 1",
            name="ck_desafio_de_coleta_registros_que_pontuam_maior_ou_igual_a_1",
        ),
    )
