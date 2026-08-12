import time
from collections.abc import Callable
from typing import Annotated

import httpx
from fastapi import Depends
from google.auth.exceptions import TransportError
from google.auth.transport import Request as RequestDeTransporte
from google.auth.transport import Response as RespostaDeTransporte
from google.oauth2 import id_token as google_id_token

from ..configuracao import Configuracao, obter_configuracao
from ..erros import ServicoIndisponivel

TEMPO_DE_CACHE_DO_JWKS_EM_SEGUNDOS = 3600


class TokenSocialInvalido(Exception):
    """O _ID token_ não confere assinatura, audiência ou validade."""


class _RespostaHttpx(RespostaDeTransporte):
    def __init__(self, resposta: httpx.Response) -> None:
        self._resposta = resposta

    @property
    def status(self) -> int:
        return self._resposta.status_code

    @property
    def headers(self) -> dict:
        return dict(self._resposta.headers)

    @property
    def data(self) -> bytes:
        return self._resposta.content


class _RequisicaoComCacheDoJwks(RequestDeTransporte):
    """Adapta `httpx` ao contrato de `google.auth.transport.Request`, com
    cache do JWKS em memória de processo (design — decisões do fluxo
    social). Falha de rede vira `TransportError`, que a rota converte em
    503 — nunca 401 (design — riscos).
    """

    def __init__(self) -> None:
        self._cache: dict[str, tuple[float, httpx.Response]] = {}

    def __call__(self, url, method="GET", body=None, headers=None, timeout=None, **kwargs):
        agora = time.monotonic()
        if method == "GET" and url in self._cache:
            buscado_em, resposta_cacheada = self._cache[url]
            if agora - buscado_em < TEMPO_DE_CACHE_DO_JWKS_EM_SEGUNDOS:
                return _RespostaHttpx(resposta_cacheada)

        try:
            resposta = httpx.request(
                method, url, content=body, headers=headers, timeout=timeout or 10
            )
        except httpx.HTTPError as exc:
            raise TransportError(str(exc)) from exc

        if method == "GET" and resposta.status_code == 200:
            self._cache[url] = (agora, resposta)
        return _RespostaHttpx(resposta)


_requisicao = _RequisicaoComCacheDoJwks()


def verificar_id_token(token: str, configuracao: Configuracao) -> str:
    """Confere assinatura, audiência e validade contra o JWKS do Google e
    devolve o e-mail da conta associada (design — fluxo social)."""
    try:
        claims = google_id_token.verify_oauth2_token(
            token, _requisicao, audience=configuracao.google_client_id or None
        )
    except TransportError as exc:
        raise ServicoIndisponivel() from exc
    except Exception as exc:
        raise TokenSocialInvalido() from exc
    return claims["email"]


def obter_verificador_social(
    configuracao: Annotated[Configuracao, Depends(obter_configuracao)],
) -> Callable[[str], str]:
    def _verificar(token: str) -> str:
        return verificar_id_token(token, configuracao)

    return _verificar
