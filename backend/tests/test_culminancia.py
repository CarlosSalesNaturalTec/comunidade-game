import pytest

from nucleo.criacoes_originais.modelo import CriacaoOriginal
from nucleo.culminancias.modelo import Culminancia, ModalidadeDaCulminancia
from nucleo.culminancias.regra import declarar_culminancia
from nucleo.erros import ErroDeValidacao, PermissaoNegada
from nucleo.personas.modelo import Papel


def test_mestre_autor_declara_a_culminancia(sessao, criar_persona, criar_trilha):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)

    culminancia = declarar_culminancia(
        sessao,
        trilha=trilha,
        operador=mestre,
        descricao="Um robô que resolve um problema da comunidade.",
        modalidade="individual",
        criterio_de_validacao="O robô precisa funcionar e resolver o problema declarado.",
    )
    sessao.commit()

    assert culminancia.trilha_id == trilha.id
    assert culminancia.modalidade == ModalidadeDaCulminancia.individual
    assert culminancia.autor_id == mestre.id
    assert sessao.query(Culminancia).filter_by(trilha_id=trilha.id).count() == 1


def test_modalidade_fora_dos_dois_valores_e_recusada(sessao, criar_persona, criar_trilha):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)

    with pytest.raises(ErroDeValidacao) as excinfo:
        declarar_culminancia(
            sessao,
            trilha=trilha,
            operador=mestre,
            descricao="Descrição.",
            modalidade="em_equipe_com_familiar",
            criterio_de_validacao="Critério.",
        )
    assert excinfo.value.campo == "modalidade"
    assert sessao.query(Culminancia).count() == 0


def test_culminancia_sem_criterio_de_validacao_e_recusada(sessao, criar_persona, criar_trilha):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)

    with pytest.raises(ErroDeValidacao) as excinfo:
        declarar_culminancia(
            sessao,
            trilha=trilha,
            operador=mestre,
            descricao="Descrição.",
            modalidade="individual",
            criterio_de_validacao=None,
        )
    assert excinfo.value.campo == "criterio_de_validacao"
    assert sessao.query(Culminancia).count() == 0


def test_mestre_que_nao_e_o_autor_e_recusado(sessao, criar_persona, criar_trilha):
    mestre_autor = criar_persona(Papel.mestre)
    outro_mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre_autor)

    with pytest.raises(PermissaoNegada):
        declarar_culminancia(
            sessao,
            trilha=trilha,
            operador=outro_mestre,
            descricao="Descrição.",
            modalidade="individual",
            criterio_de_validacao="Critério.",
        )
    assert sessao.query(Culminancia).count() == 0


def test_admin_nao_declara_culminancia(sessao, criar_persona, criar_trilha):
    mestre_autor = criar_persona(Papel.mestre)
    admin = criar_persona(Papel.admin)
    trilha = criar_trilha(mestre_autor)

    with pytest.raises(PermissaoNegada):
        declarar_culminancia(
            sessao,
            trilha=trilha,
            operador=admin,
            descricao="Descrição.",
            modalidade="individual",
            criterio_de_validacao="Critério.",
        )


def test_segunda_declaracao_substitui_a_primeira(sessao, criar_persona, criar_trilha):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)

    declarar_culminancia(
        sessao,
        trilha=trilha,
        operador=mestre,
        descricao="Primeira versão.",
        modalidade="individual",
        criterio_de_validacao="Primeiro critério.",
    )
    sessao.commit()

    culminancia = declarar_culminancia(
        sessao,
        trilha=trilha,
        operador=mestre,
        descricao="Segunda versão.",
        modalidade="em_equipe",
        criterio_de_validacao="Segundo critério.",
    )
    sessao.commit()

    assert culminancia.descricao == "Segunda versão."
    assert culminancia.modalidade == ModalidadeDaCulminancia.em_equipe
    assert sessao.query(Culminancia).filter_by(trilha_id=trilha.id).count() == 1


def test_criacao_original_nao_tem_referencia_propria_a_culminancia():
    colunas = {coluna.name for coluna in CriacaoOriginal.__table__.columns}
    assert "culminancia_id" not in colunas
    assert "trilha_id" in colunas
