import pytest
from pydantic import ValidationError

from nucleo.configuracao import Configuracao


def test_nucleo_nao_sobe_sem_identidade_do_fundador():
    with pytest.raises(ValidationError) as excinfo:
        Configuracao(_env_file=None, sessao_adulto_duracao="PT8H")
    assert "identidade_fundador" in str(excinfo.value)


def test_nucleo_nao_sobe_sem_duracao_da_sessao_do_adulto():
    with pytest.raises(ValidationError) as excinfo:
        Configuracao(_env_file=None, identidade_fundador="fundador@example.org")
    assert "sessao_adulto_duracao" in str(excinfo.value)


def test_nucleo_nao_sobe_sem_nenhum_dos_dois():
    with pytest.raises(ValidationError) as excinfo:
        Configuracao(_env_file=None)
    mensagem = str(excinfo.value)
    assert "identidade_fundador" in mensagem
    assert "sessao_adulto_duracao" in mensagem


def test_nucleo_nao_sobe_sem_chave_de_cifragem_do_template():
    with pytest.raises(ValidationError) as excinfo:
        Configuracao(
            _env_file=None,
            identidade_fundador="fundador@example.org",
            sessao_adulto_duracao="PT8H",
            sessao_guerreiro_duracao="PT4H",
            biometria_dimensao_do_descritor=128,
            biometria_limiar_de_comparacao=0.5,
        )
    assert "biometria_chave_de_cifragem" in str(excinfo.value)


def test_nucleo_nao_sobe_sem_duracao_da_sessao_do_guerreiro():
    with pytest.raises(ValidationError) as excinfo:
        Configuracao(
            _env_file=None,
            identidade_fundador="fundador@example.org",
            sessao_adulto_duracao="PT8H",
            biometria_dimensao_do_descritor=128,
            biometria_limiar_de_comparacao=0.5,
            biometria_chave_de_cifragem="qualquer",
        )
    assert "sessao_guerreiro_duracao" in str(excinfo.value)
