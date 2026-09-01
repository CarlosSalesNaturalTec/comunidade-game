from datetime import UTC, datetime

from nucleo.consentimentos.modelo import Consentimento, OrigemDoConsentimento
from nucleo.personas.modelo import Papel


def test_mestre_registra_o_ato_assistido_com_testemunha(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_vinculo, sessao
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    responsavel = criar_persona(Papel.responsavel, criada_por=admin)
    guerreiro = criar_persona(Papel.guerreiro)
    criar_vinculo(responsavel, guerreiro, cadastrado_por=admin)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.post(
        f"/v1/guerreiros/{guerreiro.id}/autorizacao/assistida",
        json={
            "responsavel_id": str(responsavel.id),
            "decisao": "concede",
            "testemunha_id": str(mestre.id),
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["responsavel_id"] == str(responsavel.id)
    assert corpo["decisao"] == "concede"

    consentimento = sessao.query(Consentimento).one()
    assert consentimento.origem == OrigemDoConsentimento.assistida
    assert consentimento.autor_id == mestre.id
    assert consentimento.testemunha_id == mestre.id
    assert consentimento.responsavel_id == responsavel.id


def test_ato_assistido_produz_o_mesmo_estado_que_o_ato_do_proprio(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_vinculo
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    responsavel = criar_persona(Papel.responsavel, criada_por=admin)
    guerreiro = criar_persona(Papel.guerreiro)
    criar_vinculo(responsavel, guerreiro, cadastrado_por=admin)
    token_do_admin, _ = criar_sessao_de_teste(admin)

    cliente.post(
        f"/v1/guerreiros/{guerreiro.id}/autorizacao/assistida",
        json={
            "responsavel_id": str(responsavel.id),
            "decisao": "concede",
            "testemunha_id": str(admin.id),
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token_do_admin}"},
    )

    token_do_responsavel, _ = criar_sessao_de_teste(responsavel)
    resposta = cliente.get(
        f"/v1/eu/guerreiros/{guerreiro.id}/autorizacao",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token_do_responsavel}"},
    )
    assert resposta.json()["estado"] == "vigente"


def test_sem_responsavel_presente_e_recusado_com_422(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, sessao
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    guerreiro = criar_persona(Papel.guerreiro)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.post(
        f"/v1/guerreiros/{guerreiro.id}/autorizacao/assistida",
        json={"decisao": "concede", "testemunha_id": str(admin.id)},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 422
    assert sessao.query(Consentimento).count() == 0


def test_sem_testemunha_e_recusado_com_422(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_vinculo, sessao
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    responsavel = criar_persona(Papel.responsavel, criada_por=admin)
    guerreiro = criar_persona(Papel.guerreiro)
    criar_vinculo(responsavel, guerreiro, cadastrado_por=admin)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.post(
        f"/v1/guerreiros/{guerreiro.id}/autorizacao/assistida",
        json={"responsavel_id": str(responsavel.id), "decisao": "concede"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 422
    assert sessao.query(Consentimento).count() == 0


def test_responsavel_sem_vinculo_vigente_e_recusado_com_403(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, sessao
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    responsavel = criar_persona(Papel.responsavel, criada_por=admin)
    guerreiro = criar_persona(Papel.guerreiro)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.post(
        f"/v1/guerreiros/{guerreiro.id}/autorizacao/assistida",
        json={
            "responsavel_id": str(responsavel.id),
            "decisao": "concede",
            "testemunha_id": str(admin.id),
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 403
    assert sessao.query(Consentimento).count() == 0


def test_recusa_assistida_suspende_como_qualquer_outra(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_vinculo
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    responsavel_1 = criar_persona(Papel.responsavel, criada_por=admin)
    responsavel_2 = criar_persona(Papel.responsavel, criada_por=admin)
    guerreiro = criar_persona(Papel.guerreiro)
    criar_vinculo(responsavel_1, guerreiro, cadastrado_por=admin)
    criar_vinculo(responsavel_2, guerreiro, cadastrado_por=admin)
    token, _ = criar_sessao_de_teste(admin)
    cabecalhos = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}

    cliente.post(
        f"/v1/guerreiros/{guerreiro.id}/autorizacao/assistida",
        json={
            "responsavel_id": str(responsavel_1.id),
            "decisao": "concede",
            "testemunha_id": str(admin.id),
        },
        headers=cabecalhos,
    )
    cliente.post(
        f"/v1/guerreiros/{guerreiro.id}/autorizacao/assistida",
        json={
            "responsavel_id": str(responsavel_2.id),
            "decisao": "nega",
            "testemunha_id": str(admin.id),
        },
        headers=cabecalhos,
    )

    token_do_responsavel_1, _ = criar_sessao_de_teste(responsavel_1)
    resposta = cliente.get(
        f"/v1/eu/guerreiros/{guerreiro.id}/autorizacao",
        headers={
            "X-Chave-Aplicacao": chave,
            "Authorization": f"Bearer {token_do_responsavel_1}",
        },
    )
    corpo = resposta.json()
    assert corpo["estado"] == "suspensa"
    assert corpo["suspensa_por"]["responsavel_id"] == str(responsavel_2.id)


def test_quem_nao_e_admin_nem_mestre_nao_opera_o_ato_assistido(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_vinculo, sessao
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    responsavel = criar_persona(Papel.responsavel, criada_por=admin)
    outro_responsavel = criar_persona(Papel.responsavel, criada_por=admin)
    guerreiro = criar_persona(Papel.guerreiro)
    criar_vinculo(responsavel, guerreiro, cadastrado_por=admin)
    token, _ = criar_sessao_de_teste(outro_responsavel)

    resposta = cliente.post(
        f"/v1/guerreiros/{guerreiro.id}/autorizacao/assistida",
        json={
            "responsavel_id": str(responsavel.id),
            "decisao": "concede",
            "testemunha_id": str(outro_responsavel.id),
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 403
    assert sessao.query(Consentimento).count() == 0


def test_lista_de_responsaveis_sem_vinculo_encerrado_sem_credencial_e_sem_contato(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_vinculo
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    responsavel_vigente = criar_persona(Papel.responsavel, criada_por=admin)
    responsavel_encerrado = criar_persona(Papel.responsavel, criada_por=admin)
    guerreiro = criar_persona(Papel.guerreiro)
    criar_vinculo(responsavel_vigente, guerreiro, grau_de_parentesco="mãe", cadastrado_por=admin)
    criar_vinculo(
        responsavel_encerrado,
        guerreiro,
        grau_de_parentesco="pai",
        cadastrado_por=admin,
        fim=datetime.now(UTC),
    )
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.get(
        f"/v1/guerreiros/{guerreiro.id}/responsaveis",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 200
    corpo = resposta.json()
    assert len(corpo) == 1
    assert corpo[0]["id"] == str(responsavel_vigente.id)
    assert corpo[0]["grau_de_parentesco"] == "mãe"
    assert set(corpo[0].keys()) == {"id", "nome", "grau_de_parentesco"}


def test_outro_papel_nao_alcanca_a_lista_de_responsaveis(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    responsavel = criar_persona(Papel.responsavel)
    guerreiro = criar_persona(Papel.guerreiro)
    token, _ = criar_sessao_de_teste(responsavel)

    resposta = cliente.get(
        f"/v1/guerreiros/{guerreiro.id}/responsaveis",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 403
