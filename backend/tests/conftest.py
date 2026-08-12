import os
from datetime import UTC, datetime, timedelta
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
from nucleo.personas.modelo import ComunidadeVirtual, Credencial, Papel, Persona, TipoDeCredencial
from nucleo.personas.senha import calcular_hash
from nucleo.principal import criar_app, incluir_roteador_de_dados
from nucleo.sessoes.modelo import ComoAutenticou, Sessao
from nucleo.sessoes.token import calcular_resumo as calcular_resumo_do_token
from nucleo.sessoes.token import gerar_token
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
    return Configuracao(
        ambiente="desenvolvimento",
        dsn_banco=DSN_DE_TESTE,
        identidade_fundador="fundador-de-teste@example.org",
        sessao_adulto_duracao=timedelta(hours=8),
        argon2_memoria_kib=8,
        argon2_iteracoes=1,
        argon2_paralelismo=1,
    )


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

    @roteador.get("/itens-de-comunidade", response_model=PaginaDeResultado[str])
    def itens_de_comunidade(
        parametros: Annotated[
            ParametrosDeListagem,
            Depends(contrato_de_listagem(filtro_comunidade_obrigatorio=True)),
        ],
    ):
        return PaginaDeResultado(itens=[parametros.filtros["comunidade"]], proximo_cursor=None)

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
    from nucleo.personas.rotas import roteador as roteador_de_personas
    from nucleo.sessoes.rotas import roteador as roteador_de_sessoes

    aplicacao = criar_app()
    aplicacao.dependency_overrides[obter_sessao] = lambda: sessao
    aplicacao.dependency_overrides[obter_configuracao] = lambda: configuracao
    incluir_roteador_de_dados(aplicacao, _montar_roteador_de_teste())
    incluir_roteador_de_dados(aplicacao, roteador_de_personas)
    incluir_roteador_de_dados(aplicacao, roteador_de_sessoes)
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


@pytest.fixture
def criar_comunidade(sessao):
    def _criar(nome: str = "Comunidade de Teste") -> ComunidadeVirtual:
        comunidade = ComunidadeVirtual(
            nome=nome,
            localizacao="Bairro de teste",
            granularidade_maxima="bairro",
        )
        sessao.add(comunidade)
        sessao.commit()
        sessao.refresh(comunidade)
        return comunidade

    return _criar


@pytest.fixture
def criar_persona(sessao, criar_comunidade):
    def _criar(
        papel: Papel = Papel.admin,
        criada_por: Persona | None = None,
        comunidade: ComunidadeVirtual | None = None,
    ) -> Persona:
        if papel == Papel.guerreiro and comunidade is None:
            comunidade = criar_comunidade()
        persona = Persona(
            papel=papel,
            comunidade_virtual_id=comunidade.id if comunidade is not None else None,
            criada_por=criada_por.id if criada_por is not None else None,
        )
        sessao.add(persona)
        sessao.commit()
        sessao.refresh(persona)
        return persona

    return _criar


@pytest.fixture
def criar_credencial(sessao, configuracao):
    def _criar(
        persona: Persona,
        tipo: TipoDeCredencial = TipoDeCredencial.login_social,
        identificador: str = "adulto-de-teste@example.org",
        senha: str | None = None,
        troca_pendente: bool = False,
        criada_por: Persona | None = None,
        ativa: bool = True,
    ) -> Credencial:
        credencial = Credencial(
            persona_id=persona.id,
            tipo=tipo,
            identificador=identificador,
            segredo=calcular_hash(senha, configuracao) if senha is not None else None,
            criada_por=criada_por.id if criada_por is not None else None,
            troca_pendente=troca_pendente,
            ativa=ativa,
        )
        sessao.add(credencial)
        sessao.commit()
        sessao.refresh(credencial)
        return credencial

    return _criar


@pytest.fixture
def criar_sessao_de_teste(sessao):
    def _criar(
        persona: Persona,
        origem: str = "app-03-gestao",
        como_autenticou: ComoAutenticou = ComoAutenticou.social,
        expira_em: datetime | None = None,
        encerrada_em: datetime | None = None,
    ) -> tuple[str, Sessao]:
        token = gerar_token()
        registro = Sessao(
            persona_id=persona.id,
            resumo_do_token=calcular_resumo_do_token(token),
            expira_em=expira_em or (datetime.now(UTC) + timedelta(hours=1)),
            origem=origem,
            como_autenticou=como_autenticou,
            encerrada_em=encerrada_em,
        )
        sessao.add(registro)
        sessao.commit()
        sessao.refresh(registro)
        return token, registro

    return _criar
