import uuid
from datetime import UTC, date, datetime
from decimal import Decimal

import pytest

from nucleo.aportes.modelo import FormaDeAporte
from nucleo.consentimentos.modelo import DecisaoDeConsentimento, TipoDeConsentimento
from nucleo.desafios_extras.modelo import (
    ConclusaoDeDesafioExtra,
    Modalidade,
    SituacaoDoDesafioExtra,
)
from nucleo.livro_razao.modelo import NaturezaDoLancamento
from nucleo.ocorrencias_de_conduta.modelo import OcorrenciaDeConduta
from nucleo.personas.modelo import ArtefatoComprobatorio, Papel
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
    assert itens == [
        {
            "avatar": "avatar-x",
            "nick": nick,
            "badges": [],
            "poderes": [],
            "pontos_regulares": 0,
            "posicao_no_ranking": 1,
            "criacoes": [],
        }
    ]


def _cenario_de_carta(
    criar_persona,
    criar_poder,
    criar_trilha,
    criar_ponto_regular,
    criar_nivel,
    criar_badge,
    criar_criacao_original,
    guerreiro_publico,
    *,
    nick,
):
    """Um Guerreiro(a) com tudo o que a variante do documento 11 §8.2 exige:
    ponto regular, nível, badge e criação original validada."""
    admin = criar_persona(Papel.admin)
    poder = criar_poder(admin)
    trilha = criar_trilha(admin, poder=poder, situacao=SituacaoDaTrilha.publicada)
    guerreiro, nick = guerreiro_publico(nick=nick)
    criar_ponto_regular(guerreiro, trilha, total=40)
    criar_nivel(guerreiro, trilha, valor=3)
    criar_badge(guerreiro, trilha=trilha)
    criar_criacao_original(trilha, admin, guerreiro=guerreiro)
    return nick, trilha, poder


def test_card_traz_a_carta_inteira_do_guerreiro(
    cliente,
    criar_chave,
    criar_persona,
    criar_poder,
    criar_trilha,
    criar_ponto_regular,
    criar_nivel,
    criar_badge,
    criar_criacao_original,
    guerreiro_publico,
):
    """`RF-03-05`: o card traz badges, poderes com nível, desempenho e as
    criações originais — a composição do documento 11 §8.2 inteira."""
    nick, trilha, poder = _cenario_de_carta(
        criar_persona,
        criar_poder,
        criar_trilha,
        criar_ponto_regular,
        criar_nivel,
        criar_badge,
        criar_criacao_original,
        guerreiro_publico,
        nick="guerreira-com-carta",
    )
    chave, _ = criar_chave()
    resposta = cliente.get("/v1/vitrine/guerreiros", headers={"X-Chave-Aplicacao": chave})

    assert resposta.status_code == 200
    (item,) = resposta.json()["itens"]
    assert item["nick"] == nick
    assert item["pontos_regulares"] == 40
    assert item["posicao_no_ranking"] == 1
    assert item["poderes"] == [{"poder": poder.nome, "nivel": 3}]
    assert item["badges"] == [{"familia": "de_nivel", "poder": poder.nome}]
    assert [criacao["trilha"] for criacao in item["criacoes"]] == [trilha.nome]


def test_pagina_por_nick_traz_a_mesma_composicao_do_card(
    cliente,
    criar_chave,
    criar_persona,
    criar_poder,
    criar_trilha,
    criar_ponto_regular,
    criar_nivel,
    criar_badge,
    criar_criacao_original,
    guerreiro_publico,
):
    """`RF-03-03`, `RF-03-05`: o que o card mostra é o que a página mostra —
    uma projeção só, nunca dois contratos para a mesma carta."""
    nick, _, _ = _cenario_de_carta(
        criar_persona,
        criar_poder,
        criar_trilha,
        criar_ponto_regular,
        criar_nivel,
        criar_badge,
        criar_criacao_original,
        guerreiro_publico,
        nick="guerreira-da-pagina",
    )
    chave, _ = criar_chave()
    headers = {"X-Chave-Aplicacao": chave}

    (card,) = cliente.get("/v1/vitrine/guerreiros", headers=headers).json()["itens"]
    pagina = cliente.get(f"/v1/vitrine/guerreiros/{nick}", headers=headers)

    assert pagina.status_code == 200
    assert pagina.json() == card


def test_pagina_de_cards_sai_de_uma_resposta_so(
    cliente,
    criar_chave,
    criar_persona,
    criar_trilha,
    criar_ponto_regular,
    criar_nivel,
    criar_badge,
    criar_criacao_original,
    guerreiro_publico,
):
    """A composição de todos os Guerreiros e Guerreiras da página vem na
    própria listagem: montá-la por nick cairia no freio (`RF-01-65`)."""
    admin = criar_persona(Papel.admin)
    trilha = criar_trilha(admin, situacao=SituacaoDaTrilha.publicada)
    for indice in range(3):
        guerreiro, _ = guerreiro_publico(nick=f"guerreira-da-pagina-{indice}")
        criar_ponto_regular(guerreiro, trilha, total=10 * (indice + 1))
        criar_nivel(guerreiro, trilha, valor=indice + 1)
        criar_badge(guerreiro, trilha=trilha)
        criar_criacao_original(trilha, admin, guerreiro=guerreiro)

    chave, _ = criar_chave()
    resposta = cliente.get("/v1/vitrine/guerreiros", headers={"X-Chave-Aplicacao": chave})

    assert resposta.status_code == 200
    itens = resposta.json()["itens"]
    assert len(itens) == 3
    for item in itens:
        assert item["poderes"] and item["badges"] and item["criacoes"]
        assert item["posicao_no_ranking"] >= 1


def test_carta_publica_nao_traz_nada_de_pessoal(
    cliente,
    criar_chave,
    criar_persona,
    criar_poder,
    criar_trilha,
    criar_ponto_regular,
    criar_nivel,
    criar_badge,
    criar_criacao_original,
    guerreiro_publico,
):
    """`RF-03-06`, `RN-03-04`: nem o card nem a página levam nome civil,
    nascimento, contato, imagem real ou valor em reais."""
    nick, _, _ = _cenario_de_carta(
        criar_persona,
        criar_poder,
        criar_trilha,
        criar_ponto_regular,
        criar_nivel,
        criar_badge,
        criar_criacao_original,
        guerreiro_publico,
        nick="guerreira-sem-dado-pessoal",
    )
    chave, _ = criar_chave()
    headers = {"X-Chave-Aplicacao": chave}
    proibidos = {"nome", "nome_civil", "nascimento", "contato", "email", "imagem", "reais"}

    for corpo in (
        cliente.get("/v1/vitrine/guerreiros", headers=headers).json()["itens"][0],
        cliente.get(f"/v1/vitrine/guerreiros/{nick}", headers=headers).json(),
    ):
        assert proibidos.isdisjoint(corpo.keys())


def test_projecao_minima_do_elenco_dos_jogos_nao_muda(cliente, criar_chave, guerreiro_publico):
    """Invariante 8 do documento 99 §6: a carta é da vitrine; o elenco dos
    jogos segue com a projeção mínima de avatar e nick."""
    _, nick = guerreiro_publico(nick="guerreira-no-elenco", avatar="avatar-y")
    chave, _ = criar_chave()
    resposta = cliente.get("/v1/jogos/elenco", headers={"X-Chave-Aplicacao": chave})
    assert resposta.status_code == 200
    assert resposta.json()["itens"] == [{"avatar": "avatar-y", "nick": nick}]


def test_carta_nao_traz_criacao_de_quem_nao_autorizou(
    cliente,
    criar_chave,
    criar_persona,
    criar_nick,
    criar_vinculo,
    criar_consentimento,
    criar_trilha,
    criar_equipe,
    adicionar_integrante,
    criar_criacao_original,
    guerreiro_publico,
):
    """`RN-03-02`: a criação com creditado sem autorização não entra na
    carta, pelo mesmo portão que a tira do portfólio."""
    admin = criar_persona(Papel.admin)
    trilha = criar_trilha(admin, situacao=SituacaoDaTrilha.publicada)
    responsavel = criar_persona(Papel.responsavel, criada_por=admin)
    autor, nick = guerreiro_publico(nick="autora-com-colega-oculto")
    equipe = criar_equipe(autor, trilha=trilha, homologada=True)

    colega = criar_persona(Papel.guerreiro)
    criar_nick(colega, "colega-nao-autorizado")
    criar_vinculo(responsavel, colega, cadastrado_por=admin)
    criar_consentimento(responsavel, colega, tipo=TIPO, decisao=DecisaoDeConsentimento.nega)
    adicionar_integrante(equipe, colega)

    criar_criacao_original(trilha, admin, equipe=equipe)

    chave, _ = criar_chave()
    resposta = cliente.get(f"/v1/vitrine/guerreiros/{nick}", headers={"X-Chave-Aplicacao": chave})
    assert resposta.status_code == 200
    assert resposta.json()["criacoes"] == []


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
    criar_criacao_original,
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

    criar_criacao_original(trilha, admin, equipe=equipe)

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
    criar_criacao_original,
    guerreiro_publico,
):
    admin = criar_persona(Papel.admin)
    trilha = criar_trilha(admin, situacao=SituacaoDaTrilha.publicada)
    autor, nick = guerreiro_publico(nick="autora-da-obra")
    equipe = criar_equipe(autor, trilha=trilha, homologada=True)

    criar_criacao_original(trilha, admin, equipe=equipe)

    chave, _ = criar_chave()
    resposta = cliente.get("/v1/vitrine/criacoes", headers={"X-Chave-Aplicacao": chave})
    assert resposta.status_code == 200
    itens = resposta.json()["itens"]
    assert len(itens) == 1
    assert itens[0]["autores"] == [{"avatar": "avatar-de-teste", "nick": nick}]


def test_criacao_publica_traz_trilha_e_data_e_nao_traz_titulo(
    cliente,
    criar_chave,
    criar_persona,
    criar_trilha,
    criar_criacao_original,
    guerreiro_publico,
):
    """`RF-03-08`: o portfólio exibe trilha, data e autoria por nick. Título
    não existe no modelo da criação original (decisão do fundador,
    2026-09-28)."""
    admin = criar_persona(Papel.admin)
    trilha = criar_trilha(admin, nome="Trilha do Portfólio", situacao=SituacaoDaTrilha.publicada)
    guerreiro, nick = guerreiro_publico(nick="autora-do-portfolio")
    criacao = criar_criacao_original(trilha, admin, guerreiro=guerreiro)

    chave, _ = criar_chave()
    resposta = cliente.get("/v1/vitrine/criacoes", headers={"X-Chave-Aplicacao": chave})

    assert resposta.status_code == 200
    (item,) = resposta.json()["itens"]
    assert item["trilha"] == "Trilha do Portfólio"
    assert datetime.fromisoformat(item["validada_em"]) == criacao.validado_em
    assert [autor["nick"] for autor in item["autores"]] == [nick]
    assert "titulo" not in item


def test_criacao_individual_aparece_creditando_quem_entregou(
    sessao,
    cliente,
    criar_chave,
    criar_persona,
    criar_trilha,
    criar_criacao_original,
    guerreiro_publico,
):
    """`RF-09-33`: a criação individual, com o Guerreiro(a) autorizado,
    aparece na vitrine creditando quem a entregou."""
    admin = criar_persona(Papel.admin)
    trilha = criar_trilha(admin, situacao=SituacaoDaTrilha.publicada)
    guerreiro, nick = guerreiro_publico(nick="guerreira-solo")

    criar_criacao_original(trilha, admin, guerreiro=guerreiro)

    chave, _ = criar_chave()
    resposta = cliente.get("/v1/vitrine/criacoes", headers={"X-Chave-Aplicacao": chave})
    assert resposta.status_code == 200
    itens = resposta.json()["itens"]
    assert len(itens) == 1
    assert itens[0]["autores"] == [{"avatar": "avatar-de-teste", "nick": nick}]


def test_criacao_individual_sem_autorizacao_nao_aparece(
    sessao,
    cliente,
    criar_chave,
    criar_persona,
    criar_nick,
    criar_vinculo,
    criar_consentimento,
    criar_trilha,
    criar_criacao_original,
):
    """`RN-09-19`: sem autorização vigente do responsável, a criação
    individual não vaza para a rota pública."""
    admin = criar_persona(Papel.admin)
    trilha = criar_trilha(admin, situacao=SituacaoDaTrilha.publicada)
    responsavel = criar_persona(Papel.responsavel, criada_por=admin)
    guerreiro = criar_persona(Papel.guerreiro)
    criar_nick(guerreiro, "guerreiro-sem-autorizacao")
    criar_vinculo(responsavel, guerreiro, cadastrado_por=admin)
    criar_consentimento(responsavel, guerreiro, tipo=TIPO, decisao=DecisaoDeConsentimento.nega)

    criar_criacao_original(trilha, admin, guerreiro=guerreiro)

    chave, _ = criar_chave()
    resposta = cliente.get("/v1/vitrine/criacoes", headers={"X-Chave-Aplicacao": chave})
    assert resposta.status_code == 200
    assert resposta.json()["itens"] == []


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


# ---------------------------------------------------------------------------
# Mestres e Apoiadores em público — fatia 7 do PRD-03.
# ---------------------------------------------------------------------------


def _artefato(sessao, persona, *, endereco, rotulo):
    artefato = ArtefatoComprobatorio(persona_id=persona.id, endereco=endereco, rotulo=rotulo)
    sessao.add(artefato)
    sessao.commit()
    return artefato


def _nomear(sessao, persona, nome):
    persona.nome = nome
    sessao.commit()
    return persona


def _aportar(
    criar_lancamento,
    criar_aporte,
    *,
    admin,
    apoiador,
    tipo,
    ponto_de_apoio,
    moedas,
    forma=FormaDeAporte.material,
):
    """Uma linha em `Aporte` é aporte já creditado: é o portão do
    `RF-03-57`."""
    credito = criar_lancamento(
        admin,
        tipo,
        ponto_de_apoio,
        natureza=NaturezaDoLancamento.credito,
        quantidade=Decimal("1.00"),
        valor_em_moedas=moedas,
    )
    return criar_aporte(
        admin,
        apoiador,
        tipo,
        ponto_de_apoio,
        credito,
        quantidade=Decimal("1.00"),
        valor_em_moedas=moedas,
        forma=forma,
    )


def test_listagem_publica_de_mestres_responde_sem_sessao_com_a_carta_inteira(
    cliente, criar_chave, sessao, criar_persona, criar_nick, criar_poder, criar_trilha
):
    """`RF-03-02`, `RF-03-07`: a carta inteira sai na listagem, sem token."""
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, avatar="avatar-do-mestre")
    criar_nick(mestre, "mestra_ana")
    _artefato(sessao, mestre, endereco="https://exemplo.org/cv", rotulo="Currículo")
    poder = criar_poder(admin)
    criar_trilha(
        mestre,
        poder=poder,
        nome="Robótica de sucata",
        area_do_conhecimento="Tecnologia",
        situacao=SituacaoDaTrilha.publicada,
    )

    chave, _ = criar_chave()
    resposta = cliente.get("/v1/vitrine/mestres", headers={"X-Chave-Aplicacao": chave})

    assert resposta.status_code == 200
    item = next(i for i in resposta.json()["itens"] if i["id"] == str(mestre.id))
    assert item["avatar"] == "avatar-do-mestre"
    assert item["identificacao"] == {"valor": "mestra_ana", "tipo": "nick"}
    assert item["areas_de_habilidade"] == ["Tecnologia"]
    assert item["artefatos"] == [{"endereco": "https://exemplo.org/cv", "rotulo": "Currículo"}]
    assert [t["nome"] for t in item["trilhas_de_autoria"]] == ["Robótica de sucata"]
    assert item["absorcoes"] == 0


def test_areas_do_mestre_vem_das_trilhas_publicadas_sem_repetir(
    cliente, criar_chave, criar_persona, criar_nick, criar_poder, criar_trilha
):
    """As áreas derivam da área do conhecimento das trilhas publicadas de
    autoria, sem repetição, e rascunho não conta (`RF-03-07`)."""
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre)
    criar_nick(mestre, "mestre_bento")
    poder = criar_poder(admin)
    for nome, area, situacao in (
        ("Trilha A", "Tecnologia", SituacaoDaTrilha.publicada),
        ("Trilha B", "Artes", SituacaoDaTrilha.publicada),
        ("Trilha C", "Tecnologia", SituacaoDaTrilha.publicada),
        ("Trilha D", "Química", SituacaoDaTrilha.rascunho),
    ):
        criar_trilha(mestre, poder=poder, nome=nome, area_do_conhecimento=area, situacao=situacao)

    chave, _ = criar_chave()
    resposta = cliente.get(f"/v1/vitrine/mestres/{mestre.id}", headers={"X-Chave-Aplicacao": chave})

    assert resposta.status_code == 200
    assert resposta.json()["areas_de_habilidade"] == ["Artes", "Tecnologia"]


def test_leitura_publica_do_mestre_nao_traz_canal_de_contato(
    cliente, criar_chave, sessao, criar_persona, criar_nick
):
    """`RN-03-01`: e-mail e WhatsApp ficam fora da rota pública."""
    mestre = criar_persona(Papel.mestre)
    criar_nick(mestre, "mestre_caio")
    mestre.email = "caio@exemplo.org"
    mestre.whatsapp = "+5511999999999"
    sessao.commit()

    chave, _ = criar_chave()
    corpo = cliente.get(
        f"/v1/vitrine/mestres/{mestre.id}", headers={"X-Chave-Aplicacao": chave}
    ).text

    assert "caio@exemplo.org" not in corpo
    assert "5511999999999" not in corpo


@pytest.mark.parametrize("papel", [Papel.guerreiro, Papel.responsavel, Papel.admin])
def test_persona_de_outro_papel_recebe_o_mesmo_404_do_inexistente(
    cliente, criar_chave, criar_persona, papel
):
    """A recusa é indistinta: papel errado e identificador inexistente têm a
    mesma resposta (`RN-03-01`)."""
    persona = criar_persona(papel)
    chave, _ = criar_chave()
    cabecalho = {"X-Chave-Aplicacao": chave}

    de_outro_papel = cliente.get(f"/v1/vitrine/mestres/{persona.id}", headers=cabecalho)
    inexistente = cliente.get(f"/v1/vitrine/mestres/{uuid.uuid4()}", headers=cabecalho)

    assert de_outro_papel.status_code == 404
    assert de_outro_papel.json() == inexistente.json()


def test_apoiador_com_aporte_aparece_e_sem_aporte_nao(
    cliente,
    criar_chave,
    criar_persona,
    criar_nick,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_lancamento,
    criar_aporte,
):
    """`RF-03-57`, `RN-03-26`: card de Apoiador só existe com aporte
    homologado, e quem não tem recebe o mesmo 404 do inexistente."""
    admin = criar_persona(Papel.admin)
    com_aporte = criar_persona(Papel.apoiador)
    sem_aporte = criar_persona(Papel.apoiador)
    criar_nick(com_aporte, "apoia_norte")
    criar_nick(sem_aporte, "apoia_sul")
    comunidade = criar_comunidade()
    ponto = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    _aportar(
        criar_lancamento,
        criar_aporte,
        admin=admin,
        apoiador=com_aporte,
        tipo=tipo,
        ponto_de_apoio=ponto,
        moedas=Decimal("12.00"),
    )

    chave, _ = criar_chave()
    cabecalho = {"X-Chave-Aplicacao": chave}
    listagem = cliente.get("/v1/vitrine/apoiadores", headers=cabecalho).json()["itens"]
    ids = {item["id"] for item in listagem}

    assert str(com_aporte.id) in ids
    assert str(sem_aporte.id) not in ids

    recusa = cliente.get(f"/v1/vitrine/apoiadores/{sem_aporte.id}", headers=cabecalho)
    inexistente = cliente.get(f"/v1/vitrine/apoiadores/{uuid.uuid4()}", headers=cabecalho)
    assert recusa.status_code == 404
    assert recusa.json() == inexistente.json()


def test_total_do_apoiador_sai_em_moedas_e_nunca_em_reais(
    cliente,
    criar_chave,
    criar_persona,
    criar_nick,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_lancamento,
    criar_aporte,
):
    """`RF-03-10`, `RN-03-18`: o valor de origem em reais não sai em campo
    algum da rota pública."""
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    criar_nick(apoiador, "apoia_leste")
    comunidade = criar_comunidade()
    ponto = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    credito = criar_lancamento(
        admin,
        tipo,
        ponto,
        natureza=NaturezaDoLancamento.credito,
        quantidade=Decimal("1.00"),
        valor_em_moedas=Decimal("15.00"),
    )
    criar_aporte(
        admin,
        apoiador,
        tipo,
        ponto,
        credito,
        quantidade=Decimal("1.00"),
        valor_em_moedas=Decimal("15.00"),
        valor_de_origem=Decimal("150.00"),
    )

    chave, _ = criar_chave()
    resposta = cliente.get(
        f"/v1/vitrine/apoiadores/{apoiador.id}", headers={"X-Chave-Aplicacao": chave}
    )

    assert Decimal(resposta.json()["total_em_moedas"]) == Decimal("15.00")
    assert "150.00" not in resposta.text
    assert "valor_de_origem" not in resposta.text


@pytest.mark.parametrize(
    ("moedas", "avatar_esperado", "padrao_esperado"),
    [(Decimal("5.00"), None, True), (Decimal("10.00"), "logo-propria", False)],
)
def test_piso_de_dez_moedas_decide_o_avatar_do_apoiador(
    cliente,
    criar_chave,
    criar_persona,
    criar_nick,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_lancamento,
    criar_aporte,
    moedas,
    avatar_esperado,
    padrao_esperado,
):
    """`RF-03-66`: abaixo do piso vale o avatar padrão, e a resposta nem
    carrega o avatar próprio; alcançado o piso, vale o próprio."""
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador, avatar="logo-propria")
    criar_nick(apoiador, "apoia_oeste")
    comunidade = criar_comunidade()
    ponto = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    _aportar(
        criar_lancamento,
        criar_aporte,
        admin=admin,
        apoiador=apoiador,
        tipo=tipo,
        ponto_de_apoio=ponto,
        moedas=moedas,
    )

    chave, _ = criar_chave()
    item = cliente.get(
        f"/v1/vitrine/apoiadores/{apoiador.id}", headers={"X-Chave-Aplicacao": chave}
    ).json()

    assert item["avatar"] == avatar_esperado
    assert item["avatar_padrao"] is padrao_esperado


def test_o_direito_ao_avatar_proprio_nao_regride_com_ressarcimento(
    cliente,
    criar_chave,
    sessao,
    criar_persona,
    criar_nick,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_lancamento,
    criar_aporte,
):
    """O total é o **acumulado em aportes**, não o Poder Sustentador: o
    ajuste que derruba o segundo não mexe no primeiro (`RN-14-11`)."""
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador, avatar="logo-propria")
    criar_nick(apoiador, "apoia_centro")
    comunidade = criar_comunidade()
    ponto = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    _aportar(
        criar_lancamento,
        criar_aporte,
        admin=admin,
        apoiador=apoiador,
        tipo=tipo,
        ponto_de_apoio=ponto,
        moedas=Decimal("10.00"),
    )
    # Um débito de ajuste derruba o Poder Sustentador, e não o acumulado.
    criar_lancamento(
        admin,
        tipo,
        ponto,
        natureza=NaturezaDoLancamento.debito,
        quantidade=Decimal("1.00"),
        valor_em_moedas=Decimal("10.00"),
    )

    chave, _ = criar_chave()
    item = cliente.get(
        f"/v1/vitrine/apoiadores/{apoiador.id}", headers={"X-Chave-Aplicacao": chave}
    ).json()

    assert Decimal(item["total_em_moedas"]) == Decimal("10.00")
    assert item["avatar_padrao"] is False


def test_a_listagem_de_apoiadores_nao_e_podio(
    cliente,
    criar_chave,
    criar_persona,
    criar_nick,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_lancamento,
    criar_aporte,
):
    """`RN-14-38`: nenhuma saída traz posição nem ordenação por valor."""
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    for numero, moedas in enumerate((Decimal("2.00"), Decimal("90.00"))):
        apoiador = criar_persona(Papel.apoiador)
        criar_nick(apoiador, f"apoia_{numero}")
        _aportar(
            criar_lancamento,
            criar_aporte,
            admin=admin,
            apoiador=apoiador,
            tipo=tipo,
            ponto_de_apoio=ponto,
            moedas=moedas,
        )

    chave, _ = criar_chave()
    itens = cliente.get("/v1/vitrine/apoiadores", headers={"X-Chave-Aplicacao": chave}).json()[
        "itens"
    ]

    assert len(itens) == 2
    assert all("posicao" not in item for item in itens)
    # A ordem é a estável do cursor (criação), nunca a do valor.
    totais = [Decimal(item["total_em_moedas"]) for item in itens]
    assert totais != sorted(totais, reverse=True)


def test_adulto_sem_nick_sai_pelo_nome_e_com_nick_sai_pelo_nick(
    cliente, criar_chave, sessao, criar_persona, criar_nick
):
    """`RF-03-79`, `RN-03-36`: o nick é opcional para adulto; não havendo,
    sai o nome, **declarado como nome**."""
    sem_nick = _nomear(sessao, criar_persona(Papel.mestre), "Ana Clara Ribeiro")
    com_nick = criar_persona(Papel.mestre)
    _nomear(sessao, com_nick, "Bento Alves")
    criar_nick(com_nick, "mestre_bento_2")

    chave, _ = criar_chave()
    cabecalho = {"X-Chave-Aplicacao": chave}

    pelo_nome = cliente.get(f"/v1/vitrine/mestres/{sem_nick.id}", headers=cabecalho).json()
    pelo_nick = cliente.get(f"/v1/vitrine/mestres/{com_nick.id}", headers=cabecalho).json()

    assert pelo_nome["identificacao"] == {"valor": "Ana Clara Ribeiro", "tipo": "nome"}
    assert pelo_nick["identificacao"] == {"valor": "mestre_bento_2", "tipo": "nick"}


def test_a_regra_do_nome_nunca_alcanca_guerreiro(cliente, criar_chave, sessao, guerreiro_publico):
    """`RN-03-36`, invariantes 9 e 12: nome civil de criança não vai a
    público, mesmo com a persona nomeada."""
    guerreiro, *_ = guerreiro_publico(nick="heroi_do_bairro")
    _nomear(sessao, guerreiro, "Criança Com Nome Civil")

    chave, _ = criar_chave()
    corpo = cliente.get("/v1/vitrine/guerreiros", headers={"X-Chave-Aplicacao": chave}).text

    assert "heroi_do_bairro" in corpo
    assert "Criança Com Nome Civil" not in corpo


def test_desafio_proposto_sai_com_trilha_periodo_e_contagem_sem_quem_concluiu(
    cliente,
    criar_chave,
    sessao,
    criar_persona,
    criar_nick,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_lancamento,
    criar_aporte,
    criar_poder,
    criar_trilha,
    criar_desafio_extra,
):
    """`RF-03-80`, `RN-03-37`: a efetividade pública é agregada — trilha,
    período e contagem —, e nunca alcança quem concluiu."""
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre)
    apoiador = criar_persona(Papel.apoiador)
    criar_nick(apoiador, "apoia_desafios")
    guerreiro = criar_persona(Papel.guerreiro)
    criar_nick(guerreiro, "quem_concluiu")
    comunidade = criar_comunidade()
    ponto = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    _aportar(
        criar_lancamento,
        criar_aporte,
        admin=admin,
        apoiador=apoiador,
        tipo=tipo,
        ponto_de_apoio=ponto,
        moedas=Decimal("20.00"),
    )
    trilha = criar_trilha(
        mestre,
        poder=criar_poder(admin),
        nome="Trilha da Água",
        situacao=SituacaoDaTrilha.publicada,
    )
    desafio = criar_desafio_extra(
        apoiador,
        trilha,
        tipo,
        ponto,
        vigencia_inicio=date(2026, 3, 1),
        vigencia_fim=date(2026, 4, 30),
        situacao=SituacaoDoDesafioExtra.publicado,
    )
    sessao.add(
        ConclusaoDeDesafioExtra(
            desafio_id=desafio.id,
            guerreiro_id=guerreiro.id,
            pontos_extras_creditados=5,
            momento_do_fato=MOMENTO_DO_FATO,
        )
    )
    sessao.commit()

    chave, _ = criar_chave()
    resposta = cliente.get(
        f"/v1/vitrine/apoiadores/{apoiador.id}", headers={"X-Chave-Aplicacao": chave}
    )

    propostos = resposta.json()["desafios_propostos"]
    assert propostos == [
        {
            "trilha": "Trilha da Água",
            "periodo_inicio": "2026-03-01",
            "periodo_fim": "2026-04-30",
            "concluiram": 1,
            "direcionado": False,
        }
    ]
    assert "quem_concluiu" not in resposta.text


def test_desafio_direcionado_nao_se_abre_em_publico(
    cliente,
    criar_chave,
    criar_persona,
    criar_nick,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_lancamento,
    criar_aporte,
    criar_poder,
    criar_trilha,
    criar_desafio_extra,
):
    """`RN-03-37`: o direcionado sai só como situação, sem alcançar o
    destinatário — nem o nick que a proposta guarda."""
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre)
    apoiador = criar_persona(Papel.apoiador)
    criar_nick(apoiador, "apoia_dirigido")
    comunidade = criar_comunidade()
    ponto = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    _aportar(
        criar_lancamento,
        criar_aporte,
        admin=admin,
        apoiador=apoiador,
        tipo=tipo,
        ponto_de_apoio=ponto,
        moedas=Decimal("20.00"),
    )
    trilha = criar_trilha(mestre, poder=criar_poder(admin), situacao=SituacaoDaTrilha.publicada)
    criar_desafio_extra(
        apoiador,
        trilha,
        tipo,
        ponto,
        modalidade=Modalidade.direcionado,
        nick_do_destinatario="nick_do_alvo",
        justificativa_do_vinculo="Justificativa pedagógica.",
        situacao=SituacaoDoDesafioExtra.publicado,
    )

    chave, _ = criar_chave()
    resposta = cliente.get(
        f"/v1/vitrine/apoiadores/{apoiador.id}", headers={"X-Chave-Aplicacao": chave}
    )

    assert resposta.json()["desafios_propostos"][0]["direcionado"] is True
    assert "nick_do_alvo" not in resposta.text


def test_desafio_ainda_nao_publicado_nao_e_fato_publico(
    cliente,
    criar_chave,
    criar_persona,
    criar_nick,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_lancamento,
    criar_aporte,
    criar_poder,
    criar_trilha,
    criar_desafio_extra,
):
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre)
    apoiador = criar_persona(Papel.apoiador)
    criar_nick(apoiador, "apoia_em_validacao")
    comunidade = criar_comunidade()
    ponto = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    _aportar(
        criar_lancamento,
        criar_aporte,
        admin=admin,
        apoiador=apoiador,
        tipo=tipo,
        ponto_de_apoio=ponto,
        moedas=Decimal("20.00"),
    )
    trilha = criar_trilha(mestre, poder=criar_poder(admin), situacao=SituacaoDaTrilha.publicada)
    criar_desafio_extra(apoiador, trilha, tipo, ponto)

    chave, _ = criar_chave()
    item = cliente.get(
        f"/v1/vitrine/apoiadores/{apoiador.id}", headers={"X-Chave-Aplicacao": chave}
    ).json()

    assert item["desafios_propostos"] == []


def test_poder_traz_os_mestres_responsaveis_e_poder_sem_trilha_sai_com_lista_vazia(
    cliente, criar_chave, criar_persona, criar_nick, criar_poder, criar_trilha
):
    """`RF-03-02`: os Mestres responsáveis do documento 11 §8.2, que a fatia
    2 deixou de fora — os autores das trilhas publicadas, deduplicados."""
    admin = criar_persona(Papel.admin)
    primeiro = criar_persona(Papel.mestre)
    segundo = criar_persona(Papel.mestre)
    criar_nick(primeiro, "mestra_zuleica")
    criar_nick(segundo, "mestre_ariel")
    com_trilhas = criar_poder(admin, nome="Poder com trilhas")
    sem_trilhas = criar_poder(admin, nome="Poder sem trilhas")
    criar_trilha(primeiro, poder=com_trilhas, nome="T1", situacao=SituacaoDaTrilha.publicada)
    # Duas trilhas do mesmo Mestre não o repetem no poder.
    criar_trilha(primeiro, poder=com_trilhas, nome="T2", situacao=SituacaoDaTrilha.publicada)
    criar_trilha(segundo, poder=com_trilhas, nome="T3", situacao=SituacaoDaTrilha.publicada)
    criar_trilha(segundo, poder=com_trilhas, nome="T4", situacao=SituacaoDaTrilha.rascunho)

    chave, _ = criar_chave()
    poderes = cliente.get("/v1/vitrine/poderes", headers={"X-Chave-Aplicacao": chave}).json()
    por_id = {poder["id"]: poder for poder in poderes}

    responsaveis = por_id[str(com_trilhas.id)]["mestres_responsaveis"]
    assert [m["identificacao"]["valor"] for m in responsaveis] == [
        "mestra_zuleica",
        "mestre_ariel",
    ]
    assert {m["id"] for m in responsaveis} == {str(primeiro.id), str(segundo.id)}
    assert por_id[str(sem_trilhas.id)]["mestres_responsaveis"] == []
