"""Paridade entre as migrações do Alembic e `Base.metadata`.

A suíte monta o schema com `Base.metadata.create_all` (conftest), que nunca
passa pelo Alembic: modelo e migração podem divergir sem que nada acuse, e
foi assim que `recompensa_de_marco` e `entrega_de_recompensa` subiram como
modelo, sem migração, e derrubaram a listagem em produção com
`UndefinedTable` (change `migracao-das-tabelas-de-recompensa-de-marco`,
design — decisão 2).

Este arquivo fecha a fresta: aplica `alembic upgrade head` num banco vazio e
confere que **nenhuma tabela e nenhuma coluna do modelo falta** no banco
migrado. Não compara tipo nem constraint — paridade de tipo entre SQLAlchemy
e o catálogo do Postgres tem falso positivo demais, e teste que grita à toa é
teste que se desliga (design — decisão 3).
"""

import uuid

import pytest
import sqlalchemy as sa
from alembic.config import Config
from sqlalchemy.engine import make_url

import nucleo.principal  # noqa: F401 — registra todo modelo do núcleo em `Base.metadata`
from alembic import command
from nucleo.banco import Base
from nucleo.configuracao import obter_configuracao

from .conftest import (
    CHAVE_DE_CIFRAGEM_DE_TESTE,
    DSN_DE_TESTE,
)

RAIZ_DO_BACKEND = __import__("pathlib").Path(__file__).resolve().parent.parent


def _tabelas_do_nucleo() -> set[str]:
    """Só as tabelas declaradas por `nucleo.*`. Arquivos de teste registram
    modelos de exemplo no mesmo `Base.metadata` — `registro_de_exemplo_autoria`
    e afins — que não têm nem devem ter migração; compará-los seria o falso
    positivo que desliga o teste (design — decisão 3)."""
    return {
        mapeador.class_.__table__.name
        for mapeador in Base.registry.mappers
        if mapeador.class_.__module__.startswith("nucleo.")
    }


@pytest.fixture
def banco_vazio():
    """Um banco próprio, criado e derrubado no teste: o banco da suíte já tem
    o schema do `create_all`, e aplicar migrações sobre ele não diria nada."""
    url = make_url(DSN_DE_TESTE)
    nome = f"cg_migracao_{uuid.uuid4().hex[:12]}"
    administrativo = sa.create_engine(url.set(database="postgres"), isolation_level="AUTOCOMMIT")
    with administrativo.connect() as conexao:
        conexao.execute(sa.text(f'CREATE DATABASE "{nome}"'))
    try:
        yield url.set(database=nome)
    finally:
        with administrativo.connect() as conexao:
            conexao.execute(
                sa.text(
                    "SELECT pg_terminate_backend(pid) FROM pg_stat_activity "
                    "WHERE datname = :nome AND pid <> pg_backend_pid()"
                ),
                {"nome": nome},
            )
            conexao.execute(sa.text(f'DROP DATABASE IF EXISTS "{nome}"'))
        administrativo.dispose()


def _configuracao_do_alembic(url, monkeypatch) -> Config:
    """O `alembic/env.py` monta a URL a partir de `obter_configuracao().dsn_banco`,
    não do `.ini` — declarar `CG_DSN_BANCO` é o mesmo caminho que o Job de
    migração usa em produção. O `.ini` não serve aqui: o caminho do socket
    (`host=%2Ftmp`) quebra a interpolação do `configparser`."""
    monkeypatch.setenv("CG_DSN_BANCO", url.render_as_string(hide_password=False))
    # As variáveis sem valor padrão: sem elas a configuração não instancia.
    monkeypatch.setenv("CG_IDENTIDADE_FUNDADOR", "fundador-de-teste@example.org")
    monkeypatch.setenv("CG_SESSAO_ADULTO_DURACAO", "PT8H")
    monkeypatch.setenv("CG_SESSAO_GUERREIRO_DURACAO", "PT4H")
    monkeypatch.setenv("CG_BIOMETRIA_CHAVE_DE_CIFRAGEM", CHAVE_DE_CIFRAGEM_DE_TESTE)
    obter_configuracao.cache_clear()
    # `Config()` sem arquivo, de propósito: com o `.ini`, o `env.py` chama
    # `fileConfig`, que desliga todos os `logger` já criados e derruba o
    # `caplog` dos testes que rodarem depois deste. Nada do `.ini` é
    # necessário aqui — a URL vem do ambiente e o `script_location` é
    # declarado abaixo.
    configuracao = Config()
    configuracao.set_main_option("script_location", str(RAIZ_DO_BACKEND / "alembic"))
    return configuracao


def test_migracoes_entregam_todas_as_tabelas_e_colunas_do_modelo(banco_vazio, monkeypatch):
    """`RF-09-71`, `RF-09-76`, `RF-07-13` e todas as demais: o que o código
    consulta precisa existir no banco que o deploy monta."""
    configuracao = _configuracao_do_alembic(banco_vazio, monkeypatch)
    command.upgrade(configuracao, "head")

    motor = sa.create_engine(banco_vazio)
    try:
        inspetor = sa.inspect(motor)
        tabelas_no_banco = set(inspetor.get_table_names())
        tabelas_no_modelo = _tabelas_do_nucleo()

        faltando = sorted(tabelas_no_modelo - tabelas_no_banco)
        assert not faltando, (
            "tabelas declaradas no modelo e ausentes das migrações: "
            f"{', '.join(faltando)}. Escreva a revisão que as cria."
        )

        colunas_faltando = {}
        for nome in sorted(tabelas_no_modelo):
            no_banco = {coluna["name"] for coluna in inspetor.get_columns(nome)}
            no_modelo = {coluna.name for coluna in Base.metadata.tables[nome].columns}
            if ausentes := sorted(no_modelo - no_banco):
                colunas_faltando[nome] = ausentes
        assert not colunas_faltando, (
            f"colunas declaradas no modelo e ausentes das migrações: {colunas_faltando}"
        )
    finally:
        motor.dispose()
        obter_configuracao.cache_clear()


def test_a_revisao_do_topo_sobe_e_desce(banco_vazio, monkeypatch):
    """Migração que não desce trava a reversão de um deploy ruim."""
    configuracao = _configuracao_do_alembic(banco_vazio, monkeypatch)
    command.upgrade(configuracao, "head")
    command.downgrade(configuracao, "-1")
    command.upgrade(configuracao, "head")

    motor = sa.create_engine(banco_vazio)
    try:
        tabelas = set(sa.inspect(motor).get_table_names())
        assert {"recompensa_de_marco", "entrega_de_recompensa"} <= tabelas
    finally:
        motor.dispose()
        obter_configuracao.cache_clear()


def test_um_dsn_com_porcento_nao_derruba_a_migracao(banco_vazio, monkeypatch):
    """`set_main_option` grava num `configparser`, que interpola `%`: sem
    escapar, `invalid interpolation syntax` derrubava o Job de migração. O
    README já lista `/` e `+` como proibidos na senha do DSN; este é o
    terceiro caractere, e o conserto tira todos os três da lista (change
    `template-da-missao-no-deepseek`, design — decisão 5)."""
    com_porcento = banco_vazio.set(query={**banco_vazio.query, "application_name": "cg%25teste"})
    configuracao = _configuracao_do_alembic(com_porcento, monkeypatch)

    command.upgrade(configuracao, "head")

    motor = sa.create_engine(banco_vazio)
    try:
        assert "recompensa_de_marco" in set(sa.inspect(motor).get_table_names())
    finally:
        motor.dispose()
        obter_configuracao.cache_clear()


def test_a_subida_do_piso_eleva_so_o_preco_vigente_abaixo_de_25(banco_vazio, monkeypatch):
    """`RF-07-50`, `RF-07-43`: a migração encerra a vigência aberta abaixo de
    25 e abre a de 25 na data da entrega; a de 40 não muda, e a consulta por
    data anterior segue lendo o preço antigo (design — decisão 5)."""
    configuracao = _configuracao_do_alembic(banco_vazio, monkeypatch)
    command.upgrade(configuracao, "e7d3c4f5a6b7")

    barato, caro, autor = uuid.uuid4(), uuid.uuid4(), uuid.uuid4()
    motor = sa.create_engine(banco_vazio)
    try:
        with motor.begin() as conexao:
            conexao.execute(
                sa.text("INSERT INTO persona (id, papel) VALUES (:autor, 'admin')"),
                {"autor": autor},
            )
            for tipo in (barato, caro):
                conexao.execute(
                    sa.text(
                        "INSERT INTO tipo_de_recurso (id, nome, natureza, unidade, autor_id, "
                        "papel_do_autor) VALUES (:tipo, :nome, 'consumivel', 'unidade', "
                        ":autor, 'admin')"
                    ),
                    {"tipo": tipo, "nome": f"Tipo {tipo.hex[:6]}", "autor": autor},
                )
            for tipo, preco in ((barato, 20), (caro, 40)):
                conexao.execute(
                    sa.text(
                        "INSERT INTO preco_de_referencia (id, tipo_de_recurso_id, "
                        "preco_em_pontos_extras, vigencia_inicio, autor_id, papel_do_autor) "
                        "VALUES (gen_random_uuid(), :tipo, :preco, DATE '2026-01-01', "
                        ":autor, 'admin')"
                    ),
                    {"tipo": tipo, "preco": preco, "autor": autor},
                )

        command.upgrade(configuracao, "head")

        with motor.connect() as conexao:
            linhas = conexao.execute(
                sa.text(
                    "SELECT tipo_de_recurso_id, preco_em_pontos_extras, vigencia_inicio, "
                    "vigencia_fim, papel_do_autor, CURRENT_DATE AS hoje "
                    "FROM preco_de_referencia ORDER BY tipo_de_recurso_id, vigencia_inicio"
                )
            ).all()
            do_barato = [linha for linha in linhas if linha.tipo_de_recurso_id == barato]
            do_caro = [linha for linha in linhas if linha.tipo_de_recurso_id == caro]

            assert [linha.preco_em_pontos_extras for linha in do_barato] == [20, 25]
            antigo, novo = do_barato
            assert antigo.vigencia_fim == antigo.hoje
            assert novo.vigencia_inicio == antigo.hoje and novo.vigencia_fim is None
            assert novo.papel_do_autor == "migracao"
            assert [(linha.preco_em_pontos_extras, linha.vigencia_fim) for linha in do_caro] == [
                (40, None)
            ]

            vigente_antes = conexao.execute(
                sa.text(
                    "SELECT preco_em_pontos_extras FROM preco_de_referencia "
                    "WHERE tipo_de_recurso_id = :tipo AND vigencia_inicio <= DATE '2026-02-01' "
                    "AND (vigencia_fim IS NULL OR vigencia_fim > DATE '2026-02-01')"
                ),
                {"tipo": barato},
            ).scalar_one()
            assert vigente_antes == 20

        with pytest.raises(sa.exc.IntegrityError), motor.begin() as conexao:
            conexao.execute(
                sa.text(
                    "INSERT INTO preco_de_referencia (id, tipo_de_recurso_id, "
                    "preco_em_pontos_extras, vigencia_inicio, autor_id, papel_do_autor) "
                    "VALUES (gen_random_uuid(), :tipo, 24, CURRENT_DATE, :autor, 'admin')"
                ),
                {"tipo": caro, "autor": autor},
            )
    finally:
        motor.dispose()
        obter_configuracao.cache_clear()
