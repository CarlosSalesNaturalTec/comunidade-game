from datetime import UTC, datetime, timedelta

from nucleo.personas.modelo import Papel
from nucleo.sessoes.modelo import ComoAutenticou, Sessao

DESCRITOR = [0.1, 0.2, 0.3, 0.4]


def _guerreiro_com_nick(criar_persona, criar_nick, nick="Guerreiro_da_rota"):
    guerreiro = criar_persona(Papel.guerreiro)
    criar_nick(guerreiro, nick)
    return guerreiro


class TestAbrirSessaoDeGuerreiro:
    def test_nick_e_descritor_conferem_abre_sessao(
        self, cliente, criar_chave, criar_persona, criar_nick, criar_template_biometrico
    ):
        chave, _ = criar_chave()
        guerreiro = _guerreiro_com_nick(criar_persona, criar_nick)
        criar_template_biometrico(guerreiro, descritor=DESCRITOR)

        resposta = cliente.post(
            "/v1/sessoes/guerreiro",
            json={"nick": "Guerreiro_da_rota", "descritor": DESCRITOR},
            headers={"X-Chave-Aplicacao": chave},
        )
        assert resposta.status_code == 201
        corpo = resposta.json()
        assert corpo["papel"] == "guerreiro"
        assert "token" in corpo

    def test_nao_exige_credencial_de_persona(
        self, cliente, criar_chave, criar_persona, criar_nick, criar_template_biometrico
    ):
        """`RF-01-04`: pública quanto à persona — sem `Authorization`."""
        chave, _ = criar_chave()
        guerreiro = _guerreiro_com_nick(criar_persona, criar_nick, nick="Sem_authorization")
        criar_template_biometrico(guerreiro, descritor=DESCRITOR)

        resposta = cliente.post(
            "/v1/sessoes/guerreiro",
            json={"nick": "Sem_authorization", "descritor": DESCRITOR},
            headers={"X-Chave-Aplicacao": chave},
        )
        assert resposta.status_code == 201

    def test_sem_chave_e_recusado(self, cliente):
        resposta = cliente.post(
            "/v1/sessoes/guerreiro", json={"nick": "qualquer", "descritor": DESCRITOR}
        )
        assert resposta.status_code == 401
        assert resposta.json()["codigo"] == "chave_invalida"

    def test_sem_descritor_e_recusado(self, cliente, criar_chave):
        chave, _ = criar_chave()
        resposta = cliente.post(
            "/v1/sessoes/guerreiro", json={"nick": "qualquer"}, headers={"X-Chave-Aplicacao": chave}
        )
        assert resposta.status_code == 422
        assert resposta.json()["campo"] == "descritor"

    def test_envio_de_imagem_e_recusado(self, cliente, criar_chave):
        """`RN-01-15`: nenhum campo além de nick e descritor é aceito."""
        chave, _ = criar_chave()
        resposta = cliente.post(
            "/v1/sessoes/guerreiro",
            json={"nick": "qualquer", "descritor": DESCRITOR, "foto": "base64=="},
            headers={"X-Chave-Aplicacao": chave},
        )
        assert resposta.status_code == 422

    def test_tres_recusas_tem_corpo_e_codigo_identicos(
        self, cliente, criar_chave, criar_persona, criar_nick, criar_template_biometrico
    ):
        chave, _ = criar_chave()
        cabecalhos = {"X-Chave-Aplicacao": chave}

        nick_inexistente = cliente.post(
            "/v1/sessoes/guerreiro",
            json={"nick": "ninguem-existe", "descritor": DESCRITOR},
            headers=cabecalhos,
        )

        _guerreiro_com_nick(criar_persona, criar_nick, nick="Sem_template_rota")
        resposta_sem_template = cliente.post(
            "/v1/sessoes/guerreiro",
            json={"nick": "Sem_template_rota", "descritor": DESCRITOR},
            headers=cabecalhos,
        )

        com_template = _guerreiro_com_nick(criar_persona, criar_nick, nick="Descritor_errado")
        criar_template_biometrico(com_template, descritor=DESCRITOR)
        resposta_descritor_errado = cliente.post(
            "/v1/sessoes/guerreiro",
            json={"nick": "Descritor_errado", "descritor": [9.0, 9.0, 9.0, 9.0]},
            headers=cabecalhos,
        )

        respostas = [nick_inexistente, resposta_sem_template, resposta_descritor_errado]
        for resposta in respostas:
            assert resposta.status_code == 401
        corpos = [resposta.json() for resposta in respostas]
        assert corpos[0] == corpos[1] == corpos[2]
        assert corpos[0]["codigo"] == "autenticacao_biometrica_invalida"

    def test_sessao_aberta_tem_a_duracao_do_guerreiro_nao_a_do_adulto(
        self,
        cliente,
        criar_chave,
        criar_persona,
        criar_nick,
        criar_template_biometrico,
        sessao,
        configuracao,
    ):
        chave, _ = criar_chave()
        guerreiro = _guerreiro_com_nick(criar_persona, criar_nick, nick="Duracao_guerreiro")
        criar_template_biometrico(guerreiro, descritor=DESCRITOR)

        antes = datetime.now(UTC)
        resposta = cliente.post(
            "/v1/sessoes/guerreiro",
            json={"nick": "Duracao_guerreiro", "descritor": DESCRITOR},
            headers={"X-Chave-Aplicacao": chave},
        )
        expira_em = datetime.fromisoformat(resposta.json()["expira_em"])

        assert configuracao.sessao_guerreiro_duracao != configuracao.sessao_adulto_duracao
        diferenca = expira_em - antes
        assert abs(diferenca - configuracao.sessao_guerreiro_duracao) < timedelta(seconds=5)

    def test_registro_de_sessao_guarda_como_autenticou_biometria(
        self, cliente, criar_chave, criar_persona, criar_nick, criar_template_biometrico, sessao
    ):
        chave, _ = criar_chave()
        guerreiro = _guerreiro_com_nick(criar_persona, criar_nick, nick="Como_autenticou_bio")
        criar_template_biometrico(guerreiro, descritor=DESCRITOR)

        cliente.post(
            "/v1/sessoes/guerreiro",
            json={"nick": "Como_autenticou_bio", "descritor": DESCRITOR},
            headers={"X-Chave-Aplicacao": chave},
        )

        registro = sessao.query(Sessao).filter_by(persona_id=guerreiro.id).one()
        assert registro.como_autenticou == ComoAutenticou.biometria


class TestConfirmacaoDeSessaoDeGuerreiro:
    def test_mestre_confirma_guerreiro_sem_template(
        self, cliente, criar_chave, criar_persona, criar_sessao_de_teste, sessao
    ):
        chave, _ = criar_chave()
        admin = criar_persona(Papel.admin)
        mestre = criar_persona(Papel.mestre, criada_por=admin)
        guerreiro = criar_persona(Papel.guerreiro)
        token_do_mestre, _ = criar_sessao_de_teste(mestre)

        resposta = cliente.post(
            "/v1/sessoes/guerreiro/confirmacao",
            json={"guerreiro_id": str(guerreiro.id)},
            headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token_do_mestre}"},
        )
        assert resposta.status_code == 201
        assert resposta.json()["papel"] == "guerreiro"

        registro = sessao.query(Sessao).filter_by(persona_id=guerreiro.id).one()
        assert registro.como_autenticou == ComoAutenticou.confirmacao_humana
        assert registro.quem_confirmou == mestre.id

    def test_admin_tambem_confirma(
        self, cliente, criar_chave, criar_persona, criar_sessao_de_teste
    ):
        chave, _ = criar_chave()
        admin = criar_persona(Papel.admin)
        guerreiro = criar_persona(Papel.guerreiro)
        token_do_admin, _ = criar_sessao_de_teste(admin)

        resposta = cliente.post(
            "/v1/sessoes/guerreiro/confirmacao",
            json={"guerreiro_id": str(guerreiro.id)},
            headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token_do_admin}"},
        )
        assert resposta.status_code == 201

    def test_apoiador_nao_confirma(
        self, cliente, criar_chave, criar_persona, criar_sessao_de_teste
    ):
        chave, _ = criar_chave()
        admin = criar_persona(Papel.admin)
        apoiador = criar_persona(Papel.apoiador, criada_por=admin)
        guerreiro = criar_persona(Papel.guerreiro)
        token_do_apoiador, _ = criar_sessao_de_teste(apoiador)

        resposta = cliente.post(
            "/v1/sessoes/guerreiro/confirmacao",
            json={"guerreiro_id": str(guerreiro.id)},
            headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token_do_apoiador}"},
        )
        assert resposta.status_code == 403

    def test_recusa_da_biometria_nao_fecha_porta_a_confirmacao(
        self,
        cliente,
        criar_chave,
        criar_persona,
        criar_nick,
        criar_template_biometrico,
        criar_sessao_de_teste,
    ):
        """Mesmo com _template_ gravado, a confirmação humana continua uma
        alternativa equivalente — não é exclusiva de quem não tem _template_
        (`RN-01-16`)."""
        chave, _ = criar_chave()
        admin = criar_persona(Papel.admin)
        mestre = criar_persona(Papel.mestre, criada_por=admin)
        guerreiro = _guerreiro_com_nick(criar_persona, criar_nick, nick="Recusou_biometria")
        criar_template_biometrico(guerreiro, descritor=DESCRITOR)
        token_do_mestre, _ = criar_sessao_de_teste(mestre)

        resposta = cliente.post(
            "/v1/sessoes/guerreiro/confirmacao",
            json={"guerreiro_id": str(guerreiro.id)},
            headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token_do_mestre}"},
        )
        assert resposta.status_code == 201

    def test_guerreiro_inexistente_e_recusado(
        self, cliente, criar_chave, criar_persona, criar_sessao_de_teste
    ):
        chave, _ = criar_chave()
        admin = criar_persona(Papel.admin)
        token_do_admin, _ = criar_sessao_de_teste(admin)

        resposta = cliente.post(
            "/v1/sessoes/guerreiro/confirmacao",
            json={"guerreiro_id": "00000000-0000-0000-0000-000000000000"},
            headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token_do_admin}"},
        )
        assert resposta.status_code == 404


class TestFluxoCompletoDoOnboardingSemImagem:
    def test_entra_por_confirmacao_e_depois_passa_a_entrar_sozinho(
        self,
        cliente,
        criar_chave,
        criar_persona,
        criar_nick,
        criar_sessao_de_teste,
        conceder_consentimento_biometrico,
    ):
        """PRD-01 §12: Guerreiro(a) sem _template_ não entra sozinho, entra
        com a confirmação do Mestre; gravado o consentimento e o descritor,
        ele passa a entrar sozinho."""
        chave, _ = criar_chave()
        admin = criar_persona(Papel.admin)
        mestre = criar_persona(Papel.mestre, criada_por=admin)
        token_do_mestre, _ = criar_sessao_de_teste(mestre)
        guerreiro = criar_persona(Papel.guerreiro)
        criar_nick(guerreiro, "Onboarding_sem_imagem")
        responsavel = criar_persona(Papel.responsavel, criada_por=admin)

        primeira_tentativa = cliente.post(
            "/v1/sessoes/guerreiro",
            json={"nick": "Onboarding_sem_imagem", "descritor": DESCRITOR},
            headers={"X-Chave-Aplicacao": chave},
        )
        assert primeira_tentativa.status_code == 401

        confirmacao = cliente.post(
            "/v1/sessoes/guerreiro/confirmacao",
            json={"guerreiro_id": str(guerreiro.id)},
            headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token_do_mestre}"},
        )
        assert confirmacao.status_code == 201

        conceder_consentimento_biometrico(responsavel, guerreiro)
        gravacao = cliente.post(
            f"/v1/guerreiros/{guerreiro.id}/descritor",
            json={"descritor": DESCRITOR},
            headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token_do_mestre}"},
        )
        assert gravacao.status_code == 201

        segunda_tentativa = cliente.post(
            "/v1/sessoes/guerreiro",
            json={"nick": "Onboarding_sem_imagem", "descritor": DESCRITOR},
            headers={"X-Chave-Aplicacao": chave},
        )
        assert segunda_tentativa.status_code == 201


class TestDuasSessoesDeGuerreirosNoMesmoAparelho:
    def test_uma_sessao_nao_alcanca_a_outra_e_expiram_independentemente(
        self, cliente, criar_chave, criar_persona, criar_sessao_de_teste
    ):
        chave, _ = criar_chave()
        primeiro = criar_persona(Papel.guerreiro)
        segundo = criar_persona(Papel.guerreiro)
        token_expirado, _ = criar_sessao_de_teste(
            primeiro,
            como_autenticou=ComoAutenticou.biometria,
            expira_em=datetime.now(UTC) - timedelta(seconds=1),
        )
        token_vigente, _ = criar_sessao_de_teste(segundo, como_autenticou=ComoAutenticou.biometria)

        expirado = cliente.get(
            "/v1/eu",
            headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token_expirado}"},
        )
        assert expirado.status_code == 401

        vigente = cliente.get(
            "/v1/eu",
            headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token_vigente}"},
        )
        assert vigente.status_code == 200
        assert vigente.json()["persona_id"] == str(segundo.id)
