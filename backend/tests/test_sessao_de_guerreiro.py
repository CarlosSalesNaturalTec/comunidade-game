from datetime import UTC, datetime, timedelta

from sqlalchemy import event

from nucleo.comunidades.modelo import VinculoJogador
from nucleo.personas.modelo import Papel
from nucleo.personas.regra import buscar_guerreiro_confirmavel_por
from nucleo.sessoes.modelo import ComoAutenticou, Sessao
from tests.conftest import descritor_de_teste

DESCRITOR = descritor_de_teste()


def _guerreiro_com_nick(criar_persona, criar_nick, nick="Guerreiro_da_rota"):
    guerreiro = criar_persona(Papel.guerreiro)
    criar_nick(guerreiro, nick)
    return guerreiro


def _corpo(nick: str, aula_id, descritor=DESCRITOR) -> dict:
    """A entrada por nick e imagem passou a levar a **aula**: é ela que
    determina o ponto de apoio, e com ele o limiar (`RF-01-73`)."""
    return {"nick": nick, "descritor": descritor, "aula_id": str(aula_id)}


class TestAbrirSessaoDeGuerreiro:
    def test_nick_e_descritor_conferem_abre_sessao(
        self,
        cliente,
        criar_chave,
        criar_persona,
        criar_nick,
        criar_template_biometrico,
        montar_cenario_de_entrada,
    ):
        chave, _ = criar_chave()
        guerreiro = _guerreiro_com_nick(criar_persona, criar_nick)
        criar_template_biometrico(guerreiro, descritor=DESCRITOR)
        cenario = montar_cenario_de_entrada(guerreiro)

        resposta = cliente.post(
            "/v1/sessoes/guerreiro",
            json=_corpo("Guerreiro_da_rota", cenario.aula.id),
            headers={"X-Chave-Aplicacao": chave},
        )
        assert resposta.status_code == 201
        corpo = resposta.json()
        assert corpo["papel"] == "guerreiro"
        assert "token" in corpo

    def test_nao_exige_credencial_de_persona(
        self,
        cliente,
        criar_chave,
        criar_persona,
        criar_nick,
        criar_template_biometrico,
        montar_cenario_de_entrada,
    ):
        """`RF-01-04`: pública quanto à persona — sem `Authorization`."""
        chave, _ = criar_chave()
        guerreiro = _guerreiro_com_nick(criar_persona, criar_nick, nick="Sem_authorization")
        criar_template_biometrico(guerreiro, descritor=DESCRITOR)
        cenario = montar_cenario_de_entrada(guerreiro)

        resposta = cliente.post(
            "/v1/sessoes/guerreiro",
            json=_corpo("Sem_authorization", cenario.aula.id),
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

    def test_cinco_recusas_tem_corpo_e_codigo_identicos(
        self,
        cliente,
        criar_chave,
        criar_persona,
        criar_nick,
        criar_template_biometrico,
        montar_cenario_de_entrada,
    ):
        """`RN-01-22`, `RN-01-56`: às três causas de sempre somam-se as duas
        que o limiar por ponto de apoio traz — ponto de apoio sem medição e
        aula que não vale para aquele Guerreiro(a). A resposta é a mesma."""
        chave, _ = criar_chave()
        cabecalhos = {"X-Chave-Aplicacao": chave}
        qualquer_cenario = montar_cenario_de_entrada()

        nick_inexistente = cliente.post(
            "/v1/sessoes/guerreiro",
            json=_corpo("ninguem-existe", qualquer_cenario.aula.id),
            headers=cabecalhos,
        )

        sem_template = _guerreiro_com_nick(criar_persona, criar_nick, nick="Sem_template_rota")
        cenario_sem_template = montar_cenario_de_entrada(sem_template)
        resposta_sem_template = cliente.post(
            "/v1/sessoes/guerreiro",
            json=_corpo("Sem_template_rota", cenario_sem_template.aula.id),
            headers=cabecalhos,
        )

        com_template = _guerreiro_com_nick(criar_persona, criar_nick, nick="Descritor_errado")
        criar_template_biometrico(com_template, descritor=DESCRITOR)
        cenario_errado = montar_cenario_de_entrada(com_template)
        resposta_descritor_errado = cliente.post(
            "/v1/sessoes/guerreiro",
            json=_corpo(
                "Descritor_errado", cenario_errado.aula.id, descritor=descritor_de_teste(9.0)
            ),
            headers=cabecalhos,
        )

        sem_limiar = _guerreiro_com_nick(criar_persona, criar_nick, nick="Ponto_sem_limiar")
        criar_template_biometrico(sem_limiar, descritor=DESCRITOR)
        cenario_sem_limiar = montar_cenario_de_entrada(sem_limiar, limiar=None)
        resposta_sem_limiar = cliente.post(
            "/v1/sessoes/guerreiro",
            json=_corpo("Ponto_sem_limiar", cenario_sem_limiar.aula.id),
            headers=cabecalhos,
        )

        de_outra = _guerreiro_com_nick(criar_persona, criar_nick, nick="Aula_alheia")
        criar_template_biometrico(de_outra, descritor=DESCRITOR)
        montar_cenario_de_entrada(de_outra)
        alheio = montar_cenario_de_entrada()
        resposta_aula_alheia = cliente.post(
            "/v1/sessoes/guerreiro",
            json=_corpo("Aula_alheia", alheio.aula.id),
            headers=cabecalhos,
        )

        respostas = [
            nick_inexistente,
            resposta_sem_template,
            resposta_descritor_errado,
            resposta_sem_limiar,
            resposta_aula_alheia,
        ]
        for resposta in respostas:
            assert resposta.status_code == 401
        corpos = [resposta.json() for resposta in respostas]
        assert all(corpo == corpos[0] for corpo in corpos)
        assert corpos[0]["codigo"] == "autenticacao_biometrica_invalida"

    def test_sem_a_aula_segue_pelo_limiar_da_comunidade(
        self,
        cliente,
        criar_chave,
        criar_persona,
        criar_nick,
        criar_comunidade,
        criar_template_biometrico,
        criar_ponto_de_apoio,
        criar_medicao_do_limiar,
    ):
        """`RN-01-57`: fora do encontro não há aula nem ponto de apoio, e o
        limiar vem da comunidade do vínculo vigente."""
        chave, _ = criar_chave()
        admin = criar_persona(papel=Papel.admin)
        comunidade = criar_comunidade()
        guerreiro = criar_persona(papel=Papel.guerreiro, comunidade=comunidade)
        criar_nick(guerreiro, "zeferina")
        criar_template_biometrico(guerreiro, DESCRITOR)
        ponto = criar_ponto_de_apoio(admin, comunidade)
        criar_medicao_do_limiar(ponto, admin, limiar=8.0)

        resposta = cliente.post(
            "/v1/sessoes/guerreiro",
            json={"nick": "zeferina", "descritor": DESCRITOR},
            headers={"X-Chave-Aplicacao": chave},
        )

        assert resposta.status_code == 201

    def test_sem_a_aula_vale_o_mais_frouxo_da_comunidade(
        self,
        cliente,
        criar_chave,
        criar_persona,
        criar_nick,
        criar_comunidade,
        criar_template_biometrico,
        criar_ponto_de_apoio,
        criar_medicao_do_limiar,
    ):
        """`RN-01-57`: entre os pontos de apoio ativos da comunidade vale o
        maior limiar — o que não tranca a criança fora."""
        chave, _ = criar_chave()
        admin = criar_persona(papel=Papel.admin)
        comunidade = criar_comunidade()
        guerreiro = criar_persona(papel=Papel.guerreiro, comunidade=comunidade)
        criar_nick(guerreiro, "zeferina")
        criar_template_biometrico(guerreiro, descritor_de_teste(0.1))
        apertado = criar_ponto_de_apoio(admin, comunidade, nome="Apertado")
        frouxo = criar_ponto_de_apoio(admin, comunidade, nome="Frouxo")
        criar_medicao_do_limiar(apertado, admin, limiar=0.5)
        criar_medicao_do_limiar(frouxo, admin, limiar=20.0)

        # Distância entre os dois descritores cabe no frouxo e não no apertado.
        resposta = cliente.post(
            "/v1/sessoes/guerreiro",
            json={"nick": "zeferina", "descritor": descritor_de_teste(0.2)},
            headers={"X-Chave-Aplicacao": chave},
        )

        assert resposta.status_code == 201

    def test_sem_a_aula_ponto_de_apoio_inativo_nao_empresta_limiar(
        self,
        cliente,
        criar_chave,
        sessao,
        criar_persona,
        criar_nick,
        criar_comunidade,
        criar_template_biometrico,
        criar_ponto_de_apoio,
        criar_medicao_do_limiar,
    ):
        """`RN-01-57`: espaço que a comunidade encerrou não empresta número."""
        chave, _ = criar_chave()
        admin = criar_persona(papel=Papel.admin)
        comunidade = criar_comunidade()
        guerreiro = criar_persona(papel=Papel.guerreiro, comunidade=comunidade)
        criar_nick(guerreiro, "zeferina")
        criar_template_biometrico(guerreiro, descritor_de_teste(0.1))
        apertado = criar_ponto_de_apoio(admin, comunidade, nome="Apertado")
        desativado = criar_ponto_de_apoio(admin, comunidade, nome="Desativado")
        criar_medicao_do_limiar(apertado, admin, limiar=0.5)
        criar_medicao_do_limiar(desativado, admin, limiar=20.0)
        desativado.ativo = False
        sessao.commit()

        resposta = cliente.post(
            "/v1/sessoes/guerreiro",
            json={"nick": "zeferina", "descritor": descritor_de_teste(0.2)},
            headers={"X-Chave-Aplicacao": chave},
        )

        assert resposta.status_code == 401

    def test_sem_a_aula_e_recusado(
        self,
        cliente,
        criar_chave,
        sessao,
        criar_persona,
        criar_nick,
        criar_comunidade,
        criar_template_biometrico,
    ):
        """`RN-01-57`, `RN-01-56`: sem vínculo vigente, e sem medição alguma na
        comunidade, a recusa é a mesma das demais causas."""
        chave, _ = criar_chave()
        comunidade = criar_comunidade()
        sem_vinculo = criar_persona(papel=Papel.guerreiro)
        # `criar_persona` sempre abre um vínculo; encerrá-lo é o que produz o
        # caso "sem vínculo vigente" do `RN-01-57`.
        sessao.query(VinculoJogador).filter_by(
            guerreiro_id=sem_vinculo.id, data_fim=None
        ).one().data_fim = datetime.now(UTC)
        sessao.commit()
        criar_nick(sem_vinculo, "sem-vinculo")
        criar_template_biometrico(sem_vinculo, DESCRITOR)
        com_vinculo = criar_persona(papel=Papel.guerreiro, comunidade=comunidade)
        criar_nick(com_vinculo, "sem-medicao")
        criar_template_biometrico(com_vinculo, DESCRITOR)

        corpos = []
        for nick in ("sem-vinculo", "sem-medicao", "inexistente"):
            resposta = cliente.post(
                "/v1/sessoes/guerreiro",
                json={"nick": nick, "descritor": DESCRITOR},
                headers={"X-Chave-Aplicacao": chave},
            )
            assert resposta.status_code == 401
            corpos.append(resposta.json())

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
        montar_cenario_de_entrada,
    ):
        chave, _ = criar_chave()
        guerreiro = _guerreiro_com_nick(criar_persona, criar_nick, nick="Duracao_guerreiro")
        cenario = montar_cenario_de_entrada(guerreiro)
        criar_template_biometrico(guerreiro, descritor=DESCRITOR)

        antes = datetime.now(UTC)
        resposta = cliente.post(
            "/v1/sessoes/guerreiro",
            json=_corpo("Duracao_guerreiro", cenario.aula.id),
            headers={"X-Chave-Aplicacao": chave},
        )
        expira_em = datetime.fromisoformat(resposta.json()["expira_em"])

        assert configuracao.sessao_guerreiro_duracao != configuracao.sessao_adulto_duracao
        diferenca = expira_em - antes
        assert abs(diferenca - configuracao.sessao_guerreiro_duracao) < timedelta(seconds=5)

    def test_registro_de_sessao_guarda_como_autenticou_biometria(
        self,
        cliente,
        criar_chave,
        criar_persona,
        criar_nick,
        criar_template_biometrico,
        sessao,
        montar_cenario_de_entrada,
    ):
        chave, _ = criar_chave()
        guerreiro = _guerreiro_com_nick(criar_persona, criar_nick, nick="Como_autenticou_bio")
        cenario = montar_cenario_de_entrada(guerreiro)
        criar_template_biometrico(guerreiro, descritor=DESCRITOR)

        cliente.post(
            "/v1/sessoes/guerreiro",
            json=_corpo("Como_autenticou_bio", cenario.aula.id),
            headers={"X-Chave-Aplicacao": chave},
        )

        registro = sessao.query(Sessao).filter_by(persona_id=guerreiro.id).one()
        assert registro.como_autenticou == ComoAutenticou.biometria


class TestConfirmacaoDeSessaoDeGuerreiro:
    def test_mestre_confirma_guerreiro_sem_template(
        self, cliente, criar_chave, criar_persona, criar_nick, criar_sessao_de_teste, sessao
    ):
        chave, _ = criar_chave()
        admin = criar_persona(Papel.admin)
        mestre = criar_persona(Papel.mestre, criada_por=admin)
        guerreiro = _guerreiro_com_nick(criar_persona, criar_nick, nick="Sem_template")
        token_do_mestre, _ = criar_sessao_de_teste(mestre)

        resposta = cliente.post(
            "/v1/sessoes/guerreiro/confirmacao",
            json={"nick": "Sem_template"},
            headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token_do_mestre}"},
        )
        assert resposta.status_code == 201
        assert resposta.json()["papel"] == "guerreiro"

        registro = sessao.query(Sessao).filter_by(persona_id=guerreiro.id).one()
        assert registro.como_autenticou == ComoAutenticou.confirmacao_humana
        assert registro.quem_confirmou == mestre.id

    def test_admin_tambem_confirma(
        self, cliente, criar_chave, criar_persona, criar_nick, criar_sessao_de_teste
    ):
        chave, _ = criar_chave()
        admin = criar_persona(Papel.admin)
        _guerreiro_com_nick(criar_persona, criar_nick, nick="Confirmado_pelo_admin")
        token_do_admin, _ = criar_sessao_de_teste(admin)

        resposta = cliente.post(
            "/v1/sessoes/guerreiro/confirmacao",
            json={"nick": "Confirmado_pelo_admin"},
            headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token_do_admin}"},
        )
        assert resposta.status_code == 201

    def test_apoiador_nao_confirma(
        self, cliente, criar_chave, criar_persona, criar_nick, criar_sessao_de_teste
    ):
        chave, _ = criar_chave()
        admin = criar_persona(Papel.admin)
        apoiador = criar_persona(Papel.apoiador, criada_por=admin)
        _guerreiro_com_nick(criar_persona, criar_nick, nick="Nao_confirmado_por_apoiador")
        token_do_apoiador, _ = criar_sessao_de_teste(apoiador)

        resposta = cliente.post(
            "/v1/sessoes/guerreiro/confirmacao",
            json={"nick": "Nao_confirmado_por_apoiador"},
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
            json={"nick": "Recusou_biometria"},
            headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token_do_mestre}"},
        )
        assert resposta.status_code == 201

    def test_nick_inexistente_e_recusado_sem_revelar_o_motivo(
        self, cliente, criar_chave, criar_persona, criar_sessao_de_teste
    ):
        chave, _ = criar_chave()
        admin = criar_persona(Papel.admin)
        token_do_admin, _ = criar_sessao_de_teste(admin)

        resposta = cliente.post(
            "/v1/sessoes/guerreiro/confirmacao",
            json={"nick": "nick_que_nao_existe"},
            headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token_do_admin}"},
        )
        assert resposta.status_code == 401
        assert resposta.json()["codigo"] == "confirmacao_de_guerreiro_recusada"

    def test_nick_de_quem_nao_e_guerreiro_e_recusado_da_mesma_forma(
        self, cliente, criar_chave, criar_persona, criar_nick, criar_sessao_de_teste
    ):
        """A recusa não distingue nick inexistente de nick de outro papel —
        é o mesmo código e a mesma mensagem dos dois casos (`RN-01-22`)."""
        chave, _ = criar_chave()
        admin = criar_persona(Papel.admin)
        mestre_com_nick = criar_persona(Papel.mestre, criada_por=admin)
        criar_nick(mestre_com_nick, "nick_de_mestre")
        token_do_admin, _ = criar_sessao_de_teste(admin)

        resposta = cliente.post(
            "/v1/sessoes/guerreiro/confirmacao",
            json={"nick": "nick_de_mestre"},
            headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token_do_admin}"},
        )
        assert resposta.status_code == 401
        assert resposta.json()["codigo"] == "confirmacao_de_guerreiro_recusada"

    def test_responsavel_confirma_quem_esta_sob_a_responsabilidade_dele(
        self,
        cliente,
        criar_chave,
        criar_persona,
        criar_nick,
        criar_vinculo,
        criar_sessao_de_teste,
        sessao,
    ):
        """`RF-01-74`: em casa quem está na sala é o responsável, e é ele quem
        abre a sessão da criança."""
        chave, _ = criar_chave()
        admin = criar_persona(Papel.admin)
        responsavel = criar_persona(Papel.responsavel, criada_por=admin)
        guerreiro = _guerreiro_com_nick(criar_persona, criar_nick, nick="Zeferina")
        criar_vinculo(responsavel, guerreiro, cadastrado_por=admin)
        token, _ = criar_sessao_de_teste(responsavel)

        resposta = cliente.post(
            "/v1/sessoes/guerreiro/confirmacao",
            json={"nick": "Zeferina"},
            headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
        )

        assert resposta.status_code == 201
        assert resposta.json()["papel"] == "guerreiro"
        registro = sessao.query(Sessao).filter_by(persona_id=guerreiro.id).one()
        assert registro.como_autenticou == ComoAutenticou.confirmacao_humana
        assert registro.quem_confirmou == responsavel.id

    def test_responsavel_nao_confirma_crianca_alheia_nem_denuncia_que_ela_existe(
        self,
        cliente,
        criar_chave,
        criar_persona,
        criar_nick,
        criar_vinculo,
        criar_sessao_de_teste,
    ):
        """`RN-01-58`, `RN-01-22`: a recusa por criança fora da sua
        responsabilidade é a mesma da recusa por nick inexistente — senão o
        responsável ganha um oráculo para sondar quais nicks existem."""
        chave, _ = criar_chave()
        admin = criar_persona(Papel.admin)
        responsavel = criar_persona(Papel.responsavel, criada_por=admin)
        seu_guerreiro = _guerreiro_com_nick(criar_persona, criar_nick, nick="Filha")
        criar_vinculo(responsavel, seu_guerreiro, cadastrado_por=admin)
        _guerreiro_com_nick(criar_persona, criar_nick, nick="Alheia")
        token, _ = criar_sessao_de_teste(responsavel)

        corpos = []
        for nick in ("Alheia", "nick_que_nao_existe"):
            resposta = cliente.post(
                "/v1/sessoes/guerreiro/confirmacao",
                json={"nick": nick},
                headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
            )
            assert resposta.status_code == 401
            corpos.append(resposta.json())

        assert corpos[0] == corpos[1]
        assert corpos[0]["codigo"] == "confirmacao_de_guerreiro_recusada"

    def test_vinculo_de_responsavel_encerrado_nao_confirma_mais(
        self,
        cliente,
        criar_chave,
        criar_persona,
        criar_nick,
        criar_vinculo,
        criar_sessao_de_teste,
    ):
        """`RF-01-74`: o escopo é do vínculo **vigente**."""
        chave, _ = criar_chave()
        admin = criar_persona(Papel.admin)
        responsavel = criar_persona(Papel.responsavel, criada_por=admin)
        guerreiro = _guerreiro_com_nick(criar_persona, criar_nick, nick="Zeferina")
        criar_vinculo(responsavel, guerreiro, cadastrado_por=admin, fim=datetime.now(UTC))
        token, _ = criar_sessao_de_teste(responsavel)

        resposta = cliente.post(
            "/v1/sessoes/guerreiro/confirmacao",
            json={"nick": "Zeferina"},
            headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
        )

        assert resposta.status_code == 401
        assert resposta.json()["codigo"] == "confirmacao_de_guerreiro_recusada"

    def test_mestre_segue_confirmando_qualquer_guerreiro(
        self, cliente, criar_chave, criar_persona, criar_nick, criar_sessao_de_teste
    ):
        """`RF-01-06`: o escopo novo é do responsável, e NÃO estreita a
        autoridade do Mestre, que é a do encontro."""
        chave, _ = criar_chave()
        admin = criar_persona(Papel.admin)
        mestre = criar_persona(Papel.mestre, criada_por=admin)
        _guerreiro_com_nick(criar_persona, criar_nick, nick="Sem_vinculo_com_o_mestre")
        token, _ = criar_sessao_de_teste(mestre)

        resposta = cliente.post(
            "/v1/sessoes/guerreiro/confirmacao",
            json={"nick": "Sem_vinculo_com_o_mestre"},
            headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
        )

        assert resposta.status_code == 201

    def test_apoiador_nao_confirma_crianca(
        self, cliente, criar_chave, criar_persona, criar_nick, criar_sessao_de_teste
    ):
        """`RF-01-16`: papel fora da matriz recebe 403, não 401 — não é recusa
        de nick, é falta de permissão."""
        chave, _ = criar_chave()
        admin = criar_persona(Papel.admin)
        apoiador = criar_persona(Papel.apoiador, criada_por=admin)
        _guerreiro_com_nick(criar_persona, criar_nick, nick="Zeferina")
        token, _ = criar_sessao_de_teste(apoiador)

        resposta = cliente.post(
            "/v1/sessoes/guerreiro/confirmacao",
            json={"nick": "Zeferina"},
            headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
        )

        assert resposta.status_code == 403

    def test_a_recusa_por_escopo_custa_o_mesmo_que_a_por_nick_inexistente(
        self,
        cliente,
        criar_chave,
        sessao,
        criar_persona,
        criar_nick,
        criar_vinculo,
        criar_sessao_de_teste,
    ):
        """`RN-01-58`, `RN-01-22`: a indistinguibilidade alcança o tempo. Se a
        recusa por criança alheia custasse uma consulta a mais que a por nick
        inexistente, o relógio entregaria quais nicks existem."""
        admin = criar_persona(Papel.admin)
        responsavel = criar_persona(Papel.responsavel, criada_por=admin)
        seu = _guerreiro_com_nick(criar_persona, criar_nick, nick="Filha")
        criar_vinculo(responsavel, seu, cadastrado_por=admin)
        _guerreiro_com_nick(criar_persona, criar_nick, nick="Alheia")

        def _contar(nick: str) -> int:
            consultas: list[int] = []
            conexao = sessao.connection()

            def _registrar(*_a, **_k):
                consultas.append(1)

            event.listen(conexao.engine, "before_cursor_execute", _registrar)
            try:
                buscar_guerreiro_confirmavel_por(sessao, nick=nick, quem_confirma=responsavel)
            finally:
                event.remove(conexao.engine, "before_cursor_execute", _registrar)
            return len(consultas)

        contagens = [_contar("Alheia"), _contar("nick_que_nao_existe")]

        assert contagens[0] == contagens[1], contagens

    def test_o_escopo_nao_depende_da_aplicacao_que_chamou(
        self,
        cliente,
        criar_chave,
        criar_persona,
        criar_nick,
        criar_vinculo,
        criar_sessao_de_teste,
    ):
        """`RF-01-16`: a conferência é sobre a persona em sessão e o vínculo
        dela, nunca sobre qual aplicação fez a chamada."""
        admin = criar_persona(Papel.admin)
        responsavel = criar_persona(Papel.responsavel, criada_por=admin)
        _guerreiro_com_nick(criar_persona, criar_nick, nick="Alheia")
        token, _ = criar_sessao_de_teste(responsavel)
        # Duas aplicações distintas do projeto: é o que torna a pergunta
        # "o escopo muda com quem chamou?" verificável.
        chave_a, _ = criar_chave(aplicacao="app-01-aula-presencial")
        chave_b, _ = criar_chave(aplicacao="app-05-guerreiro")

        respostas = [
            cliente.post(
                "/v1/sessoes/guerreiro/confirmacao",
                json={"nick": "Alheia"},
                headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
            )
            for chave in (chave_a, chave_b)
        ]

        assert [r.status_code for r in respostas] == [401, 401]
        assert respostas[0].json() == respostas[1].json()

    def test_confirmacao_nao_aceita_identificador_de_persona(
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
        assert resposta.status_code == 422


class TestFluxoCompletoDoOnboardingSemImagem:
    def test_entra_por_confirmacao_e_depois_passa_a_entrar_sozinho(
        self,
        cliente,
        criar_chave,
        criar_persona,
        criar_nick,
        criar_sessao_de_teste,
        conceder_consentimento_biometrico,
        montar_cenario_de_entrada,
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
        cenario = montar_cenario_de_entrada(guerreiro)
        responsavel = criar_persona(Papel.responsavel, criada_por=admin)

        primeira_tentativa = cliente.post(
            "/v1/sessoes/guerreiro",
            json=_corpo("Onboarding_sem_imagem", cenario.aula.id),
            headers={"X-Chave-Aplicacao": chave},
        )
        assert primeira_tentativa.status_code == 401

        confirmacao = cliente.post(
            "/v1/sessoes/guerreiro/confirmacao",
            json={"nick": "Onboarding_sem_imagem"},
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
            json=_corpo("Onboarding_sem_imagem", cenario.aula.id),
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
