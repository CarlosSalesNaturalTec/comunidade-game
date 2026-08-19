from datetime import UTC, date, datetime, timedelta
from decimal import Decimal

import pytest

from nucleo.aportes.modelo import FormaDeAporte
from nucleo.aportes.regra import registrar_aporte
from nucleo.aulas.modelo import Aula
from nucleo.aulas.regra import RecursoDeclaradoEntrada, agendar_aula
from nucleo.catalogo_avulso.modelo import ItemDeCatalogoAvulso
from nucleo.catalogo_avulso.regra import cadastrar_item
from nucleo.erros import ErroDeValidacao
from nucleo.necessidades.regra import derivar_necessidades
from nucleo.personas.modelo import Papel
from nucleo.poder_sustentador.regra import poder_sustentador_de
from nucleo.recursos.modelo import NaturezaDoRecurso


@pytest.fixture
def cenario(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_valor_de_referencia,
):
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo_duravel = criar_tipo_de_recurso(admin, nome="Livro", natureza=NaturezaDoRecurso.duravel)
    criar_valor_de_referencia(admin, tipo_duravel, valor_em_moedas=Decimal("1.00"))
    return admin, apoiador, comunidade, ponto_de_apoio, tipo_duravel


def test_aporte_duravel_credita_poder_sustentador(sessao, cenario):
    admin, apoiador, _, ponto_de_apoio, tipo_duravel = cenario

    registrar_aporte(
        sessao,
        operador=admin,
        provedor=apoiador,
        tipo=tipo_duravel,
        quantidade=Decimal("5"),
        ponto_de_apoio=ponto_de_apoio,
        data_do_aporte=date(2026, 6, 1),
        forma=FormaDeAporte.material,
    )
    sessao.commit()

    assert poder_sustentador_de(sessao, provedor_id=apoiador.id) == Decimal("5.00")


def test_agendamento_com_tipo_duravel_e_recusado_mesmo_com_saldo_de_sobra(sessao, cenario):
    admin, apoiador, comunidade, ponto_de_apoio, tipo_duravel = cenario
    registrar_aporte(
        sessao,
        operador=admin,
        provedor=apoiador,
        tipo=tipo_duravel,
        quantidade=Decimal("46"),
        ponto_de_apoio=ponto_de_apoio,
        data_do_aporte=date(2026, 6, 1),
        forma=FormaDeAporte.material,
    )
    sessao.commit()

    agora = datetime.now(UTC)
    with pytest.raises(ErroDeValidacao) as excinfo:
        agendar_aula(
            sessao,
            operador=admin,
            comunidade=comunidade,
            ponto_de_apoio=ponto_de_apoio,
            inicio_em=agora + timedelta(days=1),
            fim_em=agora + timedelta(days=1, hours=1),
            recursos_declarados=[
                RecursoDeclaradoEntrada(tipo=tipo_duravel, quantidade=Decimal("1"))
            ],
        )
    assert excinfo.value.campo == "recursos_declarados"
    assert sessao.query(Aula).count() == 0
    assert derivar_necessidades(sessao) == []


def test_cadastro_de_item_de_catalogo_de_tipo_duravel_e_recusado(
    sessao, cenario, criar_persona, criar_vinculo_jogador
):
    admin, _, comunidade, ponto_de_apoio, tipo_duravel = cenario
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    criar_vinculo_jogador(mestre, comunidade)

    with pytest.raises(ErroDeValidacao) as excinfo:
        cadastrar_item(
            sessao,
            operador=mestre,
            nome="Livro tombado",
            tipo=tipo_duravel,
            estoque=Decimal("1"),
            comunidade=comunidade,
            ponto_de_apoio=ponto_de_apoio,
        )
    assert excinfo.value.campo == "tipo_de_recurso_id"
    assert sessao.query(ItemDeCatalogoAvulso).count() == 0


def test_item_de_catalogo_consumivel_sem_lastro_segue_aceito_e_inativo(
    sessao, cenario, criar_persona, criar_vinculo_jogador, criar_tipo_de_recurso
):
    admin, _, comunidade, ponto_de_apoio, _ = cenario
    tipo_consumivel = criar_tipo_de_recurso(
        admin, nome="Kit", natureza=NaturezaDoRecurso.consumivel
    )
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    criar_vinculo_jogador(mestre, comunidade)

    item = cadastrar_item(
        sessao,
        operador=mestre,
        nome="Kit sem lastro",
        tipo=tipo_consumivel,
        estoque=Decimal("1"),
        comunidade=comunidade,
        ponto_de_apoio=ponto_de_apoio,
    )
    sessao.commit()

    assert item.ativo is False
