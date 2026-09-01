from datetime import UTC, datetime

from nucleo.auditoria.modelo import AcessoAoDadoDoGuerreiro, Auditoria
from nucleo.personas.modelo import Papel

MOMENTO_DO_FATO = datetime(2026, 8, 1, 10, 0, tzinfo=UTC)


def test_escrita_sobre_uma_crianca_fica_ligada_a_ela(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_aula,
    criar_vinculo_jogador,
    sessao,
    monkeypatch,
    fabrica_de_auditoria,
):
    monkeypatch.setattr(
        "nucleo.auditoria.middleware.obter_fabrica_de_sessao", lambda: fabrica_de_auditoria
    )
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

    registro = sessao.query(Auditoria).one()
    acesso = sessao.query(AcessoAoDadoDoGuerreiro).one()
    assert acesso.auditoria_id == registro.id
    assert acesso.guerreiro_id == guerreiro.id


def test_escrita_sobre_varias_criancas_fica_ligada_a_todas(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_aula,
    criar_trilha,
    criar_missao,
    criar_atividade,
    sessao,
    monkeypatch,
    fabrica_de_auditoria,
):
    monkeypatch.setattr(
        "nucleo.auditoria.middleware.obter_fabrica_de_sessao", lambda: fabrica_de_auditoria
    )
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade)
    guerreiro_1 = criar_persona(Papel.guerreiro, comunidade=comunidade)
    guerreiro_2 = criar_persona(Papel.guerreiro, comunidade=comunidade)
    trilha = criar_trilha(admin)
    missao = criar_missao(trilha, admin)
    atividade = criar_atividade(missao, admin)

    resposta = cliente.post(
        f"/v1/aulas/{aula.id}/lancamentos",
        json={
            "resultados": [
                {
                    "guerreiro_id": str(guerreiro_1.id),
                    "atividade_id": str(atividade.id),
                    "momento_do_fato": MOMENTO_DO_FATO.isoformat(),
                    "producao": "Produção 1.",
                    "desfecho": "realizada",
                },
                {
                    "guerreiro_id": str(guerreiro_2.id),
                    "atividade_id": str(atividade.id),
                    "momento_do_fato": MOMENTO_DO_FATO.isoformat(),
                    "producao": "Produção 2.",
                    "desfecho": "realizada",
                },
            ]
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 201

    registro = sessao.query(Auditoria).one()
    guerreiros_alcancados = {
        acesso.guerreiro_id
        for acesso in sessao.query(AcessoAoDadoDoGuerreiro).filter_by(auditoria_id=registro.id)
    }
    assert guerreiros_alcancados == {guerreiro_1.id, guerreiro_2.id}


def test_escrita_sem_crianca_fica_fora_de_todo_historico(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    sessao,
    monkeypatch,
    fabrica_de_auditoria,
):
    monkeypatch.setattr(
        "nucleo.auditoria.middleware.obter_fabrica_de_sessao", lambda: fabrica_de_auditoria
    )
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.post(
        "/v1/responsaveis",
        json={"nome": "mãe"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 201
    assert sessao.query(Auditoria).count() == 1
    assert sessao.query(AcessoAoDadoDoGuerreiro).count() == 0


def test_acesso_de_rotina_do_mestre_aparece_com_data_hora_e_dado(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_aula,
    criar_vinculo_jogador,
    criar_vinculo,
    monkeypatch,
    fabrica_de_auditoria,
):
    monkeypatch.setattr(
        "nucleo.auditoria.middleware.obter_fabrica_de_sessao", lambda: fabrica_de_auditoria
    )
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    criar_vinculo_jogador(mestre, comunidade)
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    responsavel = criar_persona(Papel.responsavel)
    criar_vinculo(responsavel, guerreiro, cadastrado_por=mestre)
    aula = criar_aula(mestre, comunidade)

    token_do_mestre, _ = criar_sessao_de_teste(mestre)
    cliente.post(
        f"/v1/aulas/{aula.id}/presencas",
        json={
            "guerreiro_id": str(guerreiro.id),
            "modo": "confirmacao",
            "momento_do_fato": MOMENTO_DO_FATO.isoformat(),
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token_do_mestre}"},
    )

    token_do_responsavel, _ = criar_sessao_de_teste(responsavel)
    resposta = cliente.get(
        f"/v1/eu/guerreiros/{guerreiro.id}/acessos",
        headers={
            "X-Chave-Aplicacao": chave,
            "Authorization": f"Bearer {token_do_responsavel}",
        },
    )
    assert resposta.status_code == 200
    corpo = resposta.json()
    assert len(corpo["itens"]) == 1
    item = corpo["itens"][0]
    assert item["momento"] is not None
    assert item["autor_id"] == str(mestre.id)
    assert item["papel_do_autor"] == Papel.mestre.value
    assert "confirmar_presenca_rota" in item["entidade_afetada"]
    assert "conteudo" not in item
    assert "producao" not in item


def test_nenhuma_linha_e_de_outra_crianca(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_aula,
    criar_vinculo_jogador,
    criar_vinculo,
    monkeypatch,
    fabrica_de_auditoria,
):
    monkeypatch.setattr(
        "nucleo.auditoria.middleware.obter_fabrica_de_sessao", lambda: fabrica_de_auditoria
    )
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    criar_vinculo_jogador(mestre, comunidade)
    guerreiro_1 = criar_persona(Papel.guerreiro, comunidade=comunidade)
    guerreiro_2 = criar_persona(Papel.guerreiro, comunidade=comunidade)
    responsavel_1 = criar_persona(Papel.responsavel)
    criar_vinculo(responsavel_1, guerreiro_1, cadastrado_por=mestre)
    aula = criar_aula(mestre, comunidade)

    token_do_mestre, _ = criar_sessao_de_teste(mestre)
    cabecalhos_do_mestre = {
        "X-Chave-Aplicacao": chave,
        "Authorization": f"Bearer {token_do_mestre}",
    }
    for guerreiro in (guerreiro_1, guerreiro_2):
        cliente.post(
            f"/v1/aulas/{aula.id}/presencas",
            json={
                "guerreiro_id": str(guerreiro.id),
                "modo": "confirmacao",
                "momento_do_fato": MOMENTO_DO_FATO.isoformat(),
            },
            headers=cabecalhos_do_mestre,
        )

    token_do_responsavel, _ = criar_sessao_de_teste(responsavel_1)
    resposta = cliente.get(
        f"/v1/eu/guerreiros/{guerreiro_1.id}/acessos",
        headers={
            "X-Chave-Aplicacao": chave,
            "Authorization": f"Bearer {token_do_responsavel}",
        },
    )
    assert resposta.status_code == 200
    corpo = resposta.json()
    assert len(corpo["itens"]) == 1


def test_403_sem_vinculo_vigente(cliente, criar_chave, criar_persona, criar_sessao_de_teste):
    chave, _ = criar_chave()
    responsavel = criar_persona(Papel.responsavel)
    guerreiro = criar_persona(Papel.guerreiro)
    token, _ = criar_sessao_de_teste(responsavel)

    resposta = cliente.get(
        f"/v1/eu/guerreiros/{guerreiro.id}/acessos",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 403


def test_responsavel_nao_alcanca_a_trilha_inteira(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    responsavel = criar_persona(Papel.responsavel)
    token, _ = criar_sessao_de_teste(responsavel)

    resposta = cliente.get(
        "/v1/auditoria", headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}
    )
    assert resposta.status_code == 403
