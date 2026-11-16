"""A escolha do adaptador de IA pelo ambiente, nas duas portas — `RF-04-36`,
`RF-04-46`, documento 03 §1.12.

A leitura da produção e o assistente seguem no **Gemini**, único modelo de
linguagem do Ciclo 01 desde a retirada do template da missão (decisão do
fundador de 2026-11-16)."""

import pytest

from nucleo.assistente.fabrica import obter_porta_do_assistente
from nucleo.assistente.local import AssistenteDeTrilhasLocal
from nucleo.assistente.nuvem import AssistenteDeTrilhasNaNuvem
from nucleo.configuracao import Configuracao
from nucleo.producoes.fabrica import obter_porta_da_producao_da_missao
from nucleo.producoes.local import ProducaoDaMissaoLocal
from nucleo.producoes.nuvem import ProducaoDaMissaoNaNuvem

# (fábrica, classe local, classe de nuvem)
_PORTAS_DO_GEMINI = [
    (obter_porta_da_producao_da_missao, ProducaoDaMissaoLocal, ProducaoDaMissaoNaNuvem),
    (obter_porta_do_assistente, AssistenteDeTrilhasLocal, AssistenteDeTrilhasNaNuvem),
]
_PORTAS = _PORTAS_DO_GEMINI


def _configuracao(**extras) -> Configuracao:
    return Configuracao(
        _env_file=None,
        identidade_fundador="fundador@example.org",
        sessao_adulto_duracao="PT8H",
        sessao_guerreiro_duracao="PT4H",
        biometria_chave_de_cifragem="chave-de-cifragem-de-teste",
        **extras,
    )


def test_as_credenciais_de_ia_tem_padrao():
    configuracao = _configuracao()

    assert configuracao.gemini_chave_de_api == ""
    assert configuracao.gemini_modelo == "gemini-2.5-flash"
    assert not hasattr(configuracao, "deepseek_chave_de_api")


def test_as_credenciais_de_ia_vem_do_ambiente(monkeypatch):
    monkeypatch.setenv("CG_GEMINI_CHAVE_DE_API", "chave-do-gemini")
    monkeypatch.setenv("CG_GEMINI_MODELO", "gemini-outro")
    # A chave antiga ainda declarada no Cloud Run não derruba a subida
    # (design — decisão 5).
    monkeypatch.setenv("CG_DEEPSEEK_CHAVE_DE_API", "chave-do-deepseek")
    configuracao = _configuracao()

    assert configuracao.gemini_chave_de_api == "chave-do-gemini"
    assert configuracao.gemini_modelo == "gemini-outro"


@pytest.mark.parametrize(("fabrica", "classe_local", "_classe_de_nuvem"), _PORTAS)
def test_fora_de_producao_a_porta_e_local(fabrica, classe_local, _classe_de_nuvem):
    porta = fabrica(_configuracao(ambiente="desenvolvimento"))

    assert isinstance(porta, classe_local)


@pytest.mark.parametrize(("fabrica", "_classe_local", "classe_de_nuvem"), _PORTAS_DO_GEMINI)
def test_em_producao_a_porta_e_a_nuvem_com_a_chave_do_gemini(
    fabrica, _classe_local, classe_de_nuvem
):
    porta = fabrica(
        _configuracao(
            ambiente="producao",
            gemini_chave_de_api="chave-de-producao",
            gemini_modelo="gemini-de-producao",
        )
    )

    assert isinstance(porta, classe_de_nuvem)
    assert porta._chave_de_api == "chave-de-producao"
    assert porta._modelo == "gemini-de-producao"


@pytest.mark.parametrize(("fabrica", "_classe_local", "classe_de_nuvem"), _PORTAS_DO_GEMINI)
def test_em_producao_sem_chave_a_porta_existe(fabrica, _classe_local, classe_de_nuvem):
    """Sem a chave provisionada, a porta de nuvem é construída do mesmo jeito:
    indisponibilidade de modelo é comportamento previsto e nunca pode virar
    exceção no arranque — ao contrário do bucket, cuja falta impede o serviço
    de ficar pronto."""
    porta = fabrica(_configuracao(ambiente="producao"))

    assert isinstance(porta, classe_de_nuvem)
