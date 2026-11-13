"""O tipo de recurso desativado sai só da escolha nova; o ato que segue fato
já existente continua aceito (`RF-07-52`, design — decisão 6)."""

from datetime import date, timedelta
from decimal import Decimal

import pytest

from nucleo.aportes.modelo import FormaDeAporte
from nucleo.aportes.regra import registrar_aporte, registrar_aporte_por_absorcao
from nucleo.aulas.modelo import SituacaoDaAula
from nucleo.aulas.regra import RecursoDeclaradoEntrada, agendar_aula
from nucleo.catalogo_avulso.regra import cadastrar_item
from nucleo.erros import ErroDeValidacao
from nucleo.livro_razao.regra import transferir_saldo
from nucleo.personas.modelo import Papel
from nucleo.recompensas_de_marco.regra import declarar_recompensa_de_marco
from nucleo.tempo import agora
from nucleo.trilhas.modelo import SituacaoDaTrilha
from tests.test_desafio_extra_regra import _propor


@pytest.fixture
def desativado(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_valor_de_referencia,
    criar_preco_de_referencia,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    criar_valor_de_referencia(admin, tipo)
    criar_preco_de_referencia(admin, tipo)
    tipo.ativo = False
    sessao.commit()
    return admin, comunidade, ponto, tipo


def _recusa_pelo_tipo(erro, campo="tipo_de_recurso_id"):
    assert erro.value.campo == campo
    assert "desativado" in erro.value.mensagem


def test_agendar_aula_com_tipo_desativado_e_recusado(sessao, criar_persona, desativado):
    admin, comunidade, ponto, tipo = desativado
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    inicio = agora() + timedelta(days=1)

    with pytest.raises(ErroDeValidacao) as erro:
        agendar_aula(
            sessao,
            operador=admin,
            comunidade=comunidade,
            ponto_de_apoio=ponto,
            mestres=[mestre],
            inicio_em=inicio,
            fim_em=inicio + timedelta(hours=1),
            recursos_declarados=[RecursoDeclaradoEntrada(tipo=tipo, quantidade=Decimal("1"))],
        )
    _recusa_pelo_tipo(erro, campo="recursos_declarados")


def test_registrar_aporte_com_tipo_desativado_e_recusado(sessao, criar_persona, desativado):
    admin, _comunidade, ponto, tipo = desativado
    apoiador = criar_persona(Papel.apoiador, criada_por=admin)

    with pytest.raises(ErroDeValidacao) as erro:
        registrar_aporte(
            sessao,
            operador=admin,
            provedor=apoiador,
            tipo=tipo,
            quantidade=Decimal("1"),
            ponto_de_apoio=ponto,
            data_do_aporte=date(2026, 6, 1),
            forma=FormaDeAporte.material,
        )
    _recusa_pelo_tipo(erro)


def test_absorcao_sem_aula_com_tipo_desativado_e_recusada(sessao, criar_persona, desativado):
    admin, _comunidade, ponto, tipo = desativado
    mestre = criar_persona(Papel.mestre, criada_por=admin)

    with pytest.raises(ErroDeValidacao) as erro:
        registrar_aporte_por_absorcao(
            sessao,
            operador=mestre,
            tipo=tipo,
            quantidade=Decimal("1"),
            ponto_de_apoio=ponto,
            data_do_aporte=date(2026, 6, 1),
            valor_de_origem=Decimal("1.00"),
        )
    _recusa_pelo_tipo(erro)


def test_absorcao_da_necessidade_ja_publicada_segue_aceita(
    sessao, criar_persona, criar_aula, criar_recurso_declarado_da_aula, desativado
):
    admin, comunidade, ponto, tipo = desativado
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    aula = criar_aula(admin, comunidade, ponto_de_apoio=ponto)
    criar_recurso_declarado_da_aula(aula, tipo, quantidade=Decimal("2.00"))
    aula.situacao = SituacaoDaAula.pendente_de_lastro
    sessao.commit()

    aporte = registrar_aporte_por_absorcao(
        sessao,
        operador=mestre,
        tipo=tipo,
        quantidade=Decimal("2"),
        ponto_de_apoio=ponto,
        data_do_aporte=date(2026, 6, 1),
        aula=aula,
        valor_de_origem=Decimal("2.00"),
    )

    assert aporte.aula_id == aula.id


def test_declarar_recompensa_com_tipo_desativado_e_recusado(
    sessao, criar_persona, criar_trilha, criar_missao, desativado
):
    admin, _comunidade, _ponto, tipo = desativado
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    trilha = criar_trilha(mestre)

    with pytest.raises(ErroDeValidacao) as erro:
        declarar_recompensa_de_marco(
            sessao,
            operador=mestre,
            trilha=trilha,
            missao=criar_missao(trilha, mestre),
            tipo=tipo,
            quantidade=Decimal("1"),
        )
    _recusa_pelo_tipo(erro)


def test_item_avulso_com_tipo_desativado_e_recusado(sessao, criar_persona, desativado):
    admin, comunidade, ponto, tipo = desativado
    mestre = criar_persona(Papel.mestre, criada_por=admin)

    with pytest.raises(ErroDeValidacao) as erro:
        cadastrar_item(
            sessao,
            operador=mestre,
            nome="Kit",
            tipo=tipo,
            estoque=Decimal("1"),
            comunidade=comunidade,
            ponto_de_apoio=ponto,
        )
    _recusa_pelo_tipo(erro)


def test_desafio_extra_com_tipo_desativado_e_recusado(
    sessao, criar_persona, criar_trilha, desativado
):
    admin, _comunidade, ponto, tipo = desativado
    apoiador = criar_persona(Papel.apoiador, criada_por=admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)

    with pytest.raises(ErroDeValidacao) as erro:
        trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
        _propor(sessao, apoiador=apoiador, trilha=trilha, tipo=tipo, ponto=ponto)
    _recusa_pelo_tipo(erro)


def test_transferencia_de_saldo_de_tipo_desativado_segue_aceita(
    sessao, criar_ponto_de_apoio, criar_lancamento, desativado
):
    admin, comunidade, ponto, tipo = desativado
    destino = criar_ponto_de_apoio(admin, comunidade, nome="Outro ponto")
    criar_lancamento(admin, tipo, ponto, quantidade=Decimal("3.00"))

    debito, credito = transferir_saldo(
        sessao,
        operador=admin,
        tipo_de_recurso=tipo,
        ponto_de_apoio_origem=ponto,
        ponto_de_apoio_destino=destino,
        quantidade=Decimal("3.00"),
        motivo="Mudança de sede",
    )

    assert credito.ponto_de_apoio_id == destino.id
