from datetime import UTC, datetime
from decimal import Decimal

import pytest

from nucleo.aulas.modelo import SituacaoDaAula
from nucleo.erros import ErroDeValidacao, PermissaoNegada
from nucleo.livro_razao.modelo import Lancamento, NaturezaDoLancamento
from nucleo.livro_razao.regra import saldo_de
from nucleo.personas.modelo import Papel
from nucleo.reservas.modelo import EstadoDaReserva, Reserva
from nucleo.resultados.modelo import DesfechoDoResultado, Resultado
from nucleo.resultados.regra import ResultadoDeclarado, lancar_atividade_realizada

MOMENTO_DO_FATO = datetime(2026, 8, 1, 10, 0, tzinfo=UTC)


def _entrada(guerreiro, atividade, desfecho=DesfechoDoResultado.realizada):
    return ResultadoDeclarado(
        guerreiro_id=guerreiro.id,
        atividade=atividade,
        momento_do_fato=MOMENTO_DO_FATO,
        producao="Produção do Guerreiro(a).",
        desfecho=desfecho,
    )


def test_lancamento_gera_um_debito_por_reserva_e_derruba_o_saldo(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_lancamento,
    criar_valor_de_referencia,
    criar_aula,
    criar_reserva,
    criar_trilha,
    criar_missao,
    criar_atividade,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo_um = criar_tipo_de_recurso(admin, nome="Lanche")
    tipo_dois = criar_tipo_de_recurso(admin, nome="Kit")
    criar_lancamento(admin, tipo_um, ponto_de_apoio, quantidade=Decimal("10.00"))
    criar_lancamento(admin, tipo_dois, ponto_de_apoio, quantidade=Decimal("10.00"))
    criar_valor_de_referencia(admin, tipo_um, valor_em_moedas=Decimal("1.00"))
    criar_valor_de_referencia(admin, tipo_dois, valor_em_moedas=Decimal("2.00"))
    aula = criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)
    criar_reserva(admin, aula, tipo_um, ponto_de_apoio, quantidade=Decimal("3.00"))
    criar_reserva(admin, aula, tipo_dois, ponto_de_apoio, quantidade=Decimal("2.00"))

    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    trilha = criar_trilha(admin)
    missao = criar_missao(trilha, admin)
    atividade = criar_atividade(missao, admin)

    aula_atualizada, resultados = lancar_atividade_realizada(
        sessao,
        operador=admin,
        aula=aula,
        resultados=[_entrada(guerreiro, atividade)],
    )
    sessao.commit()

    assert aula_atualizada.situacao == SituacaoDaAula.realizada
    assert len(resultados) == 1

    reservas = sessao.query(Reserva).filter_by(aula_id=aula.id).all()
    assert len(reservas) == 2
    assert all(r.estado == EstadoDaReserva.consumida for r in reservas)

    debitos = sessao.query(Lancamento).filter_by(natureza=NaturezaDoLancamento.debito).all()
    assert len(debitos) == 2
    assert {(d.tipo_de_recurso_id, d.quantidade) for d in debitos} == {
        (tipo_um.id, Decimal("3.00")),
        (tipo_dois.id, Decimal("2.00")),
    }

    assert saldo_de(
        sessao, tipo_de_recurso_id=tipo_um.id, ponto_de_apoio_id=ponto_de_apoio.id
    ) == Decimal("7.00")
    assert saldo_de(
        sessao, tipo_de_recurso_id=tipo_dois.id, ponto_de_apoio_id=ponto_de_apoio.id
    ) == Decimal("8.00")


def test_lancamento_de_aula_sem_reservas_apenas_registra_os_resultados(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_trilha,
    criar_missao,
    criar_atividade,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade)
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    trilha = criar_trilha(admin)
    missao = criar_missao(trilha, admin)
    atividade = criar_atividade(missao, admin)

    aula_atualizada, resultados = lancar_atividade_realizada(
        sessao,
        operador=admin,
        aula=aula,
        resultados=[_entrada(guerreiro, atividade)],
    )
    sessao.commit()

    assert aula_atualizada.situacao == SituacaoDaAula.realizada
    assert len(resultados) == 1
    assert sessao.query(Lancamento).filter_by(natureza=NaturezaDoLancamento.debito).count() == 0
    assert sessao.query(Resultado).filter_by(aula_id=aula.id).count() == 1


def test_mestre_nao_lanca_a_atividade_da_aula(sessao, criar_persona, criar_comunidade, criar_aula):
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade)

    with pytest.raises(PermissaoNegada):
        lancar_atividade_realizada(sessao, operador=mestre, aula=aula, resultados=[])
    sessao.refresh(aula)
    assert aula.situacao != SituacaoDaAula.realizada


def test_lancamento_em_aula_ja_realizada_e_recusado(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_trilha,
    criar_missao,
    criar_atividade,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade)
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    trilha = criar_trilha(admin)
    missao = criar_missao(trilha, admin)
    atividade = criar_atividade(missao, admin)

    lancar_atividade_realizada(
        sessao, operador=admin, aula=aula, resultados=[_entrada(guerreiro, atividade)]
    )
    sessao.commit()

    with pytest.raises(ErroDeValidacao) as excinfo:
        lancar_atividade_realizada(
            sessao, operador=admin, aula=aula, resultados=[_entrada(guerreiro, atividade)]
        )
    assert excinfo.value.campo == "situacao"


def test_lancamento_em_aula_cancelada_e_recusado(
    sessao, criar_persona, criar_comunidade, criar_aula
):
    from nucleo.aulas.regra import cancelar_aula

    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade)
    cancelar_aula(sessao, operador=admin, aula=aula, motivo="Chuva forte.")
    sessao.commit()

    with pytest.raises(ErroDeValidacao) as excinfo:
        lancar_atividade_realizada(sessao, operador=admin, aula=aula, resultados=[])
    assert excinfo.value.campo == "situacao"
