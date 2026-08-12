import logging

from fastapi import APIRouter, Depends, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as ExcecaoHTTP

from .chaves.conferencia import exigir_chave_de_aplicacao
from .erros import CorpoDeErro, ErroDeAplicacao, ErroInterno
from .personas.rotas import roteador as roteador_de_personas
from .sessoes.rotas import roteador as roteador_de_sessoes

logger = logging.getLogger("nucleo")

_LOCAIS_GENERICOS = {"body", "query", "path", "header", "cookie"}


def _resposta_de_erro(
    status_code: int, codigo: str, mensagem: str, campo: str | None = None
) -> JSONResponse:
    corpo = CorpoDeErro(codigo=codigo, mensagem=mensagem, campo=campo)
    return JSONResponse(status_code=status_code, content=corpo.model_dump(exclude_none=True))


async def _manipular_erro_de_aplicacao(request: Request, exc: ErroDeAplicacao) -> JSONResponse:
    return _resposta_de_erro(exc.status_code, exc.codigo, exc.mensagem, exc.campo)


async def _manipular_erro_de_validacao(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    primeiro = exc.errors()[0]
    partes = [str(parte) for parte in primeiro["loc"] if str(parte) not in _LOCAIS_GENERICOS]
    campo = ".".join(partes) or None
    return _resposta_de_erro(422, "erro_de_validacao", primeiro["msg"], campo)


async def _manipular_http_exception(request: Request, exc: ExcecaoHTTP) -> JSONResponse:
    codigo = "nao_encontrado" if exc.status_code == 404 else "erro_http"
    mensagem = exc.detail if isinstance(exc.detail, str) else "Erro ao processar a chamada."
    return _resposta_de_erro(exc.status_code, codigo, mensagem)


async def _manipular_excecao_nao_tratada(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Falha não tratada em %s %s", request.method, request.url.path)
    erro = ErroInterno()
    return _resposta_de_erro(erro.status_code, erro.codigo, erro.mensagem)


def criar_app() -> FastAPI:
    app = FastAPI(
        title="Comunidade Game — Backend API",
        description=(
            "Núcleo consumido pelas oito aplicações do Comunidade Game e por "
            "aplicações de terceiros, sempre mediante chave de aplicação."
        ),
    )

    app.add_exception_handler(ErroDeAplicacao, _manipular_erro_de_aplicacao)
    app.add_exception_handler(RequestValidationError, _manipular_erro_de_validacao)
    app.add_exception_handler(ExcecaoHTTP, _manipular_http_exception)
    app.add_exception_handler(Exception, _manipular_excecao_nao_tratada)

    return app


def incluir_roteador_de_dados(app: FastAPI, roteador: APIRouter) -> None:
    """Inclui um roteador de domínio sob `/v1`, com a chave de aplicação exigida
    em toda rota dele (`RF-01-01`, `RN-01-32`). É o que permite às fatias
    seguintes do PRD-01 estender o núcleo sem refazer a exigência da chave —
    `/docs` e `/openapi.json` ficam fora, porque nunca passam por aqui.
    """
    app.include_router(roteador, prefix="/v1", dependencies=[Depends(exigir_chave_de_aplicacao)])


app = criar_app()
incluir_roteador_de_dados(app, roteador_de_personas)
incluir_roteador_de_dados(app, roteador_de_sessoes)
