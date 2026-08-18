from nucleo.personas.modelo import Papel
from nucleo.recursos.modelo import NaturezaDoRecurso


def test_admin_cadastra_tipo_de_recurso_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.post(
        "/v1/tipos-de-recurso",
        json={
            "nome": "Lanche",
            "natureza": NaturezaDoRecurso.consumivel.value,
            "unidade": "unidade",
            "valor_em_moedas": "1.50",
            "vigencia_inicio": "2026-01-01",
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["nome"] == "Lanche"
    assert corpo["natureza"] == NaturezaDoRecurso.consumivel.value
    assert corpo["valor_em_moedas"] == "1.50"
    assert corpo["vigencia_inicio"] == "2026-01-01"


def test_quem_nao_e_admin_recebe_403_ao_cadastrar_tipo_de_recurso(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.post(
        "/v1/tipos-de-recurso",
        json={
            "nome": "Lanche",
            "natureza": NaturezaDoRecurso.consumivel.value,
            "unidade": "unidade",
            "valor_em_moedas": "1.50",
            "vigencia_inicio": "2026-01-01",
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 403


def test_cadastro_de_tipo_de_recurso_sem_chave_e_recusado_com_401(
    cliente, criar_persona, criar_sessao_de_teste
):
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.post(
        "/v1/tipos-de-recurso",
        json={
            "nome": "Lanche",
            "natureza": NaturezaDoRecurso.consumivel.value,
            "unidade": "unidade",
            "valor_em_moedas": "1.50",
            "vigencia_inicio": "2026-01-01",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 401


def test_valor_negativo_e_recusado_com_422_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.post(
        "/v1/tipos-de-recurso",
        json={
            "nome": "Lanche",
            "natureza": NaturezaDoRecurso.consumivel.value,
            "unidade": "unidade",
            "valor_em_moedas": "-1.50",
            "vigencia_inicio": "2026-01-01",
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 422
