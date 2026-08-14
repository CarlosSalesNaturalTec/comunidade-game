from nucleo.consentimentos.modelo import DecisaoDeConsentimento, TipoDeConsentimento
from nucleo.personas.modelo import Papel

TIPO = TipoDeConsentimento.autorizacao_de_divulgacao


def test_elenco_traz_so_quem_autorizou(
    cliente,
    criar_chave,
    guerreiro_publico,
    criar_persona,
    criar_nick,
    criar_vinculo,
    criar_consentimento,
):
    _, nick_autorizado = guerreiro_publico(nick="elenco-autorizado")

    admin = criar_persona(Papel.admin)
    responsavel = criar_persona(Papel.responsavel, criada_por=admin)
    sem_autorizacao = criar_persona(Papel.guerreiro)
    criar_nick(sem_autorizacao, "elenco-sem-autorizacao")
    criar_vinculo(responsavel, sem_autorizacao, cadastrado_por=admin)
    criar_consentimento(
        responsavel, sem_autorizacao, tipo=TIPO, decisao=DecisaoDeConsentimento.nega
    )

    chave, _ = criar_chave()
    resposta = cliente.get("/v1/jogos/elenco", headers={"X-Chave-Aplicacao": chave})
    assert resposta.status_code == 200
    nicks = [item["nick"] for item in resposta.json()["itens"]]
    assert nicks == [nick_autorizado]


def test_jogo_le_o_progresso_do_personagem(
    cliente,
    criar_chave,
    guerreiro_publico,
    sessao,
    criar_trilha,
    criar_persona,
    criar_ponto_regular,
    criar_ponto_extra,
    criar_nivel,
    criar_badge,
):
    guerreiro, nick = guerreiro_publico(nick="personagem-de-teste", avatar="avatar-heroi")
    admin = criar_persona(Papel.admin)
    trilha = criar_trilha(admin)
    criar_ponto_regular(guerreiro, trilha, total=42)
    criar_ponto_extra(guerreiro, acumulado=15, saldo_disponivel=5)
    criar_nivel(guerreiro, trilha, valor=1)
    criar_badge(guerreiro, trilha=trilha)

    chave, _ = criar_chave()
    resposta = cliente.get(f"/v1/jogos/personagens/{nick}", headers={"X-Chave-Aplicacao": chave})
    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["avatar"] == "avatar-heroi"
    assert corpo["nick"] == nick
    assert corpo["pontos_regulares"] == 42
    assert corpo["pontos_extra_acumulado"] == 15
    assert corpo["niveis"] == [{"trilha_id": str(trilha.id), "valor": 1}]
    assert len(corpo["badges"]) == 1


def test_progresso_de_quem_nao_autorizou_nao_e_alcancavel(
    cliente, criar_chave, criar_persona, criar_nick, criar_vinculo, criar_consentimento
):
    admin = criar_persona(Papel.admin)
    responsavel = criar_persona(Papel.responsavel, criada_por=admin)
    guerreiro = criar_persona(Papel.guerreiro)
    criar_nick(guerreiro, "jogo-sem-autorizacao")
    criar_vinculo(responsavel, guerreiro, cadastrado_por=admin)
    criar_consentimento(responsavel, guerreiro, tipo=TIPO, decisao=DecisaoDeConsentimento.nega)

    chave, _ = criar_chave()
    headers = {"X-Chave-Aplicacao": chave}
    resposta_existente_sem_autorizacao = cliente.get(
        "/v1/jogos/personagens/jogo-sem-autorizacao", headers=headers
    )
    resposta_inexistente = cliente.get("/v1/jogos/personagens/nao-existe", headers=headers)

    assert resposta_existente_sem_autorizacao.status_code == 404
    assert resposta_inexistente.status_code == 404
    assert resposta_existente_sem_autorizacao.json() == resposta_inexistente.json()


def test_trocar_ponto_extra_nao_enfraquece_o_personagem_lido_pelo_jogo(
    cliente, criar_chave, guerreiro_publico, criar_ponto_extra, sessao
):
    guerreiro, nick = guerreiro_publico(nick="personagem-trocou")
    conta = criar_ponto_extra(guerreiro, acumulado=20, saldo_disponivel=20)

    chave, _ = criar_chave()
    headers = {"X-Chave-Aplicacao": chave}
    antes = cliente.get(f"/v1/jogos/personagens/{nick}", headers=headers).json()

    # Simula a troca: o saldo disponível cai, o acumulado nunca muda
    # (`RN-01-39`, `RN-01-40`) — a leitura do jogo não pode refletir a queda.
    conta.saldo_disponivel = 5
    sessao.commit()

    depois = cliente.get(f"/v1/jogos/personagens/{nick}", headers=headers).json()

    assert antes["pontos_extra_acumulado"] == depois["pontos_extra_acumulado"] == 20


def test_nenhuma_rota_de_jogo_e_de_escrita(cliente, criar_chave):
    """Teste de ausência (`RF-01-22`, `RN-01-06`): toda rota sob o prefixo
    dos jogos é `GET`, e não há caminho de jogo que credite ponto."""
    schema = cliente.get("/openapi.json").json()
    rotas_de_jogo = {
        caminho: metodos for caminho, metodos in schema["paths"].items() if "/jogos" in caminho
    }
    assert rotas_de_jogo
    for caminho, metodos in rotas_de_jogo.items():
        assert set(metodos.keys()) <= {"get", "head"}, caminho

    chave, _ = criar_chave()
    resposta = cliente.post(
        "/v1/jogos/personagens/qualquer/pontos", headers={"X-Chave-Aplicacao": chave}
    )
    assert resposta.status_code == 404


def test_nenhuma_resposta_de_jogo_traz_o_saldo_disponivel(
    cliente, criar_chave, guerreiro_publico, criar_ponto_extra
):
    """Teste de ausência (`RF-01-59`, `RN-01-41`): nem no elenco, nem no
    personagem, o saldo disponível aparece em campo algum."""
    guerreiro, nick = guerreiro_publico(nick="personagem-com-extra")
    criar_ponto_extra(guerreiro, acumulado=30, saldo_disponivel=7)

    chave, _ = criar_chave()
    headers = {"X-Chave-Aplicacao": chave}

    elenco = cliente.get("/v1/jogos/elenco", headers=headers)
    personagem = cliente.get(f"/v1/jogos/personagens/{nick}", headers=headers)

    assert "saldo" not in str(elenco.json()).lower()
    assert "saldo" not in str(personagem.json()).lower()

    schema = cliente.get("/openapi.json").json()
    texto_do_schema = str(schema).lower()
    assert "saldo_disponivel" not in texto_do_schema
