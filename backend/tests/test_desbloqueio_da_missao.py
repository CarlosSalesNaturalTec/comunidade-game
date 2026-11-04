import uuid

import pytest

from nucleo.criacoes_originais.modelo import TipoDeProducaoDaCriacaoOriginal
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
    derivar_percurso,
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
        forma_de_comprovacao="video",
        criterio_de_aceite="Em foto ou vídeo não deve aparecer o rosto da criança, só a produção.",
        titulo_curto="Robô de sucata",
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
    assert desbloqueio.cumpriu is True


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
    julgado = julgar_desafio_pratico(sessao, operador=mestre, desbloqueio=desbloqueio, cumpriu=True)
    sessao.commit()

    assert julgado.cumpriu is True
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
    assert pendentes[0].cumpriu is None


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
        julgar_desafio_pratico(sessao, operador=outro_mestre, desbloqueio=desbloqueio, cumpriu=True)


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
        sessao,
        operador=mestre,
        desbloqueio=desbloqueio,
        cumpriu=False,
        motivo="Faltou mostrar a peça montada.",
    )
    sessao.commit()
    # `RN-09-54`: a linha **permanece**, com o veredito e o motivo — apagá-la
    # destruiria o motivo no mesmo ato em que nasce.
    assert resultado is not None
    assert resultado.cumpriu is False
    assert resultado.motivo_do_julgamento == "Faltou mostrar a peça montada."
    assert (
        sessao.query(DesbloqueioDaMissao)
        .filter_by(guerreiro_id=guerreiro.id, missao_id=missao.id)
        .count()
        == 1
    )

    nova_declaracao = submeter_desafio_de_desbloqueio(sessao, guerreiro=guerreiro, missao=missao)
    sessao.commit()
    assert nova_declaracao.aprovado is None


def test_julgar_declaracao_inexistente_e_recusado(sessao, criar_persona):
    mestre = criar_persona(Papel.mestre)
    with pytest.raises(NaoEncontrado):
        julgar_desafio_pratico(sessao, operador=mestre, desbloqueio=None, cumpriu=True)


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


# ---------------------------------------------------------------------------
# A declaração do prático: forma de comprovação, critério de aceite e título
# curto (`RF-09-129` a `RF-09-131`, `RN-09-50`, `RN-09-51`).
# ---------------------------------------------------------------------------

CRITERIO = "Em foto ou vídeo não deve aparecer o rosto da criança, só a produção."


def _declarar_pratico_cru(sessao, mestre, missao, **campos):
    """A declaração do prático com os três campos sob controle do teste — o
    `_declarar_pratico` acima já os passa completos."""
    argumentos = {
        "tipo": "pratico",
        "enunciado": "Monte o robô e mostre ao Mestre.",
        "forma_de_comprovacao": "video",
        "criterio_de_aceite": CRITERIO,
        "titulo_curto": "Robô de sucata",
    }
    argumentos.update(campos)
    return declarar_desafio_de_desbloqueio(sessao, operador=mestre, missao=missao, **argumentos)


def test_o_pratico_declarado_guarda_forma_criterio_e_titulo(
    sessao, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    declarada = _declarar_pratico_cru(sessao, mestre, missao)
    sessao.commit()

    assert declarada.desafio_pratico_forma_de_comprovacao == (TipoDeProducaoDaCriacaoOriginal.video)
    assert declarada.desafio_pratico_criterio_de_aceite == CRITERIO
    assert declarada.desafio_pratico_titulo_curto == "Robô de sucata"
    # O título é campo próprio, nunca derivado do enunciado (`RN-09-51`).
    assert declarada.desafio_de_desbloqueio_enunciado == "Monte o robô e mostre ao Mestre."


@pytest.mark.parametrize(
    ("campos", "campo_recusado"),
    [
        ({"forma_de_comprovacao": None}, "forma_de_comprovacao"),
        ({"forma_de_comprovacao": "escultura"}, "forma_de_comprovacao"),
        ({"criterio_de_aceite": None}, "criterio_de_aceite"),
        ({"criterio_de_aceite": "   "}, "criterio_de_aceite"),
        ({"titulo_curto": None}, "titulo_curto"),
        ({"titulo_curto": "   "}, "titulo_curto"),
        ({"titulo_curto": "T" * 80}, "titulo_curto"),
    ],
)
def test_o_pratico_incompleto_ou_fora_do_conjunto_e_recusado_por_campo(
    sessao, criar_persona, criar_trilha, criar_missao, campos, campo_recusado
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    with pytest.raises(ErroDeValidacao) as erro:
        _declarar_pratico_cru(sessao, mestre, missao, **campos)

    assert erro.value.campo == campo_recusado
    sessao.rollback()
    assert missao.tipo_do_desafio_de_desbloqueio is None


def test_a_recusa_do_titulo_longo_diz_o_teto(sessao, criar_persona, criar_trilha, criar_missao):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    with pytest.raises(ErroDeValidacao) as erro:
        _declarar_pratico_cru(sessao, mestre, missao, titulo_curto="T" * 80)

    assert "60" in erro.value.mensagem and "80" in erro.value.mensagem


@pytest.mark.parametrize("campo", ["forma_de_comprovacao", "criterio_de_aceite", "titulo_curto"])
def test_o_quiz_nao_declara_nenhum_dos_tres_campos_do_pratico(
    sessao, criar_persona, criar_trilha, criar_missao, campo
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    with pytest.raises(ErroDeValidacao) as erro:
        declarar_desafio_de_desbloqueio(
            sessao,
            operador=mestre,
            missao=missao,
            tipo="quiz",
            perguntas=[
                {
                    "enunciado": "Pergunta",
                    "alternativas": ALTERNATIVAS,
                    "alternativa_correta": 1,
                }
            ],
            **{campo: "video" if campo == "forma_de_comprovacao" else "Texto qualquer"},
        )

    assert erro.value.campo == campo
    sessao.rollback()
    assert missao.tipo_do_desafio_de_desbloqueio is None


def test_o_quiz_declarado_deixa_os_tres_campos_nulos(
    sessao, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    _declarar_pratico_cru(sessao, mestre, missao)
    sessao.commit()
    declarada = _declarar_quiz(sessao, mestre, missao)
    sessao.commit()

    assert declarada.desafio_pratico_forma_de_comprovacao is None
    assert declarada.desafio_pratico_criterio_de_aceite is None
    assert declarada.desafio_pratico_titulo_curto is None


def test_o_pratico_declarado_antes_da_exigencia_segue_valendo(
    sessao, criar_persona, criar_trilha, criar_missao
):
    """O prático gravado sem os três campos — como todo prático anterior a
    2026-11-04 — continua sendo o desafio da missão, e a leitura o serve com os
    três nulos (`RN-09-50`)."""
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    missao.tipo_do_desafio_de_desbloqueio = TipoDeDesafioDeDesbloqueio.pratico
    missao.desafio_de_desbloqueio_enunciado = "Monte o robô."
    sessao.commit()

    assert missao.desafio_pratico_forma_de_comprovacao is None
    assert missao.desafio_pratico_criterio_de_aceite is None
    assert missao.desafio_pratico_titulo_curto is None

    # Redeclarar exige os três, como qualquer declaração nova.
    with pytest.raises(ErroDeValidacao):
        _declarar_pratico_cru(sessao, mestre, missao, criterio_de_aceite=None)
    sessao.rollback()
    assert missao.tipo_do_desafio_de_desbloqueio == TipoDeDesafioDeDesbloqueio.pratico

    _declarar_pratico_cru(sessao, mestre, missao)
    sessao.commit()
    assert missao.desafio_pratico_titulo_curto == "Robô de sucata"


# --- A comprovação do desafio prático (fatia 13 do PRD-05) -------------------


def _declarar_pratico_com_forma(sessao, mestre, missao, forma):
    return declarar_desafio_de_desbloqueio(
        sessao,
        operador=mestre,
        missao=missao,
        tipo="pratico",
        enunciado="Monte o robô e mostre ao Mestre.",
        forma_de_comprovacao=forma,
        criterio_de_aceite="Em foto ou vídeo não deve aparecer o rosto da criança.",
        titulo_curto="Robô de sucata",
    )


def _pratico_inscrito(sessao, criar_persona, criar_trilha, criar_missao, forma):
    """O caminho comum: Mestre autor, trilha publicada, missão com prático na
    forma pedida e um Guerreiro(a) inscrito pronto a declarar."""
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    missao = criar_missao(trilha, mestre)
    missao = _declarar_pratico_com_forma(sessao, mestre, missao, forma)
    inscrever_na_trilha(sessao, guerreiro=guerreiro, trilha=trilha)
    sessao.commit()
    return mestre, guerreiro, trilha, missao


def test_comprovacao_em_texto_e_gravada_com_a_declaracao(
    sessao, criar_persona, criar_trilha, criar_missao
):
    """`RF-05-91`: a forma aceita é texto, e o corpo escrito vai na própria
    declaração, gravado como o Guerreiro(a) o escreveu."""
    _, guerreiro, _, missao = _pratico_inscrito(
        sessao, criar_persona, criar_trilha, criar_missao, "texto"
    )

    resultado = submeter_desafio_de_desbloqueio(
        sessao, guerreiro=guerreiro, missao=missao, comprovacao="Montei com tampinhas e arame."
    )
    sessao.commit()

    assert resultado.aprovado is None
    assert resultado.desbloqueio.comprovacao == "Montei com tampinhas e arame."
    assert resultado.desbloqueio.entrega_presencial is False


def test_comprovacao_em_link_externo_e_gravada_como_endereco(
    sessao, criar_persona, criar_trilha, criar_missao
):
    """`RF-05-91`: no link externo o que se grava é o endereço."""
    _, guerreiro, _, missao = _pratico_inscrito(
        sessao, criar_persona, criar_trilha, criar_missao, "link_externo"
    )

    resultado = submeter_desafio_de_desbloqueio(
        sessao, guerreiro=guerreiro, missao=missao, comprovacao="https://exemplo.org/meu-robo"
    )
    sessao.commit()

    assert resultado.desbloqueio.comprovacao == "https://exemplo.org/meu-robo"


def test_comprovacao_em_midia_nasce_sem_arquivo(sessao, criar_persona, criar_trilha, criar_missao):
    """`RF-05-91`: nas quatro formas de mídia a declaração nasce sem arquivo e
    o recebe pela sessão de envio, como a criação original."""
    _, guerreiro, _, missao = _pratico_inscrito(
        sessao, criar_persona, criar_trilha, criar_missao, "video"
    )

    resultado = submeter_desafio_de_desbloqueio(sessao, guerreiro=guerreiro, missao=missao)
    sessao.commit()

    assert resultado.aprovado is None
    assert resultado.desbloqueio.comprovacao is None
    assert resultado.desbloqueio.comprovacao_referencia is None
    assert resultado.desbloqueio.entrega_presencial is False


def test_declaracao_em_midia_com_corpo_escrito_e_recusada(
    sessao, criar_persona, criar_trilha, criar_missao
):
    """`RF-05-91`: a comprovação em vídeo vai pelo envio do arquivo, não
    escrita na declaração."""
    _, guerreiro, _, missao = _pratico_inscrito(
        sessao, criar_persona, criar_trilha, criar_missao, "video"
    )

    with pytest.raises(ErroDeValidacao):
        submeter_desafio_de_desbloqueio(
            sessao, guerreiro=guerreiro, missao=missao, comprovacao="Mandei por fora."
        )


def test_declaracao_sem_o_corpo_e_sem_alternativa_e_recusada(
    sessao, criar_persona, criar_trilha, criar_missao
):
    """`RN-05-51`: na forma texto, sem o corpo e sem a entrega no encontro não
    há o que o Mestre julgue."""
    _, guerreiro, _, missao = _pratico_inscrito(
        sessao, criar_persona, criar_trilha, criar_missao, "texto"
    )

    with pytest.raises(ErroDeValidacao):
        submeter_desafio_de_desbloqueio(sessao, guerreiro=guerreiro, missao=missao)


def test_entrega_presencial_grava_a_declaracao_sem_midia(
    sessao, criar_persona, criar_trilha, criar_missao
):
    """`RN-05-51`: quem recusa a câmera, não tem aparelho que grave ou não
    consegue enviar entrega ao Mestre no encontro — e não perde a missão."""
    _, guerreiro, _, missao = _pratico_inscrito(
        sessao, criar_persona, criar_trilha, criar_missao, "video"
    )

    resultado = submeter_desafio_de_desbloqueio(
        sessao, guerreiro=guerreiro, missao=missao, entrega_presencial=True
    )
    sessao.commit()

    assert resultado.aprovado is None
    assert resultado.desbloqueio.entrega_presencial is True
    assert resultado.desbloqueio.comprovacao is None


def test_entregar_pelo_aparelho_e_no_encontro_ao_mesmo_tempo_e_recusado(
    sessao, criar_persona, criar_trilha, criar_missao
):
    """`RN-05-51`: exatamente um dos dois."""
    _, guerreiro, _, missao = _pratico_inscrito(
        sessao, criar_persona, criar_trilha, criar_missao, "texto"
    )

    with pytest.raises(ErroDeValidacao):
        submeter_desafio_de_desbloqueio(
            sessao,
            guerreiro=guerreiro,
            missao=missao,
            comprovacao="Montei com tampinhas.",
            entrega_presencial=True,
        )


def test_entrega_presencial_nao_conta_como_tentativa_falha(
    sessao, criar_persona, criar_trilha, criar_missao
):
    """`RN-05-51`, `RN-05-20`: a escolha nunca é reprovação — o percurso a
    exibe como aguardando o Mestre, que é o que `cumpriu is None` significa."""
    _, guerreiro, _, missao = _pratico_inscrito(
        sessao, criar_persona, criar_trilha, criar_missao, "imagem"
    )

    resultado = submeter_desafio_de_desbloqueio(
        sessao, guerreiro=guerreiro, missao=missao, entrega_presencial=True
    )
    sessao.commit()

    assert resultado.aprovado is not False
    submissoes = sessao.query(SubmissaoDoDesbloqueio).filter_by(guerreiro_id=guerreiro.id).all()
    assert len(submissoes) == 1
    assert submissoes[0].acertos == 0


def test_quiz_com_comprovacao_e_recusado(sessao, criar_persona, criar_trilha, criar_missao):
    """`RF-05-91`: no quiz o corte de acertos é o critério, e o núcleo o afere
    sozinho — não há comprovação a entregar."""
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    missao = criar_missao(trilha, mestre)
    missao = _declarar_quiz(sessao, mestre, missao)
    inscrever_na_trilha(sessao, guerreiro=guerreiro, trilha=trilha)
    sessao.commit()

    with pytest.raises(ErroDeValidacao):
        submeter_desafio_de_desbloqueio(
            sessao,
            guerreiro=guerreiro,
            missao=missao,
            respostas=_responder(sessao, missao, [2]),
            comprovacao="Não é daqui.",
        )


def test_entregar_de_novo_antes_do_julgamento_substitui_a_anterior(
    sessao, criar_persona, criar_trilha, criar_missao
):
    """`RN-05-52`: a entrega nova substitui a anterior em vez de criar segundo
    registro — e segue havendo uma única declaração daquele par."""
    _, guerreiro, _, missao = _pratico_inscrito(
        sessao, criar_persona, criar_trilha, criar_missao, "texto"
    )

    submeter_desafio_de_desbloqueio(
        sessao, guerreiro=guerreiro, missao=missao, comprovacao="Primeira."
    )
    sessao.commit()
    resultado = submeter_desafio_de_desbloqueio(
        sessao, guerreiro=guerreiro, missao=missao, comprovacao="Segunda, melhor."
    )
    sessao.commit()

    assert resultado.desbloqueio.comprovacao == "Segunda, melhor."
    linhas = (
        sessao.query(DesbloqueioDaMissao)
        .filter_by(guerreiro_id=guerreiro.id, missao_id=missao.id)
        .all()
    )
    assert len(linhas) == 1


def test_entregar_de_novo_apaga_a_midia_da_entrega_anterior(
    sessao, criar_persona, criar_trilha, criar_missao
):
    """`RN-05-52`: a substituição apaga a entrega inteira, para que não sobre
    arquivo de uma entrega que o Mestre não vai mais julgar."""
    _, guerreiro, _, missao = _pratico_inscrito(
        sessao, criar_persona, criar_trilha, criar_missao, "video"
    )

    resultado = submeter_desafio_de_desbloqueio(sessao, guerreiro=guerreiro, missao=missao)
    resultado.desbloqueio.comprovacao_referencia = "desbloqueios-praticos/x/comprovacao"
    resultado.desbloqueio.comprovacao_tamanho = 10
    resultado.desbloqueio.comprovacao_tipo_do_arquivo = "video/mp4"
    sessao.commit()

    de_novo = submeter_desafio_de_desbloqueio(sessao, guerreiro=guerreiro, missao=missao)
    sessao.commit()

    assert de_novo.desbloqueio.comprovacao_referencia is None
    assert de_novo.desbloqueio.comprovacao_tamanho is None
    assert de_novo.desbloqueio.comprovacao_tipo_do_arquivo is None


def test_julgado_que_nao_cumpriu_a_declaracao_e_o_motivo_permanecem(
    sessao, criar_persona, criar_trilha, criar_missao
):
    """`RN-09-54`, `RN-05-52`: a linha **não** é apagada — ela guarda o veredito
    e o motivo, e a comprovação segue lá, para o Guerreiro(a) rever o que
    entregou. Entregar de novo **reabre a mesma linha**, sem segundo registro
    do par."""
    mestre, guerreiro, _, missao = _pratico_inscrito(
        sessao, criar_persona, criar_trilha, criar_missao, "texto"
    )

    resultado = submeter_desafio_de_desbloqueio(
        sessao, guerreiro=guerreiro, missao=missao, comprovacao="Montei assim."
    )
    sessao.commit()
    id_da_linha = resultado.desbloqueio.id
    julgar_desafio_pratico(
        sessao,
        operador=mestre,
        desbloqueio=resultado.desbloqueio,
        cumpriu=False,
        motivo="Não deu para ver a peça inteira.",
    )
    sessao.commit()

    guardada = (
        sessao.query(DesbloqueioDaMissao)
        .filter_by(guerreiro_id=guerreiro.id, missao_id=missao.id)
        .one()
    )
    assert guardada.cumpriu is False
    assert guardada.motivo_do_julgamento == "Não deu para ver a peça inteira."
    assert guardada.comprovacao == "Montei assim."
    assert guardada.julgado_em is not None

    de_novo = submeter_desafio_de_desbloqueio(
        sessao, guerreiro=guerreiro, missao=missao, comprovacao="Montei de outro jeito."
    )
    sessao.commit()
    # A mesma linha, reaberta: o julgamento anterior não sobrevive à entrega
    # nova, porque ela é outra entrega.
    assert de_novo.desbloqueio.id == id_da_linha
    assert de_novo.desbloqueio.comprovacao == "Montei de outro jeito."
    assert de_novo.desbloqueio.cumpriu is None
    assert de_novo.desbloqueio.motivo_do_julgamento is None
    assert de_novo.desbloqueio.julgado_em is None
    assert (
        sessao.query(DesbloqueioDaMissao)
        .filter_by(guerreiro_id=guerreiro.id, missao_id=missao.id)
        .count()
        == 1
    )


def test_declaracao_repetida_depois_do_julgamento_nao_toca_no_que_esta_gravado(
    sessao, criar_persona, criar_trilha, criar_missao
):
    """`RN-05-52`: julgado que **cumpriu**, a declaração repetida devolve a
    situação do julgamento e a comprovação permanece como estava — só a recusada
    reabre."""
    mestre, guerreiro, _, missao = _pratico_inscrito(
        sessao, criar_persona, criar_trilha, criar_missao, "texto"
    )

    resultado = submeter_desafio_de_desbloqueio(
        sessao, guerreiro=guerreiro, missao=missao, comprovacao="Montei assim."
    )
    sessao.commit()
    julgar_desafio_pratico(
        sessao,
        operador=mestre,
        desbloqueio=resultado.desbloqueio,
        cumpriu=True,
        publicavel=True,
    )
    sessao.commit()

    de_novo = submeter_desafio_de_desbloqueio(
        sessao, guerreiro=guerreiro, missao=missao, comprovacao="Tentando mudar."
    )
    sessao.commit()

    assert de_novo.aprovado is True
    assert de_novo.desbloqueio.comprovacao == "Montei assim."


def test_pratico_declarado_antes_da_regra_segue_declaravel(
    sessao, criar_persona, criar_trilha, criar_missao
):
    """Design — decisão 7: prático sem forma aceita declarada segue valendo, e
    a declaração é aceita sem comprovação, porque não há forma a exigir."""
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    missao = criar_missao(trilha, mestre)
    missao = _declarar_pratico_com_forma(sessao, mestre, missao, "video")
    # O estado de quem declarou o prático antes de os três campos existirem.
    missao.desafio_pratico_forma_de_comprovacao = None
    missao.desafio_pratico_criterio_de_aceite = None
    missao.desafio_pratico_titulo_curto = None
    inscrever_na_trilha(sessao, guerreiro=guerreiro, trilha=trilha)
    sessao.commit()

    resultado = submeter_desafio_de_desbloqueio(sessao, guerreiro=guerreiro, missao=missao)
    sessao.commit()

    assert resultado.aprovado is None
    assert resultado.desbloqueio.comprovacao is None


# ---------------------------------------------------------------------------
# A entrega da comprovação pelas rotas (`RF-05-91`, `RF-05-93`, `RN-05-51`).
# ---------------------------------------------------------------------------


def _cenario_do_pratico_por_http(
    sessao, criar_persona, criar_trilha, criar_missao, criar_chave, criar_sessao_de_teste, forma
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    missao = criar_missao(trilha, mestre)
    missao = _declarar_pratico_com_forma(sessao, mestre, missao, forma)
    inscrever_na_trilha(sessao, guerreiro=guerreiro, trilha=trilha)
    sessao.commit()
    chave, _ = criar_chave()
    return (
        missao,
        mestre,
        guerreiro,
        _cabecalhos(chave, criar_sessao_de_teste, guerreiro),
        _cabecalhos(chave, criar_sessao_de_teste, mestre),
        chave,
    )


def _enviar_comprovacao(cliente, cabecalhos, missao_id, conteudo=b"MP4-de-teste", tipo="video/mp4"):
    """Abre a sessão, envia os bytes direto ao armazenamento e confirma — o
    mesmo trajeto que a App 05 percorre (`RF-05-91`)."""
    resposta_sessao = cliente.post(
        f"/v1/eu/missoes/{missao_id}/desbloqueio/comprovacao",
        json={"tipo_mime": tipo, "tamanho_declarado": len(conteudo)},
        headers=cabecalhos,
    )
    assert resposta_sessao.status_code == 201, resposta_sessao.text
    cliente.put(
        resposta_sessao.json()["endereco_da_sessao"],
        content=conteudo,
        headers={**cabecalhos, "Content-Range": f"bytes 0-{len(conteudo) - 1}/{len(conteudo)}"},
    )
    return cliente.patch(f"/v1/eu/missoes/{missao_id}/desbloqueio/comprovacao", headers=cabecalhos)


def test_submissao_do_pratico_leva_a_comprovacao_e_a_devolve(
    cliente, sessao, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha, criar_missao
):
    """`RF-05-91`, `RF-05-93`: o corpo novo da submissão carrega a comprovação,
    e a saída a devolve, para a tela reencontrá-la sem segunda chamada."""
    missao, _, _, cabecalhos, _, _ = _cenario_do_pratico_por_http(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_chave,
        criar_sessao_de_teste,
        "texto",
    )

    resposta = cliente.post(
        f"/v1/eu/missoes/{missao.id}/desbloqueio",
        json={"comprovacao": "Montei com tampinhas e arame."},
        headers=cabecalhos,
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["aguardando_mestre"] is True
    assert corpo["comprovacao_entregue"]["comprovacao"] == "Montei com tampinhas e arame."
    assert corpo["comprovacao_entregue"]["forma"] == "texto"
    assert corpo["comprovacao_entregue"]["tem_arquivo"] is False


def test_submissao_recusa_campo_fora_do_contrato(
    cliente, sessao, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha, criar_missao
):
    """A entrada é `extra="forbid"`: campo inventado é 422, como o id da
    pergunta no corpo da declaração já era (`RF-05-91`)."""
    missao, _, _, cabecalhos, _, _ = _cenario_do_pratico_por_http(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_chave,
        criar_sessao_de_teste,
        "texto",
    )

    resposta = cliente.post(
        f"/v1/eu/missoes/{missao.id}/desbloqueio",
        json={"comprovacao": "Montei.", "forma_de_comprovacao": "texto"},
        headers=cabecalhos,
    )

    assert resposta.status_code == 422


def test_entrega_presencial_pela_rota(
    cliente, sessao, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha, criar_missao
):
    """`RN-05-51`: a alternativa de quem não entrega pelo aparelho chega pela
    mesma rota, e a saída diz que foi ela."""
    missao, _, _, cabecalhos, _, _ = _cenario_do_pratico_por_http(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_chave,
        criar_sessao_de_teste,
        "video",
    )

    resposta = cliente.post(
        f"/v1/eu/missoes/{missao.id}/desbloqueio",
        json={"entrega_presencial": True},
        headers=cabecalhos,
    )

    assert resposta.status_code == 201
    assert resposta.json()["comprovacao_entregue"]["entrega_presencial"] is True


def test_ciclo_de_envio_da_comprovacao_e_leitura_pelo_proprio_guerreiro(
    cliente, sessao, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha, criar_missao
):
    """`RF-05-91`, `RF-05-93`: abrir, enviar, confirmar e ler de volta — o
    ciclo inteiro por HTTP, como a criança o percorre."""
    missao, _, guerreiro, cabecalhos, _, chave = _cenario_do_pratico_por_http(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_chave,
        criar_sessao_de_teste,
        "video",
    )
    assert (
        cliente.post(
            f"/v1/eu/missoes/{missao.id}/desbloqueio", json={}, headers=cabecalhos
        ).status_code
        == 201
    )

    confirmacao = _enviar_comprovacao(cliente, cabecalhos, missao.id)
    assert confirmacao.status_code == 200
    assert confirmacao.json()["tem_arquivo"] is True

    leitura = cliente.get(
        f"/v1/missoes/{missao.id}/desbloqueios/{guerreiro.id}/comprovacao", headers=cabecalhos
    )
    assert leitura.status_code == 200
    assert leitura.content == b"MP4-de-teste"
    assert leitura.headers["content-type"].startswith("video/mp4")


def test_mestre_autor_le_a_comprovacao_que_lhe_cabe_julgar(
    cliente, sessao, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha, criar_missao
):
    """`RF-05-93`: é ele quem julga, e sem os bytes julgaria às cegas."""
    missao, _, guerreiro, cabecalhos, cabecalhos_mestre, _ = _cenario_do_pratico_por_http(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_chave,
        criar_sessao_de_teste,
        "video",
    )
    cliente.post(f"/v1/eu/missoes/{missao.id}/desbloqueio", json={}, headers=cabecalhos)
    _enviar_comprovacao(cliente, cabecalhos, missao.id)

    leitura = cliente.get(
        f"/v1/missoes/{missao.id}/desbloqueios/{guerreiro.id}/comprovacao",
        headers=cabecalhos_mestre,
    )

    assert leitura.status_code == 200
    assert leitura.content == b"MP4-de-teste"


def test_quem_nao_entregou_nem_e_o_autor_e_recusado(
    cliente, sessao, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha, criar_missao
):
    """`RF-05-93`: 403 para o resto — a comprovação é mídia de criança."""
    missao, _, guerreiro, cabecalhos, _, chave = _cenario_do_pratico_por_http(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_chave,
        criar_sessao_de_teste,
        "video",
    )
    cliente.post(f"/v1/eu/missoes/{missao.id}/desbloqueio", json={}, headers=cabecalhos)
    _enviar_comprovacao(cliente, cabecalhos, missao.id)
    # A chave é uma por aplicação e ambiente: o estranho entra pela mesma, e o
    # que o separa é a persona da sessão, que é o ponto do teste.
    cabecalhos_estranho = _cabecalhos(chave, criar_sessao_de_teste, criar_persona(Papel.mestre))

    leitura = cliente.get(
        f"/v1/missoes/{missao.id}/desbloqueios/{guerreiro.id}/comprovacao",
        headers=cabecalhos_estranho,
    )

    assert leitura.status_code == 403


def test_comprovacao_sem_midia_responde_404(
    cliente, sessao, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha, criar_missao
):
    """`RF-05-93`: entrega presencial e envio não concluído não servem bytes."""
    missao, _, guerreiro, cabecalhos, _, chave = _cenario_do_pratico_por_http(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_chave,
        criar_sessao_de_teste,
        "video",
    )
    cliente.post(
        f"/v1/eu/missoes/{missao.id}/desbloqueio",
        json={"entrega_presencial": True},
        headers=cabecalhos,
    )

    leitura = cliente.get(
        f"/v1/missoes/{missao.id}/desbloqueios/{guerreiro.id}/comprovacao", headers=cabecalhos
    )

    assert leitura.status_code == 404


def test_envio_depois_do_julgamento_e_recusado(
    cliente, sessao, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha, criar_missao
):
    """`RN-05-52`: julgado, a entrega está encerrada."""
    missao, mestre, guerreiro, cabecalhos, _, _ = _cenario_do_pratico_por_http(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_chave,
        criar_sessao_de_teste,
        "video",
    )
    cliente.post(f"/v1/eu/missoes/{missao.id}/desbloqueio", json={}, headers=cabecalhos)
    sessao.expire_all()
    desbloqueio = (
        sessao.query(DesbloqueioDaMissao)
        .filter_by(guerreiro_id=guerreiro.id, missao_id=missao.id)
        .first()
    )
    julgar_desafio_pratico(sessao, operador=mestre, desbloqueio=desbloqueio, cumpriu=True)
    sessao.commit()

    resposta = cliente.post(
        f"/v1/eu/missoes/{missao.id}/desbloqueio/comprovacao",
        json={"tipo_mime": "video/mp4", "tamanho_declarado": 10},
        headers=cabecalhos,
    )

    assert resposta.status_code == 422


def test_bancada_do_mestre_traz_o_criterio_e_a_entrega(
    cliente, sessao, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha, criar_missao
):
    """`RF-05-93`: a pendência chega ao Mestre com o critério e a entrega, e é
    o que deixa a bancada pronta — sem servir bytes na listagem."""
    missao, _, _, cabecalhos, cabecalhos_mestre, _ = _cenario_do_pratico_por_http(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_chave,
        criar_sessao_de_teste,
        "video",
    )
    cliente.post(f"/v1/eu/missoes/{missao.id}/desbloqueio", json={}, headers=cabecalhos)
    _enviar_comprovacao(cliente, cabecalhos, missao.id)

    pendentes = cliente.get("/v1/missoes/desbloqueios-pendentes", headers=cabecalhos_mestre)

    assert pendentes.status_code == 200
    linha = pendentes.json()[0]
    assert linha["criterio_de_aceite"] == ("Em foto ou vídeo não deve aparecer o rosto da criança.")
    assert linha["comprovacao_entregue"]["forma"] == "video"
    assert linha["comprovacao_entregue"]["tem_arquivo"] is True


def test_envio_da_comprovacao_recusa_formato_fora_da_lista(
    cliente, sessao, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha, criar_missao
):
    """`RF-05-91`: a comprovação lê a mesma lista fechada de MIME da criação
    original, de `armazenamento.limites` — a recusa é 422 e nomeia a lista."""
    missao, _, _, cabecalhos, _, _ = _cenario_do_pratico_por_http(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_chave,
        criar_sessao_de_teste,
        "video",
    )
    cliente.post(f"/v1/eu/missoes/{missao.id}/desbloqueio", json={}, headers=cabecalhos)

    resposta = cliente.post(
        f"/v1/eu/missoes/{missao.id}/desbloqueio/comprovacao",
        json={"tipo_mime": "image/gif", "tamanho_declarado": 10},
        headers=cabecalhos,
    )

    assert resposta.status_code == 422
    assert "MP4, WebM, JPG, PNG, WebP, MP3 e PDF" in resposta.text


def test_envio_da_comprovacao_recusa_tamanho_acima_do_teto_dizendo_o_teto(
    cliente, sessao, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha, criar_missao
):
    """`RF-05-91`: o teto é o mesmo da criação original, por tipo — 200 MB no
    vídeo —, e a recusa é o 413 de `ArquivoAcimaDoTeto`, dizendo o limite."""
    missao, _, _, cabecalhos, _, _ = _cenario_do_pratico_por_http(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_chave,
        criar_sessao_de_teste,
        "video",
    )
    cliente.post(f"/v1/eu/missoes/{missao.id}/desbloqueio", json={}, headers=cabecalhos)

    resposta = cliente.post(
        f"/v1/eu/missoes/{missao.id}/desbloqueio/comprovacao",
        json={"tipo_mime": "video/mp4", "tamanho_declarado": 201 * 1024 * 1024},
        headers=cabecalhos,
    )

    assert resposta.status_code == 413
    assert "200 MB" in resposta.text


def test_envio_da_comprovacao_e_recusado_na_entrega_presencial(
    cliente, sessao, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha, criar_missao
):
    """`RN-05-51`: quem escolheu entregar ao Mestre no encontro não tem arquivo
    a enviar — exatamente um dos dois."""
    missao, _, _, cabecalhos, _, _ = _cenario_do_pratico_por_http(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_chave,
        criar_sessao_de_teste,
        "video",
    )
    cliente.post(
        f"/v1/eu/missoes/{missao.id}/desbloqueio",
        json={"entrega_presencial": True},
        headers=cabecalhos,
    )

    resposta = cliente.post(
        f"/v1/eu/missoes/{missao.id}/desbloqueio/comprovacao",
        json={"tipo_mime": "video/mp4", "tamanho_declarado": 10},
        headers=cabecalhos,
    )

    assert resposta.status_code == 422


def test_percurso_devolve_a_comprovacao_entregue_ao_proprio_guerreiro(
    cliente, sessao, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha, criar_missao
):
    """`RF-05-93`: ao voltar à missão, a leitura do percurso traz a entrega, de
    modo que a tela a reapresente em lugar de um formulário vazio."""
    missao, _, _, cabecalhos, _, _ = _cenario_do_pratico_por_http(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_chave,
        criar_sessao_de_teste,
        "texto",
    )
    cliente.post(
        f"/v1/eu/missoes/{missao.id}/desbloqueio",
        json={"comprovacao": "Montei com tampinhas."},
        headers=cabecalhos,
    )

    leitura = cliente.get(
        f"/v1/eu/trilhas/{missao.trilha_id}/missoes/{missao.posicao}", headers=cabecalhos
    )

    assert leitura.status_code == 200
    corpo = leitura.json()
    assert corpo["comprovacao_entregue"]["comprovacao"] == "Montei com tampinhas."
    assert corpo["desafio_de_desbloqueio"]["criterio_de_aceite"] == (
        "Em foto ou vídeo não deve aparecer o rosto da criança."
    )


# ---------------------------------------------------------------------------
# Os dois vereditos do julgamento, o motivo e o que para de apagar
# (`RF-09-133`, `RF-09-134`, `RN-09-52` a `RN-09-54`)
# ---------------------------------------------------------------------------


def _declarado_em_texto(sessao, criar_persona, criar_trilha, criar_missao, corpo="Montei assim."):
    """Prático em texto, declarado e aguardando julgamento — o caminho mais
    curto a uma declaração com comprovação gravada."""
    mestre, guerreiro, trilha, missao = _pratico_inscrito(
        sessao, criar_persona, criar_trilha, criar_missao, "texto"
    )
    resultado = submeter_desafio_de_desbloqueio(
        sessao, guerreiro=guerreiro, missao=missao, comprovacao=corpo
    )
    sessao.commit()
    return mestre, guerreiro, trilha, missao, resultado.desbloqueio


def test_os_dois_vereditos_sao_gravados_num_ato_so(
    sessao, criar_persona, criar_trilha, criar_missao
):
    """`RF-09-133`: cumpriu abre a missão seguinte, publicável leva a entrega à
    vitrine, e os dois vão no mesmo ato."""
    mestre, _, _, _, desbloqueio = _declarado_em_texto(
        sessao, criar_persona, criar_trilha, criar_missao
    )

    julgado = julgar_desafio_pratico(
        sessao, operador=mestre, desbloqueio=desbloqueio, cumpriu=True, publicavel=True
    )
    sessao.commit()

    assert julgado.cumpriu is True
    assert julgado.publicavel is True
    assert julgado.julgado_por_id == mestre.id
    assert julgado.julgado_em is not None


def test_cumpriu_sem_ser_publicavel_e_julgamento_valido(
    sessao, criar_persona, criar_trilha, criar_missao
):
    """`RF-09-133`: é para isso que os dois campos existem — com um só, o Mestre
    teria de reprovar quem cumpriu e enquadrou mal."""
    mestre, _, _, _, desbloqueio = _declarado_em_texto(
        sessao, criar_persona, criar_trilha, criar_missao
    )

    julgado = julgar_desafio_pratico(
        sessao,
        operador=mestre,
        desbloqueio=desbloqueio,
        cumpriu=True,
        publicavel=False,
        motivo="Ficou ótimo, mas aparece o rosto de um colega.",
    )
    sessao.commit()

    assert julgado.cumpriu is True
    assert julgado.publicavel is False
    assert julgado.motivo_do_julgamento == "Ficou ótimo, mas aparece o rosto de um colega."


def test_publicavel_sobre_o_que_nao_cumpriu_e_recusado(
    sessao, criar_persona, criar_trilha, criar_missao
):
    """`RN-09-52`: o que o Mestre recusou não vai a público, e nenhum dos dois
    vereditos é gravado."""
    mestre, _, _, _, desbloqueio = _declarado_em_texto(
        sessao, criar_persona, criar_trilha, criar_missao
    )

    with pytest.raises(ErroDeValidacao) as erro:
        julgar_desafio_pratico(
            sessao,
            operador=mestre,
            desbloqueio=desbloqueio,
            cumpriu=False,
            publicavel=True,
            motivo="Qualquer motivo.",
        )
    assert erro.value.campo == "publicavel"
    sessao.rollback()
    assert desbloqueio.cumpriu is None
    assert desbloqueio.publicavel is None


def test_publicavel_sobre_entrega_presencial_e_recusado(
    sessao, criar_persona, criar_trilha, criar_missao
):
    """`RN-09-52`: a entrega no encontro nasce sem mídia — não há o que
    publicar."""
    mestre, guerreiro, _, missao = _pratico_inscrito(
        sessao, criar_persona, criar_trilha, criar_missao, "video"
    )
    resultado = submeter_desafio_de_desbloqueio(
        sessao, guerreiro=guerreiro, missao=missao, entrega_presencial=True
    )
    sessao.commit()

    with pytest.raises(ErroDeValidacao) as erro:
        julgar_desafio_pratico(
            sessao,
            operador=mestre,
            desbloqueio=resultado.desbloqueio,
            cumpriu=True,
            publicavel=True,
        )
    assert erro.value.campo == "publicavel"


def test_entrega_presencial_cumprida_dispensa_o_motivo(
    sessao, criar_persona, criar_trilha, criar_missao
):
    """`RN-09-53`: não publicar só é negativa quando publicar era possível —
    aqui não havia o que publicar, e cobrar motivo seria cobrá-lo de um fato
    estrutural."""
    mestre, guerreiro, _, missao = _pratico_inscrito(
        sessao, criar_persona, criar_trilha, criar_missao, "video"
    )
    resultado = submeter_desafio_de_desbloqueio(
        sessao, guerreiro=guerreiro, missao=missao, entrega_presencial=True
    )
    sessao.commit()

    julgado = julgar_desafio_pratico(
        sessao, operador=mestre, desbloqueio=resultado.desbloqueio, cumpriu=True
    )
    sessao.commit()

    assert julgado.cumpriu is True
    assert julgado.publicavel is False
    assert julgado.motivo_do_julgamento is None


def test_recusar_sem_motivo_e_recusado(sessao, criar_persona, criar_trilha, criar_missao):
    """`RN-09-53`: julgamento que nega algo exige o motivo, pelo precedente da
    devolução da criação original."""
    mestre, _, _, _, desbloqueio = _declarado_em_texto(
        sessao, criar_persona, criar_trilha, criar_missao
    )

    with pytest.raises(ErroDeValidacao) as erro:
        julgar_desafio_pratico(sessao, operador=mestre, desbloqueio=desbloqueio, cumpriu=False)
    assert erro.value.campo == "motivo"
    sessao.rollback()
    assert desbloqueio.cumpriu is None


def test_negar_a_publicacao_sem_motivo_e_recusado(
    sessao, criar_persona, criar_trilha, criar_missao
):
    """`RN-09-53`: o segundo veredito negativo também é um "não" ao
    Guerreiro(a), e ele tem o direito de saber por quê."""
    mestre, _, _, _, desbloqueio = _declarado_em_texto(
        sessao, criar_persona, criar_trilha, criar_missao
    )

    with pytest.raises(ErroDeValidacao) as erro:
        julgar_desafio_pratico(
            sessao, operador=mestre, desbloqueio=desbloqueio, cumpriu=True, publicavel=False
        )
    assert erro.value.campo == "motivo"


def test_motivo_so_de_espaco_conta_como_ausente(sessao, criar_persona, criar_trilha, criar_missao):
    """O motivo existe para ser lido: espaço em branco não diz nada ao
    Guerreiro(a) (`RN-09-53`)."""
    mestre, _, _, _, desbloqueio = _declarado_em_texto(
        sessao, criar_persona, criar_trilha, criar_missao
    )

    with pytest.raises(ErroDeValidacao) as erro:
        julgar_desafio_pratico(
            sessao, operador=mestre, desbloqueio=desbloqueio, cumpriu=False, motivo="   "
        )
    assert erro.value.campo == "motivo"


def test_julgar_de_novo_o_ja_julgado_e_recusado(sessao, criar_persona, criar_trilha, criar_missao):
    """`RF-09-133`: o julgamento é único por par enquanto a entrega não for
    refeita — e é essa recusa que dá a idempotência do crédito."""
    mestre, _, _, _, desbloqueio = _declarado_em_texto(
        sessao, criar_persona, criar_trilha, criar_missao
    )
    julgar_desafio_pratico(
        sessao, operador=mestre, desbloqueio=desbloqueio, cumpriu=True, publicavel=True
    )
    sessao.commit()

    with pytest.raises(ErroDeValidacao) as erro:
        julgar_desafio_pratico(
            sessao, operador=mestre, desbloqueio=desbloqueio, cumpriu=True, publicavel=True
        )
    assert erro.value.campo == "cumpriu"


def test_a_linha_legada_nao_se_rejulga(sessao, criar_persona, criar_trilha, criar_missao):
    """`RN-09-55`: o prático julgado **antes** desta regra tem `cumpriu`
    verdadeiro com `julgado_em` nulo — não se rejulga, e por isso não recebe
    crédito retroativo."""
    mestre, _, _, _, desbloqueio = _declarado_em_texto(
        sessao, criar_persona, criar_trilha, criar_missao
    )
    # O estado de quem foi julgado antes de os vereditos existirem.
    desbloqueio.cumpriu = True
    desbloqueio.julgado_em = None
    sessao.commit()

    with pytest.raises(ErroDeValidacao):
        julgar_desafio_pratico(
            sessao, operador=mestre, desbloqueio=desbloqueio, cumpriu=True, publicavel=True
        )


def test_o_percurso_traz_o_veredito_e_o_motivo_ao_proprio_guerreiro(
    sessao, criar_persona, criar_trilha, criar_missao
):
    """`RF-05-94`: nada do julgamento fica gravado sem ser servido ao
    Guerreiro(a) — é dele que o motivo fala."""
    mestre, guerreiro, trilha, missao, desbloqueio = _declarado_em_texto(
        sessao, criar_persona, criar_trilha, criar_missao
    )
    julgar_desafio_pratico(
        sessao,
        operador=mestre,
        desbloqueio=desbloqueio,
        cumpriu=False,
        motivo="Faltou mostrar a peça montada.",
    )
    sessao.commit()

    guardada = (
        sessao.query(DesbloqueioDaMissao)
        .filter_by(guerreiro_id=guerreiro.id, missao_id=missao.id)
        .one()
    )
    assert guardada.cumpriu is False
    assert guardada.motivo_do_julgamento == "Faltou mostrar a peça montada."
    # Recusado, a missão volta a ser a próxima dele — nunca reprovada.
    percurso = derivar_percurso(sessao, guerreiro_id=guerreiro.id, trilha_id=trilha.id)
    desta = next(item for item in percurso if item.missao.id == missao.id)
    assert desta.desbloqueada is False
    assert desta.aguardando_mestre is False
    assert desta.e_proxima is True


def test_recusado_em_midia_entrega_de_novo_e_envia_outro_arquivo(
    cliente, sessao, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha, criar_missao
):
    """`RN-09-54`: o caminho realista do prático em mídia — recusado, o
    Guerreiro(a) declara de novo, o que **reabre** a declaração e limpa o
    arquivo anterior, e só então o envio volta a ser aceito. Sem a reabertura,
    o envio seguiria recusado para sempre e a missão ficaria presa."""
    missao, mestre, guerreiro, cabecalhos, _, _ = _cenario_do_pratico_por_http(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_chave,
        criar_sessao_de_teste,
        "video",
    )
    cliente.post(f"/v1/eu/missoes/{missao.id}/desbloqueio", json={}, headers=cabecalhos)
    _enviar_comprovacao(cliente, cabecalhos, missao.id)
    sessao.expire_all()
    desbloqueio = (
        sessao.query(DesbloqueioDaMissao)
        .filter_by(guerreiro_id=guerreiro.id, missao_id=missao.id)
        .one()
    )
    assert desbloqueio.comprovacao_referencia is not None

    julgar_desafio_pratico(
        sessao,
        operador=mestre,
        desbloqueio=desbloqueio,
        cumpriu=False,
        motivo="Não deu para ver a peça montada.",
    )
    sessao.commit()

    # Antes de declarar de novo, o envio segue recusado: a declaração está
    # julgada.
    recusado = cliente.post(
        f"/v1/eu/missoes/{missao.id}/desbloqueio/comprovacao",
        json={"tipo_mime": "video/mp4", "tamanho_declarado": 10},
        headers=cabecalhos,
    )
    assert recusado.status_code == 422

    # Declarar de novo reabre a mesma linha e limpa o arquivo anterior.
    resposta = cliente.post(f"/v1/eu/missoes/{missao.id}/desbloqueio", json={}, headers=cabecalhos)
    assert resposta.status_code == 201, resposta.text
    sessao.expire_all()
    reaberta = (
        sessao.query(DesbloqueioDaMissao)
        .filter_by(guerreiro_id=guerreiro.id, missao_id=missao.id)
        .one()
    )
    assert reaberta.id == desbloqueio.id
    assert reaberta.cumpriu is None
    assert reaberta.motivo_do_julgamento is None
    assert reaberta.comprovacao_referencia is None

    # E agora o envio é aceito de novo.
    _enviar_comprovacao(cliente, cabecalhos, missao.id)
    sessao.expire_all()
    com_arquivo_novo = (
        sessao.query(DesbloqueioDaMissao)
        .filter_by(guerreiro_id=guerreiro.id, missao_id=missao.id)
        .one()
    )
    assert com_arquivo_novo.comprovacao_referencia is not None
    assert com_arquivo_novo.cumpriu is None


def test_reabrir_a_declaracao_recoloca_o_momento_da_entrega(
    sessao, criar_persona, criar_trilha, criar_missao
):
    """`RN-09-54` com `RF-05-79`: a cadência de retomada conta o prazo de
    `momento`. Antes desta fatia a linha recusada era apagada e a declaração
    seguinte nascia com momento novo; mantendo o da primeira entrega, as
    retomadas de 2, 7 e 21 dias chegariam vencidas a quem foi recusado e
    entregou de novo semanas depois. O prazo corre da entrega aceita."""
    from datetime import UTC, datetime, timedelta

    mestre, guerreiro, _, missao, desbloqueio = _declarado_em_texto(
        sessao, criar_persona, criar_trilha, criar_missao
    )
    # O estado de quem declarou há muito tempo e foi recusado.
    antigo = datetime(2026, 1, 1, tzinfo=UTC)
    desbloqueio.momento = antigo
    sessao.commit()
    julgar_desafio_pratico(
        sessao,
        operador=mestre,
        desbloqueio=desbloqueio,
        cumpriu=False,
        motivo="Faltou mostrar a peça montada.",
    )
    sessao.commit()

    de_novo = submeter_desafio_de_desbloqueio(
        sessao, guerreiro=guerreiro, missao=missao, comprovacao="Agora mostrei inteira."
    )
    sessao.commit()

    assert de_novo.desbloqueio.momento > antigo + timedelta(days=300)
