from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class EnvioConsultado:
    """O que a sessão retomável concluída devolve, apurado pelo próprio
    armazenamento — nunca o que o cliente declarou (`RF-09-16`, `RF-09-17`,
    design — decisão 1)."""

    tamanho: int
    tipo_mime: str


class PortaDeArmazenamento(ABC):
    """Interface do comprovante — gravar, ler e remover — acrescida da
    sessão retomável do vídeo e do arquivo de apoio (`RF-09-19`, design —
    decisão 2). O núcleo guarda só a referência; os bytes nunca entram na
    tabela (`RN-01-28`)."""

    @abstractmethod
    def gravar(self, *, referencia: str, conteudo: bytes) -> None: ...

    @abstractmethod
    def ler(self, *, referencia: str) -> bytes: ...

    @abstractmethod
    def remover(self, *, referencia: str) -> None: ...

    @abstractmethod
    def abrir_sessao(self, *, referencia: str, tipo_mime: str, tamanho_declarado: int) -> str:
        """Abre a sessão de envio retomável e devolve o endereço por onde o
        cliente enviará os bytes, em partes, direto ao armazenamento."""
        ...

    @abstractmethod
    def consultar_envio(self, *, referencia: str) -> EnvioConsultado | None:
        """`None` enquanto o envio não estiver concluído — conteúdo sem
        confirmação não serve bytes (`RF-09-16`, `RF-09-17`)."""
        ...
