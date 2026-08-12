import pytest

from nucleo.erros import ErroDeValidacao, PermissaoNegada
from nucleo.personas.modelo import Papel
from nucleo.poderes.modelo import NaturezaDoPoder, Poder, VigenciaDoPoder
from nucleo.poderes.regra import alterar_poder, cadastrar_poder, desativar_poder


def test_admin_cadastra_poder_com_autoria(sessao, criar_persona):
    admin = criar_persona(Papel.admin)

    poder = cadastrar_poder(
        sessao,
        operador=admin,
        nome="Poder da IA e Robótica",
        descricao="Programação, eletrônica, robótica e IA.",
        natureza=NaturezaDoPoder.de_guerreiro,
    )
    sessao.commit()

    assert poder.autor_id == admin.id
    assert poder.papel_do_autor == Papel.admin.value
    assert poder.registrado_em is not None
    assert poder.ativo is True


def test_mestre_nao_cadastra_poder(sessao, criar_persona):
    mestre = criar_persona(Papel.mestre)

    with pytest.raises(PermissaoNegada):
        cadastrar_poder(
            sessao,
            operador=mestre,
            nome="Poder da Rima",
            descricao="Expressão artística.",
            natureza=NaturezaDoPoder.de_guerreiro,
        )
    assert sessao.query(Poder).count() == 0


def test_mestre_nao_altera_nem_desativa_poder(sessao, criar_persona, criar_poder):
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre)
    poder = criar_poder(admin)

    with pytest.raises(PermissaoNegada):
        alterar_poder(sessao, poder, operador=mestre, nome="Novo nome")
    with pytest.raises(PermissaoNegada):
        desativar_poder(sessao, poder, operador=mestre)

    sessao.refresh(poder)
    assert poder.nome != "Novo nome"
    assert poder.ativo is True


def test_alterar_poder_para_nome_vazio_e_recusado(sessao, criar_persona, criar_poder):
    admin = criar_persona(Papel.admin)
    poder = criar_poder(admin, nome="Nome original")

    with pytest.raises(ErroDeValidacao) as excinfo:
        alterar_poder(sessao, poder, operador=admin, nome="   ")
    assert excinfo.value.campo == "nome"
    sessao.refresh(poder)
    assert poder.nome == "Nome original"


def test_poder_sem_nome_e_recusado(sessao, criar_persona):
    admin = criar_persona(Papel.admin)

    with pytest.raises(ErroDeValidacao) as excinfo:
        cadastrar_poder(
            sessao,
            operador=admin,
            nome="",
            descricao="Descrição qualquer.",
            natureza=NaturezaDoPoder.de_guerreiro,
        )
    assert excinfo.value.campo == "nome"
    assert sessao.query(Poder).count() == 0


def test_poder_de_ciclo_futuro_fica_no_catalogo_distinguivel(sessao, criar_persona):
    admin = criar_persona(Papel.admin)

    poder = cadastrar_poder(
        sessao,
        operador=admin,
        nome="Poder da Rima",
        descricao="Expressão artística: rima, rap, batalhas de rima.",
        natureza=NaturezaDoPoder.de_guerreiro,
        vigencia=VigenciaDoPoder.ciclo_futuro,
    )
    sessao.commit()

    do_catalogo = sessao.get(Poder, poder.id)
    assert do_catalogo.vigencia == VigenciaDoPoder.ciclo_futuro


def test_admin_altera_e_desativa_poder(sessao, criar_persona, criar_poder):
    admin = criar_persona(Papel.admin)
    poder = criar_poder(admin, nome="Nome original")

    alterar_poder(
        sessao,
        poder,
        operador=admin,
        nome="Nome revisado",
        descricao="Descrição revisada.",
        vigencia=VigenciaDoPoder.ciclo_futuro,
    )
    sessao.commit()
    sessao.refresh(poder)
    assert poder.nome == "Nome revisado"
    assert poder.descricao == "Descrição revisada."
    assert poder.vigencia == VigenciaDoPoder.ciclo_futuro

    desativar_poder(sessao, poder, operador=admin)
    sessao.commit()
    sessao.refresh(poder)
    assert poder.ativo is False
