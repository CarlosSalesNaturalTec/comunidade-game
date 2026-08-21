from datetime import date

import pytest

from nucleo.erros import ErroDeValidacao, PermissaoNegada
from nucleo.personas.modelo import (
    ArtefatoComprobatorio,
    Credencial,
    Nick,
    Papel,
    Persona,
    TipoDeCredencial,
)
from nucleo.personas.regra import (
    cadastrar_adulto_com_artefatos,
    cadastrar_guerreiro_pela_gestao,
    definir_ou_trocar_nick,
    incluir_admin,
)


def test_admin_cadastra_mestre_com_link_comprobatorio(sessao):
    admin = Persona(papel=Papel.admin)
    sessao.add(admin)
    sessao.flush()

    mestre = cadastrar_adulto_com_artefatos(
        sessao,
        papel=Papel.mestre,
        operador=admin,
        nome="Mestre de Tal",
        email="mestre@example.org",
        whatsapp=None,
        nick=None,
        artefatos=[("https://exemplo.org/curriculo", "Currículo")],
    )
    sessao.commit()

    assert mestre.papel == Papel.mestre
    assert mestre.nome == "Mestre de Tal"
    assert mestre.email == "mestre@example.org"
    artefato = sessao.query(ArtefatoComprobatorio).filter_by(persona_id=mestre.id).one()
    assert artefato.endereco == "https://exemplo.org/curriculo"
    assert artefato.rotulo == "Currículo"
    credencial = sessao.query(Credencial).filter_by(persona_id=mestre.id).one()
    assert credencial.tipo == TipoDeCredencial.login_social
    assert credencial.identificador == "mestre@example.org"


def test_cadastro_de_mestre_sem_artefato_e_recusado(sessao):
    admin = Persona(papel=Papel.admin)
    sessao.add(admin)
    sessao.flush()

    with pytest.raises(ErroDeValidacao) as excinfo:
        cadastrar_adulto_com_artefatos(
            sessao,
            papel=Papel.mestre,
            operador=admin,
            nome="Mestre de Tal",
            email="mestre@example.org",
            whatsapp=None,
            nick=None,
            artefatos=[],
        )
    assert excinfo.value.campo == "artefatos"
    assert sessao.query(Persona).filter_by(papel=Papel.mestre).count() == 0


def test_cadastro_de_apoiador_sem_artefato_e_recusado(sessao):
    admin = Persona(papel=Papel.admin)
    sessao.add(admin)
    sessao.flush()

    with pytest.raises(ErroDeValidacao) as excinfo:
        cadastrar_adulto_com_artefatos(
            sessao,
            papel=Papel.apoiador,
            operador=admin,
            nome="Apoiador de Tal",
            email="apoiador@example.org",
            whatsapp=None,
            nick=None,
            artefatos=[],
        )
    assert excinfo.value.campo == "artefatos"
    assert sessao.query(Persona).filter_by(papel=Papel.apoiador).count() == 0


def test_adulto_e_criado_sem_nick(sessao):
    admin = Persona(papel=Papel.admin)
    sessao.add(admin)
    sessao.flush()

    apoiador = cadastrar_adulto_com_artefatos(
        sessao,
        papel=Papel.apoiador,
        operador=admin,
        nome="Apoiador de Tal",
        email="apoiador@example.org",
        whatsapp=None,
        nick=None,
        artefatos=[("https://exemplo.org/doacao", "Termos de doação")],
    )
    sessao.commit()

    assert apoiador.papel == Papel.apoiador
    assert sessao.query(Nick).filter_by(persona_id=apoiador.id).first() is None


def test_apoiador_cadastrado_diretamente_recebe_o_nick_do_admin(sessao):
    admin = Persona(papel=Papel.admin)
    sessao.add(admin)
    sessao.flush()

    apoiador = cadastrar_adulto_com_artefatos(
        sessao,
        papel=Papel.apoiador,
        operador=admin,
        nome="Apoiador de Tal",
        email="apoiador@example.org",
        whatsapp="11999999999",
        nick="ApoiadorNick",
        artefatos=[("https://exemplo.org/doacao", "Termos de doação")],
    )
    sessao.commit()

    assert sessao.query(Nick).filter_by(persona_id=apoiador.id).one().valor == "ApoiadorNick"


def test_admin_inclui_outro_admin(sessao):
    admin = Persona(papel=Papel.admin)
    sessao.add(admin)
    sessao.flush()

    novo_admin = incluir_admin(
        sessao, operador=admin, nome="Admin Nova", email="nova@example.org", whatsapp=None
    )
    sessao.commit()

    assert novo_admin.papel == Papel.admin
    assert novo_admin.criada_por == admin.id
    credencial = sessao.query(Credencial).filter_by(persona_id=novo_admin.id).one()
    assert credencial.tipo == TipoDeCredencial.login_social
    assert credencial.identificador == "nova@example.org"


def test_apoiador_nao_inclui_admin(sessao):
    admin = Persona(papel=Papel.admin)
    sessao.add(admin)
    sessao.flush()
    apoiador = cadastrar_adulto_com_artefatos(
        sessao,
        papel=Papel.apoiador,
        operador=admin,
        nome="Apoiador de Tal",
        email="apoiador@example.org",
        whatsapp=None,
        nick=None,
        artefatos=[("https://exemplo.org/doacao", "Termos de doação")],
    )
    sessao.commit()

    with pytest.raises(PermissaoNegada):
        incluir_admin(
            sessao, operador=apoiador, nome="Outro Admin", email="outro@example.org", whatsapp=None
        )
    assert sessao.query(Persona).filter_by(papel=Papel.admin).count() == 1


# desfecho da colisão: o Admin grava o nick do adulto (RF-02-01, RN-01-30, RN-14-10)


def test_admin_grava_o_nick_de_um_apoiador_que_estava_sem(sessao):
    admin = Persona(papel=Papel.admin)
    sessao.add(admin)
    sessao.flush()
    apoiador = cadastrar_adulto_com_artefatos(
        sessao,
        papel=Papel.apoiador,
        operador=admin,
        nome="Apoiador de Tal",
        email="apoiador@example.org",
        whatsapp=None,
        nick=None,
        artefatos=[("https://exemplo.org/doacao", "Termos de doação")],
    )
    sessao.commit()

    definir_ou_trocar_nick(sessao, apoiador, "NickRecebidoPorFora")
    sessao.commit()

    assert sessao.query(Nick).filter_by(persona_id=apoiador.id).one().valor == "NickRecebidoPorFora"


def test_admin_troca_o_nick_de_um_mestre(sessao):
    admin = Persona(papel=Papel.admin)
    sessao.add(admin)
    sessao.flush()
    mestre = cadastrar_adulto_com_artefatos(
        sessao,
        papel=Papel.mestre,
        operador=admin,
        nome="Mestre de Tal",
        email="mestre@example.org",
        whatsapp=None,
        nick="NickAntigo",
        artefatos=[("https://exemplo.org/curriculo", "Currículo")],
    )
    sessao.commit()

    definir_ou_trocar_nick(sessao, mestre, "NickNovo")
    sessao.commit()

    assert sessao.query(Nick).filter_by(persona_id=mestre.id).one().valor == "NickNovo"


def test_nick_em_uso_e_recusado_tambem_para_o_admin(sessao):
    admin = Persona(papel=Papel.admin)
    sessao.add(admin)
    sessao.flush()
    cadastrar_adulto_com_artefatos(
        sessao,
        papel=Papel.apoiador,
        operador=admin,
        nome="Primeiro",
        email="primeiro@example.org",
        whatsapp=None,
        nick="NickOcupado",
        artefatos=[("https://exemplo.org/doacao", "Termos")],
    )
    mestre_sem_nick = cadastrar_adulto_com_artefatos(
        sessao,
        papel=Papel.mestre,
        operador=admin,
        nome="Segundo",
        email="segundo@example.org",
        whatsapp=None,
        nick=None,
        artefatos=[("https://exemplo.org/curriculo", "Currículo")],
    )
    sessao.commit()

    with pytest.raises(ErroDeValidacao) as excinfo:
        definir_ou_trocar_nick(sessao, mestre_sem_nick, "NickOcupado")
    assert excinfo.value.campo == "nick"
    assert sessao.query(Nick).filter_by(persona_id=mestre_sem_nick.id).first() is None


def test_a_rota_do_admin_nao_alcanca_guerreiro(
    sessao, criar_comunidade, criar_aula, cliente, criar_chave, criar_sessao_de_teste
):
    admin = Persona(papel=Papel.admin)
    sessao.add(admin)
    sessao.flush()
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade)
    guerreiro = cadastrar_guerreiro_pela_gestao(
        sessao,
        operador=admin,
        nome="Zeferina",
        nascimento=date(2015, 3, 20),
        nick="ZeferinaGuerreira",
        avatar="avatar-opaco",
        aula=aula,
    )
    sessao.commit()

    chave, _ = criar_chave()
    token, _ = criar_sessao_de_teste(admin)

    # A checagem de papel é da rota (`personas.rotas.gravar_nick_do_adulto_rota`),
    # não de `definir_ou_trocar_nick` — genérica a qualquer persona
    # (`RF-02-01`, `RN-14-10`).
    resposta = cliente.patch(
        f"/v1/personas/{guerreiro.id}/nick",
        json={"nick": "OutroNick"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 404
    assert sessao.query(Nick).filter_by(persona_id=guerreiro.id).one().valor == "ZeferinaGuerreira"
