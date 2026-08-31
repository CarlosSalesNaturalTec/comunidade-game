from nucleo.consentimentos.modelo import (
    Consentimento,
    DecisaoDeConsentimento,
    OrigemDoConsentimento,
    TipoDeConsentimento,
)
from nucleo.personas.modelo import Papel


def _admin_e_mestre(criar_persona):
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    return admin, mestre


def _corpo(responsavel_id, guerreiro_id, testemunha_id, tipo=TipoDeConsentimento.biometria.value):
    return {
        "responsavel_id": str(responsavel_id),
        "guerreiro_id": str(guerreiro_id),
        "tipo": tipo,
        "decisao": "concede",
        "origem": "impressa",
        "testemunha_id": str(testemunha_id),
    }


def test_mestre_registra_o_termo_assinado_no_encontro(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_vinculo
):
    chave, _ = criar_chave()
    admin, mestre = _admin_e_mestre(criar_persona)
    responsavel = criar_persona(Papel.responsavel, criada_por=admin)
    guerreiro = criar_persona(Papel.guerreiro)
    criar_vinculo(responsavel, guerreiro, cadastrado_por=admin)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.post(
        "/v1/consentimentos",
        json=_corpo(responsavel.id, guerreiro.id, mestre.id),
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 201
    corpo = resposta.json()
    assert "id" in corpo
    assert corpo["registrado_em"] is not None
    assert "+" in corpo["registrado_em"] or "Z" in corpo["registrado_em"]


def test_papel_sem_permissao_nao_registra_consentimento(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_vinculo, sessao
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador, criada_por=admin)
    responsavel = criar_persona(Papel.responsavel, criada_por=admin)
    guerreiro = criar_persona(Papel.guerreiro)
    criar_vinculo(responsavel, guerreiro, cadastrado_por=admin)
    token, _ = criar_sessao_de_teste(apoiador)

    resposta = cliente.post(
        "/v1/consentimentos",
        json=_corpo(responsavel.id, guerreiro.id, apoiador.id),
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 403
    assert sessao.query(Consentimento).count() == 0


def test_tipo_fora_do_conjunto_e_recusado_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_vinculo, sessao
):
    chave, _ = criar_chave()
    admin, mestre = _admin_e_mestre(criar_persona)
    responsavel = criar_persona(Papel.responsavel, criada_por=admin)
    guerreiro = criar_persona(Papel.guerreiro)
    criar_vinculo(responsavel, guerreiro, cadastrado_por=admin)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.post(
        "/v1/consentimentos",
        json=_corpo(responsavel.id, guerreiro.id, mestre.id, tipo="tipo_inventado"),
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 422
    assert sessao.query(Consentimento).count() == 0


def test_recusa_quando_nao_ha_vinculo_vigente(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, sessao
):
    chave, _ = criar_chave()
    admin, mestre = _admin_e_mestre(criar_persona)
    responsavel = criar_persona(Papel.responsavel, criada_por=admin)
    guerreiro_sem_vinculo = criar_persona(Papel.guerreiro)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.post(
        "/v1/consentimentos",
        json=_corpo(responsavel.id, guerreiro_sem_vinculo.id, mestre.id),
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 403
    assert sessao.query(Consentimento).count() == 0


def test_versao_vem_da_configuracao_e_nao_do_corpo(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_vinculo, sessao
):
    chave, _ = criar_chave()
    admin, mestre = _admin_e_mestre(criar_persona)
    responsavel = criar_persona(Papel.responsavel, criada_por=admin)
    guerreiro = criar_persona(Papel.guerreiro)
    criar_vinculo(responsavel, guerreiro, cadastrado_por=admin)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.post(
        "/v1/consentimentos",
        json=_corpo(responsavel.id, guerreiro.id, mestre.id),
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 201
    consentimento = sessao.get(Consentimento, resposta.json()["id"])
    assert consentimento.versao_do_termo == "2026-08"


def test_corpo_com_versao_do_termo_e_recusado(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_vinculo
):
    """`extra="forbid"` recusa quem tenta escolher a versão do termo pelo
    corpo — quem consome a API não determina a prova (design — decisão 2)."""
    chave, _ = criar_chave()
    admin, mestre = _admin_e_mestre(criar_persona)
    responsavel = criar_persona(Papel.responsavel, criada_por=admin)
    guerreiro = criar_persona(Papel.guerreiro)
    criar_vinculo(responsavel, guerreiro, cadastrado_por=admin)
    token, _ = criar_sessao_de_teste(mestre)

    corpo = _corpo(responsavel.id, guerreiro.id, mestre.id)
    corpo["versao_do_termo"] = "9999-99"
    resposta = cliente.post(
        "/v1/consentimentos",
        json=corpo,
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 422


def test_versao_trocada_nao_reescreve_o_passado(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_vinculo,
    sessao,
    sobrescrever_configuracao,
):
    chave, _ = criar_chave()
    admin, mestre = _admin_e_mestre(criar_persona)
    responsavel = criar_persona(Papel.responsavel, criada_por=admin)
    guerreiro = criar_persona(Papel.guerreiro)
    criar_vinculo(responsavel, guerreiro, cadastrado_por=admin)
    token, _ = criar_sessao_de_teste(mestre)
    cabecalhos = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}

    primeiro = cliente.post(
        "/v1/consentimentos",
        json=_corpo(responsavel.id, guerreiro.id, mestre.id),
        headers=cabecalhos,
    )
    assert primeiro.status_code == 201

    sobrescrever_configuracao(consentimento_versao_vigente_do_termo="2026-09")

    segundo = cliente.post(
        "/v1/consentimentos",
        json=_corpo(responsavel.id, guerreiro.id, mestre.id),
        headers=cabecalhos,
    )
    assert segundo.status_code == 201

    consentimento_antigo = sessao.get(Consentimento, primeiro.json()["id"])
    consentimento_novo = sessao.get(Consentimento, segundo.json()["id"])
    assert consentimento_antigo.versao_do_termo == "2026-08"
    assert consentimento_novo.versao_do_termo == "2026-09"


def _vinculo_do_responsavel(sessao, criar_persona, criar_vinculo, grau="mãe"):
    admin = criar_persona(Papel.admin)
    responsavel = criar_persona(Papel.responsavel, criada_por=admin)
    guerreiro = criar_persona(Papel.guerreiro)
    criar_vinculo(responsavel, guerreiro, grau_de_parentesco=grau, cadastrado_por=admin)
    return admin, responsavel, guerreiro


def test_responsavel_concede_a_autorizacao_do_vinculado(
    cliente, criar_chave, criar_persona, criar_vinculo, criar_sessao_de_teste, sessao
):
    chave, _ = criar_chave()
    _, responsavel, guerreiro = _vinculo_do_responsavel(sessao, criar_persona, criar_vinculo)
    token, _ = criar_sessao_de_teste(responsavel)

    resposta = cliente.post(
        f"/v1/eu/guerreiros/{guerreiro.id}/autorizacao",
        json={"decisao": "concede"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["decisao"] == "concede"
    assert corpo["estado"] == "vigente"
    consentimento = sessao.get(Consentimento, corpo["id"])
    assert consentimento.origem.value == "propria"
    assert consentimento.autor_id == responsavel.id


def test_responsavel_revoga_o_que_concedeu(
    cliente, criar_chave, criar_persona, criar_vinculo, criar_sessao_de_teste, sessao
):
    chave, _ = criar_chave()
    _, responsavel, guerreiro = _vinculo_do_responsavel(sessao, criar_persona, criar_vinculo)
    token, _ = criar_sessao_de_teste(responsavel)
    cabecalhos = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}

    cliente.post(
        f"/v1/eu/guerreiros/{guerreiro.id}/autorizacao",
        json={"decisao": "concede"},
        headers=cabecalhos,
    )
    resposta = cliente.post(
        f"/v1/eu/guerreiros/{guerreiro.id}/autorizacao",
        json={"decisao": "nega"},
        headers=cabecalhos,
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["decisao"] == "nega"
    assert corpo["estado"] == "nao_autorizada"


def test_decidir_autorizacao_sem_vinculo_e_recusado(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, sessao
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    responsavel = criar_persona(Papel.responsavel, criada_por=admin)
    guerreiro_sem_vinculo = criar_persona(Papel.guerreiro)
    token, _ = criar_sessao_de_teste(responsavel)

    resposta = cliente.post(
        f"/v1/eu/guerreiros/{guerreiro_sem_vinculo.id}/autorizacao",
        json={"decisao": "concede"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 403
    assert sessao.query(Consentimento).count() == 0


def test_decidir_autorizacao_recusado_para_outro_papel(
    cliente, criar_chave, criar_persona, criar_vinculo, criar_sessao_de_teste, sessao
):
    chave, _ = criar_chave()
    admin, _, guerreiro = _vinculo_do_responsavel(sessao, criar_persona, criar_vinculo)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.post(
        f"/v1/eu/guerreiros/{guerreiro.id}/autorizacao",
        json={"decisao": "concede"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 403
    assert sessao.query(Consentimento).count() == 0


def test_decisao_do_responsavel_carrega_a_versao_vigente(
    cliente, criar_chave, criar_persona, criar_vinculo, criar_sessao_de_teste, sessao
):
    chave, _ = criar_chave()
    _, responsavel, guerreiro = _vinculo_do_responsavel(sessao, criar_persona, criar_vinculo)
    token, _ = criar_sessao_de_teste(responsavel)

    resposta = cliente.post(
        f"/v1/eu/guerreiros/{guerreiro.id}/autorizacao",
        json={"decisao": "concede", "versao_do_termo": "9999-99"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 422


def test_conceder_divulgacao_nao_concede_biometria(
    cliente, criar_chave, criar_persona, criar_vinculo, criar_sessao_de_teste, sessao
):
    chave, _ = criar_chave()
    _, responsavel, guerreiro = _vinculo_do_responsavel(sessao, criar_persona, criar_vinculo)
    token, _ = criar_sessao_de_teste(responsavel)

    cliente.post(
        f"/v1/eu/guerreiros/{guerreiro.id}/autorizacao",
        json={"decisao": "concede"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert (
        sessao.query(Consentimento)
        .filter_by(guerreiro_id=guerreiro.id, tipo=TipoDeConsentimento.biometria)
        .count()
        == 0
    )


def test_leitura_com_historico_ordenado(
    cliente, criar_chave, criar_persona, criar_vinculo, criar_sessao_de_teste, sessao
):
    chave, _ = criar_chave()
    _, responsavel, guerreiro = _vinculo_do_responsavel(sessao, criar_persona, criar_vinculo)
    token, _ = criar_sessao_de_teste(responsavel)
    cabecalhos = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}

    cliente.post(
        f"/v1/eu/guerreiros/{guerreiro.id}/autorizacao",
        json={"decisao": "concede"},
        headers=cabecalhos,
    )
    cliente.post(
        f"/v1/eu/guerreiros/{guerreiro.id}/autorizacao",
        json={"decisao": "nega"},
        headers=cabecalhos,
    )
    cliente.post(
        f"/v1/eu/guerreiros/{guerreiro.id}/autorizacao",
        json={"decisao": "concede"},
        headers=cabecalhos,
    )

    resposta = cliente.get(f"/v1/eu/guerreiros/{guerreiro.id}/autorizacao", headers=cabecalhos)

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["estado"] == "vigente"
    assert corpo["suspensa_por"] is None
    assert len(corpo["historico"]) == 3
    decisoes = [item["decisao"] for item in corpo["historico"]]
    assert decisoes == ["concede", "nega", "concede"]
    assert all(item["versao_do_termo"] == "2026-08" for item in corpo["historico"])


def test_leitura_do_estado_suspenso_nomeia_quem_recusou(
    cliente, criar_chave, criar_persona, criar_vinculo, criar_sessao_de_teste, sessao
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    responsavel_a = criar_persona(Papel.responsavel, criada_por=admin)
    responsavel_b = criar_persona(Papel.responsavel, criada_por=admin)
    guerreiro = criar_persona(Papel.guerreiro)
    criar_vinculo(responsavel_a, guerreiro, grau_de_parentesco="mãe", cadastrado_por=admin)
    criar_vinculo(responsavel_b, guerreiro, grau_de_parentesco="pai", cadastrado_por=admin)

    token_a, _ = criar_sessao_de_teste(responsavel_a)
    cliente.post(
        f"/v1/eu/guerreiros/{guerreiro.id}/autorizacao",
        json={"decisao": "concede"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token_a}"},
    )

    token_b, _ = criar_sessao_de_teste(responsavel_b)
    cliente.post(
        f"/v1/eu/guerreiros/{guerreiro.id}/autorizacao",
        json={"decisao": "nega"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token_b}"},
    )

    resposta = cliente.get(
        f"/v1/eu/guerreiros/{guerreiro.id}/autorizacao",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token_a}"},
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["estado"] == "suspensa"
    assert corpo["suspensa_por"]["responsavel_id"] == str(responsavel_b.id)


def test_leitura_com_historico_vazio(
    cliente, criar_chave, criar_persona, criar_vinculo, criar_sessao_de_teste, sessao
):
    chave, _ = criar_chave()
    _, responsavel, guerreiro = _vinculo_do_responsavel(sessao, criar_persona, criar_vinculo)
    token, _ = criar_sessao_de_teste(responsavel)

    resposta = cliente.get(
        f"/v1/eu/guerreiros/{guerreiro.id}/autorizacao",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["estado"] == "nao_autorizada"
    assert corpo["historico"] == []


def test_leitura_nao_alcanca_biometria(
    cliente,
    criar_chave,
    criar_persona,
    criar_vinculo,
    criar_sessao_de_teste,
    criar_consentimento,
    sessao,
):
    chave, _ = criar_chave()
    admin, responsavel, guerreiro = _vinculo_do_responsavel(sessao, criar_persona, criar_vinculo)
    criar_consentimento(
        responsavel,
        guerreiro,
        tipo=TipoDeConsentimento.biometria,
        decisao=DecisaoDeConsentimento.concede,
        origem=OrigemDoConsentimento.impressa,
        operado_por=admin,
    )
    token, _ = criar_sessao_de_teste(responsavel)

    resposta = cliente.get(
        f"/v1/eu/guerreiros/{guerreiro.id}/autorizacao",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["estado"] == "nao_autorizada"
    assert corpo["historico"] == []


def test_leitura_recusada_sem_vinculo(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, sessao
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    responsavel = criar_persona(Papel.responsavel, criada_por=admin)
    guerreiro_sem_vinculo = criar_persona(Papel.guerreiro)
    token, _ = criar_sessao_de_teste(responsavel)

    resposta = cliente.get(
        f"/v1/eu/guerreiros/{guerreiro_sem_vinculo.id}/autorizacao",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 403
