from nucleo.consentimentos.modelo import DecisaoDeConsentimento, TipoDeConsentimento
from nucleo.criacoes_originais.regra import entregar_criacao_original, validar_criacao_original
from nucleo.personas.modelo import Papel
from nucleo.trilhas.modelo import SituacaoDaTrilha

TIPO = TipoDeConsentimento.autorizacao_de_divulgacao


def _guerreiro_com_decisao(
    criar_persona, criar_nick, criar_vinculo, criar_consentimento, *, nick, decisao, admin=None
):
    admin = admin or criar_persona(Papel.admin)
    responsavel = criar_persona(Papel.responsavel, criada_por=admin)
    guerreiro = criar_persona(Papel.guerreiro)
    criar_nick(guerreiro, nick)
    criar_vinculo(responsavel, guerreiro, cadastrado_por=admin)
    criar_consentimento(responsavel, guerreiro, tipo=TIPO, decisao=decisao)
    return guerreiro, responsavel, admin


def test_vitrine_responde_sem_token_de_sessao(cliente, criar_chave, guerreiro_publico):
    guerreiro_publico()
    chave, _ = criar_chave()
    resposta = cliente.get("/v1/vitrine/guerreiros", headers={"X-Chave-Aplicacao": chave})
    assert resposta.status_code == 200


def test_vitrine_sem_chave_e_recusada(cliente):
    resposta = cliente.get("/v1/vitrine/guerreiros")
    assert resposta.status_code == 401


def test_card_traz_avatar_e_nick_sem_dado_pessoal(cliente, criar_chave, guerreiro_publico):
    _, nick = guerreiro_publico(avatar="avatar-x")
    chave, _ = criar_chave()
    resposta = cliente.get("/v1/vitrine/guerreiros", headers={"X-Chave-Aplicacao": chave})
    assert resposta.status_code == 200
    itens = resposta.json()["itens"]
    assert itens == [{"avatar": "avatar-x", "nick": nick}]


def test_guerreiro_sem_autorizacao_nao_aparece_em_card(
    cliente, criar_chave, criar_persona, criar_nick, criar_vinculo, criar_consentimento
):
    _guerreiro_com_decisao(
        criar_persona,
        criar_nick,
        criar_vinculo,
        criar_consentimento,
        nick="sem-autorizacao",
        decisao=DecisaoDeConsentimento.nega,
    )
    chave, _ = criar_chave()
    resposta = cliente.get("/v1/vitrine/guerreiros", headers={"X-Chave-Aplicacao": chave})
    assert resposta.status_code == 200
    assert resposta.json()["itens"] == []


def test_revogacao_tira_do_publico_na_chamada_seguinte(
    cliente, criar_chave, criar_persona, criar_nick, criar_vinculo, criar_consentimento
):
    guerreiro, responsavel, admin = _guerreiro_com_decisao(
        criar_persona,
        criar_nick,
        criar_vinculo,
        criar_consentimento,
        nick="revogavel",
        decisao=DecisaoDeConsentimento.concede,
    )
    chave, _ = criar_chave()
    headers = {"X-Chave-Aplicacao": chave}

    antes = cliente.get("/v1/vitrine/guerreiros/revogavel", headers=headers)
    assert antes.status_code == 200

    criar_consentimento(responsavel, guerreiro, tipo=TIPO, decisao=DecisaoDeConsentimento.nega)

    depois = cliente.get("/v1/vitrine/guerreiros/revogavel", headers=headers)
    assert depois.status_code == 404


def test_nick_inexistente_e_nick_sem_autorizacao_tem_corpo_identico(
    cliente, criar_chave, criar_persona, criar_nick, criar_vinculo, criar_consentimento
):
    _guerreiro_com_decisao(
        criar_persona,
        criar_nick,
        criar_vinculo,
        criar_consentimento,
        nick="sem-autorizacao-2",
        decisao=DecisaoDeConsentimento.nega,
    )
    chave, _ = criar_chave()
    headers = {"X-Chave-Aplicacao": chave}

    resposta_inexistente = cliente.get("/v1/vitrine/guerreiros/nao-existe", headers=headers)
    resposta_sem_autorizacao = cliente.get(
        "/v1/vitrine/guerreiros/sem-autorizacao-2", headers=headers
    )

    assert resposta_inexistente.status_code == 404
    assert resposta_sem_autorizacao.status_code == 404
    assert resposta_inexistente.json() == resposta_sem_autorizacao.json()


def test_nick_parcial_nao_alcanca_ninguem(cliente, criar_chave, guerreiro_publico):
    _, nick = guerreiro_publico(nick="guerreira-completa")
    chave, _ = criar_chave()
    resposta = cliente.get(
        f"/v1/vitrine/guerreiros/{nick[:5]}", headers={"X-Chave-Aplicacao": chave}
    )
    assert resposta.status_code == 404


def test_ranking_ordena_por_ponto_regular_e_filtra_por_comunidade(
    cliente,
    criar_chave,
    criar_persona,
    criar_nick,
    criar_vinculo,
    criar_consentimento,
    criar_trilha,
    criar_ponto_regular,
):
    admin = criar_persona(Papel.admin)
    trilha = criar_trilha(admin)

    primeiro, *_ = _guerreiro_com_decisao(
        criar_persona,
        criar_nick,
        criar_vinculo,
        criar_consentimento,
        nick="primeiro-lugar",
        decisao=DecisaoDeConsentimento.concede,
        admin=admin,
    )
    criar_ponto_regular(primeiro, trilha, total=100)

    sem_autorizacao, *_ = _guerreiro_com_decisao(
        criar_persona,
        criar_nick,
        criar_vinculo,
        criar_consentimento,
        nick="sem-autorizacao-3",
        decisao=DecisaoDeConsentimento.nega,
        admin=admin,
    )
    criar_ponto_regular(sem_autorizacao, trilha, total=90)

    terceiro, *_ = _guerreiro_com_decisao(
        criar_persona,
        criar_nick,
        criar_vinculo,
        criar_consentimento,
        nick="terceiro-visivel",
        decisao=DecisaoDeConsentimento.concede,
        admin=admin,
    )
    criar_ponto_regular(terceiro, trilha, total=80)

    chave, _ = criar_chave()
    resposta = cliente.get("/v1/vitrine/rankings", headers={"X-Chave-Aplicacao": chave})
    assert resposta.status_code == 200
    itens = resposta.json()["itens"]

    assert [item["nick"] for item in itens] == ["primeiro-lugar", "terceiro-visivel"]
    assert [item["posicao"] for item in itens] == [1, 2]


def test_poderes_publicos_trazem_trilhas_publicadas(
    cliente, criar_chave, criar_persona, criar_trilha, criar_poder
):
    admin = criar_persona(Papel.admin)
    poder = criar_poder(admin)
    criar_trilha(admin, poder=poder, situacao=SituacaoDaTrilha.publicada)
    criar_trilha(admin, poder=poder, situacao=SituacaoDaTrilha.rascunho)

    chave, _ = criar_chave()
    resposta = cliente.get("/v1/vitrine/poderes", headers={"X-Chave-Aplicacao": chave})
    assert resposta.status_code == 200
    saida = resposta.json()
    poder_saida = next(p for p in saida if p["id"] == str(poder.id))
    assert len(poder_saida["trilhas"]) == 1


def test_criacao_com_integrante_sem_autorizacao_nao_aparece(
    sessao,
    cliente,
    criar_chave,
    criar_persona,
    criar_nick,
    criar_vinculo,
    criar_consentimento,
    criar_trilha,
    criar_equipe,
    adicionar_integrante,
):
    admin = criar_persona(Papel.admin)
    trilha = criar_trilha(admin, situacao=SituacaoDaTrilha.publicada)
    responsavel = criar_persona(Papel.responsavel, criada_por=admin)

    autor, *_ = _guerreiro_com_decisao(
        criar_persona,
        criar_nick,
        criar_vinculo,
        criar_consentimento,
        nick="autor-autorizado",
        decisao=DecisaoDeConsentimento.concede,
        admin=admin,
    )
    equipe = criar_equipe(autor, trilha=trilha, homologada=True)

    colega = criar_persona(Papel.guerreiro)
    criar_nick(colega, "colega-sem-autorizacao")
    criar_vinculo(responsavel, colega, cadastrado_por=admin)
    criar_consentimento(responsavel, colega, tipo=TIPO, decisao=DecisaoDeConsentimento.nega)
    adicionar_integrante(equipe, colega)

    criacao = entregar_criacao_original(
        sessao, guerreiro=autor, equipe=equipe, producao="Produção de teste."
    )
    validar_criacao_original(sessao, operador=admin, criacao=criacao)
    sessao.commit()

    chave, _ = criar_chave()
    resposta = cliente.get("/v1/vitrine/criacoes", headers={"X-Chave-Aplicacao": chave})
    assert resposta.status_code == 200
    assert resposta.json()["itens"] == []


def test_criacao_com_todos_autorizados_aparece_com_autoria_creditada(
    sessao,
    cliente,
    criar_chave,
    criar_persona,
    criar_trilha,
    criar_equipe,
    guerreiro_publico,
):
    admin = criar_persona(Papel.admin)
    trilha = criar_trilha(admin, situacao=SituacaoDaTrilha.publicada)
    autor, nick = guerreiro_publico(nick="autora-da-obra")
    equipe = criar_equipe(autor, trilha=trilha, homologada=True)

    criacao = entregar_criacao_original(
        sessao, guerreiro=autor, equipe=equipe, producao="Produção de teste."
    )
    validar_criacao_original(sessao, operador=admin, criacao=criacao)
    sessao.commit()

    chave, _ = criar_chave()
    resposta = cliente.get("/v1/vitrine/criacoes", headers={"X-Chave-Aplicacao": chave})
    assert resposta.status_code == 200
    itens = resposta.json()["itens"]
    assert len(itens) == 1
    assert itens[0]["autores"] == [{"avatar": "avatar-de-teste", "nick": nick}]


def test_cobertura_de_ods_agrega_por_comunidade_e_ciclo_sem_recorte_de_guerreiro(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_trilha,
    criar_missao,
    criar_atividade,
    sessao,
):
    from datetime import UTC, datetime

    from nucleo.ods.regra import criar_etiqueta_ods
    from nucleo.resultados.regra import registrar_resultado

    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade("Comunidade ODS")
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    trilha = criar_trilha(admin)
    missao = criar_missao(trilha, admin)
    atividade = criar_atividade(missao, admin)
    criar_etiqueta_ods(sessao, operador=admin, objetivo=4, trilha=trilha)
    registrar_resultado(
        sessao,
        operador=admin,
        guerreiro_id=guerreiro.id,
        atividade=atividade,
        momento_do_fato=datetime.now(UTC),
        producao="Produção de teste.",
        desfecho="realizada",
    )
    sessao.commit()

    chave, _ = criar_chave()
    resposta = cliente.get("/v1/vitrine/ods/cobertura", headers={"X-Chave-Aplicacao": chave})
    assert resposta.status_code == 200
    saida = resposta.json()
    linha = next(item for item in saida if item["comunidade_id"] == str(comunidade.id))
    assert linha["objetivos"] == [4]
    assert linha["ciclo"] == "Ciclo 01"

    schema = cliente.get("/openapi.json").json()
    parametros_da_rota = schema["paths"]["/v1/vitrine/ods/cobertura"]["get"].get("parameters", [])
    assert not any(p["name"] == "guerreiro" for p in parametros_da_rota)
