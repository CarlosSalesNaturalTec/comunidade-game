from nucleo.personas.modelo import Papel
from nucleo.template_de_missao.modelo import SituacaoDaSugestaoDeEstrutura


def test_mestre_autor_pede_estrutura_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha, criar_missao
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.post(
        f"/v1/missoes/{missao.id}/estrutura",
        json={"topico": "Robótica básica"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["disponivel"] is True
    assert corpo["atividades"]
    assert corpo["cadencia_de_retomada"] == [2, 7, 21]
    assert corpo["lacunas"]
    for atividade in corpo["atividades"]:
        assert "custo" not in atividade
    assert "custo" not in corpo
    assert "cota" not in corpo


def test_nao_autor_recebe_403_ao_pedir_estrutura(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha, criar_missao
):
    chave, _ = criar_chave()
    autor = criar_persona(Papel.mestre)
    outro_mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(autor)
    missao = criar_missao(trilha, autor)
    token, _ = criar_sessao_de_teste(outro_mestre)

    resposta = cliente.post(
        f"/v1/missoes/{missao.id}/estrutura",
        json={"topico": "Robótica"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 403


def test_topico_vazio_e_recusado_com_422(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha, criar_missao
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.post(
        f"/v1/missoes/{missao.id}/estrutura",
        json={"topico": ""},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 422
    assert resposta.json()["campo"] == "topico"


def test_registrar_desfecho_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha, criar_missao
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    token, _ = criar_sessao_de_teste(mestre)
    headers = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}

    resposta_do_pedido = cliente.post(
        f"/v1/missoes/{missao.id}/estrutura", json={"topico": "Robótica"}, headers=headers
    )
    sugestao_id = resposta_do_pedido.json()["sugestao_id"]

    resposta = cliente.post(
        f"/v1/sugestoes-de-estrutura/{sugestao_id}/desfecho",
        json={"situacao": SituacaoDaSugestaoDeEstrutura.recusada.value},
        headers=headers,
    )

    assert resposta.status_code == 200
    assert resposta.json()["situacao"] == SituacaoDaSugestaoDeEstrutura.recusada.value
