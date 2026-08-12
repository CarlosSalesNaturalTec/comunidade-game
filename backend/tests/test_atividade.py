import pytest

from nucleo.erros import ErroDeValidacao, PermissaoNegada
from nucleo.personas.modelo import Papel
from nucleo.trilhas.modelo import Atividade, FormatoDeAtividade, ModalidadeDeAtividade
from nucleo.trilhas.regra import criar_atividade


def test_atividade_criada_dentro_de_uma_missao(sessao, criar_persona, criar_trilha, criar_missao):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    atividade = criar_atividade(
        sessao,
        operador=mestre,
        missao=missao,
        modalidade=ModalidadeDeAtividade.individual,
        formato=FormatoDeAtividade.presencial,
        natureza="construcao",
        producao_esperada="Construir o próprio robô.",
    )
    sessao.commit()

    assert atividade.missao_id == missao.id
    assert atividade.autor_id == mestre.id
    assert atividade.registrado_em is not None


def test_atividade_sem_missao_e_recusada(sessao, criar_persona):
    mestre = criar_persona(Papel.mestre)

    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_atividade(
            sessao,
            operador=mestre,
            missao=None,
            modalidade=ModalidadeDeAtividade.individual,
            formato=FormatoDeAtividade.presencial,
            natureza="construcao",
            producao_esperada="Construir algo.",
        )
    assert excinfo.value.campo == "missao_id"
    assert sessao.query(Atividade).count() == 0


def test_mestre_que_nao_e_autor_e_recusado(sessao, criar_persona, criar_trilha, criar_missao):
    mestre_autor = criar_persona(Papel.mestre)
    outro_mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre_autor)
    missao = criar_missao(trilha, mestre_autor)

    with pytest.raises(PermissaoNegada):
        criar_atividade(
            sessao,
            operador=outro_mestre,
            missao=missao,
            modalidade=ModalidadeDeAtividade.individual,
            formato=FormatoDeAtividade.presencial,
            natureza="construcao",
            producao_esperada="Construir algo.",
        )
    assert sessao.query(Atividade).count() == 0


def test_eixos_se_combinam_livremente(sessao, criar_persona, criar_trilha, criar_missao):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    atividade = criar_atividade(
        sessao,
        operador=mestre,
        missao=missao,
        modalidade=ModalidadeDeAtividade.em_equipe,
        formato=FormatoDeAtividade.presencial,
        natureza="construcao",
        producao_esperada="Construir atacante, escudo e torre.",
    )
    sessao.commit()

    assert atividade.modalidade == ModalidadeDeAtividade.em_equipe
    assert atividade.formato == FormatoDeAtividade.presencial
    assert atividade.natureza == "construcao"


def test_atividade_sem_modalidade_e_recusada(sessao, criar_persona, criar_trilha, criar_missao):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_atividade(
            sessao,
            operador=mestre,
            missao=missao,
            modalidade=None,
            formato=FormatoDeAtividade.presencial,
            natureza="construcao",
            producao_esperada="Construir algo.",
        )
    assert excinfo.value.campo == "modalidade"
    assert sessao.query(Atividade).count() == 0


def test_atividade_sem_formato_e_recusada(sessao, criar_persona, criar_trilha, criar_missao):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_atividade(
            sessao,
            operador=mestre,
            missao=missao,
            modalidade=ModalidadeDeAtividade.individual,
            formato=None,
            natureza="construcao",
            producao_esperada="Construir algo.",
        )
    assert excinfo.value.campo == "formato"
    assert sessao.query(Atividade).count() == 0


def test_natureza_nova_e_aceita(sessao, criar_persona, criar_trilha, criar_missao):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    atividade = criar_atividade(
        sessao,
        operador=mestre,
        missao=missao,
        modalidade=ModalidadeDeAtividade.individual,
        formato=FormatoDeAtividade.presencial,
        natureza="expressao_artistica",
        producao_esperada="Declamar uma rima.",
    )
    sessao.commit()

    assert atividade.natureza == "expressao_artistica"


def test_natureza_e_normalizada_antes_de_gravar(sessao, criar_persona, criar_trilha, criar_missao):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    atividade = criar_atividade(
        sessao,
        operador=mestre,
        missao=missao,
        modalidade=ModalidadeDeAtividade.individual,
        formato=FormatoDeAtividade.presencial,
        natureza="  Construção  ",
        producao_esperada="Construir algo.",
    )
    sessao.commit()

    assert atividade.natureza == "construção"


def test_modalidade_fora_dos_valores_previstos_e_recusada(
    sessao, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_atividade(
            sessao,
            operador=mestre,
            missao=missao,
            modalidade="modalidade-inexistente",
            formato=FormatoDeAtividade.presencial,
            natureza="construcao",
            producao_esperada="Construir algo.",
        )
    assert excinfo.value.campo == "modalidade"
    assert sessao.query(Atividade).count() == 0


def test_formato_fora_dos_valores_previstos_e_recusada(
    sessao, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_atividade(
            sessao,
            operador=mestre,
            missao=missao,
            modalidade=ModalidadeDeAtividade.individual,
            formato="formato-inexistente",
            natureza="construcao",
            producao_esperada="Construir algo.",
        )
    assert excinfo.value.campo == "formato"
    assert sessao.query(Atividade).count() == 0


def test_atividade_sem_natureza_e_recusada(sessao, criar_persona, criar_trilha, criar_missao):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_atividade(
            sessao,
            operador=mestre,
            missao=missao,
            modalidade=ModalidadeDeAtividade.individual,
            formato=FormatoDeAtividade.presencial,
            natureza="",
            producao_esperada="Construir algo.",
        )
    assert excinfo.value.campo == "natureza"
    assert sessao.query(Atividade).count() == 0


def test_atividade_com_producao_declarada(sessao, criar_persona, criar_trilha, criar_missao):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    atividade = criar_atividade(
        sessao,
        operador=mestre,
        missao=missao,
        modalidade=ModalidadeDeAtividade.individual,
        formato=FormatoDeAtividade.presencial,
        natureza="construcao",
        producao_esperada="Construir o próprio robô.",
    )
    sessao.commit()

    assert atividade.producao_esperada == "Construir o próprio robô."


def test_atividade_sem_producao_e_recusada(sessao, criar_persona, criar_trilha, criar_missao):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_atividade(
            sessao,
            operador=mestre,
            missao=missao,
            modalidade=ModalidadeDeAtividade.individual,
            formato=FormatoDeAtividade.presencial,
            natureza="construcao",
            producao_esperada=None,
        )
    assert excinfo.value.campo == "producao_esperada"
    assert sessao.query(Atividade).count() == 0
