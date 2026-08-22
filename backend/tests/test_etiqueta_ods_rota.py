"""A porta HTTP da etiqueta ODS da trilha e da missão — `RF-09-92`,
`RF-09-98` e `RF-09-94`, do PRD-09 §6.1."""

from nucleo.ods.modelo import EtiquetaOds
from nucleo.personas.modelo import Papel
from nucleo.trilhas.modelo import SituacaoDaTrilha


def _cabecalhos(chave, token):
    return {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}


def test_mestre_autor_substitui_as_etiquetas_da_trilha_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    token, _ = criar_sessao_de_teste(mestre)

    primeira = cliente.post(
        f"/v1/trilhas/{trilha.id}/ods",
        json={"etiquetas": [{"objetivo": 11}, {"objetivo": 4, "meta": "4.7"}]},
        headers=_cabecalhos(chave, token),
    )
    assert primeira.status_code == 200
    assert sorted(item["objetivo"] for item in primeira.json()) == [4, 11]

    segunda = cliente.post(
        f"/v1/trilhas/{trilha.id}/ods",
        json={"etiquetas": [{"objetivo": 4}, {"objetivo": 13}]},
        headers=_cabecalhos(chave, token),
    )

    assert segunda.status_code == 200
    corpo = segunda.json()
    assert sorted(item["objetivo"] for item in corpo) == [4, 13]
    assert all(item["trilha_id"] == str(trilha.id) for item in corpo)
    assert all(item["missao_id"] is None for item in corpo)


def test_mestre_autor_substitui_as_etiquetas_da_missao_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha, criar_missao
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.post(
        f"/v1/missoes/{missao.id}/ods",
        json={"etiquetas": [{"objetivo": 13, "meta": "13.3"}]},
        headers=_cabecalhos(chave, token),
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert [item["objetivo"] for item in corpo] == [13]
    assert corpo[0]["meta"] == "13.3"
    assert corpo[0]["missao_id"] == str(missao.id)
    assert corpo[0]["trilha_id"] is None


def test_lista_vazia_deixa_a_trilha_sem_etiqueta_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    token, _ = criar_sessao_de_teste(mestre)
    cliente.post(
        f"/v1/trilhas/{trilha.id}/ods",
        json={"etiquetas": [{"objetivo": 4}]},
        headers=_cabecalhos(chave, token),
    )

    resposta = cliente.post(
        f"/v1/trilhas/{trilha.id}/ods",
        json={"etiquetas": []},
        headers=_cabecalhos(chave, token),
    )

    assert resposta.status_code == 200
    assert resposta.json() == []


def test_outro_mestre_e_o_admin_sao_recusados_com_403_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha, criar_missao
):
    chave, _ = criar_chave()
    autor = criar_persona(Papel.mestre)
    outro_mestre = criar_persona(Papel.mestre)
    admin = criar_persona(Papel.admin)
    trilha = criar_trilha(autor)
    missao = criar_missao(trilha, autor)

    for persona in (outro_mestre, admin):
        token, _ = criar_sessao_de_teste(persona)
        na_trilha = cliente.post(
            f"/v1/trilhas/{trilha.id}/ods",
            json={"etiquetas": [{"objetivo": 4}]},
            headers=_cabecalhos(chave, token),
        )
        na_missao = cliente.post(
            f"/v1/missoes/{missao.id}/ods",
            json={"etiquetas": [{"objetivo": 4}]},
            headers=_cabecalhos(chave, token),
        )
        assert na_trilha.status_code == 403
        assert na_trilha.json()["codigo"] == "permissao_negada"
        assert na_missao.status_code == 403


def test_objetivo_fora_da_faixa_e_recusado_com_422_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha, sessao
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    token, _ = criar_sessao_de_teste(mestre)
    cliente.post(
        f"/v1/trilhas/{trilha.id}/ods",
        json={"etiquetas": [{"objetivo": 4}]},
        headers=_cabecalhos(chave, token),
    )

    resposta = cliente.post(
        f"/v1/trilhas/{trilha.id}/ods",
        json={"etiquetas": [{"objetivo": 11}, {"objetivo": 19}]},
        headers=_cabecalhos(chave, token),
    )

    assert resposta.status_code == 422
    corpo = resposta.json()
    assert corpo["codigo"] == "erro_de_validacao"
    assert corpo["campo"] == "objetivo"
    objetivos = [
        objetivo
        for (objetivo,) in sessao.query(EtiquetaOds.objetivo).filter_by(trilha_id=trilha.id)
    ]
    assert objetivos == [4]


def test_as_duas_rotas_de_ods_estao_no_openapi_sob_v1(cliente):
    schema = cliente.get("/openapi.json").json()

    assert "/v1/trilhas/{id_da_trilha}/ods" in schema["paths"]
    assert "/v1/missoes/{id_da_missao}/ods" in schema["paths"]


def test_rota_de_ods_exige_chave_de_aplicacao(
    cliente, criar_persona, criar_sessao_de_teste, criar_trilha
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.post(
        f"/v1/trilhas/{trilha.id}/ods",
        json={"etiquetas": []},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 401


def test_minhas_trilhas_trazem_etiquetas_e_cobertura(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha, criar_missao
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao_etiquetada = criar_missao(trilha, mestre, posicao=1)
    missao_sem_etiqueta = criar_missao(trilha, mestre, posicao=2)
    token, _ = criar_sessao_de_teste(mestre)
    cliente.post(
        f"/v1/trilhas/{trilha.id}/ods",
        json={"etiquetas": [{"objetivo": 4, "meta": "4.7"}]},
        headers=_cabecalhos(chave, token),
    )
    cliente.post(
        f"/v1/missoes/{missao_etiquetada.id}/ods",
        json={"etiquetas": [{"objetivo": 13}]},
        headers=_cabecalhos(chave, token),
    )

    resposta = cliente.get("/v1/trilhas/minhas", headers=_cabecalhos(chave, token))

    assert resposta.status_code == 200
    corpo = next(item for item in resposta.json() if item["id"] == str(trilha.id))
    assert [e["objetivo"] for e in corpo["etiquetas_ods"]] == [4]
    assert corpo["etiquetas_ods"][0]["meta"] == "4.7"
    assert corpo["cobertura_ods"]["objetivos"] == [4, 13]
    assert corpo["cobertura_ods"]["ciclo"] == "Ciclo 01"

    por_id = {missao["id"]: missao for missao in corpo["missoes"]}
    assert [e["objetivo"] for e in por_id[str(missao_etiquetada.id)]["etiquetas_ods"]] == [13]
    assert por_id[str(missao_sem_etiqueta.id)]["etiquetas_ods"] == []


def test_trilha_publica_traz_etiquetas_e_cobertura(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha, criar_missao, sessao
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    token, _ = criar_sessao_de_teste(mestre)
    cliente.post(
        f"/v1/trilhas/{trilha.id}/ods",
        json={"etiquetas": [{"objetivo": 4}]},
        headers=_cabecalhos(chave, token),
    )
    cliente.post(
        f"/v1/missoes/{missao.id}/ods",
        json={"etiquetas": [{"objetivo": 4}, {"objetivo": 13}]},
        headers=_cabecalhos(chave, token),
    )
    trilha.situacao = SituacaoDaTrilha.publicada
    sessao.commit()

    resposta = cliente.get(f"/v1/trilhas/{trilha.id}", headers={"X-Chave-Aplicacao": chave})

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert [e["objetivo"] for e in corpo["etiquetas_ods"]] == [4]
    # Sem repetir o objetivo declarado na trilha e na missão.
    assert corpo["cobertura_ods"]["objetivos"] == [4, 13]
    assert corpo["cobertura_ods"]["ciclo"] == "Ciclo 01"
    assert sorted(e["objetivo"] for e in corpo["missoes"][0]["etiquetas_ods"]) == [4, 13]


def test_trilha_sem_etiqueta_tem_cobertura_vazia(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha, criar_missao
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    criar_missao(trilha, mestre)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.get("/v1/trilhas/minhas", headers=_cabecalhos(chave, token))

    assert resposta.status_code == 200
    corpo = next(item for item in resposta.json() if item["id"] == str(trilha.id))
    assert corpo["etiquetas_ods"] == []
    assert corpo["cobertura_ods"]["objetivos"] == []
    assert corpo["cobertura_ods"]["ciclo"] == "Ciclo 01"
