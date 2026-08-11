import os
from typing import Annotated

import pytest
from fastapi import APIRouter, Depends
from fastapi.testclient import TestClient
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from nucleo.autenticacao import exigir_persona
from nucleo.banco import Base, obter_sessao
from nucleo.chaves.conferencia import ContextoDaChave, exigir_chave_de_aplicacao
from nucleo.chaves.modelo import ChaveDeAplicacao, NaturezaDaChave, SituacaoDaChave
from nucleo.chaves.segredo import calcular_resumo, gerar_segredo, montar_chave_completa
from nucleo.configuracao import Configuracao, obter_configuracao
from nucleo.paginacao import PaginaDeResultado, ParametrosDeListagem, contrato_de_listagem
from nucleo.principal import criar_app, incluir_roteador_de_dados
from nucleo.tempo import DataHoraComFuso

DSN_DE_TESTE = os.environ.get(
    "CG_DSN_BANCO_TESTE",
    "postgresql+psycopg://comunidade:comunidade@localhost:5432/comunidade_game_teste",
)


@pytest.fixture(scope="session")
def engine():
    motor = create_engine(DSN_DE_TESTE)
    Base.metadata.create_all(motor)
    yield motor
    Base.metadata.drop_all(motor)
    motor.dispose()


@pytest.fixture
def sessao(engine):
    fabrica = sessionmaker(bind=engine, expire_on_commit=False)
    sessao = fabrica()
    yield sessao
    sessao.rollback()
    for tabela in reversed(Base.metadata.sorted_tables):
        sessao.execute(tabela.delete())
    sessao.commit()
    sessao.close()


@pytest.fixture
def configuracao():
    return Configuracao(ambiente="desenvolvimento", dsn_banco=DSN_DE_TESTE)


def _montar_roteador_de_teste() -> APIRouter:
    """Rotas de exercício: nenhuma fatia de domínio existe ainda nesta change —
    o contrato de `/v1` é testado aqui, sem entrar no app de produção."""
    roteador = APIRouter()

    @roteador.get("/publica")
    def publica(contexto: Annotated[ContextoDaChave, Depends(exigir_chave_de_aplicacao)]):
        return {"aplicacao": contexto.aplicacao, "ambiente": contexto.ambiente}

    @roteador.get("/autenticada", dependencies=[Depends(exigir_persona)])
    def autenticada():
        return {"ok": True}

    @roteador.get("/itens", response_model=PaginaDeResultado[str])
    def itens(
        parametros: Annotated[
            ParametrosDeListagem, Depends(contrato_de_listagem(frozenset({"cor"})))
        ],
    ):
        return PaginaDeResultado(itens=list(parametros.filtros.values()), proximo_cursor=None)

    class EventoEntrada(BaseModel):
        momento_do_fato: DataHoraComFuso

    @roteador.post("/eventos")
    def eventos(entrada: EventoEntrada):
        return {"momento_do_fato": entrada.momento_do_fato.isoformat()}

    @roteador.get("/quebra")
    def quebra():
        raise RuntimeError("falha proposital de teste")

    return roteador


@pytest.fixture
def app(sessao, configuracao):
    aplicacao = criar_app()
    aplicacao.dependency_overrides[obter_sessao] = lambda: sessao
    aplicacao.dependency_overrides[obter_configuracao] = lambda: configuracao
    incluir_roteador_de_dados(aplicacao, _montar_roteador_de_teste())
    return aplicacao


@pytest.fixture
def cliente(app):
    return TestClient(app, raise_server_exceptions=False)


@pytest.fixture
def criar_chave(sessao):
    """Emite uma chave vigente pronta para uso e devolve (chave_completa, registro)."""

    def _criar(
        aplicacao: str = "app-06-vitrine",
        ambiente: str = "desenvolvimento",
        situacao: SituacaoDaChave = SituacaoDaChave.vigente,
        natureza: NaturezaDaChave = NaturezaDaChave.do_projeto,
    ) -> tuple[str, ChaveDeAplicacao]:
        segredo = gerar_segredo()
        registro = ChaveDeAplicacao(
            aplicacao=aplicacao,
            ambiente=ambiente,
            natureza=natureza,
            resumo_do_segredo=calcular_resumo(segredo),
            situacao=situacao,
        )
        sessao.add(registro)
        sessao.commit()
        sessao.refresh(registro)
        chave_completa = montar_chave_completa(ambiente, str(registro.id), segredo)
        return chave_completa, registro

    return _criar
