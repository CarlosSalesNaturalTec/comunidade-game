import enum
import uuid
from datetime import datetime

from sqlalchemy import DDL, DateTime, Enum, ForeignKey, Uuid, event, func
from sqlalchemy.orm import Mapped, mapped_column

from ..banco import Base
from ..erros import AcessoAoTemplateImutavel


class NaturezaDoAcesso(enum.StrEnum):
    gravacao = "gravacao"
    recadastro = "recadastro"
    comparacao_de_login = "comparacao_de_login"


class DesfechoDoAcesso(enum.StrEnum):
    sucesso = "sucesso"
    recusa = "recusa"


class AcessoAoTemplate(Base):
    """Guarda permanente do `RN-01-14`, alargado pelo documento 03 §3.3 para
    alcançar também cada comparação de login, não só gravação e recadastro.
    Somente inserção, como `Consentimento` — as duas camadas abaixo recusam
    `UPDATE` e `DELETE` também dentro do ORM, além do _trigger_ da migração.
    """

    __tablename__ = "acesso_ao_template"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    guerreiro_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("persona.id"), nullable=False)
    acessado_por: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("persona.id"), nullable=True
    )
    natureza: Mapped[NaturezaDoAcesso] = mapped_column(
        Enum(NaturezaDoAcesso, native_enum=False, length=32), nullable=False
    )
    desfecho: Mapped[DesfechoDoAcesso] = mapped_column(
        Enum(DesfechoDoAcesso, native_enum=False, length=16), nullable=False
    )
    momento: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


def _recusar_alteracao(mapper, connection, target) -> None:
    raise AcessoAoTemplateImutavel()


event.listen(AcessoAoTemplate, "before_update", _recusar_alteracao)
event.listen(AcessoAoTemplate, "before_delete", _recusar_alteracao)

# Cópia do trigger da migração, presa à criação/remoção da tabela — o mesmo
# papel que a cópia equivalente cumpre em `consentimentos/modelo.py`.
event.listen(
    AcessoAoTemplate.__table__,
    "after_create",
    DDL(
        """
        CREATE FUNCTION recusar_alteracao_de_acesso_ao_template() RETURNS trigger AS $$
        BEGIN
            RAISE EXCEPTION
                'acesso_ao_template é somente inserção: UPDATE e DELETE não são permitidos';
        END;
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER trg_acesso_ao_template_somente_insercao
        BEFORE UPDATE OR DELETE ON acesso_ao_template
        FOR EACH ROW EXECUTE FUNCTION recusar_alteracao_de_acesso_ao_template();
        """
    ),
)
event.listen(
    AcessoAoTemplate.__table__,
    "before_drop",
    DDL(
        """
        DROP TRIGGER trg_acesso_ao_template_somente_insercao ON acesso_ao_template;
        DROP FUNCTION recusar_alteracao_de_acesso_ao_template();
        """
    ),
)
