import pytest

from nucleo.apoio_escolar.modelo import Conteudo, Disciplina
from nucleo.apoio_escolar.regra import (
    alterar_conteudo,
    cadastrar_conteudo,
    cadastrar_disciplina,
    despublicar_conteudo,
)
from nucleo.erros import ErroDeValidacao, PermissaoNegada
from nucleo.personas.modelo import Papel


def test_mestre_cadastra_disciplina_com_autoria(sessao, criar_persona):
    mestre = criar_persona(Papel.mestre)

    disciplina = cadastrar_disciplina(sessao, operador=mestre, nome="Matemática")
    sessao.commit()

    assert disciplina.nome == "Matemática"
    assert disciplina.nome_normalizado == "matemática"
    assert disciplina.autor_id == mestre.id
    assert disciplina.registrado_em is not None


def test_admin_tambem_cadastra_disciplina(sessao, criar_persona):
    admin = criar_persona(Papel.admin)

    disciplina = cadastrar_disciplina(sessao, operador=admin, nome="Português")
    sessao.commit()

    assert disciplina.autor_id == admin.id


def test_guerreiro_nao_cadastra_disciplina(sessao, criar_persona):
    guerreiro = criar_persona(Papel.guerreiro)

    with pytest.raises(PermissaoNegada):
        cadastrar_disciplina(sessao, operador=guerreiro, nome="Ciências")
    assert sessao.query(Disciplina).count() == 0


def test_disciplina_sem_nome_e_recusada(sessao, criar_persona):
    mestre = criar_persona(Papel.mestre)

    with pytest.raises(ErroDeValidacao):
        cadastrar_disciplina(sessao, operador=mestre, nome="")
    assert sessao.query(Disciplina).count() == 0


def test_disciplina_duplicada_pelo_nome_normalizado_e_recusada(sessao, criar_persona):
    mestre_1 = criar_persona(Papel.mestre)
    mestre_2 = criar_persona(Papel.mestre)
    cadastrar_disciplina(sessao, operador=mestre_1, nome="Matemática")
    sessao.commit()

    with pytest.raises(ErroDeValidacao):
        cadastrar_disciplina(sessao, operador=mestre_2, nome="  MATEMÁTICA  ")
    assert sessao.query(Disciplina).count() == 1


def test_mestre_diferente_cadastra_conteudo_na_mesma_disciplina(sessao, criar_persona):
    mestre_1 = criar_persona(Papel.mestre)
    mestre_2 = criar_persona(Papel.mestre)
    disciplina = cadastrar_disciplina(sessao, operador=mestre_1, nome="Matemática")
    sessao.commit()

    conteudo = cadastrar_conteudo(
        sessao, operador=mestre_2, disciplina=disciplina, material="Frações: o que são."
    )
    sessao.commit()

    assert conteudo.disciplina_id == disciplina.id
    assert conteudo.autor_id == mestre_2.id
    assert conteudo.despublicado_em is None


def test_conteudo_sem_disciplina_e_recusado(sessao, criar_persona):
    mestre = criar_persona(Papel.mestre)

    with pytest.raises(ErroDeValidacao):
        cadastrar_conteudo(sessao, operador=mestre, disciplina=None, material="Texto.")
    assert sessao.query(Conteudo).count() == 0


def test_conteudo_sem_material_e_recusado(sessao, criar_persona):
    mestre = criar_persona(Papel.mestre)
    disciplina = cadastrar_disciplina(sessao, operador=mestre, nome="Matemática")

    with pytest.raises(ErroDeValidacao):
        cadastrar_conteudo(sessao, operador=mestre, disciplina=disciplina, material="")
    assert sessao.query(Conteudo).count() == 0


def test_admin_altera_conteudo_de_qualquer_mestre(sessao, criar_persona):
    mestre = criar_persona(Papel.mestre)
    admin = criar_persona(Papel.admin)
    disciplina = cadastrar_disciplina(sessao, operador=mestre, nome="Matemática")
    conteudo = cadastrar_conteudo(
        sessao, operador=mestre, disciplina=disciplina, material="Versão 1."
    )
    sessao.commit()

    alterar_conteudo(sessao, conteudo, operador=admin, material="Versão 2.")
    sessao.commit()
    sessao.refresh(conteudo)

    assert conteudo.material == "Versão 2."
    assert conteudo.autor_id == mestre.id


def test_alterar_conteudo_para_material_vazio_e_recusado(sessao, criar_persona):
    mestre = criar_persona(Papel.mestre)
    disciplina = cadastrar_disciplina(sessao, operador=mestre, nome="Matemática")
    conteudo = cadastrar_conteudo(
        sessao, operador=mestre, disciplina=disciplina, material="Versão 1."
    )
    sessao.commit()

    with pytest.raises(ErroDeValidacao):
        alterar_conteudo(sessao, conteudo, operador=mestre, material="")
    sessao.refresh(conteudo)
    assert conteudo.material == "Versão 1."


def test_mestre_autor_altera_o_proprio_conteudo(sessao, criar_persona):
    mestre = criar_persona(Papel.mestre)
    disciplina = cadastrar_disciplina(sessao, operador=mestre, nome="Matemática")
    conteudo = cadastrar_conteudo(
        sessao, operador=mestre, disciplina=disciplina, material="Versão 1."
    )
    sessao.commit()

    alterar_conteudo(sessao, conteudo, operador=mestre, material="Versão 2.")
    sessao.commit()
    sessao.refresh(conteudo)

    assert conteudo.material == "Versão 2."


def test_outro_mestre_e_recusado_ao_alterar_conteudo(sessao, criar_persona):
    autor = criar_persona(Papel.mestre)
    outro_mestre = criar_persona(Papel.mestre)
    disciplina = cadastrar_disciplina(sessao, operador=autor, nome="Matemática")
    conteudo = cadastrar_conteudo(
        sessao, operador=autor, disciplina=disciplina, material="Versão 1."
    )
    sessao.commit()

    with pytest.raises(PermissaoNegada):
        alterar_conteudo(sessao, conteudo, operador=outro_mestre, material="Versão 2.")
    sessao.refresh(conteudo)
    assert conteudo.material == "Versão 1."


def test_admin_despublica_conteudo_de_qualquer_mestre(sessao, criar_persona):
    mestre = criar_persona(Papel.mestre)
    admin = criar_persona(Papel.admin)
    disciplina = cadastrar_disciplina(sessao, operador=mestre, nome="Matemática")
    conteudo = cadastrar_conteudo(
        sessao, operador=mestre, disciplina=disciplina, material="Versão 1."
    )
    sessao.commit()

    despublicar_conteudo(sessao, conteudo, operador=admin, motivo="Conteúdo desatualizado.")
    sessao.commit()
    sessao.refresh(conteudo)

    assert conteudo.despublicado_em is not None
    assert conteudo.despublicado_por_id == admin.id
    assert conteudo.motivo_da_despublicacao == "Conteúdo desatualizado."
    assert conteudo.autor_id == mestre.id


def test_mestre_nao_despublica_conteudo(sessao, criar_persona):
    mestre = criar_persona(Papel.mestre)
    disciplina = cadastrar_disciplina(sessao, operador=mestre, nome="Matemática")
    conteudo = cadastrar_conteudo(
        sessao, operador=mestre, disciplina=disciplina, material="Versão 1."
    )
    sessao.commit()

    with pytest.raises(PermissaoNegada):
        despublicar_conteudo(sessao, conteudo, operador=mestre, motivo="Qualquer motivo.")
    sessao.refresh(conteudo)
    assert conteudo.despublicado_em is None


def test_despublicacao_sem_motivo_e_recusada(sessao, criar_persona):
    mestre = criar_persona(Papel.mestre)
    admin = criar_persona(Papel.admin)
    disciplina = cadastrar_disciplina(sessao, operador=mestre, nome="Matemática")
    conteudo = cadastrar_conteudo(
        sessao, operador=mestre, disciplina=disciplina, material="Versão 1."
    )
    sessao.commit()

    with pytest.raises(ErroDeValidacao):
        despublicar_conteudo(sessao, conteudo, operador=admin, motivo="")
    sessao.refresh(conteudo)
    assert conteudo.despublicado_em is None
