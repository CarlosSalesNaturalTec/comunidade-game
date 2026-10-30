import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, String, Uuid, and_, func, text
from sqlalchemy.orm import Mapped, foreign, mapped_column, relationship

from ..banco import Base
from ..personas.modelo import Persona


class ComunidadeVirtual(Base):
    """A comunidade real, representada digitalmente. Nasce vazia — sem
    locais, sem séries e sem Guerreiros e Guerreiras —, criada só por Admin
    (`RF-08-01`, `RN-08-01`).
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


class VinculoJogador(Base):
    """Vínculo do Guerreiro(a) com a Comunidade Virtual, com histórico
    (PRD-08 §8). `data_fim` nula é o vínculo vigente, e o índice parcial
    único garante que só exista um por Guerreiro(a) mesmo sob concorrência
    (`RF-08-02`, `RN-08-02`, `RN-01-05`, design — Decisions).

    `admin_responsavel_id` é quem decide uma transferência — nula na
    abertura pela aula agendada, porque não há operador Admin nesse
    caminho de autocadastro. A rota de transferência é `RF-08-03`, fora do
    Ciclo 01: nada aqui a expõe.
    """

    __tablename__ = "vinculo_jogador"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    guerreiro_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("persona.id"), nullable=False)
    comunidade_virtual_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("comunidade_virtual.id"), nullable=False
    )
    data_inicio: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    data_fim: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    admin_responsavel_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("persona.id"), nullable=True
    )

    __table_args__ = (
        Index(
            "uq_vinculo_jogador_vigente",
            "guerreiro_id",
            unique=True,
            postgresql_where=text("data_fim IS NULL"),
        ),
    )


class VinculoDoMestre(Base):
    """Vínculo do **Mestre** com a Comunidade Virtual — entidade própria,
    separada do `VinculoJogador`, que é do Guerreiro(a) e tem um só vigente
    por pessoa (`RN-08-02`, `RN-01-05`).

    Duas diferenças de fundo, e as duas são decisão do fundador de
    2026-10-30 (documento 09 §1):

    - o Mestre pode estar vinculado a **mais de uma** comunidade, que é o
      plural que as specs de `patrimonio`, `necessidade-de-recurso`,
      `responsavel-e-vinculo` e `aula-e-presenca` já escreviam;
    - **não há `data_fim`**: no Ciclo 01 o vínculo do Mestre nunca encerra,
      e nenhuma rota o desfaz. Cancelar a aula que o abriu não o toca.

    Quem o abre é o **agendamento da aula** (`RF-02-30`), como a aula
    agendada já atribui a comunidade ao Guerreiro(a) que nela se cadastra
    (invariante 4 do documento 99 §6). O índice único por par impede o
    vínculo repetido quando o mesmo Mestre é escalado noutra aula da mesma
    comunidade.
    """

    __tablename__ = "vinculo_do_mestre"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    mestre_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("persona.id"), nullable=False)
    comunidade_virtual_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("comunidade_virtual.id"), nullable=False
    )
    data_inicio: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        Index(
            "uq_vinculo_do_mestre",
            "mestre_id",
            "comunidade_virtual_id",
            unique=True,
        ),
    )


# Ligada aqui, e não em `Persona`, para `personas/modelo.py` não depender de
# `comunidades` (`RF-01-23`) — é o acesso ao vínculo vigente a partir de uma
# persona já carregada que `aulas/regra.py` usa (design — Decisions).
Persona.vinculo_vigente = relationship(
    VinculoJogador,
    primaryjoin=lambda: and_(
        foreign(VinculoJogador.guerreiro_id) == Persona.id,
        VinculoJogador.data_fim.is_(None),
    ),
    viewonly=True,
    uselist=False,
)

# O par da linha acima para o Mestre: lista, e não um só, porque o vínculo
# dele é N comunidades e não tem vigência a conferir (decisão do fundador de
# 2026-10-30). Quem lê o escopo de uma leitura usa
# `comunidades_do_mestre`, em `regra.py`, não esta relação crua.
Persona.vinculos_do_mestre = relationship(
    VinculoDoMestre,
    primaryjoin=lambda: foreign(VinculoDoMestre.mestre_id) == Persona.id,
    viewonly=True,
    uselist=True,
)
