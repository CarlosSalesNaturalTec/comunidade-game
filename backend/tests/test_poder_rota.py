from nucleo.personas.modelo import Papel
from nucleo.poderes.modelo import NaturezaDoPoder, PapelDoPoder, VigenciaDoPoder
from nucleo.trilhas.modelo import SituacaoDaTrilha


def test_admin_cadastra_poder_pela_rota(cliente, criar_chave, criar_persona, criar_sessao_de_teste):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.post(
        "/v1/poderes",
        json={
            "nome": "Poder da IA e Robótica",
            "descricao": "Programação, eletrônica, robótica e IA.",
            "natureza": NaturezaDoPoder.de_guerreiro.value,
            "vigencia": VigenciaDoPoder.vigente.value,
            "papel": PapelDoPoder.territorio.value,
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["nome"] == "Poder da IA e Robótica"
    assert corpo["natureza"] == NaturezaDoPoder.de_guerreiro.value
    assert corpo["vigencia"] == VigenciaDoPoder.vigente.value
    assert corpo["papel"] == PapelDoPoder.territorio.value
    assert corpo["ativo"] is True


def test_mestre_recebe_403_ao_cadastrar_alterar_e_desativar_poder(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_poder
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    poder = criar_poder(admin)
    token, _ = criar_sessao_de_teste(mestre)
    headers = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}

    resposta_de_cadastro = cliente.post(
        "/v1/poderes",
        json={
            "nome": "Poder da Rima",
            "descricao": "Expressão artística.",
            "natureza": NaturezaDoPoder.de_guerreiro.value,
        },
        headers=headers,
    )
    resposta_de_alteracao = cliente.put(
        f"/v1/poderes/{poder.id}", json={"nome": "Novo nome"}, headers=headers
    )
    resposta_de_desativacao = cliente.post(f"/v1/poderes/{poder.id}/desativacao", headers=headers)

    assert resposta_de_cadastro.status_code == 403
    assert resposta_de_alteracao.status_code == 403
    assert resposta_de_desativacao.status_code == 403


def test_cadastro_sem_nome_e_recusado_com_422(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.post(
        "/v1/poderes",
        json={
            "nome": "",
            "descricao": "Descrição qualquer.",
            "natureza": NaturezaDoPoder.de_guerreiro.value,
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 422
    assert resposta.json()["campo"] == "nome"


def test_alteracao_com_nome_vazio_e_recusada_com_422(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_poder
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    poder = criar_poder(admin, nome="Nome original")
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.put(
        f"/v1/poderes/{poder.id}",
        json={"nome": "   "},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 422
    assert resposta.json()["campo"] == "nome"


def test_segundo_papel_do_territorio_e_recusado_com_409(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_poder
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    criar_poder(admin, nome="Poder do Território", papel=PapelDoPoder.territorio)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.post(
        "/v1/poderes",
        json={
            "nome": "Poder do Território (duplicado)",
            "descricao": "Descrição de teste.",
            "natureza": NaturezaDoPoder.de_guerreiro.value,
            "papel": PapelDoPoder.territorio.value,
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 409


def test_listagem_da_gestao_traz_natureza_vigencia_papel_e_ativo(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_poder
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    criar_poder(
        admin,
        nome="Poder do Território",
        papel=PapelDoPoder.territorio,
        vigencia=VigenciaDoPoder.ciclo_futuro,
    )
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.get(
        "/v1/poderes",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 200
    item = resposta.json()["itens"][0]
    assert item["natureza"] == NaturezaDoPoder.de_guerreiro.value
    assert item["vigencia"] == VigenciaDoPoder.ciclo_futuro.value
    assert item["papel"] == PapelDoPoder.territorio.value
    assert item["ativo"] is True


def test_poder_desativado_aparece_na_gestao_e_some_da_vitrine(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_poder
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    poder = criar_poder(admin, nome="Poder da Rima")
    token, _ = criar_sessao_de_teste(admin)
    headers_de_gestao = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}

    resposta_de_desativacao = cliente.post(
        f"/v1/poderes/{poder.id}/desativacao", headers=headers_de_gestao
    )
    assert resposta_de_desativacao.status_code == 200
    assert resposta_de_desativacao.json()["ativo"] is False

    resposta_da_gestao = cliente.get("/v1/poderes", headers=headers_de_gestao)
    nomes_inativos = [
        item["nome"] for item in resposta_da_gestao.json()["itens"] if not item["ativo"]
    ]
    assert "Poder da Rima" in nomes_inativos

    resposta_da_vitrine = cliente.get("/v1/vitrine/poderes", headers={"X-Chave-Aplicacao": chave})
    nomes_da_vitrine = [item["nome"] for item in resposta_da_vitrine.json()]
    assert "Poder da Rima" not in nomes_da_vitrine


def test_leitura_do_catalogo_sem_persona_e_recusada(cliente, criar_chave):
    chave, _ = criar_chave()

    resposta = cliente.get("/v1/poderes", headers={"X-Chave-Aplicacao": chave})

    assert resposta.status_code == 401


def test_listagem_pagina_por_nome_e_id(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_poder,
    sobrescrever_configuracao,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    criar_poder(admin, nome="Poder A")
    criar_poder(admin, nome="Poder B")
    token, _ = criar_sessao_de_teste(admin)
    sobrescrever_configuracao(paginacao_tamanho_padrao=1)
    headers = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}

    primeira_pagina = cliente.get("/v1/poderes", headers=headers)
    assert len(primeira_pagina.json()["itens"]) == 1
    cursor = primeira_pagina.json()["proximo_cursor"]
    assert cursor is not None

    segunda_pagina = cliente.get("/v1/poderes", params={"cursor": cursor}, headers=headers)
    assert len(segunda_pagina.json()["itens"]) == 1
    assert segunda_pagina.json()["itens"][0]["id"] != primeira_pagina.json()["itens"][0]["id"]


def test_renomear_o_poder_do_territorio_mantem_o_papel(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_poder
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    poder = criar_poder(admin, nome="Poder do Território", papel=PapelDoPoder.territorio)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.put(
        f"/v1/poderes/{poder.id}",
        json={"nome": "Novo nome do Poder do Território"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["nome"] == "Novo nome do Poder do Território"
    assert corpo["papel"] == PapelDoPoder.territorio.value

    resposta_da_vitrine = cliente.get("/v1/vitrine/poderes", headers={"X-Chave-Aplicacao": chave})
    nomes_da_vitrine = [item["nome"] for item in resposta_da_vitrine.json()]
    assert "Novo nome do Poder do Território" in nomes_da_vitrine


def test_poder_desativado_com_trilha_vinculada_mantem_o_vinculo(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_poder,
    criar_trilha,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    poder = criar_poder(admin, nome="Poder da Rima")
    trilha = criar_trilha(admin, poder=poder, situacao=SituacaoDaTrilha.publicada)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.post(
        f"/v1/poderes/{poder.id}/desativacao",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 200
    assert resposta.json()["ativo"] is False
    assert trilha.poder_id == poder.id
