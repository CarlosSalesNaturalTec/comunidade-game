import inspect

import pytest

from nucleo.erros import ErroDeValidacao, PermissaoNegada
from nucleo.personas.modelo import Papel
from nucleo.trilhas.modelo import EtapaDoCiclo, Missao, SituacaoDaTrilha
from nucleo.trilhas.regra import criar_missao, declarar_cadencia_de_retomada


def test_missao_criada_com_posicao_e_dificuldade(sessao, criar_persona, criar_trilha):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)

    missao = criar_missao(
        sessao,
        operador=mestre,
        trilha=trilha,
        titulo="Primeira missão",
        posicao=1,
        nivel_de_dificuldade=1,
        obrigatoria=True,
        etapa_do_ciclo=EtapaDoCiclo.abertura,
    )
    sessao.commit()

    assert missao.trilha_id == trilha.id
    assert missao.titulo == "Primeira missão"
    assert missao.posicao == 1
    assert missao.etapa_do_ciclo == EtapaDoCiclo.abertura
    assert missao.autor_id == mestre.id


def test_missao_sem_trilha_e_recusada(sessao, criar_persona):
    mestre = criar_persona(Papel.mestre)

    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_missao(
            sessao,
            operador=mestre,
            trilha=None,
            titulo="Missão",
            posicao=1,
            nivel_de_dificuldade=1,
            obrigatoria=True,
            etapa_do_ciclo=EtapaDoCiclo.abertura,
        )
    assert excinfo.value.campo == "trilha_id"
    assert sessao.query(Missao).count() == 0


def test_missao_sem_titulo_e_recusada(sessao, criar_persona, criar_trilha):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)

    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_missao(
            sessao,
            operador=mestre,
            trilha=trilha,
            titulo=None,
            posicao=1,
            nivel_de_dificuldade=1,
            obrigatoria=True,
            etapa_do_ciclo=EtapaDoCiclo.abertura,
        )
    assert excinfo.value.campo == "titulo"
    assert sessao.query(Missao).count() == 0


def test_missao_sem_declaracao_de_obrigatoria_e_recusada(sessao, criar_persona, criar_trilha):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)

    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_missao(
            sessao,
            operador=mestre,
            trilha=trilha,
            titulo="Missão",
            posicao=1,
            nivel_de_dificuldade=1,
            obrigatoria=None,
            etapa_do_ciclo=EtapaDoCiclo.abertura,
        )
    assert excinfo.value.campo == "obrigatoria"
    assert sessao.query(Missao).count() == 0


def test_etapa_fora_dos_quatro_valores_e_recusada(sessao, criar_persona, criar_trilha):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)

    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_missao(
            sessao,
            operador=mestre,
            trilha=trilha,
            titulo="Missão",
            posicao=1,
            nivel_de_dificuldade=1,
            obrigatoria=True,
            etapa_do_ciclo="etapa-inexistente",
        )
    assert excinfo.value.campo == "etapa_do_ciclo"
    assert sessao.query(Missao).count() == 0


def test_missao_sem_retomada_e_aceita(sessao, criar_persona, criar_trilha):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)

    missao = criar_missao(
        sessao,
        operador=mestre,
        trilha=trilha,
        titulo="Missão",
        posicao=1,
        nivel_de_dificuldade=1,
        obrigatoria=True,
        etapa_do_ciclo=EtapaDoCiclo.abertura,
    )
    sessao.commit()

    assert missao.cadencia_de_retomada is None


def test_sondagem_na_primeira_posicao_e_aceita(sessao, criar_persona, criar_trilha):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)

    missao = criar_missao(
        sessao,
        operador=mestre,
        trilha=trilha,
        titulo="Sondagem",
        posicao=1,
        nivel_de_dificuldade=1,
        obrigatoria=True,
        etapa_do_ciclo=EtapaDoCiclo.abertura,
        e_sondagem=True,
    )
    sessao.commit()

    assert missao.e_sondagem is True


def test_segunda_sondagem_na_mesma_trilha_e_recusada(sessao, criar_persona, criar_trilha):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    criar_missao(
        sessao,
        operador=mestre,
        trilha=trilha,
        titulo="Sondagem",
        posicao=1,
        nivel_de_dificuldade=1,
        obrigatoria=True,
        etapa_do_ciclo=EtapaDoCiclo.abertura,
        e_sondagem=True,
    )
    sessao.commit()

    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_missao(
            sessao,
            operador=mestre,
            trilha=trilha,
            titulo="Segunda sondagem",
            posicao=1,
            nivel_de_dificuldade=1,
            obrigatoria=True,
            etapa_do_ciclo=EtapaDoCiclo.abertura,
            e_sondagem=True,
        )
    assert excinfo.value.campo == "e_sondagem"
    assert "já tem" in excinfo.value.mensagem
    assert sessao.query(Missao).filter_by(trilha_id=trilha.id, e_sondagem=True).count() == 1


def test_sondagem_fora_da_primeira_posicao_e_recusada(sessao, criar_persona, criar_trilha):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)

    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_missao(
            sessao,
            operador=mestre,
            trilha=trilha,
            titulo="Sondagem",
            posicao=2,
            nivel_de_dificuldade=1,
            obrigatoria=True,
            etapa_do_ciclo=EtapaDoCiclo.abertura,
            e_sondagem=True,
        )
    assert excinfo.value.campo == "e_sondagem"
    assert sessao.query(Missao).count() == 0


def test_trilha_em_rascunho_existe_sem_sondagem(sessao, criar_persona, criar_trilha):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.rascunho)

    missao = criar_missao(
        sessao,
        operador=mestre,
        trilha=trilha,
        titulo="Missão",
        posicao=1,
        nivel_de_dificuldade=1,
        obrigatoria=True,
        etapa_do_ciclo=EtapaDoCiclo.abertura,
    )
    sessao.commit()

    assert missao.e_sondagem is False
    assert trilha.situacao == SituacaoDaTrilha.rascunho


def test_dificuldade_nunca_deriva_da_idade_do_guerreiro(sessao):
    """Documento 99 §6 invariante 2: a assinatura de `criar_missao` não tem
    parâmetro de idade nem de data de nascimento — a dificuldade só entra
    pelo que o Mestre autor declara."""
    parametros = set(inspect.signature(criar_missao).parameters)
    assert not any("idade" in nome or "nascimento" in nome for nome in parametros)


def test_mestre_autor_declara_a_cadencia_de_retomada(
    sessao, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    resultado = declarar_cadencia_de_retomada(
        sessao, operador=mestre, missao=missao, cadencia_de_retomada=[2, 7, 21]
    )
    sessao.commit()

    assert resultado.cadencia_de_retomada == [2, 7, 21]


def test_cadencia_declarada_depois_substitui_a_anterior(
    sessao, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    declarar_cadencia_de_retomada(
        sessao, operador=mestre, missao=missao, cadencia_de_retomada=[2, 7, 21]
    )
    sessao.commit()

    resultado = declarar_cadencia_de_retomada(
        sessao, operador=mestre, missao=missao, cadencia_de_retomada=[3]
    )
    sessao.commit()

    assert resultado.cadencia_de_retomada == [3]


def test_mestre_nao_autor_e_recusado_ao_declarar_cadencia(
    sessao, criar_persona, criar_trilha, criar_missao
):
    mestre_autor = criar_persona(Papel.mestre)
    outro_mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre_autor)
    missao = criar_missao(trilha, mestre_autor)

    with pytest.raises(PermissaoNegada):
        declarar_cadencia_de_retomada(
            sessao, operador=outro_mestre, missao=missao, cadencia_de_retomada=[2, 7, 21]
        )
