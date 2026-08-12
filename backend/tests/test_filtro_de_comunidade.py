def test_filtro_de_comunidade_obrigatorio_ausente_e_recusado(cliente, criar_chave):
    chave, _ = criar_chave()
    resposta = cliente.get("/v1/itens-de-comunidade", headers={"X-Chave-Aplicacao": chave})
    assert resposta.status_code == 422
    corpo = resposta.json()
    assert corpo["codigo"] == "erro_de_validacao"
    assert corpo["campo"] == "comunidade"


def test_consulta_filtrada_devolve_so_a_comunidade_pedida(cliente, criar_chave):
    chave, _ = criar_chave()
    resposta = cliente.get(
        "/v1/itens-de-comunidade",
        params={"comunidade": "comunidade-um"},
        headers={"X-Chave-Aplicacao": chave},
    )
    assert resposta.status_code == 200
    assert resposta.json()["itens"] == ["comunidade-um"]


def test_filtro_de_comunidade_nao_obrigatorio_continua_opcional(cliente, criar_chave):
    """A rota sem `filtro_comunidade_obrigatorio=True` segue aceitando a
    chamada sem o filtro — regressão da fatia anterior."""
    chave, _ = criar_chave()
    resposta = cliente.get("/v1/itens", headers={"X-Chave-Aplicacao": chave})
    assert resposta.status_code == 200
