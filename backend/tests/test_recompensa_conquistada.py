from datetime import UTC, datetime
from decimal import Decimal

import pytest

from nucleo.livro_razao.modelo import NaturezaDoLancamento
from nucleo.personas.modelo import Papel
from nucleo.recompensas_de_marco.regra import registrar_entrega
from nucleo.recursos.modelo import NaturezaDoRecurso
from nucleo.trilhas.modelo import DesbloqueioDaMissao

MOMENTO_DO_FATO = datetime(2026, 8, 1, 10, 0, tzinfo=UTC)


def _marcar_marco_alcancado(sessao, *, mestre, guerreiro, missao):
    """O marco alcançado é o desbloqueio aprovado (`RF-09-84`, design —
    decisão 6)."""
    desbloqueio = DesbloqueioDaMissao(guerreiro_id=guerreiro.id, missao_id=missao.id, aprovado=True)
    sessao.add(desbloqueio)
    sessao.commit()


@pytest.fixture
def cenario(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_valor_de_referencia,
    criar_lancamento,
    criar_vinculo_jogador,
    criar_trilha,
    criar_missao,
    criar_recompensa_de_marco,
):
    def _montar(*, quantidade=Decimal("1"), lastro=Decimal("10")):
        admin = criar_persona(Papel.admin)
        comunidade = criar_comunidade()
        ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
        tipo = criar_tipo_de_recurso(admin, natureza=NaturezaDoRecurso.consumivel)
        criar_valor_de_referencia(admin, tipo, valor_em_moedas=Decimal("1.00"))
        criar_lancamento(
            admin, tipo, ponto_de_apoio, natureza=NaturezaDoLancamento.credito, quantidade=lastro
        )

        mestre = criar_persona(Papel.mestre)
        criar_vinculo_jogador(mestre, comunidade)

        trilha = criar_trilha(mestre)
        missao = criar_missao(trilha, mestre)
        recompensa = criar_recompensa_de_marco(mestre, trilha, missao, tipo, quantidade=quantidade)

        guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)

        return {
            "admin": admin,
            "comunidade": comunidade,
            "ponto_de_apoio": ponto_de_apoio,
            "tipo": tipo,
            "mestre": mestre,
            "trilha": trilha,
            "missao": missao,
            "recompensa": recompensa,
            "guerreiro": guerreiro,
        }

    return _montar


def _autenticar(cliente, criar_chave, criar_sessao_de_teste, persona):
    chave, _ = criar_chave()
    token, _ = criar_sessao_de_teste(persona)
    return {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}


def test_marco_alcancado_aparece_como_conquistado(
    sessao, cliente, criar_chave, criar_sessao_de_teste, cenario
):
    c = cenario()
    _marcar_marco_alcancado(
        sessao, mestre=c["mestre"], guerreiro=c["guerreiro"], missao=c["missao"]
    )

    cabecalhos = _autenticar(cliente, criar_chave, criar_sessao_de_teste, c["guerreiro"])
    resposta = cliente.get("/v1/eu/recompensas", headers=cabecalhos)

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert len(corpo) == 1
    assert corpo[0]["recompensa_de_marco_id"] == str(c["recompensa"].id)
    assert corpo[0]["entregue"] is False
    assert corpo[0]["entregue_em"] is None


def test_marco_nao_alcancado_nao_aparece(cliente, criar_chave, criar_sessao_de_teste, cenario):
    c = cenario()

    cabecalhos = _autenticar(cliente, criar_chave, criar_sessao_de_teste, c["guerreiro"])
    resposta = cliente.get("/v1/eu/recompensas", headers=cabecalhos)

    assert resposta.status_code == 200
    assert resposta.json() == []


def test_entrega_confirmada_mostra_a_data(
    sessao, cliente, criar_chave, criar_sessao_de_teste, cenario
):
    c = cenario()
    _marcar_marco_alcancado(
        sessao, mestre=c["mestre"], guerreiro=c["guerreiro"], missao=c["missao"]
    )
    registrar_entrega(
        sessao,
        operador=c["mestre"],
        recompensa=c["recompensa"],
        guerreiro=c["guerreiro"],
        ponto_de_apoio=c["ponto_de_apoio"],
    )
    sessao.commit()

    cabecalhos = _autenticar(cliente, criar_chave, criar_sessao_de_teste, c["guerreiro"])
    resposta = cliente.get("/v1/eu/recompensas", headers=cabecalhos)

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo[0]["entregue"] is True
    assert corpo[0]["entregue_em"] is not None


def test_sem_lastro_nao_muda_a_leitura(
    sessao, cliente, criar_chave, criar_sessao_de_teste, cenario
):
    c = cenario(lastro=Decimal("0"))
    _marcar_marco_alcancado(
        sessao, mestre=c["mestre"], guerreiro=c["guerreiro"], missao=c["missao"]
    )

    cabecalhos = _autenticar(cliente, criar_chave, criar_sessao_de_teste, c["guerreiro"])
    resposta = cliente.get("/v1/eu/recompensas", headers=cabecalhos)

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert len(corpo) == 1
    assert corpo[0]["entregue"] is False


def test_nenhum_valor_em_moedas_ou_reais(
    sessao, cliente, criar_chave, criar_sessao_de_teste, cenario
):
    c = cenario()
    _marcar_marco_alcancado(
        sessao, mestre=c["mestre"], guerreiro=c["guerreiro"], missao=c["missao"]
    )

    cabecalhos = _autenticar(cliente, criar_chave, criar_sessao_de_teste, c["guerreiro"])
    resposta = cliente.get("/v1/eu/recompensas", headers=cabecalhos)

    assert resposta.status_code == 200
    for item in resposta.json():
        assert "valor_em_moedas" not in item
        assert "valor_em_reais" not in item


def test_so_as_proprias_recompensas(
    sessao, cliente, criar_chave, criar_sessao_de_teste, cenario, criar_persona
):
    c = cenario()
    _marcar_marco_alcancado(
        sessao, mestre=c["mestre"], guerreiro=c["guerreiro"], missao=c["missao"]
    )

    outro_guerreiro = criar_persona(Papel.guerreiro, comunidade=c["comunidade"])

    cabecalhos = _autenticar(cliente, criar_chave, criar_sessao_de_teste, outro_guerreiro)
    resposta = cliente.get("/v1/eu/recompensas", headers=cabecalhos)

    assert resposta.status_code == 200
    assert resposta.json() == []


def test_mestre_nao_le_esta_rota(cliente, criar_chave, criar_sessao_de_teste, cenario):
    c = cenario()

    cabecalhos = _autenticar(cliente, criar_chave, criar_sessao_de_teste, c["mestre"])
    resposta = cliente.get("/v1/eu/recompensas", headers=cabecalhos)

    assert resposta.status_code == 403
