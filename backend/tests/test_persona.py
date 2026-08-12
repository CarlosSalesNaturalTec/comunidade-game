import pytest

from nucleo.erros import ErroDeValidacao, PermissaoNegada
from nucleo.personas.modelo import Credencial, Nick, Papel, Persona, TipoDeCredencial
from nucleo.personas.regra import criar_persona, vincular_guerreiro_a_comunidade
from nucleo.personas.semeadura import semear_admin_fundador


def test_papel_ausente_nao_produz_persona(sessao):
    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_persona(sessao, papel=None, criada_por=None)
    assert excinfo.value.campo == "papel"
    assert sessao.query(Persona).count() == 0


def test_guerreiro_tem_autocadastro(sessao, criar_comunidade):
    comunidade = criar_comunidade()
    persona = criar_persona(
        sessao,
        papel=Papel.guerreiro,
        criada_por=None,
        comunidade_virtual_id=comunidade.id,
        nick="Guerreira_de_teste",
    )
    sessao.commit()
    assert persona.papel == Papel.guerreiro
    assert persona.comunidade_virtual_id == comunidade.id


def test_guerreiro_sem_comunidade_nao_e_criado(sessao):
    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_persona(sessao, papel=Papel.guerreiro, criada_por=None)
    assert excinfo.value.campo == "comunidade_virtual_id"
    assert sessao.query(Persona).count() == 0


def test_guerreiro_sem_nick_nao_e_criado(sessao, criar_comunidade):
    comunidade = criar_comunidade()
    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_persona(
            sessao, papel=Papel.guerreiro, criada_por=None, comunidade_virtual_id=comunidade.id
        )
    assert excinfo.value.campo == "nick"
    assert sessao.query(Persona).count() == 0
    assert sessao.query(Nick).count() == 0


def test_nick_repetido_e_recusado_entre_papeis_diferentes(sessao, criar_comunidade):
    comunidade = criar_comunidade()
    criar_persona(
        sessao,
        papel=Papel.guerreiro,
        criada_por=None,
        comunidade_virtual_id=comunidade.id,
        nick="MesmoNick",
    )
    sessao.commit()

    admin = Persona(papel=Papel.admin)
    sessao.add(admin)
    sessao.flush()

    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_persona(
            sessao,
            papel=Papel.guerreiro,
            criada_por=None,
            comunidade_virtual_id=comunidade.id,
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


def test_vincular_comunidade_so_vale_para_guerreiro(sessao, criar_comunidade):
    admin = Persona(papel=Papel.admin)
    sessao.add(admin)
    sessao.flush()
    comunidade = criar_comunidade()

    with pytest.raises(ErroDeValidacao):
        vincular_guerreiro_a_comunidade(admin, comunidade.id)


def test_segundo_vinculo_de_comunidade_e_recusado(sessao, criar_comunidade):
    comunidade_um = criar_comunidade("Comunidade Um")
    comunidade_dois = criar_comunidade("Comunidade Dois")
    guerreiro = criar_persona(
        sessao,
        papel=Papel.guerreiro,
        criada_por=None,
        comunidade_virtual_id=comunidade_um.id,
        nick="Guerreiro_de_teste",
    )
    sessao.commit()

    with pytest.raises(ErroDeValidacao):
        vincular_guerreiro_a_comunidade(guerreiro, comunidade_dois.id)

    assert guerreiro.comunidade_virtual_id == comunidade_um.id


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
