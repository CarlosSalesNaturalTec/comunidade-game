import enum
import uuid
from datetime import datetime

from sqlalchemy import DDL, DateTime, Enum, ForeignKey, Text, Uuid, event, func
from sqlalchemy.orm import Mapped, mapped_column

from ..banco import Base
from ..erros import FimDeVinculoImutavel


class OrigemDoFimDeVinculo(enum.StrEnum):
    admin = "admin"
    varredura = "varredura"


class FimDeVinculo(Base):
    """O marco que inicia os prazos de guarda dos dados do Guerreiro(a) com
    o projeto — ato de Admin ou varredura automática dos 12 meses sem
    atividade (`RF-13-44`, decisão do fundador, 2026-09-01). Único por
    Guerreiro(a): o vínculo já encerrado recusa segundo encerramento.
    Somente inserção, como `Consentimento` — os _listeners_ abaixo recusam
    `UPDATE` e `DELETE` também dentro do ORM, além do _trigger_ da migração.
    """

    __tablename__ = "fim_de_vinculo"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    guerreiro_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("persona.id"), unique=True, nullable=False
    )
    origem: Mapped[OrigemDoFimDeVinculo] = mapped_column(
        Enum(OrigemDoFimDeVinculo, native_enum=False, length=16), nullable=False
    )
    # Nulo na varredura — ela não é ato de ninguém (design — decisão 3).
    encerrado_por: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("persona.id"), nullable=True
    )
    motivo: Mapped[str] = mapped_column(Text, nullable=False)
    momento: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


def _recusar_alteracao(mapper, connection, target) -> None:
    raise FimDeVinculoImutavel()


event.listen(FimDeVinculo, "before_update", _recusar_alteracao)
event.listen(FimDeVinculo, "before_delete", _recusar_alteracao)

# Cópia do trigger da migração, presa à criação/remoção da tabela — o mesmo
# papel que a cópia equivalente cumpre em `consentimentos/modelo.py`.
event.listen(
    FimDeVinculo.__table__,
    "after_create",
    DDL(
        """
        CREATE FUNCTION recusar_alteracao_de_fim_de_vinculo() RETURNS trigger AS $$
        BEGIN
            RAISE EXCEPTION
                'fim_de_vinculo é somente inserção: UPDATE e DELETE não são permitidos';
        END;
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER trg_fim_de_vinculo_somente_insercao
        BEFORE UPDATE OR DELETE ON fim_de_vinculo
        FOR EACH ROW EXECUTE FUNCTION recusar_alteracao_de_fim_de_vinculo();
        """
    ),
)
event.listen(
    FimDeVinculo.__table__,
    "before_drop",
    DDL(
        """
        DROP TRIGGER trg_fim_de_vinculo_somente_insercao ON fim_de_vinculo;
        DROP FUNCTION recusar_alteracao_de_fim_de_vinculo();
        """
    ),
)
