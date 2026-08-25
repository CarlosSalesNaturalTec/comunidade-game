import json
from pathlib import Path

from .porta import EnvioConsultado, PortaDeArmazenamento


class ArmazenamentoEmDisco(PortaDeArmazenamento):
    """Adaptador padrão em desenvolvimento e na esteira (design — Migration
    Plan): grava no sistema de arquivos local, sem depender de credencial
    de nuvem. A sessão retomável expõe o mesmo protocolo `Content-Range`
    do Cloud Storage, por uma rota própria do núcleo — `armazenamento.rotas`
    — que chama os métodos abaixo (design — decisão 2)."""

    def __init__(self, diretorio: str, diretorio_sessoes: str) -> None:
        self._diretorio = Path(diretorio)
        self._diretorio.mkdir(parents=True, exist_ok=True)
        self._diretorio_sessoes = Path(diretorio_sessoes)
        self._diretorio_sessoes.mkdir(parents=True, exist_ok=True)

    def gravar(self, *, referencia: str, conteudo: bytes) -> None:
        caminho = self._diretorio / referencia
        caminho.parent.mkdir(parents=True, exist_ok=True)
        caminho.write_bytes(conteudo)

    def ler(self, *, referencia: str) -> bytes:
        return (self._diretorio / referencia).read_bytes()

    def remover(self, *, referencia: str) -> None:
        (self._diretorio / referencia).unlink(missing_ok=True)

    @staticmethod
    def chave_da_sessao(referencia: str) -> str:
        """A referência vira um único segmento de caminho da rota local
        (`armazenamento.rotas`). Troca a barra por `__` em vez de
        percent-encoding: o ASGI decodifica `%2F` antes do roteamento, o
        que quebraria o casamento de um único segmento `{chave}` — a
        referência nunca contém `__` por conta própria."""
        return referencia.replace("/", "__")

    def _caminho_parcial(self, chave: str) -> Path:
        return self._diretorio_sessoes / chave

    def _caminho_meta(self, chave: str) -> Path:
        return self._diretorio_sessoes / f"{chave}.meta.json"

    def abrir_sessao(self, *, referencia: str, tipo_mime: str, tamanho_declarado: int) -> str:
        chave = self.chave_da_sessao(referencia)
        self._caminho_meta(chave).write_text(
            json.dumps({"tipo_mime": tipo_mime, "tamanho_declarado": tamanho_declarado})
        )
        self._caminho_parcial(chave).write_bytes(b"")
        return f"/v1/armazenamento/sessoes/{chave}"

    def bytes_recebidos(self, *, chave: str) -> int:
        caminho = self._caminho_parcial(chave)
        return caminho.stat().st_size if caminho.exists() else 0

    def tamanho_declarado(self, *, chave: str) -> int | None:
        caminho = self._caminho_meta(chave)
        if not caminho.exists():
            return None
        return json.loads(caminho.read_text())["tamanho_declarado"]

    def receber_parte(self, *, chave: str, inicio: int, conteudo: bytes) -> int:
        """Escreve a parte na posição declarada, para que a retomada depois
        de queda no meio produza o mesmo arquivo do envio inteiro
        (`RF-09-19`)."""
        caminho = self._caminho_parcial(chave)
        with caminho.open("r+b") as arquivo:
            arquivo.seek(inicio)
            arquivo.write(conteudo)
        return caminho.stat().st_size

    def concluir_sessao(self, *, chave: str, referencia: str) -> None:
        meta = json.loads(self._caminho_meta(chave).read_text())
        destino = self._diretorio / referencia
        destino.parent.mkdir(parents=True, exist_ok=True)
        self._caminho_parcial(chave).replace(destino)
        meta["tamanho_real"] = destino.stat().st_size
        self._caminho_meta(chave).write_text(json.dumps(meta))

    def consultar_envio(self, *, referencia: str) -> EnvioConsultado | None:
        chave = self.chave_da_sessao(referencia)
        caminho_meta = self._caminho_meta(chave)
        if not caminho_meta.exists():
            return None
        meta = json.loads(caminho_meta.read_text())
        if "tamanho_real" not in meta:
            return None
        return EnvioConsultado(tamanho=meta["tamanho_real"], tipo_mime=meta["tipo_mime"])
