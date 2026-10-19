"""A ciência da recompensa de marco — `RF-05-45`, `RF-05-14`, `RN-05-50`.

A ciência é o ato de o Guerreiro(a) ter sido **avisado** do que conquistou, e
é ela que faz a tela da recompensa aparecer uma vez e, no desafio prático,
esperar o julgamento do Mestre autor.
"""

from decimal import Decimal

import pytest

from nucleo.livro_razao.modelo import NaturezaDoLancamento
from nucleo.personas.modelo import Papel
from nucleo.recompensas_de_marco.modelo import CienciaDaRecompensa, EntregaDeRecompensa
from nucleo.recursos.modelo import NaturezaDoRecurso
from nucleo.trilhas.modelo import DesbloqueioDaMissao


def _desbloquear(sessao, *, guerreiro, missao, aprovado=True):
    """O marco alcançado é o desbloqueio aprovado. `aprovado=None` é o
    desafio prático declarado e ainda **não julgado** pelo Mestre autor —
    enquanto ele não julga, a missão aguarda (`RF-05-14`)."""
    sessao.add(
        DesbloqueioDaMissao(guerreiro_id=guerreiro.id, missao_id=missao.id, aprovado=aprovado)
    )
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
    def _montar(*, quantidade=Decimal("1")):
        admin = criar_persona(Papel.admin)
        comunidade = criar_comunidade()
        ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
        tipo = criar_tipo_de_recurso(
            admin, nome="Camisa do Comunidade Game", natureza=NaturezaDoRecurso.consumivel
        )
        criar_valor_de_referencia(admin, tipo, valor_em_moedas=Decimal("1.00"))
        criar_lancamento(
            admin,
            tipo,
            ponto_de_apoio,
            natureza=NaturezaDoLancamento.credito,
            quantidade=Decimal("10"),
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


@pytest.fixture
def chave_da_aplicacao(criar_chave):
    """Uma chave por teste: `chave_de_aplicacao` é única por aplicação e
    ambiente, então emitir duas na mesma aplicação viola a restrição. Quem
    precisa autenticar duas personas troca só o token da sessão."""
    chave, _ = criar_chave()
    return chave


def _autenticar(chave, criar_sessao_de_teste, persona):
    token, _ = criar_sessao_de_teste(persona)
    return {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}


def _dar_ciencia(cliente, cabecalhos, recompensa):
    return cliente.post(f"/v1/eu/recompensas/{recompensa.id}/ciencia", headers=cabecalhos)


def test_guerreiro_da_ciencia_da_recompensa_que_conquistou(
    sessao, cliente, chave_da_aplicacao, criar_sessao_de_teste, cenario
):
    c = cenario()
    _desbloquear(sessao, guerreiro=c["guerreiro"], missao=c["missao"])

    cabecalhos = _autenticar(chave_da_aplicacao, criar_sessao_de_teste, c["guerreiro"])
    resposta = _dar_ciencia(cliente, cabecalhos, c["recompensa"])

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["recompensa_de_marco_id"] == str(c["recompensa"].id)
    assert corpo["guerreiro_id"] == str(c["guerreiro"].id)
    assert corpo["registrado_em"] is not None
    assert sessao.query(CienciaDaRecompensa).count() == 1


def test_a_ciencia_de_um_nao_alcanca_os_colegas(
    sessao, cliente, chave_da_aplicacao, criar_sessao_de_teste, cenario, criar_persona
):
    c = cenario()
    colega = criar_persona(Papel.guerreiro, comunidade=c["comunidade"])
    _desbloquear(sessao, guerreiro=c["guerreiro"], missao=c["missao"])
    _desbloquear(sessao, guerreiro=colega, missao=c["missao"])

    cabecalhos = _autenticar(chave_da_aplicacao, criar_sessao_de_teste, c["guerreiro"])
    assert _dar_ciencia(cliente, cabecalhos, c["recompensa"]).status_code == 201

    cabecalhos_do_colega = _autenticar(chave_da_aplicacao, criar_sessao_de_teste, colega)
    resposta = cliente.get("/v1/eu/recompensas", headers=cabecalhos_do_colega)

    assert resposta.status_code == 200
    assert resposta.json()[0]["ciente"] is False


def test_dar_ciencia_de_novo_nao_duplica_nem_falha(
    sessao, cliente, chave_da_aplicacao, criar_sessao_de_teste, cenario
):
    c = cenario()
    _desbloquear(sessao, guerreiro=c["guerreiro"], missao=c["missao"])

    cabecalhos = _autenticar(chave_da_aplicacao, criar_sessao_de_teste, c["guerreiro"])
    primeira = _dar_ciencia(cliente, cabecalhos, c["recompensa"])
    segunda = _dar_ciencia(cliente, cabecalhos, c["recompensa"])

    assert primeira.status_code == 201
    assert segunda.status_code == 201
    assert segunda.json()["registrado_em"] == primeira.json()["registrado_em"]
    assert sessao.query(CienciaDaRecompensa).count() == 1


def test_ciencia_de_recompensa_nao_conquistada_e_recusada(
    sessao, cliente, chave_da_aplicacao, criar_sessao_de_teste, cenario
):
    c = cenario()

    cabecalhos = _autenticar(chave_da_aplicacao, criar_sessao_de_teste, c["guerreiro"])
    resposta = _dar_ciencia(cliente, cabecalhos, c["recompensa"])

    assert resposta.status_code == 422
    assert sessao.query(CienciaDaRecompensa).count() == 0


def test_ninguem_da_ciencia_pelo_outro(
    sessao, cliente, chave_da_aplicacao, criar_sessao_de_teste, cenario
):
    c = cenario()
    _desbloquear(sessao, guerreiro=c["guerreiro"], missao=c["missao"])

    cabecalhos = _autenticar(chave_da_aplicacao, criar_sessao_de_teste, c["mestre"])
    resposta = _dar_ciencia(cliente, cabecalhos, c["recompensa"])

    assert resposta.status_code == 403
    assert sessao.query(CienciaDaRecompensa).count() == 0


def test_a_ciencia_nao_move_entrega_lancamento_nem_saldo(
    sessao, cliente, chave_da_aplicacao, criar_sessao_de_teste, cenario
):
    from nucleo.livro_razao.regra import saldo_de

    c = cenario()
    _desbloquear(sessao, guerreiro=c["guerreiro"], missao=c["missao"])
    saldo_antes = saldo_de(
        sessao, tipo_de_recurso_id=c["tipo"].id, ponto_de_apoio_id=c["ponto_de_apoio"].id
    )

    cabecalhos = _autenticar(chave_da_aplicacao, criar_sessao_de_teste, c["guerreiro"])
    assert _dar_ciencia(cliente, cabecalhos, c["recompensa"]).status_code == 201

    assert sessao.query(EntregaDeRecompensa).count() == 0
    assert (
        saldo_de(sessao, tipo_de_recurso_id=c["tipo"].id, ponto_de_apoio_id=c["ponto_de_apoio"].id)
        == saldo_antes
    )
    resposta = cliente.get("/v1/eu/recompensas", headers=cabecalhos)
    assert resposta.json()[0]["entregue"] is False


def test_pratico_nao_julgado_nao_admite_ciencia(
    sessao, cliente, chave_da_aplicacao, criar_sessao_de_teste, cenario
):
    c = cenario()
    _desbloquear(sessao, guerreiro=c["guerreiro"], missao=c["missao"], aprovado=None)

    cabecalhos = _autenticar(chave_da_aplicacao, criar_sessao_de_teste, c["guerreiro"])
    resposta = _dar_ciencia(cliente, cabecalhos, c["recompensa"])

    assert resposta.status_code == 422
    assert sessao.query(CienciaDaRecompensa).count() == 0
    # Enquanto o Mestre não julga, a recompensa nem consta da leitura dele.
    assert cliente.get("/v1/eu/recompensas", headers=cabecalhos).json() == []


def test_julgado_o_pratico_a_ciencia_e_admitida(
    sessao, cliente, chave_da_aplicacao, criar_sessao_de_teste, cenario
):
    c = cenario()
    desbloqueio = DesbloqueioDaMissao(
        guerreiro_id=c["guerreiro"].id, missao_id=c["missao"].id, aprovado=None
    )
    sessao.add(desbloqueio)
    sessao.commit()

    cabecalhos = _autenticar(chave_da_aplicacao, criar_sessao_de_teste, c["guerreiro"])
    assert _dar_ciencia(cliente, cabecalhos, c["recompensa"]).status_code == 422

    desbloqueio.aprovado = True
    sessao.commit()

    # Julgado, a recompensa passa a constar **sem ciência**, e a ciência é
    # admitida: é este par de fatos que faz a tela aparecer na volta.
    leitura = cliente.get("/v1/eu/recompensas", headers=cabecalhos).json()
    assert len(leitura) == 1
    assert leitura[0]["ciente"] is False
    assert _dar_ciencia(cliente, cabecalhos, c["recompensa"]).status_code == 201
