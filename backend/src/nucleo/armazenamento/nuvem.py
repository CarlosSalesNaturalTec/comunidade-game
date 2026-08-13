from .porta import PortaDeArmazenamento


class ArmazenamentoNoCloudStorage(PortaDeArmazenamento):
    """Adaptador de produção (documento 03 §1). O cliente do Cloud Storage
    só é importado na criação, para que desenvolvimento e a esteira —
    que nunca instanciam esta classe — não precisem da dependência
    instalada nem de credencial de nuvem (design — Decisions)."""

    def __init__(self, bucket: str) -> None:
        from google.cloud import storage

        self._bucket = storage.Client().bucket(bucket)

    def gravar(self, *, referencia: str, conteudo: bytes) -> None:
        self._bucket.blob(referencia).upload_from_string(conteudo)

    def ler(self, *, referencia: str) -> bytes:
        return self._bucket.blob(referencia).download_as_bytes()

    def remover(self, *, referencia: str) -> None:
        self._bucket.blob(referencia).delete()
