"""A porta HTTP da equipe da aula — `RF-04-30`, `RF-04-31`, `RF-04-32`,
`RF-04-33`, `RF-04-34` e `RF-04-59`, do PRD-04 §9."""

from datetime import UTC, datetime, timedelta

from nucleo.equipes.modelo import IntegranteDaEquipe
from nucleo.personas.modelo import Papel


def _cabecalhos(chave, token):
    return {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}


def test_guerreiro_cria_a_equipe_e_entra_como_primeiro_integrante(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_sessao_de_teste,
    criar_nick,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade, avatar="avatar-1")
    criar_nick(guerreiro, "zeferina")
    aula = criar_aula(admin, comunidade)
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.post(
        f"/v1/aulas/{aula.id}/equipes", json={}, headers=_cabecalhos(chave, token)
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["aula_id"] == str(aula.id)
    assert corpo["integrantes"] == [{"avatar": "avatar-1", "nick": "zeferina", "papel": None}]


def test_papel_declarado_e_gravado_e_papel_ausente_e_aceito(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_equipe,
    criar_sessao_de_teste,
    criar_nick,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    criador = criar_persona(Papel.guerreiro, comunidade=comunidade)
    criar_nick(criador, "criadora")
    aula = criar_aula(admin, comunidade)
    equipe = criar_equipe(criador, aula=aula)

    outro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    criar_nick(outro, "outra")
    token, _ = criar_sessao_de_teste(outro)

    com_papel = cliente.post(
        f"/v1/equipes/{equipe.id}/integrantes",
        json={"papel": "quem constrói"},
        headers=_cabecalhos(chave, token),
    )
    assert com_papel.status_code == 201
    integrante_com_papel = next(i for i in com_papel.json()["integrantes"] if i["nick"] == "outra")
    assert integrante_com_papel["papel"] == "quem constrói"

    terceiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    criar_nick(terceiro, "terceira")
    token_terceiro, _ = criar_sessao_de_teste(terceiro)
    sem_papel = cliente.post(
        f"/v1/equipes/{equipe.id}/integrantes", json={}, headers=_cabecalhos(chave, token_terceiro)
    )
    assert sem_papel.status_code == 201
    integrante_sem_papel = next(
        i for i in sem_papel.json()["integrantes"] if i["nick"] == "terceira"
    )
    assert integrante_sem_papel["papel"] is None


def test_guerreiro_sai_da_propria_equipe_pela_rota(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_equipe,
    criar_sessao_de_teste,
    sessao,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    criador = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(admin, comunidade)
    equipe = criar_equipe(criador, aula=aula)
    token, _ = criar_sessao_de_teste(criador)

    resposta = cliente.delete(
        f"/v1/equipes/{equipe.id}/integrantes/eu", headers=_cabecalhos(chave, token)
    )

    assert resposta.status_code == 204
    assert (
        sessao.query(IntegranteDaEquipe)
        .filter_by(equipe_id=equipe.id, persona_id=criador.id)
        .first()
        is None
    )


def test_sexto_integrante_e_recusado_com_422_pela_rota(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_equipe,
    criar_sessao_de_teste,
    sessao,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    criador = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(admin, comunidade)
    equipe = criar_equipe(criador, aula=aula)

    for _ in range(4):
        guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
        token, _ = criar_sessao_de_teste(guerreiro)
        cliente.post(
            f"/v1/equipes/{equipe.id}/integrantes", json={}, headers=_cabecalhos(chave, token)
        )

    sexto = criar_persona(Papel.guerreiro, comunidade=comunidade)
    token_sexto, _ = criar_sessao_de_teste(sexto)
    resposta = cliente.post(
        f"/v1/equipes/{equipe.id}/integrantes", json={}, headers=_cabecalhos(chave, token_sexto)
    )

    assert resposta.status_code == 422
    assert sessao.query(IntegranteDaEquipe).filter_by(equipe_id=equipe.id).count() == 5


def test_pessoa_que_nao_e_guerreiro_e_recusada_com_403_pela_rota(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_equipe,
    criar_sessao_de_teste,
    sessao,
):
    """`RF-01-38` restringe a equipe a um integrante de 17 anos ou mais, mas
    a matriz do PRD-01 §4 só concede `equipe_que_forma_na_aula` ao
    Guerreiro(a) (PRD-04 §9: as quatro rotas são dele, sem entrada nova na
    matriz nesta fatia) — então quem não é Guerreiro(a) é recusado antes de
    a composição ser sequer conferida, sempre com 403, nunca com 422."""
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    criador = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(admin, comunidade)
    equipe = criar_equipe(criador, aula=aula)

    responsavel = criar_persona(Papel.responsavel)
    token, _ = criar_sessao_de_teste(responsavel)
    resposta = cliente.post(
        f"/v1/equipes/{equipe.id}/integrantes", json={}, headers=_cabecalhos(chave, token)
    )

    assert resposta.status_code == 403
    assert resposta.json()["codigo"] == "permissao_negada"
    assert sessao.query(IntegranteDaEquipe).filter_by(equipe_id=equipe.id).count() == 1


def test_equipe_de_aula_encerrada_nao_recebe_integrante_pela_rota(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_equipe,
    criar_sessao_de_teste,
    sessao,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    criador = criar_persona(Papel.guerreiro, comunidade=comunidade)
    agora = datetime.now(UTC)
    aula_encerrada = criar_aula(
        admin, comunidade, inicio_em=agora - timedelta(hours=3), fim_em=agora - timedelta(hours=1)
    )
    equipe = criar_equipe(criador, aula=aula_encerrada)

    outro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    token, _ = criar_sessao_de_teste(outro)

    resposta = cliente.post(
        f"/v1/equipes/{equipe.id}/integrantes", json={}, headers=_cabecalhos(chave, token)
    )

    assert resposta.status_code == 422
    assert sessao.query(IntegranteDaEquipe).filter_by(equipe_id=equipe.id).count() == 1


def test_admin_nao_cria_equipe_pela_rota(
    cliente, criar_chave, criar_persona, criar_comunidade, criar_aula, criar_sessao_de_teste, sessao
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.post(
        f"/v1/aulas/{aula.id}/equipes", json={}, headers=_cabecalhos(chave, token)
    )

    assert resposta.status_code == 403
    assert resposta.json()["codigo"] == "permissao_negada"


def test_mestre_nao_altera_composicao_pela_rota(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_equipe,
    criar_sessao_de_teste,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    criador = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(admin, comunidade)
    equipe = criar_equipe(criador, aula=aula)
    token, _ = criar_sessao_de_teste(mestre)

    entrada = cliente.post(
        f"/v1/equipes/{equipe.id}/integrantes", json={}, headers=_cabecalhos(chave, token)
    )
    saida = cliente.delete(
        f"/v1/equipes/{equipe.id}/integrantes/eu", headers=_cabecalhos(chave, token)
    )

    assert entrada.status_code == 403
    assert saida.status_code == 403


def test_pedido_sem_credencial_de_persona_e_recusado(
    cliente, criar_chave, criar_persona, criar_comunidade, criar_aula
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade)

    resposta = cliente.post(
        f"/v1/aulas/{aula.id}/equipes", json={}, headers={"X-Chave-Aplicacao": chave}
    )

    assert resposta.status_code == 401


def test_equipes_da_aula_trazem_so_avatar_e_nick(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_equipe,
    criar_sessao_de_teste,
    criar_nick,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    criador = criar_persona(Papel.guerreiro, comunidade=comunidade, avatar="avatar-2")
    criar_nick(criador, "guerreira-dois")
    aula = criar_aula(admin, comunidade)
    criar_equipe(criador, aula=aula)
    token, _ = criar_sessao_de_teste(criador)

    resposta = cliente.get(f"/v1/aulas/{aula.id}/equipes", headers=_cabecalhos(chave, token))

    assert resposta.status_code == 200
    corpo = resposta.json()["itens"]
    assert len(corpo) == 1
    integrante = corpo[0]["integrantes"][0]
    assert set(integrante.keys()) == {"avatar", "nick", "papel"}
    assert integrante["avatar"] == "avatar-2"
    assert integrante["nick"] == "guerreira-dois"


def test_equipe_da_trilha_nao_aparece_na_leitura_da_aula(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_trilha,
    criar_equipe,
    criar_sessao_de_teste,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(admin, comunidade)
    trilha = criar_trilha(mestre)
    criar_equipe(guerreiro, trilha=trilha)
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.get(f"/v1/aulas/{aula.id}/equipes", headers=_cabecalhos(chave, token))

    assert resposta.status_code == 200
    assert resposta.json()["itens"] == []


def test_equipe_de_outra_aula_nao_aparece_na_leitura(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_equipe,
    criar_sessao_de_teste,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula_um = criar_aula(admin, comunidade)
    aula_dois = criar_aula(
        admin,
        comunidade,
        inicio_em=datetime(2026, 8, 2, 10, 0, tzinfo=UTC),
        fim_em=datetime(2026, 8, 2, 12, 0, tzinfo=UTC),
    )
    criar_equipe(guerreiro, aula=aula_um)
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.get(f"/v1/aulas/{aula_dois.id}/equipes", headers=_cabecalhos(chave, token))

    assert resposta.status_code == 200
    assert resposta.json()["itens"] == []


def test_aula_sem_equipe_devolve_conjunto_vazio_com_200(
    cliente, criar_chave, criar_persona, criar_comunidade, criar_aula, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(admin, comunidade)
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.get(f"/v1/aulas/{aula.id}/equipes", headers=_cabecalhos(chave, token))

    assert resposta.status_code == 200
    assert resposta.json()["itens"] == []


def test_as_quatro_rotas_de_equipe_estao_no_openapi_sob_v1(cliente):
    schema = cliente.get("/openapi.json").json()

    assert "/v1/aulas/{id_da_aula}/equipes" in schema["paths"]
    assert "get" in schema["paths"]["/v1/aulas/{id_da_aula}/equipes"]
    assert "post" in schema["paths"]["/v1/aulas/{id_da_aula}/equipes"]
    assert "/v1/equipes/{id_da_equipe}/integrantes" in schema["paths"]
    assert "/v1/equipes/{id_da_equipe}/integrantes/eu" in schema["paths"]
