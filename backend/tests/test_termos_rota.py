from datetime import UTC, datetime, timedelta

from nucleo.consentimentos.modelo import TipoDeConsentimento
from nucleo.personas.modelo import Papel
from nucleo.termos.modelo import LeituraDeTermo


def test_consulta_devolve_o_termo_vigente_com_o_texto(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_termo
):
    chave, _ = criar_chave()
    responsavel = criar_persona(Papel.responsavel)
    criar_termo(versao="2026-08", texto="Texto vigente de teste.")
    token, _ = criar_sessao_de_teste(responsavel)

    resposta = cliente.get(
        "/v1/termos", headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}
    )
    assert resposta.status_code == 200
    corpo = resposta.json()
    assert len(corpo) == 1
    assert corpo[0]["tipo"] == TipoDeConsentimento.autorizacao_de_divulgacao.value
    assert corpo[0]["vigente"]["versao"] == "2026-08"
    assert corpo[0]["vigente"]["texto"] == "Texto vigente de teste."


def test_consulta_sem_credencial_de_persona_e_recusada(cliente, criar_chave, criar_termo):
    chave, _ = criar_chave()
    criar_termo()

    resposta = cliente.get("/v1/termos", headers={"X-Chave-Aplicacao": chave})
    assert resposta.status_code == 401


def test_historico_traz_as_versoes_anteriores_com_o_periodo(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_termo
):
    chave, _ = criar_chave()
    responsavel = criar_persona(Papel.responsavel)
    agora = datetime.now(UTC)
    criar_termo(versao="2026-07", texto="Texto antigo.", vigente_desde=agora - timedelta(days=60))
    criar_termo(versao="2026-08", texto="Texto vigente.", vigente_desde=agora - timedelta(days=1))
    token, _ = criar_sessao_de_teste(responsavel)

    resposta = cliente.get(
        "/v1/termos", headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}
    )
    corpo = resposta.json()[0]
    assert corpo["vigente"]["versao"] == "2026-08"
    assert len(corpo["historico"]) == 1
    assert corpo["historico"][0]["versao"] == "2026-07"
    assert corpo["historico"][0]["texto"] == "Texto antigo."


def test_leitura_e_registrada_com_data_e_hora(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_termo
):
    chave, _ = criar_chave()
    responsavel = criar_persona(Papel.responsavel)
    criar_termo(versao="2026-08")
    token, _ = criar_sessao_de_teste(responsavel)

    resposta = cliente.post(
        "/v1/termos/2026-08/leitura",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["versao"] == "2026-08"
    assert corpo["lida_em"] is not None


def test_releitura_da_mesma_versao_nao_gera_segundo_registro(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_termo, sessao
):
    chave, _ = criar_chave()
    responsavel = criar_persona(Papel.responsavel)
    criar_termo(versao="2026-08")
    token, _ = criar_sessao_de_teste(responsavel)
    cabecalhos = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}

    primeira = cliente.post("/v1/termos/2026-08/leitura", headers=cabecalhos)
    segunda = cliente.post("/v1/termos/2026-08/leitura", headers=cabecalhos)

    assert primeira.status_code == 201
    assert segunda.status_code == 201
    assert primeira.json()["id"] == segunda.json()["id"]
    assert primeira.json()["lida_em"] == segunda.json()["lida_em"]
    assert (
        sessao.query(LeituraDeTermo)
        .filter_by(responsavel_id=responsavel.id, versao="2026-08")
        .count()
        == 1
    )


def test_ler_o_termo_nao_concede_autorizacao(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_termo,
    criar_vinculo,
):
    chave, _ = criar_chave()
    responsavel = criar_persona(Papel.responsavel)
    guerreiro = criar_persona(Papel.guerreiro)
    criar_vinculo(responsavel, guerreiro, cadastrado_por=responsavel)
    criar_termo(versao="2026-08")
    token, _ = criar_sessao_de_teste(responsavel)
    cabecalhos = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}

    cliente.post("/v1/termos/2026-08/leitura", headers=cabecalhos)

    resposta = cliente.get(f"/v1/eu/guerreiros/{guerreiro.id}/autorizacao", headers=cabecalhos)
    assert resposta.status_code == 200
    assert resposta.json()["estado"] == "nao_autorizada"


def test_quem_nao_e_responsavel_nao_registra_leitura(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_termo
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    criar_termo(versao="2026-08")
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.post(
        "/v1/termos/2026-08/leitura",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 403


def test_versao_inexistente_e_recusada(cliente, criar_chave, criar_persona, criar_sessao_de_teste):
    chave, _ = criar_chave()
    responsavel = criar_persona(Papel.responsavel)
    token, _ = criar_sessao_de_teste(responsavel)

    resposta = cliente.post(
        "/v1/termos/versao-inexistente/leitura",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 404
