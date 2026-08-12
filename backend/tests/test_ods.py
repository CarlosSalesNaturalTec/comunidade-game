from datetime import UTC, datetime

import pytest

from nucleo.erros import ErroDeValidacao, PermissaoNegada
from nucleo.ods.modelo import EtiquetaOds
from nucleo.ods.regra import (
    cobertura_por_comunidade,
    cobertura_por_poder,
    cobertura_por_trilha,
    criar_etiqueta_ods,
    resolver_etiquetas_da_missao,
)
from nucleo.personas.modelo import Papel
from nucleo.pontuacao.modelo import Nivel, PontoRegular
from nucleo.resultados.modelo import DesfechoDoResultado
from nucleo.resultados.regra import registrar_resultado
from nucleo.trilhas.modelo import FormatoDeAtividade, ModalidadeDeAtividade
from nucleo.trilhas.regra import criar_atividade

MOMENTO_DO_FATO = datetime(2026, 8, 1, 10, 0, tzinfo=UTC)


def _lancar_resultado(sessao, *, mestre, guerreiro, missao):
    atividade = criar_atividade(
        sessao,
        operador=mestre,
        missao=missao,
        modalidade=ModalidadeDeAtividade.individual,
        formato=FormatoDeAtividade.presencial,
        natureza="construcao",
        producao_esperada="Produção esperada.",
    )
    sessao.commit()
    resultado = registrar_resultado(
        sessao,
        operador=mestre,
        guerreiro_id=guerreiro.id,
        atividade=atividade,
        momento_do_fato=MOMENTO_DO_FATO,
        producao="Produção do Guerreiro(a).",
        desfecho=DesfechoDoResultado.realizada,
    )
    sessao.commit()
    return resultado


def test_mestre_autor_etiqueta_a_trilha(sessao, criar_persona, criar_trilha):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)

    etiqueta = criar_etiqueta_ods(sessao, operador=mestre, objetivo=4, meta="4.7", trilha=trilha)
    sessao.commit()

    assert etiqueta.trilha_id == trilha.id
    assert etiqueta.missao_id is None
    assert etiqueta.objetivo == 4
    assert etiqueta.meta == "4.7"


def test_mestre_autor_etiqueta_uma_missao_da_trilha(
    sessao, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    etiqueta = criar_etiqueta_ods(sessao, operador=mestre, objetivo=13, missao=missao)
    sessao.commit()

    assert etiqueta.missao_id == missao.id
    assert etiqueta.trilha_id is None


def test_trilha_aceita_mais_de_uma_etiqueta(sessao, criar_persona, criar_trilha):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)

    criar_etiqueta_ods(sessao, operador=mestre, objetivo=4, trilha=trilha)
    criar_etiqueta_ods(sessao, operador=mestre, objetivo=13, trilha=trilha)
    sessao.commit()

    assert sessao.query(EtiquetaOds).filter_by(trilha_id=trilha.id).count() == 2


def test_objetivo_fora_da_faixa_e_recusado(sessao, criar_persona, criar_trilha):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)

    with pytest.raises(ErroDeValidacao):
        criar_etiqueta_ods(sessao, operador=mestre, objetivo=0, trilha=trilha)
    with pytest.raises(ErroDeValidacao):
        criar_etiqueta_ods(sessao, operador=mestre, objetivo=19, trilha=trilha)
    assert sessao.query(EtiquetaOds).count() == 0


def test_etiqueta_sem_trilha_nem_missao_e_recusada(sessao, criar_persona):
    mestre = criar_persona(Papel.mestre)

    with pytest.raises(ErroDeValidacao):
        criar_etiqueta_ods(sessao, operador=mestre, objetivo=4)
    assert sessao.query(EtiquetaOds).count() == 0


def test_etiqueta_com_trilha_e_missao_ao_mesmo_tempo_e_recusada(
    sessao, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    with pytest.raises(ErroDeValidacao):
        criar_etiqueta_ods(sessao, operador=mestre, objetivo=4, trilha=trilha, missao=missao)
    assert sessao.query(EtiquetaOds).count() == 0


def test_mestre_que_nao_e_autor_e_recusado(sessao, criar_persona, criar_trilha):
    autor = criar_persona(Papel.mestre)
    outro_mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(autor)

    with pytest.raises(PermissaoNegada):
        criar_etiqueta_ods(sessao, operador=outro_mestre, objetivo=4, trilha=trilha)
    assert sessao.query(EtiquetaOds).count() == 0


def test_admin_etiqueta_trilha_de_qualquer_mestre(sessao, criar_persona, criar_trilha):
    autor = criar_persona(Papel.mestre)
    admin = criar_persona(Papel.admin)
    trilha = criar_trilha(autor)

    etiqueta = criar_etiqueta_ods(sessao, operador=admin, objetivo=4, trilha=trilha)
    sessao.commit()

    assert etiqueta.trilha_id == trilha.id


def test_missao_com_etiqueta_propria_prevalece_sobre_a_da_trilha(
    sessao, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    criar_etiqueta_ods(sessao, operador=mestre, objetivo=4, trilha=trilha)
    etiqueta_da_missao = criar_etiqueta_ods(sessao, operador=mestre, objetivo=13, missao=missao)
    sessao.commit()

    resolvidas = resolver_etiquetas_da_missao(sessao, missao)

    assert [e.id for e in resolvidas] == [etiqueta_da_missao.id]


def test_missao_sem_etiqueta_propria_herda_a_da_trilha(
    sessao, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    etiqueta_da_trilha = criar_etiqueta_ods(sessao, operador=mestre, objetivo=4, trilha=trilha)
    sessao.commit()

    resolvidas = resolver_etiquetas_da_missao(sessao, missao)

    assert [e.id for e in resolvidas] == [etiqueta_da_trilha.id]


def test_declarar_etiqueta_nao_credita_pontuacao(sessao, criar_persona, criar_trilha):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)

    criar_etiqueta_ods(sessao, operador=mestre, objetivo=4, trilha=trilha)
    sessao.commit()

    assert sessao.query(PontoRegular).count() == 0
    assert sessao.query(Nivel).count() == 0


def test_cobertura_por_trilha_soma_trilha_e_missoes(
    sessao, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    criar_etiqueta_ods(sessao, operador=mestre, objetivo=4, trilha=trilha)
    criar_etiqueta_ods(sessao, operador=mestre, objetivo=13, missao=missao)
    sessao.commit()

    cobertura = cobertura_por_trilha(sessao, trilha.id)

    assert cobertura == {4, 13}


def test_cobertura_por_poder_soma_as_trilhas_do_poder(
    sessao, criar_persona, criar_poder, criar_trilha
):
    mestre = criar_persona(Papel.mestre)
    poder = criar_poder(mestre)
    trilha_1 = criar_trilha(mestre, poder=poder)
    trilha_2 = criar_trilha(mestre, poder=poder)
    criar_etiqueta_ods(sessao, operador=mestre, objetivo=4, trilha=trilha_1)
    criar_etiqueta_ods(sessao, operador=mestre, objetivo=13, trilha=trilha_2)
    sessao.commit()

    cobertura = cobertura_por_poder(sessao, poder.id)

    assert cobertura == {4, 13}


def test_cobertura_por_comunidade_soma_trilhas_em_curso(
    sessao, criar_persona, criar_comunidade, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    criar_etiqueta_ods(sessao, operador=mestre, objetivo=4, trilha=trilha)
    sessao.commit()

    _lancar_resultado(sessao, mestre=mestre, guerreiro=guerreiro, missao=missao)

    cobertura = cobertura_por_comunidade(sessao, comunidade.id)

    assert cobertura == {4}


def test_cobertura_por_comunidade_sem_resultado_e_vazia(
    sessao, criar_persona, criar_comunidade, criar_trilha
):
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    trilha = criar_trilha(mestre)
    criar_etiqueta_ods(sessao, operador=mestre, objetivo=4, trilha=trilha)
    sessao.commit()

    cobertura = cobertura_por_comunidade(sessao, comunidade.id)

    assert cobertura == set()
