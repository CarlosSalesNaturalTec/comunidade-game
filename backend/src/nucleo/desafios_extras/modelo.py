import enum
import uuid
from datetime import date

from sqlalchemy import CheckConstraint, Date, Enum, ForeignKey, Integer, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from ..autoria import ComAutoria
from ..banco import Base


class Modalidade(enum.StrEnum):
    """`direcionado` exige nick do destinatário e justificativa do vínculo;
    `aberto` não barra ninguém, só limita a quantidade de recompensas
    (`RF-14-31`, `RF-14-32`, `RN-14-16`)."""

    aberto = "aberto"
    direcionado = "direcionado"


class FormatoDoDesafioExtra(enum.StrEnum):
    presencial = "presencial"
    on_line = "on_line"


class CusteioDoDesafioExtra(enum.StrEnum):
    """A recompensa é sempre uma quantidade de um tipo de recurso num ponto
    de apoio — o custeio declara de onde vem o lastro dela: um aporte já
    homologado do próprio proponente, ou o saldo de recurso já existente na
    plataforma (`RF-14-76`, `RF-07-41`)."""

    aporte_do_proponente = "aporte_do_proponente"
    saldo_de_recurso = "saldo_de_recurso"


class SituacaoDoDesafioExtra(enum.StrEnum):
    """Toda proposta nasce em `em_validacao_do_mestre`; as transições para
    as demais situações são das fatias 15 do PRD-09 e do PRD-02, fora
    desta (`RF-14-35`, `RN-14-13`)."""

    em_validacao_do_mestre = "em_validacao_do_mestre"
    em_aprovacao_do_admin = "em_aprovacao_do_admin"
    publicado = "publicado"
    recusado = "recusado"


class DesafioExtra(Base, ComAutoria):
    """O desafio que o Apoiador propõe a uma trilha em andamento (PRD-14
    §8). `ComAutoria.autor_id` grava o proponente.

    O **nick do destinatário** é coluna de texto, sem `ForeignKey` e sem
    consulta de existência na escrita — é o que impede a aplicação de
    confirmar que o nick existe; a ligação com a pessoa é feita só na
    validação do Mestre, fora desta fatia (`RF-14-33`, `RN-14-18`, design —
    Decisions).

    A **recompensa** é uma quantidade (`quantidade_disponivel`) de um
    `tipo_de_recurso` guardada num `ponto_de_apoio` — o mesmo desenho do
    item do catálogo avulso. `lastro_provido` (`desafios_extras.regra`) não
    é coluna: é lido na hora a partir do `custeio` declarado, no mesmo
    padrão do `ItemDeCatalogoAvulso.ativo` (design — Decisions).

    **Etiquetas ODS herdadas** (PRD-14 §8) não são coluna: são as de
    `EtiquetaOds` da trilha (e da missão, quando declarada), lidas na
    leitura — nunca duplicadas aqui.

    A **imutabilidade do publicado** é guarda de escrita em `regra.py`
    (405), não de leitura: a proposta anterior permanece registrada com o
    desfecho que teve (`RF-14-38`).
    """

    __tablename__ = "desafio_extra"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    trilha_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("trilha.id"), nullable=False)
    missao_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("missao.id"), nullable=True
    )
    modalidade: Mapped[Modalidade] = mapped_column(
        Enum(Modalidade, native_enum=False, length=16), nullable=False
    )
    nick_do_destinatario: Mapped[str | None] = mapped_column(Text, nullable=True)
    justificativa_do_vinculo: Mapped[str | None] = mapped_column(Text, nullable=True)
    tipo_de_recurso_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("tipo_de_recurso.id"), nullable=False
    )
    ponto_de_apoio_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("ponto_de_apoio.id"), nullable=False
    )
    quantidade_disponivel: Mapped[int] = mapped_column(Integer, nullable=False)
    criterio_de_atribuicao: Mapped[str] = mapped_column(Text, nullable=False)
    pontos_extras: Mapped[int] = mapped_column(Integer, nullable=False)
    formato: Mapped[FormatoDoDesafioExtra] = mapped_column(
        Enum(FormatoDoDesafioExtra, native_enum=False, length=16), nullable=False
    )
    custeio: Mapped[CusteioDoDesafioExtra] = mapped_column(
        Enum(CusteioDoDesafioExtra, native_enum=False, length=24), nullable=False
    )
    aporte_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("aporte.id"), nullable=True
    )
    vigencia_inicio: Mapped[date] = mapped_column(Date, nullable=False)
    vigencia_fim: Mapped[date] = mapped_column(Date, nullable=False)
    mestre_validador_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("persona.id"), nullable=True
    )
    admin_aprovador_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("persona.id"), nullable=True
    )
    situacao: Mapped[SituacaoDoDesafioExtra] = mapped_column(
        Enum(SituacaoDoDesafioExtra, native_enum=False, length=24),
        nullable=False,
        default=SituacaoDoDesafioExtra.em_validacao_do_mestre,
    )
    motivo_da_recusa: Mapped[str | None] = mapped_column(Text, nullable=True)

    __table_args__ = (
        CheckConstraint(
            "pontos_extras >= 1 AND pontos_extras <= 10",
            name="ck_desafio_extra_pontos_extras_teto_10",
        ),
        CheckConstraint(
            "(modalidade = 'direcionado' AND nick_do_destinatario IS NOT NULL "
            "AND justificativa_do_vinculo IS NOT NULL) OR "
            "(modalidade = 'aberto' AND nick_do_destinatario IS NULL "
            "AND justificativa_do_vinculo IS NULL)",
            name="ck_desafio_extra_direcionado_exige_nick_e_justificativa",
        ),
        CheckConstraint(
            "vigencia_fim >= vigencia_inicio", name="ck_desafio_extra_fim_apos_ou_igual_ao_inicio"
        ),
    )
