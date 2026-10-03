import pytest

from nucleo.auditoria.modelo import Auditoria
from nucleo.personas.modelo import Papel


def _cabecalhos(chave, token=None):
    cabecalhos = {"X-Chave-Aplicacao": chave}
    if token:
        cabecalhos["Authorization"] = f"Bearer {token}"
    return cabecalhos


def test_leitura_publica_devolve_as_tres_secoes_sem_token(cliente, criar_chave):
    chave, _ = criar_chave()

    resposta = cliente.get("/v1/vitrine/conteudo-institucional", headers=_cabecalhos(chave))

    assert resposta.status_code == 200
    assert [item["secao"] for item in resposta.json()] == [
        "quem-somos",
        "contatos",
        "como-apoiar",
    ]


def test_leitura_publica_recusa_sem_chave(cliente):
    resposta = cliente.get("/v1/vitrine/conteudo-institucional")

    assert resposta.status_code == 401


def test_saida_publica_nao_revela_o_autor(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    cliente.put(
        "/v1/conteudo-institucional/contatos",
        json={"texto": "Fale conosco"},
        headers=_cabecalhos(chave, token),
    )

    resposta = cliente.get("/v1/vitrine/conteudo-institucional", headers=_cabecalhos(chave))

    contatos = resposta.json()[1]
    assert contatos["texto"] == "Fale conosco"
    assert set(contatos) == {"secao", "texto", "video_url"}
    assert str(admin.id) not in resposta.text


def test_nao_ha_rota_de_escrita_sob_vitrine(cliente, criar_chave):
    chave, _ = criar_chave()

    for metodo in (cliente.put, cliente.post, cliente.delete):
        resposta = metodo("/v1/vitrine/conteudo-institucional", headers=_cabecalhos(chave))
        assert resposta.status_code in (404, 405)


def test_admin_publica_e_a_leitura_seguinte_ja_devolve(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.put(
        "/v1/conteudo-institucional/quem-somos",
        json={"texto": "Somos a comunidade.", "video_url": "https://videos.exemplo.org/a"},
        headers=_cabecalhos(chave, token),
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["autor_id"] == str(admin.id)
    assert corpo["publicado_em"] is not None
    publica = cliente.get("/v1/vitrine/conteudo-institucional", headers=_cabecalhos(chave))
    assert publica.json()[0]["video_url"] == "https://videos.exemplo.org/a"


@pytest.mark.parametrize(
    "papel", [Papel.mestre, Papel.apoiador, Papel.responsavel, Papel.guerreiro]
)
def test_outras_personas_sao_recusadas(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, papel
):
    chave, _ = criar_chave()
    persona = criar_persona(papel)
    token, _ = criar_sessao_de_teste(persona)

    resposta = cliente.put(
        "/v1/conteudo-institucional/contatos",
        json={"texto": "Invasão"},
        headers=_cabecalhos(chave, token),
    )

    assert resposta.status_code == 403
    publica = cliente.get("/v1/vitrine/conteudo-institucional", headers=_cabecalhos(chave))
    assert publica.json()[1]["texto"] is None


def test_secao_inexistente_e_texto_ausente_sao_recusados(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    cabecalhos = _cabecalhos(chave, token)

    inexistente = cliente.put(
        "/v1/conteudo-institucional/publicidade", json={"texto": "Compre"}, headers=cabecalhos
    )
    ausente = cliente.put("/v1/conteudo-institucional/contatos", json={}, headers=cabecalhos)
    em_outra_secao = cliente.put(
        "/v1/conteudo-institucional/contatos",
        json={"texto": "Olá", "video_url": "https://videos.exemplo.org/a"},
        headers=cabecalhos,
    )

    assert inexistente.status_code == 422
    assert ausente.status_code == 422
    assert em_outra_secao.status_code == 422
    assert em_outra_secao.json()["campo"] == "video_url"


def test_publicacao_entra_na_trilha_de_auditoria(
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
    chave, _ = criar_chave(aplicacao="app-03-gestao")
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.put(
        "/v1/conteudo-institucional/como-apoiar",
        json={"texto": "PIX"},
        headers=_cabecalhos(chave, token),
    )

    assert resposta.status_code == 200
    registro = sessao.query(Auditoria).one()
    assert registro.autor_id == admin.id
    assert registro.acao == "PUT publicar_secao_rota"


def test_admin_le_as_tres_secoes_com_a_autoria(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    cabecalhos = _cabecalhos(chave, token)
    for secao, texto in (
        ("quem-somos", "Somos a comunidade."),
        ("contatos", "Fale conosco"),
        ("como-apoiar", "PIX"),
    ):
        cliente.put(
            f"/v1/conteudo-institucional/{secao}", json={"texto": texto}, headers=cabecalhos
        )

    resposta = cliente.get("/v1/conteudo-institucional", headers=cabecalhos)

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert [item["secao"] for item in corpo] == ["quem-somos", "contatos", "como-apoiar"]
    for item in corpo:
        assert item["autor_id"] == str(admin.id)
        assert item["publicado_em"] is not None
    assert corpo[0]["texto"] == "Somos a comunidade."


def test_secao_nunca_publicada_vem_vazia_para_o_admin(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    cabecalhos = _cabecalhos(chave, token)
    cliente.put(
        "/v1/conteudo-institucional/quem-somos",
        json={"texto": "Somos a comunidade.", "video_url": "https://videos.exemplo.org/a"},
        headers=cabecalhos,
    )

    corpo = cliente.get("/v1/conteudo-institucional", headers=cabecalhos).json()

    quem_somos, contatos, _como_apoiar = corpo
    assert quem_somos["texto"] == "Somos a comunidade."
    assert quem_somos["video_url"] == "https://videos.exemplo.org/a"
    assert contatos["texto"] is None
    assert contatos["autor_id"] is None
    assert contatos["publicado_em"] is None


@pytest.mark.parametrize(
    "papel", [Papel.mestre, Papel.apoiador, Papel.responsavel, Papel.guerreiro]
)
def test_quem_nao_e_admin_nao_le_a_autoria(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, papel
):
    chave, _ = criar_chave()
    persona = criar_persona(papel)
    token, _ = criar_sessao_de_teste(persona)

    resposta = cliente.get("/v1/conteudo-institucional", headers=_cabecalhos(chave, token))

    assert resposta.status_code == 403


def test_leitura_de_admin_nao_tem_rota_de_escrita_nem_dispensa_sessao(cliente, criar_chave):
    chave, _ = criar_chave()

    sem_sessao = cliente.get("/v1/conteudo-institucional", headers=_cabecalhos(chave))

    assert sem_sessao.status_code == 401


def test_leitura_publica_continua_sem_autor_depois_da_rota_de_admin(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    cliente.put(
        "/v1/conteudo-institucional/contatos",
        json={"texto": "Fale conosco"},
        headers=_cabecalhos(chave, token),
    )

    publica = cliente.get("/v1/vitrine/conteudo-institucional", headers=_cabecalhos(chave))

    for item in publica.json():
        assert set(item) == {"secao", "texto", "video_url"}
    assert str(admin.id) not in publica.text
