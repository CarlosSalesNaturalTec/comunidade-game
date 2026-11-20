"""A finalidade do tipo de recurso: consumo do encontro ou recompensa, uma só
por tipo não durável, nenhuma no durável; a aula escolhe consumo do encontro e
as três recompensas escolhem recompensa (`RF-07-53`, `RF-07-01`, `RF-07-51`,
`RN-07-41`, `RF-02-31`, `RF-09-71`, `RF-09-84`)."""

from datetime import date, timedelta
from decimal import Decimal

import pytest

from nucleo.aulas.modelo import Aula, SituacaoDaAula
from nucleo.aulas.regra import RecursoDeclaradoEntrada, agendar_aula
from nucleo.catalogo_avulso.modelo import ItemDeCatalogoAvulso
from nucleo.catalogo_avulso.regra import cadastrar_item
from nucleo.desafios_extras.modelo import DesafioExtra
from nucleo.erros import ErroDeValidacao, PermissaoNegada
from nucleo.personas.modelo import Papel
from nucleo.recompensas_de_marco.modelo import RecompensaDeMarco
from nucleo.recompensas_de_marco.regra import declarar_recompensa_de_marco
from nucleo.recursos.modelo import FinalidadeDoRecurso, NaturezaDoRecurso, TipoDeRecurso
from nucleo.recursos.regra import alterar_tipo_de_recurso, cadastrar_tipo_de_recurso
from nucleo.tempo import agora
from nucleo.trilhas.modelo import SituacaoDaTrilha
from tests.test_desafio_extra_regra import _propor

# --- O catálogo -------------------------------------------------------------


def test_admin_cadastra_tipo_com_finalidade(sessao, criar_persona):
    admin = criar_persona(Papel.admin)

    tipo = cadastrar_tipo_de_recurso(
        sessao,
        operador=admin,
        nome="Lanche",
        natureza=NaturezaDoRecurso.consumivel.value,
        unidade="unidade",
        finalidade="consumo_do_encontro",
    )

    assert tipo.finalidade == FinalidadeDoRecurso.consumo_do_encontro


def test_tipo_nao_duravel_sem_finalidade_e_recusado(sessao, criar_persona):
    admin = criar_persona(Papel.admin)

    with pytest.raises(ErroDeValidacao) as erro:
        cadastrar_tipo_de_recurso(
            sessao,
            operador=admin,
            nome="Monitor",
            natureza=NaturezaDoRecurso.servico.value,
            unidade="diária",
        )
    assert erro.value.campo == "finalidade"
    assert sessao.query(TipoDeRecurso).count() == 0


def test_finalidade_fora_das_duas_previstas_e_recusada(sessao, criar_persona):
    admin = criar_persona(Papel.admin)

    with pytest.raises(ErroDeValidacao) as erro:
        cadastrar_tipo_de_recurso(
            sessao,
            operador=admin,
            nome="Lanche",
            natureza=NaturezaDoRecurso.consumivel.value,
            unidade="unidade",
            finalidade="brinde",
        )
    assert erro.value.campo == "finalidade"


def test_tipo_duravel_nao_tem_finalidade(sessao, criar_persona):
    admin = criar_persona(Papel.admin)

    with pytest.raises(ErroDeValidacao) as erro:
        cadastrar_tipo_de_recurso(
            sessao,
            operador=admin,
            nome="Notebook",
            natureza=NaturezaDoRecurso.duravel.value,
            unidade="unidade",
            finalidade="recompensa",
        )
    assert erro.value.campo == "finalidade"

    tipo = cadastrar_tipo_de_recurso(
        sessao,
        operador=admin,
        nome="Notebook",
        natureza=NaturezaDoRecurso.duravel.value,
        unidade="unidade",
    )
    assert tipo.finalidade is None


def test_admin_passa_um_tipo_a_consumo_do_encontro(sessao, criar_persona, criar_tipo_de_recurso):
    admin = criar_persona(Papel.admin)
    tipo = criar_tipo_de_recurso(admin, finalidade="recompensa")

    alterar_tipo_de_recurso(sessao, tipo, operador=admin, finalidade="consumo_do_encontro")

    assert tipo.finalidade == FinalidadeDoRecurso.consumo_do_encontro


def test_finalidade_em_tipo_duravel_e_recusada_na_correcao(
    sessao, criar_persona, criar_tipo_de_recurso
):
    admin = criar_persona(Papel.admin)
    tipo = criar_tipo_de_recurso(admin, natureza=NaturezaDoRecurso.duravel)

    with pytest.raises(ErroDeValidacao) as erro:
        alterar_tipo_de_recurso(sessao, tipo, operador=admin, finalidade="recompensa")
    assert erro.value.campo == "finalidade"
    assert tipo.finalidade is None


def test_mestre_nao_corrige_a_finalidade(sessao, criar_persona, criar_tipo_de_recurso):
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    tipo = criar_tipo_de_recurso(admin, finalidade="recompensa")

    with pytest.raises(PermissaoNegada):
        alterar_tipo_de_recurso(sessao, tipo, operador=mestre, finalidade="consumo_do_encontro")
    assert tipo.finalidade == FinalidadeDoRecurso.recompensa


def test_a_correcao_nao_alcanca_a_recompensa_ja_declarada(
    sessao, criar_persona, criar_tipo_de_recurso, criar_trilha, criar_missao
):
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    tipo = criar_tipo_de_recurso(admin, nome="Kit", finalidade="recompensa")
    trilha = criar_trilha(mestre)
    recompensa = declarar_recompensa_de_marco(
        sessao,
        operador=mestre,
        trilha=trilha,
        missao=criar_missao(trilha, mestre),
        tipo=tipo,
        quantidade=Decimal("1"),
    )
    sessao.commit()

    alterar_tipo_de_recurso(sessao, tipo, operador=admin, finalidade="consumo_do_encontro")
    sessao.commit()

    assert sessao.get(RecompensaDeMarco, recompensa.id).tipo_de_recurso_id == tipo.id


# --- As quatro escolhas novas --------------------------------------------------


@pytest.fixture
def cenario(sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto = criar_ponto_de_apoio(admin, comunidade)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    return admin, comunidade, ponto, mestre


def _agendar(sessao, admin, comunidade, ponto, mestre, tipo):
    inicio = agora() + timedelta(days=1)
    return agendar_aula(
        sessao,
        operador=admin,
        comunidade=comunidade,
        ponto_de_apoio=ponto,
        mestres=[mestre],
        inicio_em=inicio,
        fim_em=inicio + timedelta(hours=1),
        recursos_declarados=[RecursoDeclaradoEntrada(tipo=tipo, quantidade=Decimal("1"))],
    )


def test_aula_que_declara_kit_de_recompensa_e_recusada(sessao, cenario, criar_tipo_de_recurso):
    admin, comunidade, ponto, mestre = cenario
    kit = criar_tipo_de_recurso(admin, nome="Kit Robô", finalidade="recompensa")

    with pytest.raises(ErroDeValidacao) as erro:
        _agendar(sessao, admin, comunidade, ponto, mestre, kit)
    assert erro.value.campo == "recursos_declarados"
    assert sessao.query(Aula).count() == 0


def test_aula_que_declara_lanche_e_aceita(
    sessao, cenario, criar_tipo_de_recurso, criar_lancamento, criar_valor_de_referencia
):
    admin, comunidade, ponto, mestre = cenario
    lanche = criar_tipo_de_recurso(admin, finalidade="consumo_do_encontro")
    criar_valor_de_referencia(admin, lanche, vigencia_inicio=date(2026, 1, 1))
    criar_lancamento(admin, lanche, ponto, quantidade=Decimal("5"))

    aula = _agendar(sessao, admin, comunidade, ponto, mestre, lanche)

    assert aula.situacao == SituacaoDaAula.confirmada


def test_recompensa_com_tipo_de_consumo_do_encontro_e_recusada(
    sessao, criar_persona, criar_tipo_de_recurso, criar_trilha, criar_missao
):
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    lanche = criar_tipo_de_recurso(admin, finalidade="consumo_do_encontro")
    trilha = criar_trilha(mestre)

    with pytest.raises(ErroDeValidacao) as erro:
        declarar_recompensa_de_marco(
            sessao,
            operador=mestre,
            trilha=trilha,
            missao=criar_missao(trilha, mestre),
            tipo=lanche,
            quantidade=Decimal("1"),
        )
    assert erro.value.campo == "tipo_de_recurso_id"
    assert sessao.query(RecompensaDeMarco).count() == 0


def test_recompensa_com_tipo_duravel_e_recusada_na_declaracao(
    sessao, criar_persona, criar_tipo_de_recurso, criar_trilha, criar_missao
):
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    notebook = criar_tipo_de_recurso(admin, nome="Notebook", natureza=NaturezaDoRecurso.duravel)
    trilha = criar_trilha(mestre)

    with pytest.raises(ErroDeValidacao):
        declarar_recompensa_de_marco(
            sessao,
            operador=mestre,
            trilha=trilha,
            missao=criar_missao(trilha, mestre),
            tipo=notebook,
            quantidade=Decimal("1"),
        )
    assert sessao.query(RecompensaDeMarco).count() == 0


def test_item_avulso_com_tipo_de_consumo_do_encontro_e_recusado(
    sessao, cenario, criar_tipo_de_recurso, criar_vinculo_do_mestre
):
    admin, comunidade, ponto, mestre = cenario
    criar_vinculo_do_mestre(mestre, comunidade)
    lanche = criar_tipo_de_recurso(admin, finalidade="consumo_do_encontro")

    with pytest.raises(ErroDeValidacao) as erro:
        cadastrar_item(
            sessao,
            operador=mestre,
            nome="Lanche",
            tipo=lanche,
            estoque=Decimal("1"),
            comunidade=comunidade,
            ponto_de_apoio=ponto,
        )
    assert erro.value.campo == "tipo_de_recurso_id"
    assert sessao.query(ItemDeCatalogoAvulso).count() == 0


def test_desafio_com_recompensa_de_consumo_do_encontro_e_recusado(
    sessao, cenario, criar_persona, criar_tipo_de_recurso, criar_trilha
):
    admin, _comunidade, ponto, mestre = cenario
    apoiador = criar_persona(Papel.apoiador, criada_por=admin)
    lanche = criar_tipo_de_recurso(admin, finalidade="consumo_do_encontro")
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)

    with pytest.raises(ErroDeValidacao) as erro:
        _propor(sessao, apoiador=apoiador, trilha=trilha, tipo=lanche, ponto=ponto)
    assert erro.value.campo == "tipo_de_recurso_id"
    assert sessao.query(DesafioExtra).count() == 0
