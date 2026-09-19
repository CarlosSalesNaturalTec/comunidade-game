import enum
import uuid
from datetime import datetime

from sqlalchemy import DDL, DateTime, Enum, Float, ForeignKey, Integer, Uuid, event, func
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from ..autoria import ComAutoria
from ..banco import Base
from ..erros import AcessoAoTemplateImutavel


class NaturezaDoAcesso(enum.StrEnum):
    gravacao = "gravacao"
    recadastro = "recadastro"
    comparacao_de_login = "comparacao_de_login"
    apagamento = "apagamento"


class GatilhoDeApagamento(enum.StrEnum):
    """Os três gatilhos que marcam a data do apagamento do _template_, nos
    prazos do documento 03 §12.2 (`RF-13-43`, `RF-13-44`, `RN-13-22`)."""

    exclusao_deferida = "exclusao_deferida"
    recusa_biometria = "recusa_biometria"
    fim_do_vinculo = "fim_do_vinculo"


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


class ApagamentoDeTemplate(Base):
    """Marca a data em que o _template_ biométrico de um Guerreiro(a) será
    apagado — único por Guerreiro(a): é o que implementa "gatilho novo não
    empurra a data" (`RF-13-43`, `RF-13-44`, `RN-13-22`, decisão do
    fundador, 2026-09-01). Nenhuma rota edita ou substitui a marca; quem
    executa o apagamento em si é `apagar_templates_vencidos`.
    """

    __tablename__ = "apagamento_de_template"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    guerreiro_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("persona.id"), unique=True, nullable=False
    )
    gatilho: Mapped[GatilhoDeApagamento] = mapped_column(
        Enum(GatilhoDeApagamento, native_enum=False, length=32), nullable=False
    )
    apagar_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class MedicaoDoLimiar(Base, ComAutoria):
    """O limiar de comparação de um ponto de apoio, e as duas séries de
    distâncias que o produziram (`RF-01-73`, `RF-04-66`, `RN-04-35`,
    documento 03 §3.3, decisão do fundador, 2026-09-18).

    **A medição é a unidade gravada**, e o limiar vigente de um ponto de
    apoio é o da medição mais recente dele: não existe um segundo registro
    "vigente" para sair de sincronia com o histórico, e a medição suspeita
    continua consultável depois de substituída (design — decisão 4).

    Guarda **distâncias**, nunca descritor: o descritor nasce e morre no
    aparelho, e a rota que grava aqui o recusa (`RN-04-32`, `RN-01-15`).

    `pessoas_no_teto` é **declarado** por quem opera — o aparelho conta
    quantas vezes a pessoa diante da câmera trocou durante a série do teto.
    O núcleo não tem como conferir identidade aqui, e não finge que tem: o
    que ele reconfere são os mínimos e a folga, que estão nas séries
    (`RN-04-35`).
    """

    __tablename__ = "medicao_do_limiar"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    ponto_de_apoio_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("ponto_de_apoio.id"), nullable=False, index=True
    )
    limiar: Mapped[float] = mapped_column(Float, nullable=False)
    distancias_do_piso: Mapped[list[float]] = mapped_column(ARRAY(Float), nullable=False)
    distancias_do_teto: Mapped[list[float]] = mapped_column(ARRAY(Float), nullable=False)
    pessoas_no_teto: Mapped[int] = mapped_column(Integer, nullable=False)


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
