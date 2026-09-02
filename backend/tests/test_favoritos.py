from datetime import UTC, datetime, timedelta

from nucleo.consentimentos.modelo import DecisaoDeConsentimento, TipoDeConsentimento
from nucleo.personas.modelo import Papel
from nucleo.pontuacao.modelo import Badge, TipoDeBadge
from nucleo.trilhas.modelo import SituacaoDaTrilha

TIPO = TipoDeConsentimento.autorizacao_de_divulgacao


def _cabecalhos(chave: str, token: str) -> dict[str, str]:
    return {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}


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


# --- 3.2 — criação e remoção ----------------------------------------------


def test_nick_exato_de_quem_autorizou_vira_favorito(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, guerreiro_publico
):
    _, nick = guerreiro_publico(nick="favorita-por-nick")
    apoiador = criar_persona(Papel.apoiador)
    token, _ = criar_sessao_de_teste(apoiador)
    chave, _ = criar_chave()

    resposta = cliente.post(
        "/v1/eu/favoritos", json={"nick": nick}, headers=_cabecalhos(chave, token)
    )
    assert resposta.status_code == 201
    assert resposta.json()["nick"] == nick

    leitura = cliente.get("/v1/eu/favoritos", headers=_cabecalhos(chave, token))
    assert leitura.status_code == 200
    assert [g["nick"] for g in leitura.json()["guerreiros"]] == [nick]


def test_nick_inexistente_e_sem_autorizacao_tem_corpo_identico(
    cliente,
    criar_chave,
    criar_persona,
    criar_nick,
    criar_vinculo,
    criar_consentimento,
    criar_sessao_de_teste,
):
    _guerreiro_com_decisao(
        criar_persona,
        criar_nick,
        criar_vinculo,
        criar_consentimento,
        nick="sem-autorizacao-favorito",
        decisao=DecisaoDeConsentimento.nega,
    )
    apoiador = criar_persona(Papel.apoiador)
    token, _ = criar_sessao_de_teste(apoiador)
    chave, _ = criar_chave()
    headers = _cabecalhos(chave, token)

    resposta_inexistente = cliente.post(
        "/v1/eu/favoritos", json={"nick": "nao-existe-de-jeito-nenhum"}, headers=headers
    )
    resposta_sem_autorizacao = cliente.post(
        "/v1/eu/favoritos", json={"nick": "sem-autorizacao-favorito"}, headers=headers
    )

    assert resposta_inexistente.status_code == 404
    assert resposta_sem_autorizacao.status_code == 404
    assert resposta_inexistente.json() == resposta_sem_autorizacao.json()


def test_nick_aproximado_nao_alcanca_ninguem(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, guerreiro_publico
):
    _, nick = guerreiro_publico(nick="guerreira-completa-favorito")
    apoiador = criar_persona(Papel.apoiador)
    token, _ = criar_sessao_de_teste(apoiador)
    chave, _ = criar_chave()

    resposta = cliente.post(
        "/v1/eu/favoritos", json={"nick": nick[:5]}, headers=_cabecalhos(chave, token)
    )
    assert resposta.status_code == 404


def test_nenhuma_rota_de_favorito_aceita_fragmento_de_nick(cliente, criar_chave):
    schema = cliente.get("/openapi.json").json()
    rotas_de_favorito = {
        caminho: metodos for caminho, metodos in schema["paths"].items() if "/favoritos" in caminho
    }
    assert rotas_de_favorito
    for caminho, metodos in rotas_de_favorito.items():
        for metodo in metodos.values():
            parametros = metodo.get("parameters", [])
            assert not any("nick" in p["name"] for p in parametros), caminho


def test_mestre_vira_favorito_por_persona(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, sessao
):
    mestre = criar_persona(Papel.mestre, avatar="avatar-do-mestre")
    mestre.nome = "Mestre Favorito"
    sessao.commit()
    apoiador = criar_persona(Papel.apoiador)
    token, _ = criar_sessao_de_teste(apoiador)
    chave, _ = criar_chave()

    resposta = cliente.post(
        "/v1/eu/favoritos",
        json={"mestre_id": str(mestre.id)},
        headers=_cabecalhos(chave, token),
    )
    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["nome"] == "Mestre Favorito"
    assert corpo["avatar"] == "avatar-do-mestre"
    assert "email" not in corpo
    assert "whatsapp" not in corpo


def test_persona_que_nao_e_mestre_e_recusada(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    outro_apoiador = criar_persona(Papel.apoiador)
    apoiador = criar_persona(Papel.apoiador)
    token, _ = criar_sessao_de_teste(apoiador)
    chave, _ = criar_chave()

    resposta = cliente.post(
        "/v1/eu/favoritos",
        json={"mestre_id": str(outro_apoiador.id)},
        headers=_cabecalhos(chave, token),
    )
    assert resposta.status_code == 404


def test_favoritar_duas_vezes_nao_duplica(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, guerreiro_publico
):
    _, nick = guerreiro_publico(nick="favorito-repetido")
    apoiador = criar_persona(Papel.apoiador)
    token, _ = criar_sessao_de_teste(apoiador)
    chave, _ = criar_chave()
    headers = _cabecalhos(chave, token)

    primeira = cliente.post("/v1/eu/favoritos", json={"nick": nick}, headers=headers)
    segunda = cliente.post("/v1/eu/favoritos", json={"nick": nick}, headers=headers)

    assert primeira.status_code == 201
    assert segunda.status_code == 201
    assert primeira.json() == segunda.json()

    leitura = cliente.get("/v1/eu/favoritos", headers=headers)
    assert len(leitura.json()["guerreiros"]) == 1


def test_remocao_some_da_lista(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, guerreiro_publico
):
    _, nick = guerreiro_publico(nick="favorito-removivel")
    apoiador = criar_persona(Papel.apoiador)
    token, _ = criar_sessao_de_teste(apoiador)
    chave, _ = criar_chave()
    headers = _cabecalhos(chave, token)

    criado = cliente.post("/v1/eu/favoritos", json={"nick": nick}, headers=headers)
    favorito_id = criado.json()["id"]

    remocao = cliente.delete(f"/v1/eu/favoritos/{favorito_id}", headers=headers)
    assert remocao.status_code == 204

    leitura = cliente.get("/v1/eu/favoritos", headers=headers)
    assert leitura.json()["guerreiros"] == []


def test_remover_favorito_de_outro_apoiador_e_inexistente_tem_mesmo_404(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, guerreiro_publico
):
    _, nick = guerreiro_publico(nick="favorito-de-outro-apoiador")
    apoiador_a = criar_persona(Papel.apoiador)
    apoiador_b = criar_persona(Papel.apoiador)
    token_a, _ = criar_sessao_de_teste(apoiador_a)
    token_b, _ = criar_sessao_de_teste(apoiador_b)
    chave, _ = criar_chave()

    criado = cliente.post(
        "/v1/eu/favoritos", json={"nick": nick}, headers=_cabecalhos(chave, token_a)
    )
    favorito_id = criado.json()["id"]

    resposta_de_outro = cliente.delete(
        f"/v1/eu/favoritos/{favorito_id}", headers=_cabecalhos(chave, token_b)
    )
    resposta_inexistente = cliente.delete(
        "/v1/eu/favoritos/00000000-0000-0000-0000-000000000000",
        headers=_cabecalhos(chave, token_b),
    )

    assert resposta_de_outro.status_code == 404
    assert resposta_inexistente.status_code == 404
    assert resposta_de_outro.json() == resposta_inexistente.json()


def test_papel_diferente_de_apoiador_e_recusado_nas_tres_rotas(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    mestre = criar_persona(Papel.mestre)
    token, _ = criar_sessao_de_teste(mestre)
    chave, _ = criar_chave()
    headers = _cabecalhos(chave, token)

    assert cliente.get("/v1/eu/favoritos", headers=headers).status_code == 403
    assert (
        cliente.post("/v1/eu/favoritos", json={"nick": "qualquer"}, headers=headers).status_code
        == 403
    )
    assert (
        cliente.delete(
            "/v1/eu/favoritos/00000000-0000-0000-0000-000000000000", headers=headers
        ).status_code
        == 403
    )


# --- 3.3 — leitura com novidades -------------------------------------------


def test_os_quatro_fatos_aparecem_com_data(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    guerreiro_publico,
    criar_trilha,
    criar_criacao_original,
    criar_badge,
    criar_nivel,
    sessao,
):
    admin = criar_persona(Papel.admin)
    guerreiro, nick = guerreiro_publico(nick="favorito-com-novidade")
    trilha = criar_trilha(admin, situacao=SituacaoDaTrilha.publicada)
    criar_criacao_original(trilha, admin, guerreiro=guerreiro)
    criar_badge(guerreiro, trilha=trilha)
    criar_nivel(guerreiro, trilha)

    mestre = criar_persona(Papel.mestre)
    trilha_do_mestre = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    trilha_do_mestre.situacao_alterada_em = datetime.now(UTC)
    sessao.commit()

    apoiador = criar_persona(Papel.apoiador)
    token, _ = criar_sessao_de_teste(apoiador)
    chave, _ = criar_chave()
    headers = _cabecalhos(chave, token)

    cliente.post("/v1/eu/favoritos", json={"nick": nick}, headers=headers)
    cliente.post("/v1/eu/favoritos", json={"mestre_id": str(mestre.id)}, headers=headers)

    leitura = cliente.get("/v1/eu/favoritos", headers=headers)
    assert leitura.status_code == 200
    corpo = leitura.json()

    tipos_do_guerreiro = {n["tipo"] for n in corpo["guerreiros"][0]["novidades"]}
    assert tipos_do_guerreiro == {"criacao_original", "badge", "nivel"}
    for novidade in corpo["guerreiros"][0]["novidades"]:
        assert novidade["data"]

    tipos_do_mestre = {n["tipo"] for n in corpo["mestres"][0]["novidades"]}
    assert tipos_do_mestre == {"trilha"}


def test_fato_com_mais_de_30_dias_sai_do_destaque_sem_apagar_nada(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    guerreiro_publico,
    criar_trilha,
    sessao,
):
    admin = criar_persona(Papel.admin)
    guerreiro, nick = guerreiro_publico(nick="favorito-com-novidade-antiga")
    trilha = criar_trilha(admin, situacao=SituacaoDaTrilha.publicada)

    antigo = datetime.now(UTC) - timedelta(days=31)
    badge = Badge(guerreiro_id=guerreiro.id, trilha_id=trilha.id, tipo=TipoDeBadge.de_nivel)
    badge.certificado_em = antigo
    sessao.add(badge)
    sessao.commit()

    apoiador = criar_persona(Papel.apoiador)
    token, _ = criar_sessao_de_teste(apoiador)
    chave, _ = criar_chave()
    headers = _cabecalhos(chave, token)

    cliente.post("/v1/eu/favoritos", json={"nick": nick}, headers=headers)
    leitura = cliente.get("/v1/eu/favoritos", headers=headers)
    assert leitura.json()["guerreiros"][0]["novidades"] == []

    assert sessao.get(Badge, badge.id) is not None


def test_trilha_de_outro_mestre_nao_entra(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_trilha,
    sessao,
):
    mestre_favoritado = criar_persona(Papel.mestre)
    outro_mestre = criar_persona(Papel.mestre)
    criar_trilha(outro_mestre, situacao=SituacaoDaTrilha.publicada)
    trilha_do_favoritado = criar_trilha(mestre_favoritado, situacao=SituacaoDaTrilha.publicada)
    trilha_do_favoritado.situacao_alterada_em = datetime.now(UTC)
    sessao.commit()

    apoiador = criar_persona(Papel.apoiador)
    token, _ = criar_sessao_de_teste(apoiador)
    chave, _ = criar_chave()
    headers = _cabecalhos(chave, token)

    cliente.post("/v1/eu/favoritos", json={"mestre_id": str(mestre_favoritado.id)}, headers=headers)
    leitura = cliente.get("/v1/eu/favoritos", headers=headers)
    novidades = leitura.json()["mestres"][0]["novidades"]
    assert len(novidades) == 1
    assert novidades[0]["trilha_id"] == str(trilha_do_favoritado.id)


def test_criacao_de_equipe_com_integrante_sem_autorizacao_nao_aparece(
    cliente,
    criar_chave,
    criar_persona,
    criar_nick,
    criar_vinculo,
    criar_consentimento,
    criar_sessao_de_teste,
    guerreiro_publico,
    criar_trilha,
    criar_equipe,
    criar_criacao_original,
    adicionar_integrante,
):
    admin = criar_persona(Papel.admin)
    trilha = criar_trilha(admin, situacao=SituacaoDaTrilha.publicada)
    autor, nick = guerreiro_publico(nick="autora-em-equipe-favorito")
    equipe = criar_equipe(autor, trilha=trilha, homologada=True)

    responsavel = criar_persona(Papel.responsavel, criada_por=admin)
    colega = criar_persona(Papel.guerreiro)
    criar_nick(colega, "colega-sem-autorizacao-favorito")
    criar_vinculo(responsavel, colega, cadastrado_por=admin)
    criar_consentimento(responsavel, colega, tipo=TIPO, decisao=DecisaoDeConsentimento.nega)
    adicionar_integrante(equipe, colega)

    criar_criacao_original(trilha, admin, equipe=equipe)

    apoiador = criar_persona(Papel.apoiador)
    token, _ = criar_sessao_de_teste(apoiador)
    chave, _ = criar_chave()
    headers = _cabecalhos(chave, token)

    cliente.post("/v1/eu/favoritos", json={"nick": nick}, headers=headers)
    leitura = cliente.get("/v1/eu/favoritos", headers=headers)
    assert leitura.json()["guerreiros"][0]["novidades"] == []


def test_revogacao_tira_da_leitura_e_autorizacao_de_volta_traz_de_volta(
    cliente,
    criar_chave,
    criar_persona,
    criar_nick,
    criar_vinculo,
    criar_consentimento,
    criar_sessao_de_teste,
):
    admin = criar_persona(Papel.admin)
    responsavel = criar_persona(Papel.responsavel, criada_por=admin)
    guerreiro = criar_persona(Papel.guerreiro, avatar="avatar-revogavel")
    criar_nick(guerreiro, "favorito-revogavel")
    criar_vinculo(responsavel, guerreiro, cadastrado_por=admin)
    criar_consentimento(responsavel, guerreiro, tipo=TIPO, decisao=DecisaoDeConsentimento.concede)

    apoiador = criar_persona(Papel.apoiador)
    token, _ = criar_sessao_de_teste(apoiador)
    chave, _ = criar_chave()
    headers = _cabecalhos(chave, token)

    cliente.post("/v1/eu/favoritos", json={"nick": "favorito-revogavel"}, headers=headers)

    antes = cliente.get("/v1/eu/favoritos", headers=headers)
    assert len(antes.json()["guerreiros"]) == 1

    criar_consentimento(responsavel, guerreiro, tipo=TIPO, decisao=DecisaoDeConsentimento.nega)

    durante = cliente.get("/v1/eu/favoritos", headers=headers)
    assert durante.json()["guerreiros"] == []
    assert durante.json()["mestres"] == []

    criar_consentimento(responsavel, guerreiro, tipo=TIPO, decisao=DecisaoDeConsentimento.concede)

    depois = cliente.get("/v1/eu/favoritos", headers=headers)
    assert len(depois.json()["guerreiros"]) == 1


def test_saida_de_guerreiro_e_so_avatar_e_nick_e_mestre_sem_contato(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, guerreiro_publico, sessao
):
    _, nick = guerreiro_publico(nick="favorito-so-avatar-e-nick", avatar="avatar-so-publico")
    mestre = criar_persona(Papel.mestre, avatar="avatar-mestre-sem-contato")
    mestre.nome = "Mestre Sem Contato"
    mestre.email = "mestre@example.com"
    mestre.whatsapp = "5599999999999"
    sessao.commit()

    apoiador = criar_persona(Papel.apoiador)
    token, _ = criar_sessao_de_teste(apoiador)
    chave, _ = criar_chave()
    headers = _cabecalhos(chave, token)

    cliente.post("/v1/eu/favoritos", json={"nick": nick}, headers=headers)
    cliente.post("/v1/eu/favoritos", json={"mestre_id": str(mestre.id)}, headers=headers)

    leitura = cliente.get("/v1/eu/favoritos", headers=headers)
    corpo = leitura.json()

    assert set(corpo["guerreiros"][0].keys()) == {"id", "avatar", "nick", "novidades"}
    assert corpo["guerreiros"][0]["avatar"] == "avatar-so-publico"
    assert set(corpo["mestres"][0].keys()) == {"id", "avatar", "nome", "novidades"}
