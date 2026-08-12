from nucleo.personas.modelo import Credencial, Papel, TipoDeCredencial

DESCRITOR = [0.1, 0.2, 0.3, 0.4]


def _mestre_com_sessao(criar_persona, criar_sessao_de_teste):
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    token, _ = criar_sessao_de_teste(mestre)
    return mestre, token


class TestGravarDescritor:
    def test_mestre_grava_com_consentimento_vigente(
        self,
        cliente,
        criar_chave,
        criar_persona,
        criar_sessao_de_teste,
        conceder_consentimento_biometrico,
    ):
        chave, _ = criar_chave()
        mestre, token = _mestre_com_sessao(criar_persona, criar_sessao_de_teste)
        guerreiro = criar_persona(Papel.guerreiro)
        admin = criar_persona(Papel.admin)
        responsavel = criar_persona(Papel.responsavel, criada_por=admin)
        conceder_consentimento_biometrico(responsavel, guerreiro)

        resposta = cliente.post(
            f"/v1/guerreiros/{guerreiro.id}/descritor",
            json={"descritor": DESCRITOR},
            headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
        )
        assert resposta.status_code == 201
        corpo = resposta.json()
        assert corpo["guerreiro_id"] == str(guerreiro.id)
        assert "descritor" not in corpo
        assert "segredo" not in corpo
        assert "template" not in corpo

    def test_sem_consentimento_e_recusado(
        self, cliente, criar_chave, criar_persona, criar_sessao_de_teste
    ):
        chave, _ = criar_chave()
        _, token = _mestre_com_sessao(criar_persona, criar_sessao_de_teste)
        guerreiro = criar_persona(Papel.guerreiro)

        resposta = cliente.post(
            f"/v1/guerreiros/{guerreiro.id}/descritor",
            json={"descritor": DESCRITOR},
            headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
        )
        assert resposta.status_code == 422

    def test_guerreiro_nao_grava_o_proprio_template(
        self, cliente, criar_chave, criar_persona, criar_sessao_de_teste
    ):
        chave, _ = criar_chave()
        guerreiro = criar_persona(Papel.guerreiro)
        token, _ = criar_sessao_de_teste(guerreiro)

        resposta = cliente.post(
            f"/v1/guerreiros/{guerreiro.id}/descritor",
            json={"descritor": DESCRITOR},
            headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
        )
        assert resposta.status_code == 403

    def test_papel_diferente_de_mestre_ou_admin_recebe_403(
        self, cliente, criar_chave, criar_persona, criar_sessao_de_teste
    ):
        chave, _ = criar_chave()
        admin = criar_persona(Papel.admin)
        apoiador = criar_persona(Papel.apoiador, criada_por=admin)
        guerreiro = criar_persona(Papel.guerreiro)
        token, _ = criar_sessao_de_teste(apoiador)

        resposta = cliente.post(
            f"/v1/guerreiros/{guerreiro.id}/descritor",
            json={"descritor": DESCRITOR},
            headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
        )
        assert resposta.status_code == 403

    def test_envio_de_imagem_e_recusado(
        self, cliente, criar_chave, criar_persona, criar_sessao_de_teste
    ):
        chave, _ = criar_chave()
        _, token = _mestre_com_sessao(criar_persona, criar_sessao_de_teste)
        guerreiro = criar_persona(Papel.guerreiro)

        resposta = cliente.post(
            f"/v1/guerreiros/{guerreiro.id}/descritor",
            json={"descritor": DESCRITOR, "foto": "base64=="},
            headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
        )
        assert resposta.status_code == 422

    def test_guerreiro_inexistente_e_recusado(
        self, cliente, criar_chave, criar_persona, criar_sessao_de_teste
    ):
        chave, _ = criar_chave()
        _, token = _mestre_com_sessao(criar_persona, criar_sessao_de_teste)

        resposta = cliente.post(
            "/v1/guerreiros/00000000-0000-0000-0000-000000000000/descritor",
            json={"descritor": DESCRITOR},
            headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
        )
        assert resposta.status_code == 404

    def test_recadastro_grava_quem_recadastrou_com_data_e_hora(
        self,
        cliente,
        criar_chave,
        criar_persona,
        criar_sessao_de_teste,
        conceder_consentimento_biometrico,
        sessao,
    ):
        chave, _ = criar_chave()
        mestre, token = _mestre_com_sessao(criar_persona, criar_sessao_de_teste)
        guerreiro = criar_persona(Papel.guerreiro)
        admin = criar_persona(Papel.admin)
        responsavel = criar_persona(Papel.responsavel, criada_por=admin)
        conceder_consentimento_biometrico(responsavel, guerreiro)
        cabecalhos = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}

        cliente.post(
            f"/v1/guerreiros/{guerreiro.id}/descritor",
            json={"descritor": DESCRITOR},
            headers=cabecalhos,
        )
        cliente.post(
            f"/v1/guerreiros/{guerreiro.id}/descritor",
            json={"descritor": [0.9, 0.8, 0.7, 0.6]},
            headers=cabecalhos,
        )

        ativas = (
            sessao.query(Credencial)
            .filter_by(persona_id=guerreiro.id, tipo=TipoDeCredencial.biometria, ativa=True)
            .all()
        )
        assert len(ativas) == 1
        assert ativas[0].criada_por == mestre.id
        assert ativas[0].criada_em is not None


class TestNaoExisteRotaDeLeituraDoTemplate:
    def test_get_no_descritor_nao_e_permitido(
        self, cliente, criar_chave, criar_persona, criar_sessao_de_teste
    ):
        """A rota `.../descritor` só aceita `POST` — não há verbo de
        leitura registrado nela."""
        chave, _ = criar_chave()
        _, token = _mestre_com_sessao(criar_persona, criar_sessao_de_teste)
        guerreiro = criar_persona(Papel.guerreiro)

        resposta = cliente.get(
            f"/v1/guerreiros/{guerreiro.id}/descritor",
            headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
        )
        assert resposta.status_code == 405

    def test_nenhuma_rota_de_leitura_do_template_existe(
        self, cliente, criar_chave, criar_persona, criar_sessao_de_teste
    ):
        chave, _ = criar_chave()
        _, token = _mestre_com_sessao(criar_persona, criar_sessao_de_teste)
        guerreiro = criar_persona(Papel.guerreiro)
        cabecalhos = {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}

        for caminho in (
            f"/v1/guerreiros/{guerreiro.id}/template",
            f"/v1/guerreiros/{guerreiro.id}",
            "/v1/templates",
        ):
            resposta = cliente.get(caminho, headers=cabecalhos)
            assert resposta.status_code == 404
