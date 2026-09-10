"""A escolha do adaptador de IA pelo ambiente, nas três portas que leem a
credencial única do Gemini — `RF-04-36`, `RF-04-46`, `RF-09-85`, documento 03
§1.12. Change `chave-do-gemini-em-producao`, decisão 1: uma chave e um modelo
servem as três; estes testes guardam a renomeação contra ponto de leitura
esquecido (design — Risks)."""

import pytest

from nucleo.assistente.fabrica import obter_porta_do_assistente
from nucleo.assistente.local import AssistenteDeTrilhasLocal
from nucleo.assistente.nuvem import AssistenteDeTrilhasNaNuvem
from nucleo.configuracao import Configuracao
from nucleo.producoes.fabrica import obter_porta_da_producao_da_missao
from nucleo.producoes.local import ProducaoDaMissaoLocal
from nucleo.producoes.nuvem import ProducaoDaMissaoNaNuvem
from nucleo.template_de_missao.fabrica import obter_porta_do_template_de_missao
from nucleo.template_de_missao.local import TemplateDeMissaoLocal
from nucleo.template_de_missao.nuvem import TemplateDeMissaoNaNuvem

# (fábrica, classe local, classe de nuvem)
_PORTAS = [
    (obter_porta_do_template_de_missao, TemplateDeMissaoLocal, TemplateDeMissaoNaNuvem),
    (obter_porta_da_producao_da_missao, ProducaoDaMissaoLocal, ProducaoDaMissaoNaNuvem),
    (obter_porta_do_assistente, AssistenteDeTrilhasLocal, AssistenteDeTrilhasNaNuvem),
]


def _configuracao(**extras) -> Configuracao:
    return Configuracao(
        _env_file=None,
        identidade_fundador="fundador@example.org",
        sessao_adulto_duracao="PT8H",
        sessao_guerreiro_duracao="PT4H",
        biometria_dimensao_do_descritor=128,
        biometria_limiar_de_comparacao=0.5,
        biometria_chave_de_cifragem="chave-de-cifragem-de-teste",
        **extras,
    )


def test_a_chave_e_o_modelo_do_gemini_tem_padrao():
    configuracao = _configuracao()

    assert configuracao.gemini_chave_de_api == ""
    assert configuracao.gemini_modelo == "gemini-2.5-flash"


def test_a_chave_e_o_modelo_vem_do_ambiente(monkeypatch):
    monkeypatch.setenv("CG_GEMINI_CHAVE_DE_API", "chave-vinda-do-secret-manager")
    monkeypatch.setenv("CG_GEMINI_MODELO", "gemini-outro")
    configuracao = _configuracao()

    assert configuracao.gemini_chave_de_api == "chave-vinda-do-secret-manager"
    assert configuracao.gemini_modelo == "gemini-outro"


@pytest.mark.parametrize(("fabrica", "classe_local", "_classe_de_nuvem"), _PORTAS)
def test_fora_de_producao_a_porta_e_local(fabrica, classe_local, _classe_de_nuvem):
    porta = fabrica(_configuracao(ambiente="desenvolvimento"))

    assert isinstance(porta, classe_local)


@pytest.mark.parametrize(("fabrica", "_classe_local", "classe_de_nuvem"), _PORTAS)
def test_em_producao_a_porta_e_a_nuvem_com_a_chave_unica(fabrica, _classe_local, classe_de_nuvem):
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


def test_as_tres_portas_leem_a_mesma_chave_e_o_mesmo_modelo():
    """Decisão 1: a credencial é do projeto, não do template da missão —
    provisionar uma vez acende as três funcionalidades."""
    configuracao = _configuracao(
        ambiente="producao",
        gemini_chave_de_api="chave-unica",
        gemini_modelo="gemini-unico",
    )

    portas = [fabrica(configuracao) for fabrica, _, _ in _PORTAS]

    assert {porta._chave_de_api for porta in portas} == {"chave-unica"}
    assert {porta._modelo for porta in portas} == {"gemini-unico"}


def test_em_producao_sem_chave_a_porta_existe_e_responde_indisponivel():
    """Sem a chave provisionada, a porta de nuvem é construída do mesmo jeito e
    devolve `None` — é o estado que a change vem consertar, e ele nunca pode
    virar exceção no arranque (`RF-09-91`)."""
    porta = obter_porta_do_template_de_missao(_configuracao(ambiente="producao"))

    assert isinstance(porta, TemplateDeMissaoNaNuvem)
    assert porta.sugerir_estrutura(topico="horta", exigir_atividade_desplugada=False) is None
