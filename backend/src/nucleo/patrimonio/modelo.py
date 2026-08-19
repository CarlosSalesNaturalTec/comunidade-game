import enum
import uuid

from sqlalchemy import DDL, Enum, ForeignKey, Index, String, UniqueConstraint, Uuid, event
from sqlalchemy.orm import Mapped, mapped_column

from ..autoria import ComAutoria
from ..banco import Base
from ..erros import FichaDeVidaImutavel


class TeorDaAnotacao(enum.StrEnum):
    """O que a ficha de vida registra sobre o exemplar (`RF-07-48`,
    design — Decisions 2)."""

    cuidado = "cuidado"
    perda = "perda"
    dano = "dano"


class ItemPatrimonial(Base, ComAutoria):
    """O exemplar permanente tombado num ponto de apoio — a face do
    livro-razão que não se consome (`RF-07-11`, PRD-07 §8). O aporte de
    origem é opcional e, quando declarado, precisa ser de tipo durável e
    não pode exceder a quantidade aportada (`RN-07-07`, design —
    Decisions 6).

    O **responsável não é coluna aqui**: deriva do `PontoDeApoio.
    responsavel_id` por junção, para que a troca do responsável alcance
    todos os exemplares sem escrita em cada um (`RN-07-10`, design —
    Decisions 4). `estado_de_conservacao` guarda o **corrente**, reescrito
    a cada anotação da ficha de vida — a leitura do acervo não depende de
    subconsulta por item (design — Decisions 3).
    """

    __tablename__ = "item_patrimonial"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    aporte_de_origem_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("aporte.id"), nullable=True
    )
    titulo: Mapped[str] = mapped_column(String(256), nullable=False)
    numero_de_tombo: Mapped[str] = mapped_column(String(64), nullable=False)
    ponto_de_apoio_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("ponto_de_apoio.id"), nullable=False
    )
    estado_de_conservacao: Mapped[str] = mapped_column(String(128), nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "ponto_de_apoio_id",
            "numero_de_tombo",
            name="uq_item_patrimonial_ponto_de_apoio_numero_de_tombo",
        ),
        Index("ix_item_patrimonial_ponto_de_apoio_id", "ponto_de_apoio_id"),
    )


class AnotacaoDaFichaDeVida(Base, ComAutoria):
    """A ficha de vida do exemplar — histórico de somente inserção, à
    imagem da imutabilidade que `Lancamento` já pratica (`RF-07-11`,
    `RF-07-48`, design — Decisions 2). Perda e dano nunca viram débito: a
    anotação não referencia Guerreiro(a) algum, e nenhuma rota altera ou
    remove uma anotação já gravada, também fora do ORM (`RN-07-09`, design
    — Decisions 7).
    """

    __tablename__ = "anotacao_da_ficha_de_vida"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    item_patrimonial_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("item_patrimonial.id"), nullable=False
    )
    teor: Mapped[TeorDaAnotacao] = mapped_column(
        Enum(TeorDaAnotacao, native_enum=False, length=16), nullable=False
    )
    estado_de_conservacao: Mapped[str] = mapped_column(String(128), nullable=False)

    __table_args__ = (
        Index("ix_anotacao_da_ficha_de_vida_item_patrimonial_id", "item_patrimonial_id"),
    )


def _recusar_alteracao(mapper, connection, target) -> None:
    raise FichaDeVidaImutavel()


event.listen(AnotacaoDaFichaDeVida, "before_update", _recusar_alteracao)
event.listen(AnotacaoDaFichaDeVida, "before_delete", _recusar_alteracao)

# O mesmo trigger da migração, preso à criação/remoção da tabela — mesmo
# papel que a cópia equivalente cumpre em `livro_razao/modelo.py` e
# `auditoria/modelo.py`.
event.listen(
    AnotacaoDaFichaDeVida.__table__,
    "after_create",
    DDL(
        """
        CREATE FUNCTION recusar_alteracao_de_anotacao_da_ficha_de_vida() RETURNS trigger AS $$
        BEGIN
            RAISE EXCEPTION
                'anotação da ficha de vida é somente inserção: UPDATE e DELETE não são permitidos';
        END;
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER trg_anotacao_da_ficha_de_vida_somente_insercao
        BEFORE UPDATE OR DELETE ON anotacao_da_ficha_de_vida
        FOR EACH ROW EXECUTE FUNCTION recusar_alteracao_de_anotacao_da_ficha_de_vida();
        """
    ),
)
event.listen(
    AnotacaoDaFichaDeVida.__table__,
    "before_drop",
    DDL(
        """
        DROP TRIGGER trg_anotacao_da_ficha_de_vida_somente_insercao ON anotacao_da_ficha_de_vida;
        DROP FUNCTION recusar_alteracao_de_anotacao_da_ficha_de_vida();
        """
    ),
)
