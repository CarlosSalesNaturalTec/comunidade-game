"""A entrega da produção da missão pela equipe e a entrega individual do
Guerreiro(a) — `RF-04-45` a `RF-04-47`, `RN-04-31`, do PRD-04 §9; `RF-05-74`
a `RF-05-78`, `RN-05-05`, `RN-05-21`, `RN-05-35` a `RN-05-37`, do PRD-05 §9."""

import io

from nucleo.livro_razao.modelo import Lancamento
from nucleo.personas.modelo import Papel
from nucleo.producoes.modelo import ProducaoDaMissao
from nucleo.resultados.modelo import Resultado
from nucleo.trilhas.modelo import SituacaoDaTrilha


def _cabecalhos(chave, token):
    return {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}


def _montar_guerreiro_com_missao_desbloqueada(
    *,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_inscricao_na_trilha,
    criar_desbloqueio_da_missao,
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    missao = criar_missao(trilha, mestre)
    atividade = criar_atividade(missao, mestre, producao_esperada="Um texto sobre o tema.")
    criar_inscricao_na_trilha(guerreiro, trilha)
    criar_desbloqueio_da_missao(guerreiro, missao, aprovado=True)
    return guerreiro, trilha, missao, atividade


def _montar_equipe_com_atividade_corrente(
    *,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_equipe,
    sessao,
):
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(admin, comunidade)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    missao = criar_missao(trilha, mestre)
    atividade = criar_atividade(
        missao, mestre, aula=aula, producao_esperada="Um texto sobre o tema."
    )
    equipe = criar_equipe(guerreiro, aula=aula)
    equipe.atividade_corrente_id = atividade.id
    sessao.commit()
    return guerreiro, equipe, missao, atividade


def test_entrega_por_texto(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_equipe,
    criar_sessao_de_teste,
    sessao,
):
    chave, _ = criar_chave()
    guerreiro, equipe, missao, atividade = _montar_equipe_com_atividade_corrente(
        criar_persona=criar_persona,
        criar_comunidade=criar_comunidade,
        criar_aula=criar_aula,
        criar_trilha=criar_trilha,
        criar_missao=criar_missao,
        criar_atividade=criar_atividade,
        criar_equipe=criar_equipe,
        sessao=sessao,
    )
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.post(
        f"/v1/equipes/{equipe.id}/producao",
        data={"forma": "texto", "texto": "Minha produção em texto."},
        headers=_cabecalhos(chave, token),
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["forma"] == "texto"
    assert corpo["transcricao"] == "Minha produção em texto."
    assert corpo["equipe_id"] == str(equipe.id)
    assert corpo["guerreiro_id"] is None
    assert corpo["missao_id"] == str(missao.id)
    assert corpo["atividade_id"] == str(atividade.id)
    assert "foto" not in corpo
    assert "audio" not in corpo


def test_entrega_por_fala(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_equipe,
    criar_sessao_de_teste,
    sessao,
):
    chave, _ = criar_chave()
    guerreiro, equipe, _, _ = _montar_equipe_com_atividade_corrente(
        criar_persona=criar_persona,
        criar_comunidade=criar_comunidade,
        criar_aula=criar_aula,
        criar_trilha=criar_trilha,
        criar_missao=criar_missao,
        criar_atividade=criar_atividade,
        criar_equipe=criar_equipe,
        sessao=sessao,
    )
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.post(
        f"/v1/equipes/{equipe.id}/producao",
        data={"forma": "audio"},
        files={"arquivo": ("fala.webm", io.BytesIO(b"audio-fake"), "audio/webm")},
        headers=_cabecalhos(chave, token),
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["forma"] == "audio"
    assert corpo["transcricao"]


def test_entrega_por_foto_do_manuscrito(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_equipe,
    criar_sessao_de_teste,
    sessao,
):
    chave, _ = criar_chave()
    guerreiro, equipe, _, _ = _montar_equipe_com_atividade_corrente(
        criar_persona=criar_persona,
        criar_comunidade=criar_comunidade,
        criar_aula=criar_aula,
        criar_trilha=criar_trilha,
        criar_missao=criar_missao,
        criar_atividade=criar_atividade,
        criar_equipe=criar_equipe,
        sessao=sessao,
    )
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.post(
        f"/v1/equipes/{equipe.id}/producao",
        data={"forma": "foto"},
        files={"arquivo": ("manuscrito.jpg", io.BytesIO(b"foto-fake"), "image/jpeg")},
        headers=_cabecalhos(chave, token),
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["forma"] == "foto"
    assert corpo["transcricao"]


def test_entrega_sem_conteudo_e_recusada(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_equipe,
    criar_sessao_de_teste,
    sessao,
):
    chave, _ = criar_chave()
    guerreiro, equipe, _, _ = _montar_equipe_com_atividade_corrente(
        criar_persona=criar_persona,
        criar_comunidade=criar_comunidade,
        criar_aula=criar_aula,
        criar_trilha=criar_trilha,
        criar_missao=criar_missao,
        criar_atividade=criar_atividade,
        criar_equipe=criar_equipe,
        sessao=sessao,
    )
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.post(
        f"/v1/equipes/{equipe.id}/producao",
        data={"forma": "texto"},
        headers=_cabecalhos(chave, token),
    )

    assert resposta.status_code == 422
    assert sessao.query(ProducaoDaMissao).count() == 0


def test_entrega_com_duas_formas_e_recusada(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_equipe,
    criar_sessao_de_teste,
    sessao,
):
    chave, _ = criar_chave()
    guerreiro, equipe, _, _ = _montar_equipe_com_atividade_corrente(
        criar_persona=criar_persona,
        criar_comunidade=criar_comunidade,
        criar_aula=criar_aula,
        criar_trilha=criar_trilha,
        criar_missao=criar_missao,
        criar_atividade=criar_atividade,
        criar_equipe=criar_equipe,
        sessao=sessao,
    )
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.post(
        f"/v1/equipes/{equipe.id}/producao",
        data={"forma": "texto", "texto": "Um texto"},
        files={"arquivo": ("foto.jpg", io.BytesIO(b"foto-fake"), "image/jpeg")},
        headers=_cabecalhos(chave, token),
    )

    assert resposta.status_code == 422
    assert sessao.query(ProducaoDaMissao).count() == 0


def test_equipe_sem_atividade_corrente_nao_entrega(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_equipe,
    criar_sessao_de_teste,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade)
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    equipe = criar_equipe(guerreiro, aula=aula)
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.post(
        f"/v1/equipes/{equipe.id}/producao",
        data={"forma": "texto", "texto": "Um texto"},
        headers=_cabecalhos(chave, token),
    )

    assert resposta.status_code == 422


def test_um_registro_por_equipe_com_guerreiro_em_branco(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_equipe,
    adicionar_integrante,
    criar_sessao_de_teste,
    sessao,
):
    chave, _ = criar_chave()
    guerreiro, equipe, _, _ = _montar_equipe_com_atividade_corrente(
        criar_persona=criar_persona,
        criar_comunidade=criar_comunidade,
        criar_aula=criar_aula,
        criar_trilha=criar_trilha,
        criar_missao=criar_missao,
        criar_atividade=criar_atividade,
        criar_equipe=criar_equipe,
        sessao=sessao,
    )
    outros = [criar_persona(Papel.guerreiro) for _ in range(4)]
    for outro in outros:
        adicionar_integrante(equipe, outro)
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.post(
        f"/v1/equipes/{equipe.id}/producao",
        data={"forma": "texto", "texto": "Produção da equipe inteira."},
        headers=_cabecalhos(chave, token),
    )

    assert resposta.status_code == 201
    producoes = sessao.query(ProducaoDaMissao).filter_by(equipe_id=equipe.id).all()
    assert len(producoes) == 1
    assert producoes[0].guerreiro_id is None


def test_producao_da_equipe_alcanca_todos_os_integrantes(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_equipe,
    adicionar_integrante,
    criar_sessao_de_teste,
    sessao,
):
    """`RF-04-45`, documento 02 §5: a produção da equipe está entre as de um
    integrante que não foi quem enviou — consultada pela composição
    gravada, sem cópia por integrante."""
    from nucleo.equipes.modelo import IntegranteDaEquipe

    chave, _ = criar_chave()
    guerreiro, equipe, _, _ = _montar_equipe_com_atividade_corrente(
        criar_persona=criar_persona,
        criar_comunidade=criar_comunidade,
        criar_aula=criar_aula,
        criar_trilha=criar_trilha,
        criar_missao=criar_missao,
        criar_atividade=criar_atividade,
        criar_equipe=criar_equipe,
        sessao=sessao,
    )
    outro_integrante = criar_persona(Papel.guerreiro)
    adicionar_integrante(equipe, outro_integrante)
    token, _ = criar_sessao_de_teste(guerreiro)

    cliente.post(
        f"/v1/equipes/{equipe.id}/producao",
        data={"forma": "texto", "texto": "Produção enviada por outra pessoa."},
        headers=_cabecalhos(chave, token),
    )

    equipes_do_outro = {
        i.equipe_id
        for i in sessao.query(IntegranteDaEquipe).filter_by(persona_id=outro_integrante.id)
    }
    producoes_do_outro = (
        sessao.query(ProducaoDaMissao)
        .filter(ProducaoDaMissao.equipe_id.in_(equipes_do_outro))
        .all()
    )
    assert len(producoes_do_outro) == 1


def test_devolutiva_nao_credita_ponto_nem_gera_resultado(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_equipe,
    criar_sessao_de_teste,
    sessao,
):
    chave, _ = criar_chave()
    guerreiro, equipe, _, _ = _montar_equipe_com_atividade_corrente(
        criar_persona=criar_persona,
        criar_comunidade=criar_comunidade,
        criar_aula=criar_aula,
        criar_trilha=criar_trilha,
        criar_missao=criar_missao,
        criar_atividade=criar_atividade,
        criar_equipe=criar_equipe,
        sessao=sessao,
    )
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.post(
        f"/v1/equipes/{equipe.id}/producao",
        data={"forma": "texto", "texto": "Uma produção qualquer."},
        headers=_cabecalhos(chave, token),
    )

    assert resposta.status_code == 201
    assert resposta.json()["devolutiva"]
    assert sessao.query(Resultado).count() == 0
    assert sessao.query(Lancamento).count() == 0


def test_varias_entregas_nao_mudam_nivel_nem_percurso(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_equipe,
    criar_sessao_de_teste,
    sessao,
):
    """`RN-04-31`: nem a devolutiva nem o número de entregas alteram o
    percurso de nenhum integrante — não há chave de personalização
    consultada em nenhum ponto de `registrar_producao`."""
    chave, _ = criar_chave()
    guerreiro, equipe, _, _ = _montar_equipe_com_atividade_corrente(
        criar_persona=criar_persona,
        criar_comunidade=criar_comunidade,
        criar_aula=criar_aula,
        criar_trilha=criar_trilha,
        criar_missao=criar_missao,
        criar_atividade=criar_atividade,
        criar_equipe=criar_equipe,
        sessao=sessao,
    )
    token, _ = criar_sessao_de_teste(guerreiro)

    for indice in range(3):
        resposta = cliente.post(
            f"/v1/equipes/{equipe.id}/producao",
            data={"forma": "texto", "texto": f"Produção número {indice}."},
            headers=_cabecalhos(chave, token),
        )
        assert resposta.status_code == 201

    assert sessao.query(ProducaoDaMissao).filter_by(equipe_id=equipe.id).count() == 3
    assert sessao.query(Resultado).count() == 0
    assert sessao.query(Lancamento).count() == 0


def test_quem_nao_integra_a_equipe_nao_entrega_por_ela(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_equipe,
    criar_sessao_de_teste,
    sessao,
):
    chave, _ = criar_chave()
    _, equipe, _, _ = _montar_equipe_com_atividade_corrente(
        criar_persona=criar_persona,
        criar_comunidade=criar_comunidade,
        criar_aula=criar_aula,
        criar_trilha=criar_trilha,
        criar_missao=criar_missao,
        criar_atividade=criar_atividade,
        criar_equipe=criar_equipe,
        sessao=sessao,
    )
    de_fora = criar_persona(Papel.guerreiro)
    token, _ = criar_sessao_de_teste(de_fora)

    resposta = cliente.post(
        f"/v1/equipes/{equipe.id}/producao",
        data={"forma": "texto", "texto": "Um texto"},
        headers=_cabecalhos(chave, token),
    )

    assert resposta.status_code == 403


def test_mestre_e_admin_nao_entregam_pela_equipe(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_equipe,
    criar_sessao_de_teste,
    sessao,
):
    chave, _ = criar_chave()
    _, equipe, _, _ = _montar_equipe_com_atividade_corrente(
        criar_persona=criar_persona,
        criar_comunidade=criar_comunidade,
        criar_aula=criar_aula,
        criar_trilha=criar_trilha,
        criar_missao=criar_missao,
        criar_atividade=criar_atividade,
        criar_equipe=criar_equipe,
        sessao=sessao,
    )
    for operador in (criar_persona(Papel.mestre), criar_persona(Papel.admin)):
        token, _ = criar_sessao_de_teste(operador)
        resposta = cliente.post(
            f"/v1/equipes/{equipe.id}/producao",
            data={"forma": "texto", "texto": "Um texto"},
            headers=_cabecalhos(chave, token),
        )
        assert resposta.status_code == 403


def test_equipe_de_aula_encerrada_nao_entrega(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_equipe,
    criar_sessao_de_teste,
    sessao,
):
    from datetime import UTC, datetime, timedelta

    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(
        admin,
        comunidade,
        inicio_em=datetime.now(UTC) - timedelta(hours=3),
        fim_em=datetime.now(UTC) - timedelta(hours=1),
    )
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    missao = criar_missao(trilha, mestre)
    atividade = criar_atividade(missao, mestre, aula=aula)
    equipe = criar_equipe(guerreiro, aula=aula)
    equipe.atividade_corrente_id = atividade.id
    sessao.commit()
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.post(
        f"/v1/equipes/{equipe.id}/producao",
        data={"forma": "texto", "texto": "Um texto"},
        headers=_cabecalhos(chave, token),
    )

    assert resposta.status_code == 422


def test_sem_sessao_a_porta_nao_abre(cliente, criar_chave):
    chave, _ = criar_chave()
    resposta = cliente.post(
        "/v1/equipes/00000000-0000-0000-0000-000000000000/producao",
        data={"forma": "texto", "texto": "Um texto"},
        headers={"X-Chave-Aplicacao": chave},
    )
    assert resposta.status_code == 401


# --- A entrega individual do Guerreiro(a) — `RF-05-74` a `RF-05-78` ---


def test_entrega_individual_por_texto(
    cliente,
    criar_chave,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_inscricao_na_trilha,
    criar_desbloqueio_da_missao,
    criar_sessao_de_teste,
    sessao,
):
    chave, _ = criar_chave()
    guerreiro, _, missao, atividade = _montar_guerreiro_com_missao_desbloqueada(
        criar_persona=criar_persona,
        criar_trilha=criar_trilha,
        criar_missao=criar_missao,
        criar_atividade=criar_atividade,
        criar_inscricao_na_trilha=criar_inscricao_na_trilha,
        criar_desbloqueio_da_missao=criar_desbloqueio_da_missao,
    )
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.post(
        f"/v1/eu/missoes/{missao.id}/producao",
        data={
            "forma": "texto",
            "texto": "Minha produção sozinho.",
            "atividade_id": str(atividade.id),
        },
        headers=_cabecalhos(chave, token),
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["forma"] == "texto"
    assert corpo["transcricao"] == "Minha produção sozinho."
    assert corpo["equipe_id"] is None
    assert corpo["guerreiro_id"] == str(guerreiro.id)
    assert corpo["missao_id"] == str(missao.id)
    assert corpo["atividade_id"] == str(atividade.id)


def test_entrega_individual_por_fala(
    cliente,
    criar_chave,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_inscricao_na_trilha,
    criar_desbloqueio_da_missao,
    criar_sessao_de_teste,
    sessao,
):
    chave, _ = criar_chave()
    guerreiro, _, missao, atividade = _montar_guerreiro_com_missao_desbloqueada(
        criar_persona=criar_persona,
        criar_trilha=criar_trilha,
        criar_missao=criar_missao,
        criar_atividade=criar_atividade,
        criar_inscricao_na_trilha=criar_inscricao_na_trilha,
        criar_desbloqueio_da_missao=criar_desbloqueio_da_missao,
    )
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.post(
        f"/v1/eu/missoes/{missao.id}/producao",
        data={"forma": "audio", "atividade_id": str(atividade.id)},
        files={"arquivo": ("fala.webm", io.BytesIO(b"audio-fake"), "audio/webm")},
        headers=_cabecalhos(chave, token),
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["forma"] == "audio"
    assert corpo["transcricao"]


def test_entrega_individual_por_foto_do_manuscrito(
    cliente,
    criar_chave,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_inscricao_na_trilha,
    criar_desbloqueio_da_missao,
    criar_sessao_de_teste,
    sessao,
):
    chave, _ = criar_chave()
    guerreiro, _, missao, atividade = _montar_guerreiro_com_missao_desbloqueada(
        criar_persona=criar_persona,
        criar_trilha=criar_trilha,
        criar_missao=criar_missao,
        criar_atividade=criar_atividade,
        criar_inscricao_na_trilha=criar_inscricao_na_trilha,
        criar_desbloqueio_da_missao=criar_desbloqueio_da_missao,
    )
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.post(
        f"/v1/eu/missoes/{missao.id}/producao",
        data={"forma": "foto", "atividade_id": str(atividade.id)},
        files={"arquivo": ("manuscrito.jpg", io.BytesIO(b"foto-fake"), "image/jpeg")},
        headers=_cabecalhos(chave, token),
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["forma"] == "foto"
    assert corpo["transcricao"]


def test_entrega_individual_sem_conteudo_e_recusada(
    cliente,
    criar_chave,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_inscricao_na_trilha,
    criar_desbloqueio_da_missao,
    criar_sessao_de_teste,
    sessao,
):
    chave, _ = criar_chave()
    guerreiro, _, missao, atividade = _montar_guerreiro_com_missao_desbloqueada(
        criar_persona=criar_persona,
        criar_trilha=criar_trilha,
        criar_missao=criar_missao,
        criar_atividade=criar_atividade,
        criar_inscricao_na_trilha=criar_inscricao_na_trilha,
        criar_desbloqueio_da_missao=criar_desbloqueio_da_missao,
    )
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.post(
        f"/v1/eu/missoes/{missao.id}/producao",
        data={"forma": "texto", "atividade_id": str(atividade.id)},
        headers=_cabecalhos(chave, token),
    )

    assert resposta.status_code == 422
    assert sessao.query(ProducaoDaMissao).count() == 0


def test_entrega_individual_com_duas_formas_e_recusada(
    cliente,
    criar_chave,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_inscricao_na_trilha,
    criar_desbloqueio_da_missao,
    criar_sessao_de_teste,
    sessao,
):
    chave, _ = criar_chave()
    guerreiro, _, missao, atividade = _montar_guerreiro_com_missao_desbloqueada(
        criar_persona=criar_persona,
        criar_trilha=criar_trilha,
        criar_missao=criar_missao,
        criar_atividade=criar_atividade,
        criar_inscricao_na_trilha=criar_inscricao_na_trilha,
        criar_desbloqueio_da_missao=criar_desbloqueio_da_missao,
    )
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.post(
        f"/v1/eu/missoes/{missao.id}/producao",
        data={"forma": "texto", "texto": "Um texto", "atividade_id": str(atividade.id)},
        files={"arquivo": ("foto.jpg", io.BytesIO(b"foto-fake"), "image/jpeg")},
        headers=_cabecalhos(chave, token),
    )

    assert resposta.status_code == 422
    assert sessao.query(ProducaoDaMissao).count() == 0


def test_entrega_individual_com_atividade_de_outra_missao_e_recusada(
    cliente,
    criar_chave,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_inscricao_na_trilha,
    criar_desbloqueio_da_missao,
    criar_sessao_de_teste,
    sessao,
):
    chave, _ = criar_chave()
    guerreiro, trilha, missao, _ = _montar_guerreiro_com_missao_desbloqueada(
        criar_persona=criar_persona,
        criar_trilha=criar_trilha,
        criar_missao=criar_missao,
        criar_atividade=criar_atividade,
        criar_inscricao_na_trilha=criar_inscricao_na_trilha,
        criar_desbloqueio_da_missao=criar_desbloqueio_da_missao,
    )
    outra_missao = criar_missao(trilha, criar_persona(Papel.mestre), posicao=2)
    atividade_de_outra_missao = criar_atividade(outra_missao, criar_persona(Papel.mestre))
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.post(
        f"/v1/eu/missoes/{missao.id}/producao",
        data={
            "forma": "texto",
            "texto": "Um texto",
            "atividade_id": str(atividade_de_outra_missao.id),
        },
        headers=_cabecalhos(chave, token),
    )

    assert resposta.status_code == 422
    assert sessao.query(ProducaoDaMissao).count() == 0


def test_entrega_individual_de_trilha_nao_inscrita_e_recusada(
    cliente,
    criar_chave,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_sessao_de_teste,
    sessao,
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    missao = criar_missao(trilha, mestre)
    atividade = criar_atividade(missao, mestre)
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.post(
        f"/v1/eu/missoes/{missao.id}/producao",
        data={"forma": "texto", "texto": "Um texto", "atividade_id": str(atividade.id)},
        headers=_cabecalhos(chave, token),
    )

    assert resposta.status_code == 422
    assert sessao.query(ProducaoDaMissao).count() == 0


def test_entrega_individual_de_missao_nao_desbloqueada_e_recusada(
    cliente,
    criar_chave,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_inscricao_na_trilha,
    criar_sessao_de_teste,
    sessao,
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    missao = criar_missao(trilha, mestre)
    atividade = criar_atividade(missao, mestre)
    criar_inscricao_na_trilha(guerreiro, trilha)
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.post(
        f"/v1/eu/missoes/{missao.id}/producao",
        data={"forma": "texto", "texto": "Um texto", "atividade_id": str(atividade.id)},
        headers=_cabecalhos(chave, token),
    )

    assert resposta.status_code == 422
    assert sessao.query(ProducaoDaMissao).count() == 0


def test_entrega_individual_nasce_com_guerreiro_e_equipe_em_branco(
    cliente,
    criar_chave,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_inscricao_na_trilha,
    criar_desbloqueio_da_missao,
    criar_sessao_de_teste,
    sessao,
):
    chave, _ = criar_chave()
    guerreiro, _, missao, atividade = _montar_guerreiro_com_missao_desbloqueada(
        criar_persona=criar_persona,
        criar_trilha=criar_trilha,
        criar_missao=criar_missao,
        criar_atividade=criar_atividade,
        criar_inscricao_na_trilha=criar_inscricao_na_trilha,
        criar_desbloqueio_da_missao=criar_desbloqueio_da_missao,
    )
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.post(
        f"/v1/eu/missoes/{missao.id}/producao",
        data={"forma": "texto", "texto": "Um texto", "atividade_id": str(atividade.id)},
        headers=_cabecalhos(chave, token),
    )

    assert resposta.status_code == 201
    producoes = sessao.query(ProducaoDaMissao).filter_by(guerreiro_id=guerreiro.id).all()
    assert len(producoes) == 1
    assert producoes[0].equipe_id is None


def test_producao_individual_nao_alcanca_colega(
    cliente,
    criar_chave,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_inscricao_na_trilha,
    criar_desbloqueio_da_missao,
    criar_sessao_de_teste,
    sessao,
):
    chave, _ = criar_chave()
    guerreiro, trilha, missao, atividade = _montar_guerreiro_com_missao_desbloqueada(
        criar_persona=criar_persona,
        criar_trilha=criar_trilha,
        criar_missao=criar_missao,
        criar_atividade=criar_atividade,
        criar_inscricao_na_trilha=criar_inscricao_na_trilha,
        criar_desbloqueio_da_missao=criar_desbloqueio_da_missao,
    )
    colega = criar_persona(Papel.guerreiro)
    criar_inscricao_na_trilha(colega, trilha)
    criar_desbloqueio_da_missao(colega, missao, aprovado=True)
    token, _ = criar_sessao_de_teste(guerreiro)

    cliente.post(
        f"/v1/eu/missoes/{missao.id}/producao",
        data={"forma": "texto", "texto": "Minha produção.", "atividade_id": str(atividade.id)},
        headers=_cabecalhos(chave, token),
    )

    producoes_do_colega = sessao.query(ProducaoDaMissao).filter_by(guerreiro_id=colega.id).all()
    assert len(producoes_do_colega) == 0


def test_devolutiva_individual_nao_credita_ponto_nem_gera_resultado(
    cliente,
    criar_chave,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_inscricao_na_trilha,
    criar_desbloqueio_da_missao,
    criar_sessao_de_teste,
    sessao,
):
    chave, _ = criar_chave()
    guerreiro, _, missao, atividade = _montar_guerreiro_com_missao_desbloqueada(
        criar_persona=criar_persona,
        criar_trilha=criar_trilha,
        criar_missao=criar_missao,
        criar_atividade=criar_atividade,
        criar_inscricao_na_trilha=criar_inscricao_na_trilha,
        criar_desbloqueio_da_missao=criar_desbloqueio_da_missao,
    )
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.post(
        f"/v1/eu/missoes/{missao.id}/producao",
        data={
            "forma": "texto",
            "texto": "Uma produção qualquer.",
            "atividade_id": str(atividade.id),
        },
        headers=_cabecalhos(chave, token),
    )

    assert resposta.status_code == 201
    assert resposta.json()["devolutiva"]
    assert sessao.query(Resultado).count() == 0
    assert sessao.query(Lancamento).count() == 0


def test_entrega_individual_com_arquivo_e_texto_descarta_a_midia(
    cliente,
    criar_chave,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_inscricao_na_trilha,
    criar_desbloqueio_da_missao,
    criar_sessao_de_teste,
    sessao,
):
    """`RF-05-76`, `RN-05-36`: a mídia some da resposta na porta
    individual, igual à porta de equipe."""
    chave, _ = criar_chave()
    guerreiro, _, missao, atividade = _montar_guerreiro_com_missao_desbloqueada(
        criar_persona=criar_persona,
        criar_trilha=criar_trilha,
        criar_missao=criar_missao,
        criar_atividade=criar_atividade,
        criar_inscricao_na_trilha=criar_inscricao_na_trilha,
        criar_desbloqueio_da_missao=criar_desbloqueio_da_missao,
    )
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.post(
        f"/v1/eu/missoes/{missao.id}/producao",
        data={"forma": "foto", "atividade_id": str(atividade.id)},
        files={"arquivo": ("manuscrito.jpg", io.BytesIO(b"foto-fake"), "image/jpeg")},
        headers=_cabecalhos(chave, token),
    )

    corpo = resposta.json()
    assert "foto" not in corpo
    assert "audio" not in corpo
    assert "custo" not in corpo
    assert "cota" not in corpo


def test_so_texto_basta_para_entregar_individualmente(
    cliente,
    criar_chave,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_inscricao_na_trilha,
    criar_desbloqueio_da_missao,
    criar_sessao_de_teste,
    sessao,
):
    """`RF-05-78`, `RN-05-37`: texto basta, sem exigir foto nem áudio."""
    chave, _ = criar_chave()
    guerreiro, _, missao, atividade = _montar_guerreiro_com_missao_desbloqueada(
        criar_persona=criar_persona,
        criar_trilha=criar_trilha,
        criar_missao=criar_missao,
        criar_atividade=criar_atividade,
        criar_inscricao_na_trilha=criar_inscricao_na_trilha,
        criar_desbloqueio_da_missao=criar_desbloqueio_da_missao,
    )
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.post(
        f"/v1/eu/missoes/{missao.id}/producao",
        data={"forma": "texto", "texto": "Só texto.", "atividade_id": str(atividade.id)},
        headers=_cabecalhos(chave, token),
    )

    assert resposta.status_code == 201


def test_missao_sem_producao_individual_segue_desbloqueada(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_inscricao_na_trilha,
    criar_desbloqueio_da_missao,
):
    """`RF-05-78`, `RN-05-37`: não entregar não retira a missão do
    percurso — o desbloqueio já gravado é o que `derivar_percurso` lê."""
    from nucleo.trilhas.regra import derivar_percurso

    guerreiro, trilha, missao, _atividade = _montar_guerreiro_com_missao_desbloqueada(
        criar_persona=criar_persona,
        criar_trilha=criar_trilha,
        criar_missao=criar_missao,
        criar_atividade=criar_atividade,
        criar_inscricao_na_trilha=criar_inscricao_na_trilha,
        criar_desbloqueio_da_missao=criar_desbloqueio_da_missao,
    )

    percurso = derivar_percurso(sessao, guerreiro_id=guerreiro.id, trilha_id=trilha.id)
    item = next(item for item in percurso if item.missao.id == missao.id)
    assert item.desbloqueada is True
