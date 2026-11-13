import enum
import uuid
from datetime import datetime

from sqlalchemy import (
    DDL,
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    String,
    Uuid,
    event,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from ..banco import Base
from ..erros import LancamentoDePontuacaoImutavel


class ContaDoLancamento(enum.StrEnum):
    regular = "regular"
    extra = "extra"


class OrigemDoLancamento(enum.StrEnum):
    """O fato que moveu a conta (design — decisão 3). O rótulo em linguagem
    simples é das aplicações."""

    resultado = "resultado"
    merito_do_resultado = "merito_do_resultado"
    criacao_original = "criacao_original"
    partida_de_quiz = "partida_de_quiz"
    registro_de_coleta = "registro_de_coleta"
    estorno_de_coleta = "estorno_de_coleta"
    desafio_pratico = "desafio_pratico"
    ocorrencia_de_conduta = "ocorrencia_de_conduta"
    presenca = "presenca"
    estorno_de_presenca = "estorno_de_presenca"
    cuidado_do_bem = "cuidado_do_bem"
    proposta_adotada = "proposta_adotada"
    troca = "troca"
    saldo_anterior = "saldo_anterior"


class LancamentoDePontuacao(Base):
    """Um movimento de ponto regular ou extra, somente inserção (`RF-01-88`,
    `RN-01-67`). `valor` é o que de fato moveu a conta — na regular, o total
    da trilha ou do poder; na extra, o saldo disponível —, e
    `valor_no_acumulado` o que moveu o acumulado da extra. O motivo da
    conduta nunca é copiado aqui: a leitura o busca na ocorrência pela
    `referencia_id`, para que a guarda dele valha também no histórico
    (design — decisão 4)."""

    __tablename__ = "lancamento_de_pontuacao"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    guerreiro_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("persona.id"), nullable=False)
    conta: Mapped[ContaDoLancamento] = mapped_column(
        Enum(ContaDoLancamento, native_enum=False, length=16), nullable=False
    )
    trilha_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("trilha.id"), nullable=True
    )
    poder_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, ForeignKey("poder.id"), nullable=True)
    origem: Mapped[OrigemDoLancamento] = mapped_column(
        Enum(OrigemDoLancamento, native_enum=False, length=32), nullable=False
    )
    referencia_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, nullable=True)
    detalhe: Mapped[str | None] = mapped_column(String(256), nullable=True)
    valor: Mapped[int] = mapped_column(Integer, nullable=False)
    valor_no_acumulado: Mapped[int | None] = mapped_column(Integer, nullable=True)
    registrado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        CheckConstraint(
            "(conta = 'regular' AND (trilha_id IS NOT NULL) != (poder_id IS NOT NULL)"
            " AND valor_no_acumulado IS NULL)"
            " OR (conta = 'extra' AND trilha_id IS NULL AND poder_id IS NULL"
            " AND valor_no_acumulado IS NOT NULL)",
            name="ck_lancamento_de_pontuacao_conta",
        ),
        Index(
            "ix_lancamento_de_pontuacao_guerreiro_registrado_em",
            "guerreiro_id",
            "registrado_em",
            "id",
        ),
    )


def _recusar_alteracao(mapper, connection, target) -> None:
    raise LancamentoDePontuacaoImutavel()


event.listen(LancamentoDePontuacao, "before_update", _recusar_alteracao)
event.listen(LancamentoDePontuacao, "before_delete", _recusar_alteracao)

# O mesmo gatilho da migração, preso à criação/remoção da tabela, para que
# `Base.metadata.create_all()` — caminho dos testes — também recuse fora do
# ORM (mesmo padrão de `pontuacao.modelo`).
event.listen(
    LancamentoDePontuacao.__table__,
    "after_create",
    DDL(
        """
        CREATE FUNCTION recusar_alteracao_de_lancamento_de_pontuacao() RETURNS trigger AS $$
        BEGIN
            RAISE EXCEPTION 'lançamento de pontuação é somente inserção';
        END;
        $$ LANGUAGE plpgsql;
        CREATE TRIGGER trg_lancamento_de_pontuacao_somente_insercao
        BEFORE UPDATE OR DELETE ON lancamento_de_pontuacao
        FOR EACH ROW EXECUTE FUNCTION recusar_alteracao_de_lancamento_de_pontuacao();
        """
    ),
)
event.listen(
    LancamentoDePontuacao.__table__,
    "before_drop",
    DDL(
        """
        DROP TRIGGER trg_lancamento_de_pontuacao_somente_insercao ON lancamento_de_pontuacao;
        DROP FUNCTION recusar_alteracao_de_lancamento_de_pontuacao();
        """
    ),
)
