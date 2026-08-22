import enum
import uuid

from sqlalchemy import (
    ARRAY,
    Boolean,
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


class SituacaoDaTrilha(enum.StrEnum):
    rascunho = "rascunho"
    publicada = "publicada"


class Trilha(Base, ComAutoria):
    """Trilha de autoria de um Mestre, vinculada a um poder do catálogo,
    bem comum da plataforma — **sem** coluna de comunidade (`RN-01-42`,
    design — decisões). O ciclo de publicação e as travas dele são do
    PRD-09; aqui nasce só a situação. `ComAutoria.autor_id` é o Mestre autor
    contra o qual a posse é conferida (`trilhas.regra.conferir_posse_da_trilha`).
    """

    __tablename__ = "trilha"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    nome: Mapped[str] = mapped_column(String(128), nullable=False)
    objetivo: Mapped[str] = mapped_column(Text, nullable=False)
    area_do_conhecimento: Mapped[str] = mapped_column(String(128), nullable=False)
    poder_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("poder.id"), nullable=False)
    situacao: Mapped[SituacaoDaTrilha] = mapped_column(
        Enum(SituacaoDaTrilha, native_enum=False, length=16),
        nullable=False,
        default=SituacaoDaTrilha.rascunho,
    )


class EtapaDoCiclo(enum.StrEnum):
    abertura = "abertura"
    desenvolvimento = "desenvolvimento"
    marcos = "marcos"
    fechamento = "fechamento"


class Missao(Base, ComAutoria):
    """Menor unidade de progressão da trilha (documento 11 §2.2). A posição
    tem unicidade adiável (`uq_missao_trilha_id_posicao`) para que o PRD-09
    reordene as missões numa única transação, sem migração nova
    (`RF-09-02`, design — decisões). A sondagem é declarada em `e_sondagem`,
    nunca deduzida da posição, e o índice único parcial admite no máximo uma
    por trilha. `cadencia_de_retomada` é a lista de dias contados do
    desbloqueio (`RF-09-101`, design — decisões 3); anulável porque a
    retomada é opcional (`RF-09-83`).
    """

    __tablename__ = "missao"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    trilha_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("trilha.id"), nullable=False)
    titulo: Mapped[str] = mapped_column(String(128), nullable=False)
    posicao: Mapped[int] = mapped_column(Integer, nullable=False)
    nivel_de_dificuldade: Mapped[int] = mapped_column(Integer, nullable=False)
    obrigatoria: Mapped[bool] = mapped_column(Boolean, nullable=False)
    e_sondagem: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    etapa_do_ciclo: Mapped[EtapaDoCiclo] = mapped_column(
        Enum(EtapaDoCiclo, native_enum=False, length=16), nullable=False
    )
    cadencia_de_retomada: Mapped[list[int] | None] = mapped_column(ARRAY(Integer), nullable=True)

    __table_args__ = (
        UniqueConstraint(
            "trilha_id",
            "posicao",
            name="uq_missao_trilha_id_posicao",
            deferrable=True,
            initially="IMMEDIATE",
        ),
        Index(
            "uq_missao_sondagem_por_trilha",
            "trilha_id",
            unique=True,
            postgresql_where=text("e_sondagem"),
        ),
    )


class ModalidadeDeAtividade(enum.StrEnum):
    individual = "individual"
    em_equipe = "em_equipe"
    em_equipe_com_familiar = "em_equipe_com_familiar"


class FormatoDeAtividade(enum.StrEnum):
    presencial = "presencial"
    on_line_assincrona = "on_line_assincrona"


class Atividade(Base, ComAutoria):
    """Sempre pertencente a uma missão, classificada nos três eixos
    ortogonais do documento 11 §4: modalidade e formato fechados nos
    valores do documento; natureza aberta, no mesmo padrão que
    `Consentimento.tipo` já firmou (design — decisões).
    """

    __tablename__ = "atividade"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    missao_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("missao.id"), nullable=False)
    titulo: Mapped[str] = mapped_column(String(128), nullable=False)
    descricao: Mapped[str | None] = mapped_column(Text, nullable=True)
    modalidade: Mapped[ModalidadeDeAtividade] = mapped_column(
        Enum(ModalidadeDeAtividade, native_enum=False, length=32), nullable=False
    )
    formato: Mapped[FormatoDeAtividade] = mapped_column(
        Enum(FormatoDeAtividade, native_enum=False, length=32), nullable=False
    )
    natureza: Mapped[str] = mapped_column(String(64), nullable=False)
    producao_esperada: Mapped[str] = mapped_column(Text, nullable=False)
