"""Fatia 1 do PRD-08 — a leitura pública devolve o contorno com o crédito do
OSM, e a exportação não o leva (`RF-08-34`, `RN-08-31`, `RN-08-32`, change
`2026-11-27-contorno-da-comunidade`)."""

from datetime import UTC, datetime

from nucleo.comunidades.contorno import CREDITO_DO_OSM, LICENCA_DO_CONTORNO
from nucleo.locais.modelo import NivelDoLocal
from nucleo.personas.modelo import Papel

MOMENTO = datetime(2026, 6, 1, 12, 0, tzinfo=UTC)
COPIADO_EM = datetime(2026, 11, 27, 20, 0, tzinfo=UTC)
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
CAMPOS_DO_CONTORNO = {"geometria", "origem_osm", "copiado_em", "credito", "licenca"}


def _com_contorno(sessao, comunidade):
    comunidade.contorno = CONTORNO
    comunidade.contorno_origem_osm = "relation/12582832"
    comunidade.contorno_copiado_em = COPIADO_EM
    sessao.commit()
    return comunidade


def _territorio_com_coleta(
    criar_comunidade,
    criar_local,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
    criar_desafio_de_coleta,
    criar_serie_de_coleta,
    criar_registro_de_coleta,
    coletores: int,
):
    """Comunidade com bairro e `coletores` Guerreiros e Guerreiras com
    registro válido — dois fica abaixo do piso de três."""
    comunidade = criar_comunidade()
    raiz = criar_local(comunidade, nivel=NivelDoLocal.comunidade, rotulo="Comunidade")
    bairro = criar_local(comunidade, nivel=NivelDoLocal.bairro, rotulo="Bairro", local_pai=raiz)
    mestre = criar_persona(Papel.mestre)
    missao = criar_missao(criar_trilha(mestre), mestre)
    desafio = criar_desafio_de_coleta(missao, mestre, tipo=criar_tipo_de_coleta(mestre))
    for _ in range(coletores):
        guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
        serie = criar_serie_de_coleta(guerreiro, desafio, bairro)
        criar_registro_de_coleta(serie, guerreiro, comunidade.id, momento_do_fato=MOMENTO)
    return comunidade


def _item_da_lista(cliente, chave, comunidade):
    resposta = cliente.get("/v1/comunidades", headers={"X-Chave-Aplicacao": chave})
    assert resposta.status_code == 200
    return next(i for i in resposta.json()["itens"] if i["id"] == str(comunidade.id))


def _confere_contorno(contorno):
    assert set(contorno) == CAMPOS_DO_CONTORNO
    assert contorno["geometria"] == CONTORNO
    assert contorno["origem_osm"] == "relation/12582832"
    assert datetime.fromisoformat(contorno["copiado_em"]) == COPIADO_EM
    assert contorno["credito"] == CREDITO_DO_OSM == "© colaboradores do OpenStreetMap"
    assert contorno["licenca"] == LICENCA_DO_CONTORNO == "ODbL"


def test_lista_e_leitura_trazem_o_contorno_com_credito_e_licenca(
    cliente, sessao, criar_chave, criar_comunidade
):
    comunidade = _com_contorno(sessao, criar_comunidade())
    chave, _ = criar_chave()

    _confere_contorno(_item_da_lista(cliente, chave, comunidade)["contorno"])
    resposta = cliente.get(f"/v1/comunidades/{comunidade.id}", headers={"X-Chave-Aplicacao": chave})
    assert resposta.status_code == 200
    _confere_contorno(resposta.json()["contorno"])


def test_comunidade_sem_contorno_sai_sem_ele_e_segue_na_lista(
    cliente, criar_chave, criar_comunidade
):
    comunidade = criar_comunidade()
    chave, _ = criar_chave()

    assert _item_da_lista(cliente, chave, comunidade)["contorno"] is None
    resposta = cliente.get(f"/v1/comunidades/{comunidade.id}", headers={"X-Chave-Aplicacao": chave})
    assert resposta.json()["contorno"] is None


def test_contorno_sai_abaixo_do_piso_e_sem_dado_de_coleta(
    cliente,
    sessao,
    criar_chave,
    criar_comunidade,
    criar_local,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
    criar_desafio_de_coleta,
    criar_serie_de_coleta,
    criar_registro_de_coleta,
):
    """Dois coletores e piso três: os indicadores somem, o contorno não — e
    ele traz só os cinco campos, sem local, série, registro ou coletor
    (`RF-08-34`, `RN-08-28`, `RN-08-32`)."""
    comunidade = _territorio_com_coleta(
        criar_comunidade,
        criar_local,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_tipo_de_coleta,
        criar_desafio_de_coleta,
        criar_serie_de_coleta,
        criar_registro_de_coleta,
        coletores=2,
    )
    _com_contorno(sessao, comunidade)
    chave, _ = criar_chave()

    item = _item_da_lista(cliente, chave, comunidade)
    assert item["series_abertas"] is None
    _confere_contorno(item["contorno"])


def test_exportacao_e_dicionario_nao_levam_o_contorno(
    cliente,
    sessao,
    criar_chave,
    criar_comunidade,
    criar_local,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
    criar_desafio_de_coleta,
    criar_serie_de_coleta,
    criar_registro_de_coleta,
):
    comunidade = _territorio_com_coleta(
        criar_comunidade,
        criar_local,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_tipo_de_coleta,
        criar_desafio_de_coleta,
        criar_serie_de_coleta,
        criar_registro_de_coleta,
        coletores=3,
    )
    _com_contorno(sessao, comunidade)
    chave, _ = criar_chave()

    exportacao = cliente.get(
        f"/v1/comunidades/{comunidade.id}/exportacao", headers={"X-Chave-Aplicacao": chave}
    )
    assert exportacao.status_code == 200
    assert exportacao.headers["X-Licenca"] == "CC BY-SA"
    assert exportacao.text.strip()
    for vestigio in ("contorno", "Polygon", "-38.4801", "relation/12582832"):
        assert vestigio not in exportacao.text

    dicionario = cliente.get(
        exportacao.headers["X-Dicionario-De-Dados"], headers={"X-Chave-Aplicacao": chave}
    )
    assert dicionario.status_code == 200
    assert dicionario.json()["licenca"] == "CC BY-SA"
    for vestigio in ("contorno", "Polygon", "relation/12582832"):
        assert vestigio not in dicionario.text
