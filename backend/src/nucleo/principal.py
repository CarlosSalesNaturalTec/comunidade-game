import logging

from fastapi import APIRouter, Depends, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as ExcecaoHTTP

from .aportes.rotas import roteador as roteador_de_aportes
from .armazenamento.rotas import roteador as roteador_de_armazenamento
from .atividades.rotas import roteador as roteador_de_atividades
from .auditoria.middleware import MiddlewareDeAuditoria
from .auditoria.rotas import roteador as roteador_de_auditoria
from .aulas.rotas import roteador as roteador_de_aulas
from .autenticacao import NOME_DO_CABECALHO_DE_SESSAO
from .bibliografias.rotas import roteador as roteador_de_bibliografias
from .biometria.rotas import roteador as roteador_de_biometria
from .catalogo_avulso.rotas import roteador as roteador_de_catalogo_avulso
from .chaves.conferencia import NOME_DO_CABECALHO as NOME_DO_CABECALHO_DA_CHAVE
from .chaves.conferencia import exigir_chave_de_aplicacao
from .chaves.rotas import roteador as roteador_de_chaves
from .ciclo.rotas import roteador as roteador_de_ciclo
from .coletas.rotas import roteador as roteador_de_coletas
from .comunidades.rotas import roteador as roteador_de_comunidades
from .consentimentos.rotas import roteador as roteador_de_consentimentos
from .conteudos.rotas import roteador as roteador_de_conteudos
from .criacoes_originais.rotas import roteador as roteador_de_criacoes_originais
from .culminancias.rotas import roteador as roteador_de_culminancias
from .equipes.rotas import roteador as roteador_de_equipes
from .erros import CorpoDeErro, ErroDeAplicacao, ErroInterno
from .fila.rotas import roteador as roteador_de_fila
from .jogos.rotas import roteador as roteador_de_jogos
from .livro_razao.rotas import roteador as roteador_de_livro_razao
from .locais.rotas import roteador as roteador_de_locais
from .necessidades.rotas import roteador as roteador_de_necessidades
from .ocorrencias_de_conduta.rotas import roteador as roteador_de_ocorrencias_de_conduta
from .ods.rotas import roteador as roteador_de_ods
from .painel_do_dia.rotas import roteador as roteador_de_painel_do_dia
from .patrimonio.rotas import roteador as roteador_de_patrimonio
from .personas.rotas import roteador as roteador_de_personas
from .poder_sustentador.rotas import roteador as roteador_de_poder_sustentador
from .poderes.rotas import roteador as roteador_de_poderes
from .ponto_extra.rotas import roteador as roteador_de_ponto_extra
from .pontos_de_apoio.rotas import roteador as roteador_de_pontos_de_apoio
from .pontuacao.rotas import roteador as roteador_de_pontuacao
from .prestacao_de_contas.rotas import roteador as roteador_de_prestacao_de_contas
from .protecao import registrar_premissa_de_conteiner_unico
from .protecao.cota import exigir_cota_de_leitura
from .quiz.rotas import roteador as roteador_de_quiz
from .recompensas_de_marco.rotas import roteador as roteador_de_recompensas_de_marco
from .recursos.rotas import roteador as roteador_de_recursos
from .responsaveis.rotas import roteador as roteador_de_responsaveis
from .ressarcimentos.rotas import roteador as roteador_de_ressarcimentos
from .resultados.rotas import roteador as roteador_de_resultados
from .sessoes.rotas import roteador as roteador_de_sessoes
from .trilhas.rotas import roteador as roteador_de_trilhas
from .trocas.rotas import roteador as roteador_de_trocas
from .vitrine.rotas import roteador as roteador_de_vitrine

logger = logging.getLogger("nucleo")

_LOCAIS_GENERICOS = {"body", "query", "path", "header", "cookie"}


def _resposta_de_erro(
    status_code: int,
    codigo: str,
    mensagem: str,
    campo: str | None = None,
    sugestoes: list[str] | None = None,
) -> JSONResponse:
    corpo = CorpoDeErro(codigo=codigo, mensagem=mensagem, campo=campo, sugestoes=sugestoes)
    return JSONResponse(status_code=status_code, content=corpo.model_dump(exclude_none=True))


async def _manipular_erro_de_aplicacao(request: Request, exc: ErroDeAplicacao) -> JSONResponse:
    resposta = _resposta_de_erro(
        exc.status_code, exc.codigo, exc.mensagem, exc.campo, getattr(exc, "sugestoes", None)
    )
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

    # Origem aberta, sem cookie credenciado (documento 03 §1, princípio 2):
    # a proteção está nas duas credenciais de cabeçalho, não no navegador.
    # Adicionado por último para ficar por fora de tudo, inclusive da
    # auditoria, e assim responder ao preflight antes de qualquer rota.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["GET", "POST", "PATCH", "PUT", "DELETE"],
        allow_headers=[NOME_DO_CABECALHO_DA_CHAVE, NOME_DO_CABECALHO_DE_SESSAO, "Content-Type"],
    )

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
incluir_roteador_de_dados(app, roteador_de_necessidades)
incluir_roteador_de_dados(app, roteador_de_poder_sustentador)
incluir_roteador_de_dados(app, roteador_de_poderes)
incluir_roteador_de_dados(app, roteador_de_prestacao_de_contas)
incluir_roteador_de_dados(app, roteador_de_ressarcimentos)
incluir_roteador_de_dados(app, roteador_de_catalogo_avulso)
incluir_roteador_de_dados(app, roteador_de_trocas)
incluir_roteador_de_dados(app, roteador_de_patrimonio)
incluir_roteador_de_dados(app, roteador_de_recompensas_de_marco)
incluir_roteador_de_dados(app, roteador_de_trilhas)
incluir_roteador_de_dados(app, roteador_de_atividades)
incluir_roteador_de_dados(app, roteador_de_culminancias)
incluir_roteador_de_dados(app, roteador_de_criacoes_originais)
incluir_roteador_de_dados(app, roteador_de_ods)
incluir_roteador_de_dados(app, roteador_de_resultados)
incluir_roteador_de_dados(app, roteador_de_ocorrencias_de_conduta)
incluir_roteador_de_dados(app, roteador_de_quiz)
incluir_roteador_de_dados(app, roteador_de_equipes)
incluir_roteador_de_dados(app, roteador_de_consentimentos)
incluir_roteador_de_dados(app, roteador_de_ponto_extra)
incluir_roteador_de_dados(app, roteador_de_conteudos)
incluir_roteador_de_dados(app, roteador_de_bibliografias)
incluir_roteador_de_dados(app, roteador_de_painel_do_dia)
incluir_roteador_de_dados(app, roteador_de_ciclo)
incluir_roteador_de_dados(app, roteador_de_pontuacao)
# A rota local do protocolo `Content-Range` (`armazenamento.rotas`) só
# conclui algo com o adaptador de disco — em produção, a dependência
# devolve o Cloud Storage e o manipulador responde 404 (`RF-09-19`, design
# — decisão 2).
incluir_roteador_de_dados(app, roteador_de_armazenamento)
