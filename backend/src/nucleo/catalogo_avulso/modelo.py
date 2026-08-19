import enum
import uuid
from decimal import Decimal

from sqlalchemy import Boolean, CheckConstraint, Enum, ForeignKey, Numeric, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from ..autoria import ComAutoria
from ..banco import Base


class OrigemDoCadastroDoItem(enum.StrEnum):
    """Quem cadastrou decide se o item precisa de homologação de Admin
    (`RF-09-100`, `RN-14-42`)."""

    mestre = "mestre"
    apoiador = "apoiador"


class SituacaoDeHomologacao(enum.StrEnum):
    """`nao_se_aplica` é o item de Mestre, que dispensa homologação;
    `pendente` nasce inativo até o Admin decidir (`RF-09-100`, `RN-14-42`)."""

    nao_se_aplica = "nao_se_aplica"
    pendente = "pendente"
    homologado = "homologado"
    recusado = "recusado"


class ItemDeCatalogoAvulso(Base, ComAutoria):
    """A recompensa avulsa que o Guerreiro(a) troca por pontos extras — a
    troca em si é capacidade própria, fora desta fatia (`RF-07-33`,
    PRD-07 §8). O preço não é coluna daqui: lido sempre da vigência
    corrente de `recursos.modelo.PrecoDeReferencia` do seu tipo de recurso,
    nunca declarado no cadastro (`RF-07-45`, `RN-07-29`).

    `ponto_de_apoio_id` é decisão nova desta fatia (documento 04 §1): o
    saldo que lastreia o item é por tipo **e** ponto de apoio, e sem essa
    dimensão o item não acha o saldo que o lastreia. `ativo` nasce falso e
    só passa a verdadeiro quando homologação, preço de referência vigente e
    lastro convergem — recalculado a cada escrita que possa mudar qualquer
    uma das três condições, nunca puramente derivado na leitura (`RF-07-34`,
    `RN-07-26`, design — Decisions).

    `ComAutoria` grava quem cadastrou; a retirada e a alteração de estoque
    não a reescrevem — a trilha de auditoria transversal (`RF-01-29`) já
    cobre quem operou depois, o mesmo precedente de `Aula.cancelamento_
    motivo`. `homologacao_motivo` só se preenche na recusa.
    """

    __tablename__ = "item_de_catalogo_avulso"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    nome: Mapped[str] = mapped_column(String(128), nullable=False)
    tipo_de_recurso_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("tipo_de_recurso.id"), nullable=False
    )
    estoque: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    comunidade_virtual_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("comunidade_virtual.id"), nullable=False
    )
    ponto_de_apoio_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("ponto_de_apoio.id"), nullable=False
    )
    origem_do_cadastro: Mapped[OrigemDoCadastroDoItem] = mapped_column(
        Enum(OrigemDoCadastroDoItem, native_enum=False, length=16), nullable=False
    )
    situacao_de_homologacao: Mapped[SituacaoDeHomologacao] = mapped_column(
        Enum(SituacaoDeHomologacao, native_enum=False, length=16), nullable=False
    )
    homologacao_motivo: Mapped[str | None] = mapped_column(Text, nullable=True)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    __table_args__ = (
        # O piso de gestão continua sendo 1 (`catalogo_avulso.regra.ESTOQUE_MINIMO`), aplicado
        # no cadastro e na alteração de estoque; a trava de banco só impede negativo, porque a
        # troca (PRD-07) decrementa até zero sem passar por esse caminho (`RF-07-36`, `RN-07-27`).
        CheckConstraint("estoque >= 0", name="ck_item_de_catalogo_avulso_estoque_nao_negativo"),
    )
