from types import SimpleNamespace

import pytest

from nucleo.personas.modelo import Papel
from nucleo.quiz.regra import NATUREZA_DE_COMPETICAO_AO_VIVO

ALTERNATIVAS = ["Salvador", "Recife", "Cachoeira", "Ilhéus"]
CORRETA = 3


def test_openapi_lista_as_duas_rotas_do_banco(cliente):
    esquema = cliente.get("/openapi.json").json()
    assert "/v1/perguntas" in esquema["paths"]
    assert "post" in esquema["paths"]["/v1/perguntas"]
    assert "/v1/perguntas/minhas" in esquema["paths"]
    assert "get" in esquema["paths"]["/v1/perguntas/minhas"]


def test_cadastro_e_leitura_do_banco_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha, criar_missao
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    token, _ = criar_sessao_de_teste(mestre)
    cabecalhos = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}

    resposta_cadastro = cliente.post(
        "/v1/perguntas",
        json={
            "enunciado": "Qual é a primeira capital do Brasil?",
            "alternativas": ALTERNATIVAS,
            "alternativa_correta": 3,
            "missao_id": str(missao.id),
        },
        headers=cabecalhos,
    )

    assert resposta_cadastro.status_code == 201
    corpo = resposta_cadastro.json()
    assert corpo["missao_id"] == str(missao.id)
    assert corpo["trilha_id"] == str(trilha.id)

    resposta_leitura = cliente.get("/v1/perguntas/minhas", headers=cabecalhos)

    assert resposta_leitura.status_code == 200
    pagina = resposta_leitura.json()
    assert [item["id"] for item in pagina["itens"]] == [corpo["id"]]


def test_guerreiro_recebe_403_ao_ler_o_banco(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_comunidade
):
    chave, _ = criar_chave()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=criar_comunidade())
    token, _ = criar_sessao_de_teste(guerreiro)
    cabecalhos = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}

    resposta = cliente.get("/v1/perguntas/minhas", headers=cabecalhos)

    assert resposta.status_code == 403


def _cabecalhos(chave: str, token: str) -> dict:
    return {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}


@pytest.fixture
def cenario_de_partida(
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_aula,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_equipe,
):
    """Aula, trilha com atividade de competição ao vivo e duas equipes
    disputantes, cada uma com um único integrante — o suficiente para o
    percurso completo pelas rotas da partida (`RF-02-59` a `RF-02-62`,
    `RF-02-72`, `RF-02-73`)."""

    def _montar():
        chave, _ = criar_chave()
        admin = criar_persona(Papel.admin)
        mestre = criar_persona(Papel.mestre)
        comunidade = criar_comunidade()
        aula = criar_aula(admin, comunidade)
        trilha = criar_trilha(mestre)
        missao = criar_missao(trilha, mestre)
        atividade = criar_atividade(missao, mestre, natureza=NATUREZA_DE_COMPETICAO_AO_VIVO)

        guerreiro_a = criar_persona(Papel.guerreiro, comunidade=comunidade)
        equipe_a = criar_equipe(guerreiro_a, aula=aula)
        guerreiro_b = criar_persona(Papel.guerreiro, comunidade=comunidade)
        equipe_b = criar_equipe(guerreiro_b, aula=aula)

        token_mestre, _ = criar_sessao_de_teste(mestre)
        token_guerreiro_a, _ = criar_sessao_de_teste(guerreiro_a)
        token_guerreiro_b, _ = criar_sessao_de_teste(guerreiro_b)

        return SimpleNamespace(
            chave=chave,
            mestre=mestre,
            aula=aula,
            missao=missao,
            atividade=atividade,
            equipe_a=equipe_a,
            equipe_b=equipe_b,
            cabecalhos_mestre=_cabecalhos(chave, token_mestre),
            cabecalhos_guerreiro_a=_cabecalhos(chave, token_guerreiro_a),
            cabecalhos_guerreiro_b=_cabecalhos(chave, token_guerreiro_b),
        )

    return _montar


def _abrir_partida(cliente, cen) -> dict:
    resposta = cliente.post(
        "/v1/partidas-de-quiz",
        json={
            "aula_id": str(cen.aula.id),
            "atividade_id": str(cen.atividade.id),
            "equipes": [str(cen.equipe_a.id), str(cen.equipe_b.id)],
        },
        headers=cen.cabecalhos_mestre,
    )
    assert resposta.status_code == 201
    return resposta.json()


def _cadastrar_pergunta(cliente, cen) -> dict:
    resposta = cliente.post(
        "/v1/perguntas",
        json={
            "enunciado": "Qual é a primeira capital do Brasil?",
            "alternativas": ALTERNATIVAS,
            "alternativa_correta": CORRETA,
            "missao_id": str(cen.missao.id),
        },
        headers=cen.cabecalhos_mestre,
    )
    assert resposta.status_code == 201
    return resposta.json()


def test_openapi_lista_as_rotas_da_partida(cliente):
    esquema = cliente.get("/openapi.json").json()
    rotas_esperadas = {
        ("post", "/v1/partidas-de-quiz"),
        ("post", "/v1/partidas-de-quiz/{id_da_partida}/perguntas"),
        ("post", "/v1/partidas-de-quiz/{id_da_partida}/resultado"),
        ("post", "/v1/partidas-de-quiz/{id_da_partida}/anulacoes"),
        ("post", "/v1/partidas-de-quiz/{id_da_partida}/encerramento"),
        ("get", "/v1/partidas-de-quiz/{id_da_partida}"),
        ("get", "/v1/partidas-de-quiz/{id_da_partida}/pergunta"),
        ("post", "/v1/partidas-de-quiz/{id_da_partida}/respostas"),
    }
    for metodo, rota in rotas_esperadas:
        assert metodo in esquema["paths"][rota]


def test_percurso_completo_da_partida_pelas_rotas(cliente, cenario_de_partida):
    cen = cenario_de_partida()
    partida = _abrir_partida(cliente, cen)
    pergunta = _cadastrar_pergunta(cliente, cen)

    resposta_start = cliente.post(
        f"/v1/partidas-de-quiz/{partida['id']}/perguntas",
        json={"pergunta_id": pergunta["id"]},
        headers=cen.cabecalhos_mestre,
    )
    assert resposta_start.status_code == 201
    assert resposta_start.json()["pergunta_no_ar"]["pergunta_id"] == pergunta["id"]

    resposta_a = cliente.post(
        f"/v1/partidas-de-quiz/{partida['id']}/respostas",
        json={
            "pergunta_id": pergunta["id"],
            "equipe_id": str(cen.equipe_a.id),
            "alternativa_escolhida": CORRETA,
        },
        headers=cen.cabecalhos_guerreiro_a,
    )
    assert resposta_a.status_code == 201

    resposta_b = cliente.post(
        f"/v1/partidas-de-quiz/{partida['id']}/respostas",
        json={
            "pergunta_id": pergunta["id"],
            "equipe_id": str(cen.equipe_b.id),
            "alternativa_escolhida": CORRETA,
        },
        headers=cen.cabecalhos_guerreiro_b,
    )
    assert resposta_b.status_code == 201

    estado_antes = cliente.get(
        f"/v1/partidas-de-quiz/{partida['id']}", headers=cen.cabecalhos_mestre
    ).json()
    assert estado_antes["pergunta_no_ar"]["resultado_liberado"] is False
    assert estado_antes["pergunta_no_ar"]["alternativa_correta"] is None
    assert sorted(estado_antes["equipes_que_responderam"]) == sorted(
        [str(cen.equipe_a.id), str(cen.equipe_b.id)]
    )

    resposta_liberacao = cliente.post(
        f"/v1/partidas-de-quiz/{partida['id']}/resultado", headers=cen.cabecalhos_mestre
    )
    assert resposta_liberacao.status_code == 200
    estado_depois = resposta_liberacao.json()
    assert estado_depois["pergunta_no_ar"]["resultado_liberado"] is True
    assert estado_depois["pergunta_no_ar"]["alternativa_correta"] == CORRETA
    assert estado_depois["pergunta_no_ar"]["primeira_equipe_a_acertar"] == str(cen.equipe_a.id)

    outra_pergunta = _cadastrar_pergunta(cliente, cen)
    resposta_anulacao = cliente.post(
        f"/v1/partidas-de-quiz/{partida['id']}/anulacoes",
        json={"pergunta_id": outra_pergunta["id"]},
        headers=cen.cabecalhos_mestre,
    )
    assert resposta_anulacao.status_code == 201
    assert resposta_anulacao.json()["pergunta_id"] == outra_pergunta["id"]

    resposta_encerramento = cliente.post(
        f"/v1/partidas-de-quiz/{partida['id']}/encerramento", headers=cen.cabecalhos_mestre
    )
    assert resposta_encerramento.status_code == 200
    assert resposta_encerramento.json()["situacao"] == "encerrada"


def test_aparelho_da_equipe_volta_na_pergunta_corrente(cliente, cenario_de_partida):
    cen = cenario_de_partida()
    partida = _abrir_partida(cliente, cen)
    primeira = _cadastrar_pergunta(cliente, cen)
    segunda = _cadastrar_pergunta(cliente, cen)

    cliente.post(
        f"/v1/partidas-de-quiz/{partida['id']}/perguntas",
        json={"pergunta_id": primeira["id"]},
        headers=cen.cabecalhos_mestre,
    )
    cliente.post(
        f"/v1/partidas-de-quiz/{partida['id']}/perguntas",
        json={"pergunta_id": segunda["id"]},
        headers=cen.cabecalhos_mestre,
    )

    resposta = cliente.get(
        f"/v1/partidas-de-quiz/{partida['id']}/pergunta", headers=cen.cabecalhos_guerreiro_a
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["id"] == segunda["id"]
    assert "alternativa_correta" not in corpo


def test_mestre_que_nao_conduz_recebe_403_em_toda_escrita_da_partida(
    cliente, cenario_de_partida, criar_persona, criar_sessao_de_teste
):
    cen = cenario_de_partida()
    partida = _abrir_partida(cliente, cen)
    pergunta = _cadastrar_pergunta(cliente, cen)
    outro_mestre = criar_persona(Papel.mestre)
    token_outro, _ = criar_sessao_de_teste(outro_mestre)
    cabecalhos_outro = _cabecalhos(cen.chave, token_outro)

    resposta_start = cliente.post(
        f"/v1/partidas-de-quiz/{partida['id']}/perguntas",
        json={"pergunta_id": pergunta["id"]},
        headers=cabecalhos_outro,
    )
    assert resposta_start.status_code == 403

    resposta_liberacao = cliente.post(
        f"/v1/partidas-de-quiz/{partida['id']}/resultado", headers=cabecalhos_outro
    )
    assert resposta_liberacao.status_code == 403

    resposta_anulacao = cliente.post(
        f"/v1/partidas-de-quiz/{partida['id']}/anulacoes",
        json={"pergunta_id": pergunta["id"]},
        headers=cabecalhos_outro,
    )
    assert resposta_anulacao.status_code == 403

    resposta_encerramento = cliente.post(
        f"/v1/partidas-de-quiz/{partida['id']}/encerramento", headers=cabecalhos_outro
    )
    assert resposta_encerramento.status_code == 403
