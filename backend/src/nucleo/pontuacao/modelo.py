import enum
import uuid
from datetime import datetime

from sqlalchemy import (
    DDL,
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    UniqueConstraint,
    Uuid,
    event,
    func,
    inspect,
)
from sqlalchemy.orm import Mapped, mapped_column

from ..banco import Base
from ..erros import DebitoDePontoRegularRecusado


class PontoRegular(Base):
    """Ponto regular por Guerreiro(a) e trilha — nunca por poder nesta
    fatia, nem global (`RF-01-21`). Uma linha por par, somada a cada
    Resultado; o detalhe por evento fica para quando o crédito precisar de
    estorno (design — riscos). `total` nunca decresce nem é removido
    (`RF-01-57`, `RN-01-38`) — os gatilhos abaixo recusam fora do ORM tanto
    quanto dentro dele, no mesmo padrão de `consentimentos.modelo`.
    """

    __tablename__ = "ponto_regular"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    guerreiro_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("persona.id"), nullable=False)
    trilha_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("trilha.id"), nullable=False)
    total: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    __table_args__ = (
        UniqueConstraint(
            "guerreiro_id", "trilha_id", name="uq_ponto_regular_guerreiro_id_trilha_id"
        ),
        CheckConstraint("total >= 0", name="ck_ponto_regular_total_nao_negativo"),
    )


def _recusar_debito_de_ponto_regular(mapper, connection, target: PontoRegular) -> None:
    historico = inspect(target).attrs.total.history
    if not historico.deleted:
        return
    anterior = historico.deleted[0]
    novo = historico.added[0] if historico.added else target.total
    if novo < anterior:
        raise DebitoDePontoRegularRecusado()


def _recusar_remocao_de_ponto_regular(mapper, connection, target: PontoRegular) -> None:
    raise DebitoDePontoRegularRecusado()


event.listen(PontoRegular, "before_update", _recusar_debito_de_ponto_regular)
event.listen(PontoRegular, "before_delete", _recusar_remocao_de_ponto_regular)

# O mesmo gatilho da migração, preso à criação/remoção da tabela, para que
# `Base.metadata.create_all()` — caminho dos testes, fora do Alembic —
# também recuse fora do ORM (mesmo padrão de `consentimentos.modelo`).
event.listen(
    PontoRegular.__table__,
    "after_create",
    DDL(
        """
        CREATE FUNCTION recusar_debito_de_ponto_regular() RETURNS trigger AS $$
        BEGIN
            IF (TG_OP = 'DELETE') THEN
                RAISE EXCEPTION
                    'ponto regular nunca é debitado: DELETE não é permitido';
            END IF;
            IF NEW.total < OLD.total THEN
                RAISE EXCEPTION
                    'ponto regular nunca é debitado: total não pode diminuir';
            END IF;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER trg_ponto_regular_nunca_debita
        BEFORE UPDATE OR DELETE ON ponto_regular
        FOR EACH ROW EXECUTE FUNCTION recusar_debito_de_ponto_regular();
        """
    ),
)
event.listen(
    PontoRegular.__table__,
    "before_drop",
    DDL(
        """
        DROP TRIGGER trg_ponto_regular_nunca_debita ON ponto_regular;
        DROP FUNCTION recusar_debito_de_ponto_regular();
        """
    ),
)


class Nivel(Base):
    """Nível certificado por Guerreiro(a), trilha e valor — persistido como
    fato, não recalculado a cada leitura, para que a não regressão não
    precise de lógica extra além de nunca apagar o registro
    (`RF-01-21`, 11 §6, design — decisões).
    """

    __tablename__ = "nivel"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    guerreiro_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("persona.id"), nullable=False)
    trilha_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("trilha.id"), nullable=False)
    valor: Mapped[int] = mapped_column(Integer, nullable=False)
    certificado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        UniqueConstraint(
            "guerreiro_id", "trilha_id", "valor", name="uq_nivel_guerreiro_id_trilha_id_valor"
        ),
    )


class TipoDeBadge(enum.StrEnum):
    de_nivel = "de_nivel"
    de_valores_e_causas = "de_valores_e_causas"
    de_autoria = "de_autoria"
    de_protagonismo = "de_protagonismo"


class Badge(Base):
    """Badge certificado por Guerreiro(a), trilha ou poder — nunca global
    (`RF-01-21`, 11 §7), com **uma única exceção: o badge de protagonismo**,
    que é global porque a proposta que o rende é sobre a plataforma inteira,
    não sobre uma trilha (`RN-01-50`). Fora dessa exceção, exatamente uma
    das duas referências é preenchida; nesta fatia sempre `trilha_id`, já
    que `de_nivel`, `de_valores_e_causas` e `de_autoria` nascem de
    Resultado ou de Criação Original, sempre alcançáveis por trilha.
    `poder_id` existe para o badge de território de fatia futura (design —
    decisões). O badge de nível é concedido a cada nível certificado — por
    isso não há restrição de unicidade por (Guerreiro(a), trilha, tipo): um
    mesmo Guerreiro(a) acumula um badge de nível por nível alcançado na
    mesma trilha.
    """

    __tablename__ = "badge"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    guerreiro_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("persona.id"), nullable=False)
    trilha_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("trilha.id"), nullable=True
    )
    poder_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, ForeignKey("poder.id"), nullable=True)
    tipo: Mapped[TipoDeBadge] = mapped_column(
        Enum(TipoDeBadge, native_enum=False, length=32), nullable=False
    )
    certificado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        CheckConstraint(
            "(tipo = 'de_protagonismo' AND trilha_id IS NULL AND poder_id IS NULL) "
            "OR (tipo != 'de_protagonismo' AND (trilha_id IS NOT NULL) != (poder_id IS NOT NULL))",
            name="ck_badge_trilha_ou_poder",
        ),
    )
