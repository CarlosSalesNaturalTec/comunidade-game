from datetime import UTC, datetime

import pytest

from nucleo.erros import ErroDeValidacao, PermissaoNegada
from nucleo.personas.modelo import Papel
from nucleo.pontuacao.modelo import PontoRegular
from nucleo.resultados.modelo import DesfechoDoResultado, Resultado
from nucleo.resultados.regra import registrar_resultado
from tests.conftest import criar_aula_para_resultado

MOMENTO_DO_FATO = datetime(2026, 8, 1, 10, 0, tzinfo=UTC)


def test_resultado_registrado_com_producao_declarada(
    sessao, criar_persona, criar_trilha, criar_missao, criar_atividade
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    atividade = criar_atividade(missao, mestre)
    aula = criar_aula_para_resultado(sessao, mestre)

    resultado = registrar_resultado(
        sessao,
        operador=mestre,
        aula=aula,
        guerreiro_id=guerreiro.id,
        atividade=atividade,
        momento_do_fato=MOMENTO_DO_FATO,
        producao="Construiu o próprio robô.",
        desfecho=DesfechoDoResultado.realizada,
    )
    sessao.commit()

    assert resultado.guerreiro_id == guerreiro.id
    assert resultado.atividade_id == atividade.id
    assert resultado.aula_id == aula.id
    assert resultado.momento_do_fato == MOMENTO_DO_FATO
    assert resultado.desfecho == DesfechoDoResultado.realizada


def test_resultado_sem_atividade_e_recusado(sessao, criar_persona):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    aula = criar_aula_para_resultado(sessao, mestre)

    with pytest.raises(ErroDeValidacao) as excinfo:
        registrar_resultado(
            sessao,
            operador=mestre,
            aula=aula,
            guerreiro_id=guerreiro.id,
            atividade=None,
            momento_do_fato=MOMENTO_DO_FATO,
            producao="Construiu algo.",
            desfecho=DesfechoDoResultado.realizada,
        )
    assert excinfo.value.campo == "atividade_id"
    assert sessao.query(Resultado).count() == 0


def test_resultado_sem_guerreiro_e_recusado(
    sessao, criar_persona, criar_trilha, criar_missao, criar_atividade
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    atividade = criar_atividade(missao, mestre)
    aula = criar_aula_para_resultado(sessao, mestre)

    with pytest.raises(ErroDeValidacao) as excinfo:
        registrar_resultado(
            sessao,
            operador=mestre,
            aula=aula,
            guerreiro_id=None,
            atividade=atividade,
            momento_do_fato=MOMENTO_DO_FATO,
            producao="Construiu algo.",
            desfecho=DesfechoDoResultado.realizada,
        )
    assert excinfo.value.campo == "guerreiro_id"
    assert sessao.query(Resultado).count() == 0


def test_resultado_sem_aula_e_recusado(
    sessao, criar_persona, criar_trilha, criar_missao, criar_atividade
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    atividade = criar_atividade(missao, mestre)

    with pytest.raises(ErroDeValidacao) as excinfo:
        registrar_resultado(
            sessao,
            operador=mestre,
            aula=None,
            guerreiro_id=guerreiro.id,
            atividade=atividade,
            momento_do_fato=MOMENTO_DO_FATO,
            producao="Construiu algo.",
            desfecho=DesfechoDoResultado.realizada,
        )
    assert excinfo.value.campo == "aula_id"
    assert sessao.query(Resultado).count() == 0


def test_resultado_sem_producao_e_recusado(
    sessao, criar_persona, criar_trilha, criar_missao, criar_atividade
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    atividade = criar_atividade(missao, mestre)
    aula = criar_aula_para_resultado(sessao, mestre)

    with pytest.raises(ErroDeValidacao) as excinfo:
        registrar_resultado(
            sessao,
            operador=mestre,
            aula=aula,
            guerreiro_id=guerreiro.id,
            atividade=atividade,
            momento_do_fato=MOMENTO_DO_FATO,
            producao=None,
            desfecho=DesfechoDoResultado.realizada,
        )
    assert excinfo.value.campo == "producao"
    assert sessao.query(Resultado).count() == 0


def test_resultado_sem_data_do_fato_e_recusado(
    sessao, criar_persona, criar_trilha, criar_missao, criar_atividade
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    atividade = criar_atividade(missao, mestre)
    aula = criar_aula_para_resultado(sessao, mestre)

    with pytest.raises(ErroDeValidacao) as excinfo:
        registrar_resultado(
            sessao,
            operador=mestre,
            aula=aula,
            guerreiro_id=guerreiro.id,
            atividade=atividade,
            momento_do_fato=None,
            producao="Construiu algo.",
            desfecho=DesfechoDoResultado.realizada,
        )
    assert excinfo.value.campo == "momento_do_fato"
    assert sessao.query(Resultado).count() == 0


def test_resultado_sem_desfecho_e_recusado(
    sessao, criar_persona, criar_trilha, criar_missao, criar_atividade
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    atividade = criar_atividade(missao, mestre)
    aula = criar_aula_para_resultado(sessao, mestre)

    with pytest.raises(ErroDeValidacao) as excinfo:
        registrar_resultado(
            sessao,
            operador=mestre,
            aula=aula,
            guerreiro_id=guerreiro.id,
            atividade=atividade,
            momento_do_fato=MOMENTO_DO_FATO,
            producao="Construiu algo.",
            desfecho=None,
        )
    assert excinfo.value.campo == "desfecho"
    assert sessao.query(Resultado).count() == 0


def test_desfecho_fora_dos_valores_previstos_e_recusado(
    sessao, criar_persona, criar_trilha, criar_missao, criar_atividade
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    atividade = criar_atividade(missao, mestre)
    aula = criar_aula_para_resultado(sessao, mestre)

    with pytest.raises(ErroDeValidacao) as excinfo:
        registrar_resultado(
            sessao,
            operador=mestre,
            aula=aula,
            guerreiro_id=guerreiro.id,
            atividade=atividade,
            momento_do_fato=MOMENTO_DO_FATO,
            producao="Construiu algo.",
            desfecho="desfecho-inexistente",
        )
    assert excinfo.value.campo == "desfecho"
    assert sessao.query(Resultado).count() == 0


def test_mestre_que_nao_e_autor_e_recusado(
    sessao, criar_persona, criar_trilha, criar_missao, criar_atividade
):
    mestre_autor = criar_persona(Papel.mestre)
    outro_mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre_autor)
    missao = criar_missao(trilha, mestre_autor)
    atividade = criar_atividade(missao, mestre_autor)
    aula = criar_aula_para_resultado(sessao, mestre_autor)

    with pytest.raises(PermissaoNegada):
        registrar_resultado(
            sessao,
            operador=outro_mestre,
            aula=aula,
            guerreiro_id=guerreiro.id,
            atividade=atividade,
            momento_do_fato=MOMENTO_DO_FATO,
            producao="Construiu algo.",
            desfecho=DesfechoDoResultado.realizada,
        )
    assert sessao.query(Resultado).count() == 0


def test_admin_lanca_desfecho_mesmo_sem_ser_o_autor(
    sessao, criar_persona, criar_trilha, criar_missao, criar_atividade
):
    mestre_autor = criar_persona(Papel.mestre)
    admin = criar_persona(Papel.admin)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre_autor)
    missao = criar_missao(trilha, mestre_autor)
    atividade = criar_atividade(missao, mestre_autor)
    aula = criar_aula_para_resultado(sessao, admin)

    resultado = registrar_resultado(
        sessao,
        operador=admin,
        aula=aula,
        guerreiro_id=guerreiro.id,
        atividade=atividade,
        momento_do_fato=MOMENTO_DO_FATO,
        producao="Construiu algo.",
        desfecho=DesfechoDoResultado.realizada,
    )
    sessao.commit()

    assert resultado.autor_id == admin.id


def test_autoria_de_quem_lancou_fica_gravada(
    sessao, criar_persona, criar_trilha, criar_missao, criar_atividade
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    atividade = criar_atividade(missao, mestre)
    aula = criar_aula_para_resultado(sessao, mestre)

    resultado = registrar_resultado(
        sessao,
        operador=mestre,
        aula=aula,
        guerreiro_id=guerreiro.id,
        atividade=atividade,
        momento_do_fato=MOMENTO_DO_FATO,
        producao="Construiu algo.",
        desfecho=DesfechoDoResultado.realizada_com_merito,
    )
    sessao.commit()

    assert resultado.autor_id == mestre.id
    assert resultado.papel_do_autor == Papel.mestre.value
    assert resultado.registrado_em is not None


def test_registrar_resultado_credita_a_pontuacao_na_mesma_operacao(
    sessao, criar_persona, criar_trilha, criar_missao, criar_atividade
):
    """O Resultado não fica isolado: a mesma chamada credita o ponto
    regular, encerrando o que a proposta descreve como "entrega os dois
    juntos" (`RF-01-20`, `RF-01-21`)."""
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    atividade = criar_atividade(missao, mestre)
    aula = criar_aula_para_resultado(sessao, mestre)

    registrar_resultado(
        sessao,
        operador=mestre,
        aula=aula,
        guerreiro_id=guerreiro.id,
        atividade=atividade,
        momento_do_fato=MOMENTO_DO_FATO,
        producao="Construiu algo.",
        desfecho=DesfechoDoResultado.realizada,
    )
    sessao.commit()

    conta = (
        sessao.query(PontoRegular).filter_by(guerreiro_id=guerreiro.id, trilha_id=trilha.id).one()
    )
    assert conta.total == 10
