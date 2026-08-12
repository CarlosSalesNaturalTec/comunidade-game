import pytest

from nucleo.criacoes_originais.modelo import CriacaoOriginal, SituacaoDaCriacaoOriginal
from nucleo.criacoes_originais.regra import (
    devolver_criacao_original,
    entregar_criacao_original,
    validar_criacao_original,
)
from nucleo.erros import ErroDeValidacao, PermissaoNegada
from nucleo.personas.modelo import Papel


def test_entrega_com_trilha_guerreiro_e_producao_grava_o_registro(
    sessao, criar_persona, criar_trilha
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)

    criacao = entregar_criacao_original(
        sessao, guerreiro=guerreiro, trilha=trilha, producao="Meu robô de sucata."
    )
    sessao.commit()

    assert criacao.trilha_id == trilha.id
    assert criacao.autor_id == guerreiro.id
    assert criacao.papel_do_autor == Papel.guerreiro.value
    assert criacao.situacao == SituacaoDaCriacaoOriginal.entregue
    assert criacao.validado_por_id is None
    assert criacao.validado_em is None


def test_entrega_sem_trilha_e_recusada(sessao, criar_persona):
    guerreiro = criar_persona(Papel.guerreiro)

    with pytest.raises(ErroDeValidacao) as excinfo:
        entregar_criacao_original(
            sessao, guerreiro=guerreiro, trilha=None, producao="Meu robô de sucata."
        )
    assert excinfo.value.campo == "trilha_id"
    assert sessao.query(CriacaoOriginal).count() == 0


def test_entrega_sem_guerreiro_e_recusada(sessao, criar_persona, criar_trilha):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)

    with pytest.raises(ErroDeValidacao) as excinfo:
        entregar_criacao_original(
            sessao, guerreiro=None, trilha=trilha, producao="Meu robô de sucata."
        )
    assert excinfo.value.campo == "guerreiro_id"
    assert sessao.query(CriacaoOriginal).count() == 0


def test_entrega_sem_producao_e_recusada(sessao, criar_persona, criar_trilha):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)

    with pytest.raises(ErroDeValidacao) as excinfo:
        entregar_criacao_original(sessao, guerreiro=guerreiro, trilha=trilha, producao=None)
    assert excinfo.value.campo == "producao"
    assert sessao.query(CriacaoOriginal).count() == 0


def test_mestre_autor_valida_a_entrega(sessao, criar_persona, criar_trilha):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    criacao = entregar_criacao_original(
        sessao, guerreiro=guerreiro, trilha=trilha, producao="Produção."
    )
    sessao.commit()

    validar_criacao_original(sessao, operador=mestre, criacao=criacao)
    sessao.commit()

    assert criacao.situacao == SituacaoDaCriacaoOriginal.validada
    assert criacao.validado_por_id == mestre.id
    assert criacao.validado_em is not None


def test_mestre_autor_devolve_a_entrega(sessao, criar_persona, criar_trilha):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    criacao = entregar_criacao_original(
        sessao, guerreiro=guerreiro, trilha=trilha, producao="Produção."
    )
    sessao.commit()

    devolver_criacao_original(sessao, operador=mestre, criacao=criacao)
    sessao.commit()

    assert criacao.situacao == SituacaoDaCriacaoOriginal.devolvida
    assert criacao.validado_por_id == mestre.id
    assert criacao.validado_em is not None


def test_admin_valida_mesmo_sem_ser_o_autor(sessao, criar_persona, criar_trilha):
    mestre_autor = criar_persona(Papel.mestre)
    admin = criar_persona(Papel.admin)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre_autor)
    criacao = entregar_criacao_original(
        sessao, guerreiro=guerreiro, trilha=trilha, producao="Produção."
    )
    sessao.commit()

    validar_criacao_original(sessao, operador=admin, criacao=criacao)
    sessao.commit()

    assert criacao.situacao == SituacaoDaCriacaoOriginal.validada
    assert criacao.validado_por_id == admin.id


def test_mestre_que_nao_e_autor_e_recusado_ao_validar(sessao, criar_persona, criar_trilha):
    mestre_autor = criar_persona(Papel.mestre)
    outro_mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre_autor)
    criacao = entregar_criacao_original(
        sessao, guerreiro=guerreiro, trilha=trilha, producao="Produção."
    )
    sessao.commit()

    with pytest.raises(PermissaoNegada):
        validar_criacao_original(sessao, operador=outro_mestre, criacao=criacao)

    assert criacao.situacao == SituacaoDaCriacaoOriginal.entregue


def test_mestre_que_nao_e_autor_e_recusado_ao_devolver(sessao, criar_persona, criar_trilha):
    mestre_autor = criar_persona(Papel.mestre)
    outro_mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre_autor)
    criacao = entregar_criacao_original(
        sessao, guerreiro=guerreiro, trilha=trilha, producao="Produção."
    )
    sessao.commit()

    with pytest.raises(PermissaoNegada):
        devolver_criacao_original(sessao, operador=outro_mestre, criacao=criacao)

    assert criacao.situacao == SituacaoDaCriacaoOriginal.entregue


def test_validar_criacao_ja_validada_e_recusado(sessao, criar_persona, criar_trilha):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    criacao = entregar_criacao_original(
        sessao, guerreiro=guerreiro, trilha=trilha, producao="Produção."
    )
    sessao.commit()
    validar_criacao_original(sessao, operador=mestre, criacao=criacao)
    sessao.commit()

    with pytest.raises(ErroDeValidacao) as excinfo:
        validar_criacao_original(sessao, operador=mestre, criacao=criacao)
    assert excinfo.value.campo == "situacao"


def test_devolver_criacao_ja_devolvida_e_recusado(sessao, criar_persona, criar_trilha):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    criacao = entregar_criacao_original(
        sessao, guerreiro=guerreiro, trilha=trilha, producao="Produção."
    )
    sessao.commit()
    devolver_criacao_original(sessao, operador=mestre, criacao=criacao)
    sessao.commit()

    with pytest.raises(ErroDeValidacao) as excinfo:
        devolver_criacao_original(sessao, operador=mestre, criacao=criacao)
    assert excinfo.value.campo == "situacao"


def test_devolucao_preserva_a_autoria_original(sessao, criar_persona, criar_trilha):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    criacao = entregar_criacao_original(
        sessao, guerreiro=guerreiro, trilha=trilha, producao="Produção."
    )
    sessao.commit()

    devolver_criacao_original(sessao, operador=mestre, criacao=criacao)
    sessao.commit()

    assert criacao.autor_id == guerreiro.id
    assert criacao.papel_do_autor == Papel.guerreiro.value
