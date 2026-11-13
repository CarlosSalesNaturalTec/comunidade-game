from nucleo.personas.modelo import Papel
from nucleo.recursos.modelo import NaturezaDoRecurso


def test_admin_cadastra_tipo_de_recurso_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.post(
        "/v1/tipos-de-recurso",
        json={
            "nome": "Lanche",
            "natureza": NaturezaDoRecurso.consumivel.value,
            "unidade": "unidade",
            "valor_em_moedas": "1.50",
            "vigencia_inicio": "2026-01-01",
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["nome"] == "Lanche"
    assert corpo["natureza"] == NaturezaDoRecurso.consumivel.value
    assert corpo["valor_em_moedas"] == "1.50"
    assert corpo["vigencia_inicio"] == "2026-01-01"


def test_quem_nao_e_admin_recebe_403_ao_cadastrar_tipo_de_recurso(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.post(
        "/v1/tipos-de-recurso",
        json={
            "nome": "Lanche",
            "natureza": NaturezaDoRecurso.consumivel.value,
            "unidade": "unidade",
            "valor_em_moedas": "1.50",
            "vigencia_inicio": "2026-01-01",
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 403


def test_cadastro_de_tipo_de_recurso_sem_chave_e_recusado_com_401(
    cliente, criar_persona, criar_sessao_de_teste
):
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.post(
        "/v1/tipos-de-recurso",
        json={
            "nome": "Lanche",
            "natureza": NaturezaDoRecurso.consumivel.value,
            "unidade": "unidade",
            "valor_em_moedas": "1.50",
            "vigencia_inicio": "2026-01-01",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 401


def test_valor_negativo_e_recusado_com_422_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.post(
        "/v1/tipos-de-recurso",
        json={
            "nome": "Lanche",
            "natureza": NaturezaDoRecurso.consumivel.value,
            "unidade": "unidade",
            "valor_em_moedas": "-1.50",
            "vigencia_inicio": "2026-01-01",
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 422


def test_admin_le_o_catalogo_de_tipos_de_recurso(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    """Rota fora da proposal desta change — sem ela não há como montar o
    seletor de tipo de recurso da homologação do aporte (`RF-02-84`)."""
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    headers = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}

    cliente.post(
        "/v1/tipos-de-recurso",
        json={
            "nome": "Lanche",
            "natureza": NaturezaDoRecurso.consumivel.value,
            "unidade": "unidade",
            "valor_em_moedas": "1.50",
            "vigencia_inicio": "2026-01-01",
        },
        headers=headers,
    )
    cliente.post(
        "/v1/tipos-de-recurso",
        json={
            "nome": "Cloud",
            "natureza": NaturezaDoRecurso.financeiro.value,
            "unidade": "mês",
            "valor_em_moedas": "40.00",
            "vigencia_inicio": "2026-01-01",
        },
        headers=headers,
    )

    resposta = cliente.get("/v1/tipos-de-recurso", headers=headers)

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert [item["nome"] for item in corpo] == ["Cloud", "Lanche"]
    assert corpo[0]["valor_em_moedas"] == "40.00"


def test_mestre_le_o_catalogo_de_tipos_de_recurso(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    headers_admin = {"X-Chave-Aplicacao": chave}
    token_admin, _ = criar_sessao_de_teste(admin)
    headers_admin["Authorization"] = f"Bearer {token_admin}"

    cliente.post(
        "/v1/tipos-de-recurso",
        json={
            "nome": "Lanche",
            "natureza": NaturezaDoRecurso.consumivel.value,
            "unidade": "unidade",
            "valor_em_moedas": "1.50",
            "vigencia_inicio": "2026-01-01",
        },
        headers=headers_admin,
    )

    mestre = criar_persona(Papel.mestre, criada_por=admin)
    token_mestre, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.get(
        "/v1/tipos-de-recurso",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token_mestre}"},
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo[0]["nome"] == "Lanche"
    assert corpo[0]["natureza"] == NaturezaDoRecurso.consumivel.value
    assert "exige_comprovante" in corpo[0]


def test_quem_nao_e_admin_nem_mestre_recebe_403_ao_ler_o_catalogo(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador, criada_por=admin)
    token, _ = criar_sessao_de_teste(apoiador)

    resposta = cliente.get(
        "/v1/tipos-de-recurso",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 403


def test_leitura_do_catalogo_sem_chave_e_recusada_com_401(
    cliente, criar_persona, criar_sessao_de_teste
):
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.get(
        "/v1/tipos-de-recurso",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 401


# --- Rotas de edição, vigência, desativação e exclusão (`RF-07-51`, `RF-07-52`,
# `RN-07-40`, `RF-07-02`) ---

import uuid  # noqa: E402
from datetime import date  # noqa: E402

import pytest  # noqa: E402


@pytest.fixture
def admin_na_rota(cliente, criar_chave, criar_persona, criar_sessao_de_teste):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    return admin, {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}


def _tipo_com_valor(admin, criar_tipo_de_recurso, criar_valor_de_referencia):
    tipo = criar_tipo_de_recurso(admin)
    criar_valor_de_referencia(admin, tipo, vigencia_inicio=date(2026, 1, 1))
    return tipo


def test_admin_altera_o_tipo_pela_rota(
    cliente, admin_na_rota, criar_tipo_de_recurso, criar_valor_de_referencia
):
    admin, cabecalhos = admin_na_rota
    tipo = _tipo_com_valor(admin, criar_tipo_de_recurso, criar_valor_de_referencia)

    resposta = cliente.patch(
        f"/v1/tipos-de-recurso/{tipo.id}",
        json={"nome": "Lanche da tarde", "exige_comprovante": True},
        headers=cabecalhos,
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["nome"] == "Lanche da tarde"
    assert corpo["unidade"] == "unidade"
    assert corpo["exige_comprovante"] is True
    assert corpo["ativo"] is True


def test_natureza_na_alteracao_e_recusada_com_422(cliente, admin_na_rota, criar_tipo_de_recurso):
    admin, cabecalhos = admin_na_rota
    tipo = criar_tipo_de_recurso(admin)

    resposta = cliente.patch(
        f"/v1/tipos-de-recurso/{tipo.id}", json={"natureza": "servico"}, headers=cabecalhos
    )

    assert resposta.status_code == 422
    assert resposta.json()["campo"] == "natureza"


def test_tipo_inexistente_responde_404(cliente, admin_na_rota):
    _, cabecalhos = admin_na_rota
    id_qualquer = uuid.uuid4()

    assert (
        cliente.patch(
            f"/v1/tipos-de-recurso/{id_qualquer}", json={"nome": "X"}, headers=cabecalhos
        ).status_code
        == 404
    )
    assert (
        cliente.delete(f"/v1/tipos-de-recurso/{id_qualquer}", headers=cabecalhos).status_code == 404
    )
    assert (
        cliente.post(
            f"/v1/tipos-de-recurso/{id_qualquer}/desativacao", headers=cabecalhos
        ).status_code
        == 404
    )


def test_mestre_recebe_403_nas_escritas_novas(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_tipo_de_recurso
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    token, _ = criar_sessao_de_teste(mestre)
    cabecalhos = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}
    tipo = criar_tipo_de_recurso(admin)
    base = f"/v1/tipos-de-recurso/{tipo.id}"

    assert cliente.patch(base, json={"nome": "X"}, headers=cabecalhos).status_code == 403
    assert cliente.post(f"{base}/desativacao", headers=cabecalhos).status_code == 403
    assert cliente.post(f"{base}/reativacao", headers=cabecalhos).status_code == 403
    assert cliente.delete(base, headers=cabecalhos).status_code == 403
    assert (
        cliente.post(
            f"{base}/valores-de-referencia",
            json={"valor_em_moedas": "2.00", "vigencia_inicio": "2026-02-01"},
            headers=cabecalhos,
        ).status_code
        == 403
    )


def test_vigencia_nova_do_valor_encerra_a_anterior(
    cliente, sessao, admin_na_rota, criar_tipo_de_recurso, criar_valor_de_referencia
):
    admin, cabecalhos = admin_na_rota
    tipo = criar_tipo_de_recurso(admin)
    anterior = criar_valor_de_referencia(admin, tipo, vigencia_inicio=date(2026, 1, 1))

    resposta = cliente.post(
        f"/v1/tipos-de-recurso/{tipo.id}/valores-de-referencia",
        json={"valor_em_moedas": "2.50", "vigencia_inicio": "2026-03-01"},
        headers=cabecalhos,
    )

    assert resposta.status_code == 201
    assert resposta.json()["valor_em_moedas"] == "2.50"
    sessao.refresh(anterior)
    assert anterior.vigencia_fim == date(2026, 3, 1)


def test_valor_com_tres_casas_e_recusado_e_a_anterior_segue_aberta(
    cliente, sessao, admin_na_rota, criar_tipo_de_recurso, criar_valor_de_referencia
):
    admin, cabecalhos = admin_na_rota
    tipo = criar_tipo_de_recurso(admin)
    anterior = criar_valor_de_referencia(admin, tipo)

    resposta = cliente.post(
        f"/v1/tipos-de-recurso/{tipo.id}/valores-de-referencia",
        json={"valor_em_moedas": "2.555", "vigencia_inicio": "2026-03-01"},
        headers=cabecalhos,
    )

    assert resposta.status_code == 422
    sessao.refresh(anterior)
    assert anterior.vigencia_fim is None


def test_desativado_sai_assinalado_na_leitura_e_reativa(
    cliente, admin_na_rota, criar_tipo_de_recurso, criar_valor_de_referencia
):
    admin, cabecalhos = admin_na_rota
    tipo = _tipo_com_valor(admin, criar_tipo_de_recurso, criar_valor_de_referencia)

    desativado = cliente.post(f"/v1/tipos-de-recurso/{tipo.id}/desativacao", headers=cabecalhos)
    assert desativado.status_code == 200 and desativado.json()["ativo"] is False

    lista = cliente.get("/v1/tipos-de-recurso", headers=cabecalhos).json()
    assert [item["ativo"] for item in lista if item["id"] == str(tipo.id)] == [False]

    reativado = cliente.post(f"/v1/tipos-de-recurso/{tipo.id}/reativacao", headers=cabecalhos)
    assert reativado.json()["ativo"] is True


def test_exclusao_do_nunca_usado_e_recusa_do_usado(
    cliente,
    admin_na_rota,
    criar_tipo_de_recurso,
    criar_valor_de_referencia,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_lancamento,
):
    admin, cabecalhos = admin_na_rota
    livre = _tipo_com_valor(admin, criar_tipo_de_recurso, criar_valor_de_referencia)
    usado = _tipo_com_valor(admin, criar_tipo_de_recurso, criar_valor_de_referencia)
    criar_lancamento(admin, usado, criar_ponto_de_apoio(admin, criar_comunidade()))

    assert cliente.delete(f"/v1/tipos-de-recurso/{livre.id}", headers=cabecalhos).status_code == 204

    recusa = cliente.delete(f"/v1/tipos-de-recurso/{usado.id}", headers=cabecalhos)
    assert recusa.status_code == 422
    assert recusa.json()["codigo"] == "tipo_em_uso"

    ids = {item["id"] for item in cliente.get("/v1/tipos-de-recurso", headers=cabecalhos).json()}
    assert str(livre.id) not in ids and str(usado.id) in ids
