import pytest

from nucleo.erros import ErroDeValidacao, NaoEncontrado, PermissaoNegada
from nucleo.personas.modelo import Papel
from nucleo.trilhas.modelo import DesbloqueioDaMissao, SituacaoDaTrilha, TipoDeDesafioDeDesbloqueio
from nucleo.trilhas.regra import (
    declarar_desafio_de_desbloqueio,
    inscrever_na_trilha,
    julgar_desafio_pratico,
    listar_desbloqueios_praticos_pendentes,
    submeter_desafio_de_desbloqueio,
)

ALTERNATIVAS = ["Um", "Dois", "Três", "Quatro"]


def _declarar_quiz(sessao, mestre, missao, alternativa_correta=2):
    return declarar_desafio_de_desbloqueio(
        sessao,
        operador=mestre,
        missao=missao,
        tipo="quiz",
        enunciado="Quanto é 1 + 1?",
        alternativas=ALTERNATIVAS,
        alternativa_correta=alternativa_correta,
    )


def _declarar_pratico(sessao, mestre, missao):
    return declarar_desafio_de_desbloqueio(
        sessao,
        operador=mestre,
        missao=missao,
        tipo="pratico",
        enunciado="Monte o robô e mostre ao Mestre.",
    )


def test_mestre_autor_declara_o_desafio_da_sua_missao(
    sessao, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    missao = _declarar_quiz(sessao, mestre, missao)
    sessao.commit()

    assert missao.tipo_do_desafio_de_desbloqueio == TipoDeDesafioDeDesbloqueio.quiz
    assert missao.desafio_de_desbloqueio_enunciado == "Quanto é 1 + 1?"
    assert missao.desafio_de_desbloqueio_alternativa_correta == 2


def test_quem_nao_e_autor_nao_declara(sessao, criar_persona, criar_trilha, criar_missao):
    mestre = criar_persona(Papel.mestre)
    outro_mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    with pytest.raises(PermissaoNegada):
        _declarar_quiz(sessao, outro_mestre, missao)


def test_declarar_de_novo_substitui_o_desafio_anterior(
    sessao, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    _declarar_quiz(sessao, mestre, missao)
    sessao.commit()

    missao = _declarar_pratico(sessao, mestre, missao)
    sessao.commit()

    assert missao.tipo_do_desafio_de_desbloqueio == TipoDeDesafioDeDesbloqueio.pratico
    assert missao.desafio_de_desbloqueio_enunciado == "Monte o robô e mostre ao Mestre."
    assert missao.desafio_de_desbloqueio_alternativa_correta is None


def test_missao_sem_desafio_continua_valida(sessao, criar_persona, criar_trilha, criar_missao):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    assert missao.tipo_do_desafio_de_desbloqueio is None


def test_quiz_exige_quatro_alternativas(sessao, criar_persona, criar_trilha, criar_missao):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    with pytest.raises(ErroDeValidacao):
        declarar_desafio_de_desbloqueio(
            sessao,
            operador=mestre,
            missao=missao,
            tipo="quiz",
            enunciado="Pergunta",
            alternativas=["Só uma"],
            alternativa_correta=1,
        )


def test_passar_no_quiz_desbloqueia_a_missao_para_quem_submeteu(
    sessao, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    missao = criar_missao(trilha, mestre)
    _declarar_quiz(sessao, mestre, missao, alternativa_correta=3)
    inscrever_na_trilha(sessao, guerreiro=guerreiro, trilha=trilha)
    sessao.commit()

    resultado = submeter_desafio_de_desbloqueio(
        sessao, guerreiro=guerreiro, missao=missao, alternativa_escolhida=3
    )
    sessao.commit()

    assert resultado.aprovado is True
    assert resultado.desbloqueio is not None
    desbloqueio = (
        sessao.query(DesbloqueioDaMissao)
        .filter_by(guerreiro_id=guerreiro.id, missao_id=missao.id)
        .one()
    )
    assert desbloqueio.aprovado is True


def test_desbloqueio_de_um_nao_desbloqueia_os_colegas(
    sessao, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    guerreiro_1 = criar_persona(Papel.guerreiro)
    guerreiro_2 = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    missao = criar_missao(trilha, mestre)
    _declarar_quiz(sessao, mestre, missao, alternativa_correta=1)
    inscrever_na_trilha(sessao, guerreiro=guerreiro_1, trilha=trilha)
    inscrever_na_trilha(sessao, guerreiro=guerreiro_2, trilha=trilha)
    sessao.commit()

    submeter_desafio_de_desbloqueio(
        sessao, guerreiro=guerreiro_1, missao=missao, alternativa_escolhida=1
    )
    sessao.commit()

    assert (
        sessao.query(DesbloqueioDaMissao)
        .filter_by(guerreiro_id=guerreiro_2.id, missao_id=missao.id)
        .first()
        is None
    )


def test_nao_passar_permite_repetir_sem_punicao(sessao, criar_persona, criar_trilha, criar_missao):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    missao = criar_missao(trilha, mestre)
    _declarar_quiz(sessao, mestre, missao, alternativa_correta=4)
    inscrever_na_trilha(sessao, guerreiro=guerreiro, trilha=trilha)
    sessao.commit()

    resultado = submeter_desafio_de_desbloqueio(
        sessao, guerreiro=guerreiro, missao=missao, alternativa_escolhida=1
    )
    sessao.commit()
    assert resultado.aprovado is False
    assert resultado.desbloqueio is None

    resultado_2 = submeter_desafio_de_desbloqueio(
        sessao, guerreiro=guerreiro, missao=missao, alternativa_escolhida=4
    )
    sessao.commit()
    assert resultado_2.aprovado is True


def test_submissao_sem_inscricao_e_recusada(sessao, criar_persona, criar_trilha, criar_missao):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    missao = criar_missao(trilha, mestre)
    _declarar_quiz(sessao, mestre, missao)
    sessao.commit()

    with pytest.raises(ErroDeValidacao):
        submeter_desafio_de_desbloqueio(
            sessao, guerreiro=guerreiro, missao=missao, alternativa_escolhida=2
        )


def test_desbloqueio_nao_credita_ponto(sessao, criar_persona, criar_trilha, criar_missao):
    from nucleo.pontuacao.modelo import PontoRegular

    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    missao = criar_missao(trilha, mestre)
    _declarar_quiz(sessao, mestre, missao, alternativa_correta=1)
    inscrever_na_trilha(sessao, guerreiro=guerreiro, trilha=trilha)
    sessao.commit()

    submeter_desafio_de_desbloqueio(
        sessao, guerreiro=guerreiro, missao=missao, alternativa_escolhida=1
    )
    sessao.commit()

    assert (
        sessao.query(PontoRegular).filter_by(guerreiro_id=guerreiro.id, trilha_id=trilha.id).first()
        is None
    )


def test_mestre_autor_julga_o_pratico_e_a_missao_desbloqueia(
    sessao, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    missao = criar_missao(trilha, mestre)
    _declarar_pratico(sessao, mestre, missao)
    inscrever_na_trilha(sessao, guerreiro=guerreiro, trilha=trilha)
    sessao.commit()

    resultado = submeter_desafio_de_desbloqueio(sessao, guerreiro=guerreiro, missao=missao)
    sessao.commit()
    assert resultado.aprovado is None

    desbloqueio = (
        sessao.query(DesbloqueioDaMissao)
        .filter_by(guerreiro_id=guerreiro.id, missao_id=missao.id)
        .one()
    )
    julgado = julgar_desafio_pratico(
        sessao, operador=mestre, desbloqueio=desbloqueio, aprovado=True
    )
    sessao.commit()

    assert julgado.aprovado is True
    assert julgado.julgado_por_id == mestre.id


def test_enquanto_o_mestre_nao_julga_nada_e_reprovado(
    sessao, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    missao = criar_missao(trilha, mestre)
    _declarar_pratico(sessao, mestre, missao)
    inscrever_na_trilha(sessao, guerreiro=guerreiro, trilha=trilha)
    sessao.commit()

    submeter_desafio_de_desbloqueio(sessao, guerreiro=guerreiro, missao=missao)
    sessao.commit()

    pendentes = listar_desbloqueios_praticos_pendentes(sessao, operador=mestre)
    assert len(pendentes) == 1
    assert pendentes[0].aprovado is None


def test_quem_nao_e_autor_nao_julga(sessao, criar_persona, criar_trilha, criar_missao):
    mestre = criar_persona(Papel.mestre)
    outro_mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    missao = criar_missao(trilha, mestre)
    _declarar_pratico(sessao, mestre, missao)
    inscrever_na_trilha(sessao, guerreiro=guerreiro, trilha=trilha)
    sessao.commit()

    submeter_desafio_de_desbloqueio(sessao, guerreiro=guerreiro, missao=missao)
    sessao.commit()
    desbloqueio = (
        sessao.query(DesbloqueioDaMissao)
        .filter_by(guerreiro_id=guerreiro.id, missao_id=missao.id)
        .one()
    )

    with pytest.raises(PermissaoNegada):
        julgar_desafio_pratico(
            sessao, operador=outro_mestre, desbloqueio=desbloqueio, aprovado=True
        )


def test_julgado_como_nao_passou_o_guerreiro_declara_de_novo(
    sessao, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    missao = criar_missao(trilha, mestre)
    _declarar_pratico(sessao, mestre, missao)
    inscrever_na_trilha(sessao, guerreiro=guerreiro, trilha=trilha)
    sessao.commit()

    submeter_desafio_de_desbloqueio(sessao, guerreiro=guerreiro, missao=missao)
    sessao.commit()
    desbloqueio = (
        sessao.query(DesbloqueioDaMissao)
        .filter_by(guerreiro_id=guerreiro.id, missao_id=missao.id)
        .one()
    )

    resultado = julgar_desafio_pratico(
        sessao, operador=mestre, desbloqueio=desbloqueio, aprovado=False
    )
    sessao.commit()
    assert resultado is None
    assert (
        sessao.query(DesbloqueioDaMissao)
        .filter_by(guerreiro_id=guerreiro.id, missao_id=missao.id)
        .first()
        is None
    )

    nova_declaracao = submeter_desafio_de_desbloqueio(sessao, guerreiro=guerreiro, missao=missao)
    sessao.commit()
    assert nova_declaracao.aprovado is None


def test_julgar_declaracao_inexistente_e_recusado(sessao, criar_persona):
    mestre = criar_persona(Papel.mestre)
    with pytest.raises(NaoEncontrado):
        julgar_desafio_pratico(sessao, operador=mestre, desbloqueio=None, aprovado=True)
