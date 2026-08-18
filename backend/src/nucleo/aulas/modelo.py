import enum
import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, Enum, ForeignKey, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from ..autoria import ComAutoria
from ..banco import Base
from ..tempo import ComMomentoDoFato


class Aula(Base, ComAutoria):
    """Aula/Agenda do PRD-01 §8: é dela que sai a comunidade do cadastro
    novo e a existência dela que habilita o onboarding, sem parâmetro de
    liberação separado (`RF-01-20`, `RF-01-32`). `inicio_em` e `fim_em`
    guardam o instante com fuso — a derivação das aulas vigentes vira uma
    comparação só contra `tempo.agora()` (design — decisões). `ComAutoria`
    grava o Admin que agendou. `ponto_de_apoio_id` é o espaço em que a aula
    acontece e de onde sai o recurso, sempre da mesma comunidade da aula
    (`RF-01-71`, `RN-07-33`).
    """

    __tablename__ = "aula"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    comunidade_virtual_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("comunidade_virtual.id"), nullable=False
    )
    ponto_de_apoio_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("ponto_de_apoio.id"), nullable=False
    )
    inicio_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    fim_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    __table_args__ = (CheckConstraint("fim_em > inicio_em", name="ck_aula_fim_em_apos_inicio_em"),)


class ModoDeComprovacao(enum.StrEnum):
    reconhecimento = "reconhecimento"
    confirmacao = "confirmacao"


class Presenca(Base, ComAutoria, ComMomentoDoFato):
    """Quem esteve na aula, por reconhecimento do próprio Guerreiro(a) ou
    confirmação de Mestre ou Admin, com o registro de quem confirmou
    (`RF-01-20`, `RF-01-03`). Única por (aula, guerreiro): o reenvio do
    App 01 depois de operar com a rede fora não duplica o registro
    (PRD-01 §10, design — decisões). `ComMomentoDoFato` guarda quando a
    presença aconteceu, separado de quando o núcleo recebeu o registro.
    """

    __tablename__ = "presenca"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    aula_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("aula.id"), nullable=False)
    guerreiro_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("persona.id"), nullable=False)
    modo: Mapped[ModoDeComprovacao] = mapped_column(
        Enum(ModoDeComprovacao, native_enum=False, length=16), nullable=False
    )
    confirmador_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("persona.id"), nullable=True
    )

    __table_args__ = (
        UniqueConstraint("aula_id", "guerreiro_id", name="uq_presenca_aula_id_guerreiro_id"),
    )
