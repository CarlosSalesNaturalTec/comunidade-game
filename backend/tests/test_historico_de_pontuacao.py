"""Leitura do histórico de pontuação (`RF-01-89`, `RN-01-68`)."""

from datetime import UTC, datetime

import pytest
from sqlalchemy import text

from nucleo.historico_de_pontuacao.modelo import OrigemDoLancamento
from nucleo.ocorrencias_de_conduta.regra import lancar_ocorrencia_de_conduta
from nucleo.personas.modelo import Papel
from nucleo.ponto_extra.regra import creditar_ponto_extra, debitar_ponto_extra
from nucleo.pontuacao.regra import creditar_ponto_regular

MOMENTO_DO_FATO = datetime(2026, 8, 1, 10, 0, tzinfo=UTC)


@pytest.fixture
def cenario(
    sessao,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_vinculo_do_mestre,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_aula,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade("Comunidade do Mestre")
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    criar_vinculo_do_mestre(mestre, comunidade)
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    trilha = criar_trilha(mestre, nome="Robótica")
    atividade = criar_atividade(criar_missao(trilha, mestre), mestre)
    aula = criar_aula(mestre, comunidade)

    creditar_ponto_regular(
        sessao,
        guerreiro_id=guerreiro.id,
        trilha_id=trilha.id,
        valor=20,
        origem=OrigemDoLancamento.resultado,
        referencia_id=None,
        detalhe="Primeira atividade",
    )
    sessao.commit()
    creditar_ponto_extra(
        sessao,
        guerreiro_id=guerreiro.id,
        valor=30,
        origem=OrigemDoLancamento.presenca,
        referencia_id=None,
    )
    sessao.commit()
    debitar_ponto_extra(
        sessao,
        guerreiro_id=guerreiro.id,
        valor=25,
        origem=OrigemDoLancamento.troca,
        referencia_id=None,
        detalhe="Camiseta",
    )
    sessao.commit()
    ocorrencia = lancar_ocorrencia_de_conduta(
        sessao,
        operador=mestre,
        aula=aula,
        atividade=atividade,
        guerreiro_id=guerreiro.id,
        motivo="Desrespeitou um colega.",
        momento_do_fato=MOMENTO_DO_FATO,
    )
    sessao.commit()

    def cabecalhos(persona):
        token, _ = criar_sessao_de_teste(persona)
        return {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}

    return {
        "admin": admin,
        "mestre": mestre,
        "guerreiro": guerreiro,
        "trilha": trilha,
        "ocorrencia": ocorrencia,
        "comunidade": comunidade,
        "cabecalhos": cabecalhos,
    }


def _rota(guerreiro):
    return f"/v1/guerreiros/{guerreiro.id}/historico-de-pontuacao"


def test_mestre_do_vinculo_le_o_historico_com_os_saldos(cliente, cenario):
    resposta = cliente.get(
        _rota(cenario["guerreiro"]), headers=cenario["cabecalhos"](cenario["mestre"])
    )
    assert resposta.status_code == 200
    corpo = resposta.json()

    assert corpo["saldos"]["extra"] == {"acumulado": 30, "saldo_disponivel": 5}
    (regular,) = corpo["saldos"]["regular"]
    assert (regular["nome"], regular["total"]) == ("Robótica", 15)

    origens = [item["origem"] for item in corpo["itens"]]
    assert origens == ["ocorrencia_de_conduta", "troca", "presenca", "resultado"]
    conduta, troca, _, resultado = corpo["itens"]
    assert conduta["valor"] == -5
    assert conduta["motivo"] == "Desrespeitou um colega."
    assert conduta["nome_da_trilha_ou_poder"] == "Robótica"
    assert (troca["valor"], troca["valor_no_acumulado"], troca["detalhe"]) == (-25, 0, "Camiseta")
    assert resultado["detalhe"] == "Primeira atividade"


def test_motivo_apagado_nao_apaga_o_lancamento(cliente, conexao, cenario):
    conexao.execute(
        text("UPDATE ocorrencia_de_conduta SET motivo = NULL, encerrada_em = now() WHERE id = :id"),
        {"id": str(cenario["ocorrencia"].id)},
    )
    resposta = cliente.get(
        _rota(cenario["guerreiro"]), headers=cenario["cabecalhos"](cenario["admin"])
    )
    conduta = resposta.json()["itens"][0]
    assert conduta["origem"] == "ocorrencia_de_conduta"
    assert conduta["valor"] == -5
    assert conduta["motivo"] is None


def test_paginacao_do_mais_recente_ao_mais_antigo(cliente, cenario):
    cabecalhos = cenario["cabecalhos"](cenario["admin"])
    primeira = cliente.get(_rota(cenario["guerreiro"]), params={"tamanho": 3}, headers=cabecalhos)
    assert primeira.status_code == 200
    assert len(primeira.json()["itens"]) == 3
    cursor = primeira.json()["proximo_cursor"]
    assert cursor

    segunda = cliente.get(
        _rota(cenario["guerreiro"]), params={"tamanho": 3, "cursor": cursor}, headers=cabecalhos
    ).json()
    assert [item["origem"] for item in segunda["itens"]] == ["resultado"]
    assert segunda["proximo_cursor"] is None
    assert segunda["saldos"]["extra"]["saldo_disponivel"] == 5


def test_guerreiro_le_o_proprio_historico_sem_identificador(cliente, cenario):
    resposta = cliente.get(
        "/v1/eu/historico-de-pontuacao", headers=cenario["cabecalhos"](cenario["guerreiro"])
    )
    assert resposta.status_code == 200
    corpo = resposta.json()
    assert len(corpo["itens"]) == 4
    assert corpo["itens"][0]["motivo"] == "Desrespeitou um colega."


def test_guerreiro_sem_pontuacao_tem_historico_vazio(cliente, cenario, criar_persona):
    novato = criar_persona(Papel.guerreiro, comunidade=cenario["comunidade"])
    resposta = cliente.get("/v1/eu/historico-de-pontuacao", headers=cenario["cabecalhos"](novato))
    assert resposta.status_code == 200
    assert resposta.json() == {
        "saldos": {"regular": [], "extra": {"acumulado": 0, "saldo_disponivel": 0}},
        "itens": [],
        "proximo_cursor": None,
    }


def test_adulto_nao_usa_a_rota_do_proprio(cliente, cenario):
    resposta = cliente.get(
        "/v1/eu/historico-de-pontuacao", headers=cenario["cabecalhos"](cenario["mestre"])
    )
    assert resposta.status_code == 403


def test_mestre_de_outra_comunidade_e_recusado(
    cliente, cenario, criar_persona, criar_comunidade, criar_vinculo_do_mestre
):
    outro = criar_persona(Papel.mestre, criada_por=cenario["admin"])
    criar_vinculo_do_mestre(outro, criar_comunidade("Outra"))
    resposta = cliente.get(_rota(cenario["guerreiro"]), headers=cenario["cabecalhos"](outro))
    assert resposta.status_code == 403
    assert "itens" not in resposta.json()


@pytest.mark.parametrize("papel", [Papel.guerreiro, Papel.responsavel, Papel.apoiador])
def test_demais_papeis_sao_recusados_na_rota_com_identificador(
    cliente, cenario, criar_persona, papel
):
    if papel == Papel.guerreiro:
        persona = criar_persona(papel, comunidade=cenario["comunidade"])
    else:
        persona = criar_persona(papel, criada_por=cenario["admin"])
    resposta = cliente.get(_rota(cenario["guerreiro"]), headers=cenario["cabecalhos"](persona))
    assert resposta.status_code == 403


def test_saldo_extra_segue_fora_da_rota_do_guerreiro_para_adultos(cliente, cenario):
    for adulto in (cenario["mestre"], cenario["admin"]):
        resposta = cliente.get("/v1/eu/pontos-extras", headers=cenario["cabecalhos"](adulto))
        assert resposta.status_code == 403
