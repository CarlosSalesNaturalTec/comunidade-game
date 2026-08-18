from datetime import date
from decimal import Decimal

import pytest

from nucleo.aportes.modelo import SituacaoDeRessarcimento
from nucleo.aportes.regra import registrar_aporte_por_absorcao
from nucleo.aulas.modelo import SituacaoDaAula
from nucleo.erros import ErroDeValidacao
from nucleo.necessidades.regra import derivar_necessidades
from nucleo.personas.modelo import Papel
from nucleo.recursos.modelo import NaturezaDoRecurso


def _tornar_pendente(sessao, aula):
    aula.situacao = SituacaoDaAula.pendente_de_lastro
    sessao.commit()


@pytest.fixture
def cenario(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_valor_de_referencia,
    criar_aula,
    criar_recurso_declarado_da_aula,
):
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin, nome="Lanche", natureza=NaturezaDoRecurso.consumivel)
    criar_valor_de_referencia(admin, tipo, valor_em_moedas=Decimal("1.00"))
    aula = criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)
    criar_recurso_declarado_da_aula(aula, tipo, quantidade=Decimal("6.00"))
    _tornar_pendente(sessao, aula)
    return admin, mestre, comunidade, ponto_de_apoio, tipo, aula


def test_absorcao_declarada_abate_a_falta_da_aula_que_atende(sessao, cenario):
    _admin, mestre, _comunidade, ponto_de_apoio, tipo, aula = cenario

    registrar_aporte_por_absorcao(
        sessao,
        operador=mestre,
        tipo=tipo,
        quantidade=Decimal("2"),
        ponto_de_apoio=ponto_de_apoio,
        data_do_aporte=date(2026, 6, 1),
        aula=aula,
        valor_de_origem=Decimal("20.00"),
    )
    sessao.commit()
    sessao.refresh(aula)

    assert aula.situacao == SituacaoDaAula.pendente_de_lastro
    necessidades = derivar_necessidades(sessao)
    assert len(necessidades) == 1
    assert necessidades[0].quantidade_faltante == Decimal("4.00")


def test_absorcao_que_fecha_a_falta_confirma_a_aula(sessao, cenario):
    _admin, mestre, _comunidade, ponto_de_apoio, tipo, aula = cenario

    aporte = registrar_aporte_por_absorcao(
        sessao,
        operador=mestre,
        tipo=tipo,
        quantidade=Decimal("6"),
        ponto_de_apoio=ponto_de_apoio,
        data_do_aporte=date(2026, 6, 1),
        aula=aula,
        valor_de_origem=Decimal("60.00"),
    )
    sessao.commit()
    sessao.refresh(aula)

    assert aporte.aula_id == aula.id
    assert aula.situacao == SituacaoDaAula.confirmada
    assert derivar_necessidades(sessao) == []


def test_absorcao_de_tipo_que_a_aula_nao_consome_e_recusada(
    sessao, cenario, criar_tipo_de_recurso, criar_valor_de_referencia
):
    admin, mestre, _comunidade, ponto_de_apoio, _tipo, aula = cenario
    outro_tipo = criar_tipo_de_recurso(admin, nome="Insumo", natureza=NaturezaDoRecurso.consumivel)
    criar_valor_de_referencia(admin, outro_tipo, valor_em_moedas=Decimal("1.00"))

    with pytest.raises(ErroDeValidacao) as excinfo:
        registrar_aporte_por_absorcao(
            sessao,
            operador=mestre,
            tipo=outro_tipo,
            quantidade=Decimal("1"),
            ponto_de_apoio=ponto_de_apoio,
            data_do_aporte=date(2026, 6, 1),
            aula=aula,
            valor_de_origem=Decimal("10.00"),
        )
    assert excinfo.value.campo == "aula_id"


def test_absorcao_com_desembolso_exige_valor_de_origem(sessao, cenario):
    _admin, mestre, _comunidade, ponto_de_apoio, tipo, _aula = cenario

    with pytest.raises(ErroDeValidacao) as excinfo:
        registrar_aporte_por_absorcao(
            sessao,
            operador=mestre,
            tipo=tipo,
            quantidade=Decimal("1"),
            ponto_de_apoio=ponto_de_apoio,
            data_do_aporte=date(2026, 6, 1),
        )
    assert excinfo.value.campo == "valor_de_origem"


def test_absorcao_de_servico_nao_exige_valor_e_nao_e_ressarcivel(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_valor_de_referencia,
):
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo_servico = criar_tipo_de_recurso(
        admin, nome="Hora-aula", natureza=NaturezaDoRecurso.servico
    )
    criar_valor_de_referencia(admin, tipo_servico, valor_em_moedas=Decimal("2.00"))

    aporte = registrar_aporte_por_absorcao(
        sessao,
        operador=mestre,
        tipo=tipo_servico,
        quantidade=Decimal("1"),
        ponto_de_apoio=ponto_de_apoio,
        data_do_aporte=date(2026, 6, 1),
    )
    sessao.commit()

    assert aporte.valor_de_origem is None
    assert aporte.ressarcivel is False
    assert aporte.situacao_de_ressarcimento == SituacaoDeRessarcimento.nao_se_aplica
