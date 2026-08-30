import enum
import uuid

from sqlalchemy import Boolean, Enum, Index, String, Text, Uuid, text
from sqlalchemy.orm import Mapped, mapped_column

from ..autoria import ComAutoria
from ..banco import Base


class NaturezaDoPoder(enum.StrEnum):
    de_guerreiro = "de_guerreiro"
    derivado_do_aporte = "derivado_do_aporte"


class VigenciaDoPoder(enum.StrEnum):
    vigente = "vigente"
    ciclo_futuro = "ciclo_futuro"


# O papel que um poder exerce nas regras da plataforma, declarado por Admin —
# nunca deduzido do `nome`, que é só rótulo de exibição (`RN-01-54`). Hoje só
# o papel do Território existe: é o que o crédito da coleta busca
# (`RN-08-15`). Comentário, não docstring: a classe agora entra em resposta
# HTTP (`catalogo-de-poderes-e-tela-da-gestao`), e um docstring vira
# descrição no schema OpenAPI publicado sem chave — `território`, aqui,
# fugiria da convenção de `test_openapi_nao_serve_dado_de_dominio`.
class PapelDoPoder(enum.StrEnum):
    territorio = "territorio"


class Poder(Base, ComAutoria):
    """Catálogo cadastrado por Admin a que toda trilha se vincula
    (`RF-01-62`). A natureza distingue o poder que o Guerreiro(a) conquista
    do derivado do aporte (`RN-01-43`, documento 99 §6 invariante 21) — só o
    primeiro recebe trilha. A vigência só descreve o que vale no ciclo
    corrente e nunca trava vínculo de trilha (02 §2, design — decisões).
    `papel` é opcional — a maioria dos poderes não exerce papel algum — e o
    índice único parcial garante no máximo um poder com o papel do
    Território (`RN-01-54`).
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
    papel: Mapped[PapelDoPoder | None] = mapped_column(
        Enum(PapelDoPoder, native_enum=False, length=16), nullable=True
    )
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    # Declarada por Admin, nunca deduzida do nome — mesmo princípio do `papel`
    # (`RN-01-54`). Só orienta a sugestão do template de atividade desplugada;
    # não é papel e não tem limite de quantos poderes a recebem (`RF-01-62`,
    # `RN-09-34`, decisão do fundador de 2026-08-29).
    tecnico: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    __table_args__ = (
        Index(
            "uq_poder_papel_territorio",
            "papel",
            unique=True,
            postgresql_where=text("papel = 'territorio'"),
        ),
    )
