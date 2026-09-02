from datetime import timedelta
from decimal import Decimal

from nucleo.aulas.modelo import SituacaoDaAula
from nucleo.personas.modelo import Papel
from nucleo.tempo import agora


def _tornar_pendente(sessao, aula):
    aula.situacao = SituacaoDaAula.pendente_de_lastro
    sessao.commit()


def _corpo_da_publicacao(aula, tipo, **mudancas):
    corpo = {
        "aula_id": str(aula.id),
        "tipo_de_recurso_id": str(tipo.id),
        "nivel_de_necessidade": "acontecer",
        "titulo": "O lanche do encontro",
        "o_que_se_pede": "Um lanche para vinte crianças",
        "quantidade": "100.00",
        "prazo": str(agora().date() + timedelta(days=30)),
        "selo_nome": "Lanche garantido",
        "selo_familia": "frente",
    }
    corpo.update(mudancas)
    return corpo


def test_admin_publica_missao_pela_rota(
    cliente,
    sessao,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_aula,
    criar_recurso_declarado_da_aula,
    criar_sessao_de_teste,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    aula = criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)
    criar_recurso_declarado_da_aula(aula, tipo, quantidade=Decimal("2.00"))
    _tornar_pendente(sessao, aula)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.post(
        "/v1/missoes-do-apoiador",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
        json=_corpo_da_publicacao(aula, tipo),
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["situacao"] == "aberta"
    assert corpo["falta"] == "100.00"


def test_apoiador_nao_publica_missao_pela_rota(
    cliente,
    sessao,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_aula,
    criar_recurso_declarado_da_aula,
    criar_sessao_de_teste,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    aula = criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)
    criar_recurso_declarado_da_aula(aula, tipo, quantidade=Decimal("2.00"))
    _tornar_pendente(sessao, aula)
    token, _ = criar_sessao_de_teste(apoiador)

    resposta = cliente.post(
        "/v1/missoes-do-apoiador",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
        json=_corpo_da_publicacao(aula, tipo),
    )

    assert resposta.status_code == 403


def test_leitura_publica_sem_sessao_agrupa_por_nivel(
    cliente,
    sessao,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_aula,
    criar_recurso_declarado_da_aula,
    criar_sessao_de_teste,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    aula = criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)
    criar_recurso_declarado_da_aula(aula, tipo, quantidade=Decimal("2.00"))
    _tornar_pendente(sessao, aula)
    token, _ = criar_sessao_de_teste(admin)
    cliente.post(
        "/v1/missoes-do-apoiador",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
        json=_corpo_da_publicacao(aula, tipo),
    )

    resposta = cliente.get("/v1/missoes-do-apoiador", headers={"X-Chave-Aplicacao": chave})

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert set(corpo.keys()) == {"existir", "acontecer", "reconhecer", "permanecer"}
    assert len(corpo["acontecer"]) == 1
    assert "situacao" not in corpo["acontecer"][0]


def test_leitura_do_admin_traz_qualquer_situacao(
    cliente,
    sessao,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_aula,
    criar_recurso_declarado_da_aula,
    criar_sessao_de_teste,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    aula = criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)
    criar_recurso_declarado_da_aula(aula, tipo, quantidade=Decimal("2.00"))
    _tornar_pendente(sessao, aula)
    token, _ = criar_sessao_de_teste(admin)
    publicada = cliente.post(
        "/v1/missoes-do-apoiador",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
        json=_corpo_da_publicacao(aula, tipo),
    ).json()

    resposta = cliente.get(
        "/v1/missoes-do-apoiador",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert isinstance(corpo, list)
    missao = next(item for item in corpo if item["id"] == publicada["id"])
    assert missao["situacao"] == "aberta"
    assert missao["coberto"] == "0.00"


def test_admin_despublica_missao_sem_estornar(
    cliente,
    sessao,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_aula,
    criar_recurso_declarado_da_aula,
    criar_sessao_de_teste,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    aula = criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)
    criar_recurso_declarado_da_aula(aula, tipo, quantidade=Decimal("2.00"))
    _tornar_pendente(sessao, aula)
    token, _ = criar_sessao_de_teste(admin)
    publicada = cliente.post(
        "/v1/missoes-do-apoiador",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
        json=_corpo_da_publicacao(aula, tipo),
    ).json()

    resposta = cliente.post(
        f"/v1/missoes-do-apoiador/{publicada['id']}/despublicacao",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 200
    assert resposta.json()["situacao"] == "despublicada"


def test_apoiador_le_o_proprio_sustento(
    cliente, sessao, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    apoiador = criar_persona(Papel.apoiador)
    token, _ = criar_sessao_de_teste(apoiador)

    resposta = cliente.get(
        "/v1/eu/apoiador/sustento",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["nivel"] == 0
    assert set(corpo["selos"].keys()) == {"frente", "modalidade", "ato", "multiplicacao"}


def test_rotas_de_missao_exigem_chave_de_aplicacao(cliente):
    resposta = cliente.get("/v1/missoes-do-apoiador")

    assert resposta.status_code == 401
