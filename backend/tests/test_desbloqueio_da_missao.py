import uuid

import pytest

from nucleo.erros import ErroDeValidacao, NaoEncontrado, PermissaoNegada
from nucleo.personas.modelo import Papel
from nucleo.trilhas.modelo import (
    DesbloqueioDaMissao,
    PerguntaDoDesbloqueio,
    RespostaDaSubmissao,
    SituacaoDaTrilha,
    SubmissaoDoDesbloqueio,
    TipoDeDesafioDeDesbloqueio,
)
from nucleo.trilhas.regra import (
    acrescentar_pergunta_do_desbloqueio,
    corrigir_pergunta_do_desbloqueio,
    declarar_desafio_de_desbloqueio,
    inscrever_na_trilha,
    julgar_desafio_pratico,
    listar_desbloqueios_praticos_pendentes,
    perguntas_do_desbloqueio,
    remover_pergunta_do_desbloqueio,
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


# --- Fatia 19: a imagem opcional da pergunta do quiz -----------------------


def _cabecalhos(chave, criar_sessao_de_teste, persona):
    token, _ = criar_sessao_de_teste(persona)
    return {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}


def _primeira_pergunta(sessao, missao):
    return perguntas_do_desbloqueio(sessao, missao_id=missao.id)[0]


def _enviar_imagem(cliente, cabecalhos, pergunta_id, conteudo=b"PNG-de-teste", tipo="image/png"):
    """Abre a sessão, envia os bytes direto ao armazenamento e confirma —
    o mesmo trajeto que a App 09 percorre (`RF-09-119`)."""
    resposta_sessao = cliente.post(
        f"/v1/perguntas-do-desbloqueio/{pergunta_id}/imagem",
        json={"tipo_mime": tipo, "tamanho_declarado": len(conteudo)},
        headers=cabecalhos,
    )
    assert resposta_sessao.status_code == 201
    endereco = resposta_sessao.json()["endereco_da_sessao"]
    cliente.put(
        endereco,
        content=conteudo,
        headers={**cabecalhos, "Content-Range": f"bytes 0-{len(conteudo) - 1}/{len(conteudo)}"},
    )
    return cliente.patch(f"/v1/perguntas-do-desbloqueio/{pergunta_id}/imagem", headers=cabecalhos)


def test_mestre_autor_anexa_e_confirma_a_imagem_da_pergunta(
    cliente,
    sessao,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    _declarar_quiz(sessao, mestre, missao)
    sessao.commit()
    pergunta = _primeira_pergunta(sessao, missao)
    chave, _ = criar_chave()
    cabecalhos = _cabecalhos(chave, criar_sessao_de_teste, mestre)

    resposta = _enviar_imagem(cliente, cabecalhos, pergunta.id)

    assert resposta.status_code == 200
    sessao.expire_all()
    pergunta = _primeira_pergunta(sessao, missao)
    assert pergunta.imagem_referencia == f"perguntas-do-desbloqueio/{pergunta.id}/imagem"
    assert pergunta.imagem_tipo == "image/png"
    assert pergunta.imagem_tamanho == len(b"PNG-de-teste")


def test_pergunta_sem_imagem_segue_valida(sessao, criar_persona, criar_trilha, criar_missao):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    _declarar_quiz(sessao, mestre, missao, quantidade=3)
    sessao.commit()

    perguntas = perguntas_do_desbloqueio(sessao, missao_id=missao.id)
    assert len(perguntas) == 3
    assert all(pergunta.imagem_referencia is None for pergunta in perguntas)


def test_formato_fora_da_lista_e_recusado_antes_do_envio(
    cliente,
    sessao,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    _declarar_quiz(sessao, mestre, missao)
    sessao.commit()
    pergunta = _primeira_pergunta(sessao, missao)
    chave, _ = criar_chave()
    cabecalhos = _cabecalhos(chave, criar_sessao_de_teste, mestre)

    resposta = cliente.post(
        f"/v1/perguntas-do-desbloqueio/{pergunta.id}/imagem",
        json={"tipo_mime": "image/gif", "tamanho_declarado": 10},
        headers=cabecalhos,
    )

    assert resposta.status_code == 422
    assert "JPG, PNG e WebP" in resposta.json()["mensagem"]
    sessao.expire_all()
    assert _primeira_pergunta(sessao, missao).imagem_referencia is None


def test_imagem_acima_de_um_mega_e_recusada_na_abertura(
    cliente,
    sessao,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    _declarar_quiz(sessao, mestre, missao)
    sessao.commit()
    pergunta = _primeira_pergunta(sessao, missao)
    chave, _ = criar_chave()
    cabecalhos = _cabecalhos(chave, criar_sessao_de_teste, mestre)

    resposta = cliente.post(
        f"/v1/perguntas-do-desbloqueio/{pergunta.id}/imagem",
        json={"tipo_mime": "image/png", "tamanho_declarado": 3 * 1024 * 1024},
        headers=cabecalhos,
    )

    assert resposta.status_code == 413
    mensagem = resposta.json()["mensagem"]
    assert "3 MB" in mensagem and "1 MB" in mensagem


def test_envio_que_diverge_do_declarado_e_recusado_na_confirmacao(
    cliente,
    sessao,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    _declarar_quiz(sessao, mestre, missao)
    sessao.commit()
    pergunta = _primeira_pergunta(sessao, missao)
    chave, _ = criar_chave()
    cabecalhos = _cabecalhos(chave, criar_sessao_de_teste, mestre)

    # Declara 10 bytes; o que chega ao fim passa do teto de 1 MB.
    resposta_sessao = cliente.post(
        f"/v1/perguntas-do-desbloqueio/{pergunta.id}/imagem",
        json={"tipo_mime": "image/png", "tamanho_declarado": 10},
        headers=cabecalhos,
    )
    endereco = resposta_sessao.json()["endereco_da_sessao"]
    real = 2 * 1024 * 1024
    cliente.put(
        endereco,
        content=b"x" * real,
        headers={**cabecalhos, "Content-Range": f"bytes 0-{real - 1}/{real}"},
    )

    resposta = cliente.patch(
        f"/v1/perguntas-do-desbloqueio/{pergunta.id}/imagem", headers=cabecalhos
    )

    assert resposta.status_code == 413
    sessao.expire_all()
    assert _primeira_pergunta(sessao, missao).imagem_referencia is None


def test_mestre_que_nao_e_autor_nao_anexa_imagem(
    cliente,
    sessao,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
):
    mestre = criar_persona(Papel.mestre)
    outro_mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    _declarar_quiz(sessao, mestre, missao)
    sessao.commit()
    pergunta = _primeira_pergunta(sessao, missao)
    chave, _ = criar_chave()
    cabecalhos = _cabecalhos(chave, criar_sessao_de_teste, outro_mestre)

    resposta = cliente.post(
        f"/v1/perguntas-do-desbloqueio/{pergunta.id}/imagem",
        json={"tipo_mime": "image/png", "tamanho_declarado": 10},
        headers=cabecalhos,
    )

    assert resposta.status_code == 403
    sessao.expire_all()
    assert _primeira_pergunta(sessao, missao).imagem_referencia is None


def test_pergunta_sem_envio_confirmado_nao_serve_imagem(
    cliente,
    sessao,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    _declarar_quiz(sessao, mestre, missao)
    sessao.commit()
    pergunta = _primeira_pergunta(sessao, missao)
    chave, _ = criar_chave()
    cabecalhos = _cabecalhos(chave, criar_sessao_de_teste, mestre)

    # A sessão é aberta, mas o envio não é confirmado.
    cliente.post(
        f"/v1/perguntas-do-desbloqueio/{pergunta.id}/imagem",
        json={"tipo_mime": "image/png", "tamanho_declarado": 10},
        headers=cabecalhos,
    )

    sessao.expire_all()
    assert _primeira_pergunta(sessao, missao).imagem_referencia is None
    resposta = cliente.get(f"/v1/perguntas-do-desbloqueio/{pergunta.id}/imagem", headers=cabecalhos)
    assert resposta.status_code == 404


# --- Fatia 19: a imagem servida a quem pode ver a pergunta -----------------


def _missao_publicada_com_imagem(
    cliente, sessao, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    missao = criar_missao(trilha, mestre)
    _declarar_quiz(sessao, mestre, missao)
    sessao.commit()
    pergunta = _primeira_pergunta(sessao, missao)
    chave, _ = criar_chave()
    cabecalhos_do_mestre = _cabecalhos(chave, criar_sessao_de_teste, mestre)
    assert _enviar_imagem(cliente, cabecalhos_do_mestre, pergunta.id).status_code == 200
    sessao.expire_all()
    return mestre, trilha, missao, pergunta, chave, cabecalhos_do_mestre


def test_guerreiro_inscrito_ve_a_imagem_da_pergunta(
    cliente,
    sessao,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
):
    _, trilha, _, pergunta, chave, _ = _missao_publicada_com_imagem(
        cliente,
        sessao,
        criar_chave,
        criar_persona,
        criar_sessao_de_teste,
        criar_trilha,
        criar_missao,
    )
    guerreiro = criar_persona(Papel.guerreiro)
    inscrever_na_trilha(sessao, guerreiro=guerreiro, trilha=trilha)
    sessao.commit()
    cabecalhos = _cabecalhos(chave, criar_sessao_de_teste, guerreiro)

    resposta = cliente.get(f"/v1/perguntas-do-desbloqueio/{pergunta.id}/imagem", headers=cabecalhos)

    assert resposta.status_code == 200
    assert resposta.content == b"PNG-de-teste"
    assert resposta.headers["content-type"] == "image/png"


def test_mestre_autor_ve_a_imagem_que_anexou(
    cliente,
    sessao,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
):
    _, _, _, pergunta, _, cabecalhos = _missao_publicada_com_imagem(
        cliente,
        sessao,
        criar_chave,
        criar_persona,
        criar_sessao_de_teste,
        criar_trilha,
        criar_missao,
    )

    resposta = cliente.get(f"/v1/perguntas-do-desbloqueio/{pergunta.id}/imagem", headers=cabecalhos)

    assert resposta.status_code == 200
    assert resposta.content == b"PNG-de-teste"


def test_quem_nao_e_inscrito_nem_autor_nao_ve_a_imagem(
    cliente,
    sessao,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
):
    _, _, _, pergunta, chave, _ = _missao_publicada_com_imagem(
        cliente,
        sessao,
        criar_chave,
        criar_persona,
        criar_sessao_de_teste,
        criar_trilha,
        criar_missao,
    )
    nao_inscrito = criar_persona(Papel.guerreiro)
    outro_mestre = criar_persona(Papel.mestre)

    for persona in (nao_inscrito, outro_mestre):
        resposta = cliente.get(
            f"/v1/perguntas-do-desbloqueio/{pergunta.id}/imagem",
            headers=_cabecalhos(chave, criar_sessao_de_teste, persona),
        )
        assert resposta.status_code == 403
        assert resposta.content != b"PNG-de-teste"


def test_pergunta_sem_imagem_responde_404(
    cliente,
    sessao,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    _declarar_quiz(sessao, mestre, missao)
    sessao.commit()
    pergunta = _primeira_pergunta(sessao, missao)
    chave, _ = criar_chave()
    cabecalhos = _cabecalhos(chave, criar_sessao_de_teste, mestre)

    resposta = cliente.get(f"/v1/perguntas-do-desbloqueio/{pergunta.id}/imagem", headers=cabecalhos)

    assert resposta.status_code == 404


# --- Fatia 19: a redeclaração preserva a imagem e não apaga pergunta -------


def _redeclarar(sessao, mestre, missao, perguntas):
    return declarar_desafio_de_desbloqueio(
        sessao, operador=mestre, missao=missao, tipo="quiz", perguntas=perguntas
    )


def test_redeclarar_com_a_referencia_de_volta_conserva_a_imagem(
    cliente,
    sessao,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
):
    mestre, _, missao, pergunta, _, _ = _missao_publicada_com_imagem(
        cliente,
        sessao,
        criar_chave,
        criar_persona,
        criar_sessao_de_teste,
        criar_trilha,
        criar_missao,
    )
    referencia = _primeira_pergunta(sessao, missao).imagem_referencia

    _redeclarar(
        sessao,
        mestre,
        missao,
        [
            {
                "enunciado": "Pergunta 1, com a vírgula corrigida",
                "alternativas": ALTERNATIVAS,
                "alternativa_correta": 2,
                "imagem_referencia": referencia,
            }
        ],
    )
    sessao.commit()

    vigente = _primeira_pergunta(sessao, missao)
    assert vigente.id != pergunta.id
    assert vigente.enunciado == "Pergunta 1, com a vírgula corrigida"
    # A referência não se renomeia: a linha nova aponta o mesmo objeto, e
    # nenhum byte foi reenviado (design — decisão 2).
    assert vigente.imagem_referencia == referencia
    assert vigente.imagem_tipo == "image/png"
    assert vigente.imagem_tamanho == len(b"PNG-de-teste")


def test_redeclarar_sem_a_referencia_remove_a_imagem(
    cliente,
    sessao,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
):
    mestre, _, missao, _, _, _ = _missao_publicada_com_imagem(
        cliente,
        sessao,
        criar_chave,
        criar_persona,
        criar_sessao_de_teste,
        criar_trilha,
        criar_missao,
    )

    _declarar_quiz(sessao, mestre, missao)
    sessao.commit()

    assert _primeira_pergunta(sessao, missao).imagem_referencia is None


def test_referencia_de_outra_origem_e_recusada(
    cliente,
    sessao,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
):
    mestre, trilha, missao, _, _, _ = _missao_publicada_com_imagem(
        cliente,
        sessao,
        criar_chave,
        criar_persona,
        criar_sessao_de_teste,
        criar_trilha,
        criar_missao,
    )
    # A imagem de uma pergunta de **outra** missão não alcança esta.
    outra = criar_missao(trilha, mestre, titulo="Outra", posicao=2)
    _declarar_quiz(sessao, mestre, outra)
    sessao.commit()
    pergunta_da_outra = _primeira_pergunta(sessao, outra)
    referencia_de_fora = f"perguntas-do-desbloqueio/{pergunta_da_outra.id}/imagem"

    with pytest.raises(ErroDeValidacao):
        _redeclarar(
            sessao,
            mestre,
            missao,
            [
                {
                    "enunciado": "Pergunta 1",
                    "alternativas": ALTERNATIVAS,
                    "alternativa_correta": 2,
                    "imagem_referencia": referencia_de_fora,
                }
            ],
        )
    sessao.rollback()

    assert _primeira_pergunta(sessao, missao).imagem_referencia is not None


def test_redeclarar_depois_de_respondido_nao_falha_e_preserva_a_submissao(
    sessao, criar_persona, criar_trilha, criar_missao
):
    """`RN-05-47`: a submissão gravada aponta a pergunta respondida, e a
    substituição não a apaga nem estoura — o conserto da fatia 18."""
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    missao = criar_missao(trilha, mestre)
    _declarar_quiz(sessao, mestre, missao, alternativa_correta=2, quantidade=2)
    inscrever_na_trilha(sessao, guerreiro=guerreiro, trilha=trilha)
    sessao.commit()
    respondidas = [
        pergunta.id for pergunta in perguntas_do_desbloqueio(sessao, missao_id=missao.id)
    ]
    submeter_desafio_de_desbloqueio(
        sessao, guerreiro=guerreiro, missao=missao, respostas=_responder(sessao, missao, [2, 2])
    )
    sessao.commit()
    submissoes_antes = sessao.query(SubmissaoDoDesbloqueio).count()
    respostas_antes = sessao.query(RespostaDaSubmissao).count()

    _declarar_quiz(sessao, mestre, missao, alternativa_correta=1, quantidade=3)
    sessao.commit()

    vigentes = perguntas_do_desbloqueio(sessao, missao_id=missao.id)
    assert len(vigentes) == 3
    assert all(pergunta.id not in respondidas for pergunta in vigentes)
    # Nada foi apagado: a submissão e as respostas seguem apontando as
    # perguntas que o Guerreiro(a) respondeu.
    assert sessao.query(SubmissaoDoDesbloqueio).count() == submissoes_antes
    assert sessao.query(RespostaDaSubmissao).count() == respostas_antes
    for pergunta_id in respondidas:
        guardada = sessao.query(PerguntaDoDesbloqueio).filter_by(id=pergunta_id).one()
        assert guardada.substituida_em is not None


# `RF-09-120`, `RN-09-44`: a escrita de **uma** pergunta, ao lado da
# declaração do desafio inteiro, que não muda.


def _uma(enunciado="Quanto é 1 + 1?", correta=2, alternativas=None):
    return {
        "enunciado": enunciado,
        "alternativas": alternativas if alternativas is not None else ALTERNATIVAS,
        "alternativa_correta": correta,
    }


def test_acrescentar_pergunta_entra_ao_fim_sem_tocar_nas_demais(
    sessao, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    _declarar_quiz(sessao, mestre, missao, quantidade=3)
    sessao.commit()
    antes = [
        (p.id, p.enunciado, p.ordem) for p in perguntas_do_desbloqueio(sessao, missao_id=missao.id)
    ]

    nova = acrescentar_pergunta_do_desbloqueio(
        sessao, operador=mestre, missao=missao, pergunta=_uma()
    )
    sessao.commit()

    vigentes = perguntas_do_desbloqueio(sessao, missao_id=missao.id)
    assert len(vigentes) == 4
    assert nova.ordem == 4
    # As três anteriores seguem com o mesmo id, enunciado e ordem.
    assert [(p.id, p.enunciado, p.ordem) for p in vigentes[:3]] == antes


def test_a_primeira_pergunta_declara_a_missao_como_quiz(
    sessao, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    assert missao.tipo_do_desafio_de_desbloqueio is None

    acrescentar_pergunta_do_desbloqueio(sessao, operador=mestre, missao=missao, pergunta=_uma())
    sessao.commit()

    assert missao.tipo_do_desafio_de_desbloqueio == TipoDeDesafioDeDesbloqueio.quiz
    assert len(perguntas_do_desbloqueio(sessao, missao_id=missao.id)) == 1


def test_missao_de_desafio_pratico_nao_recebe_pergunta(
    sessao, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    _declarar_pratico(sessao, mestre, missao)
    sessao.commit()

    with pytest.raises(ErroDeValidacao):
        acrescentar_pergunta_do_desbloqueio(sessao, operador=mestre, missao=missao, pergunta=_uma())


def test_corrigir_uma_pergunta_nao_toca_nas_demais(
    sessao, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    _declarar_quiz(sessao, mestre, missao, quantidade=5)
    sessao.commit()
    vigentes = perguntas_do_desbloqueio(sessao, missao_id=missao.id)
    segunda = vigentes[1]
    outras = [(p.id, p.enunciado) for p in vigentes if p.id != segunda.id]

    corrigida = corrigir_pergunta_do_desbloqueio(
        sessao, operador=mestre, pergunta=segunda, conteudo=_uma(enunciado="Corrigida")
    )
    sessao.commit()

    depois = perguntas_do_desbloqueio(sessao, missao_id=missao.id)
    assert len(depois) == 5
    assert depois[1].enunciado == "Corrigida"
    assert depois[1].ordem == segunda.ordem
    # Ninguém respondeu: a linha é a mesma, e o id não muda.
    assert corrigida.id == segunda.id
    assert [(p.id, p.enunciado) for p in depois if p.id != segunda.id] == outras


def test_pergunta_incompleta_e_recusada(sessao, criar_persona, criar_trilha, criar_missao):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    with pytest.raises(ErroDeValidacao):
        acrescentar_pergunta_do_desbloqueio(
            sessao,
            operador=mestre,
            missao=missao,
            pergunta=_uma(alternativas=["Um", "Dois", "Três", ""]),
        )
    assert perguntas_do_desbloqueio(sessao, missao_id=missao.id) == []


def test_pergunta_sem_alternativa_correta_e_recusada(
    sessao, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    with pytest.raises(ErroDeValidacao):
        acrescentar_pergunta_do_desbloqueio(
            sessao, operador=mestre, missao=missao, pergunta=_uma(correta=None)
        )
    assert perguntas_do_desbloqueio(sessao, missao_id=missao.id) == []


def test_quem_nao_e_autor_nao_grava_pergunta(sessao, criar_persona, criar_trilha, criar_missao):
    mestre = criar_persona(Papel.mestre)
    outro = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    _declarar_quiz(sessao, mestre, missao, quantidade=2)
    sessao.commit()
    primeira = perguntas_do_desbloqueio(sessao, missao_id=missao.id)[0]

    with pytest.raises(PermissaoNegada):
        acrescentar_pergunta_do_desbloqueio(sessao, operador=outro, missao=missao, pergunta=_uma())
    with pytest.raises(PermissaoNegada):
        corrigir_pergunta_do_desbloqueio(sessao, operador=outro, pergunta=primeira, conteudo=_uma())
    with pytest.raises(PermissaoNegada):
        remover_pergunta_do_desbloqueio(sessao, operador=outro, pergunta=primeira)


def test_corrigir_pergunta_ja_respondida_nao_apaga_a_tentativa(
    sessao, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    missao = criar_missao(trilha, mestre)
    _declarar_quiz(sessao, mestre, missao, quantidade=2)
    sessao.commit()
    inscrever_na_trilha(sessao, guerreiro=guerreiro, trilha=trilha)
    submeter_desafio_de_desbloqueio(
        sessao, guerreiro=guerreiro, missao=missao, respostas=_responder(sessao, missao, [2, 2])
    )
    sessao.commit()
    respondida = perguntas_do_desbloqueio(sessao, missao_id=missao.id)[0]
    respostas_antes = sessao.query(RespostaDaSubmissao).count()

    corrigida = corrigir_pergunta_do_desbloqueio(
        sessao, operador=mestre, pergunta=respondida, conteudo=_uma(enunciado="Outro enunciado")
    )
    sessao.commit()

    # A corrigida nasce em linha nova, na mesma ordem; a anterior sai da
    # leitura e permanece guardada (`RN-05-47`).
    assert corrigida.id != respondida.id
    assert corrigida.ordem == respondida.ordem
    vigentes = perguntas_do_desbloqueio(sessao, missao_id=missao.id)
    assert [p.id for p in vigentes] == [corrigida.id, vigentes[1].id]
    guardada = sessao.query(PerguntaDoDesbloqueio).filter_by(id=respondida.id).one()
    assert guardada.substituida_em is not None
    assert sessao.query(RespostaDaSubmissao).count() == respostas_antes


def test_corrigir_o_texto_conserva_a_imagem_da_pergunta(
    sessao, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    _declarar_quiz(sessao, mestre, missao, quantidade=1)
    sessao.commit()
    pergunta = perguntas_do_desbloqueio(sessao, missao_id=missao.id)[0]
    pergunta.imagem_referencia = f"perguntas-do-desbloqueio/{pergunta.id}/imagem"
    pergunta.imagem_tipo = "image/png"
    pergunta.imagem_tamanho = 1234
    sessao.commit()
    referencia = pergunta.imagem_referencia

    corrigida = corrigir_pergunta_do_desbloqueio(
        sessao, operador=mestre, pergunta=pergunta, conteudo=_uma(enunciado="Só o texto mudou")
    )
    sessao.commit()

    assert corrigida.imagem_referencia == referencia
    assert corrigida.imagem_tipo == "image/png"
    assert corrigida.imagem_tamanho == 1234


def test_remover_uma_pergunta_tira_so_ela(sessao, criar_persona, criar_trilha, criar_missao):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    _declarar_quiz(sessao, mestre, missao, quantidade=4)
    sessao.commit()
    vigentes = perguntas_do_desbloqueio(sessao, missao_id=missao.id)
    terceira = vigentes[2]
    restantes = [p.id for p in vigentes if p.id != terceira.id]

    remover_pergunta_do_desbloqueio(sessao, operador=mestre, pergunta=terceira)
    sessao.commit()

    depois = perguntas_do_desbloqueio(sessao, missao_id=missao.id)
    assert [p.id for p in depois] == restantes
    # Não foi apagada, e as restantes não foram renumeradas.
    guardada = sessao.query(PerguntaDoDesbloqueio).filter_by(id=terceira.id).one()
    assert guardada.substituida_em is not None
    assert [p.ordem for p in depois] == [1, 2, 4]


def test_remover_a_unica_pergunta_e_recusado(sessao, criar_persona, criar_trilha, criar_missao):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    _declarar_quiz(sessao, mestre, missao, quantidade=1)
    sessao.commit()
    unica = perguntas_do_desbloqueio(sessao, missao_id=missao.id)[0]

    with pytest.raises(ErroDeValidacao):
        remover_pergunta_do_desbloqueio(sessao, operador=mestre, pergunta=unica)

    assert [p.id for p in perguntas_do_desbloqueio(sessao, missao_id=missao.id)] == [unica.id]


def test_a_sondagem_grava_pergunta_a_pergunta_como_qualquer_quiz(
    sessao, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    sondagem = criar_missao(trilha, mestre, e_sondagem=True)

    primeira = acrescentar_pergunta_do_desbloqueio(
        sessao, operador=mestre, missao=sondagem, pergunta=_uma(enunciado="De onde você parte?")
    )
    segunda = acrescentar_pergunta_do_desbloqueio(
        sessao, operador=mestre, missao=sondagem, pergunta=_uma(enunciado="E aqui?")
    )
    corrigir_pergunta_do_desbloqueio(
        sessao, operador=mestre, pergunta=primeira, conteudo=_uma(enunciado="Corrigida")
    )
    remover_pergunta_do_desbloqueio(sessao, operador=mestre, pergunta=segunda)
    sessao.commit()

    vigentes = perguntas_do_desbloqueio(sessao, missao_id=sondagem.id)
    assert [p.enunciado for p in vigentes] == ["Corrigida"]
    assert sondagem.tipo_do_desafio_de_desbloqueio == TipoDeDesafioDeDesbloqueio.quiz


def test_declarar_o_desafio_inteiro_sobre_quiz_gravado_pergunta_a_pergunta(
    sessao, criar_persona, criar_trilha, criar_missao
):
    """Os dois caminhos convivem: a declaração substitui o conjunto, como já
    fazia, e a escrita por pergunta atua sobre o que ela deixou
    (`RF-09-118`, `RF-09-120`)."""
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    acrescentar_pergunta_do_desbloqueio(
        sessao, operador=mestre, missao=missao, pergunta=_uma(enunciado="Gravada isolada")
    )
    sessao.commit()

    _declarar_quiz(sessao, mestre, missao, quantidade=2)
    sessao.commit()
    assert [p.enunciado for p in perguntas_do_desbloqueio(sessao, missao_id=missao.id)] == [
        "Pergunta 1",
        "Pergunta 2",
    ]

    acrescentar_pergunta_do_desbloqueio(
        sessao, operador=mestre, missao=missao, pergunta=_uma(enunciado="Depois da declaração")
    )
    sessao.commit()

    vigentes = perguntas_do_desbloqueio(sessao, missao_id=missao.id)
    assert [p.enunciado for p in vigentes] == [
        "Pergunta 1",
        "Pergunta 2",
        "Depois da declaração",
    ]
    assert [p.ordem for p in vigentes] == [1, 2, 3]


def test_as_rotas_da_pergunta_gravam_uma_a_uma_e_a_nova_aceita_imagem(
    cliente,
    sessao,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
):
    """`RF-09-120`, `RF-09-119`: o trajeto que a App 09 percorre — acrescenta
    a pergunta, anexa a imagem dela sem declarar o desafio inteiro antes,
    corrige o texto e remove — pelas três rotas novas."""
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    chave, _ = criar_chave()
    cabecalhos = _cabecalhos(chave, criar_sessao_de_teste, mestre)

    criada = cliente.post(
        f"/v1/missoes/{missao.id}/perguntas-do-desbloqueio",
        json=_uma(enunciado="O que o gráfico mostra?"),
        headers=cabecalhos,
    )
    assert criada.status_code == 201
    pergunta_id = criada.json()["id"]
    assert criada.json()["alternativa_correta"] == 2
    assert criada.json()["ordem"] == 1

    # A pergunta nasceu isolada e já é endereço de imagem.
    assert _enviar_imagem(cliente, cabecalhos, pergunta_id).status_code == 200

    corrigida = cliente.put(
        f"/v1/perguntas-do-desbloqueio/{pergunta_id}",
        json=_uma(enunciado="E agora?", correta=3),
        headers=cabecalhos,
    )
    assert corrigida.status_code == 200
    # Ninguém respondeu: o id não muda, e a imagem segue na pergunta.
    assert corrigida.json()["id"] == pergunta_id
    assert corrigida.json()["enunciado"] == "E agora?"
    assert corrigida.json()["imagem_referencia"] is not None

    # Remover a única é recusado; com duas, remove só ela.
    assert (
        cliente.delete(
            f"/v1/perguntas-do-desbloqueio/{pergunta_id}", headers=cabecalhos
        ).status_code
        == 422
    )
    segunda = cliente.post(
        f"/v1/missoes/{missao.id}/perguntas-do-desbloqueio",
        json=_uma(enunciado="A segunda"),
        headers=cabecalhos,
    ).json()
    assert (
        cliente.delete(
            f"/v1/perguntas-do-desbloqueio/{segunda['id']}", headers=cabecalhos
        ).status_code
        == 204
    )

    sessao.expire_all()
    assert [p.id for p in perguntas_do_desbloqueio(sessao, missao_id=missao.id)] == [
        uuid.UUID(pergunta_id)
    ]


def test_a_declaracao_recusa_o_identificador_da_pergunta_no_corpo(
    cliente,
    sessao,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
):
    """O id é endereço da pergunta, não campo declarável: devolvê-lo no corpo
    da declaração é recusado, e era o que derrubava toda regravação de quiz
    já declarado (`RF-09-118`)."""
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    _declarar_quiz(sessao, mestre, missao)
    sessao.commit()
    pergunta = _primeira_pergunta(sessao, missao)
    chave, _ = criar_chave()
    cabecalhos = _cabecalhos(chave, criar_sessao_de_teste, mestre)

    resposta = cliente.post(
        f"/v1/missoes/{missao.id}/desbloqueio",
        json={"tipo": "quiz", "perguntas": [{**_uma(), "id": str(pergunta.id)}]},
        headers=cabecalhos,
    )

    assert resposta.status_code == 422
