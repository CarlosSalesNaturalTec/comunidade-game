import enum
import uuid
from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    String,
    Text,
    Uuid,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from ..banco import Base


class Papel(enum.StrEnum):
    admin = "admin"
    mestre = "mestre"
    guerreiro = "guerreiro"
    responsavel = "responsavel"
    apoiador = "apoiador"


class ComunidadeVirtual(Base):
    """Território ao qual o Guerreiro(a) se vincula (RF-01-23). Criação,
    hierarquia de locais e transferência são comportamento do PRD-08; aqui
    ela existe só como entidade para que o vínculo e o filtro por comunidade
    tenham a que apontar — nenhuma rota desta fatia a expõe.
    """

    __tablename__ = "comunidade_virtual"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    nome: Mapped[str] = mapped_column(String(128), nullable=False)
    localizacao: Mapped[str] = mapped_column(String(256), nullable=False)
    granularidade_maxima: Mapped[str] = mapped_column(String(32), nullable=False)
    admin_criador_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid,
        ForeignKey("persona.id", name="fk_comunidade_virtual_admin_criador_id_persona"),
        nullable=True,
    )
    criada_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class Persona(Base):
    """Tabela única para os cinco papéis do PRD-01 §4 (RF-01-19). Atributo
    próprio de papel entra em tabela satélite quando a fatia que o traz
    chegar (design — riscos); o vínculo de comunidade do Guerreiro(a) é
    exceção deliberada, porque `RN-01-05` já o exige nesta fatia e a
    migração desta fatia cria só quatro tabelas.
    """

    __tablename__ = "persona"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    papel: Mapped[Papel] = mapped_column(Enum(Papel, native_enum=False, length=32), nullable=False)
    comunidade_virtual_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid,
        ForeignKey(
            "comunidade_virtual.id", name="fk_persona_comunidade_virtual_id_comunidade_virtual"
        ),
        nullable=True,
    )
    criada_por: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("persona.id"), nullable=True
    )
    criada_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        CheckConstraint(
            "papel != 'guerreiro' OR comunidade_virtual_id IS NOT NULL",
            name="ck_persona_guerreiro_tem_comunidade",
        ),
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
        Index("uq_nick_valor", "valor", unique=True),
        Index("uq_nick_persona_id", "persona_id", unique=True),
    )


class TipoDeCredencial(enum.StrEnum):
    biometria = "biometria"
    login_social = "login_social"
    usuario_e_senha = "usuario_e_senha"


class Credencial(Base):
    """Atributos do PRD-01 §8. O tipo `biometria`, usado a partir desta fatia,
    guarda o _template_ cifrado e codificado em `segredo` — maior que o hash
    de senha que a coluna foi dimensionada para caber, por isso `Text` e não
    `String` (design — decisões).
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

    __table_args__ = (
        Index(
            "uq_credencial_identificador_por_tipo_ativa",
            "tipo",
            "identificador",
            unique=True,
            postgresql_where=text("ativa"),
        ),
    )
