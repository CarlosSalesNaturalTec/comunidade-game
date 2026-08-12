import uuid

import pytest

from nucleo.erros import ErroDeValidacao, PermissaoNegada
from nucleo.personas.modelo import Papel
from nucleo.poderes.modelo import NaturezaDoPoder, VigenciaDoPoder
from nucleo.trilhas.modelo import SituacaoDaTrilha, Trilha
from nucleo.trilhas.regra import conferir_posse_da_trilha, consultar_trilhas, criar_trilha


def test_trilha_criada_com_poder_e_autor(sessao, criar_persona, criar_poder):
    mestre = criar_persona(Papel.mestre)
    poder = criar_poder(mestre, natureza=NaturezaDoPoder.de_guerreiro)

    trilha = criar_trilha(
        sessao,
        autor=mestre,
        nome="Robô Educa",
        objetivo="Construir o próprio robô.",
        area_do_conhecimento="Programação e Robótica",
        poder_id=poder.id,
    )
    sessao.commit()

    assert trilha.poder_id == poder.id
    assert trilha.autor_id == mestre.id
    assert trilha.papel_do_autor == Papel.mestre.value
    assert trilha.registrado_em is not None
    assert trilha.situacao == SituacaoDaTrilha.rascunho


def test_trilha_sem_poder_e_recusada(sessao, criar_persona):
    mestre = criar_persona(Papel.mestre)

    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_trilha(
            sessao,
            autor=mestre,
            nome="Trilha sem poder",
            objetivo="Objetivo qualquer.",
            area_do_conhecimento="Tecnologia",
            poder_id=None,
        )
    assert excinfo.value.campo == "poder_id"
    assert sessao.query(Trilha).count() == 0


def test_trilha_com_poder_inexistente_e_recusada(sessao, criar_persona):
    mestre = criar_persona(Papel.mestre)

    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_trilha(
            sessao,
            autor=mestre,
            nome="Trilha com poder inexistente",
            objetivo="Objetivo.",
            area_do_conhecimento="Tecnologia",
            poder_id=uuid.uuid4(),
        )
    assert excinfo.value.campo == "poder_id"
    assert sessao.query(Trilha).count() == 0


def test_trilha_se_vincula_a_poder_de_guerreiro(sessao, criar_persona, criar_poder):
    mestre = criar_persona(Papel.mestre)
    poder = criar_poder(mestre, natureza=NaturezaDoPoder.de_guerreiro)

    trilha = criar_trilha(
        sessao,
        autor=mestre,
        nome="Robô Educa",
        objetivo="Objetivo.",
        area_do_conhecimento="Tecnologia",
        poder_id=poder.id,
    )
    assert trilha.poder_id == poder.id


def test_trilha_no_poder_sustentador_e_recusada(sessao, criar_persona, criar_poder):
    mestre = criar_persona(Papel.mestre)
    poder_sustentador = criar_poder(mestre, natureza=NaturezaDoPoder.derivado_do_aporte)

    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_trilha(
            sessao,
            autor=mestre,
            nome="Trilha inválida",
            objetivo="Objetivo.",
            area_do_conhecimento="Tecnologia",
            poder_id=poder_sustentador.id,
        )
    assert excinfo.value.campo == "poder_id"
    assert sessao.query(Trilha).count() == 0


def test_vigencia_de_ciclo_futuro_nao_bloqueia_vinculo_de_trilha(
    sessao, criar_persona, criar_poder
):
    mestre = criar_persona(Papel.mestre)
    poder = criar_poder(
        mestre, natureza=NaturezaDoPoder.de_guerreiro, vigencia=VigenciaDoPoder.ciclo_futuro
    )

    trilha = criar_trilha(
        sessao,
        autor=mestre,
        nome="Trilha de ciclo futuro",
        objetivo="Objetivo.",
        area_do_conhecimento="Tecnologia",
        poder_id=poder.id,
    )
    assert trilha.poder_id == poder.id


def test_mestre_autor_tem_posse_da_propria_trilha(sessao, criar_persona, criar_trilha):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)

    conferir_posse_da_trilha(trilha, mestre)


def test_outro_mestre_e_recusado(sessao, criar_persona, criar_trilha):
    mestre_autor = criar_persona(Papel.mestre)
    outro_mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre_autor)

    with pytest.raises(PermissaoNegada):
        conferir_posse_da_trilha(trilha, outro_mestre)


def test_admin_alcanca_qualquer_trilha(sessao, criar_persona, criar_trilha):
    mestre_autor = criar_persona(Papel.mestre)
    admin = criar_persona(Papel.admin)
    trilha = criar_trilha(mestre_autor)

    conferir_posse_da_trilha(trilha, admin)


def test_rascunho_nao_aparece_a_quem_nao_e_autor(sessao, criar_persona, criar_trilha):
    mestre_autor = criar_persona(Papel.mestre)
    outro_mestre = criar_persona(Papel.mestre)
    criar_trilha(mestre_autor, situacao=SituacaoDaTrilha.rascunho)

    resultado = consultar_trilhas(sessao, persona=outro_mestre)
    assert resultado == []


def test_mestre_autor_ve_o_proprio_rascunho(sessao, criar_persona, criar_trilha):
    mestre_autor = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre_autor, situacao=SituacaoDaTrilha.rascunho)

    resultado = consultar_trilhas(sessao, persona=mestre_autor)
    assert [t.id for t in resultado] == [trilha.id]


def test_admin_alcanca_todas_as_trilhas_na_consulta(sessao, criar_persona, criar_trilha):
    mestre_autor = criar_persona(Papel.mestre)
    admin = criar_persona(Papel.admin)
    trilha_rascunho = criar_trilha(mestre_autor, situacao=SituacaoDaTrilha.rascunho)
    trilha_publicada = criar_trilha(mestre_autor, situacao=SituacaoDaTrilha.publicada)

    resultado = {t.id for t in consultar_trilhas(sessao, persona=admin)}
    assert resultado == {trilha_rascunho.id, trilha_publicada.id}


def test_consulta_de_trilha_sem_informar_comunidade(sessao, criar_trilha, criar_persona):
    mestre_autor = criar_persona(Papel.mestre)
    criar_trilha(mestre_autor, situacao=SituacaoDaTrilha.publicada)

    resultado = consultar_trilhas(sessao)
    assert len(resultado) == 1


def test_mesma_trilha_alcanca_comunidades_diferentes(
    sessao, criar_persona, criar_comunidade, criar_trilha
):
    mestre_autor = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre_autor, situacao=SituacaoDaTrilha.publicada)

    comunidade_um = criar_comunidade("Comunidade Um")
    comunidade_dois = criar_comunidade("Comunidade Dois")
    guerreiro_um = criar_persona(Papel.guerreiro, comunidade=comunidade_um)
    guerreiro_dois = criar_persona(Papel.guerreiro, comunidade=comunidade_dois)

    resultado_um = consultar_trilhas(sessao, persona=guerreiro_um)
    resultado_dois = consultar_trilhas(sessao, persona=guerreiro_dois)

    assert [t.id for t in resultado_um] == [trilha.id]
    assert [t.id for t in resultado_dois] == [trilha.id]


def test_nao_ha_vinculo_de_comunidade_na_entidade_trilha():
    colunas = {coluna.name for coluna in Trilha.__table__.columns}
    assert not any("comunidade" in coluna for coluna in colunas)
