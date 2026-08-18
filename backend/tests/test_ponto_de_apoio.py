import pytest

from nucleo.erros import ErroDeValidacao, NaoEncontrado, PermissaoNegada
from nucleo.personas.modelo import Papel
from nucleo.pontos_de_apoio.modelo import PontoDeApoio
from nucleo.pontos_de_apoio.regra import cadastrar_ponto_de_apoio, designar_responsavel


def test_admin_cadastra_ponto_de_apoio_com_autoria_gravada(sessao, criar_persona, criar_comunidade):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()

    ponto_de_apoio = cadastrar_ponto_de_apoio(
        sessao, operador=admin, nome="Sede", comunidade_id=comunidade.id
    )
    sessao.commit()

    assert ponto_de_apoio.nome == "Sede"
    assert ponto_de_apoio.comunidade_virtual_id == comunidade.id
    assert ponto_de_apoio.responsavel_id is None
    assert ponto_de_apoio.ativo is True
    assert ponto_de_apoio.autor_id == admin.id
    assert ponto_de_apoio.papel_do_autor == Papel.admin.value


def test_mestre_nao_cadastra_ponto_de_apoio(sessao, criar_persona, criar_comunidade):
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()

    with pytest.raises(PermissaoNegada):
        cadastrar_ponto_de_apoio(sessao, operador=mestre, nome="Sede", comunidade_id=comunidade.id)
    assert sessao.query(PontoDeApoio).count() == 0


def test_ponto_de_apoio_sem_nome_e_recusado(sessao, criar_persona, criar_comunidade):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()

    with pytest.raises(ErroDeValidacao) as excinfo:
        cadastrar_ponto_de_apoio(sessao, operador=admin, nome=None, comunidade_id=comunidade.id)
    assert excinfo.value.campo == "nome"
    assert sessao.query(PontoDeApoio).count() == 0


def test_ponto_de_apoio_sem_comunidade_e_recusado(sessao, criar_persona):
    admin = criar_persona(Papel.admin)

    with pytest.raises(ErroDeValidacao) as excinfo:
        cadastrar_ponto_de_apoio(sessao, operador=admin, nome="Sede", comunidade_id=None)
    assert excinfo.value.campo == "comunidade_id"
    assert sessao.query(PontoDeApoio).count() == 0


def test_ponto_de_apoio_de_comunidade_inexistente_e_recusado(sessao, criar_persona):
    admin = criar_persona(Papel.admin)

    with pytest.raises(ErroDeValidacao) as excinfo:
        cadastrar_ponto_de_apoio(sessao, operador=admin, nome="Sede", comunidade_id=admin.id)
    assert excinfo.value.campo == "comunidade_id"
    assert sessao.query(PontoDeApoio).count() == 0


def test_ponto_de_apoio_nasce_sem_responsavel(
    sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()

    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)

    assert ponto_de_apoio.responsavel_id is None


def test_admin_designa_mestre_como_responsavel(
    sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    mestre = criar_persona(Papel.mestre)

    resultado = designar_responsavel(sessao, ponto_de_apoio, operador=admin, responsavel=mestre)
    sessao.commit()

    assert resultado.responsavel_id == mestre.id


def test_apoiador_pode_ser_designado_responsavel(
    sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    apoiador = criar_persona(Papel.apoiador)

    resultado = designar_responsavel(sessao, ponto_de_apoio, operador=admin, responsavel=apoiador)
    sessao.commit()

    assert resultado.responsavel_id == apoiador.id


def test_guerreiro_nao_e_designado_responsavel(
    sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)

    with pytest.raises(ErroDeValidacao) as excinfo:
        designar_responsavel(sessao, ponto_de_apoio, operador=admin, responsavel=guerreiro)
    assert excinfo.value.campo == "responsavel_id"
    assert ponto_de_apoio.responsavel_id is None


def test_responsavel_familiar_nao_e_designado_responsavel_pelo_acervo(
    sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    responsavel = criar_persona(Papel.responsavel, criada_por=admin)

    with pytest.raises(ErroDeValidacao) as excinfo:
        designar_responsavel(sessao, ponto_de_apoio, operador=admin, responsavel=responsavel)
    assert excinfo.value.campo == "responsavel_id"
    assert ponto_de_apoio.responsavel_id is None


def test_troca_do_responsavel_substitui_o_anterior(
    sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    primeiro = criar_persona(Papel.mestre)
    segundo = criar_persona(Papel.apoiador)

    designar_responsavel(sessao, ponto_de_apoio, operador=admin, responsavel=primeiro)
    sessao.commit()

    resultado = designar_responsavel(sessao, ponto_de_apoio, operador=admin, responsavel=segundo)
    sessao.commit()

    assert resultado.responsavel_id == segundo.id


def test_mestre_nao_designa_responsavel(
    sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    mestre = criar_persona(Papel.mestre)
    outro_mestre = criar_persona(Papel.mestre)

    with pytest.raises(PermissaoNegada):
        designar_responsavel(sessao, ponto_de_apoio, operador=mestre, responsavel=outro_mestre)
    assert ponto_de_apoio.responsavel_id is None


def test_designacao_em_ponto_de_apoio_inexistente_e_recusada(sessao, criar_persona):
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre)

    with pytest.raises(NaoEncontrado):
        designar_responsavel(sessao, None, operador=admin, responsavel=mestre)
