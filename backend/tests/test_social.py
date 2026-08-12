import httpx
import pytest
from google.auth.exceptions import TransportError

from nucleo.erros import ServicoIndisponivel
from nucleo.sessoes.social import TokenSocialInvalido, verificar_id_token


def test_falha_de_rede_no_jwks_responde_servico_indisponivel(monkeypatch, configuracao):
    def _levanta_falha_de_transporte(*args, **kwargs):
        raise httpx.ConnectError("rede indisponível")

    monkeypatch.setattr(httpx, "request", _levanta_falha_de_transporte)

    with pytest.raises(ServicoIndisponivel):
        verificar_id_token("um-token-qualquer", configuracao)


def test_token_invalido_nao_e_confundido_com_falha_de_rede(monkeypatch, configuracao):
    def _levanta_erro_de_verificacao(*args, **kwargs):
        raise ValueError("assinatura inválida")

    monkeypatch.setattr(
        "nucleo.sessoes.social.google_id_token.verify_oauth2_token",
        _levanta_erro_de_verificacao,
    )

    with pytest.raises(TokenSocialInvalido):
        verificar_id_token("um-token-qualquer", configuracao)


def test_transport_error_nunca_vira_token_invalido(monkeypatch, configuracao):
    def _levanta_transport_error(*args, **kwargs):
        raise TransportError("timeout buscando certs")

    monkeypatch.setattr(
        "nucleo.sessoes.social.google_id_token.verify_oauth2_token",
        _levanta_transport_error,
    )

    with pytest.raises(ServicoIndisponivel):
        verificar_id_token("um-token-qualquer", configuracao)
