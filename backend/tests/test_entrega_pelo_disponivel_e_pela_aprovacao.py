"""A entrega confere o disponível, e a aprovação do desafio prático já entrega a
recompensa (`RF-07-13`, `RN-07-42`, `RF-09-146`, `RN-09-63`, `RN-07-44`, change
`entrega-pelo-disponivel-e-pela-aprovacao`)."""

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nucleo.erros import ErroDeValidacao
from nucleo.livro_razao.modelo import NaturezaDoLancamento
from nucleo.personas.modelo import Papel
from nucleo.recompensas_de_marco.modelo import EntregaDeRecompensa
from nucleo.recompensas_de_marco.regra import registrar_entrega
from nucleo.trilhas.modelo import DesbloqueioDaMissao, SituacaoDaTrilha
from nucleo.trilhas.regra import (
    declarar_desafio_de_desbloqueio,
    inscrever_na_trilha,
    submeter_desafio_de_desbloqueio,
)

ONTEM = datetime.now(UTC) - timedelta(days=1)


@pytest.fixture
def cenario(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_valor_de_referencia,
    criar_lancamento,
    criar_vinculo_do_mestre,
    criar_trilha,
    criar_missao,
    criar_recompensa_de_marco,
    criar_aula,
):
    def _montar(*, lastro=Decimal("10"), julgador_vinculado=True):
        admin = criar_persona(Papel.admin)
        comunidade = criar_comunidade()
        ponto = criar_ponto_de_apoio(admin, comunidade)
        criar_aula(
            admin,
            comunidade,
            ponto_de_apoio=ponto,
            inicio_em=ONTEM - timedelta(hours=2),
            fim_em=ONTEM,
        )
        kit = criar_tipo_de_recurso(admin, nome="Kit Robô", finalidade="recompensa")
        criar_valor_de_referencia(admin, kit, valor_em_moedas=Decimal("5.00"))
        if lastro:
            criar_lancamento(
                admin, kit, ponto, natureza=NaturezaDoLancamento.credito, quantidade=lastro
            )
        mestre = criar_persona(Papel.mestre)
        if julgador_vinculado:
            criar_vinculo_do_mestre(mestre, comunidade)
        trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
        missao = criar_missao(trilha, mestre)
        recompensa = criar_recompensa_de_marco(mestre, trilha, missao, kit, quantidade=Decimal("1"))
        guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
        return {
            "admin": admin,
            "comunidade": comunidade,
            "ponto": ponto,
            "kit": kit,
            "mestre": mestre,
            "trilha": trilha,
            "missao": missao,
            "recompensa": recompensa,
            "guerreiro": guerreiro,
        }

    return _montar


def _declarar_e_submeter_pratico(sessao, c):
    declarar_desafio_de_desbloqueio(
        sessao,
        operador=c["mestre"],
        missao=c["missao"],
        tipo="pratico",
        enunciado="Monte o robô e mostre ao Mestre.",
        forma_de_comprovacao="video",
        criterio_de_aceite="Só a produção aparece, nunca o rosto da criança.",
        titulo_curto="Robô de sucata",
    )
    inscrever_na_trilha(sessao, guerreiro=c["guerreiro"], trilha=c["trilha"])
    sessao.commit()
    submeter_desafio_de_desbloqueio(sessao, guerreiro=c["guerreiro"], missao=c["missao"])
    sessao.commit()


def _julgar(cliente, criar_chave, criar_sessao_de_teste, c, cumpriu=True):
    chave, _ = criar_chave()
    token, _ = criar_sessao_de_teste(c["mestre"])
    return cliente.post(
        f"/v1/missoes/{c['missao'].id}/desbloqueios/{c['guerreiro'].id}/julgamento",
        json={"cumpriu": cumpriu, "publicavel": False, "motivo": None if cumpriu else "Faltou."},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )


def test_o_saldo_reservado_nao_lastreia_a_entrega(sessao, cenario, criar_reserva, criar_aula):
    """`RN-07-42`, `RF-07-13`: o disponível, não o saldo — o kit reservado
    para outra aula não sai na entrega."""
    c = cenario(lastro=Decimal("1"))
    outra_aula = criar_aula(c["admin"], c["comunidade"], ponto_de_apoio=c["ponto"])
    criar_reserva(c["admin"], outra_aula, c["kit"], c["ponto"], quantidade=Decimal("1"))
    sessao.add(DesbloqueioDaMissao(guerreiro_id=c["guerreiro"].id, missao_id=c["missao"].id))
    sessao.commit()

    with pytest.raises(ErroDeValidacao) as excinfo:
        registrar_entrega(
            sessao, operador=c["mestre"], recompensa=c["recompensa"], guerreiro=c["guerreiro"]
        )
    assert "lastro" in excinfo.value.mensagem.lower()
    assert sessao.query(EntregaDeRecompensa).count() == 0


def test_a_aprovacao_do_pratico_entrega_a_recompensa(
    cliente, sessao, cenario, criar_chave, criar_sessao_de_teste
):
    c = cenario()
    _declarar_e_submeter_pratico(sessao, c)

    resposta = _julgar(cliente, criar_chave, criar_sessao_de_teste, c)

    assert resposta.status_code == 200, resposta.text
    assert resposta.json()["recompensas_entregues"] == [str(c["recompensa"].id)]
    entrega = sessao.query(EntregaDeRecompensa).one()
    assert entrega.guerreiro_id == c["guerreiro"].id
    assert entrega.ponto_de_apoio_id == c["ponto"].id


def test_sem_lastro_a_aprovacao_vale_e_a_entrega_fica_pendente(
    cliente, sessao, cenario, criar_chave, criar_sessao_de_teste
):
    c = cenario(lastro=None)
    _declarar_e_submeter_pratico(sessao, c)

    resposta = _julgar(cliente, criar_chave, criar_sessao_de_teste, c)

    assert resposta.status_code == 200, resposta.text
    assert resposta.json()["cumpriu"] is True
    assert resposta.json()["recompensas_entregues"] == []
    assert sessao.query(EntregaDeRecompensa).count() == 0


def test_quem_julga_sem_vinculo_com_a_comunidade_nao_entrega(
    cliente, sessao, cenario, criar_chave, criar_sessao_de_teste
):
    c = cenario(julgador_vinculado=False)
    _declarar_e_submeter_pratico(sessao, c)

    resposta = _julgar(cliente, criar_chave, criar_sessao_de_teste, c)

    assert resposta.status_code == 200, resposta.text
    assert resposta.json()["recompensas_entregues"] == []
    assert sessao.query(EntregaDeRecompensa).count() == 0


def test_reprovar_nao_entrega(cliente, sessao, cenario, criar_chave, criar_sessao_de_teste):
    c = cenario()
    _declarar_e_submeter_pratico(sessao, c)

    resposta = _julgar(cliente, criar_chave, criar_sessao_de_teste, c, cumpriu=False)

    assert resposta.status_code == 200, resposta.text
    assert resposta.json()["recompensas_entregues"] == []
    assert sessao.query(EntregaDeRecompensa).count() == 0
