import pytest

from nucleo.erros import ErroDeValidacao
from nucleo.personas.modelo import Papel
from nucleo.trilhas.modelo import SituacaoDaTrilha
from nucleo.trilhas.regra import (
    declarar_desafio_de_desbloqueio,
    derivar_percurso,
    inscrever_na_trilha,
    obter_proxima_missao,
    submeter_desafio_de_desbloqueio,
)

ALTERNATIVAS = ["Um", "Dois", "Três", "Quatro"]


def _declarar_quiz(sessao, mestre, missao, alternativa_correta=1):
    return declarar_desafio_de_desbloqueio(
        sessao,
        operador=mestre,
        missao=missao,
        tipo="quiz",
        enunciado="Pergunta da missão.",
        alternativas=ALTERNATIVAS,
        alternativa_correta=alternativa_correta,
    )


def test_proxima_missao_e_a_de_menor_posicao_nao_desbloqueada(
    sessao, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    missao_1 = criar_missao(trilha, mestre, posicao=1)
    missao_2 = criar_missao(trilha, mestre, posicao=2)
    inscrever_na_trilha(sessao, guerreiro=guerreiro, trilha=trilha)
    sessao.commit()

    percurso = derivar_percurso(sessao, guerreiro_id=guerreiro.id, trilha_id=trilha.id)

    item_1 = next(item for item in percurso if item.missao.id == missao_1.id)
    item_2 = next(item for item in percurso if item.missao.id == missao_2.id)
    assert item_1.e_proxima is True
    assert item_2.e_proxima is False


def test_missao_bloqueada_diz_o_que_falta(sessao, criar_persona, criar_trilha, criar_missao):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    criar_missao(trilha, mestre, posicao=1, titulo="Primeira Missão")
    missao_2 = criar_missao(trilha, mestre, posicao=2, titulo="Segunda Missão")
    inscrever_na_trilha(sessao, guerreiro=guerreiro, trilha=trilha)
    sessao.commit()

    percurso = derivar_percurso(sessao, guerreiro_id=guerreiro.id, trilha_id=trilha.id)

    item_2 = next(item for item in percurso if item.missao.id == missao_2.id)
    assert item_2.desbloqueada is False
    assert "Primeira Missão" in item_2.motivo_do_bloqueio


def test_missao_ja_desbloqueada_permanece_aberta(sessao, criar_persona, criar_trilha, criar_missao):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    missao_1 = criar_missao(trilha, mestre, posicao=1)
    _declarar_quiz(sessao, mestre, missao_1)
    inscrever_na_trilha(sessao, guerreiro=guerreiro, trilha=trilha)
    sessao.commit()

    submeter_desafio_de_desbloqueio(
        sessao, guerreiro=guerreiro, missao=missao_1, alternativa_escolhida=1
    )
    sessao.commit()

    percurso = derivar_percurso(sessao, guerreiro_id=guerreiro.id, trilha_id=trilha.id)
    item_1 = next(item for item in percurso if item.missao.id == missao_1.id)
    assert item_1.desbloqueada is True

    percurso_de_novo = derivar_percurso(sessao, guerreiro_id=guerreiro.id, trilha_id=trilha.id)
    item_1_de_novo = next(item for item in percurso_de_novo if item.missao.id == missao_1.id)
    assert item_1_de_novo.desbloqueada is True


def test_percurso_de_terceiro_nao_e_servido(sessao, criar_persona, criar_trilha, criar_missao):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    outro_guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    criar_missao(trilha, mestre, posicao=1)
    inscrever_na_trilha(sessao, guerreiro=guerreiro, trilha=trilha)
    sessao.commit()

    with pytest.raises(ErroDeValidacao):
        derivar_percurso(sessao, guerreiro_id=outro_guerreiro.id, trilha_id=trilha.id)


def test_sondagem_e_a_proxima_missao_de_quem_acabou_de_se_inscrever(
    sessao, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    sondagem = criar_missao(trilha, mestre, posicao=1, e_sondagem=True)
    criar_missao(trilha, mestre, posicao=2)
    inscrever_na_trilha(sessao, guerreiro=guerreiro, trilha=trilha)
    sessao.commit()

    proxima = obter_proxima_missao(sessao, guerreiro_id=guerreiro.id, trilha_id=trilha.id)
    assert proxima.id == sondagem.id


def test_respondida_a_sondagem_a_primeira_missao_comum_abre(
    sessao, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    sondagem = criar_missao(trilha, mestre, posicao=1, e_sondagem=True)
    _declarar_quiz(sessao, mestre, sondagem)
    missao_comum = criar_missao(trilha, mestre, posicao=2)
    inscrever_na_trilha(sessao, guerreiro=guerreiro, trilha=trilha)
    sessao.commit()

    submeter_desafio_de_desbloqueio(
        sessao, guerreiro=guerreiro, missao=sondagem, alternativa_escolhida=1
    )
    sessao.commit()

    proxima = obter_proxima_missao(sessao, guerreiro_id=guerreiro.id, trilha_id=trilha.id)
    assert proxima.id == missao_comum.id


def test_sondagem_sem_nivel_nem_ponto(sessao, criar_persona, criar_trilha, criar_missao):
    from nucleo.pontuacao.modelo import Nivel, PontoRegular

    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    sondagem = criar_missao(trilha, mestre, posicao=1, e_sondagem=True, obrigatoria=False)
    _declarar_quiz(sessao, mestre, sondagem)
    inscrever_na_trilha(sessao, guerreiro=guerreiro, trilha=trilha)
    sessao.commit()

    submeter_desafio_de_desbloqueio(
        sessao, guerreiro=guerreiro, missao=sondagem, alternativa_escolhida=1
    )
    sessao.commit()

    assert (
        sessao.query(Nivel).filter_by(guerreiro_id=guerreiro.id, trilha_id=trilha.id).first()
        is None
    )
    assert (
        sessao.query(PontoRegular).filter_by(guerreiro_id=guerreiro.id, trilha_id=trilha.id).first()
        is None
    )


def test_missao_opcional_marcada_e_fora_da_conta(sessao, criar_persona, criar_trilha, criar_missao):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    criar_missao(trilha, mestre, posicao=1, obrigatoria=True)
    opcional = criar_missao(trilha, mestre, posicao=2, obrigatoria=False)
    inscrever_na_trilha(sessao, guerreiro=guerreiro, trilha=trilha)
    sessao.commit()

    percurso = derivar_percurso(sessao, guerreiro_id=guerreiro.id, trilha_id=trilha.id)
    item_opcional = next(item for item in percurso if item.missao.id == opcional.id)
    assert item_opcional.missao.obrigatoria is False


def test_aguardando_o_mestre_enquanto_o_pratico_nao_e_julgado(
    sessao, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    missao = criar_missao(trilha, mestre, posicao=1)
    declarar_desafio_de_desbloqueio(
        sessao,
        operador=mestre,
        missao=missao,
        tipo="pratico",
        enunciado="Mostre o que fez.",
    )
    inscrever_na_trilha(sessao, guerreiro=guerreiro, trilha=trilha)
    sessao.commit()

    submeter_desafio_de_desbloqueio(sessao, guerreiro=guerreiro, missao=missao)
    sessao.commit()

    percurso = derivar_percurso(sessao, guerreiro_id=guerreiro.id, trilha_id=trilha.id)
    item = next(item for item in percurso if item.missao.id == missao.id)
    assert item.aguardando_mestre is True
    assert item.desbloqueada is False
