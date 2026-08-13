import uuid
from datetime import datetime

from sqlalchemy import DDL, DateTime, ForeignKey, Index, String, Uuid, event, func
from sqlalchemy.orm import Mapped, mapped_column

from ..banco import Base
from ..erros import AuditoriaImutavel


class Auditoria(Base):
    """Trilha central do PRD-01 §8: uma linha por escrita bem-sucedida sob
    `/v1`, de qualquer persona (proposal.md — Interpretação aplicada).
    Somente inserção, no mesmo padrão de `Consentimento` e
    `AcessoAoTemplate` — os listeners abaixo recusam `UPDATE` e `DELETE`
    também dentro do ORM, além do trigger da migração.
    """

    __tablename__ = "auditoria"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    autor_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("persona.id"), nullable=False)
    papel_do_autor: Mapped[str] = mapped_column(String(32), nullable=False)
    acao: Mapped[str] = mapped_column(String(256), nullable=False)
    entidade_afetada: Mapped[str] = mapped_column(String(128), nullable=False)
    momento: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    origem: Mapped[str] = mapped_column(String(64), nullable=False)

    __table_args__ = (
        Index("ix_auditoria_autor_id", "autor_id"),
        Index("ix_auditoria_momento", "momento"),
    )


def _recusar_alteracao(mapper, connection, target) -> None:
    raise AuditoriaImutavel()


event.listen(Auditoria, "before_update", _recusar_alteracao)
event.listen(Auditoria, "before_delete", _recusar_alteracao)

# Cópia do trigger da migração, presa à criação/remoção da tabela — o mesmo
# papel que a cópia equivalente cumpre em `consentimentos/modelo.py`.
event.listen(
    Auditoria.__table__,
    "after_create",
    DDL(
        """
        CREATE FUNCTION recusar_alteracao_de_auditoria() RETURNS trigger AS $$
        BEGIN
            RAISE EXCEPTION
                'auditoria é somente inserção: UPDATE e DELETE não são permitidos';
        END;
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER trg_auditoria_somente_insercao
        BEFORE UPDATE OR DELETE ON auditoria
        FOR EACH ROW EXECUTE FUNCTION recusar_alteracao_de_auditoria();
        """
    ),
)
event.listen(
    Auditoria.__table__,
    "before_drop",
    DDL(
        """
        DROP TRIGGER trg_auditoria_somente_insercao ON auditoria;
        DROP FUNCTION recusar_alteracao_de_auditoria();
        """
    ),
)
