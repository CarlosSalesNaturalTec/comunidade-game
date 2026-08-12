import enum
import uuid

from sqlalchemy import Boolean, Enum, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from ..autoria import ComAutoria
from ..banco import Base


class NaturezaDoPoder(enum.StrEnum):
    de_guerreiro = "de_guerreiro"
    derivado_do_aporte = "derivado_do_aporte"


class VigenciaDoPoder(enum.StrEnum):
    vigente = "vigente"
    ciclo_futuro = "ciclo_futuro"


class Poder(Base, ComAutoria):
    """Catálogo cadastrado por Admin a que toda trilha se vincula
    (`RF-01-62`). A natureza distingue o poder que o Guerreiro(a) conquista
    do derivado do aporte (`RN-01-43`, documento 99 §6 invariante 21) — só o
    primeiro recebe trilha. A vigência só descreve o que vale no ciclo
    corrente e nunca trava vínculo de trilha (02 §2, design — decisões).
    """

    __tablename__ = "poder"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    nome: Mapped[str] = mapped_column(String(128), nullable=False)
    descricao: Mapped[str] = mapped_column(Text, nullable=False)
    natureza: Mapped[NaturezaDoPoder] = mapped_column(
        Enum(NaturezaDoPoder, native_enum=False, length=32), nullable=False
    )
    vigencia: Mapped[VigenciaDoPoder] = mapped_column(
        Enum(VigenciaDoPoder, native_enum=False, length=16), nullable=False
    )
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
