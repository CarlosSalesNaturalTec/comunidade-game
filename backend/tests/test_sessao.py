from datetime import UTC, datetime, timedelta

from nucleo.personas.modelo import Papel, Persona, TipoDeCredencial
from nucleo.sessoes.social import obter_verificador_social


def _sobrescrever_verificador_social(app, email: str | None):
    """Substitui a verificação real do Google por um dublê — os testes de
    rota não fazem chamada de rede nenhuma."""

    def _falso_verificador():
        def _verificar(token: str) -> str:
            if email is None:
                from nucleo.sessoes.social import TokenSocialInvalido

                raise TokenSocialInvalido()
            return email

        return _verificar

    app.dependency_overrides[obter_verificador_social] = _falso_verificador


def test_login_social_com_cadastro_abre_sessao(cliente, app, criar_chave, criar_persona, sessao):
    from nucleo.personas.modelo import Credencial

    chave, _ = criar_chave()
    persona = criar_persona(Papel.mestre)
    sessao.add(
        Credencial(
            persona_id=persona.id,
            tipo=TipoDeCredencial.login_social,
            identificador="mestre@example.org",
            ativa=True,
        )
    )
    sessao.commit()
    _sobrescrever_verificador_social(app, "mestre@example.org")

    resposta = cliente.post(
        "/v1/sessoes/social",
        json={"id_token": "qualquer-coisa"},
        headers={"X-Chave-Aplicacao": chave},
    )
    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["papel"] == "mestre"
    assert "token" in corpo


def test_login_social_sem_cadastro_e_recusado_e_nao_cria_persona(cliente, app, criar_chave, sessao):
    chave, _ = criar_chave()
    _sobrescrever_verificador_social(app, "ninguem@example.org")

    antes = sessao.query(Persona).count()
    resposta = cliente.post(
        "/v1/sessoes/social",
        json={"id_token": "qualquer-coisa"},
        headers={"X-Chave-Aplicacao": chave},
    )
    assert resposta.status_code == 403
    assert resposta.json()["codigo"] == "login_sem_cadastro"
    assert sessao.query(Persona).count() == antes


def test_token_social_invalido_e_recusado_sem_criar_persona(cliente, app, criar_chave, sessao):
    chave, _ = criar_chave()
    _sobrescrever_verificador_social(app, None)

    antes = sessao.query(Persona).count()
    resposta = cliente.post(
        "/v1/sessoes/social",
        json={"id_token": "invalido"},
        headers={"X-Chave-Aplicacao": chave},
    )
    assert resposta.status_code == 403
    assert sessao.query(Persona).count() == antes


def test_login_por_credencial_valida_abre_sessao(
    cliente, criar_chave, criar_persona, criar_credencial, configuracao
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    responsavel = criar_persona(Papel.responsavel, criada_por=admin)
    criar_credencial(
        responsavel,
        tipo=TipoDeCredencial.usuario_e_senha,
        identificador="Pai_da_Maria",
        senha="senha-provisoria-123",
        troca_pendente=False,
    )

    resposta = cliente.post(
        "/v1/sessoes/credencial",
        json={"usuario": "Pai_da_Maria", "senha": "senha-provisoria-123"},
        headers={"X-Chave-Aplicacao": chave},
    )
    assert resposta.status_code == 201
    assert resposta.json()["papel"] == "responsavel"


def test_login_por_credencial_com_senha_errada_nao_abre_sessao(
    cliente, criar_chave, criar_persona, criar_credencial
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    responsavel = criar_persona(Papel.responsavel, criada_por=admin)
    criar_credencial(
        responsavel,
        tipo=TipoDeCredencial.usuario_e_senha,
        identificador="Pai_da_Maria",
        senha="senha-certa",
        troca_pendente=False,
    )

    resposta = cliente.post(
        "/v1/sessoes/credencial",
        json={"usuario": "Pai_da_Maria", "senha": "senha-errada"},
        headers={"X-Chave-Aplicacao": chave},
    )
    assert resposta.status_code == 401


def test_login_por_usuario_inexistente_e_recusado_do_mesmo_modo(cliente, criar_chave, sessao):
    chave, _ = criar_chave()
    antes = sessao.query(Persona).count()

    resposta = cliente.post(
        "/v1/sessoes/credencial",
        json={"usuario": "ninguem", "senha": "qualquer"},
        headers={"X-Chave-Aplicacao": chave},
    )
    assert resposta.status_code == 403
    assert resposta.json()["codigo"] == "login_sem_cadastro"
    assert sessao.query(Persona).count() == antes


def test_senha_provisoria_trava_a_sessao_ate_ser_trocada(
    cliente, criar_chave, criar_persona, criar_credencial, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    criar_credencial(
        mestre,
        tipo=TipoDeCredencial.usuario_e_senha,
        identificador="Mestre_novo",
        senha="provisoria",
        troca_pendente=True,
    )
    token, _ = criar_sessao_de_teste(mestre)
    cabecalhos = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}

    outra_rota = cliente.get("/v1/eu", headers=cabecalhos)
    assert outra_rota.status_code == 403
    assert outra_rota.json()["codigo"] == "troca_de_senha_pendente"

    rota_de_troca = cliente.post(
        "/v1/credenciais/senha", json={"senha_nova": "senha-nova-123"}, headers=cabecalhos
    )
    assert rota_de_troca.status_code == 204


def test_trocada_a_senha_a_trava_cai(
    cliente, criar_chave, criar_persona, criar_credencial, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    criar_credencial(
        mestre,
        tipo=TipoDeCredencial.usuario_e_senha,
        identificador="Mestre_novo",
        senha="provisoria",
        troca_pendente=True,
    )
    token, _ = criar_sessao_de_teste(mestre)
    cabecalhos = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}

    cliente.post("/v1/credenciais/senha", json={"senha_nova": "senha-nova-123"}, headers=cabecalhos)

    resposta = cliente.get("/v1/eu", headers=cabecalhos)
    assert resposta.status_code == 200
    assert resposta.json()["papel"] == "mestre"


def test_senha_provisoria_nao_serve_para_segundo_acesso(
    cliente, criar_chave, criar_persona, criar_credencial, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    criar_credencial(
        mestre,
        tipo=TipoDeCredencial.usuario_e_senha,
        identificador="Mestre_novo",
        senha="provisoria",
        troca_pendente=True,
    )
    token, _ = criar_sessao_de_teste(mestre)
    cliente.post(
        "/v1/credenciais/senha",
        json={"senha_nova": "senha-nova-123"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    segundo_login = cliente.post(
        "/v1/sessoes/credencial",
        json={"usuario": "Mestre_novo", "senha": "provisoria"},
        headers={"X-Chave-Aplicacao": chave},
    )
    assert segundo_login.status_code == 401


def test_encerrar_sessao_derruba_o_token(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    persona = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(persona)
    cabecalhos = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}

    encerrar = cliente.delete("/v1/sessoes/atual", headers=cabecalhos)
    assert encerrar.status_code == 204

    depois = cliente.get("/v1/eu", headers=cabecalhos)
    assert depois.status_code == 401
    assert depois.json()["codigo"] == "sessao_invalida"


def test_sessao_expirada_responde_401(cliente, criar_chave, criar_persona, criar_sessao_de_teste):
    chave, _ = criar_chave()
    persona = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(persona, expira_em=datetime.now(UTC) - timedelta(seconds=1))

    resposta = cliente.get(
        "/v1/eu", headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}
    )
    assert resposta.status_code == 401
    assert resposta.json()["codigo"] == "sessao_invalida"


def test_uma_sessao_nao_alcanca_outra(cliente, criar_chave, criar_persona, criar_sessao_de_teste):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    token_do_admin, _ = criar_sessao_de_teste(admin)
    token_do_mestre, _ = criar_sessao_de_teste(mestre)

    cliente.delete(
        "/v1/sessoes/atual",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token_do_admin}"},
    )

    ainda_valida = cliente.get(
        "/v1/eu",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token_do_mestre}"},
    )
    assert ainda_valida.status_code == 200
    assert ainda_valida.json()["papel"] == "mestre"


def test_eu_devolve_persona_papel_e_permissoes(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    persona = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(persona)

    resposta = cliente.get(
        "/v1/eu", headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}
    )
    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["persona_id"] == str(persona.id)
    assert corpo["papel"] == "admin"
    assert corpo["permissoes"]["escreve"] == ["tudo"]


def test_rota_nova_sem_chave_responde_401_sem_diferenciar_motivo(cliente):
    """Regressão da fatia anterior (RN-01-32): as rotas desta fatia também
    ficam atrás da exigência de chave."""
    resposta = cliente.get("/v1/eu")
    assert resposta.status_code == 401
    assert resposta.json()["codigo"] == "chave_invalida"


def test_escrita_sem_persona_e_recusada_mesmo_com_chave_vigente(cliente, criar_chave):
    chave, _ = criar_chave()
    resposta = cliente.post(
        "/v1/credenciais/senha", json={"senha_nova": "x"}, headers={"X-Chave-Aplicacao": chave}
    )
    assert resposta.status_code == 401
    assert resposta.json()["codigo"] == "sessao_ausente"
