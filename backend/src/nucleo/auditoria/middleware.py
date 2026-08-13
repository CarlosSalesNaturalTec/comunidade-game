import logging

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from ..autenticacao import ContextoDaSessao
from ..banco import obter_fabrica_de_sessao
from ..chaves.conferencia import ContextoDaChave
from .modelo import Auditoria

logger = logging.getLogger("nucleo.auditoria")

_METODOS_DE_ESCRITA = frozenset({"POST", "PUT", "PATCH", "DELETE"})
_PREFIXO_DE_VERSAO = "/v1"


class MiddlewareDeAuditoria(BaseHTTPMiddleware):
    """Grava uma linha de auditoria por escrita aceita sob `/v1`, sem que
    nenhuma rota — presente ou futura — declare nada (design.md —
    Decisions). Lê o contexto que `exigir_persona` e
    `exigir_chave_de_aplicacao` já gravaram em `request.state`; nunca
    recalcula sessão nem chave.
    """

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        resposta = await call_next(request)

        e_escrita = request.method in _METODOS_DE_ESCRITA
        e_sob_v1 = request.url.path.startswith(_PREFIXO_DE_VERSAO)
        if not e_escrita or not e_sob_v1 or resposta.status_code >= 400:
            return resposta

        contexto_da_sessao: ContextoDaSessao | None = getattr(
            request.state, "contexto_da_sessao", None
        )
        if contexto_da_sessao is None:
            return resposta

        contexto_da_chave: ContextoDaChave | None = getattr(
            request.state, "contexto_da_chave", None
        )

        rota = request.scope.get("route")
        nome_da_rota = rota.name if rota is not None else request.url.path
        acao = f"{request.method} {nome_da_rota}"

        self._gravar(
            autor_id=contexto_da_sessao.persona_id,
            papel_do_autor=contexto_da_sessao.papel.value,
            acao=acao,
            entidade_afetada=nome_da_rota,
            origem=contexto_da_chave.aplicacao if contexto_da_chave is not None else "",
        )
        return resposta

    def _gravar(self, **campos: object) -> None:
        """Best-effort (design.md — Risks): falha aqui vai só para o log —
        a resposta já pronta, que o cliente já recebe como sucesso, não
        espera pela auditoria nem é desfeita por ela.
        """
        try:
            fabrica = obter_fabrica_de_sessao()
            sessao = fabrica()
            try:
                sessao.add(Auditoria(**campos))
                sessao.commit()
            finally:
                sessao.close()
        except Exception:
            logger.exception("Falha ao gravar registro de auditoria: %s", campos.get("acao"))
