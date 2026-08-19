from datetime import date
from decimal import Decimal

import pytest

from nucleo.aportes.modelo import FormaDeAporte
from nucleo.aportes.regra import registrar_aporte
from nucleo.erros import ErroDeValidacao, PermissaoNegada
from nucleo.patrimonio.modelo import ItemPatrimonial
from nucleo.patrimonio.regra import tombar_item
from nucleo.personas.modelo import Papel
from nucleo.recursos.modelo import NaturezaDoRecurso


@pytest.fixture
def cenario(sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio, criar_tipo_de_recurso):
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo_duravel = criar_tipo_de_recurso(admin, nome="Livro", natureza=NaturezaDoRecurso.duravel)
    return admin, apoiador, comunidade, ponto_de_apoio, tipo_duravel


def _aportar(sessao, criar_valor_de_referencia, admin, apoiador, tipo, ponto_de_apoio, quantidade):
    criar_valor_de_referencia(admin, tipo, valor_em_moedas=Decimal("1.00"))
    aporte = registrar_aporte(
        sessao,
        operador=admin,
        provedor=apoiador,
        tipo=tipo,
        quantidade=quantidade,
        ponto_de_apoio=ponto_de_apoio,
        data_do_aporte=date(2026, 6, 1),
        forma=FormaDeAporte.material,
    )
    sessao.commit()
    return aporte


def test_admin_tomba_exemplar_com_aporte_de_origem(sessao, cenario, criar_valor_de_referencia):
    admin, apoiador, _, ponto_de_apoio, tipo_duravel = cenario
    aporte = _aportar(
        sessao,
        criar_valor_de_referencia,
        admin,
        apoiador,
        tipo_duravel,
        ponto_de_apoio,
        Decimal("3"),
    )

    item = tombar_item(
        sessao,
        operador=admin,
        titulo="Descobrindo o Mundo",
        numero_de_tombo="0001",
        ponto_de_apoio=ponto_de_apoio,
        estado_de_conservacao="novo",
        aporte_de_origem=aporte,
    )
    sessao.commit()

    assert item.aporte_de_origem_id == aporte.id
    assert item.autor_id == admin.id


def test_exemplar_sem_aporte_de_origem_e_tombado(sessao, cenario):
    admin, _, _, ponto_de_apoio, _ = cenario

    item = tombar_item(
        sessao,
        operador=admin,
        titulo="Descobrindo o Mundo",
        numero_de_tombo="0001",
        ponto_de_apoio=ponto_de_apoio,
        estado_de_conservacao="novo",
    )
    sessao.commit()

    assert item.aporte_de_origem_id is None


def test_mestre_nao_tomba(sessao, cenario, criar_persona):
    admin, _, _, ponto_de_apoio, _ = cenario
    mestre = criar_persona(Papel.mestre, criada_por=admin)

    with pytest.raises(PermissaoNegada):
        tombar_item(
            sessao,
            operador=mestre,
            titulo="Descobrindo o Mundo",
            numero_de_tombo="0001",
            ponto_de_apoio=ponto_de_apoio,
            estado_de_conservacao="novo",
        )
    assert sessao.query(ItemPatrimonial).count() == 0


def test_aporte_de_origem_de_natureza_nao_duravel_e_recusado(
    sessao, cenario, criar_tipo_de_recurso, criar_valor_de_referencia
):
    admin, apoiador, _, ponto_de_apoio, _ = cenario
    tipo_consumivel = criar_tipo_de_recurso(
        admin, nome="Lanche", natureza=NaturezaDoRecurso.consumivel
    )
    aporte = _aportar(
        sessao,
        criar_valor_de_referencia,
        admin,
        apoiador,
        tipo_consumivel,
        ponto_de_apoio,
        Decimal("3"),
    )

    with pytest.raises(ErroDeValidacao) as excinfo:
        tombar_item(
            sessao,
            operador=admin,
            titulo="Descobrindo o Mundo",
            numero_de_tombo="0001",
            ponto_de_apoio=ponto_de_apoio,
            estado_de_conservacao="novo",
            aporte_de_origem=aporte,
        )
    assert excinfo.value.campo == "aporte_de_origem_id"
    assert sessao.query(ItemPatrimonial).count() == 0


def test_tombo_repetido_no_mesmo_ponto_de_apoio_e_recusado(sessao, cenario, criar_item_patrimonial):
    admin, _, _, ponto_de_apoio, _ = cenario
    criar_item_patrimonial(admin, ponto_de_apoio, numero_de_tombo="0001")

    with pytest.raises(ErroDeValidacao) as excinfo:
        tombar_item(
            sessao,
            operador=admin,
            titulo="Outro Título",
            numero_de_tombo="0001",
            ponto_de_apoio=ponto_de_apoio,
            estado_de_conservacao="novo",
        )
    assert excinfo.value.campo == "numero_de_tombo"
    assert sessao.query(ItemPatrimonial).count() == 1


def test_mesmo_tombo_em_pontos_de_apoio_diferentes_e_aceito(
    sessao, cenario, criar_ponto_de_apoio, criar_item_patrimonial
):
    admin, _, comunidade, ponto_de_apoio, _ = cenario
    outro_ponto = criar_ponto_de_apoio(admin, comunidade, nome="Outro Ponto")
    criar_item_patrimonial(admin, ponto_de_apoio, numero_de_tombo="0001")

    item = tombar_item(
        sessao,
        operador=admin,
        titulo="Descobrindo o Mundo",
        numero_de_tombo="0001",
        ponto_de_apoio=outro_ponto,
        estado_de_conservacao="novo",
    )
    sessao.commit()

    assert sessao.query(ItemPatrimonial).count() == 2
    assert item.ponto_de_apoio_id == outro_ponto.id


def test_tombamento_no_limite_do_aporte_e_aceito(
    sessao, cenario, criar_valor_de_referencia, criar_item_patrimonial
):
    admin, apoiador, _, ponto_de_apoio, tipo_duravel = cenario
    aporte = _aportar(
        sessao,
        criar_valor_de_referencia,
        admin,
        apoiador,
        tipo_duravel,
        ponto_de_apoio,
        Decimal("3"),
    )
    criar_item_patrimonial(admin, ponto_de_apoio, aporte_de_origem=aporte, numero_de_tombo="0001")
    criar_item_patrimonial(admin, ponto_de_apoio, aporte_de_origem=aporte, numero_de_tombo="0002")

    tombar_item(
        sessao,
        operador=admin,
        titulo="Descobrindo o Mundo",
        numero_de_tombo="0003",
        ponto_de_apoio=ponto_de_apoio,
        estado_de_conservacao="novo",
        aporte_de_origem=aporte,
    )
    sessao.commit()

    assert sessao.query(ItemPatrimonial).filter_by(aporte_de_origem_id=aporte.id).count() == 3


def test_tombamento_alem_da_quantidade_aportada_e_recusado(
    sessao, cenario, criar_valor_de_referencia, criar_item_patrimonial
):
    admin, apoiador, _, ponto_de_apoio, tipo_duravel = cenario
    aporte = _aportar(
        sessao,
        criar_valor_de_referencia,
        admin,
        apoiador,
        tipo_duravel,
        ponto_de_apoio,
        Decimal("3"),
    )
    criar_item_patrimonial(admin, ponto_de_apoio, aporte_de_origem=aporte, numero_de_tombo="0001")
    criar_item_patrimonial(admin, ponto_de_apoio, aporte_de_origem=aporte, numero_de_tombo="0002")
    criar_item_patrimonial(admin, ponto_de_apoio, aporte_de_origem=aporte, numero_de_tombo="0003")

    with pytest.raises(ErroDeValidacao) as excinfo:
        tombar_item(
            sessao,
            operador=admin,
            titulo="Descobrindo o Mundo",
            numero_de_tombo="0004",
            ponto_de_apoio=ponto_de_apoio,
            estado_de_conservacao="novo",
            aporte_de_origem=aporte,
        )
    assert excinfo.value.campo == "aporte_de_origem_id"
    assert sessao.query(ItemPatrimonial).filter_by(aporte_de_origem_id=aporte.id).count() == 3
