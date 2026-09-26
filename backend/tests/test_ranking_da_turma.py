from datetime import UTC, datetime

from nucleo.comunidades.modelo import VinculoJogador
from nucleo.consentimentos.modelo import TipoDeConsentimento
from nucleo.personas.modelo import Papel

TIPO = TipoDeConsentimento.autorizacao_de_divulgacao


def _guerreiro_na_comunidade(
    criar_persona,
    criar_nick,
    criar_vinculo_jogador,
    *,
    comunidade,
    nick,
    total=0,
    trilha=None,
    poder=None,
    criar_ponto_regular=None,
):
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    criar_nick(guerreiro, nick)
    if criar_ponto_regular is not None and total:
        criar_ponto_regular(guerreiro, trilha, total=total, poder=poder)
    return guerreiro


def _autenticar(cliente, criar_chave, criar_sessao_de_teste, persona):
    chave, _ = criar_chave()
    token, _ = criar_sessao_de_teste(persona)
    return {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}


def test_turma_inteira_aparece_mesmo_sem_autorizacao(
    cliente,
    criar_chave,
    criar_sessao_de_teste,
    criar_persona,
    criar_nick,
    criar_vinculo_jogador,
    criar_comunidade,
    criar_trilha,
    criar_ponto_regular,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade("Comunidade da turma")
    trilha = criar_trilha(admin)

    eu = _guerreiro_na_comunidade(
        criar_persona,
        criar_nick,
        criar_vinculo_jogador,
        comunidade=comunidade,
        nick="eu-mesma",
        total=10,
        trilha=trilha,
        criar_ponto_regular=criar_ponto_regular,
    )
    _guerreiro_na_comunidade(
        criar_persona,
        criar_nick,
        criar_vinculo_jogador,
        comunidade=comunidade,
        nick="sem-divulgacao",
        total=20,
        trilha=trilha,
        criar_ponto_regular=criar_ponto_regular,
    )

    cabecalhos = _autenticar(cliente, criar_chave, criar_sessao_de_teste, eu)
    resposta = cliente.get("/v1/eu/ranking", headers=cabecalhos)

    assert resposta.status_code == 200
    nicks = [item["nick"] for item in resposta.json()["itens"]]
    assert "sem-divulgacao" in nicks


def test_propria_posicao_vem_mesmo_fora_da_pagina(
    cliente,
    criar_chave,
    criar_sessao_de_teste,
    criar_persona,
    criar_nick,
    criar_vinculo_jogador,
    criar_comunidade,
    criar_trilha,
    criar_ponto_regular,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade("Comunidade da paginação")
    trilha = criar_trilha(admin)

    ultimo = _guerreiro_na_comunidade(
        criar_persona,
        criar_nick,
        criar_vinculo_jogador,
        comunidade=comunidade,
        nick="ultima-posicao",
        total=1,
        trilha=trilha,
        criar_ponto_regular=criar_ponto_regular,
    )
    for indice in range(3):
        _guerreiro_na_comunidade(
            criar_persona,
            criar_nick,
            criar_vinculo_jogador,
            comunidade=comunidade,
            nick=f"na-frente-{indice}",
            total=100 - indice,
            trilha=trilha,
            criar_ponto_regular=criar_ponto_regular,
        )

    cabecalhos = _autenticar(cliente, criar_chave, criar_sessao_de_teste, ultimo)
    resposta = cliente.get("/v1/eu/ranking", params={"tamanho": 2}, headers=cabecalhos)

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert "ultima-posicao" not in [item["nick"] for item in corpo["itens"]]
    assert corpo["minha_posicao"]["nick"] == "ultima-posicao"
    assert corpo["minha_posicao"]["posicao"] == 4


def test_ordena_so_por_ponto_regular(
    cliente,
    criar_chave,
    criar_sessao_de_teste,
    criar_persona,
    criar_nick,
    criar_vinculo_jogador,
    criar_comunidade,
    criar_trilha,
    criar_ponto_regular,
    criar_ponto_extra,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade("Comunidade do ponto extra")
    trilha = criar_trilha(admin)

    muito_extra_pouco_regular = _guerreiro_na_comunidade(
        criar_persona,
        criar_nick,
        criar_vinculo_jogador,
        comunidade=comunidade,
        nick="muito-extra",
        total=5,
        trilha=trilha,
        criar_ponto_regular=criar_ponto_regular,
    )
    criar_ponto_extra(muito_extra_pouco_regular, acumulado=999, saldo_disponivel=999)

    _guerreiro_na_comunidade(
        criar_persona,
        criar_nick,
        criar_vinculo_jogador,
        comunidade=comunidade,
        nick="so-regular",
        total=50,
        trilha=trilha,
        criar_ponto_regular=criar_ponto_regular,
    )

    cabecalhos = _autenticar(cliente, criar_chave, criar_sessao_de_teste, muito_extra_pouco_regular)
    resposta = cliente.get("/v1/eu/ranking", headers=cabecalhos)

    assert resposta.status_code == 200
    itens = resposta.json()["itens"]
    assert itens[0]["nick"] == "so-regular"
    assert itens[1]["nick"] == "muito-extra"
    assert all("pontos_extras" not in item for item in itens)


def test_filtra_por_trilha_e_por_poder(
    cliente,
    criar_chave,
    criar_sessao_de_teste,
    criar_persona,
    criar_nick,
    criar_vinculo_jogador,
    criar_comunidade,
    criar_trilha,
    criar_poder,
    criar_ponto_regular,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade("Comunidade do recorte")
    trilha_a = criar_trilha(admin)
    trilha_b = criar_trilha(admin)
    poder = criar_poder(admin)

    eu = _guerreiro_na_comunidade(
        criar_persona, criar_nick, criar_vinculo_jogador, comunidade=comunidade, nick="eu-recorte"
    )
    criar_ponto_regular(eu, trilha_a, total=5)
    criar_ponto_regular(eu, poder=poder, total=50)

    colega = _guerreiro_na_comunidade(
        criar_persona,
        criar_nick,
        criar_vinculo_jogador,
        comunidade=comunidade,
        nick="colega-recorte",
    )
    criar_ponto_regular(colega, trilha_b, total=100)

    cabecalhos = _autenticar(cliente, criar_chave, criar_sessao_de_teste, eu)

    por_trilha = cliente.get(
        "/v1/eu/ranking", params={"trilha": str(trilha_a.id)}, headers=cabecalhos
    )
    assert por_trilha.status_code == 200
    assert por_trilha.json()["itens"][0]["nick"] == "eu-recorte"
    assert por_trilha.json()["itens"][0]["pontos_regulares"] == 5

    por_poder = cliente.get("/v1/eu/ranking", params={"poder": str(poder.id)}, headers=cabecalhos)
    assert por_poder.status_code == 200
    assert por_poder.json()["itens"][0]["nick"] == "eu-recorte"
    assert por_poder.json()["itens"][0]["pontos_regulares"] == 50


def test_papel_que_nao_e_guerreiro_recebe_403(
    cliente, criar_chave, criar_sessao_de_teste, criar_persona
):
    mestre = criar_persona(Papel.mestre)

    cabecalhos = _autenticar(cliente, criar_chave, criar_sessao_de_teste, mestre)
    resposta = cliente.get("/v1/eu/ranking", headers=cabecalhos)

    assert resposta.status_code == 403


def test_ranking_nao_alcanca_comunidade_alheia(
    cliente,
    criar_chave,
    criar_sessao_de_teste,
    criar_persona,
    criar_nick,
    criar_vinculo_jogador,
    criar_comunidade,
):
    comunidade_do_guerreiro = criar_comunidade("Minha comunidade")
    outra_comunidade = criar_comunidade("Outra comunidade")
    guerreiro = _guerreiro_na_comunidade(
        criar_persona,
        criar_nick,
        criar_vinculo_jogador,
        comunidade=comunidade_do_guerreiro,
        nick="guerreiro-de-outra",
    )
    _guerreiro_na_comunidade(
        criar_persona,
        criar_nick,
        criar_vinculo_jogador,
        comunidade=outra_comunidade,
        nick="colega-de-fora",
    )

    cabecalhos = _autenticar(cliente, criar_chave, criar_sessao_de_teste, guerreiro)
    resposta = cliente.get("/v1/eu/ranking", headers=cabecalhos)

    # Não há como pedir comunidade alheia: a rota devolve a do vínculo
    # vigente, e nenhuma posição de fora dela chega a quem perguntou.
    assert resposta.status_code == 200
    nicks = [item["nick"] for item in resposta.json()["itens"]]
    assert nicks == ["guerreiro-de-outra"]


def test_saida_sem_dado_pessoal(
    cliente,
    criar_chave,
    criar_sessao_de_teste,
    criar_persona,
    criar_nick,
    criar_vinculo_jogador,
    criar_comunidade,
    criar_trilha,
    criar_ponto_regular,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade("Comunidade sem dado pessoal")
    trilha = criar_trilha(admin)
    eu = _guerreiro_na_comunidade(
        criar_persona,
        criar_nick,
        criar_vinculo_jogador,
        comunidade=comunidade,
        nick="sem-dado-pessoal",
        total=10,
        trilha=trilha,
        criar_ponto_regular=criar_ponto_regular,
    )

    cabecalhos = _autenticar(cliente, criar_chave, criar_sessao_de_teste, eu)
    resposta = cliente.get("/v1/eu/ranking", headers=cabecalhos)

    assert resposta.status_code == 200
    item = resposta.json()["itens"][0]
    assert set(item.keys()) == {"avatar", "nick", "posicao", "pontos_regulares"}


def test_comunidade_vem_do_vinculo_sem_serie_de_coleta(
    cliente,
    criar_chave,
    criar_sessao_de_teste,
    criar_persona,
    criar_nick,
    criar_vinculo_jogador,
    criar_comunidade,
):
    """O que prendia a carta e o ranking à coleta era a comunidade vir de
    fora: quem nunca abriu série de coleta não tinha de onde tirá-la
    (`RF-05-52`, decisão do fundador de 2026-09-26)."""
    comunidade = criar_comunidade("Comunidade sem coleta alguma")
    eu = _guerreiro_na_comunidade(
        criar_persona,
        criar_nick,
        criar_vinculo_jogador,
        comunidade=comunidade,
        nick="sem-coleta",
    )

    cabecalhos = _autenticar(cliente, criar_chave, criar_sessao_de_teste, eu)
    resposta = cliente.get("/v1/eu/ranking", headers=cabecalhos)

    assert resposta.status_code == 200
    assert resposta.json()["minha_posicao"]["nick"] == "sem-coleta"


def test_propria_posicao_existe_sem_ponto_creditado(
    cliente,
    criar_chave,
    criar_sessao_de_teste,
    criar_persona,
    criar_nick,
    criar_vinculo_jogador,
    criar_comunidade,
):
    comunidade = criar_comunidade("Comunidade de quem acabou de chegar")
    eu = _guerreiro_na_comunidade(
        criar_persona,
        criar_nick,
        criar_vinculo_jogador,
        comunidade=comunidade,
        nick="acabei-de-chegar",
    )

    cabecalhos = _autenticar(cliente, criar_chave, criar_sessao_de_teste, eu)
    resposta = cliente.get("/v1/eu/ranking", headers=cabecalhos)

    assert resposta.status_code == 200
    minha_posicao = resposta.json()["minha_posicao"]
    assert minha_posicao["pontos_regulares"] == 0
    assert minha_posicao["posicao"] >= 1


def test_sem_vinculo_vigente_nao_ha_ranking(
    cliente,
    sessao,
    criar_chave,
    criar_sessao_de_teste,
    criar_persona,
    criar_nick,
    criar_vinculo_jogador,
    criar_comunidade,
):
    comunidade = criar_comunidade("Comunidade de quem saiu")
    eu = _guerreiro_na_comunidade(
        criar_persona,
        criar_nick,
        criar_vinculo_jogador,
        comunidade=comunidade,
        nick="vinculo-encerrado",
    )
    vinculo = sessao.query(VinculoJogador).filter_by(guerreiro_id=eu.id, data_fim=None).one()
    vinculo.data_fim = datetime.now(UTC)
    sessao.commit()

    cabecalhos = _autenticar(cliente, criar_chave, criar_sessao_de_teste, eu)
    resposta = cliente.get("/v1/eu/ranking", headers=cabecalhos)

    # Recusa, não ranking vazio: sem vínculo não há turma a apresentar.
    assert resposta.status_code == 403
