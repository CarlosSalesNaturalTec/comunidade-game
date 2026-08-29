import enum
import uuid
from datetime import date, datetime

from sqlalchemy import Date, DateTime, Enum, ForeignKey, Index, String, Text, Uuid, func, text
from sqlalchemy.orm import Mapped, mapped_column

from ..banco import Base


class Papel(enum.StrEnum):
    admin = "admin"
    mestre = "mestre"
    guerreiro = "guerreiro"
    responsavel = "responsavel"
    apoiador = "apoiador"


class Persona(Base):
    """Tabela única para os cinco papéis do PRD-01 §4 (RF-01-19). Atributo
    próprio de papel entra em tabela satélite quando a fatia que o traz
    chegar (design — riscos). `avatar` segue o mesmo precedente do nick:
    nasce aqui, opaco ao núcleo — nenhuma validação de forma —, e a rota que
    o grava é do PRD-04 (`RN-01-10`, design — decisões). O vínculo de
    comunidade do Guerreiro(a) não é coluna daqui: vive em
    `comunidades.modelo.VinculoJogador`, entidade com histórico
    (`RN-01-05`, `RF-08-02`, PRD-08 §8).

    `nome`, `email` e `whatsapp` são atributos comuns aos cinco papéis
    (PRD-01 §8); `nascimento` é de quem o tem — só o Guerreiro(a). Todos
    nulos no banco porque a semeadura e as personas anteriores a esta fatia
    não os carregam; a exigência de cada um por papel é do cadastro da
    gestão (`RF-02-01` a `RF-02-05`, documento 02 §1).
    """

    __tablename__ = "persona"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    papel: Mapped[Papel] = mapped_column(Enum(Papel, native_enum=False, length=32), nullable=False)
    nome: Mapped[str | None] = mapped_column(String(256), nullable=True)
    nascimento: Mapped[date | None] = mapped_column(Date, nullable=True)
    email: Mapped[str | None] = mapped_column(String(256), nullable=True)
    whatsapp: Mapped[str | None] = mapped_column(String(32), nullable=True)
    avatar: Mapped[str | None] = mapped_column(Text, nullable=True)
    criada_por: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("persona.id"), nullable=True
    )
    criada_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class Nick(Base):
    """Tabela própria, não coluna de `persona` nem de satélite de papel: é o
    que dá à unicidade um único índice a conferir, alcançando qualquer papel
    que venha a ter nick — Guerreiro(a) nesta fatia, Apoiador em fatia futura
    (`RF-01-19`, `RN-01-22`, `RN-01-30`, design — decisões).
    """

    __tablename__ = "nick"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    persona_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("persona.id"), nullable=False)
    valor: Mapped[str] = mapped_column(String(64), nullable=False)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        # Insensível a caixa (`RN-01-30`, design — Decisions): "Zeferina" e
        # "zeferina" são o mesmo nick para a unicidade.
        Index("uq_nick_valor", func.lower(valor), unique=True),
        Index("uq_nick_persona_id", "persona_id", unique=True),
    )


class TipoDeCredencial(enum.StrEnum):
    biometria = "biometria"
    login_social = "login_social"
    usuario_e_senha = "usuario_e_senha"
    dispositivo = "dispositivo"


class Credencial(Base):
    """Atributos do PRD-01 §8. O tipo `biometria`, usado a partir desta fatia,
    guarda o _template_ cifrado e codificado em `segredo` — maior que o hash
    de senha que a coluna foi dimensionada para caber, por isso `Text` e não
    `String` (design — decisões).

    O tipo `dispositivo` (`RF-01-67`, `RN-01-53`) é o próprio registro do
    sensor construído pelo Guerreiro(a): `persona_id` é o **coletor** da
    série, `serie_de_coleta_id` e `trilha_id` só existem nela, e os três
    campos de revogação — `revogada_por`, `motivo_da_revogacao`,
    `revogada_em` — espelham os já usados por `ChaveDeAplicacao` (`RF-01-68`).
    """

    __tablename__ = "credencial"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    persona_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("persona.id"), nullable=False)
    tipo: Mapped[TipoDeCredencial] = mapped_column(
        Enum(TipoDeCredencial, native_enum=False, length=32), nullable=False
    )
    identificador: Mapped[str] = mapped_column(String(256), nullable=False)
    segredo: Mapped[str | None] = mapped_column(Text, nullable=True)
    criada_por: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("persona.id"), nullable=True
    )
    criada_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    troca_pendente: Mapped[bool] = mapped_column(nullable=False, default=False)
    ativa: Mapped[bool] = mapped_column(nullable=False, default=True)
    serie_de_coleta_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("serie_de_coleta.id"), nullable=True
    )
    trilha_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("trilha.id"), nullable=True
    )
    revogada_por: Mapped[str | None] = mapped_column(String(128), nullable=True)
    motivo_da_revogacao: Mapped[str | None] = mapped_column(String(512), nullable=True)
    revogada_em: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        Index(
            "uq_credencial_identificador_por_tipo_ativa",
            "tipo",
            "identificador",
            unique=True,
            postgresql_where=text("ativa AND tipo != 'dispositivo'"),
        ),
        Index(
            "uq_credencial_dispositivo_serie_ativa",
            "serie_de_coleta_id",
            unique=True,
            postgresql_where=text("ativa AND tipo = 'dispositivo'"),
        ),
    )


class ArtefatoComprobatorio(Base):
    """Prova declarada do adulto — link de currículo, portfólio, redes ou
    documento externo —, nunca anexo de arquivo (`RF-02-02`, `RF-02-03`,
    `RF-02-04`, `RN-02-01`, documento 02 §1). A persona pode ter vários;
    satélite porque é atributo próprio de Mestre e de Apoiador, no mesmo
    precedente do nick (design — decisões).
    """

    __tablename__ = "artefato_comprobatorio"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    persona_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("persona.id"), nullable=False)
    endereco: Mapped[str] = mapped_column(String(512), nullable=False)
    rotulo: Mapped[str] = mapped_column(String(256), nullable=False)
    # Quem declarou o artefato — nulo é, por definição, o cadastro (todo o
    # legado nasceu assim); a rota nova sempre grava a persona em sessão. É
    # o que decide a remoção: só quem declarou remove (`RN-09-14`, decisão
    # do fundador, 2026-08-29, documento 09 §1).
    declarado_por_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("persona.id"), nullable=True
    )
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
