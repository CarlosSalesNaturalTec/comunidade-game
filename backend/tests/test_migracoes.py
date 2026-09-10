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
    DIMENSAO_DE_TESTE_DO_DESCRITOR,
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
    monkeypatch.setenv("CG_BIOMETRIA_DIMENSAO_DO_DESCRITOR", str(DIMENSAO_DE_TESTE_DO_DESCRITOR))
    monkeypatch.setenv("CG_BIOMETRIA_LIMIAR_DE_COMPARACAO", "0.5")
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
