from datetime import timedelta

import pytest

from nucleo.chaves.modelo import ChaveDeAplicacao, NaturezaDaChave, SituacaoDaChave
from nucleo.chaves.segredo import decompor_chave
from nucleo.fila.modelo import SituacaoDaSolicitacao, SolicitacaoDeChave
from nucleo.personas.modelo import Papel
from nucleo.tempo import agora

# --- Emissão (RF-01-50) ---------------------------------------------------


def test_admin_emite_chave_sobre_solicitacao_aprovada(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_solicitacao_de_chave, sessao
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    solicitacao = criar_solicitacao_de_chave()

    resposta = cliente.post(
        "/v1/chaves",
        json={"solicitacao_id": str(solicitacao.id)},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert set(corpo.keys()) == {"id", "segredo"}
    ambiente, id_bruto, _ = decompor_chave(corpo["segredo"])
    assert ambiente == "producao"
    assert id_bruto == corpo["id"]

    registro = sessao.get(ChaveDeAplicacao, corpo["id"])
    assert registro.natureza == NaturezaDaChave.de_terceiro
    assert registro.solicitacao_de_chave_id == solicitacao.id


@pytest.mark.parametrize("papel", [Papel.mestre, Papel.apoiador, Papel.responsavel])
def test_emissao_recusada_para_quem_nao_e_admin(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_solicitacao_de_chave,
    papel,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    outra_persona = criar_persona(papel, criada_por=admin)
    token, _ = criar_sessao_de_teste(outra_persona)
    solicitacao = criar_solicitacao_de_chave()

    resposta = cliente.post(
        "/v1/chaves",
        json={"solicitacao_id": str(solicitacao.id)},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 403
    assert resposta.json()["codigo"] == "permissao_negada"


def test_emissao_sobre_solicitacao_nao_aprovada_e_recusada(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_solicitacao_de_chave
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    solicitacao = criar_solicitacao_de_chave(situacao=SituacaoDaSolicitacao.recebida)

    resposta = cliente.post(
        "/v1/chaves",
        json={"solicitacao_id": str(solicitacao.id)},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 409
    assert resposta.json()["codigo"] == "solicitacao_de_chave_nao_disponivel_para_emissao"


def test_emissao_com_solicitacao_desconhecida_e_404(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.post(
        "/v1/chaves",
        json={"solicitacao_id": "11111111-1111-4111-8111-111111111111"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 404


# --- Apresentação da URL (RF-01-51) ---------------------------------------


def test_apresentar_url_e_publica_e_nao_confunde_a_chave_da_chamada(cliente, criar_chave, sessao):
    chave_da_vitrine, _ = criar_chave(aplicacao="app-06-vitrine")
    _, chave_de_terceiro = criar_chave(
        natureza=NaturezaDaChave.de_terceiro, prazo_de_apresentacao=agora() + timedelta(days=30)
    )

    resposta = cliente.post(
        f"/v1/chaves/{chave_de_terceiro.id}/url",
        json={"url": "https://exemplo.org/painel"},
        headers={"X-Chave-Aplicacao": chave_da_vitrine},
    )

    assert resposta.status_code == 204
    sessao.refresh(chave_de_terceiro)
    assert chave_de_terceiro.url_apresentada == "https://exemplo.org/painel"

    chave_da_vitrine_registro = (
        sessao.query(ChaveDeAplicacao)
        .filter_by(aplicacao="app-06-vitrine", natureza=NaturezaDaChave.do_projeto)
        .one()
    )
    assert chave_da_vitrine_registro.url_apresentada is None


def test_apresentacao_sem_credencial_de_persona_funciona(cliente, criar_chave):
    chave_da_vitrine, _ = criar_chave()
    _, chave_de_terceiro = criar_chave(
        natureza=NaturezaDaChave.de_terceiro, prazo_de_apresentacao=agora() + timedelta(days=30)
    )

    resposta = cliente.post(
        f"/v1/chaves/{chave_de_terceiro.id}/url",
        json={"url": "https://exemplo.org/painel"},
        headers={"X-Chave-Aplicacao": chave_da_vitrine},
    )

    assert resposta.status_code == 204


def test_apresentacao_fora_do_prazo_traz_orientacao_em_linguagem_simples(cliente, criar_chave):
    chave_da_vitrine, _ = criar_chave()
    _, chave_de_terceiro = criar_chave(
        natureza=NaturezaDaChave.de_terceiro, prazo_de_apresentacao=agora() - timedelta(seconds=1)
    )

    resposta = cliente.post(
        f"/v1/chaves/{chave_de_terceiro.id}/url",
        json={"url": "https://exemplo.org/painel"},
        headers={"X-Chave-Aplicacao": chave_da_vitrine},
    )

    assert resposta.status_code == 422
    assert "nova chave" in resposta.json()["mensagem"]


# --- Revogação (RF-01-52, RF-01-53) ---------------------------------------


def test_chamada_seguinte_ao_vencimento_recebe_401_identico_a_chave_inexistente(
    cliente, criar_chave
):
    chave_vencida, _ = criar_chave(
        natureza=NaturezaDaChave.de_terceiro, prazo_de_apresentacao=agora() - timedelta(seconds=1)
    )

    resposta_com_chave_vencida = cliente.get(
        "/v1/publica", headers={"X-Chave-Aplicacao": chave_vencida}
    )
    resposta_sem_chave = cliente.get("/v1/publica")

    assert resposta_com_chave_vencida.status_code == 401
    assert resposta_sem_chave.status_code == 401
    assert resposta_com_chave_vencida.json() == resposta_sem_chave.json()


def test_admin_revoga_chave_com_motivo_e_autoria(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, sessao
):
    chave_da_vitrine, _ = criar_chave()
    _, chave_de_terceiro = criar_chave(natureza=NaturezaDaChave.de_terceiro)
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.request(
        "DELETE",
        f"/v1/chaves/{chave_de_terceiro.id}",
        json={"motivo": "Uso indevido detectado."},
        headers={"X-Chave-Aplicacao": chave_da_vitrine, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 204
    sessao.refresh(chave_de_terceiro)
    assert chave_de_terceiro.situacao == SituacaoDaChave.revogada
    assert chave_de_terceiro.motivo_da_revogacao == "Uso indevido detectado."
    assert chave_de_terceiro.revogada_por == str(admin.id)
    assert chave_de_terceiro.revogada_em is not None


def test_revogacao_sem_motivo_e_recusada_e_chave_permanece_vigente(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, sessao
):
    chave_da_vitrine, _ = criar_chave()
    _, chave_de_terceiro = criar_chave(natureza=NaturezaDaChave.de_terceiro)
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.request(
        "DELETE",
        f"/v1/chaves/{chave_de_terceiro.id}",
        json={"motivo": ""},
        headers={"X-Chave-Aplicacao": chave_da_vitrine, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 422
    sessao.refresh(chave_de_terceiro)
    assert chave_de_terceiro.situacao == SituacaoDaChave.vigente


@pytest.mark.parametrize("papel", [Papel.mestre, Papel.apoiador, Papel.responsavel])
def test_revogacao_recusada_para_quem_nao_e_admin(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, papel
):
    chave_da_vitrine, _ = criar_chave()
    _, chave_de_terceiro = criar_chave(natureza=NaturezaDaChave.de_terceiro)
    admin = criar_persona(Papel.admin)
    outra_persona = criar_persona(papel, criada_por=admin)
    token, _ = criar_sessao_de_teste(outra_persona)

    resposta = cliente.request(
        "DELETE",
        f"/v1/chaves/{chave_de_terceiro.id}",
        json={"motivo": "Qualquer motivo."},
        headers={"X-Chave-Aplicacao": chave_da_vitrine, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 403


def test_revogacao_de_chave_desconhecida_e_404(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave_da_vitrine, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.request(
        "DELETE",
        "/v1/chaves/11111111-1111-4111-8111-111111111111",
        json={"motivo": "Qualquer motivo."},
        headers={"X-Chave-Aplicacao": chave_da_vitrine, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 404


# --- Leitura de gestão (RF-01-53) ------------------------------------------


def test_leitura_de_gestao_responde_no_formato_de_paginacao(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave_da_vitrine, _ = criar_chave()
    criar_chave(natureza=NaturezaDaChave.de_terceiro)
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.get(
        "/v1/chaves",
        headers={"X-Chave-Aplicacao": chave_da_vitrine, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert set(corpo.keys()) == {"itens", "proximo_cursor"}
    assert len(corpo["itens"]) >= 1
    item = corpo["itens"][0]
    assert set(item.keys()) == {
        "id",
        "aplicacao",
        "natureza",
        "ambiente",
        "prazo_de_apresentacao",
        "url_apresentada",
        "situacao",
    }


def test_leitura_de_gestao_pagina_com_cursor(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, sobrescrever_configuracao
):
    chave_da_vitrine, _ = criar_chave()
    criar_chave(natureza=NaturezaDaChave.de_terceiro, aplicacao="dev-1")
    criar_chave(natureza=NaturezaDaChave.de_terceiro, aplicacao="dev-2")
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    sobrescrever_configuracao(paginacao_tamanho_padrao=1)
    headers = {"X-Chave-Aplicacao": chave_da_vitrine, "Authorization": f"Bearer {token}"}

    primeira_pagina = cliente.get("/v1/chaves", headers=headers)
    assert len(primeira_pagina.json()["itens"]) == 1
    cursor = primeira_pagina.json()["proximo_cursor"]
    assert cursor is not None

    segunda_pagina = cliente.get("/v1/chaves", params={"cursor": cursor}, headers=headers)
    assert len(segunda_pagina.json()["itens"]) == 1
    assert segunda_pagina.json()["itens"][0]["id"] != primeira_pagina.json()["itens"][0]["id"]


def test_leitura_de_gestao_com_cursor_invalido_e_422(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave_da_vitrine, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.get(
        "/v1/chaves",
        params={"cursor": "cursor-invalido"},
        headers={"X-Chave-Aplicacao": chave_da_vitrine, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 422


def test_leitura_de_gestao_nunca_devolve_o_segredo(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave_da_vitrine, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.get(
        "/v1/chaves",
        headers={"X-Chave-Aplicacao": chave_da_vitrine, "Authorization": f"Bearer {token}"},
    )

    assert "segredo" not in str(resposta.json()).lower()
    assert "resumo_do_segredo" not in str(resposta.json())


@pytest.mark.parametrize("papel", [Papel.mestre, Papel.apoiador, Papel.responsavel])
def test_leitura_de_gestao_recusada_para_quem_nao_e_admin(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, papel
):
    chave_da_vitrine, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    outra_persona = criar_persona(papel, criada_por=admin)
    token, _ = criar_sessao_de_teste(outra_persona)

    resposta = cliente.get(
        "/v1/chaves",
        headers={"X-Chave-Aplicacao": chave_da_vitrine, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 403


def test_chave_vencida_aparece_revogada_no_painel_mesmo_sem_chamar_de_novo(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, sessao
):
    chave_da_vitrine, _ = criar_chave()
    _, chave_vencida = criar_chave(
        natureza=NaturezaDaChave.de_terceiro, prazo_de_apresentacao=agora() - timedelta(seconds=1)
    )
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.get(
        "/v1/chaves",
        headers={"X-Chave-Aplicacao": chave_da_vitrine, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 200
    item = next(i for i in resposta.json()["itens"] if i["id"] == str(chave_vencida.id))
    assert item["situacao"] == "revogada"

    sessao.refresh(chave_vencida)
    assert chave_vencida.situacao == SituacaoDaChave.revogada
    assert chave_vencida.revogada_por is None


# --- Fila de avaliação (RF-01-49, RF-01-50) --------------------------------


def test_solicitacao_e_chave_ficam_consultaveis_juntas(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_solicitacao_de_chave, sessao
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    solicitacao = criar_solicitacao_de_chave()

    resposta = cliente.post(
        "/v1/chaves",
        json={"solicitacao_id": str(solicitacao.id)},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 201

    solicitacao_recarregada = sessao.get(SolicitacaoDeChave, solicitacao.id)
    chave_emitida = sessao.get(ChaveDeAplicacao, solicitacao_recarregada.chave_id)
    assert chave_emitida is not None
    assert chave_emitida.solicitacao_de_chave_id == solicitacao.id


# --- Ciclo completo pela fila (`RF-02-88`, `RF-02-89`) ---------------------


def _registrar_e_aprovar_solicitacao_de_chave(cliente, headers, *, situacao="aceita"):
    id_solicitacao = cliente.post(
        "/v1/solicitacoes-de-chave",
        json={
            "solicitante": "Desenvolvedora de Tal",
            "contato": "dev@example.org",
            "o_que_pretende_construir": "Um painel comunitário.",
        },
        headers={"X-Chave-Aplicacao": headers["X-Chave-Aplicacao"]},
    ).json()["id"]
    if situacao is not None:
        cliente.post(
            f"/v1/solicitacoes-de-chave/{id_solicitacao}/avaliacao",
            json={"situacao": situacao, "parecer": "Parecer do Admin."},
            headers=headers,
        )
    return id_solicitacao


def test_ciclo_completo_solicitacao_aprovacao_emissao_e_apresentacao(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    """Caminho de ponta a ponta que ninguém percorreu junto até esta fatia
    (design — Risks/Trade-offs): solicitação pública, aprovação pela rota
    nova da fila, emissão que devolve o segredo uma única vez e
    apresentação pública da URL."""
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    headers = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}

    id_solicitacao = _registrar_e_aprovar_solicitacao_de_chave(cliente, headers)

    emitida = cliente.post("/v1/chaves", json={"solicitacao_id": id_solicitacao}, headers=headers)
    assert emitida.status_code == 201
    corpo_emitido = emitida.json()
    assert set(corpo_emitido.keys()) == {"id", "segredo"}

    apresentada = cliente.post(
        f"/v1/chaves/{corpo_emitido['id']}/url",
        json={"url": "https://exemplo.org/painel"},
        headers={"X-Chave-Aplicacao": chave},
    )
    assert apresentada.status_code == 204


def test_aprovar_solicitacao_de_chave_pela_fila_nao_emite(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    headers = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}

    id_solicitacao = _registrar_e_aprovar_solicitacao_de_chave(cliente, headers)

    fila = cliente.get("/v1/solicitacoes-de-chave", headers=headers)
    item = next(i for i in fila.json()["itens"] if i["id"] == id_solicitacao)
    assert item["situacao"] == "aceita"
    assert item["chave_emitida"] is False


def test_emissao_sobre_solicitacao_recusada_pela_fila_e_recusada(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    headers = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}

    id_solicitacao = _registrar_e_aprovar_solicitacao_de_chave(
        cliente, headers, situacao="recusada"
    )

    resposta = cliente.post("/v1/chaves", json={"solicitacao_id": id_solicitacao}, headers=headers)

    assert resposta.status_code == 409
    assert resposta.json()["codigo"] == "solicitacao_de_chave_nao_disponivel_para_emissao"


def test_emissao_sobre_solicitacao_sem_desfecho_pela_fila_e_recusada(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    headers = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}

    id_solicitacao = _registrar_e_aprovar_solicitacao_de_chave(cliente, headers, situacao=None)

    resposta = cliente.post("/v1/chaves", json={"solicitacao_id": id_solicitacao}, headers=headers)

    assert resposta.status_code == 409


def test_mesma_solicitacao_de_chave_nao_rende_duas_chaves(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    headers = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}

    id_solicitacao = _registrar_e_aprovar_solicitacao_de_chave(cliente, headers)
    primeira = cliente.post("/v1/chaves", json={"solicitacao_id": id_solicitacao}, headers=headers)
    assert primeira.status_code == 201

    segunda = cliente.post("/v1/chaves", json={"solicitacao_id": id_solicitacao}, headers=headers)

    assert segunda.status_code == 409
