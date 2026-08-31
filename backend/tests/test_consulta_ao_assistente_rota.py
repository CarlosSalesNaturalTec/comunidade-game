"""A consulta ao assistente de trilhas — `RF-04-36` a `RF-04-40`,
`RN-04-19` a `RN-04-21`, PRD-04 §9."""

import io

from nucleo.assistente.fabrica import dependencia_do_assistente
from nucleo.assistente.modelo import ConsultaAoAssistente
from nucleo.assistente.porta import PortaDoAssistente
from nucleo.conteudos.modelo import TipoDeConteudo
from nucleo.livro_razao.modelo import Lancamento
from nucleo.personas.modelo import Papel
from nucleo.resultados.modelo import Resultado
from nucleo.trilhas.modelo import SituacaoDaTrilha


def _cabecalhos(chave, token):
    return {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}


def _montar_equipe_com_missao_corrente(
    *,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_equipe,
    criar_conteudo_da_missao,
    sessao,
    corpo_da_missao_corrente="Variável é um espaço na memória para guardar um valor.",
):
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(admin, comunidade)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    missao = criar_missao(trilha, mestre, titulo="Programação", posicao=1)
    criar_conteudo_da_missao(
        missao, mestre, tipo=TipoDeConteudo.texto, corpo=corpo_da_missao_corrente
    )
    atividade = criar_atividade(missao, mestre, aula=aula)
    equipe = criar_equipe(guerreiro, aula=aula)
    equipe.atividade_corrente_id = atividade.id
    sessao.commit()
    return guerreiro, equipe, trilha, missao


def test_integrante_pergunta_pela_equipe(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_equipe,
    criar_conteudo_da_missao,
    criar_sessao_de_teste,
    sessao,
):
    chave, _ = criar_chave()
    guerreiro, equipe, _, _ = _montar_equipe_com_missao_corrente(
        criar_persona=criar_persona,
        criar_comunidade=criar_comunidade,
        criar_aula=criar_aula,
        criar_trilha=criar_trilha,
        criar_missao=criar_missao,
        criar_atividade=criar_atividade,
        criar_equipe=criar_equipe,
        criar_conteudo_da_missao=criar_conteudo_da_missao,
        sessao=sessao,
    )
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.post(
        "/v1/assistente/trilhas/consultas",
        data={"equipe_id": str(equipe.id), "texto": "O que é uma variável?"},
        headers=_cabecalhos(chave, token),
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["desfecho"] == "respondida"
    assert corpo["equipe_id"] == str(equipe.id)
    assert corpo["guerreiro_id"] is None
    assert corpo["assistente"] == "trilhas"
    assert sessao.query(ConsultaAoAssistente).filter_by(equipe_id=equipe.id).count() == 1


def test_quem_nao_integra_a_equipe_e_recusado(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_equipe,
    criar_conteudo_da_missao,
    criar_sessao_de_teste,
    sessao,
):
    chave, _ = criar_chave()
    _, equipe, _, _ = _montar_equipe_com_missao_corrente(
        criar_persona=criar_persona,
        criar_comunidade=criar_comunidade,
        criar_aula=criar_aula,
        criar_trilha=criar_trilha,
        criar_missao=criar_missao,
        criar_atividade=criar_atividade,
        criar_equipe=criar_equipe,
        criar_conteudo_da_missao=criar_conteudo_da_missao,
        sessao=sessao,
    )
    de_fora = criar_persona(Papel.guerreiro)
    token, _ = criar_sessao_de_teste(de_fora)

    resposta = cliente.post(
        "/v1/assistente/trilhas/consultas",
        data={"equipe_id": str(equipe.id), "texto": "Uma pergunta qualquer"},
        headers=_cabecalhos(chave, token),
    )

    assert resposta.status_code == 403
    assert sessao.query(ConsultaAoAssistente).count() == 0


def test_mestre_e_admin_nao_consultam_pela_equipe(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_equipe,
    criar_conteudo_da_missao,
    criar_sessao_de_teste,
    sessao,
):
    chave, _ = criar_chave()
    _, equipe, _, _ = _montar_equipe_com_missao_corrente(
        criar_persona=criar_persona,
        criar_comunidade=criar_comunidade,
        criar_aula=criar_aula,
        criar_trilha=criar_trilha,
        criar_missao=criar_missao,
        criar_atividade=criar_atividade,
        criar_equipe=criar_equipe,
        criar_conteudo_da_missao=criar_conteudo_da_missao,
        sessao=sessao,
    )
    for operador in (criar_persona(Papel.mestre), criar_persona(Papel.admin)):
        token, _ = criar_sessao_de_teste(operador)
        resposta = cliente.post(
            "/v1/assistente/trilhas/consultas",
            data={"equipe_id": str(equipe.id), "texto": "Uma pergunta qualquer"},
            headers=_cabecalhos(chave, token),
        )
        assert resposta.status_code == 403
    assert sessao.query(ConsultaAoAssistente).count() == 0


def test_duas_formas_juntas_e_recusada(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_equipe,
    criar_conteudo_da_missao,
    criar_sessao_de_teste,
    sessao,
):
    chave, _ = criar_chave()
    guerreiro, equipe, _, _ = _montar_equipe_com_missao_corrente(
        criar_persona=criar_persona,
        criar_comunidade=criar_comunidade,
        criar_aula=criar_aula,
        criar_trilha=criar_trilha,
        criar_missao=criar_missao,
        criar_atividade=criar_atividade,
        criar_equipe=criar_equipe,
        criar_conteudo_da_missao=criar_conteudo_da_missao,
        sessao=sessao,
    )
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.post(
        "/v1/assistente/trilhas/consultas",
        data={"equipe_id": str(equipe.id), "texto": "Uma pergunta"},
        files={"arquivo": ("fala.webm", io.BytesIO(b"audio-fake"), "audio/webm")},
        headers=_cabecalhos(chave, token),
    )

    assert resposta.status_code == 422
    assert sessao.query(ConsultaAoAssistente).count() == 0


def test_nenhuma_forma_e_recusada(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_equipe,
    criar_conteudo_da_missao,
    criar_sessao_de_teste,
    sessao,
):
    chave, _ = criar_chave()
    guerreiro, equipe, _, _ = _montar_equipe_com_missao_corrente(
        criar_persona=criar_persona,
        criar_comunidade=criar_comunidade,
        criar_aula=criar_aula,
        criar_trilha=criar_trilha,
        criar_missao=criar_missao,
        criar_atividade=criar_atividade,
        criar_equipe=criar_equipe,
        criar_conteudo_da_missao=criar_conteudo_da_missao,
        sessao=sessao,
    )
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.post(
        "/v1/assistente/trilhas/consultas",
        data={"equipe_id": str(equipe.id)},
        headers=_cabecalhos(chave, token),
    )

    assert resposta.status_code == 422
    assert sessao.query(ConsultaAoAssistente).count() == 0


def test_equipe_sem_atividade_corrente_e_recusada(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_equipe,
    criar_sessao_de_teste,
    sessao,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade)
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    equipe = criar_equipe(guerreiro, aula=aula)
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.post(
        "/v1/assistente/trilhas/consultas",
        data={"equipe_id": str(equipe.id), "texto": "Uma pergunta"},
        headers=_cabecalhos(chave, token),
    )

    assert resposta.status_code == 422
    assert sessao.query(ConsultaAoAssistente).count() == 0


def test_pergunta_fora_do_corpus_recebe_200_com_recusa_explicada(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_equipe,
    criar_conteudo_da_missao,
    criar_sessao_de_teste,
    sessao,
):
    chave, _ = criar_chave()
    guerreiro, equipe, _, _ = _montar_equipe_com_missao_corrente(
        criar_persona=criar_persona,
        criar_comunidade=criar_comunidade,
        criar_aula=criar_aula,
        criar_trilha=criar_trilha,
        criar_missao=criar_missao,
        criar_atividade=criar_atividade,
        criar_equipe=criar_equipe,
        criar_conteudo_da_missao=criar_conteudo_da_missao,
        sessao=sessao,
    )
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.post(
        "/v1/assistente/trilhas/consultas",
        data={"equipe_id": str(equipe.id), "texto": "Qual é a capital da Mongólia?"},
        headers=_cabecalhos(chave, token),
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["desfecho"] == "fora_do_corpus"
    assert "Mestre" in corpo["resposta"]
    consulta = sessao.query(ConsultaAoAssistente).filter_by(equipe_id=equipe.id).one()
    assert consulta.desfecho.value == "fora_do_corpus"


def test_pergunta_de_tarefa_escolar_e_encaminhada(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_equipe,
    criar_conteudo_da_missao,
    criar_sessao_de_teste,
    sessao,
):
    chave, _ = criar_chave()
    guerreiro, equipe, _, _ = _montar_equipe_com_missao_corrente(
        criar_persona=criar_persona,
        criar_comunidade=criar_comunidade,
        criar_aula=criar_aula,
        criar_trilha=criar_trilha,
        criar_missao=criar_missao,
        criar_atividade=criar_atividade,
        criar_equipe=criar_equipe,
        criar_conteudo_da_missao=criar_conteudo_da_missao,
        sessao=sessao,
    )
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.post(
        "/v1/assistente/trilhas/consultas",
        data={"equipe_id": str(equipe.id), "texto": "Preciso fazer o dever de casa de história"},
        headers=_cabecalhos(chave, token),
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["desfecho"] == "tarefa_escolar"
    assert "App 05" in corpo["resposta"]


def test_missao_posterior_nao_entra_no_corpus(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_equipe,
    criar_conteudo_da_missao,
    criar_sessao_de_teste,
    sessao,
):
    """`RN-04-19`, design — decisão 2: assunto de missão à frente não entra
    no corpus, e a pergunta sobre ele recebe a recusa explicada."""
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(admin, comunidade)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    missao_corrente = criar_missao(trilha, mestre, titulo="Missão 1", posicao=1)
    criar_conteudo_da_missao(
        missao_corrente, mestre, tipo=TipoDeConteudo.texto, corpo="Conteúdo da missão corrente."
    )
    missao_futura = criar_missao(trilha, mestre, titulo="Missão 2", posicao=2)
    criar_conteudo_da_missao(
        missao_futura,
        mestre,
        tipo=TipoDeConteudo.texto,
        corpo="Segredo exclusivo da missão futura sobre criptografia quântica.",
    )
    atividade = criar_atividade(missao_corrente, mestre, aula=aula)
    equipe = criar_equipe(guerreiro, aula=aula)
    equipe.atividade_corrente_id = atividade.id
    sessao.commit()
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.post(
        "/v1/assistente/trilhas/consultas",
        data={"equipe_id": str(equipe.id), "texto": "O que é criptografia quântica?"},
        headers=_cabecalhos(chave, token),
    )

    assert resposta.status_code == 200
    assert resposta.json()["desfecho"] == "fora_do_corpus"


def test_missao_anterior_entra_no_corpus(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_equipe,
    criar_conteudo_da_missao,
    criar_sessao_de_teste,
    sessao,
):
    """A missão já percorrida entra no corpus da corrente (design —
    decisão 2)."""
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(admin, comunidade)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    missao_anterior = criar_missao(trilha, mestre, titulo="Missão 1", posicao=1)
    criar_conteudo_da_missao(
        missao_anterior,
        mestre,
        tipo=TipoDeConteudo.texto,
        corpo="Algoritmo é uma sequência de passos para resolver um problema.",
    )
    missao_corrente = criar_missao(trilha, mestre, titulo="Missão 2", posicao=2)
    criar_conteudo_da_missao(
        missao_corrente, mestre, tipo=TipoDeConteudo.texto, corpo="Conteúdo da missão corrente."
    )
    atividade = criar_atividade(missao_corrente, mestre, aula=aula)
    equipe = criar_equipe(guerreiro, aula=aula)
    equipe.atividade_corrente_id = atividade.id
    sessao.commit()
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.post(
        "/v1/assistente/trilhas/consultas",
        data={"equipe_id": str(equipe.id), "texto": "O que é um algoritmo?"},
        headers=_cabecalhos(chave, token),
    )

    assert resposta.status_code == 200
    assert resposta.json()["desfecho"] == "respondida"


class _PortaSempreIndisponivel(PortaDoAssistente):
    def responder(self, *, texto, arquivo, corpus):
        return None


def test_indisponibilidade_nao_grava_nada(
    app,
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_equipe,
    criar_conteudo_da_missao,
    criar_sessao_de_teste,
    sessao,
):
    app.dependency_overrides[dependencia_do_assistente] = lambda: _PortaSempreIndisponivel()
    try:
        chave, _ = criar_chave()
        guerreiro, equipe, _, _ = _montar_equipe_com_missao_corrente(
            criar_persona=criar_persona,
            criar_comunidade=criar_comunidade,
            criar_aula=criar_aula,
            criar_trilha=criar_trilha,
            criar_missao=criar_missao,
            criar_atividade=criar_atividade,
            criar_equipe=criar_equipe,
            criar_conteudo_da_missao=criar_conteudo_da_missao,
            sessao=sessao,
        )
        token, _ = criar_sessao_de_teste(guerreiro)

        resposta = cliente.post(
            "/v1/assistente/trilhas/consultas",
            data={"equipe_id": str(equipe.id), "texto": "Uma pergunta qualquer"},
            headers=_cabecalhos(chave, token),
        )

        assert resposta.status_code == 503
        assert sessao.query(ConsultaAoAssistente).count() == 0
    finally:
        del app.dependency_overrides[dependencia_do_assistente]


def test_consulta_nao_credita_ponto_nem_gera_resultado(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_equipe,
    criar_conteudo_da_missao,
    criar_sessao_de_teste,
    sessao,
):
    chave, _ = criar_chave()
    guerreiro, equipe, _, _ = _montar_equipe_com_missao_corrente(
        criar_persona=criar_persona,
        criar_comunidade=criar_comunidade,
        criar_aula=criar_aula,
        criar_trilha=criar_trilha,
        criar_missao=criar_missao,
        criar_atividade=criar_atividade,
        criar_equipe=criar_equipe,
        criar_conteudo_da_missao=criar_conteudo_da_missao,
        sessao=sessao,
    )
    token, _ = criar_sessao_de_teste(guerreiro)

    for _ in range(3):
        resposta = cliente.post(
            "/v1/assistente/trilhas/consultas",
            data={"equipe_id": str(equipe.id), "texto": "O que é uma variável?"},
            headers=_cabecalhos(chave, token),
        )
        assert resposta.status_code == 200

    assert sessao.query(ConsultaAoAssistente).filter_by(equipe_id=equipe.id).count() == 3
    assert sessao.query(Resultado).count() == 0
    assert sessao.query(Lancamento).count() == 0


def test_pergunta_por_audio_e_transcrita(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_equipe,
    criar_conteudo_da_missao,
    criar_sessao_de_teste,
    sessao,
):
    chave, _ = criar_chave()
    guerreiro, equipe, _, _ = _montar_equipe_com_missao_corrente(
        criar_persona=criar_persona,
        criar_comunidade=criar_comunidade,
        criar_aula=criar_aula,
        criar_trilha=criar_trilha,
        criar_missao=criar_missao,
        criar_atividade=criar_atividade,
        criar_equipe=criar_equipe,
        criar_conteudo_da_missao=criar_conteudo_da_missao,
        sessao=sessao,
    )
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.post(
        "/v1/assistente/trilhas/consultas",
        data={"equipe_id": str(equipe.id)},
        files={"arquivo": ("fala.webm", io.BytesIO(b"audio-fake"), "audio/webm")},
        headers=_cabecalhos(chave, token),
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["pergunta"]
    assert "audio-fake" not in corpo["pergunta"]


def test_rota_aparece_no_openapi_sob_v1(cliente):
    """`RF-01-02`: a rota nasce sob `/v1`, na mesma exigência de chave de
    aplicação das demais rotas de dados (`principal.incluir_roteador_de_dados`)."""
    schema = cliente.get("/openapi.json").json()
    assert "/v1/assistente/trilhas/consultas" in schema["paths"]


def test_sem_sessao_a_porta_nao_abre(cliente, criar_chave):
    chave, _ = criar_chave()
    resposta = cliente.post(
        "/v1/assistente/trilhas/consultas",
        data={"equipe_id": "00000000-0000-0000-0000-000000000000", "texto": "Uma pergunta"},
        headers={"X-Chave-Aplicacao": chave},
    )
    assert resposta.status_code == 401
