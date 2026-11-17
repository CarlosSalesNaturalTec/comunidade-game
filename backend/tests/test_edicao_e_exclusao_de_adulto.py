"""Edição, exclusão, desativação e reativação de Mestre e Apoiador pela
gestão (`RF-02-117` a `RF-02-119`, `RN-02-34`, `RN-02-35`)."""

import uuid
from decimal import Decimal

from nucleo.aportes.modelo import FormaDeAporte
from nucleo.livro_razao.modelo import NaturezaDoLancamento
from nucleo.personas.modelo import ArtefatoComprobatorio, Credencial, Nick, Papel, Persona
from nucleo.sessoes.modelo import Sessao
from nucleo.sessoes.social import obter_verificador_social


def _verificador(app, email: str) -> None:
    app.dependency_overrides[obter_verificador_social] = lambda: lambda _token: email


def _cadastrar(cliente, cabecalhos, caminho="apoiadores", email="apoia@example.org"):
    resposta = cliente.post(
        f"/v1/{caminho}",
        json={
            "nome": "Fulana",
            "email": email,
            "artefatos": [{"endereco": "https://exemplo.org/a", "rotulo": "Portfólio"}],
        },
        headers=cabecalhos,
    )
    assert resposta.status_code == 201, resposta.text
    return resposta.json()


def _admin(criar_chave, criar_persona, criar_sessao_de_teste):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    return admin, chave, {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}


def _aportar(
    criar_lancamento,
    criar_aporte,
    criar_ponto_de_apoio,
    criar_comunidade,
    criar_tipo_de_recurso,
    *,
    admin,
    apoiador,
):
    ponto = criar_ponto_de_apoio(admin, criar_comunidade())
    tipo = criar_tipo_de_recurso(admin)
    credito = criar_lancamento(
        admin,
        tipo,
        ponto,
        natureza=NaturezaDoLancamento.credito,
        quantidade=Decimal("1.00"),
        valor_em_moedas=Decimal("12.00"),
    )
    return criar_aporte(
        admin,
        apoiador,
        tipo,
        ponto,
        credito,
        quantidade=Decimal("1.00"),
        valor_em_moedas=Decimal("12.00"),
        forma=FormaDeAporte.material,
    )


# --- Edição (`RF-02-117`) ------------------------------------------------------


def test_admin_troca_o_email_e_o_login_segue_o_novo(
    cliente, app, criar_chave, criar_persona, criar_sessao_de_teste
):
    _, chave, cabecalhos = _admin(criar_chave, criar_persona, criar_sessao_de_teste)
    apoiador = _cadastrar(cliente, cabecalhos)

    resposta = cliente.patch(
        f"/v1/apoiadores/{apoiador['id']}",
        json={"email": "novo@example.org", "whatsapp": "71999990000"},
        headers=cabecalhos,
    )
    assert resposta.status_code == 200, resposta.text
    corpo = resposta.json()
    assert corpo["email"] == "novo@example.org"
    assert corpo["whatsapp"] == "71999990000"
    assert corpo["nome"] == "Fulana"
    assert corpo["ativo"] is True

    _verificador(app, "novo@example.org")
    entrada = cliente.post(
        "/v1/sessoes/social", json={"id_token": "x"}, headers={"X-Chave-Aplicacao": chave}
    )
    assert entrada.status_code == 201
    _verificador(app, "apoia@example.org")
    antigo = cliente.post(
        "/v1/sessoes/social", json={"id_token": "x"}, headers={"X-Chave-Aplicacao": chave}
    )
    assert antigo.status_code != 201


def test_email_de_outra_pessoa_e_recusado(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    _, _, cabecalhos = _admin(criar_chave, criar_persona, criar_sessao_de_teste)
    _cadastrar(cliente, cabecalhos, caminho="mestres", email="mestre@example.org")
    apoiador = _cadastrar(cliente, cabecalhos)

    resposta = cliente.patch(
        f"/v1/apoiadores/{apoiador['id']}", json={"email": "mestre@example.org"}, headers=cabecalhos
    )
    assert resposta.status_code == 422
    leitura = cliente.get("/v1/apoiadores", headers=cabecalhos).json()["itens"]
    assert next(i for i in leitura if i["id"] == apoiador["id"])["email"] == "apoia@example.org"


def test_nick_no_corpo_e_recusado(cliente, criar_chave, criar_persona, criar_sessao_de_teste):
    _, _, cabecalhos = _admin(criar_chave, criar_persona, criar_sessao_de_teste)
    apoiador = _cadastrar(cliente, cabecalhos)

    resposta = cliente.patch(
        f"/v1/apoiadores/{apoiador['id']}", json={"nick": "outro"}, headers=cabecalhos
    )
    assert resposta.status_code == 422


def test_ultimo_artefato_nao_sai_e_o_segundo_sai(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    _, _, cabecalhos = _admin(criar_chave, criar_persona, criar_sessao_de_teste)
    mestre = _cadastrar(cliente, cabecalhos, caminho="mestres", email="m@example.org")
    unico = mestre["artefatos"][0]["id"]

    recusa = cliente.delete(
        f"/v1/mestres/{mestre['id']}/artefatos-da-gestao/{unico}", headers=cabecalhos
    )
    assert recusa.status_code == 422

    incluido = cliente.post(
        f"/v1/mestres/{mestre['id']}/artefatos-da-gestao",
        json={"endereco": "https://exemplo.org/b", "rotulo": "Currículo"},
        headers=cabecalhos,
    )
    assert incluido.status_code == 201
    assert len(incluido.json()["artefatos"]) == 2

    removido = cliente.delete(
        f"/v1/mestres/{mestre['id']}/artefatos-da-gestao/{unico}", headers=cabecalhos
    )
    assert removido.status_code == 200
    assert [a["rotulo"] for a in removido.json()["artefatos"]] == ["Currículo"]


def test_correcao_do_admin_preserva_o_original_do_mestre(
    cliente, sessao, criar_chave, criar_persona, criar_sessao_de_teste
):
    _, _, cabecalhos = _admin(criar_chave, criar_persona, criar_sessao_de_teste)
    mestre = _cadastrar(cliente, cabecalhos, caminho="mestres", email="m@example.org")
    artefato = sessao.get(ArtefatoComprobatorio, uuid.UUID(mestre["artefatos"][0]["id"]))
    artefato.endereco_original = "https://exemplo.org/a"
    artefato.rotulo_original = "Portfólio"
    artefato.endereco = "https://exemplo.org/editado"
    sessao.commit()

    resposta = cliente.patch(
        f"/v1/mestres/{mestre['id']}/artefatos-da-gestao/{artefato.id}",
        json={"endereco": "https://exemplo.org/corrigido", "rotulo": "Portfólio novo"},
        headers=cabecalhos,
    )
    assert resposta.status_code == 200
    saida = resposta.json()["artefatos"][0]
    assert saida["endereco"] == "https://exemplo.org/corrigido"
    assert saida["endereco_original"] == "https://exemplo.org/a"


def test_quem_nao_e_admin_nao_altera(cliente, criar_chave, criar_persona, criar_sessao_de_teste):
    _, chave, cabecalhos = _admin(criar_chave, criar_persona, criar_sessao_de_teste)
    apoiador = _cadastrar(cliente, cabecalhos)
    mestre = criar_persona(Papel.mestre)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.patch(
        f"/v1/apoiadores/{apoiador['id']}",
        json={"nome": "Outro"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 403


def test_papel_trocado_responde_404(cliente, criar_chave, criar_persona, criar_sessao_de_teste):
    _, _, cabecalhos = _admin(criar_chave, criar_persona, criar_sessao_de_teste)
    apoiador = _cadastrar(cliente, cabecalhos)

    resposta = cliente.patch(
        f"/v1/mestres/{apoiador['id']}", json={"nome": "Outro"}, headers=cabecalhos
    )
    assert resposta.status_code == 404


# --- Exclusão (`RF-02-118`, `RN-02-34`) ---------------------------------------


def test_cadastro_nunca_usado_e_excluido(
    cliente, sessao, criar_chave, criar_persona, criar_sessao_de_teste, criar_nick
):
    _, _, cabecalhos = _admin(criar_chave, criar_persona, criar_sessao_de_teste)
    apoiador = _cadastrar(cliente, cabecalhos)
    persona = sessao.get(Persona, uuid.UUID(apoiador["id"]))
    criar_nick(persona, "apoia_engano")
    criar_sessao_de_teste(persona, origem="app-08-apoiador")

    resposta = cliente.delete(f"/v1/apoiadores/{apoiador['id']}", headers=cabecalhos)
    assert resposta.status_code == 204
    sessao.expire_all()
    pid = uuid.UUID(apoiador["id"])
    assert sessao.get(Persona, pid) is None
    for modelo in (Nick, Credencial, Sessao, ArtefatoComprobatorio):
        assert sessao.query(modelo).filter_by(persona_id=pid).count() == 0


def test_apoiador_com_aporte_nao_e_excluido(
    cliente,
    sessao,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_lancamento,
    criar_aporte,
    criar_ponto_de_apoio,
    criar_comunidade,
    criar_tipo_de_recurso,
):
    admin, _, cabecalhos = _admin(criar_chave, criar_persona, criar_sessao_de_teste)
    apoiador = _cadastrar(cliente, cabecalhos)
    persona = sessao.get(Persona, uuid.UUID(apoiador["id"]))
    _aportar(
        criar_lancamento,
        criar_aporte,
        criar_ponto_de_apoio,
        criar_comunidade,
        criar_tipo_de_recurso,
        admin=admin,
        apoiador=persona,
    )

    resposta = cliente.delete(f"/v1/apoiadores/{apoiador['id']}", headers=cabecalhos)
    assert resposta.status_code == 422
    assert resposta.json()["codigo"] == "adulto_em_uso"
    sessao.expire_all()
    assert sessao.get(Persona, persona.id) is not None


def test_mestre_com_trilha_nao_e_excluido(
    cliente, sessao, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha
):
    _, _, cabecalhos = _admin(criar_chave, criar_persona, criar_sessao_de_teste)
    mestre = _cadastrar(cliente, cabecalhos, caminho="mestres", email="m@example.org")
    criar_trilha(sessao.get(Persona, uuid.UUID(mestre["id"])))

    resposta = cliente.delete(f"/v1/mestres/{mestre['id']}", headers=cabecalhos)
    assert resposta.status_code == 422


# --- Desativação e reativação (`RF-02-119`, `RN-02-35`) -----------------------


def test_desativado_perde_acesso_e_vitrine_e_reativado_volta(
    cliente,
    app,
    sessao,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_nick,
    criar_lancamento,
    criar_aporte,
    criar_ponto_de_apoio,
    criar_comunidade,
    criar_tipo_de_recurso,
):
    admin, chave, cabecalhos = _admin(criar_chave, criar_persona, criar_sessao_de_teste)
    apoiador = _cadastrar(cliente, cabecalhos)
    persona = sessao.get(Persona, uuid.UUID(apoiador["id"]))
    criar_nick(persona, "apoia_norte")
    aporte = _aportar(
        criar_lancamento,
        criar_aporte,
        criar_ponto_de_apoio,
        criar_comunidade,
        criar_tipo_de_recurso,
        admin=admin,
        apoiador=persona,
    )
    token_do_apoiador, _ = criar_sessao_de_teste(persona, origem="app-08-apoiador")
    publico = {"X-Chave-Aplicacao": chave}
    assert cliente.get(f"/v1/vitrine/apoiadores/{persona.id}", headers=publico).status_code == 200

    desativado = cliente.post(f"/v1/apoiadores/{persona.id}/desativacao", headers=cabecalhos)
    assert desativado.status_code == 200
    assert desativado.json()["ativo"] is False

    eu = cliente.get(
        "/v1/eu",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token_do_apoiador}"},
    )
    assert eu.status_code == 401
    _verificador(app, "apoia@example.org")
    login = cliente.post("/v1/sessoes/social", json={"id_token": "x"}, headers=publico)
    assert login.status_code != 201

    ids = {i["id"] for i in cliente.get("/v1/vitrine/apoiadores", headers=publico).json()["itens"]}
    assert str(persona.id) not in ids
    pagina = cliente.get(f"/v1/vitrine/apoiadores/{persona.id}", headers=publico)
    inexistente = cliente.get(f"/v1/vitrine/apoiadores/{uuid.uuid4()}", headers=publico)
    assert pagina.status_code == 404
    assert pagina.json() == inexistente.json()

    sessao.expire_all()
    assert sessao.get(type(aporte), aporte.id) is not None
    lista = cliente.get("/v1/apoiadores", headers=cabecalhos).json()["itens"]
    assert next(i for i in lista if i["id"] == str(persona.id))["ativo"] is False

    reativado = cliente.post(f"/v1/apoiadores/{persona.id}/reativacao", headers=cabecalhos)
    assert reativado.status_code == 200
    assert reativado.json()["ativo"] is True
    assert (
        cliente.post("/v1/sessoes/social", json={"id_token": "x"}, headers=publico).status_code
        == 201
    )
    assert cliente.get(f"/v1/vitrine/apoiadores/{persona.id}", headers=publico).status_code == 200


def test_mestre_desativado_sai_da_vitrine(
    cliente, sessao, criar_chave, criar_persona, criar_sessao_de_teste
):
    _, chave, cabecalhos = _admin(criar_chave, criar_persona, criar_sessao_de_teste)
    mestre = _cadastrar(cliente, cabecalhos, caminho="mestres", email="m@example.org")
    publico = {"X-Chave-Aplicacao": chave}
    assert cliente.get(f"/v1/vitrine/mestres/{mestre['id']}", headers=publico).status_code == 200

    cliente.post(f"/v1/mestres/{mestre['id']}/desativacao", headers=cabecalhos)

    assert cliente.get(f"/v1/vitrine/mestres/{mestre['id']}", headers=publico).status_code == 404
    ids = {i["id"] for i in cliente.get("/v1/vitrine/mestres", headers=publico).json()["itens"]}
    assert mestre["id"] not in ids
