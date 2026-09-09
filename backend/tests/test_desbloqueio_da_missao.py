import pytest

from nucleo.erros import ErroDeValidacao, NaoEncontrado, PermissaoNegada
from nucleo.personas.modelo import Papel
from nucleo.trilhas.modelo import (
    DesbloqueioDaMissao,
    RespostaDaSubmissao,
    SituacaoDaTrilha,
    SubmissaoDoDesbloqueio,
    TipoDeDesafioDeDesbloqueio,
)
from nucleo.trilhas.regra import (
    declarar_desafio_de_desbloqueio,
    inscrever_na_trilha,
    julgar_desafio_pratico,
    listar_desbloqueios_praticos_pendentes,
    perguntas_do_desbloqueio,
    submeter_desafio_de_desbloqueio,
)

ALTERNATIVAS = ["Um", "Dois", "Três", "Quatro"]


def _declarar_quiz(sessao, mestre, missao, alternativa_correta=2, quantidade=1):
    return declarar_desafio_de_desbloqueio(
        sessao,
        operador=mestre,
        missao=missao,
        tipo="quiz",
        perguntas=[
            {
                "enunciado": f"Pergunta {ordem}",
                "alternativas": ALTERNATIVAS,
                "alternativa_correta": alternativa_correta,
            }
            for ordem in range(1, quantidade + 1)
        ],
    )


def _responder(sessao, missao, escolhas):
    """As respostas na ordem das perguntas da missão (`RF-05-89`)."""
    return [
        {"pergunta_id": pergunta.id, "alternativa_escolhida": escolha}
        for pergunta, escolha in zip(
            perguntas_do_desbloqueio(sessao, missao_id=missao.id), escolhas, strict=True
        )
    ]


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
    perguntas = perguntas_do_desbloqueio(sessao, missao_id=missao.id)
    assert len(perguntas) == 1
    assert perguntas[0].enunciado == "Pergunta 1"
    assert perguntas[0].alternativa_correta == 2


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
    assert perguntas_do_desbloqueio(sessao, missao_id=missao.id) == []


def test_missao_sem_desafio_continua_valida(sessao, criar_persona, criar_trilha, criar_missao):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    assert missao.tipo_do_desafio_de_desbloqueio is None


def test_toda_pergunta_do_quiz_exige_quatro_alternativas(
    sessao, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    with pytest.raises(ErroDeValidacao):
        declarar_desafio_de_desbloqueio(
            sessao,
            operador=mestre,
            missao=missao,
            tipo="quiz",
            perguntas=[
                {"enunciado": "Pergunta", "alternativas": ["Só uma"], "alternativa_correta": 1}
            ],
        )


def test_quiz_sem_pergunta_e_recusado(sessao, criar_persona, criar_trilha, criar_missao):
    """`RN-09-43`."""
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    with pytest.raises(ErroDeValidacao):
        declarar_desafio_de_desbloqueio(
            sessao, operador=mestre, missao=missao, tipo="quiz", perguntas=[]
        )


def test_o_quiz_aceita_quantas_perguntas_o_mestre_declarar(
    sessao, criar_persona, criar_trilha, criar_missao
):
    """`RF-09-118`."""
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    _declarar_quiz(sessao, mestre, missao, quantidade=12)
    sessao.commit()

    perguntas = perguntas_do_desbloqueio(sessao, missao_id=missao.id)
    assert [pergunta.ordem for pergunta in perguntas] == list(range(1, 13))
    assert [pergunta.enunciado for pergunta in perguntas] == [
        f"Pergunta {ordem}" for ordem in range(1, 13)
    ]


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
        sessao, guerreiro=guerreiro, missao=missao, respostas=_responder(sessao, missao, [3])
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
        sessao, guerreiro=guerreiro_1, missao=missao, respostas=_responder(sessao, missao, [1])
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
        sessao, guerreiro=guerreiro, missao=missao, respostas=_responder(sessao, missao, [1])
    )
    sessao.commit()
    assert resultado.aprovado is False
    assert resultado.desbloqueio is None

    resultado_2 = submeter_desafio_de_desbloqueio(
        sessao, guerreiro=guerreiro, missao=missao, respostas=_responder(sessao, missao, [4])
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
            sessao, guerreiro=guerreiro, missao=missao, respostas=_responder(sessao, missao, [2])
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
        sessao, guerreiro=guerreiro, missao=missao, respostas=_responder(sessao, missao, [1])
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


def _quiz_com_corretas(sessao, mestre, missao, corretas):
    """Quiz cujas perguntas têm, cada uma, a correta que a lista indica."""
    return declarar_desafio_de_desbloqueio(
        sessao,
        operador=mestre,
        missao=missao,
        tipo="quiz",
        perguntas=[
            {
                "enunciado": f"Pergunta {ordem}",
                "alternativas": ALTERNATIVAS,
                "alternativa_correta": correta,
            }
            for ordem, correta in enumerate(corretas, start=1)
        ],
    )


def _trilha_inscrita(sessao, criar_persona, criar_trilha, criar_missao, **kwargs):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    missao = criar_missao(trilha, mestre, **kwargs)
    inscrever_na_trilha(sessao, guerreiro=guerreiro, trilha=trilha)
    sessao.commit()
    return mestre, guerreiro, trilha, missao


def test_acertar_60_por_cento_desbloqueia(sessao, criar_persona, criar_trilha, criar_missao):
    """`RN-05-45`: 3 de 5 é 60% e passa."""
    mestre, guerreiro, _, missao = _trilha_inscrita(
        sessao, criar_persona, criar_trilha, criar_missao
    )
    _quiz_com_corretas(sessao, mestre, missao, [1, 1, 1, 1, 1])
    sessao.commit()

    resultado = submeter_desafio_de_desbloqueio(
        sessao,
        guerreiro=guerreiro,
        missao=missao,
        respostas=_responder(sessao, missao, [1, 1, 1, 2, 2]),
    )
    sessao.commit()

    assert resultado.aprovado is True
    assert (resultado.acertos, resultado.total) == (3, 5)


def test_acertar_menos_de_60_por_cento_nao_desbloqueia(
    sessao, criar_persona, criar_trilha, criar_missao
):
    """`RN-05-45`: 5 de 10 é 50% e não passa; a devolutiva diz o placar."""
    mestre, guerreiro, _, missao = _trilha_inscrita(
        sessao, criar_persona, criar_trilha, criar_missao
    )
    _quiz_com_corretas(sessao, mestre, missao, [1] * 10)
    sessao.commit()

    resultado = submeter_desafio_de_desbloqueio(
        sessao,
        guerreiro=guerreiro,
        missao=missao,
        respostas=_responder(sessao, missao, [1] * 5 + [2] * 5),
    )
    sessao.commit()

    assert resultado.aprovado is False
    assert (resultado.acertos, resultado.total) == (5, 10)
    assert (
        sessao.query(DesbloqueioDaMissao)
        .filter_by(guerreiro_id=guerreiro.id, missao_id=missao.id)
        .first()
        is None
    )


def test_a_sondagem_abre_a_trilha_ao_ser_respondida(
    sessao, criar_persona, criar_trilha, criar_missao
):
    """`RN-05-46`: errar tudo na sondagem não tranca a trilha."""
    mestre, guerreiro, _, sondagem = _trilha_inscrita(
        sessao, criar_persona, criar_trilha, criar_missao, e_sondagem=True
    )
    _quiz_com_corretas(sessao, mestre, sondagem, [1, 1, 1, 1])
    sessao.commit()

    resultado = submeter_desafio_de_desbloqueio(
        sessao,
        guerreiro=guerreiro,
        missao=sondagem,
        respostas=_responder(sessao, sondagem, [2, 2, 2, 2]),
    )
    sessao.commit()

    assert resultado.aprovado is True
    assert (resultado.acertos, resultado.total) == (0, 4)


def test_toda_tentativa_fica_gravada_com_a_resposta_de_cada_pergunta(
    sessao, criar_persona, criar_trilha, criar_missao
):
    """`RN-05-47`: repetir acrescenta, nunca sobrescreve."""
    mestre, guerreiro, _, missao = _trilha_inscrita(
        sessao, criar_persona, criar_trilha, criar_missao
    )
    _quiz_com_corretas(sessao, mestre, missao, [1, 1])
    sessao.commit()

    submeter_desafio_de_desbloqueio(
        sessao, guerreiro=guerreiro, missao=missao, respostas=_responder(sessao, missao, [2, 2])
    )
    sessao.commit()
    submeter_desafio_de_desbloqueio(
        sessao, guerreiro=guerreiro, missao=missao, respostas=_responder(sessao, missao, [1, 1])
    )
    sessao.commit()

    submissoes = (
        sessao.query(SubmissaoDoDesbloqueio)
        .filter_by(guerreiro_id=guerreiro.id, missao_id=missao.id)
        .order_by(SubmissaoDoDesbloqueio.momento)
        .all()
    )
    assert [(s.acertos, s.total) for s in submissoes] == [(0, 2), (2, 2)]
    respostas_da_primeira = (
        sessao.query(RespostaDaSubmissao).filter_by(submissao_id=submissoes[0].id).all()
    )
    assert len(respostas_da_primeira) == 2
    assert all(resposta.acertou is False for resposta in respostas_da_primeira)


def test_submissao_sem_responder_todas_as_perguntas_e_recusada(
    sessao, criar_persona, criar_trilha, criar_missao
):
    """`RF-05-89`."""
    mestre, guerreiro, _, missao = _trilha_inscrita(
        sessao, criar_persona, criar_trilha, criar_missao
    )
    _quiz_com_corretas(sessao, mestre, missao, [1, 1, 1])
    sessao.commit()
    perguntas = perguntas_do_desbloqueio(sessao, missao_id=missao.id)

    with pytest.raises(ErroDeValidacao):
        submeter_desafio_de_desbloqueio(
            sessao,
            guerreiro=guerreiro,
            missao=missao,
            respostas=[{"pergunta_id": perguntas[0].id, "alternativa_escolhida": 1}],
        )


def test_resposta_repetida_ou_de_outra_missao_e_recusada(
    sessao, criar_persona, criar_trilha, criar_missao
):
    """`RF-05-89`."""
    mestre, guerreiro, trilha, missao = _trilha_inscrita(
        sessao, criar_persona, criar_trilha, criar_missao
    )
    _quiz_com_corretas(sessao, mestre, missao, [1, 1])
    outra = criar_missao(trilha, mestre, titulo="Outra", posicao=2)
    _quiz_com_corretas(sessao, mestre, outra, [1])
    sessao.commit()
    perguntas = perguntas_do_desbloqueio(sessao, missao_id=missao.id)
    de_outra = perguntas_do_desbloqueio(sessao, missao_id=outra.id)[0]

    with pytest.raises(ErroDeValidacao):
        submeter_desafio_de_desbloqueio(
            sessao,
            guerreiro=guerreiro,
            missao=missao,
            respostas=[
                {"pergunta_id": perguntas[0].id, "alternativa_escolhida": 1},
                {"pergunta_id": perguntas[0].id, "alternativa_escolhida": 2},
            ],
        )

    with pytest.raises(ErroDeValidacao):
        submeter_desafio_de_desbloqueio(
            sessao,
            guerreiro=guerreiro,
            missao=missao,
            respostas=[
                {"pergunta_id": perguntas[0].id, "alternativa_escolhida": 1},
                {"pergunta_id": de_outra.id, "alternativa_escolhida": 1},
            ],
        )
