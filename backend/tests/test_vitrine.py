from datetime import UTC, datetime

from nucleo.consentimentos.modelo import DecisaoDeConsentimento, TipoDeConsentimento
from nucleo.criacoes_originais.regra import entregar_criacao_original, validar_criacao_original
from nucleo.ocorrencias_de_conduta.modelo import OcorrenciaDeConduta
from nucleo.personas.modelo import Papel
from nucleo.trilhas.modelo import SituacaoDaTrilha

MOMENTO_DO_FATO = datetime(2026, 8, 1, 10, 0, tzinfo=UTC)

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


def test_vitrine_nao_tem_rota_de_escrita(cliente, criar_chave):
    """A vitrine é só leitura (`RF-01-02`): toda rota sob o prefixo é
    `GET`, e não há caminho por onde criar, alterar ou remover registro."""
    schema = cliente.get("/openapi.json").json()
    rotas_da_vitrine = {
        caminho: metodos for caminho, metodos in schema["paths"].items() if "/vitrine" in caminho
    }
    assert rotas_da_vitrine
    for caminho, metodos in rotas_da_vitrine.items():
        assert set(metodos.keys()) <= {"get", "head"}, caminho

    chave, _ = criar_chave()
    resposta = cliente.post("/v1/vitrine/guerreiros", headers={"X-Chave-Aplicacao": chave}, json={})
    assert resposta.status_code == 405


def test_guerreiros_filtra_por_comunidade(
    cliente,
    criar_chave,
    criar_persona,
    criar_nick,
    criar_vinculo,
    criar_consentimento,
    criar_comunidade,
):
    comunidade_a = criar_comunidade("Comunidade A")
    comunidade_b = criar_comunidade("Comunidade B")
    admin = criar_persona(Papel.admin)
    responsavel = criar_persona(Papel.responsavel, criada_por=admin)

    guerreiro_a = criar_persona(Papel.guerreiro, comunidade=comunidade_a)
    criar_nick(guerreiro_a, "guerreiro-comunidade-a")
    criar_vinculo(responsavel, guerreiro_a, cadastrado_por=admin)
    criar_consentimento(responsavel, guerreiro_a, tipo=TIPO, decisao=DecisaoDeConsentimento.concede)

    guerreiro_b = criar_persona(Papel.guerreiro, comunidade=comunidade_b)
    criar_nick(guerreiro_b, "guerreiro-comunidade-b")
    criar_vinculo(responsavel, guerreiro_b, cadastrado_por=admin)
    criar_consentimento(responsavel, guerreiro_b, tipo=TIPO, decisao=DecisaoDeConsentimento.concede)

    chave, _ = criar_chave()
    resposta = cliente.get(
        "/v1/vitrine/guerreiros",
        params={"comunidade": str(comunidade_a.id)},
        headers={"X-Chave-Aplicacao": chave},
    )
    assert resposta.status_code == 200
    nicks = [item["nick"] for item in resposta.json()["itens"]]
    assert nicks == ["guerreiro-comunidade-a"]


def test_ranking_filtra_por_comunidade(
    cliente,
    criar_chave,
    criar_persona,
    criar_nick,
    criar_vinculo,
    criar_consentimento,
    criar_comunidade,
    criar_trilha,
    criar_ponto_regular,
):
    comunidade_a = criar_comunidade("Comunidade Ranking A")
    comunidade_b = criar_comunidade("Comunidade Ranking B")
    admin = criar_persona(Papel.admin)
    trilha = criar_trilha(admin)
    responsavel = criar_persona(Papel.responsavel, criada_por=admin)

    guerreiro_a = criar_persona(Papel.guerreiro, comunidade=comunidade_a)
    criar_nick(guerreiro_a, "ranking-comunidade-a")
    criar_vinculo(responsavel, guerreiro_a, cadastrado_por=admin)
    criar_consentimento(responsavel, guerreiro_a, tipo=TIPO, decisao=DecisaoDeConsentimento.concede)
    criar_ponto_regular(guerreiro_a, trilha, total=10)

    guerreiro_b = criar_persona(Papel.guerreiro, comunidade=comunidade_b)
    criar_nick(guerreiro_b, "ranking-comunidade-b")
    criar_vinculo(responsavel, guerreiro_b, cadastrado_por=admin)
    criar_consentimento(responsavel, guerreiro_b, tipo=TIPO, decisao=DecisaoDeConsentimento.concede)
    criar_ponto_regular(guerreiro_b, trilha, total=20)

    chave, _ = criar_chave()
    resposta = cliente.get(
        "/v1/vitrine/rankings",
        params={"comunidade": str(comunidade_a.id)},
        headers={"X-Chave-Aplicacao": chave},
    )
    assert resposta.status_code == 200
    itens = resposta.json()["itens"]
    assert [item["nick"] for item in itens] == ["ranking-comunidade-a"]
    assert itens[0]["posicao"] == 1


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
    criar_aula,
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
    aula = criar_aula(admin, comunidade)
    criar_etiqueta_ods(sessao, operador=admin, objetivo=4, trilha=trilha)
    registrar_resultado(
        sessao,
        operador=admin,
        aula=aula,
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


def test_cobertura_publica_inclui_comunidade_so_com_coleta(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
    criar_desafio_de_coleta,
    criar_local,
    criar_serie_de_coleta,
    sessao,
):
    """4.11: comunidade sem Resultado registrado e com série aberta sobre
    desafio etiquetado aparece na cobertura pública (`RF-08-26`)."""
    from nucleo.ods.regra import criar_etiqueta_ods

    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade("Comunidade só de coleta")
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    local = criar_local(comunidade)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    criar_etiqueta_ods(sessao, operador=mestre, objetivo=6, missao=missao)
    sessao.commit()
    tipo = criar_tipo_de_coleta(mestre)
    desafio = criar_desafio_de_coleta(missao, mestre, tipo=tipo)
    criar_serie_de_coleta(guerreiro, desafio, local)

    chave, _ = criar_chave()
    resposta = cliente.get("/v1/vitrine/ods/cobertura", headers={"X-Chave-Aplicacao": chave})
    assert resposta.status_code == 200
    linha = next(item for item in resposta.json() if item["comunidade_id"] == str(comunidade.id))
    assert linha["objetivos"] == [6]


def _ocorrencia_de_conduta(
    sessao, *, guerreiro, aula, atividade, autor, valor=5, valor_debitado=5, encerrada_em=None
):
    ocorrencia = OcorrenciaDeConduta(
        guerreiro_id=guerreiro.id,
        aula_id=aula.id,
        atividade_id=atividade.id,
        valor=valor,
        valor_debitado=valor_debitado,
        motivo=None if encerrada_em is not None else "Desrespeitou um colega.",
        momento_do_fato=MOMENTO_DO_FATO,
        autor_id=autor.id,
        papel_do_autor=autor.papel.value,
        encerrada_em=encerrada_em,
    )
    sessao.add(ocorrencia)
    sessao.commit()
    return ocorrencia


def test_ocorrencia_de_ciclo_encerrado_nao_pesa_no_ranking(
    cliente,
    criar_chave,
    criar_persona,
    criar_nick,
    criar_vinculo,
    criar_consentimento,
    criar_comunidade,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_aula,
    criar_ponto_regular,
    sessao,
):
    """A ocorrência de ciclo encerrado devolve o que foi debitado de fato,
    não o nominal, e sai do ranking (`RF-02-100`, documento 11 §5)."""
    comunidade = criar_comunidade("Comunidade do ranking do ciclo")
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre)
    responsavel = criar_persona(Papel.responsavel, criada_por=admin)
    trilha = criar_trilha(admin)
    missao = criar_missao(trilha, admin)
    atividade = criar_atividade(missao, admin)
    aula = criar_aula(mestre, comunidade)

    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    criar_nick(guerreiro, "encerrada-no-ranking")
    criar_vinculo(responsavel, guerreiro, cadastrado_por=admin)
    criar_consentimento(
        responsavel,
        guerreiro,
        tipo=TipoDeConsentimento.autorizacao_de_divulgacao,
        decisao=DecisaoDeConsentimento.concede,
    )
    criar_ponto_regular(guerreiro, trilha, total=15)
    _ocorrencia_de_conduta(
        sessao,
        guerreiro=guerreiro,
        aula=aula,
        atividade=atividade,
        autor=mestre,
        encerrada_em=MOMENTO_DO_FATO,
    )

    chave, _ = criar_chave()
    resposta = cliente.get(
        "/v1/vitrine/rankings",
        params={"comunidade": str(comunidade.id)},
        headers={"X-Chave-Aplicacao": chave},
    )
    assert resposta.status_code == 200
    itens = resposta.json()["itens"]
    assert itens[0]["nick"] == "encerrada-no-ranking"
    assert itens[0]["pontos_regulares"] == 20  # 15 do saldo + 5 devolvidos pelo expurgo


def test_ocorrencia_do_ciclo_corrente_segue_pesando_no_ranking(
    cliente,
    criar_chave,
    criar_persona,
    criar_nick,
    criar_vinculo,
    criar_consentimento,
    criar_comunidade,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_aula,
    criar_ponto_regular,
    sessao,
):
    comunidade = criar_comunidade("Comunidade do ciclo corrente")
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre)
    responsavel = criar_persona(Papel.responsavel, criada_por=admin)
    trilha = criar_trilha(admin)
    missao = criar_missao(trilha, admin)
    atividade = criar_atividade(missao, admin)
    aula = criar_aula(mestre, comunidade)

    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    criar_nick(guerreiro, "ciclo-corrente-no-ranking")
    criar_vinculo(responsavel, guerreiro, cadastrado_por=admin)
    criar_consentimento(
        responsavel,
        guerreiro,
        tipo=TipoDeConsentimento.autorizacao_de_divulgacao,
        decisao=DecisaoDeConsentimento.concede,
    )
    criar_ponto_regular(guerreiro, trilha, total=15)
    _ocorrencia_de_conduta(
        sessao, guerreiro=guerreiro, aula=aula, atividade=atividade, autor=mestre
    )

    chave, _ = criar_chave()
    resposta = cliente.get(
        "/v1/vitrine/rankings",
        params={"comunidade": str(comunidade.id)},
        headers={"X-Chave-Aplicacao": chave},
    )
    assert resposta.status_code == 200
    itens = resposta.json()["itens"]
    assert itens[0]["nick"] == "ciclo-corrente-no-ranking"
    assert itens[0]["pontos_regulares"] == 15  # sem devolução: o ciclo não foi encerrado
