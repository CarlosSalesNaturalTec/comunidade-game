import pytest

from nucleo.erros import PermissaoNegada
from nucleo.personas.modelo import Papel
from nucleo.recompensas_de_marco.modelo import RecompensaDeMarco
from nucleo.trilhas.modelo import (
    Atividade,
    DesbloqueioDaMissao,
    InscricaoNaTrilha,
    Missao,
    SituacaoDaTrilha,
    Trilha,
)
from nucleo.trilhas.regra import duplicar_trilha


def _montar_trilha_com_missao_e_atividade(
    criar_persona, criar_poder, criar_trilha, criar_missao, criar_atividade
):
    autor = criar_persona(Papel.mestre)
    poder = criar_poder(autor)
    trilha = criar_trilha(autor, poder=poder, situacao=SituacaoDaTrilha.publicada)
    missao = criar_missao(trilha, autor, posicao=1, cadencia_de_retomada=[2, 7, 21])
    criar_atividade(missao, autor, titulo="Atividade original")
    return autor, trilha, missao


def test_mestre_duplica_trilha_publicada_de_outro_autor(
    sessao, criar_persona, criar_poder, criar_trilha, criar_missao, criar_atividade
):
    autor, trilha, missao = _montar_trilha_com_missao_e_atividade(
        criar_persona, criar_poder, criar_trilha, criar_missao, criar_atividade
    )
    outro_mestre = criar_persona(Papel.mestre)

    copia = duplicar_trilha(sessao, trilha, operador=outro_mestre)
    sessao.commit()

    assert copia.id != trilha.id
    assert copia.autor_id == outro_mestre.id
    assert copia.situacao == SituacaoDaTrilha.rascunho
    assert copia.poder_id == trilha.poder_id

    missoes_da_copia = sessao.query(Missao).filter_by(trilha_id=copia.id).all()
    assert len(missoes_da_copia) == 1
    missao_copiada = missoes_da_copia[0]
    assert missao_copiada.titulo == missao.titulo
    assert missao_copiada.cadencia_de_retomada == [2, 7, 21]

    atividades_da_copia = sessao.query(Atividade).filter_by(missao_id=missao_copiada.id).all()
    assert len(atividades_da_copia) == 1
    assert atividades_da_copia[0].titulo == "Atividade original"


def test_copia_nao_traz_percurso_nem_fato_de_pessoa(
    sessao,
    criar_persona,
    criar_poder,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_inscricao_na_trilha,
    criar_tipo_de_recurso,
    criar_recompensa_de_marco,
):
    autor, trilha, missao = _montar_trilha_com_missao_e_atividade(
        criar_persona, criar_poder, criar_trilha, criar_missao, criar_atividade
    )
    guerreiro = criar_persona(Papel.guerreiro)
    criar_inscricao_na_trilha(guerreiro, trilha)
    sessao.add(DesbloqueioDaMissao(guerreiro_id=guerreiro.id, missao_id=missao.id, aprovado=True))
    tipo = criar_tipo_de_recurso(autor)
    criar_recompensa_de_marco(autor, trilha, missao, tipo)
    sessao.commit()

    copia = duplicar_trilha(sessao, trilha, operador=autor)
    sessao.commit()

    assert sessao.query(InscricaoNaTrilha).filter_by(trilha_id=copia.id).count() == 0
    missoes_da_copia = sessao.query(Missao).filter_by(trilha_id=copia.id).all()
    ids_missoes_da_copia = [m.id for m in missoes_da_copia]
    assert (
        sessao.query(DesbloqueioDaMissao)
        .filter(DesbloqueioDaMissao.missao_id.in_(ids_missoes_da_copia))
        .count()
        == 0
    )
    assert sessao.query(RecompensaDeMarco).filter_by(trilha_id=copia.id).count() == 0


def test_origem_nao_e_alterada(
    sessao, criar_persona, criar_poder, criar_trilha, criar_missao, criar_atividade
):
    autor, trilha, missao = _montar_trilha_com_missao_e_atividade(
        criar_persona, criar_poder, criar_trilha, criar_missao, criar_atividade
    )
    outro_mestre = criar_persona(Papel.mestre)

    duplicar_trilha(sessao, trilha, operador=outro_mestre)
    sessao.commit()
    sessao.refresh(trilha)

    assert trilha.situacao == SituacaoDaTrilha.publicada
    assert trilha.autor_id == autor.id
    assert sessao.query(Missao).filter_by(trilha_id=trilha.id).count() == 1


def test_copia_nasce_em_rascunho(
    sessao, criar_persona, criar_poder, criar_trilha, criar_missao, criar_atividade
):
    autor, trilha, missao = _montar_trilha_com_missao_e_atividade(
        criar_persona, criar_poder, criar_trilha, criar_missao, criar_atividade
    )
    outro_mestre = criar_persona(Papel.mestre)

    copia = duplicar_trilha(sessao, trilha, operador=outro_mestre)
    sessao.commit()

    assert copia.situacao == SituacaoDaTrilha.rascunho


def test_rascunho_de_outro_mestre_nao_se_duplica(sessao, criar_persona, criar_trilha):
    autor = criar_persona(Papel.mestre)
    outro_mestre = criar_persona(Papel.mestre)
    rascunho = criar_trilha(autor, situacao=SituacaoDaTrilha.rascunho)

    with pytest.raises(PermissaoNegada):
        duplicar_trilha(sessao, rascunho, operador=outro_mestre)

    assert sessao.query(Trilha).filter(Trilha.id != rascunho.id).count() == 0


def test_quem_nao_e_mestre_nao_duplica(sessao, criar_persona, criar_trilha):
    autor = criar_persona(Papel.mestre)
    admin = criar_persona(Papel.admin)
    trilha = criar_trilha(autor, situacao=SituacaoDaTrilha.publicada)

    with pytest.raises(PermissaoNegada):
        duplicar_trilha(sessao, trilha, operador=admin)

    assert sessao.query(Trilha).filter(Trilha.id != trilha.id).count() == 0


def test_mestre_duplica_o_proprio_rascunho(sessao, criar_persona, criar_trilha):
    autor = criar_persona(Papel.mestre)
    rascunho = criar_trilha(autor, situacao=SituacaoDaTrilha.rascunho)

    copia = duplicar_trilha(sessao, rascunho, operador=autor)
    sessao.commit()

    assert copia.autor_id == autor.id
    assert copia.situacao == SituacaoDaTrilha.rascunho
