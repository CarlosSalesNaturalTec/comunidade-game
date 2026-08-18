from datetime import date
from decimal import Decimal

import pytest

from nucleo.aportes.modelo import FormaDeAporte, SituacaoDeRessarcimento
from nucleo.erros import PermissaoNegada
from nucleo.livro_razao.modelo import NaturezaDoLancamento
from nucleo.personas.modelo import Papel
from nucleo.recursos.modelo import NaturezaDoRecurso
from nucleo.ressarcimentos.regra import listar_ressarciveis


@pytest.fixture
def cenario(sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio, criar_tipo_de_recurso):
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin, nome="Lanche", natureza=NaturezaDoRecurso.consumivel)
    return admin, mestre, ponto_de_apoio, tipo


def _absorcao_em_aberto(
    sessao, criar_lancamento, criar_aporte, *, autor, provedor, tipo, ponto_de_apoio, data
):
    lancamento = criar_lancamento(
        autor,
        tipo,
        ponto_de_apoio,
        natureza=NaturezaDoLancamento.credito,
        quantidade=Decimal("1.00"),
        valor_em_moedas=Decimal("1.00"),
    )
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
        data_do_aporte=data,
    )


def test_admin_le_a_fila_do_mais_antigo_ao_mais_novo(
    sessao, cenario, criar_lancamento, criar_aporte
):
    admin, mestre, ponto_de_apoio, tipo = cenario
    mais_novo = _absorcao_em_aberto(
        sessao,
        criar_lancamento,
        criar_aporte,
        autor=admin,
        provedor=mestre,
        tipo=tipo,
        ponto_de_apoio=ponto_de_apoio,
        data=date(2026, 6, 3),
    )
    mais_antigo = _absorcao_em_aberto(
        sessao,
        criar_lancamento,
        criar_aporte,
        autor=admin,
        provedor=mestre,
        tipo=tipo,
        ponto_de_apoio=ponto_de_apoio,
        data=date(2026, 6, 1),
    )
    meio = _absorcao_em_aberto(
        sessao,
        criar_lancamento,
        criar_aporte,
        autor=admin,
        provedor=mestre,
        tipo=tipo,
        ponto_de_apoio=ponto_de_apoio,
        data=date(2026, 6, 2),
    )

    aportes = listar_ressarciveis(sessao, operador=admin)

    assert [aporte.id for aporte in aportes] == [mais_antigo.id, meio.id, mais_novo.id]


def test_aporte_ressarcido_sai_da_lista(sessao, cenario, criar_lancamento, criar_aporte):
    admin, mestre, ponto_de_apoio, tipo = cenario
    aberto = _absorcao_em_aberto(
        sessao,
        criar_lancamento,
        criar_aporte,
        autor=admin,
        provedor=mestre,
        tipo=tipo,
        ponto_de_apoio=ponto_de_apoio,
        data=date(2026, 6, 1),
    )
    ressarcido = _absorcao_em_aberto(
        sessao,
        criar_lancamento,
        criar_aporte,
        autor=admin,
        provedor=mestre,
        tipo=tipo,
        ponto_de_apoio=ponto_de_apoio,
        data=date(2026, 6, 2),
    )
    ressarcido.situacao_de_ressarcimento = SituacaoDeRessarcimento.ressarcido
    sessao.commit()

    aportes = listar_ressarciveis(sessao, operador=admin)

    assert [aporte.id for aporte in aportes] == [aberto.id]


def test_aporte_da_gestao_nunca_entra_na_fila(
    sessao, cenario, criar_lancamento, criar_aporte, criar_valor_de_referencia
):
    admin, _mestre, ponto_de_apoio, tipo = cenario
    lancamento = criar_lancamento(admin, tipo, ponto_de_apoio)
    criar_aporte(
        admin,
        admin,
        tipo,
        ponto_de_apoio,
        lancamento,
        forma=FormaDeAporte.material,
        ressarcivel=False,
        situacao_de_ressarcimento=SituacaoDeRessarcimento.nao_se_aplica,
    )

    assert listar_ressarciveis(sessao, operador=admin) == []


def test_absorcao_de_servico_nunca_entra_na_fila(sessao, cenario, criar_lancamento, criar_aporte):
    admin, mestre, ponto_de_apoio, tipo = cenario
    lancamento = criar_lancamento(admin, tipo, ponto_de_apoio)
    criar_aporte(
        admin,
        mestre,
        tipo,
        ponto_de_apoio,
        lancamento,
        forma=FormaDeAporte.absorcao,
        ressarcivel=False,
        situacao_de_ressarcimento=SituacaoDeRessarcimento.nao_se_aplica,
    )

    assert listar_ressarciveis(sessao, operador=admin) == []


def test_mestre_nao_le_a_fila_da_gestao(sessao, cenario):
    _admin, mestre, _ponto_de_apoio, _tipo = cenario

    with pytest.raises(PermissaoNegada):
        listar_ressarciveis(sessao, operador=mestre)
