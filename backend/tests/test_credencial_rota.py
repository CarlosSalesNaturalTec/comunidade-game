import uuid

from nucleo.personas.modelo import Papel


def test_admin_cria_credencial_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.post(
        "/v1/credenciais",
        json={"persona_id": str(mestre.id), "usuario": "Mestre_sem_conta"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["usuario"] == "Mestre_sem_conta"
    assert "senha_provisoria" in corpo


def test_quem_nao_e_admin_nem_mestre_recebe_403_na_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador, criada_por=admin)
    responsavel = criar_persona(Papel.responsavel, criada_por=admin)
    token, _ = criar_sessao_de_teste(apoiador)

    resposta = cliente.post(
        "/v1/credenciais",
        json={"persona_id": str(responsavel.id), "usuario": "alguem"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 403
    assert resposta.json()["codigo"] == "permissao_negada"


def test_criar_credencial_para_persona_inexistente_e_404(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.post(
        "/v1/credenciais",
        json={"persona_id": str(uuid.uuid4()), "usuario": "alguem"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 404


def test_trocar_senha_sem_credencial_de_usuario_e_senha_e_404(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    """Persona autenticada só por login social não tem o que trocar."""
    chave, _ = criar_chave()
    persona = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(persona)

    resposta = cliente.post(
        "/v1/credenciais/senha",
        json={"senha_nova": "nova-senha"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 404
