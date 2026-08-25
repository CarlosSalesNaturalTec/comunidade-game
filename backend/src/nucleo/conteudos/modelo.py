import enum
import uuid

from sqlalchemy import Enum, ForeignKey, Integer, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from ..autoria import ComAutoria
from ..banco import Base


class TipoDeConteudo(enum.StrEnum):
    """Os cinco tipos do `RF-09-14`, `RF-09-15` e PRD-09 §8. Texto e link
    externo trazem o que lhes cabe na criação; imagem, vídeo e arquivo
    nascem sem bytes e os recebem depois, pela sessão de envio (design —
    decisão 4)."""

    texto = "texto"
    imagem = "imagem"
    link_externo = "link_externo"
    video = "video"
    arquivo = "arquivo"


class AutoriaDoConteudo(enum.StrEnum):
    propria = "propria"
    terceiro = "terceiro"


class ConteudoDaMissao(Base, ComAutoria):
    """O corpo da missão (PRD-09 §8) — nome distinto de
    `apoio_escolar.modelo.Conteudo`, o corpus fechado de outra fatia, que já
    ocupa a classe e a tabela `conteudo`. `corpo`, `endereco`, `referencia`
    e `tamanho` são todos anuláveis, com a coerência conferida na regra e
    não no banco — cada tipo traz só o que lhe corresponde (design —
    decisão 4). `referencia` só é gravada quando
    `conteudos.regra.confirmar_envio` apura, no armazenamento, o tamanho e
    o tipo reais do arquivo — nunca no ato de abrir a sessão (design —
    decisão 1). `fonte` é exigida na autoria de terceiro (`RF-09-24`).
    """

    __tablename__ = "conteudo_da_missao"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    missao_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("missao.id"), nullable=False)
    ordem: Mapped[int] = mapped_column(Integer, nullable=False)
    tipo: Mapped[TipoDeConteudo] = mapped_column(
        Enum(TipoDeConteudo, native_enum=False, length=16), nullable=False
    )
    corpo: Mapped[str | None] = mapped_column(Text, nullable=True)
    endereco: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    referencia: Mapped[str | None] = mapped_column(String(512), nullable=True)
    tamanho: Mapped[int | None] = mapped_column(Integer, nullable=True)
    autoria: Mapped[AutoriaDoConteudo] = mapped_column(
        Enum(AutoriaDoConteudo, native_enum=False, length=16), nullable=False
    )
    fonte: Mapped[str | None] = mapped_column(Text, nullable=True)
