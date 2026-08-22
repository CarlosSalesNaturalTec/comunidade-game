from datetime import UTC, datetime, timedelta

from sqlalchemy import insert, select
from sqlalchemy.orm import Mapped, mapped_column

from nucleo.banco import Base
from nucleo.tempo import ComMomentoDoFato


class _RegistroDeExemplo(Base, ComMomentoDoFato):
    """Modelo só de teste, para exercitar o mixin sem inventar entidade de domínio."""

    __tablename__ = "registro_de_exemplo_momento_do_fato"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


def test_rota_de_dados_sob_prefixo_responde(cliente, criar_chave):
    chave, _ = criar_chave()
    resposta = cliente.get("/v1/publica", headers={"X-Chave-Aplicacao": chave})
    assert resposta.status_code == 200


def test_rota_de_dados_sem_prefixo_nao_existe(cliente, criar_chave):
    chave, _ = criar_chave()
    resposta = cliente.get("/publica", headers={"X-Chave-Aplicacao": chave})
    assert resposta.status_code == 404
    corpo = resposta.json()
    assert corpo["codigo"] == "nao_encontrado"
    assert "mensagem" in corpo


def test_erro_de_validacao_nomeia_o_campo(cliente, criar_chave):
    chave, _ = criar_chave()
    resposta = cliente.post(
        "/v1/eventos",
        json={"momento_do_fato": "não é uma data"},
        headers={"X-Chave-Aplicacao": chave},
    )
    assert resposta.status_code == 422
    corpo = resposta.json()
    assert corpo["codigo"] == "erro_de_validacao"
    assert corpo["campo"] == "momento_do_fato"


def test_falha_nao_tratada_responde_500_sem_detalhe_interno(cliente, criar_chave, caplog):
    chave, _ = criar_chave()
    resposta = cliente.get("/v1/quebra", headers={"X-Chave-Aplicacao": chave})
    assert resposta.status_code == 500
    corpo = resposta.json()
    assert corpo == {"codigo": "erro_interno", "mensagem": corpo["mensagem"]}
    texto = str(corpo)
    assert "RuntimeError" not in texto
    assert "Traceback" not in texto
    assert ".py" not in texto


def test_tamanho_de_pagina_acima_do_teto_e_recusado(cliente, criar_chave):
    chave, _ = criar_chave()
    resposta = cliente.get(
        "/v1/itens", params={"tamanho": "1000"}, headers={"X-Chave-Aplicacao": chave}
    )
    assert resposta.status_code == 422
    corpo = resposta.json()
    assert corpo["codigo"] == "tamanho_de_pagina_acima_do_teto"
    assert corpo["campo"] == "tamanho"


def test_parametro_desconhecido_e_recusado_em_vez_de_ignorado(cliente, criar_chave):
    chave, _ = criar_chave()
    resposta = cliente.get(
        "/v1/itens", params={"tema": "espacial"}, headers={"X-Chave-Aplicacao": chave}
    )
    assert resposta.status_code == 422
    corpo = resposta.json()
    assert corpo["codigo"] == "parametro_desconhecido"
    assert corpo["campo"] == "tema"


def test_filtro_do_dominio_declarado_e_aceito(cliente, criar_chave):
    chave, _ = criar_chave()
    resposta = cliente.get(
        "/v1/itens", params={"cor": "azul"}, headers={"X-Chave-Aplicacao": chave}
    )
    assert resposta.status_code == 200
    assert resposta.json()["itens"] == ["azul"]


def test_data_e_hora_sem_fuso_e_recusada(cliente, criar_chave):
    chave, _ = criar_chave()
    resposta = cliente.post(
        "/v1/eventos",
        json={"momento_do_fato": "2026-08-01T10:00:00"},
        headers={"X-Chave-Aplicacao": chave},
    )
    assert resposta.status_code == 422
    corpo = resposta.json()
    assert corpo["codigo"] == "erro_de_validacao"
    assert corpo["campo"] == "momento_do_fato"


def test_data_e_hora_com_fuso_e_aceita(cliente, criar_chave):
    chave, _ = criar_chave()
    resposta = cliente.post(
        "/v1/eventos",
        json={"momento_do_fato": "2026-08-01T10:00:00-03:00"},
        headers={"X-Chave-Aplicacao": chave},
    )
    assert resposta.status_code == 200


def test_data_do_fato_sobrevive_a_envio_atrasado(conexao):
    """Exercita o mixin `ComMomentoDoFato`: o momento do fato é o que foi
    informado, e o momento do registro é sempre o instante da gravação —
    mesmo quando o fato aconteceu bem antes de chegar ao núcleo."""
    momento_do_fato_atrasado = datetime.now(UTC) - timedelta(days=3)
    with conexao.begin_nested():
        conexao.execute(
            insert(_RegistroDeExemplo.__table__).values(momento_do_fato=momento_do_fato_atrasado)
        )
        linha = conexao.execute(select(_RegistroDeExemplo.__table__)).one()

    assert linha.momento_do_fato == momento_do_fato_atrasado
    assert linha.momento_do_registro > momento_do_fato_atrasado


def test_openapi_responde_sem_chave(cliente):
    resposta = cliente.get("/openapi.json")
    assert resposta.status_code == 200


def test_openapi_nao_serve_dado_de_dominio(cliente):
    """ "guerreiro" é um valor legítimo do enum `Papel`, contrato desta fatia
    (RF-01-19), "aporte" é o aporte declarado na solicitação de
    participação (`RF-01-25`, PRD-01 §8), e "comunidade virtual" é a
    própria capacidade que esta fatia abre (`RF-08-01`) — o que a rota
    nunca serve é entidade de domínio de fatia futura, como o território
    georreferenciado da série de coleta (PRD-08 §9, fora deste recorte)."""
    schema = cliente.get("/openapi.json").json()
    texto = str(schema).lower()
    assert "território" not in texto


def test_ler_schema_nao_abre_rota_de_dados(cliente):
    cliente.get("/openapi.json")
    resposta = cliente.get("/v1/publica")
    assert resposta.status_code == 401


def test_preflight_permite_os_cabecalhos_da_chave_e_da_sessao(cliente):
    resposta = cliente.options(
        "/v1/publica",
        headers={
            "Origin": "https://app-06-vitrine.web.app",
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "x-chave-aplicacao, authorization",
        },
    )
    assert resposta.status_code == 200
    cabecalhos_permitidos = resposta.headers["access-control-allow-headers"].lower()
    assert "x-chave-aplicacao" in cabecalhos_permitidos
    assert "authorization" in cabecalhos_permitidos
    assert resposta.headers["access-control-allow-origin"] == "*"


def test_chamada_de_origem_qualquer_sem_chave_e_recusada_como_qualquer_outra(cliente):
    resposta = cliente.get("/v1/publica", headers={"Origin": "https://app-06-vitrine.web.app"})
    assert resposta.status_code == 401
    assert resposta.json()["codigo"] == "chave_invalida"


def test_nenhuma_rota_lista_ou_sugere_nick(cliente):
    """`RN-01-22`: o núcleo nunca descobre nem sugere um nick de
    Guerreiro(a) — não existe rota de listagem, busca parcial ou sugestão
    de nick em toda a API, fora da única exceção declarada:
    `GET /v1/nicks/disponibilidade`, restrita a nicks de adulto e que por
    isso nunca alcança nick de Guerreiro(a) (`RF-14-13`, capacidade
    `identidade-do-adulto`). `/v1/sugestoes` é a fila de propostas da
    gestão (`RF-01-25`), sem relação com nick — só a combinação dos dois
    termos denunciaria isso."""
    schema = cliente.get("/openapi.json").json()
    for caminho in schema["paths"]:
        if caminho == "/v1/nicks/disponibilidade":
            continue
        caminho_em_minusculas = caminho.lower()
        assert "nicks" not in caminho_em_minusculas
        assert "nick" not in caminho_em_minusculas or "sugest" not in caminho_em_minusculas
