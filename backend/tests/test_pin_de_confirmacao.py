"""PIN de confirmação do adulto no encontro — cadastro, verificador, conferência
e bloqueio (`RF-01-75`, `RN-01-59`, `RN-04-37`, `RN-04-38`), a confirmação do
Guerreiro(a) pelo App 01 (`RF-01-06`) e a presença sem rede (`RF-04-23`)."""

from datetime import UTC, datetime

import pytest

from nucleo.auditoria.modelo import Auditoria
from nucleo.aulas.modelo import ModoDeComprovacao, Presenca
from nucleo.configuracao import Configuracao
from nucleo.personas.modelo import Papel, Persona
from nucleo.pin_de_confirmacao.regra import gerar_verificador
from nucleo.sessoes.modelo import Sessao

APP_01 = "app-01-aula-presencial"
PIN = "4821"
MOMENTO_DO_FATO = datetime(2026, 9, 23, 14, 0, tzinfo=UTC)


def _cabecalhos(chave: str, token: str) -> dict:
    return {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}


@pytest.fixture
def com_pin(sessao, configuracao):
    def _gravar(persona: Persona, pin: str = PIN) -> Persona:
        persona.pin_verificador = gerar_verificador(pin, configuracao)
        sessao.commit()
        return persona

    return _gravar


class TestCadastroDoPin:
    def test_mestre_cadastra_e_a_resposta_nao_traz_o_pin(
        self, cliente, criar_chave, criar_persona, criar_sessao_de_teste, sessao
    ):
        chave, _ = criar_chave("app-09-mestre")
        mestre = criar_persona(Papel.mestre)
        token, _ = criar_sessao_de_teste(mestre)

        resposta = cliente.put(
            "/v1/eu/pin-de-confirmacao", json={"pin": PIN}, headers=_cabecalhos(chave, token)
        )

        assert resposta.status_code == 204
        assert resposta.content == b""
        sessao.refresh(mestre)
        verificador = mestre.pin_verificador
        assert set(verificador) == {"algoritmo", "iteracoes", "sal", "resumo"}
        assert PIN not in str(verificador)

    def test_troca_nao_pede_o_antigo_e_o_antigo_deixa_de_conferir(
        self, cliente, criar_chave, criar_persona, criar_sessao_de_teste, com_pin, sessao
    ):
        chave, _ = criar_chave("app-03-gestao")
        admin = com_pin(criar_persona(Papel.admin))
        antigo = dict(admin.pin_verificador)
        token, _ = criar_sessao_de_teste(admin)

        resposta = cliente.put(
            "/v1/eu/pin-de-confirmacao", json={"pin": "0007"}, headers=_cabecalhos(chave, token)
        )

        assert resposta.status_code == 204
        sessao.refresh(admin)
        assert admin.pin_verificador != antigo

    @pytest.mark.parametrize("pin", ["123", "12345", "12a4", ""])
    def test_pin_fora_do_formato_e_recusado(
        self, cliente, criar_chave, criar_persona, criar_sessao_de_teste, sessao, pin
    ):
        chave, _ = criar_chave("app-09-mestre")
        mestre = criar_persona(Papel.mestre)
        token, _ = criar_sessao_de_teste(mestre)

        resposta = cliente.put(
            "/v1/eu/pin-de-confirmacao", json={"pin": pin}, headers=_cabecalhos(chave, token)
        )

        assert resposta.status_code == 422
        sessao.refresh(mestre)
        assert mestre.pin_verificador is None

    @pytest.mark.parametrize("papel", [Papel.apoiador, Papel.responsavel, Papel.guerreiro])
    def test_quem_nao_e_mestre_nem_admin_nao_cadastra(
        self, cliente, criar_chave, criar_persona, criar_sessao_de_teste, papel
    ):
        chave, _ = criar_chave("app-09-mestre")
        persona = criar_persona(papel)
        token, _ = criar_sessao_de_teste(persona)

        resposta = cliente.put(
            "/v1/eu/pin-de-confirmacao", json={"pin": PIN}, headers=_cabecalhos(chave, token)
        )

        assert resposta.status_code == 403

    def test_o_pin_nao_chega_a_auditoria(
        self,
        cliente,
        criar_chave,
        criar_persona,
        criar_sessao_de_teste,
        sessao,
        monkeypatch,
        fabrica_de_auditoria,
    ):
        monkeypatch.setattr(
            "nucleo.auditoria.middleware.obter_fabrica_de_sessao", lambda: fabrica_de_auditoria
        )
        chave, _ = criar_chave("app-09-mestre")
        mestre = criar_persona(Papel.mestre)
        token, _ = criar_sessao_de_teste(mestre)

        cliente.put(
            "/v1/eu/pin-de-confirmacao", json={"pin": PIN}, headers=_cabecalhos(chave, token)
        )

        for registro in sessao.query(Auditoria).all():
            assert PIN not in str(vars(registro))

    def test_eu_diz_se_ha_pin_sem_mostra_lo(
        self, cliente, criar_chave, criar_persona, criar_sessao_de_teste, com_pin
    ):
        chave, _ = criar_chave("app-09-mestre")
        sem_pin = criar_persona(Papel.mestre)
        com = com_pin(criar_persona(Papel.mestre))
        apoiador = criar_persona(Papel.apoiador)

        def _eu(persona):
            token, _ = criar_sessao_de_teste(persona)
            return cliente.get("/v1/eu", headers=_cabecalhos(chave, token)).json()

        assert _eu(sem_pin)["tem_pin_de_confirmacao"] is False
        assert _eu(com)["tem_pin_de_confirmacao"] is True
        assert "tem_pin_de_confirmacao" not in _eu(apoiador)


class TestVerificador:
    def test_app_01_recebe_o_verificador_de_quem_abriu(
        self, cliente, criar_chave, criar_persona, criar_sessao_de_teste, com_pin
    ):
        chave, _ = criar_chave(APP_01)
        mestre = com_pin(criar_persona(Papel.mestre))
        token, _ = criar_sessao_de_teste(mestre, origem=APP_01)

        resposta = cliente.get(
            "/v1/eu/pin-de-confirmacao/verificador", headers=_cabecalhos(chave, token)
        )

        assert resposta.status_code == 200
        assert resposta.json() == mestre.pin_verificador
        assert PIN not in resposta.text

    def test_outra_aplicacao_nao_recebe(
        self, cliente, criar_chave, criar_persona, criar_sessao_de_teste, com_pin
    ):
        chave, _ = criar_chave("app-09-mestre")
        mestre = com_pin(criar_persona(Papel.mestre))
        token, _ = criar_sessao_de_teste(mestre)

        resposta = cliente.get(
            "/v1/eu/pin-de-confirmacao/verificador", headers=_cabecalhos(chave, token)
        )

        assert resposta.status_code == 403

    def test_sem_pin_cadastrado_a_resposta_diz_isso(
        self, cliente, criar_chave, criar_persona, criar_sessao_de_teste
    ):
        chave, _ = criar_chave(APP_01)
        admin = criar_persona(Papel.admin)
        token, _ = criar_sessao_de_teste(admin, origem=APP_01)

        resposta = cliente.get(
            "/v1/eu/pin-de-confirmacao/verificador", headers=_cabecalhos(chave, token)
        )

        assert resposta.status_code == 403
        assert resposta.json()["codigo"] == "pin_nao_cadastrado"


def _confirmar(cliente, chave, token, nick, pin=PIN):
    corpo = {"nick": nick}
    if pin is not None:
        corpo["pin"] = pin
    return cliente.post(
        "/v1/sessoes/guerreiro/confirmacao", json=corpo, headers=_cabecalhos(chave, token)
    )


class TestConfirmacaoPeloApp01:
    def test_mestre_confirma_com_o_pin_certo(
        self,
        cliente,
        criar_chave,
        criar_persona,
        criar_nick,
        criar_sessao_de_teste,
        com_pin,
        sessao,
    ):
        chave, _ = criar_chave(APP_01)
        mestre = com_pin(criar_persona(Papel.mestre))
        guerreiro = criar_persona(Papel.guerreiro)
        criar_nick(guerreiro, "Com_pin")
        token, _ = criar_sessao_de_teste(mestre, origem=APP_01)

        resposta = _confirmar(cliente, chave, token, "Com_pin")

        assert resposta.status_code == 201
        registro = sessao.query(Sessao).filter_by(persona_id=guerreiro.id).one()
        assert registro.quem_confirmou == mestre.id

    def test_sem_pin_no_corpo_nao_ha_confirmacao(
        self,
        cliente,
        criar_chave,
        criar_persona,
        criar_nick,
        criar_sessao_de_teste,
        com_pin,
        sessao,
    ):
        chave, _ = criar_chave(APP_01)
        mestre = com_pin(criar_persona(Papel.mestre))
        guerreiro = criar_persona(Papel.guerreiro)
        criar_nick(guerreiro, "Sem_pin_no_corpo")
        token, _ = criar_sessao_de_teste(mestre, origem=APP_01)

        resposta = _confirmar(cliente, chave, token, "Sem_pin_no_corpo", pin=None)

        assert resposta.status_code == 422
        assert sessao.query(Sessao).filter_by(persona_id=guerreiro.id).count() == 0

    def test_pin_errado_e_recusado_antes_do_nick(
        self,
        cliente,
        criar_chave,
        criar_persona,
        criar_nick,
        criar_sessao_de_teste,
        com_pin,
        sessao,
    ):
        chave, _ = criar_chave(APP_01)
        mestre = com_pin(criar_persona(Papel.mestre))
        guerreiro = criar_persona(Papel.guerreiro)
        criar_nick(guerreiro, "Existe_mesmo")
        token, _ = criar_sessao_de_teste(mestre, origem=APP_01)

        existente = _confirmar(cliente, chave, token, "Existe_mesmo", pin="0000")
        inexistente = _confirmar(cliente, chave, token, "Nao_existe_nunca", pin="0000")

        assert existente.status_code == inexistente.status_code == 401
        assert existente.json() == inexistente.json()
        assert existente.json()["codigo"] == "pin_recusado"
        assert sessao.query(Sessao).filter_by(persona_id=guerreiro.id).count() == 0

    def test_sem_pin_cadastrado_nao_confirma(
        self, cliente, criar_chave, criar_persona, criar_nick, criar_sessao_de_teste
    ):
        chave, _ = criar_chave(APP_01)
        admin = criar_persona(Papel.admin)
        guerreiro = criar_persona(Papel.guerreiro)
        criar_nick(guerreiro, "Admin_sem_pin")
        token, _ = criar_sessao_de_teste(admin, origem=APP_01)

        resposta = _confirmar(cliente, chave, token, "Admin_sem_pin")

        assert resposta.status_code == 403
        assert resposta.json()["codigo"] == "pin_nao_cadastrado"

    def test_nick_recusado_nao_conta_para_o_bloqueio(
        self, cliente, criar_chave, criar_persona, criar_sessao_de_teste, com_pin
    ):
        chave, _ = criar_chave(APP_01)
        mestre = com_pin(criar_persona(Papel.mestre))
        token, registro = criar_sessao_de_teste(mestre, origem=APP_01)

        for _ in range(6):
            assert _confirmar(cliente, chave, token, "Ninguem_aqui").status_code == 401

        assert registro.erros_de_pin_seguidos == 0

    def test_app_05_segue_sem_pin(
        self,
        cliente,
        criar_chave,
        criar_persona,
        criar_nick,
        criar_sessao_de_teste,
        criar_vinculo,
    ):
        chave, _ = criar_chave("app-05-guerreiro")
        responsavel = criar_persona(Papel.responsavel)
        guerreiro = criar_persona(Papel.guerreiro)
        criar_nick(guerreiro, "Em_casa")
        criar_vinculo(responsavel, guerreiro)
        token, _ = criar_sessao_de_teste(responsavel, origem="app-05-guerreiro")

        resposta = _confirmar(cliente, chave, token, "Em_casa", pin=None)

        assert resposta.status_code == 201


class TestBloqueio:
    def test_o_quinto_erro_bloqueia_mesmo_com_o_pin_certo(
        self,
        cliente,
        criar_chave,
        criar_persona,
        criar_nick,
        criar_sessao_de_teste,
        com_pin,
    ):
        chave, _ = criar_chave(APP_01)
        mestre = com_pin(criar_persona(Papel.mestre))
        criar_nick(criar_persona(Papel.guerreiro), "Bloqueio")
        token, _ = criar_sessao_de_teste(mestre, origem=APP_01)

        codigos = [
            _confirmar(cliente, chave, token, "Bloqueio", pin="0000").json()["codigo"]
            for _ in range(5)
        ]
        assert codigos == ["pin_recusado"] * 4 + ["pin_bloqueado"]

        certo = _confirmar(cliente, chave, token, "Bloqueio")
        assert certo.status_code == 403
        assert certo.json()["codigo"] == "pin_bloqueado"

    def test_o_acerto_zera_a_contagem(
        self,
        cliente,
        criar_chave,
        criar_persona,
        criar_nick,
        criar_sessao_de_teste,
        com_pin,
    ):
        chave, _ = criar_chave(APP_01)
        mestre = com_pin(criar_persona(Papel.mestre))
        criar_nick(criar_persona(Papel.guerreiro), "Zera")
        token, _ = criar_sessao_de_teste(mestre, origem=APP_01)

        for _ in range(4):
            _confirmar(cliente, chave, token, "Zera", pin="0000")
        assert _confirmar(cliente, chave, token, "Zera").status_code == 201
        for _ in range(4):
            _confirmar(cliente, chave, token, "Zera", pin="0000")

        assert _confirmar(cliente, chave, token, "Zera").status_code == 201

    def test_nova_sessao_desbloqueia_e_outro_aparelho_nao_herda(
        self,
        cliente,
        criar_chave,
        criar_persona,
        criar_nick,
        criar_sessao_de_teste,
        com_pin,
    ):
        chave, _ = criar_chave(APP_01)
        mestre = com_pin(criar_persona(Papel.mestre))
        criar_nick(criar_persona(Papel.guerreiro), "Outro_aparelho")
        bloqueada, _ = criar_sessao_de_teste(mestre, origem=APP_01)
        outra, _ = criar_sessao_de_teste(mestre, origem=APP_01)

        for _ in range(5):
            _confirmar(cliente, chave, bloqueada, "Outro_aparelho", pin="0000")

        assert _confirmar(cliente, chave, bloqueada, "Outro_aparelho").status_code == 403
        assert _confirmar(cliente, chave, outra, "Outro_aparelho").status_code == 201


def _sem_rede(cliente, chave, token, aula_id, nick):
    return cliente.post(
        f"/v1/aulas/{aula_id}/presencas/sem-rede",
        json={"nick": nick, "momento_do_fato": MOMENTO_DO_FATO.isoformat()},
        headers=_cabecalhos(chave, token),
    )


class TestPresencaSemRede:
    @pytest.fixture
    def encontro(
        self,
        criar_chave,
        criar_persona,
        criar_sessao_de_teste,
        criar_comunidade,
        criar_aula,
        criar_vinculo_jogador,
        criar_nick,
        com_pin,
    ):
        chave, _ = criar_chave(APP_01)
        mestre = com_pin(criar_persona(Papel.mestre))
        comunidade = criar_comunidade()
        criar_vinculo_jogador(mestre, comunidade)
        guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
        criar_nick(guerreiro, "Chegou_sem_rede")
        aula = criar_aula(mestre, comunidade)
        token, _ = criar_sessao_de_teste(mestre, origem=APP_01)
        return chave, token, mestre, guerreiro, aula

    def test_grava_com_quem_confirmou_e_a_hora_do_fato_sem_abrir_sessao(
        self, cliente, encontro, sessao
    ):
        chave, token, mestre, guerreiro, aula = encontro

        resposta = _sem_rede(cliente, chave, token, aula.id, "Chegou_sem_rede")

        assert resposta.status_code == 201
        presenca = sessao.query(Presenca).filter_by(guerreiro_id=guerreiro.id).one()
        assert presenca.modo == ModoDeComprovacao.confirmacao
        assert presenca.confirmador_id == mestre.id
        assert presenca.momento_do_fato == MOMENTO_DO_FATO
        assert sessao.query(Sessao).filter_by(persona_id=guerreiro.id).count() == 0

    def test_reenvio_nao_duplica(self, cliente, encontro, sessao):
        chave, token, _, guerreiro, aula = encontro

        primeira = _sem_rede(cliente, chave, token, aula.id, "Chegou_sem_rede")
        segunda = _sem_rede(cliente, chave, token, aula.id, "Chegou_sem_rede")

        assert primeira.status_code == segunda.status_code == 201
        assert primeira.json()["id"] == segunda.json()["id"]
        assert sessao.query(Presenca).filter_by(guerreiro_id=guerreiro.id).count() == 1

    def test_nick_que_nao_resolve_e_indistinguivel(
        self, cliente, encontro, criar_persona, criar_nick
    ):
        chave, token, _, _, aula = encontro
        criar_nick(criar_persona(Papel.mestre), "Nick_de_mestre")

        inexistente = _sem_rede(cliente, chave, token, aula.id, "Ninguem_com_esse")
        de_mestre = _sem_rede(cliente, chave, token, aula.id, "Nick_de_mestre")

        assert inexistente.status_code == de_mestre.status_code == 401
        assert inexistente.json() == de_mestre.json()

    def test_so_o_app_01_sincroniza(self, cliente, encontro, criar_chave, sessao):
        _, token, _, _, aula = encontro
        outra, _ = criar_chave("app-03-gestao")

        resposta = _sem_rede(cliente, outra, token, aula.id, "Chegou_sem_rede")

        assert resposta.status_code == 403
        assert sessao.query(Presenca).count() == 0

    def test_sem_pin_cadastrado_nao_sincroniza(self, cliente, encontro, sessao):
        chave, token, mestre, _, aula = encontro
        mestre.pin_verificador = None
        sessao.commit()

        resposta = _sem_rede(cliente, chave, token, aula.id, "Chegou_sem_rede")

        assert resposta.status_code == 403
        assert resposta.json()["codigo"] == "pin_nao_cadastrado"
        assert sessao.query(Presenca).count() == 0


def test_a_derivacao_usa_as_iteracoes_gravadas(configuracao: Configuracao):
    verificador = gerar_verificador(PIN, configuracao)
    assert verificador["algoritmo"] == "PBKDF2-SHA256"
    assert verificador["iteracoes"] == configuracao.pin_iteracoes
