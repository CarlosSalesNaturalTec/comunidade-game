import enum
import uuid

from sqlalchemy import Enum, ForeignKey, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from ..autoria import ComAutoria
from ..banco import Base
from ..tempo import ComMomentoDoFato


class DesfechoDoResultado(enum.StrEnum):
    realizada = "realizada"
    realizada_com_merito = "realizada_com_merito"
    merito_extra_por_auxilio = "merito_extra_por_auxilio"


class Resultado(Base, ComAutoria, ComMomentoDoFato):
    """Registro de que um Guerreiro(a) realizou uma atividade da trilha
    (documento 11 §4). `ComMomentoDoFato` guarda a data do fato separada da
    data do registro; `ComAutoria` grava quem lançou o desfecho — o Mestre
    autor da trilha ou o Admin (`trilhas.regra.conferir_posse_da_trilha`).
    O desfecho é enumeração fechada (design — decisões): os três valores que
    o documento 11 §4 declara, ao contrário da natureza aberta da atividade.
    """

    __tablename__ = "resultado"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    guerreiro_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("persona.id"), nullable=False)
    atividade_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("atividade.id"), nullable=False
    )
    producao: Mapped[str] = mapped_column(Text, nullable=False)
    desfecho: Mapped[DesfechoDoResultado] = mapped_column(
        Enum(DesfechoDoResultado, native_enum=False, length=32), nullable=False
    )
