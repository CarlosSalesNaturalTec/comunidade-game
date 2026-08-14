import enum
import uuid
from datetime import datetime

from sqlalchemy import (
    DDL,
    Boolean,
    CheckConstraint,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    Uuid,
    event,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from ..autoria import ComAutoria
from ..banco import Base
from ..locais.modelo import NivelDoLocal
from ..tempo import ComMomentoDoFato


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


class EstadoDaSerie(enum.StrEnum):
    """Só `ativa` nesta fatia — a interrupção por dois períodos de cadência
    sem registro e o encerramento pelo fim da vigência do desafio são
    `RF-08-10` e `RF-08-11`, de entrega posterior (proposal.md)."""

    ativa = "ativa"


class SerieDeColeta(Base):
    """Compromisso individual do Guerreiro(a) da sessão com um desafio de
    coleta num local da sua comunidade — nunca do aparelho de onde veio a
    chamada (`RN-08-04`). A cadência é herdada do desafio na abertura, para
    que a transição de estado da entrega seguinte não dependa de o desafio
    permanecer inalterado (`RF-08-07`, PRD-08 §8).
    """

    __tablename__ = "serie_de_coleta"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    desafio_de_coleta_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("desafio_de_coleta.id"), nullable=False
    )
    coletor_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("persona.id"), nullable=False)
    local_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("local.id"), nullable=False)
    cadencia: Mapped[Cadencia] = mapped_column(
        Enum(Cadencia, native_enum=False, length=16), nullable=False
    )
    estado: Mapped[EstadoDaSerie] = mapped_column(
        Enum(EstadoDaSerie, native_enum=False, length=16),
        nullable=False,
        default=EstadoDaSerie.ativa,
    )
    aberta_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    ultima_medicao_valida_em: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    __table_args__ = (
        UniqueConstraint(
            "coletor_id",
            "desafio_de_coleta_id",
            "local_id",
            name="uq_serie_de_coleta_coletor_desafio_local",
        ),
    )


class OrigemDoRegistro(enum.StrEnum):
    manual = "manual"
    voz = "voz"
    # `sensor` exige a credencial de dispositivo (`RF-01-67`, `RN-08-23`) —
    # a rota de sessão de persona continua recusando esta origem com 422.
    sensor = "sensor"


class SituacaoDoRegistro(enum.StrEnum):
    """Só `valida` nesta fatia — `invalidada`, com o estorno, é a entrega da
    auditoria do Mestre (proposal.md)."""

    valida = "valida"


# Anos do Ciclo 01 (documento 01 §pré-âmbulo — ago a dez/2026): a migração
# do Alembic cria as mesmas partições fora dos testes; este evento cobre o
# caminho de `Base.metadata.create_all()`, que os testes usam
# (mesmo padrão do gatilho de `pontuacao.modelo.PontoRegular`).
_ANOS_PARTICIONADOS_DO_REGISTRO_DE_COLETA: tuple[int, ...] = (2026,)


def _sql_de_criacao_das_particoes() -> str:
    trechos = [
        f"""
        CREATE TABLE registro_de_coleta_{ano} PARTITION OF registro_de_coleta
            FOR VALUES FROM ('{ano}-01-01 00:00:00+00') TO ('{ano + 1}-01-01 00:00:00+00');
        """
        for ano in _ANOS_PARTICIONADOS_DO_REGISTRO_DE_COLETA
    ]
    trechos.append(
        "CREATE TABLE registro_de_coleta_default PARTITION OF registro_de_coleta DEFAULT;"
    )
    return "\n".join(trechos)


class RegistroDeColeta(Base, ComAutoria, ComMomentoDoFato):
    """A medição em si — o dado do território guardado em definitivo, com
    o coletor identificado e a hora da medição preservada (`RF-08-08`,
    invariante 7 do documento 99 §6). Somente inserção: `valor`,
    `momento_do_fato` e o coletor da série nunca mudam depois de gravados
    (`RN-08-10`, `RN-08-11`) — não há rota de alteração nem de exclusão.

    Particionada por RANGE em `momento_do_fato` (documento 03 §1), o que
    exige que a chave de particionamento integre a chave primária — daí o
    par `(id, momento_do_fato)` em vez de `id` sozinho (design — decisões).
    Quem apontar para o registro em entrega futura aponta para o par.
    """

    __tablename__ = "registro_de_coleta"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    # Sobrescreve o mixin para integrar a chave primária composta que o
    # particionamento por RANGE exige (design — decisões).
    momento_do_fato: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), primary_key=True, nullable=False
    )
    serie_de_coleta_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("serie_de_coleta.id"), nullable=False
    )
    valor: Mapped[float | None] = mapped_column(Float, nullable=True)
    unidade: Mapped[str | None] = mapped_column(String(32), nullable=True)
    midia_referencia: Mapped[str | None] = mapped_column(Text, nullable=True)
    origem: Mapped[OrigemDoRegistro] = mapped_column(
        Enum(OrigemDoRegistro, native_enum=False, length=16), nullable=False
    )
    situacao: Mapped[SituacaoDoRegistro] = mapped_column(
        Enum(SituacaoDoRegistro, native_enum=False, length=16),
        nullable=False,
        default=SituacaoDoRegistro.valida,
    )
    a_conferir: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    comunidade_virtual_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("comunidade_virtual.id"), nullable=False
    )
    pontos_creditados: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    # O atributo `dispositivo` do PRD-08 §8: só preenchido na origem `sensor`
    # (`RF-08-14`) — manual e voz nunca gravam credencial.
    credencial_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("credencial.id"), nullable=True
    )

    __table_args__ = ({"postgresql_partition_by": "RANGE (momento_do_fato)"},)


event.listen(RegistroDeColeta.__table__, "after_create", DDL(_sql_de_criacao_das_particoes()))
