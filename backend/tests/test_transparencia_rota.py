from nucleo.personas.modelo import Papel


def test_catalogo_traz_finalidade_e_prazo(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_vinculo
):
    chave, _ = criar_chave()
    responsavel = criar_persona(Papel.responsavel)
    guerreiro = criar_persona(Papel.guerreiro)
    criar_vinculo(responsavel, guerreiro, cadastrado_por=responsavel)
    token, _ = criar_sessao_de_teste(responsavel)

    resposta = cliente.get(
        f"/v1/eu/guerreiros/{guerreiro.id}/dados",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 200
    corpo = resposta.json()
    assert len(corpo) > 0
    for item in corpo:
        assert item["dado"]
        assert item["finalidade"]
        assert item["prazo"]
        assert isinstance(item["guardado"], bool)
        assert isinstance(item["restrito_a_gestao"], bool)


def test_linha_nao_guardada_permanece_na_lista(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_vinculo
):
    """O Guerreiro(a) sem template biométrico continua com a linha na
    lista, marcada como não guardada — não some do catálogo (`RF-13-29`)."""
    chave, _ = criar_chave()
    responsavel = criar_persona(Papel.responsavel)
    guerreiro = criar_persona(Papel.guerreiro)
    criar_vinculo(responsavel, guerreiro, cadastrado_por=responsavel)
    token, _ = criar_sessao_de_teste(responsavel)

    resposta = cliente.get(
        f"/v1/eu/guerreiros/{guerreiro.id}/dados",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    corpo = resposta.json()
    linha_do_template = next(item for item in corpo if item["dado"] == "Template biométrico")
    assert linha_do_template["guardado"] is False


def test_catalogo_nao_devolve_conteudo(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_vinculo
):
    chave, _ = criar_chave()
    responsavel = criar_persona(Papel.responsavel)
    guerreiro = criar_persona(Papel.guerreiro)
    criar_vinculo(responsavel, guerreiro, cadastrado_por=responsavel)
    token, _ = criar_sessao_de_teste(responsavel)

    resposta = cliente.get(
        f"/v1/eu/guerreiros/{guerreiro.id}/dados",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    corpo = resposta.json()
    campos_permitidos = {"dado", "finalidade", "prazo", "restrito_a_gestao", "guardado"}
    for item in corpo:
        assert set(item.keys()) == campos_permitidos


def test_consulta_ao_assistente_aparece_como_restrita_a_gestao(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_vinculo
):
    chave, _ = criar_chave()
    responsavel = criar_persona(Papel.responsavel)
    guerreiro = criar_persona(Papel.guerreiro)
    criar_vinculo(responsavel, guerreiro, cadastrado_por=responsavel)
    token, _ = criar_sessao_de_teste(responsavel)

    resposta = cliente.get(
        f"/v1/eu/guerreiros/{guerreiro.id}/dados",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    corpo = resposta.json()
    consulta = next(item for item in corpo if item["dado"] == "Consulta ao assistente de trilhas")
    apoio_escolar = next(item for item in corpo if item["dado"] == "Transcrição de apoio escolar")
    assert consulta["restrito_a_gestao"] is True
    assert apoio_escolar["restrito_a_gestao"] is True


def test_guerreiro_nao_vinculado_e_recusado(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    responsavel = criar_persona(Papel.responsavel)
    guerreiro = criar_persona(Papel.guerreiro)
    token, _ = criar_sessao_de_teste(responsavel)

    resposta = cliente.get(
        f"/v1/eu/guerreiros/{guerreiro.id}/dados",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 403


def test_outro_papel_nao_alcanca_o_catalogo(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    guerreiro = criar_persona(Papel.guerreiro)
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.get(
        f"/v1/eu/guerreiros/{guerreiro.id}/dados",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 403
