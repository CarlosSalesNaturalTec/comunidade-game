"""A leitura da própria presença pelo Guerreiro(a) em sessão — `RF-04-68` e
`RN-04-40`, a porta que deixa a App 01 recusar o caminho das equipes antes
de chegar a elas."""

import uuid

from nucleo.personas.modelo import Papel


def _cabecalhos(chave, token):
    return {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}


def test_quem_registrou_a_presenca_a_le(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_presenca,
    criar_sessao_de_teste,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(admin, comunidade)
    presenca = criar_presenca(aula, guerreiro)
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.get(f"/v1/aulas/{aula.id}/presencas/eu", headers=_cabecalhos(chave, token))

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["presente"] is True
    assert corpo["modo"] == presenca.modo.value
    assert corpo["momento_do_fato"] is not None


def test_quem_nao_registrou_recebe_resposta_e_nao_erro(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_sessao_de_teste,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(admin, comunidade)
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.get(f"/v1/aulas/{aula.id}/presencas/eu", headers=_cabecalhos(chave, token))

    assert resposta.status_code == 200
    assert resposta.json() == {"presente": False, "momento_do_fato": None, "modo": None}


def test_presenca_anulada_e_lida_como_ausencia(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_presenca,
    criar_sessao_de_teste,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(admin, comunidade)
    criar_presenca(aula, guerreiro, confirmador=admin, anulada=True)
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.get(f"/v1/aulas/{aula.id}/presencas/eu", headers=_cabecalhos(chave, token))

    assert resposta.status_code == 200
    assert resposta.json()["presente"] is False


def test_a_leitura_e_sempre_da_propria_persona(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_presenca,
    criar_sessao_de_teste,
):
    """A presença do outro não vaza: o Guerreiro(a) lido vem do contexto da
    sessão, e a rota não tem por onde receber outro (invariante 15)."""
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    presente = criar_persona(Papel.guerreiro, comunidade=comunidade)
    ausente = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(admin, comunidade)
    criar_presenca(aula, presente)
    token, _ = criar_sessao_de_teste(ausente)

    resposta = cliente.get(f"/v1/aulas/{aula.id}/presencas/eu", headers=_cabecalhos(chave, token))

    assert resposta.status_code == 200
    assert resposta.json()["presente"] is False


def test_aula_inexistente_responde_404(
    cliente, criar_chave, criar_persona, criar_comunidade, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.get(
        f"/v1/aulas/{uuid.uuid4()}/presencas/eu", headers=_cabecalhos(chave, token)
    )

    assert resposta.status_code == 404


def test_a_rota_esta_no_openapi_sob_v1(cliente):
    caminhos = cliente.get("/openapi.json").json()["paths"]

    assert "/v1/aulas/{id_da_aula}/presencas/eu" in caminhos
