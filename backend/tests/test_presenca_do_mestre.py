from datetime import UTC, datetime

from nucleo.aulas.modelo import ModoDeComprovacao, Presenca
from nucleo.personas.modelo import Papel
from nucleo.trilhas.modelo import FormatoDeAtividade

MOMENTO_DO_FATO = datetime(2026, 8, 1, 10, 0, tzinfo=UTC)


def test_mestre_confirma_a_presenca_que_faltou(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_aula,
    criar_vinculo_jogador,
    sessao,
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    token, _ = criar_sessao_de_teste(mestre)
    comunidade = criar_comunidade()
    criar_vinculo_jogador(mestre, comunidade)
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(mestre, comunidade)

    resposta = cliente.post(
        f"/v1/aulas/{aula.id}/presencas",
        json={
            "guerreiro_id": str(guerreiro.id),
            "modo": "confirmacao",
            "momento_do_fato": MOMENTO_DO_FATO.isoformat(),
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["modo"] == "confirmacao"
    assert corpo["confirmador_id"] == str(mestre.id)

    presenca = sessao.query(Presenca).filter_by(aula_id=aula.id, guerreiro_id=guerreiro.id).one()
    assert presenca.modo == ModoDeComprovacao.confirmacao
    assert presenca.confirmador_id == mestre.id


def test_mestre_nao_registra_presenca_por_reconhecimento(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_aula,
    criar_vinculo_jogador,
    sessao,
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    token, _ = criar_sessao_de_teste(mestre)
    comunidade = criar_comunidade()
    criar_vinculo_jogador(mestre, comunidade)
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(mestre, comunidade)

    resposta = cliente.post(
        f"/v1/aulas/{aula.id}/presencas",
        json={
            "guerreiro_id": str(guerreiro.id),
            "modo": "reconhecimento",
            "momento_do_fato": MOMENTO_DO_FATO.isoformat(),
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 403
    assert sessao.query(Presenca).count() == 0


def test_reenvio_da_mesma_presenca_nao_duplica(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_aula,
    criar_vinculo_jogador,
    sessao,
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    token, _ = criar_sessao_de_teste(mestre)
    comunidade = criar_comunidade()
    criar_vinculo_jogador(mestre, comunidade)
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(mestre, comunidade)

    corpo_da_requisicao = {
        "guerreiro_id": str(guerreiro.id),
        "modo": "confirmacao",
        "momento_do_fato": MOMENTO_DO_FATO.isoformat(),
    }
    headers = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}

    primeira = cliente.post(
        f"/v1/aulas/{aula.id}/presencas", json=corpo_da_requisicao, headers=headers
    )
    segunda = cliente.post(
        f"/v1/aulas/{aula.id}/presencas", json=corpo_da_requisicao, headers=headers
    )

    assert primeira.status_code == 201
    assert segunda.status_code == 201
    assert primeira.json()["id"] == segunda.json()["id"]
    assert sessao.query(Presenca).filter_by(aula_id=aula.id, guerreiro_id=guerreiro.id).count() == 1


def test_papel_sem_a_operacao_e_recusado_na_presenca(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_comunidade, criar_aula
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    token, _ = criar_sessao_de_teste(apoiador)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(admin, comunidade)

    resposta = cliente.post(
        f"/v1/aulas/{aula.id}/presencas",
        json={
            "guerreiro_id": str(guerreiro.id),
            "modo": "confirmacao",
            "momento_do_fato": MOMENTO_DO_FATO.isoformat(),
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 403


def test_mestre_ve_as_proprias_turmas_e_atividades(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_aula,
    criar_vinculo_jogador,
    criar_trilha,
    criar_missao,
    criar_atividade,
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    token, _ = criar_sessao_de_teste(mestre)
    comunidade = criar_comunidade()
    criar_vinculo_jogador(mestre, comunidade)
    aula = criar_aula(mestre, comunidade)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    atividade = criar_atividade(missao, mestre)

    resposta = cliente.get(
        "/v1/minhas-turmas",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert [item["id"] for item in corpo["itens"]] == [str(aula.id)]
    assert [a["id"] for a in corpo["atividades_presenciais"]] == [str(atividade.id)]
    assert corpo["atividades_on_line"] == []


def test_atividade_de_outro_mestre_nao_aparece(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_aula,
    criar_vinculo_jogador,
    criar_trilha,
    criar_missao,
    criar_atividade,
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    outro_mestre = criar_persona(Papel.mestre)
    token, _ = criar_sessao_de_teste(mestre)
    comunidade = criar_comunidade()
    criar_vinculo_jogador(mestre, comunidade)
    criar_aula(mestre, comunidade)
    trilha_do_outro = criar_trilha(outro_mestre)
    missao_do_outro = criar_missao(trilha_do_outro, outro_mestre)
    criar_atividade(missao_do_outro, outro_mestre)

    resposta = cliente.get(
        "/v1/minhas-turmas",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 200
    assert resposta.json()["atividades_presenciais"] == []


def test_atividades_saem_separadas_por_formato(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_aula,
    criar_vinculo_jogador,
    criar_trilha,
    criar_missao,
    criar_atividade,
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    token, _ = criar_sessao_de_teste(mestre)
    comunidade = criar_comunidade()
    criar_vinculo_jogador(mestre, comunidade)
    criar_aula(mestre, comunidade)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    presencial = criar_atividade(missao, mestre, formato=FormatoDeAtividade.presencial)
    on_line = criar_atividade(missao, mestre, formato=FormatoDeAtividade.on_line_assincrona)

    resposta = cliente.get(
        "/v1/minhas-turmas",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    corpo = resposta.json()
    assert [a["id"] for a in corpo["atividades_presenciais"]] == [str(presencial.id)]
    assert [a["id"] for a in corpo["atividades_on_line"]] == [str(on_line.id)]


def test_papel_sem_a_operacao_e_recusado_em_minhas_turmas(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    guerreiro = criar_persona(Papel.guerreiro)
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.get(
        "/v1/minhas-turmas",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 403
