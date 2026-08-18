import logging

from fastapi import APIRouter, Depends, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as ExcecaoHTTP

from .aportes.rotas import roteador as roteador_de_aportes
from .auditoria.middleware import MiddlewareDeAuditoria
from .auditoria.rotas import roteador as roteador_de_auditoria
from .aulas.rotas import roteador as roteador_de_aulas
from .biometria.rotas import roteador as roteador_de_biometria
from .chaves.conferencia import exigir_chave_de_aplicacao
from .chaves.rotas import roteador as roteador_de_chaves
from .coletas.rotas import roteador as roteador_de_coletas
from .comunidades.rotas import roteador as roteador_de_comunidades
from .erros import CorpoDeErro, ErroDeAplicacao, ErroInterno
from .fila.rotas import roteador as roteador_de_fila
from .jogos.rotas import roteador as roteador_de_jogos
from .livro_razao.rotas import roteador as roteador_de_livro_razao
from .locais.rotas import roteador as roteador_de_locais
from .personas.rotas import roteador as roteador_de_personas
from .pontos_de_apoio.rotas import roteador as roteador_de_pontos_de_apoio
from .protecao import registrar_premissa_de_conteiner_unico
from .protecao.cota import exigir_cota_de_leitura
from .recursos.rotas import roteador as roteador_de_recursos
from .responsaveis.rotas import roteador as roteador_de_responsaveis
from .sessoes.rotas import roteador as roteador_de_sessoes
from .vitrine.rotas import roteador as roteador_de_vitrine

logger = logging.getLogger("nucleo")

_LOCAIS_GENERICOS = {"body", "query", "path", "header", "cookie"}


def _resposta_de_erro(
    status_code: int, codigo: str, mensagem: str, campo: str | None = None
) -> JSONResponse:
    corpo = CorpoDeErro(codigo=codigo, mensagem=mensagem, campo=campo)
    return JSONResponse(status_code=status_code, content=corpo.model_dump(exclude_none=True))


async def _manipular_erro_de_aplicacao(request: Request, exc: ErroDeAplicacao) -> JSONResponse:
    resposta = _resposta_de_erro(exc.status_code, exc.codigo, exc.mensagem, exc.campo)
    tempo_de_espera = getattr(exc, "tempo_de_espera_em_segundos", None)
    if tempo_de_espera is not None:
        resposta.headers["Retry-After"] = str(tempo_de_espera)
    return resposta


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

    # Transversal a toda a aplicação (RF-01-29): nenhuma rota, presente ou
    # futura, precisa declarar nada para entrar na trilha de auditoria.
    app.add_middleware(MiddlewareDeAuditoria)

    registrar_premissa_de_conteiner_unico()

    return app


def incluir_roteador_de_dados(app: FastAPI, roteador: APIRouter) -> None:
    """Inclui um roteador de domínio sob `/v1`, com a chave de aplicação e a
    cota de leitura por faixa dela exigidas em toda rota (`RF-01-01`,
    `RN-01-32`, `RF-01-55`). A cota vem depois da chave, para que chave
    inválida receba 401 antes de a cota contar qualquer coisa (design —
    Decisions). É o que permite às fatias seguintes do PRD-01 estender o
    núcleo sem refazer nenhuma das duas — `/docs` e `/openapi.json` ficam
    fora, porque nunca passam por aqui.
    """
    app.include_router(
        roteador,
        prefix="/v1",
        dependencies=[Depends(exigir_chave_de_aplicacao), Depends(exigir_cota_de_leitura)],
    )


app = criar_app()
incluir_roteador_de_dados(app, roteador_de_personas)
incluir_roteador_de_dados(app, roteador_de_sessoes)
incluir_roteador_de_dados(app, roteador_de_responsaveis)
incluir_roteador_de_dados(app, roteador_de_biometria)
incluir_roteador_de_dados(app, roteador_de_auditoria)
incluir_roteador_de_dados(app, roteador_de_fila)
incluir_roteador_de_dados(app, roteador_de_chaves)
incluir_roteador_de_dados(app, roteador_de_vitrine)
incluir_roteador_de_dados(app, roteador_de_jogos)
incluir_roteador_de_dados(app, roteador_de_comunidades)
incluir_roteador_de_dados(app, roteador_de_locais)
incluir_roteador_de_dados(app, roteador_de_coletas)
incluir_roteador_de_dados(app, roteador_de_pontos_de_apoio)
incluir_roteador_de_dados(app, roteador_de_recursos)
incluir_roteador_de_dados(app, roteador_de_livro_razao)
incluir_roteador_de_dados(app, roteador_de_aportes)
incluir_roteador_de_dados(app, roteador_de_aulas)
