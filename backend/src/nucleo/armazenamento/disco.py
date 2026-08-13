from pathlib import Path

from .porta import PortaDeArmazenamento


class ArmazenamentoEmDisco(PortaDeArmazenamento):
    """Adaptador padrão em desenvolvimento e na esteira (design — Migration
    Plan): grava no sistema de arquivos local, sem depender de credencial
    de nuvem."""

    def __init__(self, diretorio: str) -> None:
        self._diretorio = Path(diretorio)
        self._diretorio.mkdir(parents=True, exist_ok=True)

    def gravar(self, *, referencia: str, conteudo: bytes) -> None:
        caminho = self._diretorio / referencia
        caminho.parent.mkdir(parents=True, exist_ok=True)
        caminho.write_bytes(conteudo)

    def ler(self, *, referencia: str) -> bytes:
        return (self._diretorio / referencia).read_bytes()

    def remover(self, *, referencia: str) -> None:
        (self._diretorio / referencia).unlink(missing_ok=True)
