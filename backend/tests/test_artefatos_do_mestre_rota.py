from nucleo.personas.modelo import ArtefatoComprobatorio, Papel


def test_mestre_publica_dois_artefatos_no_proprio_perfil(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    token, _ = criar_sessao_de_teste(mestre)
    cabecalhos = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}

    for endereco, rotulo in [
        ("https://exemplo.org/curriculo", "Currículo"),
        ("https://exemplo.org/portfolio", "Portfólio"),
    ]:
        resposta = cliente.post(
            f"/v1/mestres/{mestre.id}/artefatos",
            json={"endereco": endereco, "rotulo": rotulo},
            headers=cabecalhos,
        )
        assert resposta.status_code == 201
        assert resposta.json()["declarado_no_cadastro"] is False

    leitura = cliente.get(f"/v1/mestres/{mestre.id}/artefatos", headers=cabecalhos)
    assert leitura.status_code == 200
    assert len(leitura.json()) == 2


def test_artefato_sem_endereco_ou_sem_rotulo_e_recusado(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    token, _ = criar_sessao_de_teste(mestre)
    cabecalhos = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}

    sem_endereco = cliente.post(
        f"/v1/mestres/{mestre.id}/artefatos",
        json={"endereco": "", "rotulo": "Currículo"},
        headers=cabecalhos,
    )
    assert sem_endereco.status_code == 422

    sem_rotulo = cliente.post(
        f"/v1/mestres/{mestre.id}/artefatos",
        json={"endereco": "https://exemplo.org", "rotulo": ""},
        headers=cabecalhos,
    )
    assert sem_rotulo.status_code == 422


def test_mestre_nao_publica_no_perfil_de_outra_persona(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    outro_mestre = criar_persona(Papel.mestre, criada_por=admin)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.post(
        f"/v1/mestres/{outro_mestre.id}/artefatos",
        json={"endereco": "https://exemplo.org", "rotulo": "Currículo"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 403


def test_campo_de_cadastro_enviado_junto_e_recusado(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.post(
        f"/v1/mestres/{mestre.id}/artefatos",
        json={"endereco": "https://exemplo.org", "rotulo": "Currículo", "nome": "Outro nome"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 422


def test_persona_de_outro_papel_recebe_403_na_rota_de_artefatos(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador, criada_por=admin)
    token, _ = criar_sessao_de_teste(apoiador)

    resposta = cliente.post(
        f"/v1/mestres/{apoiador.id}/artefatos",
        json={"endereco": "https://exemplo.org", "rotulo": "Currículo"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 403


def test_mestre_remove_o_que_ele_mesmo_publicou(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    token, _ = criar_sessao_de_teste(mestre)
    cabecalhos = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}

    criado = cliente.post(
        f"/v1/mestres/{mestre.id}/artefatos",
        json={"endereco": "https://exemplo.org", "rotulo": "Currículo"},
        headers=cabecalhos,
    ).json()

    remocao = cliente.delete(
        f"/v1/mestres/{mestre.id}/artefatos/{criado['id']}", headers=cabecalhos
    )
    assert remocao.status_code == 204

    leitura = cliente.get(f"/v1/mestres/{mestre.id}/artefatos", headers=cabecalhos)
    assert leitura.json() == []


def test_artefato_declarado_por_admin_no_cadastro_nao_e_removido_pelo_mestre(
    sessao, cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    artefato_do_cadastro = ArtefatoComprobatorio(
        persona_id=mestre.id,
        endereco="https://exemplo.org/curriculo-do-cadastro",
        rotulo="Currículo do cadastro",
        declarado_por_id=admin.id,
    )
    sessao.add(artefato_do_cadastro)
    sessao.commit()
    token, _ = criar_sessao_de_teste(mestre)
    cabecalhos = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}

    leitura = cliente.get(f"/v1/mestres/{mestre.id}/artefatos", headers=cabecalhos)
    assert leitura.status_code == 200
    (item,) = leitura.json()
    assert item["declarado_no_cadastro"] is True

    remocao = cliente.delete(
        f"/v1/mestres/{mestre.id}/artefatos/{artefato_do_cadastro.id}", headers=cabecalhos
    )
    assert remocao.status_code == 403

    leitura_apos = cliente.get(f"/v1/mestres/{mestre.id}/artefatos", headers=cabecalhos)
    assert len(leitura_apos.json()) == 1


def test_artefato_do_mestre_e_do_cadastro_seguem_publicos_com_as_colunas_novas_vazias(
    sessao, cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    """`anexado_por_id` e `anexado_em` nascem nulas para o legado do Mestre
    e o declarado por Admin no cadastro, e nenhum dos dois gira em torno
    delas: seguem públicos na leitura, sem gate algum de anexação — essa
    exigência é só do Apoiador (`RF-09-66`, `RN-14-12`, design — decisão
    5)."""
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)

    publicado_pelo_mestre = ArtefatoComprobatorio(
        persona_id=mestre.id,
        endereco="https://exemplo.org/curriculo",
        rotulo="Currículo",
        declarado_por_id=mestre.id,
    )
    declarado_no_cadastro = ArtefatoComprobatorio(
        persona_id=mestre.id,
        endereco="https://exemplo.org/curriculo-do-cadastro",
        rotulo="Currículo do cadastro",
        declarado_por_id=admin.id,
    )
    sessao.add_all([publicado_pelo_mestre, declarado_no_cadastro])
    sessao.commit()

    assert publicado_pelo_mestre.anexado_por_id is None
    assert publicado_pelo_mestre.anexado_em is None
    assert declarado_no_cadastro.anexado_por_id is None
    assert declarado_no_cadastro.anexado_em is None

    token, _ = criar_sessao_de_teste(mestre)
    leitura = cliente.get(
        f"/v1/mestres/{mestre.id}/artefatos",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert leitura.status_code == 200
    assert len(leitura.json()) == 2
