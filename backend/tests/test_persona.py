import pytest

from nucleo.erros import ErroDeValidacao, PermissaoNegada
from nucleo.personas.modelo import Credencial, Nick, Papel, Persona, TipoDeCredencial
from nucleo.personas.regra import criar_persona
from nucleo.personas.semeadura import semear_admin_fundador


def test_papel_ausente_nao_produz_persona(sessao):
    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_persona(sessao, papel=None, criada_por=None)
    assert excinfo.value.campo == "papel"
    assert sessao.query(Persona).count() == 0


def test_guerreiro_tem_autocadastro(sessao, criar_comunidade, criar_aula):
    admin = Persona(papel=Papel.admin)
    sessao.add(admin)
    sessao.flush()
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade)

    persona = criar_persona(
        sessao,
        papel=Papel.guerreiro,
        criada_por=None,
        aula=aula,
        nick="Guerreira_de_teste",
    )
    sessao.commit()
    assert persona.papel == Papel.guerreiro
    assert persona.vinculo_vigente.comunidade_virtual_id == comunidade.id


def test_guerreiro_sem_aula_nao_e_criado(sessao):
    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_persona(sessao, papel=Papel.guerreiro, criada_por=None)
    assert excinfo.value.campo == "aula_id"
    assert sessao.query(Persona).count() == 0


def test_guerreiro_com_comunidade_declarada_e_recusado(sessao, criar_comunidade, criar_aula):
    """A comunidade nunca é parâmetro desta função: só a aula a origina
    (`RF-08-02`) — o parâmetro nem existe mais na assinatura."""
    admin = Persona(papel=Papel.admin)
    sessao.add(admin)
    sessao.flush()
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade)

    with pytest.raises(TypeError):
        criar_persona(
            sessao,
            papel=Papel.guerreiro,
            criada_por=None,
            aula=aula,
            nick="Guerreira_de_teste",
            comunidade_virtual_id=comunidade.id,
        )


def test_guerreiro_sem_nick_nao_e_criado(sessao, criar_comunidade, criar_aula):
    admin = Persona(papel=Papel.admin)
    sessao.add(admin)
    sessao.flush()
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade)

    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_persona(sessao, papel=Papel.guerreiro, criada_por=None, aula=aula)
    assert excinfo.value.campo == "nick"
    assert sessao.query(Persona).filter_by(papel=Papel.guerreiro).count() == 0
    assert sessao.query(Nick).count() == 0


def test_nick_repetido_e_recusado_entre_papeis_diferentes(sessao, criar_comunidade, criar_aula):
    admin = Persona(papel=Papel.admin)
    sessao.add(admin)
    sessao.flush()
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade)

    criar_persona(
        sessao,
        papel=Papel.guerreiro,
        criada_por=None,
        aula=aula,
        nick="MesmoNick",
    )
    sessao.commit()

    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_persona(
            sessao,
            papel=Papel.guerreiro,
            criada_por=None,
            aula=aula,
            nick="MesmoNick",
        )
    assert excinfo.value.campo == "nick"
    assert sessao.query(Persona).filter_by(papel=Papel.guerreiro).count() == 1
    assert sessao.query(Nick).filter_by(valor="MesmoNick").count() == 1


def test_mestre_so_e_cadastrado_por_admin(sessao):
    with pytest.raises(PermissaoNegada):
        criar_persona(sessao, papel=Papel.mestre, criada_por=None)

    apoiador_qualquer = Persona(papel=Papel.apoiador)
    sessao.add(apoiador_qualquer)
    sessao.flush()
    with pytest.raises(PermissaoNegada):
        criar_persona(sessao, papel=Papel.mestre, criada_por=apoiador_qualquer)

    admin = Persona(papel=Papel.admin)
    sessao.add(admin)
    sessao.flush()
    mestre = criar_persona(sessao, papel=Papel.mestre, criada_por=admin)
    assert mestre.papel == Papel.mestre
    assert mestre.criada_por == admin.id


def test_apoiador_so_e_cadastrado_por_admin(sessao):
    admin = Persona(papel=Papel.admin)
    mestre = Persona(papel=Papel.mestre)
    sessao.add_all([admin, mestre])
    sessao.flush()

    with pytest.raises(PermissaoNegada):
        criar_persona(sessao, papel=Papel.apoiador, criada_por=mestre)

    apoiador = criar_persona(sessao, papel=Papel.apoiador, criada_por=admin)
    assert apoiador.papel == Papel.apoiador


def test_responsavel_e_cadastrado_por_admin_ou_mestre(sessao):
    admin = Persona(papel=Papel.admin)
    mestre = Persona(papel=Papel.mestre)
    apoiador = Persona(papel=Papel.apoiador)
    sessao.add_all([admin, mestre, apoiador])
    sessao.flush()

    with pytest.raises(PermissaoNegada):
        criar_persona(sessao, papel=Papel.responsavel, criada_por=apoiador)

    por_admin = criar_persona(sessao, papel=Papel.responsavel, criada_por=admin)
    por_mestre = criar_persona(sessao, papel=Papel.responsavel, criada_por=mestre)
    assert por_admin.papel == Papel.responsavel
    assert por_mestre.papel == Papel.responsavel


def test_admin_novo_exige_admin_existente(sessao):
    mestre = Persona(papel=Papel.mestre)
    sessao.add(mestre)
    sessao.flush()

    with pytest.raises(PermissaoNegada):
        criar_persona(sessao, papel=Papel.admin, criada_por=mestre)
    with pytest.raises(PermissaoNegada):
        criar_persona(sessao, papel=Papel.admin, criada_por=None)

    admin_existente = Persona(papel=Papel.admin)
    sessao.add(admin_existente)
    sessao.flush()
    novo_admin = criar_persona(sessao, papel=Papel.admin, criada_por=admin_existente)
    assert novo_admin.papel == Papel.admin


def test_semeadura_cria_admin_fundador(sessao):
    persona = semear_admin_fundador(sessao, "fundador@example.org")
    assert persona is not None
    assert persona.papel == Papel.admin

    credencial = sessao.query(Persona).count()
    assert credencial == 1


def test_semear_duas_vezes_nao_duplica_a_persona(sessao):
    primeira = semear_admin_fundador(sessao, "fundador@example.org")
    segunda = semear_admin_fundador(sessao, "fundador@example.org")

    assert primeira is not None
    assert segunda is None
    assert sessao.query(Persona).filter_by(papel=Papel.admin).count() == 1


def test_semeadura_nao_cria_persona_de_outro_papel(sessao):
    semear_admin_fundador(sessao, "fundador@example.org")
    papeis = {persona.papel for persona in sessao.query(Persona).all()}
    assert papeis == {Papel.admin}


def test_admin_semeado_tem_credencial_de_login_social(sessao):
    persona = semear_admin_fundador(sessao, "fundador@example.org")
    credencial = sessao.query(Credencial).filter_by(persona_id=persona.id).one()
    assert credencial.tipo == TipoDeCredencial.login_social
    assert credencial.identificador == "fundador@example.org"
    assert credencial.troca_pendente is False
