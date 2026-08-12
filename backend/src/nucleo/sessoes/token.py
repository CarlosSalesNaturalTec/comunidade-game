import hashlib
import secrets


def gerar_token() -> str:
    """256 bits de entropia — a rota nunca devolve o token de novo depois de
    aberta a sessão, como o segredo da chave (design — token opaco)."""
    return secrets.token_urlsafe(32)


def calcular_resumo(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()
