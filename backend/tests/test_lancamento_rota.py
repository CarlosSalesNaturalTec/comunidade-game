from decimal import Decimal

from nucleo.livro_razao.regra import lancar_credito
from nucleo.personas.modelo import Papel


def test_admin_lanca_ajuste_pela_rota(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    sessao,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)

    credito = lancar_credito(
        sessao,
        tipo_de_recurso_id=tipo.id,
        ponto_de_apoio_id=ponto_de_apoio.id,
        quantidade=Decimal("3.00"),
        valor_em_moedas=Decimal("3.00"),
        operador=admin,
    )
    sessao.commit()

    resposta = cliente.post(
        f"/v1/lancamentos/{credito.id}/ajuste",
        json={"quantidade": "-1.00", "valor_em_moedas": "-1.00", "motivo": "Corrige a maior."},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["natureza"] == "ajuste"
    assert corpo["lancamento_original_id"] == str(credito.id)
    assert corpo["motivo_do_ajuste"] == "Corrige a maior."


def test_mestre_nao_lanca_ajuste_pela_rota(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    sessao,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    token, _ = criar_sessao_de_teste(mestre)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)

    credito = lancar_credito(
        sessao,
        tipo_de_recurso_id=tipo.id,
        ponto_de_apoio_id=ponto_de_apoio.id,
        quantidade=Decimal("3.00"),
        valor_em_moedas=Decimal("3.00"),
        operador=admin,
    )
    sessao.commit()

    resposta = cliente.post(
        f"/v1/lancamentos/{credito.id}/ajuste",
        json={"quantidade": "-1.00", "valor_em_moedas": "-1.00", "motivo": "Corrige a maior."},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 403


def test_edicao_de_lancamento_responde_405(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    sessao,
):
    """Não há `PUT` nem `PATCH` declarados sobre `lancamento`: o FastAPI
    responde 405 sozinho ao método não previsto no caminho existente
    (`RF-07-19`, design — Decisions 4)."""
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)

    credito = lancar_credito(
        sessao,
        tipo_de_recurso_id=tipo.id,
        ponto_de_apoio_id=ponto_de_apoio.id,
        quantidade=Decimal("3.00"),
        valor_em_moedas=Decimal("3.00"),
        operador=admin,
    )
    sessao.commit()

    resposta = cliente.put(
        f"/v1/lancamentos/{credito.id}/ajuste", headers={"X-Chave-Aplicacao": chave}
    )

    assert resposta.status_code == 405


def test_ajuste_sem_chave_e_recusado_com_401(
    cliente,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    sessao,
):
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)

    credito = lancar_credito(
        sessao,
        tipo_de_recurso_id=tipo.id,
        ponto_de_apoio_id=ponto_de_apoio.id,
        quantidade=Decimal("3.00"),
        valor_em_moedas=Decimal("3.00"),
        operador=admin,
    )
    sessao.commit()

    resposta = cliente.post(
        f"/v1/lancamentos/{credito.id}/ajuste",
        json={"quantidade": "-1.00", "valor_em_moedas": "-1.00", "motivo": "Corrige."},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 401
