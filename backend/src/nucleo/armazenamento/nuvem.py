from .porta import EnvioConsultado, PortaDeArmazenamento


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

    def abrir_sessao(self, *, referencia: str, tipo_mime: str, tamanho_declarado: int) -> str:
        """A sessão retomável nativa do Cloud Storage, que já fala o
        protocolo `Content-Range` — não se inventa protocolo novo (design —
        decisão 2)."""
        blob = self._bucket.blob(referencia)
        return blob.create_resumable_upload_session(content_type=tipo_mime, size=tamanho_declarado)

    def consultar_envio(self, *, referencia: str) -> EnvioConsultado | None:
        blob = self._bucket.blob(referencia)
        if not blob.exists():
            return None
        blob.reload()
        return EnvioConsultado(tamanho=blob.size, tipo_mime=blob.content_type)
