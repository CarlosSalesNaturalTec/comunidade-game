import enum
import uuid

from sqlalchemy import DDL, Enum, ForeignKey, String, Uuid, event
from sqlalchemy.orm import Mapped, mapped_column

from ..autoria import ComAutoria
from ..banco import Base
from ..erros import ConsentimentoImutavel


class DecisaoDeConsentimento(enum.StrEnum):
    concede = "concede"
    nega = "nega"


class OrigemDoConsentimento(enum.StrEnum):
    propria = "propria"
    assistida = "assistida"
    impressa = "impressa"


class Consentimento(Base, ComAutoria):
    """Atributos do PRD-01 §8. `ComAutoria` cobre "quem operou" e a data e
    hora com fuso; `tipo` fica aberto, com os dois valores que os PRDs já
    nomeiam, sem virar enumeração fechada nesta fatia (design — decisões).
    Somente inserção: os _listeners_ abaixo recusam `UPDATE` e `DELETE`
    também dentro do ORM, além do _trigger_ da migração (`RN-01-12`).
    """

    __tablename__ = "consentimento"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    responsavel_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("persona.id"), nullable=False
    )
    guerreiro_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("persona.id"), nullable=False)
    tipo: Mapped[str] = mapped_column(String(64), nullable=False)
    versao_do_termo: Mapped[str] = mapped_column(String(32), nullable=False)
    decisao: Mapped[DecisaoDeConsentimento] = mapped_column(
        Enum(DecisaoDeConsentimento, native_enum=False, length=16), nullable=False
    )
    origem: Mapped[OrigemDoConsentimento] = mapped_column(
        Enum(OrigemDoConsentimento, native_enum=False, length=16), nullable=False
    )
    testemunha_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("persona.id"), nullable=True
    )
    anexo: Mapped[str | None] = mapped_column(String(512), nullable=True)


def _recusar_alteracao(mapper, connection, target) -> None:
    raise ConsentimentoImutavel()


event.listen(Consentimento, "before_update", _recusar_alteracao)
event.listen(Consentimento, "before_delete", _recusar_alteracao)

# O mesmo trigger da migração, preso à criação/remoção da tabela: garante que
# `Base.metadata.create_all()` — caminho que os testes usam, fora do Alembic —
# também recusa `UPDATE` e `DELETE` fora do ORM. A migração mantém a cópia
# dela própria porque uma migração é histórico congelado, e não deve mudar se
# este arquivo mudar.
event.listen(
    Consentimento.__table__,
    "after_create",
    DDL(
        """
        CREATE FUNCTION recusar_alteracao_de_consentimento() RETURNS trigger AS $$
        BEGIN
            RAISE EXCEPTION
                'consentimento é somente inserção: UPDATE e DELETE não são permitidos';
        END;
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER trg_consentimento_somente_insercao
        BEFORE UPDATE OR DELETE ON consentimento
        FOR EACH ROW EXECUTE FUNCTION recusar_alteracao_de_consentimento();
        """
    ),
)
event.listen(
    Consentimento.__table__,
    "before_drop",
    DDL(
        """
        DROP TRIGGER trg_consentimento_somente_insercao ON consentimento;
        DROP FUNCTION recusar_alteracao_de_consentimento();
        """
    ),
)
