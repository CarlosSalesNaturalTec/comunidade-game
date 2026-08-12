import uuid

from sqlalchemy import DDL, CheckConstraint, ForeignKey, Integer, Uuid, event, inspect
from sqlalchemy.orm import Mapped, mapped_column

from ..banco import Base
from ..erros import DebitoDePontoExtraRecusado


class PontoExtra(Base):
    """Duas contas por Guerreiro(a): acumulado, que só cresce, e saldo
    disponível, que nunca fica negativo (`RN-01-39`, `RN-01-40`, documento
    11 §5). Nesta fatia as duas só recebem crédito; o débito por troca
    chega com o livro-razão (PRD-07, `RF-01-59`). O saldo negativo é
    recusado pela `CheckConstraint` abaixo, válida em qualquer via; a
    redução do acumulado é recusada pelos gatilhos, no mesmo padrão de
    `consentimentos.modelo`.
    """

    __tablename__ = "ponto_extra"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    guerreiro_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("persona.id"), nullable=False, unique=True
    )
    acumulado: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    saldo_disponivel: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    __table_args__ = (
        CheckConstraint("acumulado >= 0", name="ck_ponto_extra_acumulado_nao_negativo"),
        CheckConstraint("saldo_disponivel >= 0", name="ck_ponto_extra_saldo_nao_negativo"),
    )


def _recusar_debito_de_ponto_extra(mapper, connection, target: PontoExtra) -> None:
    historico = inspect(target).attrs.acumulado.history
    if not historico.deleted:
        return
    anterior = historico.deleted[0]
    novo = historico.added[0] if historico.added else target.acumulado
    if novo < anterior:
        raise DebitoDePontoExtraRecusado()


def _recusar_remocao_de_ponto_extra(mapper, connection, target: PontoExtra) -> None:
    raise DebitoDePontoExtraRecusado()


event.listen(PontoExtra, "before_update", _recusar_debito_de_ponto_extra)
event.listen(PontoExtra, "before_delete", _recusar_remocao_de_ponto_extra)

event.listen(
    PontoExtra.__table__,
    "after_create",
    DDL(
        """
        CREATE FUNCTION recusar_debito_de_ponto_extra() RETURNS trigger AS $$
        BEGIN
            IF (TG_OP = 'DELETE') THEN
                RAISE EXCEPTION
                    'ponto extra nunca é debitado nesta fatia: DELETE não é permitido';
            END IF;
            IF NEW.acumulado < OLD.acumulado THEN
                RAISE EXCEPTION
                    'o acumulado de ponto extra só cresce: não pode diminuir';
            END IF;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER trg_ponto_extra_acumulado_so_cresce
        BEFORE UPDATE OR DELETE ON ponto_extra
        FOR EACH ROW EXECUTE FUNCTION recusar_debito_de_ponto_extra();
        """
    ),
)
event.listen(
    PontoExtra.__table__,
    "before_drop",
    DDL(
        """
        DROP TRIGGER trg_ponto_extra_acumulado_so_cresce ON ponto_extra;
        DROP FUNCTION recusar_debito_de_ponto_extra();
        """
    ),
)
