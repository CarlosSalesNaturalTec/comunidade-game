from datetime import date
from decimal import Decimal

import pytest

from nucleo.aportes.modelo import FormaDeAporte
from nucleo.aportes.regra import registrar_aporte, registrar_aporte_por_absorcao
from nucleo.aulas.modelo import SituacaoDaAula
from nucleo.comunidades.modelo import ComunidadeVirtual
from nucleo.erros import ErroDeValidacao
from nucleo.livro_razao.modelo import DestinacaoDoAporte
from nucleo.livro_razao.regra import saldo_de
from nucleo.personas.modelo import Papel
from nucleo.poder_sustentador.regra import poder_sustentador_de
from nucleo.recursos.modelo import NaturezaDoRecurso
from nucleo.reservas.modelo import Reserva


@pytest.fixture
def cenario(sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio, criar_tipo_de_recurso):
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin, nome="Lanche", natureza=NaturezaDoRecurso.consumivel)
    return admin, apoiador, ponto_de_apoio, tipo


def test_doacao_destinada_credita_sem_virar_lastro(sessao, cenario, criar_valor_de_referencia):
    admin, apoiador, ponto_de_apoio, tipo = cenario
    criar_valor_de_referencia(admin, tipo, valor_em_moedas=Decimal("1.00"))

    aporte = registrar_aporte(
        sessao,
        operador=admin,
        provedor=apoiador,
        tipo=tipo,
        quantidade=Decimal("5"),
        ponto_de_apoio=ponto_de_apoio,
        data_do_aporte=date(2026, 6, 1),
        forma=FormaDeAporte.financeira,
        destinacao=DestinacaoDoAporte.ressarcimento,
    )
    sessao.commit()

    assert poder_sustentador_de(sessao, provedor_id=apoiador.id) == Decimal("5.00")
    assert saldo_de(
        sessao, tipo_de_recurso_id=tipo.id, ponto_de_apoio_id=ponto_de_apoio.id
    ) == Decimal("0.00")
    assert aporte.destinacao == DestinacaoDoAporte.ressarcimento


def test_receita_destinada_nao_confirma_aula_pendente(
    sessao, cenario, criar_valor_de_referencia, criar_aula, criar_recurso_declarado_da_aula
):
    admin, apoiador, ponto_de_apoio, tipo = cenario
    criar_valor_de_referencia(admin, tipo, valor_em_moedas=Decimal("1.00"))
    comunidade = sessao.get(ComunidadeVirtual, ponto_de_apoio.comunidade_virtual_id)
    aula = criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)
    criar_recurso_declarado_da_aula(aula, tipo, quantidade=Decimal("3.00"))
    aula.situacao = SituacaoDaAula.pendente_de_lastro
    sessao.commit()

    registrar_aporte(
        sessao,
        operador=admin,
        provedor=apoiador,
        tipo=tipo,
        quantidade=Decimal("3"),
        ponto_de_apoio=ponto_de_apoio,
        data_do_aporte=date(2026, 6, 1),
        forma=FormaDeAporte.financeira,
        destinacao=DestinacaoDoAporte.ressarcimento,
    )
    sessao.commit()
    sessao.refresh(aula)

    assert aula.situacao == SituacaoDaAula.pendente_de_lastro
    assert sessao.query(Reserva).filter_by(aula_id=aula.id).count() == 0


def test_aporte_sem_destinacao_declarada_e_de_lastro(sessao, cenario, criar_valor_de_referencia):
    admin, apoiador, ponto_de_apoio, tipo = cenario
    criar_valor_de_referencia(admin, tipo, valor_em_moedas=Decimal("1.00"))

    aporte = registrar_aporte(
        sessao,
        operador=admin,
        provedor=apoiador,
        tipo=tipo,
        quantidade=Decimal("2"),
        ponto_de_apoio=ponto_de_apoio,
        data_do_aporte=date(2026, 6, 1),
        forma=FormaDeAporte.material,
    )
    sessao.commit()

    assert aporte.destinacao == DestinacaoDoAporte.lastro
    assert saldo_de(
        sessao, tipo_de_recurso_id=tipo.id, ponto_de_apoio_id=ponto_de_apoio.id
    ) == Decimal("2.00")


def test_absorcao_nao_se_destina_a_ressarcimento(sessao, cenario, criar_valor_de_referencia):
    admin, _apoiador, ponto_de_apoio, tipo = cenario
    criar_valor_de_referencia(admin, tipo, valor_em_moedas=Decimal("1.00"))

    with pytest.raises(ErroDeValidacao) as excinfo:
        registrar_aporte_por_absorcao(
            sessao,
            operador=admin,
            tipo=tipo,
            quantidade=Decimal("1"),
            ponto_de_apoio=ponto_de_apoio,
            data_do_aporte=date(2026, 6, 1),
            valor_de_origem=Decimal("10.00"),
            destinacao=DestinacaoDoAporte.ressarcimento,
        )
    assert excinfo.value.campo == "destinacao"
