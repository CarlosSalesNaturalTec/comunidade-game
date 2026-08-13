import uuid
from datetime import UTC, datetime, timedelta

from nucleo.chaves.modelo import NaturezaDaChave, SituacaoDaChave
from nucleo.chaves.segredo import gerar_segredo, montar_chave_completa


def test_leitura_dentro_da_cota_e_processada(cliente, criar_chave, sobrescrever_configuracao):
    sobrescrever_configuracao(protecao_cota_do_projeto_por_hora=3)
    chave, _ = criar_chave()

    for _ in range(3):
        resposta = cliente.get("/v1/publica", headers={"X-Chave-Aplicacao": chave})
        assert resposta.status_code == 200


def test_leitura_acima_da_cota_e_recusada_com_429(cliente, criar_chave, sobrescrever_configuracao):
    sobrescrever_configuracao(protecao_cota_do_projeto_por_hora=2)
    chave, _ = criar_chave()

    cliente.get("/v1/publica", headers={"X-Chave-Aplicacao": chave})
    cliente.get("/v1/publica", headers={"X-Chave-Aplicacao": chave})
    resposta = cliente.get("/v1/publica", headers={"X-Chave-Aplicacao": chave})

    assert resposta.status_code == 429
    assert resposta.json()["codigo"] == "cota_de_leitura_excedida"


def test_faixa_de_terceiro_tem_cota_menor_que_a_do_projeto(
    cliente, criar_chave, sobrescrever_configuracao
):
    sobrescrever_configuracao(
        protecao_cota_do_projeto_por_hora=10, protecao_cota_de_terceiro_por_hora=3
    )
    chave_projeto, _ = criar_chave(aplicacao="app-06-vitrine", natureza=NaturezaDaChave.do_projeto)
    chave_terceiro, _ = criar_chave(
        aplicacao="terceiro-de-teste", natureza=NaturezaDaChave.de_terceiro
    )

    respostas_terceiro = [
        cliente.get("/v1/publica", headers={"X-Chave-Aplicacao": chave_terceiro}) for _ in range(4)
    ]
    respostas_projeto = [
        cliente.get("/v1/publica", headers={"X-Chave-Aplicacao": chave_projeto}) for _ in range(4)
    ]

    assert respostas_terceiro[-1].status_code == 429
    assert all(resposta.status_code == 200 for resposta in respostas_projeto)


def test_escrita_nao_consome_a_cota(cliente, criar_chave, sobrescrever_configuracao):
    sobrescrever_configuracao(protecao_cota_do_projeto_por_hora=2)
    chave, _ = criar_chave()

    for _ in range(5):
        resposta = cliente.post(
            "/v1/eventos",
            json={"momento_do_fato": "2026-08-01T10:00:00-03:00"},
            headers={"X-Chave-Aplicacao": chave},
        )
        assert resposta.status_code == 200

    leitura = cliente.get("/v1/publica", headers={"X-Chave-Aplicacao": chave})
    assert leitura.status_code == 200


def test_janela_deslizante_libera_a_chave_sem_intervencao_humana(
    cliente, criar_chave, sobrescrever_configuracao, monkeypatch
):
    sobrescrever_configuracao(protecao_cota_do_projeto_por_hora=1)
    chave, _ = criar_chave()

    relogio = {"agora": datetime(2026, 1, 1, tzinfo=UTC)}
    monkeypatch.setattr("nucleo.protecao.cota.agora", lambda: relogio["agora"])

    primeira = cliente.get("/v1/publica", headers={"X-Chave-Aplicacao": chave})
    segunda = cliente.get("/v1/publica", headers={"X-Chave-Aplicacao": chave})
    assert primeira.status_code == 200
    assert segunda.status_code == 429

    relogio["agora"] += timedelta(hours=1, seconds=1)
    terceira = cliente.get("/v1/publica", headers={"X-Chave-Aplicacao": chave})
    assert terceira.status_code == 200


def test_chave_desconhecida_e_revogada_nunca_recebem_429(
    cliente, criar_chave, sobrescrever_configuracao
):
    sobrescrever_configuracao(protecao_cota_do_projeto_por_hora=1)
    chave_revogada, _ = criar_chave(situacao=SituacaoDaChave.revogada)
    chave_inexistente = montar_chave_completa("desenvolvimento", str(uuid.uuid4()), gerar_segredo())

    for _ in range(5):
        resposta = cliente.get("/v1/publica", headers={"X-Chave-Aplicacao": chave_revogada})
        assert resposta.status_code == 401

    for _ in range(5):
        resposta = cliente.get("/v1/publica", headers={"X-Chave-Aplicacao": chave_inexistente})
        assert resposta.status_code == 401
