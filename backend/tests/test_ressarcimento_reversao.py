from datetime import date
from decimal import Decimal

import pytest

from nucleo.aportes.modelo import Aporte, FormaDeAporte, SituacaoDeRessarcimento
from nucleo.aportes.regra import registrar_aporte, registrar_aporte_por_absorcao
from nucleo.armazenamento.disco import ArmazenamentoEmDisco
from nucleo.livro_razao.modelo import DestinacaoDoAporte, Lancamento
from nucleo.livro_razao.regra import saldo_de
from nucleo.personas.modelo import Papel
from nucleo.poder_sustentador.regra import contagem_de_absorcoes_de, poder_sustentador_de
from nucleo.recursos.modelo import NaturezaDoRecurso
from nucleo.ressarcimentos.regra import registrar_ressarcimento


@pytest.fixture
def cenario(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_valor_de_referencia,
    tmp_path,
):
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    apoiador = criar_persona(Papel.apoiador)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin, nome="Lanche", natureza=NaturezaDoRecurso.consumivel)
    criar_valor_de_referencia(admin, tipo, valor_em_moedas=Decimal("1.00"))
    armazenamento = ArmazenamentoEmDisco(str(tmp_path), str(tmp_path / "sessoes"))

    absorcao_mantida = registrar_aporte_por_absorcao(
        sessao,
        operador=mestre,
        tipo=tipo,
        quantidade=Decimal("30"),
        ponto_de_apoio=ponto_de_apoio,
        data_do_aporte=date(2026, 6, 1),
        valor_de_origem=Decimal("300.00"),
    )
    sessao.commit()
    absorcao_a_ressarcir = registrar_aporte_por_absorcao(
        sessao,
        operador=mestre,
        tipo=tipo,
        quantidade=Decimal("5"),
        ponto_de_apoio=ponto_de_apoio,
        data_do_aporte=date(2026, 6, 2),
        valor_de_origem=Decimal("50.00"),
    )
    sessao.commit()

    receita = registrar_aporte(
        sessao,
        operador=admin,
        provedor=apoiador,
        tipo=tipo,
        quantidade=Decimal("100"),
        ponto_de_apoio=ponto_de_apoio,
        data_do_aporte=date(2026, 6, 3),
        forma=FormaDeAporte.financeira,
        destinacao=DestinacaoDoAporte.ressarcimento,
        valor_de_origem=Decimal("100.00"),
    )
    sessao.commit()

    return {
        "admin": admin,
        "mestre": mestre,
        "ponto_de_apoio": ponto_de_apoio,
        "tipo": tipo,
        "absorcao_mantida": absorcao_mantida,
        "absorcao_a_ressarcir": absorcao_a_ressarcir,
        "receita": receita,
        "armazenamento": armazenamento,
    }


def _ressarcir(sessao, cenario):
    return registrar_ressarcimento(
        sessao,
        operador=cenario["admin"],
        aporte=cenario["absorcao_a_ressarcir"],
        receita_destinada=cenario["receita"],
        data=date(2026, 7, 1),
        comprovante_conteudo=b"comprovante",
        comprovante_nome_original="c.pdf",
        comprovante_tipo="application/pdf",
        armazenamento=cenario["armazenamento"],
    )


def test_poder_sustentador_volta_ao_valor_anterior(sessao, cenario):
    mestre = cenario["mestre"]
    assert poder_sustentador_de(sessao, provedor_id=mestre.id) == Decimal("35.00")

    _ressarcir(sessao, cenario)
    sessao.commit()

    assert poder_sustentador_de(sessao, provedor_id=mestre.id) == Decimal("30.00")


def test_contagem_de_absorcoes_nao_muda(sessao, cenario):
    mestre = cenario["mestre"]
    assert contagem_de_absorcoes_de(sessao, provedor_id=mestre.id) == 2

    _ressarcir(sessao, cenario)
    sessao.commit()

    assert contagem_de_absorcoes_de(sessao, provedor_id=mestre.id) == 2


def test_reversao_nao_move_o_saldo_de_recurso(sessao, cenario):
    tipo = cenario["tipo"]
    ponto_de_apoio = cenario["ponto_de_apoio"]
    saldo_antes = saldo_de(sessao, tipo_de_recurso_id=tipo.id, ponto_de_apoio_id=ponto_de_apoio.id)

    _ressarcir(sessao, cenario)
    sessao.commit()

    saldo_depois = saldo_de(sessao, tipo_de_recurso_id=tipo.id, ponto_de_apoio_id=ponto_de_apoio.id)
    assert saldo_depois == saldo_antes


def test_aporte_e_credito_originais_permanecem_intactos(sessao, cenario):
    absorcao = cenario["absorcao_a_ressarcir"]
    valor_em_moedas_antes = absorcao.valor_em_moedas
    lancamento_id = absorcao.lancamento_id

    _ressarcir(sessao, cenario)
    sessao.commit()

    aporte_persistido = sessao.get(Aporte, absorcao.id)
    lancamento_persistido = sessao.get(Lancamento, lancamento_id)
    assert aporte_persistido.valor_em_moedas == valor_em_moedas_antes
    assert lancamento_persistido.valor_em_moedas == valor_em_moedas_antes


def test_situacao_do_aporte_passa_a_ressarcido(sessao, cenario):
    absorcao = cenario["absorcao_a_ressarcir"]

    _ressarcir(sessao, cenario)
    sessao.commit()

    sessao.refresh(absorcao)
    assert absorcao.situacao_de_ressarcimento == SituacaoDeRessarcimento.ressarcido
