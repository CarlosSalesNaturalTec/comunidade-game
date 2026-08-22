import uuid
from decimal import Decimal

import pytest

from nucleo.culminancias.modelo import Culminancia, ModalidadeDaCulminancia
from nucleo.erros import ErroDeValidacao, PermissaoNegada
from nucleo.personas.modelo import Papel
from nucleo.poderes.modelo import NaturezaDoPoder, VigenciaDoPoder
from nucleo.trilhas.modelo import SituacaoDaTrilha, Trilha
from nucleo.trilhas.regra import (
    conferir_posse_da_trilha,
    consultar_trilhas,
    criar_missao,
    criar_trilha,
    despublicar_trilha,
    publicar_trilha,
)


def _declarar_culminancia(sessao, trilha, autor):
    culminancia = Culminancia(
        trilha_id=trilha.id,
        descricao="Descrição da criação esperada.",
        modalidade=ModalidadeDaCulminancia.individual,
        criterio_de_validacao="Critério de validação.",
        autor_id=autor.id,
        papel_do_autor=autor.papel.value,
    )
    sessao.add(culminancia)
    sessao.commit()
    return culminancia


def _trilha_completa(sessao, criar_trilha, criar_missao, criar_desafio_de_coleta, mestre):
    """Trilha em rascunho que atende às três travas de publicação."""
    trilha = criar_trilha(mestre)
    sondagem = criar_missao(trilha, mestre, posicao=1, e_sondagem=True)
    criar_desafio_de_coleta(sondagem, mestre)
    _declarar_culminancia(sessao, trilha, mestre)
    return trilha


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


def test_despublicada_nao_aparece_em_consulta_publica(sessao, criar_persona, criar_trilha):
    mestre_autor = criar_persona(Papel.mestre)
    criar_trilha(mestre_autor, situacao=SituacaoDaTrilha.despublicada)

    resultado = consultar_trilhas(sessao)
    assert resultado == []


def test_mestre_autor_edita_trilha_despublicada(sessao, criar_persona, criar_trilha):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.despublicada)

    missao = criar_missao(
        sessao,
        operador=mestre,
        trilha=trilha,
        titulo="Missão nova",
        posicao=1,
        nivel_de_dificuldade=1,
        obrigatoria=True,
        etapa_do_ciclo="abertura",
    )

    assert missao.trilha_id == trilha.id
    assert trilha.situacao == SituacaoDaTrilha.despublicada


def test_trilha_completa_e_publicada_pelo_autor(
    sessao, criar_persona, criar_trilha, criar_missao, criar_desafio_de_coleta
):
    mestre = criar_persona(Papel.mestre)
    trilha = _trilha_completa(sessao, criar_trilha, criar_missao, criar_desafio_de_coleta, mestre)

    publicar_trilha(sessao, trilha, operador=mestre)
    sessao.commit()

    assert trilha.situacao == SituacaoDaTrilha.publicada
    assert trilha.autor_da_situacao_id == mestre.id
    assert trilha.motivo_da_situacao is None


def test_trilha_sem_sondagem_e_recusada(
    sessao, criar_persona, criar_trilha, criar_missao, criar_desafio_de_coleta
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre, posicao=1, e_sondagem=False)
    criar_desafio_de_coleta(missao, mestre)
    _declarar_culminancia(sessao, trilha, mestre)

    with pytest.raises(ErroDeValidacao) as excinfo:
        publicar_trilha(sessao, trilha, operador=mestre)
    assert "sondagem" in excinfo.value.mensagem
    assert trilha.situacao == SituacaoDaTrilha.rascunho


def test_trilha_sem_desafio_de_coleta_e_recusada(sessao, criar_persona, criar_trilha, criar_missao):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    criar_missao(trilha, mestre, posicao=1, e_sondagem=True)
    _declarar_culminancia(sessao, trilha, mestre)

    with pytest.raises(ErroDeValidacao) as excinfo:
        publicar_trilha(sessao, trilha, operador=mestre)
    assert "desafio de coleta" in excinfo.value.mensagem
    assert trilha.situacao == SituacaoDaTrilha.rascunho


def test_trilha_sem_culminancia_e_recusada(
    sessao, criar_persona, criar_trilha, criar_missao, criar_desafio_de_coleta
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre, posicao=1, e_sondagem=True)
    criar_desafio_de_coleta(missao, mestre)

    with pytest.raises(ErroDeValidacao) as excinfo:
        publicar_trilha(sessao, trilha, operador=mestre)
    assert "culminância" in excinfo.value.mensagem
    assert trilha.situacao == SituacaoDaTrilha.rascunho


def test_recusa_nomeia_as_tres_travas_juntas(sessao, criar_persona, criar_trilha):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)

    with pytest.raises(ErroDeValidacao) as excinfo:
        publicar_trilha(sessao, trilha, operador=mestre)
    mensagem = excinfo.value.mensagem
    assert "sondagem" in mensagem
    assert "desafio de coleta" in mensagem
    assert "culminância" in mensagem


def test_recompensa_de_marco_sem_lastro_nao_impede_publicacao(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_tipo_de_recurso,
    criar_recompensa_de_marco,
):
    mestre = criar_persona(Papel.mestre)
    trilha = _trilha_completa(sessao, criar_trilha, criar_missao, criar_desafio_de_coleta, mestre)
    missao_de_marco = criar_missao(trilha, mestre, posicao=2, e_sondagem=False)
    tipo_de_recurso = criar_tipo_de_recurso(mestre)
    criar_recompensa_de_marco(
        mestre, trilha, missao_de_marco, tipo_de_recurso, quantidade=Decimal("30")
    )

    publicar_trilha(sessao, trilha, operador=mestre)
    sessao.commit()

    assert trilha.situacao == SituacaoDaTrilha.publicada


def test_percurso_preservado_na_despublicacao(
    sessao, criar_persona, criar_trilha, criar_missao, criar_atividade
):
    mestre = criar_persona(Papel.mestre)
    admin = criar_persona(Papel.admin)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    missao = criar_missao(trilha, mestre)
    atividade = criar_atividade(missao, mestre)

    despublicar_trilha(sessao, trilha, operador=admin, motivo="Conteúdo desatualizado.")
    sessao.commit()
    sessao.refresh(missao)
    sessao.refresh(atividade)

    assert trilha.situacao == SituacaoDaTrilha.despublicada
    assert missao.titulo == "Missão de Teste"
    assert atividade.titulo == "Atividade de Teste"
