import base64
import os
import uuid
from datetime import UTC, datetime, timedelta
from typing import Annotated

import pytest
from fastapi import APIRouter, Depends
from fastapi.testclient import TestClient
from pydantic import BaseModel
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from nucleo.auditoria.modelo import Auditoria
from nucleo.aulas.modelo import Aula
from nucleo.autenticacao import exigir_persona
from nucleo.banco import Base, obter_sessao
from nucleo.biometria.cifra import cifrar_descritor
from nucleo.chaves.conferencia import ContextoDaChave, exigir_chave_de_aplicacao
from nucleo.chaves.modelo import ChaveDeAplicacao, NaturezaDaChave, SituacaoDaChave
from nucleo.chaves.segredo import calcular_resumo, gerar_segredo, montar_chave_completa
from nucleo.configuracao import Configuracao, obter_configuracao
from nucleo.consentimentos.modelo import (
    Consentimento,
    DecisaoDeConsentimento,
    OrigemDoConsentimento,
    TipoDeConsentimento,
)
from nucleo.equipes.modelo import Equipe, IntegranteDaEquipe
from nucleo.fila.modelo import SituacaoDaSolicitacao, SolicitacaoDeChave
from nucleo.fila.regra import avaliar_solicitacao_de_chave, registrar_solicitacao_de_chave
from nucleo.paginacao import PaginaDeResultado, ParametrosDeListagem, contrato_de_listagem
from nucleo.personas.modelo import (
    ComunidadeVirtual,
    Credencial,
    Nick,
    Papel,
    Persona,
    TipoDeCredencial,
)
from nucleo.personas.senha import calcular_hash
from nucleo.poderes.modelo import NaturezaDoPoder, Poder, VigenciaDoPoder
from nucleo.ponto_extra.modelo import PontoExtra
from nucleo.pontuacao.modelo import Badge, Nivel, PontoRegular, TipoDeBadge
from nucleo.principal import criar_app, incluir_roteador_de_dados
from nucleo.protecao.freio import exigir_freio_por_origem
from nucleo.responsaveis.modelo import VinculoResponsavel
from nucleo.sessoes.modelo import ComoAutenticou, Sessao
from nucleo.sessoes.token import calcular_resumo as calcular_resumo_do_token
from nucleo.sessoes.token import gerar_token
from nucleo.tempo import DataHoraComFuso
from nucleo.trilhas.modelo import (
    Atividade,
    FormatoDeAtividade,
    Missao,
    ModalidadeDeAtividade,
    SituacaoDaTrilha,
    Trilha,
)

DSN_DE_TESTE = os.environ.get(
    "CG_DSN_BANCO_TESTE",
    "postgresql+psycopg://comunidade:comunidade@localhost:5432/comunidade_game_teste",
)

# Dimensão pequena para os testes ficarem legíveis; chave fixa para que a
# cifra e a decifra sejam determinísticas dentro da suíte.
DIMENSAO_DE_TESTE_DO_DESCRITOR = 4
CHAVE_DE_CIFRAGEM_DE_TESTE = base64.urlsafe_b64encode(b"0" * 32).decode()


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
    # `TRUNCATE`, ao contrário de `DELETE`, não dispara o trigger de linha que
    # recusa remoção em `consentimento` (RN-01-12) — é o que permite limpar o
    # banco entre testes sem violar a imutabilidade que a própria fatia exige.
    nomes_das_tabelas = ", ".join(f'"{tabela.name}"' for tabela in Base.metadata.sorted_tables)
    sessao.execute(text(f"TRUNCATE TABLE {nomes_das_tabelas} RESTART IDENTITY CASCADE"))
    sessao.commit()
    sessao.close()


@pytest.fixture
def configuracao(tmp_path):
    return Configuracao(
        ambiente="desenvolvimento",
        dsn_banco=DSN_DE_TESTE,
        identidade_fundador="fundador-de-teste@example.org",
        sessao_adulto_duracao=timedelta(hours=8),
        sessao_guerreiro_duracao=timedelta(hours=4),
        biometria_dimensao_do_descritor=DIMENSAO_DE_TESTE_DO_DESCRITOR,
        biometria_limiar_de_comparacao=0.5,
        biometria_chave_de_cifragem=CHAVE_DE_CIFRAGEM_DE_TESTE,
        argon2_memoria_kib=8,
        argon2_iteracoes=1,
        argon2_paralelismo=1,
        armazenamento_diretorio_local=str(tmp_path / "armazenamento"),
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

    @roteador.post(
        "/formulario-participacao",
        dependencies=[Depends(exigir_freio_por_origem("formulario_participacao"))],
    )
    def formulario_participacao():
        return {"ok": True}

    @roteador.post(
        "/formulario-dados",
        dependencies=[Depends(exigir_freio_por_origem("formulario_dados"))],
    )
    def formulario_dados():
        return {"ok": True}

    return roteador


@pytest.fixture
def app(sessao, configuracao):
    from nucleo.auditoria.rotas import roteador as roteador_de_auditoria
    from nucleo.biometria.rotas import roteador as roteador_de_biometria
    from nucleo.chaves.rotas import roteador as roteador_de_chaves
    from nucleo.fila.rotas import roteador as roteador_de_fila
    from nucleo.jogos.rotas import roteador as roteador_de_jogos
    from nucleo.personas.rotas import roteador as roteador_de_personas
    from nucleo.responsaveis.rotas import roteador as roteador_de_responsaveis
    from nucleo.sessoes.rotas import roteador as roteador_de_sessoes
    from nucleo.vitrine.rotas import roteador as roteador_de_vitrine

    aplicacao = criar_app()
    aplicacao.dependency_overrides[obter_sessao] = lambda: sessao
    aplicacao.dependency_overrides[obter_configuracao] = lambda: configuracao
    incluir_roteador_de_dados(aplicacao, _montar_roteador_de_teste())
    incluir_roteador_de_dados(aplicacao, roteador_de_personas)
    incluir_roteador_de_dados(aplicacao, roteador_de_sessoes)
    incluir_roteador_de_dados(aplicacao, roteador_de_responsaveis)
    incluir_roteador_de_dados(aplicacao, roteador_de_biometria)
    incluir_roteador_de_dados(aplicacao, roteador_de_auditoria)
    incluir_roteador_de_dados(aplicacao, roteador_de_fila)
    incluir_roteador_de_dados(aplicacao, roteador_de_chaves)
    incluir_roteador_de_dados(aplicacao, roteador_de_vitrine)
    incluir_roteador_de_dados(aplicacao, roteador_de_jogos)
    return aplicacao


@pytest.fixture
def cliente(app):
    return TestClient(app, raise_server_exceptions=False)


@pytest.fixture
def cliente_com_origem(app):
    """Um `TestClient` por origem simulada — o freio por origem agrupa por
    endereço de rede (`RN-01-45`), e testes precisam de origens distintas
    para provar que uma não compartilha o freio da outra."""

    def _criar(endereco: str = "203.0.113.10") -> TestClient:
        return TestClient(app, client=(endereco, 12345), raise_server_exceptions=False)

    return _criar


@pytest.fixture
def sobrescrever_configuracao(app, configuracao):
    """Troca a `Configuracao` injetada nas rotas de teste por uma cópia com
    os campos indicados alterados, sem tocar nos demais — usado para testar
    a cota e o freio com números pequenos, em vez de esperar o padrão do
    documento 03 §8 se esgotar de verdade."""

    def _sobrescrever(**mudancas) -> Configuracao:
        nova = configuracao.model_copy(update=mudancas)
        app.dependency_overrides[obter_configuracao] = lambda: nova
        return nova

    return _sobrescrever


@pytest.fixture
def criar_chave(sessao):
    """Emite uma chave vigente pronta para uso e devolve (chave_completa, registro)."""

    def _criar(
        aplicacao: str = "app-06-vitrine",
        ambiente: str = "desenvolvimento",
        situacao: SituacaoDaChave = SituacaoDaChave.vigente,
        natureza: NaturezaDaChave = NaturezaDaChave.do_projeto,
        prazo_de_apresentacao: datetime | None = None,
        url_apresentada: str | None = None,
        solicitacao_de_chave_id: uuid.UUID | None = None,
    ) -> tuple[str, ChaveDeAplicacao]:
        segredo = gerar_segredo()
        registro = ChaveDeAplicacao(
            aplicacao=aplicacao,
            ambiente=ambiente,
            natureza=natureza,
            resumo_do_segredo=calcular_resumo(segredo),
            situacao=situacao,
            prazo_de_apresentacao=prazo_de_apresentacao,
            url_apresentada=url_apresentada,
            solicitacao_de_chave_id=solicitacao_de_chave_id,
        )
        sessao.add(registro)
        sessao.commit()
        sessao.refresh(registro)
        chave_completa = montar_chave_completa(ambiente, str(registro.id), segredo)
        return chave_completa, registro

    return _criar


@pytest.fixture
def criar_solicitacao_de_chave(sessao, criar_persona):
    """Registra uma solicitação de chave e, por padrão, já a aprova — o
    estado de que a emissão (`RF-01-50`) precisa partir."""

    def _criar(
        situacao: SituacaoDaSolicitacao = SituacaoDaSolicitacao.aceita,
        solicitante: str = "Desenvolvedora de Tal",
        avaliado_por: Persona | None = None,
    ) -> SolicitacaoDeChave:
        solicitacao = registrar_solicitacao_de_chave(
            sessao,
            solicitante=solicitante,
            contato="dev@example.org",
            o_que_pretende_construir="Um painel comunitário.",
        )
        sessao.commit()

        if situacao in (SituacaoDaSolicitacao.aceita, SituacaoDaSolicitacao.recusada):
            admin = avaliado_por or criar_persona(Papel.admin)
            avaliar_solicitacao_de_chave(
                sessao, solicitacao, situacao=situacao, avaliado_por=admin, parecer="Aprovado."
            )
            sessao.commit()
        elif situacao == SituacaoDaSolicitacao.em_avaliacao:
            solicitacao.situacao = situacao
            sessao.commit()

        return solicitacao

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
        avatar: str | None = None,
    ) -> Persona:
        if papel == Papel.guerreiro and comunidade is None:
            comunidade = criar_comunidade()
        persona = Persona(
            papel=papel,
            comunidade_virtual_id=comunidade.id if comunidade is not None else None,
            criada_por=criada_por.id if criada_por is not None else None,
            avatar=avatar,
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


@pytest.fixture
def criar_vinculo(sessao):
    def _criar(
        responsavel: Persona,
        guerreiro: Persona,
        grau_de_parentesco: str = "mãe",
        cadastrado_por: Persona | None = None,
        fim: datetime | None = None,
    ) -> VinculoResponsavel:
        autor = cadastrado_por or responsavel
        vinculo = VinculoResponsavel(
            responsavel_id=responsavel.id,
            guerreiro_id=guerreiro.id,
            grau_de_parentesco=grau_de_parentesco,
            fim=fim,
            autor_id=autor.id,
            papel_do_autor=autor.papel.value,
        )
        sessao.add(vinculo)
        sessao.commit()
        sessao.refresh(vinculo)
        return vinculo

    return _criar


@pytest.fixture
def criar_consentimento(sessao):
    def _criar(
        responsavel: Persona,
        guerreiro: Persona,
        tipo: TipoDeConsentimento | str = TipoDeConsentimento.autorizacao_de_divulgacao,
        versao_do_termo: str = "1.0",
        decisao: DecisaoDeConsentimento = DecisaoDeConsentimento.concede,
        origem: OrigemDoConsentimento = OrigemDoConsentimento.propria,
        operado_por: Persona | None = None,
        testemunha: Persona | None = None,
        anexo: str | None = None,
    ) -> Consentimento:
        autor = operado_por or responsavel
        consentimento = Consentimento(
            responsavel_id=responsavel.id,
            guerreiro_id=guerreiro.id,
            tipo=tipo,
            versao_do_termo=versao_do_termo,
            decisao=decisao,
            origem=origem,
            testemunha_id=testemunha.id if testemunha is not None else None,
            anexo=anexo,
            autor_id=autor.id,
            papel_do_autor=autor.papel.value,
        )
        sessao.add(consentimento)
        sessao.commit()
        sessao.refresh(consentimento)
        return consentimento

    return _criar


@pytest.fixture
def criar_nick(sessao):
    def _criar(persona: Persona, valor: str) -> Nick:
        registro = Nick(persona_id=persona.id, valor=valor)
        sessao.add(registro)
        sessao.commit()
        sessao.refresh(registro)
        return registro

    return _criar


@pytest.fixture
def conceder_consentimento_biometrico(criar_consentimento):
    """Atalho para o consentimento que `RN-01-17` exige antes da gravação do
    _template_ — mesma `tipo` que `nucleo.biometria.regra` usa na consulta."""

    def _conceder(responsavel: Persona, guerreiro: Persona, **kwargs) -> Consentimento:
        from nucleo.biometria.regra import TIPO_DE_CONSENTIMENTO_BIOMETRIA

        kwargs.setdefault("decisao", DecisaoDeConsentimento.concede)
        return criar_consentimento(
            responsavel, guerreiro, tipo=TIPO_DE_CONSENTIMENTO_BIOMETRIA, **kwargs
        )

    return _conceder


@pytest.fixture
def criar_poder(sessao):
    def _criar(
        autor: Persona,
        nome: str = "Poder de Teste",
        descricao: str = "Descrição de teste.",
        natureza: NaturezaDoPoder = NaturezaDoPoder.de_guerreiro,
        vigencia: VigenciaDoPoder = VigenciaDoPoder.vigente,
        ativo: bool = True,
    ) -> Poder:
        poder = Poder(
            nome=nome,
            descricao=descricao,
            natureza=natureza,
            vigencia=vigencia,
            ativo=ativo,
            autor_id=autor.id,
            papel_do_autor=autor.papel.value,
        )
        sessao.add(poder)
        sessao.commit()
        sessao.refresh(poder)
        return poder

    return _criar


@pytest.fixture
def criar_trilha(sessao, criar_poder):
    def _criar(
        autor: Persona,
        poder: Poder | None = None,
        nome: str = "Trilha de Teste",
        objetivo: str = "Objetivo de teste.",
        area_do_conhecimento: str = "Tecnologia",
        situacao: SituacaoDaTrilha = SituacaoDaTrilha.rascunho,
    ) -> Trilha:
        poder_da_trilha = poder or criar_poder(autor)
        trilha = Trilha(
            nome=nome,
            objetivo=objetivo,
            area_do_conhecimento=area_do_conhecimento,
            poder_id=poder_da_trilha.id,
            situacao=situacao,
            autor_id=autor.id,
            papel_do_autor=autor.papel.value,
        )
        sessao.add(trilha)
        sessao.commit()
        sessao.refresh(trilha)
        return trilha

    return _criar


@pytest.fixture
def criar_missao(sessao):
    def _criar(
        trilha: Trilha,
        autor: Persona,
        posicao: int = 1,
        nivel_de_dificuldade: int = 1,
        obrigatoria: bool = True,
        e_sondagem: bool = False,
    ) -> Missao:
        missao = Missao(
            trilha_id=trilha.id,
            posicao=posicao,
            nivel_de_dificuldade=nivel_de_dificuldade,
            obrigatoria=obrigatoria,
            e_sondagem=e_sondagem,
            autor_id=autor.id,
            papel_do_autor=autor.papel.value,
        )
        sessao.add(missao)
        sessao.commit()
        sessao.refresh(missao)
        return missao

    return _criar


@pytest.fixture
def criar_atividade(sessao):
    def _criar(
        missao: Missao,
        autor: Persona,
        modalidade: ModalidadeDeAtividade = ModalidadeDeAtividade.individual,
        formato: FormatoDeAtividade = FormatoDeAtividade.presencial,
        natureza: str = "construcao",
        producao_esperada: str = "Produção de teste.",
    ) -> Atividade:
        atividade = Atividade(
            missao_id=missao.id,
            modalidade=modalidade,
            formato=formato,
            natureza=natureza,
            producao_esperada=producao_esperada,
            autor_id=autor.id,
            papel_do_autor=autor.papel.value,
        )
        sessao.add(atividade)
        sessao.commit()
        sessao.refresh(atividade)
        return atividade

    return _criar


@pytest.fixture
def criar_aula(sessao):
    def _criar(
        autor: Persona,
        comunidade: ComunidadeVirtual,
        inicio_em: datetime | None = None,
        fim_em: datetime | None = None,
    ) -> Aula:
        agora = datetime.now(UTC)
        inicio = inicio_em or (agora - timedelta(hours=1))
        fim = fim_em or (agora + timedelta(hours=1))
        aula = Aula(
            comunidade_virtual_id=comunidade.id,
            inicio_em=inicio,
            fim_em=fim,
            autor_id=autor.id,
            papel_do_autor=autor.papel.value,
        )
        sessao.add(aula)
        sessao.commit()
        sessao.refresh(aula)
        return aula

    return _criar


@pytest.fixture
def criar_equipe(sessao):
    def _criar(
        criador: Persona,
        aula: Aula | None = None,
        trilha: Trilha | None = None,
        homologada: bool = False,
        homologado_por: Persona | None = None,
    ) -> Equipe:
        equipe = Equipe(
            aula_id=aula.id if aula is not None else None,
            trilha_id=trilha.id if trilha is not None else None,
            autor_id=criador.id,
            papel_do_autor=criador.papel.value,
        )
        if homologada:
            equipe.homologado_por_id = (homologado_por or criador).id
            equipe.homologado_em = datetime.now(UTC)
        sessao.add(equipe)
        sessao.commit()
        sessao.refresh(equipe)
        sessao.add(IntegranteDaEquipe(equipe_id=equipe.id, persona_id=criador.id))
        sessao.commit()
        return equipe

    return _criar


@pytest.fixture
def adicionar_integrante(sessao):
    """Vincula direto, sem passar por `entrar_na_equipe`: montar uma equipe
    de vários integrantes é cenário do teste, não o que ele exercita."""

    def _adicionar(equipe: Equipe, persona: Persona) -> IntegranteDaEquipe:
        integrante = IntegranteDaEquipe(equipe_id=equipe.id, persona_id=persona.id)
        sessao.add(integrante)
        sessao.commit()
        sessao.refresh(integrante)
        return integrante

    return _adicionar


@pytest.fixture
def criar_template_biometrico(sessao, configuracao):
    def _criar(
        guerreiro: Persona,
        descritor: list[float] | None = None,
        criada_por: Persona | None = None,
        ativa: bool = True,
    ) -> Credencial:
        valor = descritor or [0.1 * (i + 1) for i in range(DIMENSAO_DE_TESTE_DO_DESCRITOR)]
        credencial = Credencial(
            persona_id=guerreiro.id,
            tipo=TipoDeCredencial.biometria,
            identificador=str(guerreiro.id),
            segredo=cifrar_descritor(valor, configuracao),
            criada_por=criada_por.id if criada_por is not None else None,
            ativa=ativa,
        )
        sessao.add(credencial)
        sessao.commit()
        sessao.refresh(credencial)
        return credencial

    return _criar


@pytest.fixture
def criar_registro_de_auditoria(sessao):
    def _criar(
        autor: Persona,
        acao: str = "POST acao_de_teste",
        entidade_afetada: str = "acao_de_teste",
        origem: str = "app-06-vitrine",
        momento: datetime | None = None,
    ) -> Auditoria:
        registro = Auditoria(
            autor_id=autor.id,
            papel_do_autor=autor.papel.value,
            acao=acao,
            entidade_afetada=entidade_afetada,
            origem=origem,
        )
        if momento is not None:
            # `server_default` só se aplica quando a coluna não é informada
            # na inserção — a trilha é somente inserção, sem `UPDATE` depois.
            registro.momento = momento
        sessao.add(registro)
        sessao.commit()
        sessao.refresh(registro)
        return registro

    return _criar


@pytest.fixture
def fabrica_de_auditoria(engine):
    """Sessionmaker do middleware de auditoria, para testes que precisam
    ver a gravação acontecer de verdade — o mesmo padrão de
    `nucleo.cli.obter_fabrica_de_sessao`, ligado ao `engine` de teste em vez
    de à configuração real do processo."""
    return sessionmaker(bind=engine, expire_on_commit=False)


@pytest.fixture
def criar_ponto_regular(sessao):
    def _criar(guerreiro: Persona, trilha: Trilha, total: int = 10) -> PontoRegular:
        registro = PontoRegular(guerreiro_id=guerreiro.id, trilha_id=trilha.id, total=total)
        sessao.add(registro)
        sessao.commit()
        sessao.refresh(registro)
        return registro

    return _criar


@pytest.fixture
def criar_ponto_extra(sessao):
    def _criar(
        guerreiro: Persona, acumulado: int = 10, saldo_disponivel: int | None = None
    ) -> PontoExtra:
        registro = PontoExtra(
            guerreiro_id=guerreiro.id,
            acumulado=acumulado,
            saldo_disponivel=saldo_disponivel if saldo_disponivel is not None else acumulado,
        )
        sessao.add(registro)
        sessao.commit()
        sessao.refresh(registro)
        return registro

    return _criar


@pytest.fixture
def criar_nivel(sessao):
    def _criar(guerreiro: Persona, trilha: Trilha, valor: int = 1) -> Nivel:
        registro = Nivel(guerreiro_id=guerreiro.id, trilha_id=trilha.id, valor=valor)
        sessao.add(registro)
        sessao.commit()
        sessao.refresh(registro)
        return registro

    return _criar


@pytest.fixture
def criar_badge(sessao):
    def _criar(
        guerreiro: Persona,
        trilha: Trilha | None = None,
        poder: Poder | None = None,
        tipo: TipoDeBadge = TipoDeBadge.de_nivel,
    ) -> Badge:
        registro = Badge(
            guerreiro_id=guerreiro.id,
            trilha_id=trilha.id if trilha is not None else None,
            poder_id=poder.id if poder is not None else None,
            tipo=tipo,
        )
        sessao.add(registro)
        sessao.commit()
        sessao.refresh(registro)
        return registro

    return _criar


@pytest.fixture
def guerreiro_publico(criar_persona, criar_nick, criar_vinculo, criar_consentimento):
    """Guerreiro(a) com nick e autorização de divulgação vigente — o cenário
    comum a toda rota de leitura pública desta fatia."""

    def _criar(
        nick: str = "guerreira-de-teste", avatar: str | None = "avatar-de-teste"
    ) -> tuple[Persona, str]:
        guerreiro = criar_persona(Papel.guerreiro, avatar=avatar)
        criar_nick(guerreiro, nick)
        admin = criar_persona(Papel.admin)
        responsavel = criar_persona(Papel.responsavel, criada_por=admin)
        criar_vinculo(responsavel, guerreiro, cadastrado_por=admin)
        criar_consentimento(
            responsavel,
            guerreiro,
            tipo=TipoDeConsentimento.autorizacao_de_divulgacao,
            decisao=DecisaoDeConsentimento.concede,
        )
        return guerreiro, nick

    return _criar
