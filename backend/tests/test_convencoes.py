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


def test_data_do_fato_sobrevive_a_envio_atrasado(engine):
    """Exercita o mixin `ComMomentoDoFato`: o momento do fato é o que foi
    informado, e o momento do registro é sempre o instante da gravação —
    mesmo quando o fato aconteceu bem antes de chegar ao núcleo."""
    momento_do_fato_atrasado = datetime.now(UTC) - timedelta(days=3)
    with engine.begin() as conexao:
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
    (RF-01-19), e "aporte" é o aporte declarado na solicitação de
    participação (`RF-01-25`, PRD-01 §8) — o que a rota nunca serve é
    entidade de domínio de fatia futura."""
    schema = cliente.get("/openapi.json").json()
    texto = str(schema).lower()
    for termo in ("comunidade virtual", "território"):
        assert termo not in texto


def test_ler_schema_nao_abre_rota_de_dados(cliente):
    cliente.get("/openapi.json")
    resposta = cliente.get("/v1/publica")
    assert resposta.status_code == 401


def test_nenhuma_rota_lista_ou_sugere_nick(cliente):
    """`RN-01-22`: o núcleo nunca descobre nem sugere um nick — não existe
    rota de listagem, busca parcial ou sugestão de nick em toda a API.
    `/v1/sugestoes` é a fila de propostas da gestão (`RF-01-25`), sem
    relação com nick — só a combinação dos dois termos denunciaria isso."""
    schema = cliente.get("/openapi.json").json()
    for caminho in schema["paths"]:
        caminho_em_minusculas = caminho.lower()
        assert "nicks" not in caminho_em_minusculas
        assert "nick" not in caminho_em_minusculas or "sugest" not in caminho_em_minusculas
