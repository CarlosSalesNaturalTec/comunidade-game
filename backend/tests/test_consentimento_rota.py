from nucleo.consentimentos.modelo import Consentimento, TipoDeConsentimento
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
