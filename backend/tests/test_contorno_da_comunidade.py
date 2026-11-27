"""Fatia 1 do PRD-08 — o Admin cadastra e substitui o contorno da comunidade
(`RF-08-33`, `RN-08-32`, change `2026-11-27-contorno-da-comunidade`)."""

import uuid

import pytest

from nucleo.comunidades.modelo import ComunidadeVirtual
from nucleo.personas.modelo import Papel

CONTORNO = {
    "type": "Polygon",
    "coordinates": [
        [
            [-38.4801, -12.8632],
            [-38.4788, -12.8632],
            [-38.4788, -12.8605],
            [-38.4801, -12.8605],
            [-38.4801, -12.8632],
        ]
    ],
}


def _gravar(cliente, chave, token, comunidade_id, corpo):
    return cliente.put(
        f"/v1/comunidades/{comunidade_id}/contorno",
        json=corpo,
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )


@pytest.fixture
def admin_em_sessao(criar_chave, criar_persona, criar_sessao_de_teste):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    return chave, token


def test_admin_cadastra_o_contorno_copiado_do_osm(
    cliente, sessao, admin_em_sessao, criar_comunidade
):
    chave, token = admin_em_sessao
    comunidade = criar_comunidade()

    resposta = _gravar(
        cliente,
        chave,
        token,
        comunidade.id,
        {"geometria": CONTORNO, "origem_osm": "relation/12582832"},
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["geometria"] == CONTORNO
    assert corpo["origem_osm"] == "relation/12582832"
    assert corpo["copiado_em"]
    sessao.expire_all()
    gravada = sessao.get(ComunidadeVirtual, comunidade.id)
    assert gravada.contorno == CONTORNO
    assert gravada.contorno_origem_osm == "relation/12582832"
    assert gravada.contorno_copiado_em.tzinfo is not None


def test_cadastrar_de_novo_substitui_o_contorno(cliente, sessao, admin_em_sessao, criar_comunidade):
    chave, token = admin_em_sessao
    comunidade = criar_comunidade()
    _gravar(cliente, chave, token, comunidade.id, {"geometria": CONTORNO, "origem_osm": "way/1"})
    segundo = {"type": "MultiPolygon", "coordinates": [CONTORNO["coordinates"]]}

    resposta = _gravar(
        cliente, chave, token, comunidade.id, {"geometria": segundo, "origem_osm": "relation/2"}
    )

    assert resposta.status_code == 200
    sessao.expire_all()
    gravada = sessao.get(ComunidadeVirtual, comunidade.id)
    assert gravada.contorno == segundo
    assert gravada.contorno_origem_osm == "relation/2"


@pytest.mark.parametrize(
    "geometria",
    [
        {"type": "Point", "coordinates": [-38.48, -12.86]},
        {"type": "Feature", "geometry": CONTORNO},
        {"type": "Polygon", "coordinates": [CONTORNO["coordinates"][0][:-1]]},
        {
            "type": "Polygon",
            "coordinates": [[[-38.48, -12.86], [-38.47, -12.86], [-38.48, -12.86]]],
        },
        {
            "type": "Polygon",
            "coordinates": [
                [[-238.0, -12.86], [-38.47, -12.86], [-38.47, -12.85], [-238.0, -12.86]]
            ],
        },
        {"type": "Polygon", "coordinates": [[["a", "b"], [1, 2], [3, 4], ["a", "b"]]]},
        {"type": "MultiPolygon", "coordinates": []},
    ],
    ids=["ponto", "feature", "anel-aberto", "anel-curto", "fora-da-faixa", "texto", "multi-vazio"],
)
def test_geometria_invalida_e_recusada_e_o_contorno_anterior_permanece(
    cliente, sessao, admin_em_sessao, criar_comunidade, geometria
):
    chave, token = admin_em_sessao
    comunidade = criar_comunidade()
    _gravar(cliente, chave, token, comunidade.id, {"geometria": CONTORNO, "origem_osm": "way/1"})

    resposta = _gravar(
        cliente, chave, token, comunidade.id, {"geometria": geometria, "origem_osm": "way/9"}
    )

    assert resposta.status_code == 422
    assert resposta.json()["campo"] == "geometria"
    sessao.expire_all()
    gravada = sessao.get(ComunidadeVirtual, comunidade.id)
    assert gravada.contorno == CONTORNO
    assert gravada.contorno_origem_osm == "way/1"


@pytest.mark.parametrize("origem", ["node/123", "relation/", "12582832", "relation/12a"])
def test_origem_fora_do_padrao_do_osm_e_recusada(
    cliente, sessao, admin_em_sessao, criar_comunidade, origem
):
    chave, token = admin_em_sessao
    comunidade = criar_comunidade()

    resposta = _gravar(
        cliente, chave, token, comunidade.id, {"geometria": CONTORNO, "origem_osm": origem}
    )

    assert resposta.status_code == 422
    assert resposta.json()["campo"] == "origem_osm"
    sessao.expire_all()
    assert sessao.get(ComunidadeVirtual, comunidade.id).contorno is None


@pytest.mark.parametrize(
    "papel", [Papel.mestre, Papel.guerreiro, Papel.responsavel, Papel.apoiador]
)
def test_quem_nao_e_admin_recebe_403_e_nada_muda(
    cliente,
    sessao,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    papel,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    persona = criar_persona(papel, criada_por=admin, comunidade=comunidade)
    token, _ = criar_sessao_de_teste(persona)

    resposta = _gravar(
        cliente, chave, token, comunidade.id, {"geometria": CONTORNO, "origem_osm": "way/1"}
    )

    assert resposta.status_code == 403
    sessao.expire_all()
    assert sessao.get(ComunidadeVirtual, comunidade.id).contorno is None


def test_comunidade_inexistente_responde_404(cliente, admin_em_sessao):
    chave, token = admin_em_sessao
    resposta = _gravar(
        cliente, chave, token, uuid.uuid4(), {"geometria": CONTORNO, "origem_osm": "way/1"}
    )
    assert resposta.status_code == 404
