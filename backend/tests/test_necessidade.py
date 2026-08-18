from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nucleo.aportes.regra import registrar_aporte_por_absorcao
from nucleo.aulas.modelo import SituacaoDaAula
from nucleo.necessidades.regra import (
    consultar_necessidades_do_mestre,
    consultar_necessidades_publicas,
    derivar_necessidades,
)
from nucleo.personas.modelo import Papel
from nucleo.reservas.regra import confirmar_aulas_pendentes


def _tornar_pendente(sessao, aula):
    aula.situacao = SituacaoDaAula.pendente_de_lastro
    sessao.commit()


def test_falta_de_aula_pendente_vira_necessidade(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_valor_de_referencia,
    criar_lancamento,
    criar_aula,
    criar_recurso_declarado_da_aula,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    criar_valor_de_referencia(admin, tipo, valor_em_moedas=Decimal("0.50"))
    criar_lancamento(admin, tipo, ponto_de_apoio, quantidade=Decimal("4.00"))
    aula = criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)
    criar_recurso_declarado_da_aula(aula, tipo, quantidade=Decimal("10.00"))
    _tornar_pendente(sessao, aula)

    necessidades = derivar_necessidades(sessao)

    assert len(necessidades) == 1
    necessidade = necessidades[0]
    assert necessidade.aula_id == aula.id
    assert necessidade.tipo_de_recurso_id == tipo.id
    assert necessidade.quantidade_faltante == Decimal("6.00")
    assert necessidade.valor_em_moedas == Decimal("3.00")


def test_tipo_ja_coberto_nao_aparece(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_lancamento,
    criar_aula,
    criar_recurso_declarado_da_aula,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo_coberto = criar_tipo_de_recurso(admin, nome="Água")
    tipo_faltante = criar_tipo_de_recurso(admin, nome="Lanche")
    criar_lancamento(admin, tipo_coberto, ponto_de_apoio, quantidade=Decimal("5.00"))
    aula = criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)
    criar_recurso_declarado_da_aula(aula, tipo_coberto, quantidade=Decimal("5.00"))
    criar_recurso_declarado_da_aula(aula, tipo_faltante, quantidade=Decimal("2.00"))
    _tornar_pendente(sessao, aula)

    necessidades = derivar_necessidades(sessao)

    assert len(necessidades) == 1
    assert necessidades[0].tipo_de_recurso_id == tipo_faltante.id


@pytest.mark.parametrize(
    "situacao",
    [
        SituacaoDaAula.prevista,
        SituacaoDaAula.confirmada,
        SituacaoDaAula.realizada,
        SituacaoDaAula.cancelada,
    ],
)
def test_aula_em_outra_situacao_nao_gera_necessidade(
    situacao,
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_aula,
    criar_recurso_declarado_da_aula,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    aula = criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)
    criar_recurso_declarado_da_aula(aula, tipo, quantidade=Decimal("10.00"))
    aula.situacao = situacao
    sessao.commit()

    necessidades = derivar_necessidades(sessao)

    assert necessidades == []


def test_duas_aulas_disputando_o_mesmo_saldo(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_lancamento,
    criar_aula,
    criar_recurso_declarado_da_aula,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    criar_lancamento(admin, tipo, ponto_de_apoio, quantidade=Decimal("6.00"))
    agora = datetime.now(UTC)

    aula_distante = criar_aula(
        admin,
        comunidade,
        ponto_de_apoio=ponto_de_apoio,
        inicio_em=agora + timedelta(days=5),
        fim_em=agora + timedelta(days=5, hours=1),
    )
    aula_proxima = criar_aula(
        admin,
        comunidade,
        ponto_de_apoio=ponto_de_apoio,
        inicio_em=agora + timedelta(days=1),
        fim_em=agora + timedelta(days=1, hours=1),
    )
    criar_recurso_declarado_da_aula(aula_distante, tipo, quantidade=Decimal("10.00"))
    criar_recurso_declarado_da_aula(aula_proxima, tipo, quantidade=Decimal("10.00"))
    _tornar_pendente(sessao, aula_distante)
    _tornar_pendente(sessao, aula_proxima)

    necessidades = derivar_necessidades(sessao)

    por_aula = {necessidade.aula_id: necessidade for necessidade in necessidades}
    assert por_aula[aula_proxima.id].quantidade_faltante == Decimal("4.00")
    assert por_aula[aula_distante.id].quantidade_faltante == Decimal("10.00")
    assert sum(n.quantidade_faltante for n in necessidades) == Decimal("14.00")


def test_ordem_da_derivacao_e_da_confirmacao_e_a_mesma(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_lancamento,
    criar_aula,
    criar_recurso_declarado_da_aula,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    agora = datetime.now(UTC)

    aula_distante = criar_aula(
        admin,
        comunidade,
        ponto_de_apoio=ponto_de_apoio,
        inicio_em=agora + timedelta(days=5),
        fim_em=agora + timedelta(days=5, hours=1),
    )
    aula_proxima = criar_aula(
        admin,
        comunidade,
        ponto_de_apoio=ponto_de_apoio,
        inicio_em=agora + timedelta(days=1),
        fim_em=agora + timedelta(days=1, hours=1),
    )
    criar_recurso_declarado_da_aula(aula_distante, tipo, quantidade=Decimal("6.00"))
    criar_recurso_declarado_da_aula(aula_proxima, tipo, quantidade=Decimal("6.00"))
    _tornar_pendente(sessao, aula_distante)
    _tornar_pendente(sessao, aula_proxima)

    # Só há disponível para a mais próxima — o mesmo cenário de
    # `test_reserva.test_confirmar_aulas_pendentes_atende_a_mais_proxima_primeiro`.
    criar_lancamento(admin, tipo, ponto_de_apoio, quantidade=Decimal("6.00"))
    confirmadas = confirmar_aulas_pendentes(
        sessao, tipo=tipo, ponto_de_apoio=ponto_de_apoio, operador=admin
    )
    sessao.commit()

    assert [a.id for a in confirmadas] == [aula_proxima.id]

    necessidades_apos = derivar_necessidades(sessao)
    assert [n.aula_id for n in necessidades_apos] == [aula_distante.id]


def test_aula_com_horario_passado_continua_na_lista(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_aula,
    criar_recurso_declarado_da_aula,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    agora = datetime.now(UTC)
    aula = criar_aula(
        admin,
        comunidade,
        ponto_de_apoio=ponto_de_apoio,
        inicio_em=agora - timedelta(days=2),
        fim_em=agora - timedelta(days=2) + timedelta(hours=1),
    )
    criar_recurso_declarado_da_aula(aula, tipo, quantidade=Decimal("3.00"))
    _tornar_pendente(sessao, aula)

    necessidades = derivar_necessidades(sessao)

    assert len(necessidades) == 1
    assert necessidades[0].aula_id == aula.id
    assert necessidades[0].quantidade_faltante == Decimal("3.00")


def test_aporte_parcial_abate_a_falta(
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
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    criar_valor_de_referencia(admin, tipo)
    aula = criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)
    criar_recurso_declarado_da_aula(aula, tipo, quantidade=Decimal("6.00"))
    _tornar_pendente(sessao, aula)

    registrar_aporte_por_absorcao(
        sessao,
        operador=mestre,
        tipo=tipo,
        quantidade=Decimal("2.00"),
        ponto_de_apoio=ponto_de_apoio,
        data_do_aporte=aula.inicio_em.date(),
        valor_de_origem=Decimal("20.00"),
    )
    sessao.commit()
    sessao.refresh(aula)

    assert aula.situacao == SituacaoDaAula.pendente_de_lastro
    necessidades = derivar_necessidades(sessao)
    assert len(necessidades) == 1
    assert necessidades[0].quantidade_faltante == Decimal("4.00")


def test_aporte_que_fecha_o_saldo_apaga_a_necessidade_e_confirma_a_aula(
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
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    criar_valor_de_referencia(admin, tipo)
    aula = criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)
    criar_recurso_declarado_da_aula(aula, tipo, quantidade=Decimal("6.00"))
    _tornar_pendente(sessao, aula)

    registrar_aporte_por_absorcao(
        sessao,
        operador=mestre,
        tipo=tipo,
        quantidade=Decimal("6.00"),
        ponto_de_apoio=ponto_de_apoio,
        data_do_aporte=aula.inicio_em.date(),
        valor_de_origem=Decimal("60.00"),
    )
    sessao.commit()
    sessao.refresh(aula)

    assert aula.situacao == SituacaoDaAula.confirmada
    assert derivar_necessidades(sessao) == []


def test_cada_provedor_recebe_as_moedas_do_que_aportou(
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
    mestre_um = criar_persona(Papel.mestre)
    mestre_dois = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    criar_valor_de_referencia(admin, tipo, valor_em_moedas=Decimal("2.00"))
    aula = criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)
    criar_recurso_declarado_da_aula(aula, tipo, quantidade=Decimal("6.00"))
    _tornar_pendente(sessao, aula)

    aporte_um = registrar_aporte_por_absorcao(
        sessao,
        operador=mestre_um,
        tipo=tipo,
        quantidade=Decimal("2.00"),
        ponto_de_apoio=ponto_de_apoio,
        data_do_aporte=aula.inicio_em.date(),
        valor_de_origem=Decimal("20.00"),
    )
    sessao.commit()
    aporte_dois = registrar_aporte_por_absorcao(
        sessao,
        operador=mestre_dois,
        tipo=tipo,
        quantidade=Decimal("4.00"),
        ponto_de_apoio=ponto_de_apoio,
        data_do_aporte=aula.inicio_em.date(),
        valor_de_origem=Decimal("40.00"),
    )
    sessao.commit()
    sessao.refresh(aula)

    assert aporte_um.provedor_id == mestre_um.id
    assert aporte_um.valor_em_moedas == Decimal("4.00")
    assert aporte_dois.provedor_id == mestre_dois.id
    assert aporte_dois.valor_em_moedas == Decimal("8.00")
    assert aula.situacao == SituacaoDaAula.confirmada
    assert derivar_necessidades(sessao) == []


def test_falta_valorada_pela_vigencia_corrente(
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
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    criar_valor_de_referencia(admin, tipo, valor_em_moedas=Decimal("0.50"))
    aula = criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)
    criar_recurso_declarado_da_aula(aula, tipo, quantidade=Decimal("3.00"))
    _tornar_pendente(sessao, aula)

    necessidades = derivar_necessidades(sessao)

    assert necessidades[0].valor_em_moedas == Decimal("1.50")


def test_tipo_sem_vigencia_sai_sem_valor(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_aula,
    criar_recurso_declarado_da_aula,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    aula = criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)
    criar_recurso_declarado_da_aula(aula, tipo, quantidade=Decimal("3.00"))
    _tornar_pendente(sessao, aula)

    necessidades = derivar_necessidades(sessao)

    assert len(necessidades) == 1
    assert necessidades[0].quantidade_faltante == Decimal("3.00")
    assert necessidades[0].valor_em_moedas is None


def test_lista_do_mestre_alcanca_as_comunidades_a_que_ele_esta_vinculado(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_aula,
    criar_recurso_declarado_da_aula,
    criar_vinculo_jogador,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    outra_comunidade = criar_comunidade()
    mestre = criar_persona(Papel.mestre)
    criar_vinculo_jogador(mestre, comunidade)

    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    ponto_de_apoio_alheio = criar_ponto_de_apoio(admin, outra_comunidade)
    tipo = criar_tipo_de_recurso(admin)

    aula = criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)
    criar_recurso_declarado_da_aula(aula, tipo, quantidade=Decimal("2.00"))
    _tornar_pendente(sessao, aula)

    aula_alheia = criar_aula(admin, outra_comunidade, ponto_de_apoio=ponto_de_apoio_alheio)
    criar_recurso_declarado_da_aula(aula_alheia, tipo, quantidade=Decimal("2.00"))
    _tornar_pendente(sessao, aula_alheia)

    necessidades = consultar_necessidades_do_mestre(sessao, operador=mestre)

    assert [n.aula_id for n in necessidades] == [aula.id]


def test_necessidades_publicas_alcancam_todas_as_comunidades(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_aula,
    criar_recurso_declarado_da_aula,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    aula = criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)
    criar_recurso_declarado_da_aula(aula, tipo, quantidade=Decimal("2.00"))
    _tornar_pendente(sessao, aula)

    necessidades = consultar_necessidades_publicas(sessao)

    assert [n.aula_id for n in necessidades] == [aula.id]
