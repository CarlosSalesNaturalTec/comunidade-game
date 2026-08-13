from abc import ABC, abstractmethod


class PortaDeArmazenamento(ABC):
    """Interface mínima para o comprovante — gravar, ler e remover, sem
    versionamento nem ciclo de vida (design — Decisions). O núcleo guarda
    só a referência; os bytes nunca entram na tabela (`RN-01-28`)."""

    @abstractmethod
    def gravar(self, *, referencia: str, conteudo: bytes) -> None: ...

    @abstractmethod
    def ler(self, *, referencia: str) -> bytes: ...

    @abstractmethod
    def remover(self, *, referencia: str) -> None: ...
