import pytest

from nucleo.criacoes_originais.modelo import (
    CriacaoOriginal,
    SituacaoDaCriacaoOriginal,
    TipoDeProducaoDaCriacaoOriginal,
)
from nucleo.criacoes_originais.regra import (
    devolver_criacao_original,
    entregar_criacao_original,
    validar_criacao_original,
)
from nucleo.culminancias.modelo import ModalidadeDaCulminancia
from nucleo.equipes.regra import entrar_na_equipe
from nucleo.erros import (
    CriacaoOriginalJaValidada,
    ErroDeValidacao,
    NaoEncontrado,
    PermissaoNegada,
    TrilhaSemCulminanciaDeclarada,
)
from nucleo.personas.modelo import Papel

TEXTO = TipoDeProducaoDaCriacaoOriginal.texto


def test_entrega_em_equipe_com_producao_grava_o_registro(
    sessao, criar_persona, criar_trilha, criar_culminancia, criar_equipe
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    criar_culminancia(trilha, mestre, modalidade=ModalidadeDaCulminancia.em_equipe)
    equipe = criar_equipe(guerreiro, trilha=trilha)

    criacao = entregar_criacao_original(
        sessao,
        guerreiro=guerreiro,
        trilha=trilha,
        equipe=equipe,
        tipo=TEXTO,
        producao="Meu robô de sucata.",
    )
    sessao.commit()

    assert criacao.trilha_id == trilha.id
    assert criacao.equipe_id == equipe.id
    assert criacao.guerreiro_id is None
    assert criacao.autor_id == guerreiro.id
    assert criacao.papel_do_autor == Papel.guerreiro.value
    assert criacao.situacao == SituacaoDaCriacaoOriginal.entregue
    assert criacao.validado_por_id is None
    assert criacao.validado_em is None


def test_entrega_individual_registrada_em_nome_do_guerreiro(
    sessao, criar_persona, criar_trilha, criar_culminancia
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    criar_culminancia(trilha, mestre, modalidade=ModalidadeDaCulminancia.individual)

    criacao = entregar_criacao_original(
        sessao,
        guerreiro=guerreiro,
        trilha=trilha,
        equipe=None,
        tipo=TEXTO,
        producao="Meu diário do território.",
    )
    sessao.commit()

    assert criacao.trilha_id == trilha.id
    assert criacao.equipe_id is None
    assert criacao.guerreiro_id == guerreiro.id
    assert criacao.autor_id == guerreiro.id
    assert criacao.situacao == SituacaoDaCriacaoOriginal.entregue


def test_entrega_em_trilha_inexistente_e_recusada(sessao, criar_persona):
    guerreiro = criar_persona(Papel.guerreiro)

    with pytest.raises(NaoEncontrado):
        entregar_criacao_original(
            sessao, guerreiro=guerreiro, trilha=None, equipe=None, tipo=TEXTO, producao="Produção."
        )
    assert sessao.query(CriacaoOriginal).count() == 0


def test_entrega_em_trilha_sem_culminancia_declarada_e_recusada(
    sessao, criar_persona, criar_trilha
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)

    with pytest.raises(TrilhaSemCulminanciaDeclarada):
        entregar_criacao_original(
            sessao,
            guerreiro=guerreiro,
            trilha=trilha,
            equipe=None,
            tipo=TEXTO,
            producao="Produção.",
        )
    assert sessao.query(CriacaoOriginal).count() == 0


def test_entrega_sem_producao_e_recusada(
    sessao, criar_persona, criar_trilha, criar_culminancia, criar_equipe
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    criar_culminancia(trilha, mestre, modalidade=ModalidadeDaCulminancia.em_equipe)
    equipe = criar_equipe(guerreiro, trilha=trilha)

    with pytest.raises(ErroDeValidacao) as excinfo:
        entregar_criacao_original(
            sessao, guerreiro=guerreiro, trilha=trilha, equipe=equipe, tipo=TEXTO, producao=None
        )
    assert excinfo.value.campo == "producao"
    assert sessao.query(CriacaoOriginal).count() == 0


def test_tipo_fora_dos_cinco_valores_e_recusado(
    sessao, criar_persona, criar_trilha, criar_culminancia, criar_equipe
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    criar_culminancia(trilha, mestre, modalidade=ModalidadeDaCulminancia.em_equipe)
    equipe = criar_equipe(guerreiro, trilha=trilha)

    with pytest.raises(ErroDeValidacao) as excinfo:
        entregar_criacao_original(
            sessao,
            guerreiro=guerreiro,
            trilha=trilha,
            equipe=equipe,
            tipo="desenho_animado",
            producao="Produção.",
        )
    assert excinfo.value.campo == "tipo"
    assert sessao.query(CriacaoOriginal).count() == 0


def test_entrega_pela_equipe_em_culminancia_individual_e_recusada(
    sessao, criar_persona, criar_trilha, criar_culminancia, criar_equipe
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    criar_culminancia(trilha, mestre, modalidade=ModalidadeDaCulminancia.individual)
    equipe = criar_equipe(guerreiro, trilha=trilha)

    with pytest.raises(ErroDeValidacao) as excinfo:
        entregar_criacao_original(
            sessao,
            guerreiro=guerreiro,
            trilha=trilha,
            equipe=equipe,
            tipo=TEXTO,
            producao="Produção.",
        )
    assert excinfo.value.campo == "equipe_id"
    assert sessao.query(CriacaoOriginal).count() == 0


def test_entrega_sem_equipe_em_culminancia_em_equipe_e_recusada(
    sessao, criar_persona, criar_trilha, criar_culminancia
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    criar_culminancia(trilha, mestre, modalidade=ModalidadeDaCulminancia.em_equipe)

    with pytest.raises(ErroDeValidacao) as excinfo:
        entregar_criacao_original(
            sessao,
            guerreiro=guerreiro,
            trilha=trilha,
            equipe=None,
            tipo=TEXTO,
            producao="Produção.",
        )
    assert excinfo.value.campo == "equipe_id"
    assert sessao.query(CriacaoOriginal).count() == 0


def test_quem_nao_integra_a_equipe_nao_entrega(
    sessao, criar_persona, criar_trilha, criar_culminancia, criar_equipe
):
    mestre = criar_persona(Papel.mestre)
    guerreiro_da_equipe = criar_persona(Papel.guerreiro)
    guerreiro_de_fora = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    criar_culminancia(trilha, mestre, modalidade=ModalidadeDaCulminancia.em_equipe)
    equipe = criar_equipe(guerreiro_da_equipe, trilha=trilha)

    with pytest.raises(PermissaoNegada):
        entregar_criacao_original(
            sessao,
            guerreiro=guerreiro_de_fora,
            trilha=trilha,
            equipe=equipe,
            tipo=TEXTO,
            producao="Produção.",
        )
    assert sessao.query(CriacaoOriginal).count() == 0


def test_qualquer_integrante_entrega_pela_equipe(
    sessao, criar_persona, criar_trilha, criar_culminancia, criar_equipe
):
    mestre = criar_persona(Papel.mestre)
    criador = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    criar_culminancia(trilha, mestre, modalidade=ModalidadeDaCulminancia.em_equipe)
    equipe = criar_equipe(criador, trilha=trilha)
    colega = criar_persona(Papel.guerreiro)
    entrar_na_equipe(sessao, operador=colega, equipe=equipe)
    sessao.commit()

    criacao = entregar_criacao_original(
        sessao,
        guerreiro=colega,
        trilha=trilha,
        equipe=equipe,
        tipo=TEXTO,
        producao="Produção da equipe.",
    )
    sessao.commit()

    assert criacao.autor_id == colega.id
    assert criacao.equipe_id == equipe.id


def test_nova_entrega_antes_da_validacao_substitui_a_anterior(
    sessao, criar_persona, criar_trilha, criar_culminancia, criar_equipe
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    criar_culminancia(trilha, mestre, modalidade=ModalidadeDaCulminancia.em_equipe)
    equipe = criar_equipe(guerreiro, trilha=trilha)
    entregar_criacao_original(
        sessao, guerreiro=guerreiro, trilha=trilha, equipe=equipe, tipo=TEXTO, producao="Primeira."
    )
    sessao.commit()

    criacao = entregar_criacao_original(
        sessao, guerreiro=guerreiro, trilha=trilha, equipe=equipe, tipo=TEXTO, producao="Segunda."
    )
    sessao.commit()

    assert sessao.query(CriacaoOriginal).count() == 1
    assert criacao.producao == "Segunda."
    assert criacao.situacao == SituacaoDaCriacaoOriginal.entregue


def test_nova_entrega_individual_antes_da_validacao_substitui_a_anterior(
    sessao, criar_persona, criar_trilha, criar_culminancia
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    criar_culminancia(trilha, mestre, modalidade=ModalidadeDaCulminancia.individual)
    entregar_criacao_original(
        sessao,
        guerreiro=guerreiro,
        trilha=trilha,
        equipe=None,
        tipo=TEXTO,
        producao="Primeira.",
    )
    sessao.commit()

    criacao = entregar_criacao_original(
        sessao,
        guerreiro=guerreiro,
        trilha=trilha,
        equipe=None,
        tipo=TEXTO,
        producao="Segunda.",
    )
    sessao.commit()

    assert sessao.query(CriacaoOriginal).count() == 1
    assert criacao.producao == "Segunda."


def test_nova_entrega_depois_de_validada_e_recusada(
    sessao, criar_persona, criar_trilha, criar_culminancia, criar_equipe
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    criar_culminancia(trilha, mestre, modalidade=ModalidadeDaCulminancia.em_equipe)
    equipe = criar_equipe(guerreiro, trilha=trilha)
    criacao = entregar_criacao_original(
        sessao, guerreiro=guerreiro, trilha=trilha, equipe=equipe, tipo=TEXTO, producao="Produção."
    )
    sessao.commit()
    validar_criacao_original(sessao, operador=mestre, criacao=criacao)
    sessao.commit()

    with pytest.raises(CriacaoOriginalJaValidada):
        entregar_criacao_original(
            sessao,
            guerreiro=guerreiro,
            trilha=trilha,
            equipe=equipe,
            tipo=TEXTO,
            producao="Nova produção.",
        )
    sessao.refresh(criacao)
    assert criacao.situacao == SituacaoDaCriacaoOriginal.validada
    assert criacao.producao == "Produção."


def test_mestre_autor_valida_a_entrega(
    sessao, criar_persona, criar_trilha, criar_culminancia, criar_equipe
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    criar_culminancia(trilha, mestre, modalidade=ModalidadeDaCulminancia.em_equipe)
    equipe = criar_equipe(guerreiro, trilha=trilha)
    criacao = entregar_criacao_original(
        sessao, guerreiro=guerreiro, trilha=trilha, equipe=equipe, tipo=TEXTO, producao="Produção."
    )
    sessao.commit()

    validar_criacao_original(sessao, operador=mestre, criacao=criacao)
    sessao.commit()

    assert criacao.situacao == SituacaoDaCriacaoOriginal.validada
    assert criacao.validado_por_id == mestre.id
    assert criacao.validado_em is not None


def test_mestre_autor_devolve_a_entrega_com_motivo(
    sessao, criar_persona, criar_trilha, criar_culminancia, criar_equipe
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    criar_culminancia(trilha, mestre, modalidade=ModalidadeDaCulminancia.em_equipe)
    equipe = criar_equipe(guerreiro, trilha=trilha)
    criacao = entregar_criacao_original(
        sessao, guerreiro=guerreiro, trilha=trilha, equipe=equipe, tipo=TEXTO, producao="Produção."
    )
    sessao.commit()

    devolver_criacao_original(
        sessao, operador=mestre, criacao=criacao, motivo="Falta explicar o funcionamento."
    )
    sessao.commit()

    assert criacao.situacao == SituacaoDaCriacaoOriginal.devolvida
    assert criacao.motivo_da_devolucao == "Falta explicar o funcionamento."
    assert criacao.validado_por_id == mestre.id
    assert criacao.validado_em is not None


def test_devolucao_sem_motivo_e_recusada(
    sessao, criar_persona, criar_trilha, criar_culminancia, criar_equipe
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    criar_culminancia(trilha, mestre, modalidade=ModalidadeDaCulminancia.em_equipe)
    equipe = criar_equipe(guerreiro, trilha=trilha)
    criacao = entregar_criacao_original(
        sessao, guerreiro=guerreiro, trilha=trilha, equipe=equipe, tipo=TEXTO, producao="Produção."
    )
    sessao.commit()

    with pytest.raises(ErroDeValidacao) as excinfo:
        devolver_criacao_original(sessao, operador=mestre, criacao=criacao, motivo=None)
    assert excinfo.value.campo == "motivo"
    assert criacao.situacao == SituacaoDaCriacaoOriginal.entregue


def test_admin_valida_mesmo_sem_ser_o_autor(
    sessao, criar_persona, criar_trilha, criar_culminancia, criar_equipe
):
    mestre_autor = criar_persona(Papel.mestre)
    admin = criar_persona(Papel.admin)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre_autor)
    criar_culminancia(trilha, mestre_autor, modalidade=ModalidadeDaCulminancia.em_equipe)
    equipe = criar_equipe(guerreiro, trilha=trilha)
    criacao = entregar_criacao_original(
        sessao, guerreiro=guerreiro, trilha=trilha, equipe=equipe, tipo=TEXTO, producao="Produção."
    )
    sessao.commit()

    validar_criacao_original(sessao, operador=admin, criacao=criacao)
    sessao.commit()

    assert criacao.situacao == SituacaoDaCriacaoOriginal.validada
    assert criacao.validado_por_id == admin.id


def test_mestre_que_nao_e_autor_e_recusado_ao_validar(
    sessao, criar_persona, criar_trilha, criar_culminancia, criar_equipe
):
    mestre_autor = criar_persona(Papel.mestre)
    outro_mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre_autor)
    criar_culminancia(trilha, mestre_autor, modalidade=ModalidadeDaCulminancia.em_equipe)
    equipe = criar_equipe(guerreiro, trilha=trilha)
    criacao = entregar_criacao_original(
        sessao, guerreiro=guerreiro, trilha=trilha, equipe=equipe, tipo=TEXTO, producao="Produção."
    )
    sessao.commit()

    with pytest.raises(PermissaoNegada):
        validar_criacao_original(sessao, operador=outro_mestre, criacao=criacao)

    assert criacao.situacao == SituacaoDaCriacaoOriginal.entregue


def test_mestre_que_nao_e_autor_e_recusado_ao_devolver(
    sessao, criar_persona, criar_trilha, criar_culminancia, criar_equipe
):
    mestre_autor = criar_persona(Papel.mestre)
    outro_mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre_autor)
    criar_culminancia(trilha, mestre_autor, modalidade=ModalidadeDaCulminancia.em_equipe)
    equipe = criar_equipe(guerreiro, trilha=trilha)
    criacao = entregar_criacao_original(
        sessao, guerreiro=guerreiro, trilha=trilha, equipe=equipe, tipo=TEXTO, producao="Produção."
    )
    sessao.commit()

    with pytest.raises(PermissaoNegada):
        devolver_criacao_original(
            sessao, operador=outro_mestre, criacao=criacao, motivo="Motivo qualquer."
        )

    assert criacao.situacao == SituacaoDaCriacaoOriginal.entregue


def test_validar_criacao_ja_validada_e_recusado(
    sessao, criar_persona, criar_trilha, criar_culminancia, criar_equipe
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    criar_culminancia(trilha, mestre, modalidade=ModalidadeDaCulminancia.em_equipe)
    equipe = criar_equipe(guerreiro, trilha=trilha)
    criacao = entregar_criacao_original(
        sessao, guerreiro=guerreiro, trilha=trilha, equipe=equipe, tipo=TEXTO, producao="Produção."
    )
    sessao.commit()
    validar_criacao_original(sessao, operador=mestre, criacao=criacao)
    sessao.commit()

    with pytest.raises(ErroDeValidacao) as excinfo:
        validar_criacao_original(sessao, operador=mestre, criacao=criacao)
    assert excinfo.value.campo == "situacao"


def test_devolver_criacao_ja_devolvida_e_recusado(
    sessao, criar_persona, criar_trilha, criar_culminancia, criar_equipe
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    criar_culminancia(trilha, mestre, modalidade=ModalidadeDaCulminancia.em_equipe)
    equipe = criar_equipe(guerreiro, trilha=trilha)
    criacao = entregar_criacao_original(
        sessao, guerreiro=guerreiro, trilha=trilha, equipe=equipe, tipo=TEXTO, producao="Produção."
    )
    sessao.commit()
    devolver_criacao_original(sessao, operador=mestre, criacao=criacao, motivo="Ajuste isto.")
    sessao.commit()

    with pytest.raises(ErroDeValidacao) as excinfo:
        devolver_criacao_original(sessao, operador=mestre, criacao=criacao, motivo="De novo.")
    assert excinfo.value.campo == "situacao"


def test_devolucao_preserva_a_autoria_original(
    sessao, criar_persona, criar_trilha, criar_culminancia, criar_equipe
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    criar_culminancia(trilha, mestre, modalidade=ModalidadeDaCulminancia.em_equipe)
    equipe = criar_equipe(guerreiro, trilha=trilha)
    criacao = entregar_criacao_original(
        sessao, guerreiro=guerreiro, trilha=trilha, equipe=equipe, tipo=TEXTO, producao="Produção."
    )
    sessao.commit()

    devolver_criacao_original(sessao, operador=mestre, criacao=criacao, motivo="Ajuste isto.")
    sessao.commit()

    assert criacao.autor_id == guerreiro.id
    assert criacao.papel_do_autor == Papel.guerreiro.value
    assert criacao.equipe_id == equipe.id


def test_reenvio_preserva_a_autoria(
    sessao, criar_persona, criar_trilha, criar_culminancia, criar_equipe
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    criar_culminancia(trilha, mestre, modalidade=ModalidadeDaCulminancia.em_equipe)
    equipe = criar_equipe(guerreiro, trilha=trilha)
    criacao = entregar_criacao_original(
        sessao, guerreiro=guerreiro, trilha=trilha, equipe=equipe, tipo=TEXTO, producao="Produção."
    )
    sessao.commit()
    devolver_criacao_original(sessao, operador=mestre, criacao=criacao, motivo="Ajuste isto.")
    sessao.commit()

    reenviada = entregar_criacao_original(
        sessao,
        guerreiro=guerreiro,
        trilha=trilha,
        equipe=equipe,
        tipo=TEXTO,
        producao="Produção ajustada.",
    )
    sessao.commit()

    assert reenviada.id == criacao.id
    assert reenviada.autor_id == guerreiro.id
    assert reenviada.situacao == SituacaoDaCriacaoOriginal.entregue
    assert reenviada.producao == "Produção ajustada."
