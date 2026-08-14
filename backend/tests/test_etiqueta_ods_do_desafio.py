from nucleo.coletas.regra import resolver_etiquetas_do_desafio
from nucleo.ods.regra import criar_etiqueta_ods
from nucleo.personas.modelo import Papel
from nucleo.pontuacao.modelo import Nivel, PontoRegular


def test_desafio_herda_a_etiqueta_da_missao_que_o_criou(
    sessao, criar_persona, criar_trilha, criar_missao, criar_tipo_de_coleta, criar_desafio_de_coleta
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    criar_etiqueta_ods(sessao, operador=mestre, objetivo=13, missao=missao)
    criar_etiqueta_ods(sessao, operador=mestre, objetivo=4, trilha=trilha)
    sessao.commit()
    desafio = criar_desafio_de_coleta(missao, mestre)

    resolvidas = resolver_etiquetas_do_desafio(sessao, desafio)

    assert [e.objetivo for e in resolvidas] == [13]


def test_desafio_recua_para_a_etiqueta_da_trilha(
    sessao, criar_persona, criar_trilha, criar_missao, criar_desafio_de_coleta
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    criar_etiqueta_ods(sessao, operador=mestre, objetivo=4, trilha=trilha)
    sessao.commit()
    desafio = criar_desafio_de_coleta(missao, mestre)

    resolvidas = resolver_etiquetas_do_desafio(sessao, desafio)

    assert [e.objetivo for e in resolvidas] == [4]


def test_desafio_sem_etiqueta_na_missao_nem_na_trilha_fica_sem_etiqueta(
    sessao, criar_persona, criar_trilha, criar_missao, criar_desafio_de_coleta
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    desafio = criar_desafio_de_coleta(missao, mestre)

    resolvidas = resolver_etiquetas_do_desafio(sessao, desafio)

    assert resolvidas == []


def test_mudar_a_etiqueta_da_missao_muda_a_do_desafio(
    sessao, criar_persona, criar_trilha, criar_missao, criar_desafio_de_coleta
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    criar_etiqueta_ods(sessao, operador=mestre, objetivo=4, trilha=trilha)
    sessao.commit()
    desafio = criar_desafio_de_coleta(missao, mestre)
    assert [e.objetivo for e in resolver_etiquetas_do_desafio(sessao, desafio)] == [4]

    criar_etiqueta_ods(sessao, operador=mestre, objetivo=13, missao=missao)
    sessao.commit()

    resolvidas = resolver_etiquetas_do_desafio(sessao, desafio)
    assert [e.objetivo for e in resolvidas] == [13]


def test_desafio_etiquetado_pontua_igual_ao_nao_etiquetado(
    sessao, criar_persona, criar_trilha, criar_missao, criar_desafio_de_coleta
):
    mestre = criar_persona(Papel.mestre)
    trilha_etiquetada = criar_trilha(mestre)
    trilha_sem_etiqueta = criar_trilha(mestre)
    missao_etiquetada = criar_missao(trilha_etiquetada, mestre)
    missao_sem_etiqueta = criar_missao(trilha_sem_etiqueta, mestre)
    criar_etiqueta_ods(sessao, operador=mestre, objetivo=4, trilha=trilha_etiquetada)
    sessao.commit()

    desafio_etiquetado = criar_desafio_de_coleta(missao_etiquetada, mestre)
    desafio_sem_etiqueta = criar_desafio_de_coleta(missao_sem_etiqueta, mestre)

    assert len(resolver_etiquetas_do_desafio(sessao, desafio_etiquetado)) == 1
    assert resolver_etiquetas_do_desafio(sessao, desafio_sem_etiqueta) == []
    # A etiqueta é descritiva: nenhum ponto é creditado pela sua presença
    # (RN-08-21) — esta fatia não pontua registro algum ainda.
    assert sessao.query(PontoRegular).count() == 0
    assert sessao.query(Nivel).count() == 0


def test_trocar_a_etiqueta_nao_reprocessa_pontuacao(
    sessao, criar_persona, criar_trilha, criar_missao, criar_desafio_de_coleta
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    criar_etiqueta_ods(sessao, operador=mestre, objetivo=4, trilha=trilha)
    sessao.commit()
    criar_desafio_de_coleta(missao, mestre)

    criar_etiqueta_ods(sessao, operador=mestre, objetivo=13, trilha=trilha)
    sessao.commit()

    assert sessao.query(PontoRegular).count() == 0
    assert sessao.query(Nivel).count() == 0
