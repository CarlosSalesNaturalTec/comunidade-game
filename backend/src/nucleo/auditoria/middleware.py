import logging

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from ..autenticacao import ContextoDaSessao
from ..banco import obter_fabrica_de_sessao
from ..chaves.conferencia import ContextoDaChave
from .modelo import AcessoAoDadoDoGuerreiro, Auditoria

logger = logging.getLogger("nucleo.auditoria")

_METODOS_DE_ESCRITA = frozenset({"POST", "PUT", "PATCH", "DELETE"})
_PREFIXO_DE_VERSAO = "/v1"
_CHAVE_DO_GUERREIRO_NO_CORPO = "guerreiro_id"


def _guerreiro_ids_do_caminho(rota, path_params: dict) -> set[str]:
    """Todo segmento literal `guerreiros` seguido de um parâmetro de rota
    aponta um Guerreiro(a) alcançado — funciona para `{id}`, `{guerreiro_id}`
    ou qualquer outro nome, porque olha o padrão da URL, não o nome do
    parâmetro (`RF-13-30`, design — decisão 1)."""
    caminho = getattr(rota, "path", None)
    if not caminho:
        return set()

    segmentos = caminho.strip("/").split("/")
    encontrados: set[str] = set()
    for indice, segmento in enumerate(segmentos):
        if segmento != "guerreiros" or indice + 1 >= len(segmentos):
            continue
        proximo = segmentos[indice + 1]
        if proximo.startswith("{") and proximo.endswith("}"):
            nome_do_parametro = proximo[1:-1].split(":")[0]
            valor = path_params.get(nome_do_parametro)
            if valor is not None:
                encontrados.add(str(valor))
    return encontrados


def _guerreiro_ids_do_corpo(no: object, encontrados: set[str]) -> None:
    """Varre o corpo JSON já em cache — inclusive dentro de listas, para o
    lançamento em lote (`RF-13-30`, design — decisão 1)."""
    if isinstance(no, dict):
        for chave, valor in no.items():
            if chave == _CHAVE_DO_GUERREIRO_NO_CORPO and isinstance(valor, str):
                encontrados.add(valor)
            else:
                _guerreiro_ids_do_corpo(valor, encontrados)
    elif isinstance(no, list):
        for item in no:
            _guerreiro_ids_do_corpo(item, encontrados)


class MiddlewareDeAuditoria(BaseHTTPMiddleware):
    """Grava uma linha de auditoria por escrita aceita sob `/v1`, sem que
    nenhuma rota — presente ou futura — declare nada (design.md —
    Decisions). Lê o contexto que `exigir_persona` e
    `exigir_chave_de_aplicacao` já gravaram em `request.state`; nunca
    recalcula sessão nem chave. Também colhe, para a mesma linha, todo
    Guerreiro(a) que a escrita alcançou — dos `path_params` e do corpo
    JSON —, gravado em `acesso_ao_dado_do_guerreiro` (`RF-13-30`, design —
    decisão 1).
    """

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        e_escrita = request.method in _METODOS_DE_ESCRITA
        e_sob_v1 = request.url.path.startswith(_PREFIXO_DE_VERSAO)

        # Lê e cacheia o corpo ANTES de `call_next`, só quando pode conter
        # `guerreiro_id` — nunca em upload, que nunca é `application/json`
        # (design.md — Risks). O Starlette repassa o corpo já lido para a
        # rota downstream: nenhum handler perde o próprio `await
        # request.json()`.
        corpo_json: object | None = None
        if (
            e_escrita
            and e_sob_v1
            and request.headers.get("content-type", "").startswith("application/json")
        ):
            try:
                corpo_json = await request.json()
            except Exception:
                corpo_json = None

        resposta = await call_next(request)

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

        guerreiro_ids = _guerreiro_ids_do_caminho(rota, dict(request.path_params))
        if corpo_json is not None:
            _guerreiro_ids_do_corpo(corpo_json, guerreiro_ids)

        self._gravar(
            guerreiro_ids=guerreiro_ids,
            autor_id=contexto_da_sessao.persona_id,
            papel_do_autor=contexto_da_sessao.papel.value,
            acao=acao,
            entidade_afetada=nome_da_rota,
            origem=contexto_da_chave.aplicacao if contexto_da_chave is not None else "",
        )
        return resposta

    def _gravar(self, *, guerreiro_ids: set[str], **campos: object) -> None:
        """Best-effort (design.md — Risks): falha aqui vai só para o log —
        a resposta já pronta, que o cliente já recebe como sucesso, não
        espera pela auditoria nem é desfeita por ela.
        """
        try:
            fabrica = obter_fabrica_de_sessao()
            sessao = fabrica()
            try:
                registro = Auditoria(**campos)
                sessao.add(registro)
                sessao.flush()
                for guerreiro_id in guerreiro_ids:
                    sessao.add(
                        AcessoAoDadoDoGuerreiro(auditoria_id=registro.id, guerreiro_id=guerreiro_id)
                    )
                sessao.commit()
            finally:
                sessao.close()
        except Exception:
            logger.exception("Falha ao gravar registro de auditoria: %s", campos.get("acao"))
