"""A escolha do adaptador de IA pelo ambiente, nas três portas — `RF-04-36`,
`RF-04-46`, `RF-09-85`, documento 03 §1.12.

O modelo é escolhido por funcionalidade, não por provedor único: o template
da missão manda só texto e vai para o **DeepSeek**; a leitura da produção e o
assistente leem imagem e áudio e seguem no **Gemini**. Estes testes guardam a
divisão contra ponto de leitura trocado."""

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
# As duas que leem imagem e áudio seguem no Gemini; o template da missão
# manda só texto e foi para o DeepSeek (documento 03 §1.12).
_PORTAS_DO_GEMINI = [
    (obter_porta_da_producao_da_missao, ProducaoDaMissaoLocal, ProducaoDaMissaoNaNuvem),
    (obter_porta_do_assistente, AssistenteDeTrilhasLocal, AssistenteDeTrilhasNaNuvem),
]
_PORTAS = [
    (obter_porta_do_template_de_missao, TemplateDeMissaoLocal, TemplateDeMissaoNaNuvem),
    *_PORTAS_DO_GEMINI,
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


def test_as_credenciais_de_ia_tem_padrao():
    configuracao = _configuracao()

    assert configuracao.gemini_chave_de_api == ""
    assert configuracao.gemini_modelo == "gemini-2.5-flash"
    assert configuracao.deepseek_chave_de_api == ""
    assert configuracao.deepseek_modelo == "deepseek-v4-flash"


def test_as_credenciais_de_ia_vem_do_ambiente(monkeypatch):
    monkeypatch.setenv("CG_GEMINI_CHAVE_DE_API", "chave-do-gemini")
    monkeypatch.setenv("CG_GEMINI_MODELO", "gemini-outro")
    monkeypatch.setenv("CG_DEEPSEEK_CHAVE_DE_API", "chave-do-deepseek")
    monkeypatch.setenv("CG_DEEPSEEK_MODELO", "deepseek-outro")
    configuracao = _configuracao()

    assert configuracao.gemini_chave_de_api == "chave-do-gemini"
    assert configuracao.gemini_modelo == "gemini-outro"
    assert configuracao.deepseek_chave_de_api == "chave-do-deepseek"
    assert configuracao.deepseek_modelo == "deepseek-outro"


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


def test_o_template_da_missao_le_a_dupla_do_deepseek():
    """A porta de texto foi para o provedor de menor custo, e deixou de
    compartilhar credencial com as outras duas (documento 03 §1.12)."""
    porta = obter_porta_do_template_de_missao(
        _configuracao(
            ambiente="producao",
            deepseek_chave_de_api="chave-do-deepseek",
            deepseek_modelo="deepseek-de-producao",
            gemini_chave_de_api="chave-do-gemini",
        )
    )

    assert isinstance(porta, TemplateDeMissaoNaNuvem)
    assert porta._chave_de_api == "chave-do-deepseek"
    assert porta._modelo == "deepseek-de-producao"


def test_cada_provedor_tem_a_sua_credencial():
    """Trocar as duplas de lugar é o erro que este teste existe para pegar."""
    configuracao = _configuracao(
        ambiente="producao",
        gemini_chave_de_api="chave-do-gemini",
        deepseek_chave_de_api="chave-do-deepseek",
    )

    do_gemini = [fabrica(configuracao) for fabrica, _, _ in _PORTAS_DO_GEMINI]

    assert {porta._chave_de_api for porta in do_gemini} == {"chave-do-gemini"}
    assert obter_porta_do_template_de_missao(configuracao)._chave_de_api == "chave-do-deepseek"


def test_em_producao_sem_chave_a_porta_existe_e_responde_indisponivel():
    """Sem a chave provisionada, a porta de nuvem é construída do mesmo jeito e
    devolve `None`: indisponibilidade de modelo é comportamento previsto e
    nunca pode virar exceção no arranque (`RF-09-91`) — ao contrário do
    bucket, cuja falta impede o serviço de ficar pronto."""
    porta = obter_porta_do_template_de_missao(_configuracao(ambiente="producao"))

    assert isinstance(porta, TemplateDeMissaoNaNuvem)
    assert porta.sugerir_estrutura(topico="horta", exigir_atividade_desplugada=False) is None
