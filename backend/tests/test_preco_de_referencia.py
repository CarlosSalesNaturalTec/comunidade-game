from datetime import date
from decimal import Decimal

import pytest

from nucleo.erros import ErroDeValidacao, PermissaoNegada
from nucleo.personas.modelo import Papel
from nucleo.recursos.modelo import PrecoDeReferencia, ValorDeReferencia
from nucleo.recursos.regra import (
    consultar_preco_de_referencia,
    consultar_valor_de_referencia,
    registrar_preco_de_referencia,
    registrar_valor_de_referencia,
)


def test_primeira_vigencia_do_preco_nasce_sem_encerramento(
    sessao, criar_persona, criar_tipo_de_recurso
):
    admin = criar_persona(Papel.admin)
    tipo = criar_tipo_de_recurso(admin)

    preco = registrar_preco_de_referencia(
        sessao,
        operador=admin,
        tipo=tipo,
        preco_em_pontos_extras=20,
        vigencia_inicio=date(2026, 1, 1),
    )
    sessao.commit()

    assert preco.preco_em_pontos_extras == 20
    assert preco.vigencia_fim is None


def test_preco_novo_encerra_a_vigencia_anterior_sem_reescreve_la(
    sessao, criar_persona, criar_tipo_de_recurso
):
    admin = criar_persona(Papel.admin)
    tipo = criar_tipo_de_recurso(admin)

    primeiro = registrar_preco_de_referencia(
        sessao,
        operador=admin,
        tipo=tipo,
        preco_em_pontos_extras=20,
        vigencia_inicio=date(2026, 1, 1),
    )
    sessao.commit()

    registrar_preco_de_referencia(
        sessao,
        operador=admin,
        tipo=tipo,
        preco_em_pontos_extras=30,
        vigencia_inicio=date(2026, 6, 1),
    )
    sessao.commit()
    sessao.refresh(primeiro)

    assert primeiro.vigencia_fim == date(2026, 6, 1)
    assert primeiro.preco_em_pontos_extras == 20
    assert sessao.query(PrecoDeReferencia).count() == 2


def test_empate_no_mesmo_dia_a_consulta_devolve_o_registrado_por_ultimo(
    sessao, criar_persona, criar_tipo_de_recurso
):
    admin = criar_persona(Papel.admin)
    tipo = criar_tipo_de_recurso(admin)

    registrar_preco_de_referencia(
        sessao,
        operador=admin,
        tipo=tipo,
        preco_em_pontos_extras=20,
        vigencia_inicio=date(2026, 1, 1),
    )
    sessao.commit()
    registrar_preco_de_referencia(
        sessao,
        operador=admin,
        tipo=tipo,
        preco_em_pontos_extras=50,
        vigencia_inicio=date(2026, 1, 1),
    )
    sessao.commit()

    preco = consultar_preco_de_referencia(sessao, tipo=tipo, data=date(2026, 1, 1))

    assert preco.preco_em_pontos_extras == 50


def test_leitura_pela_data_da_epoca_devolve_o_preco_daquela_vigencia(
    sessao, criar_persona, criar_tipo_de_recurso
):
    admin = criar_persona(Papel.admin)
    tipo = criar_tipo_de_recurso(admin)

    registrar_preco_de_referencia(
        sessao,
        operador=admin,
        tipo=tipo,
        preco_em_pontos_extras=20,
        vigencia_inicio=date(2026, 1, 1),
    )
    registrar_preco_de_referencia(
        sessao,
        operador=admin,
        tipo=tipo,
        preco_em_pontos_extras=40,
        vigencia_inicio=date(2026, 6, 1),
    )
    sessao.commit()

    preco = consultar_preco_de_referencia(sessao, tipo=tipo, data=date(2026, 3, 1))

    assert preco.preco_em_pontos_extras == 20


def test_piso_de_vinte_e_aceito(sessao, criar_persona, criar_tipo_de_recurso):
    admin = criar_persona(Papel.admin)
    tipo = criar_tipo_de_recurso(admin)

    preco = registrar_preco_de_referencia(
        sessao,
        operador=admin,
        tipo=tipo,
        preco_em_pontos_extras=20,
        vigencia_inicio=date(2026, 1, 1),
    )
    sessao.commit()

    assert preco.preco_em_pontos_extras == 20


def test_dezenove_e_recusado(sessao, criar_persona, criar_tipo_de_recurso):
    admin = criar_persona(Papel.admin)
    tipo = criar_tipo_de_recurso(admin)

    with pytest.raises(ErroDeValidacao) as excinfo:
        registrar_preco_de_referencia(
            sessao,
            operador=admin,
            tipo=tipo,
            preco_em_pontos_extras=19,
            vigencia_inicio=date(2026, 1, 1),
        )
    assert excinfo.value.campo == "preco_em_pontos_extras"
    assert sessao.query(PrecoDeReferencia).count() == 0


def test_alteracao_para_abaixo_do_piso_e_recusada(sessao, criar_persona, criar_tipo_de_recurso):
    admin = criar_persona(Papel.admin)
    tipo = criar_tipo_de_recurso(admin)
    primeiro = registrar_preco_de_referencia(
        sessao,
        operador=admin,
        tipo=tipo,
        preco_em_pontos_extras=20,
        vigencia_inicio=date(2026, 1, 1),
    )
    sessao.commit()

    with pytest.raises(ErroDeValidacao):
        registrar_preco_de_referencia(
            sessao,
            operador=admin,
            tipo=tipo,
            preco_em_pontos_extras=10,
            vigencia_inicio=date(2026, 6, 1),
        )
    sessao.commit()
    sessao.refresh(primeiro)

    assert primeiro.vigencia_fim is None
    assert sessao.query(PrecoDeReferencia).count() == 1


def test_preco_fracionario_e_recusado(sessao, criar_persona, criar_tipo_de_recurso):
    admin = criar_persona(Papel.admin)
    tipo = criar_tipo_de_recurso(admin)

    with pytest.raises(ErroDeValidacao) as excinfo:
        registrar_preco_de_referencia(
            sessao,
            operador=admin,
            tipo=tipo,
            preco_em_pontos_extras=Decimal("20.5"),
            vigencia_inicio=date(2026, 1, 1),
        )
    assert excinfo.value.campo == "preco_em_pontos_extras"
    assert sessao.query(PrecoDeReferencia).count() == 0


def test_mestre_nao_registra_preco_de_referencia(sessao, criar_persona, criar_tipo_de_recurso):
    admin = criar_persona(Papel.admin)
    tipo = criar_tipo_de_recurso(admin)
    mestre = criar_persona(Papel.mestre)

    with pytest.raises(PermissaoNegada):
        registrar_preco_de_referencia(
            sessao,
            operador=mestre,
            tipo=tipo,
            preco_em_pontos_extras=20,
            vigencia_inicio=date(2026, 1, 1),
        )
    assert sessao.query(PrecoDeReferencia).count() == 0


def test_registrar_preco_em_pontos_nao_mexe_no_valor_em_moedas(
    sessao, criar_persona, criar_tipo_de_recurso
):
    admin = criar_persona(Papel.admin)
    tipo = criar_tipo_de_recurso(admin)
    registrar_valor_de_referencia(
        sessao,
        operador=admin,
        tipo=tipo,
        valor_em_moedas=Decimal("1.50"),
        vigencia_inicio=date(2026, 1, 1),
    )
    sessao.commit()

    registrar_preco_de_referencia(
        sessao,
        operador=admin,
        tipo=tipo,
        preco_em_pontos_extras=20,
        vigencia_inicio=date(2026, 1, 1),
    )
    sessao.commit()

    valor = consultar_valor_de_referencia(sessao, tipo=tipo, data=date(2026, 1, 1))
    assert valor.valor_em_moedas == Decimal("1.50")
    assert sessao.query(ValorDeReferencia).count() == 1
    assert sessao.query(PrecoDeReferencia).count() == 1


def test_tipo_com_preco_em_pontos_e_sem_valor_em_moedas(
    sessao, criar_persona, criar_tipo_de_recurso
):
    admin = criar_persona(Papel.admin)
    tipo = criar_tipo_de_recurso(admin)

    registrar_preco_de_referencia(
        sessao,
        operador=admin,
        tipo=tipo,
        preco_em_pontos_extras=20,
        vigencia_inicio=date(2026, 1, 1),
    )
    sessao.commit()

    valor = consultar_valor_de_referencia(sessao, tipo=tipo, data=date(2026, 1, 1))
    assert valor is None


def test_saida_do_preco_nao_traz_moedas_nem_reais(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_tipo_de_recurso
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    tipo = criar_tipo_de_recurso(admin)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.post(
        f"/v1/tipos-de-recurso/{tipo.id}/precos-de-referencia",
        json={"preco_em_pontos_extras": 20, "vigencia_inicio": "2026-01-01"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["preco_em_pontos_extras"] == 20
    assert "valor_em_moedas" not in corpo
    assert "valor_em_reais" not in corpo
