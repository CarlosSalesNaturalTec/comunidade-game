"""A escolha do adaptador de armazenamento e a guarda da implantação.

O adaptador de nuvem não tinha teste nenhum, e foi por aí que a implantação
subiu sem `CG_ARMAZENAMENTO_BUCKET_CLOUD_STORAGE`: em produção a fábrica
devolve **sempre** o adaptador de nuvem — não há queda para disco, ao
contrário do que o README afirmava —, e o nome vazio estourava `IndexError`
na validação do bucket, numa requisição qualquer. Oito módulos responderam
500 por isso (change `bucket-de-armazenamento-em-producao`, decisão 2).
"""

from datetime import timedelta

import pytest

from nucleo.armazenamento.disco import ArmazenamentoEmDisco
from nucleo.armazenamento.fabrica import obter_porta_de_armazenamento
from nucleo.configuracao import (
    Configuracao,
    ConfiguracaoDeProducaoIncompleta,
    conferir_configuracao_de_producao,
)

CHAVE_DE_CIFRAGEM = "a" * 32


def _configuracao(**extras) -> Configuracao:
    return Configuracao(
        _env_file=None,
        identidade_fundador="fundador-de-teste@example.org",
        sessao_adulto_duracao=timedelta(hours=8),
        sessao_guerreiro_duracao=timedelta(hours=4),
        biometria_dimensao_do_descritor=4,
        biometria_limiar_de_comparacao=0.5,
        biometria_chave_de_cifragem=CHAVE_DE_CIFRAGEM,
        **extras,
    )


def test_fora_de_producao_a_porta_e_disco_sem_exigir_credencial(tmp_path):
    """`RF-09-19` e o desenho de sempre: desenvolvimento e a esteira não
    precisam de bucket nem de credencial de nuvem."""
    porta = obter_porta_de_armazenamento(
        _configuracao(
            ambiente="desenvolvimento",
            armazenamento_diretorio_local=str(tmp_path / "arquivos"),
            armazenamento_diretorio_sessoes_locais=str(tmp_path / "sessoes"),
        )
    )

    assert isinstance(porta, ArmazenamentoEmDisco)


def test_fora_de_producao_o_bucket_vazio_nao_atrapalha(tmp_path):
    porta = obter_porta_de_armazenamento(
        _configuracao(
            ambiente="desenvolvimento",
            armazenamento_bucket_cloud_storage="",
            armazenamento_diretorio_local=str(tmp_path / "arquivos"),
            armazenamento_diretorio_sessoes_locais=str(tmp_path / "sessoes"),
        )
    )

    assert isinstance(porta, ArmazenamentoEmDisco)


def test_em_producao_sem_bucket_a_fabrica_recusa_nomeando_a_variavel():
    """Nunca `IndexError`, e nunca queda silenciosa para disco: o disco do
    Cloud Run é efêmero e perderia o envio no deploy seguinte."""
    with pytest.raises(ConfiguracaoDeProducaoIncompleta) as excinfo:
        obter_porta_de_armazenamento(_configuracao(ambiente="producao"))

    assert "CG_ARMAZENAMENTO_BUCKET_CLOUD_STORAGE" in str(excinfo.value)


def test_o_arranque_recusa_producao_sem_bucket():
    """A mesma falta derruba o arranque, e não uma requisição de usuário: o
    Cloud Run mantém a revisão anterior servindo quando a nova não sobe."""
    with pytest.raises(ConfiguracaoDeProducaoIncompleta) as excinfo:
        conferir_configuracao_de_producao(_configuracao(ambiente="producao"))

    assert "CG_ARMAZENAMENTO_BUCKET_CLOUD_STORAGE" in str(excinfo.value)


def test_o_arranque_passa_em_producao_com_bucket_declarado():
    conferir_configuracao_de_producao(
        _configuracao(ambiente="producao", armazenamento_bucket_cloud_storage="um-bucket")
    )


def test_o_arranque_nao_exige_bucket_fora_de_producao():
    conferir_configuracao_de_producao(_configuracao(ambiente="desenvolvimento"))


def test_o_arranque_nao_exige_chave_de_ia():
    """As portas de IA ficam de fora da guarda de propósito: ali a
    indisponibilidade é comportamento previsto e a tela avisa em linguagem
    simples (`RF-09-91`, `RN-04-21`, `RN-05-35`)."""
    conferir_configuracao_de_producao(
        _configuracao(
            ambiente="producao",
            armazenamento_bucket_cloud_storage="um-bucket",
            gemini_chave_de_api="",
        )
    )


def test_o_lifespan_recusa_o_servico_em_producao_sem_bucket(monkeypatch):
    """A guarda é do `lifespan`, não do corpo de `criar_app`: importar o
    módulo continua não exigindo ambiente completo, e é o serviço que deixa
    de ficar pronto — o Cloud Run mantém a revisão anterior no ar."""
    from fastapi.testclient import TestClient

    from nucleo.configuracao import obter_configuracao
    from nucleo.principal import criar_app

    for variavel, valor in {
        "CG_AMBIENTE": "producao",
        "CG_IDENTIDADE_FUNDADOR": "fundador-de-teste@example.org",
        "CG_SESSAO_ADULTO_DURACAO": "PT8H",
        "CG_SESSAO_GUERREIRO_DURACAO": "PT4H",
        "CG_BIOMETRIA_DIMENSAO_DO_DESCRITOR": "4",
        "CG_BIOMETRIA_LIMIAR_DE_COMPARACAO": "0.5",
        "CG_BIOMETRIA_CHAVE_DE_CIFRAGEM": CHAVE_DE_CIFRAGEM,
    }.items():
        monkeypatch.setenv(variavel, valor)
    monkeypatch.delenv("CG_ARMAZENAMENTO_BUCKET_CLOUD_STORAGE", raising=False)
    obter_configuracao.cache_clear()

    try:
        with pytest.raises(ConfiguracaoDeProducaoIncompleta):
            with TestClient(criar_app()):
                pass
    finally:
        obter_configuracao.cache_clear()
