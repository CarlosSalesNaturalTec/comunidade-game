from decimal import Decimal

import pytest

from nucleo.aportes.modelo import FormaDeAporte, SituacaoDeRessarcimento
from nucleo.erros import PermissaoNegada
from nucleo.personas.modelo import Papel
from nucleo.recursos.modelo import NaturezaDoRecurso
from nucleo.ressarcimentos.regra import listar_absorcoes_do_provedor


@pytest.fixture
def cenario(sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio, criar_tipo_de_recurso):
    admin = criar_persona(Papel.admin)
    mestre_um = criar_persona(Papel.mestre, criada_por=admin)
    mestre_dois = criar_persona(Papel.mestre, criada_por=admin)
    apoiador = criar_persona(Papel.apoiador)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin, nome="Lanche", natureza=NaturezaDoRecurso.consumivel)
    return admin, mestre_um, mestre_dois, apoiador, ponto_de_apoio, tipo


def _absorcao(sessao, criar_lancamento, criar_aporte, *, autor, provedor, tipo, ponto_de_apoio):
    lancamento = criar_lancamento(autor, tipo, ponto_de_apoio)
    return criar_aporte(
        autor,
        provedor,
        tipo,
        ponto_de_apoio,
        lancamento,
        valor_de_origem=Decimal("10.00"),
        forma=FormaDeAporte.absorcao,
        ressarcivel=True,
        situacao_de_ressarcimento=SituacaoDeRessarcimento.em_aberto,
    )


def test_mestre_ve_a_situacao_do_que_absorveu(sessao, cenario, criar_lancamento, criar_aporte):
    admin, mestre_um, _mestre_dois, _apoiador, ponto_de_apoio, tipo = cenario
    absorcao = _absorcao(
        sessao,
        criar_lancamento,
        criar_aporte,
        autor=admin,
        provedor=mestre_um,
        tipo=tipo,
        ponto_de_apoio=ponto_de_apoio,
    )

    aportes = listar_absorcoes_do_provedor(sessao, operador=mestre_um)

    assert [aporte.id for aporte in aportes] == [absorcao.id]
    assert aportes[0].situacao_de_ressarcimento == SituacaoDeRessarcimento.em_aberto


def test_leitura_nao_alcanca_aporte_de_outro_provedor(
    sessao, cenario, criar_lancamento, criar_aporte
):
    admin, mestre_um, mestre_dois, _apoiador, ponto_de_apoio, tipo = cenario
    _absorcao(
        sessao,
        criar_lancamento,
        criar_aporte,
        autor=admin,
        provedor=mestre_dois,
        tipo=tipo,
        ponto_de_apoio=ponto_de_apoio,
    )

    aportes = listar_absorcoes_do_provedor(sessao, operador=mestre_um)

    assert aportes == []


def test_apoiador_nao_le_a_rota_de_absorcoes(sessao, cenario):
    _admin, _mestre_um, _mestre_dois, apoiador, _ponto_de_apoio, _tipo = cenario

    with pytest.raises(PermissaoNegada):
        listar_absorcoes_do_provedor(sessao, operador=apoiador)
