import enum
import uuid
from datetime import datetime

from sqlalchemy import (
    ARRAY,
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    Uuid,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from ..autoria import ComAutoria
from ..banco import Base


class SituacaoDaTrilha(enum.StrEnum):
    rascunho = "rascunho"
    publicada = "publicada"
    despublicada = "despublicada"


class Trilha(Base, ComAutoria):
    """Trilha de autoria de um Mestre, vinculada a um poder do catálogo,
    bem comum da plataforma — **sem** coluna de comunidade (`RN-01-42`,
    design — decisões). O ciclo de publicação e as travas dele são do
    PRD-09; aqui nasce só a situação. `ComAutoria.autor_id` é o Mestre autor
    contra o qual a posse é conferida (`trilhas.regra.conferir_posse_da_trilha`).

    `motivo_da_situacao`, `autor_da_situacao_id`, `papel_do_autor_da_situacao`
    e `situacao_alterada_em` guardam a procedência da última mudança de
    situação — publicação, despublicação ou republicação —, separada da
    autoria do cadastro já gravada por `ComAutoria`, no mesmo padrão do
    `PontoDeApoio` (`RF-09-10`, `RF-09-11`, design — decisões 3).
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
    motivo_da_situacao: Mapped[str | None] = mapped_column(Text, nullable=True)
    autor_da_situacao_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("persona.id"), nullable=True
    )
    papel_do_autor_da_situacao: Mapped[str | None] = mapped_column(String(32), nullable=True)
    situacao_alterada_em: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )


class InscricaoNaTrilha(Base):
    """Fato de que o Guerreiro(a) entrou no percurso de uma trilha — ato
    dele, nunca lançamento de terceiro (documento 11 §2.1, `RF-05-09`,
    `RN-05-43`, `RN-05-44`). Guarda só o par e o momento: não se desfaz,
    não tem situação e não obriga a concluir, no mesmo padrão de `Nivel`.
    A trilha publicada é conferida por quem grava (`trilhas.regra.
    inscrever_na_trilha`), nunca por esta tabela.
    """

    __tablename__ = "inscricao_na_trilha"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    guerreiro_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("persona.id"), nullable=False)
    trilha_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("trilha.id"), nullable=False)
    momento: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        UniqueConstraint(
            "guerreiro_id", "trilha_id", name="uq_inscricao_na_trilha_guerreiro_id_trilha_id"
        ),
    )


class TipoDeDesafioDeDesbloqueio(enum.StrEnum):
    quiz = "quiz"
    pratico = "pratico"


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
    # O desafio de desbloqueio, declarado pelo Mestre autor (`RF-09-26`,
    # design — decisão 4): coluna da missão, não entidade nova — declarar
    # de novo substitui, como `cadencia_de_retomada` já faz. No quiz,
    # `enunciado` e as quatro alternativas seguem o mesmo formato de
    # `quiz.modelo.PerguntaDeQuiz` (`RF-09-36`); no prático, só `enunciado`
    # é usado, como a descrição do que o Guerreiro(a) precisa cumprir.
    tipo_do_desafio_de_desbloqueio: Mapped[TipoDeDesafioDeDesbloqueio | None] = mapped_column(
        Enum(TipoDeDesafioDeDesbloqueio, native_enum=False, length=16), nullable=True
    )
    desafio_de_desbloqueio_enunciado: Mapped[str | None] = mapped_column(Text, nullable=True)
    desafio_de_desbloqueio_alternativa_1: Mapped[str | None] = mapped_column(Text, nullable=True)
    desafio_de_desbloqueio_alternativa_2: Mapped[str | None] = mapped_column(Text, nullable=True)
    desafio_de_desbloqueio_alternativa_3: Mapped[str | None] = mapped_column(Text, nullable=True)
    desafio_de_desbloqueio_alternativa_4: Mapped[str | None] = mapped_column(Text, nullable=True)
    desafio_de_desbloqueio_alternativa_correta: Mapped[int | None] = mapped_column(
        Integer, nullable=True
    )

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


class DesbloqueioDaMissao(Base):
    """Fato de que o Guerreiro(a) desbloqueou uma missão na própria trilha —
    nunca da equipe (design — decisão 1, documento 11 §2.2). Uma linha por
    par, com unicidade em (`guerreiro_id`, `missao_id`): no quiz, ela nasce
    já `aprovado=True`, aferida e gravada na mesma transação da submissão;
    no desafio prático, ela nasce com `aprovado` em aberto — a declaração
    do Guerreiro(a) de que cumpriu — e só vira desbloqueio de fato quando o
    Mestre autor julga (`julgado_por_id`). Julgado que não passou, a linha é
    apagada para que o Guerreiro(a) declare de novo, sem limite e sem
    punição (`RN-05-20`) — nada aqui é reprovação persistida.
    """

    __tablename__ = "desbloqueio_da_missao"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    guerreiro_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("persona.id"), nullable=False)
    missao_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("missao.id"), nullable=False)
    momento: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    aprovado: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    julgado_por_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("persona.id"), nullable=True
    )

    __table_args__ = (
        UniqueConstraint(
            "guerreiro_id", "missao_id", name="uq_desbloqueio_da_missao_guerreiro_id_missao_id"
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

    `aula_id` é o vínculo opcional com o encontro em que a atividade
    presencial acontece — a programação do encontro que a equipe lê nasce
    daqui (`RF-09-69`, `RF-09-73`, documento 05 §4). Atividade on-line ou
    assíncrona nunca o declara; a recusa é de `trilhas.regra.criar_atividade`.
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
    aula_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, ForeignKey("aula.id"), nullable=True)

    __table_args__ = (Index("ix_atividade_aula_id", "aula_id"),)
