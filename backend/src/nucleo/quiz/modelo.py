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
    Text,
    UniqueConstraint,
    Uuid,
)
from sqlalchemy.orm import Mapped, mapped_column

from ..autoria import ComAutoria
from ..banco import Base

# As quatro alternativas do documento 05 §5 viram quatro colunas, e a
# correta é o índice de uma delas: "exatamente quatro" deixa de depender de
# validação e passa a ser a estrutura da tabela (`RF-01-36`, documento 09).
PRIMEIRA_ALTERNATIVA = 1
TOTAL_DE_ALTERNATIVAS = 4


class PerguntaDeQuiz(Base, ComAutoria):
    """Pergunta de múltipla escolha pré-cadastrada pelo Mestre curador, com
    quatro alternativas, a indicação da correta e o vínculo com a missão a
    que ela se refere, de onde a trilha decorre (`RF-01-36`, `RF-01-03`,
    `RF-09-39`, documento 05 §5). **Sem tempo-limite**: o ritmo é de quem
    conduz a partida, e o núcleo não cronometra. A pergunta é do banco do
    Mestre e não pertence a uma partida — a mesma pergunta serve a partidas
    diferentes, e por isso a anulação é da partida, não dela. **Sem
    situação**: ela nasce disponível e assim permanece (decisão do
    fundador, 2026-08-23, documento 09).
    """

    __tablename__ = "pergunta_de_quiz"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    enunciado: Mapped[str] = mapped_column(Text, nullable=False)
    alternativa_1: Mapped[str] = mapped_column(Text, nullable=False)
    alternativa_2: Mapped[str] = mapped_column(Text, nullable=False)
    alternativa_3: Mapped[str] = mapped_column(Text, nullable=False)
    alternativa_4: Mapped[str] = mapped_column(Text, nullable=False)
    alternativa_correta: Mapped[int] = mapped_column(Integer, nullable=False)
    # A trilha é derivada da missão no cadastro e persistida — não pedida ao
    # cliente — para que uma missão nunca seja declarada sob a trilha errada
    # (design — decisão 1). Ambas alimentam o filtro de `RF-09-40`.
    missao_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("missao.id"), nullable=False)
    trilha_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("trilha.id"), nullable=False)

    __table_args__ = (
        CheckConstraint(
            f"alternativa_correta BETWEEN {PRIMEIRA_ALTERNATIVA} AND {TOTAL_DE_ALTERNATIVAS}",
            name="ck_pergunta_de_quiz_alternativa_correta",
        ),
        Index("ix_pergunta_de_quiz_missao_id", "missao_id"),
        Index("ix_pergunta_de_quiz_trilha_id", "trilha_id"),
    )


class SituacaoDaPartida(enum.StrEnum):
    aberta = "aberta"
    encerrada = "encerrada"


class PartidaDeQuiz(Base, ComAutoria):
    """Partida do Quiz ao Vivo, que corre numa aula sobre uma atividade de
    natureza competição ao vivo (`RF-01-17`, `RF-01-21`, documento 05 §5).
    **Sem `trilha_id`**: a trilha é derivada de `atividade → missao →
    trilha`, para que a partida não vire uma segunda fonte de verdade do
    mesmo fato (design — decisão 3). `ComAutoria` grava quem abriu;
    `encerrada_por_id` e `encerrada_em`, anuláveis, gravam quem encerrou, no
    padrão de `CriacaoOriginal.validado_por_id`/`validado_em`. O crédito
    acontece só na transição `aberta → encerrada` (design — decisão 1).
    """

    __tablename__ = "partida_de_quiz"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    aula_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("aula.id"), nullable=False)
    atividade_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("atividade.id"), nullable=False
    )
    situacao: Mapped[SituacaoDaPartida] = mapped_column(
        Enum(SituacaoDaPartida, native_enum=False, length=16),
        nullable=False,
        default=SituacaoDaPartida.aberta,
    )
    encerrada_por_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("persona.id"), nullable=True
    )
    encerrada_em: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class EquipeNaPartida(Base):
    """Equipe disputante, fixada na abertura da partida. É contra esta lista
    que a recusa do Guerreiro(a) repetido é verificada uma vez só, em vez de
    reavaliada a cada resposta — a composição da equipe da aula ainda pode
    mudar depois (`RF-01-39`, design — decisão 4).
    """

    __tablename__ = "equipe_na_partida"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    partida_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("partida_de_quiz.id"), nullable=False
    )
    equipe_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("equipe.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "partida_id", "equipe_id", name="uq_equipe_na_partida_partida_id_equipe_id"
        ),
    )


class PerguntaAnuladaNaPartida(Base, ComAutoria):
    """Pergunta anulada pelo Mestre que conduz a partida, havendo
    contestação (documento 05 §5). A anulação é **da partida**, nunca da
    pergunta do banco, e é registro próprio porque a partida segue aberta
    depois dela: resposta que chegue mais tarde precisa encontrar a marca,
    e anular pergunta ainda sem resposta precisa guardar quem anulou
    (`RF-01-03`, `RN-01-38`, design — decisão 6). `ComAutoria` grava quem
    anulou, com que papel e quando.
    """

    __tablename__ = "pergunta_anulada_na_partida"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    partida_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("partida_de_quiz.id"), nullable=False
    )
    pergunta_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("pergunta_de_quiz.id"), nullable=False
    )

    __table_args__ = (
        UniqueConstraint(
            "partida_id",
            "pergunta_id",
            name="uq_pergunta_anulada_na_partida_partida_id_pergunta_id",
        ),
    )


class RespostaDeQuiz(Base, ComAutoria):
    """Resposta da **equipe** a uma pergunta da partida — nunca do aparelho
    de onde veio nem do integrante que a enviou (`RF-01-36`, documento
    05 §5). `momento_de_chegada` é carimbado pelo núcleo na gravação, e é o
    critério de desempate do bônus; instante declarado pelo chamador não é
    aceito (design — decisão 2). Única por (partida, pergunta, equipe), o
    que torna o reenvio com a rede instável inofensivo, no mesmo desenho de
    tolerância da `Presenca` (PRD-01 §10). `anulada_em` é a projeção
    consultável de `PerguntaAnuladaNaPartida`: a resposta permanece
    consultável, marcada, e a apuração lê a anulação na tabela dela
    (design — decisão 6).
    """

    __tablename__ = "resposta_de_quiz"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    partida_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("partida_de_quiz.id"), nullable=False
    )
    pergunta_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("pergunta_de_quiz.id"), nullable=False
    )
    equipe_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("equipe.id"), nullable=False)
    alternativa_escolhida: Mapped[int] = mapped_column(Integer, nullable=False)
    momento_de_chegada: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    anulada_em: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        CheckConstraint(
            f"alternativa_escolhida BETWEEN {PRIMEIRA_ALTERNATIVA} AND {TOTAL_DE_ALTERNATIVAS}",
            name="ck_resposta_de_quiz_alternativa_escolhida",
        ),
        UniqueConstraint(
            "partida_id",
            "pergunta_id",
            "equipe_id",
            name="uq_resposta_de_quiz_partida_id_pergunta_id_equipe_id",
        ),
    )
