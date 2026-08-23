from datetime import UTC, datetime

import pytest

from nucleo.coletas.modelo import EstadoDaSerie
from nucleo.erros import ErroDeValidacao, PermissaoNegada
from nucleo.ods.modelo import EtiquetaOds
from nucleo.ods.regra import (
    EtiquetaDeclarada,
    cobertura_por_comunidade,
    cobertura_por_poder,
    cobertura_por_trilha,
    comunidades_com_cobertura,
    criar_etiqueta_ods,
    resolver_etiquetas_da_missao,
    substituir_etiquetas_da_missao,
    substituir_etiquetas_da_trilha,
)
from nucleo.personas.modelo import Papel
from nucleo.pontuacao.modelo import Nivel, PontoRegular
from nucleo.resultados.modelo import DesfechoDoResultado
from nucleo.resultados.regra import registrar_resultado
from nucleo.trilhas.modelo import FormatoDeAtividade, ModalidadeDeAtividade
from nucleo.trilhas.regra import criar_atividade

MOMENTO_DO_FATO = datetime(2026, 8, 1, 10, 0, tzinfo=UTC)


def _lancar_resultado(sessao, *, mestre, guerreiro, missao):
    from tests.conftest import criar_aula_para_resultado

    atividade = criar_atividade(
        sessao,
        operador=mestre,
        missao=missao,
        titulo="Atividade de Teste",
        modalidade=ModalidadeDeAtividade.individual,
        formato=FormatoDeAtividade.presencial,
        natureza="construcao",
        producao_esperada="Produção esperada.",
    )
    aula = criar_aula_para_resultado(sessao, mestre)
    sessao.commit()
    resultado = registrar_resultado(
        sessao,
        operador=mestre,
        aula=aula,
        guerreiro_id=guerreiro.id,
        atividade=atividade,
        momento_do_fato=MOMENTO_DO_FATO,
        producao="Produção do Guerreiro(a).",
        desfecho=DesfechoDoResultado.realizada,
    )
    sessao.commit()
    return resultado


def test_mestre_autor_etiqueta_a_trilha(sessao, criar_persona, criar_trilha):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)

    etiqueta = criar_etiqueta_ods(sessao, operador=mestre, objetivo=4, meta="4.7", trilha=trilha)
    sessao.commit()

    assert etiqueta.trilha_id == trilha.id
    assert etiqueta.missao_id is None
    assert etiqueta.objetivo == 4
    assert etiqueta.meta == "4.7"


def test_mestre_autor_etiqueta_uma_missao_da_trilha(
    sessao, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    etiqueta = criar_etiqueta_ods(sessao, operador=mestre, objetivo=13, missao=missao)
    sessao.commit()

    assert etiqueta.missao_id == missao.id
    assert etiqueta.trilha_id is None


def test_trilha_aceita_mais_de_uma_etiqueta(sessao, criar_persona, criar_trilha):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)

    criar_etiqueta_ods(sessao, operador=mestre, objetivo=4, trilha=trilha)
    criar_etiqueta_ods(sessao, operador=mestre, objetivo=13, trilha=trilha)
    sessao.commit()

    assert sessao.query(EtiquetaOds).filter_by(trilha_id=trilha.id).count() == 2


def test_objetivo_fora_da_faixa_e_recusado(sessao, criar_persona, criar_trilha):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)

    with pytest.raises(ErroDeValidacao):
        criar_etiqueta_ods(sessao, operador=mestre, objetivo=0, trilha=trilha)
    with pytest.raises(ErroDeValidacao):
        criar_etiqueta_ods(sessao, operador=mestre, objetivo=19, trilha=trilha)
    assert sessao.query(EtiquetaOds).count() == 0


def test_etiqueta_sem_trilha_nem_missao_e_recusada(sessao, criar_persona):
    mestre = criar_persona(Papel.mestre)

    with pytest.raises(ErroDeValidacao):
        criar_etiqueta_ods(sessao, operador=mestre, objetivo=4)
    assert sessao.query(EtiquetaOds).count() == 0


def test_etiqueta_com_trilha_e_missao_ao_mesmo_tempo_e_recusada(
    sessao, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    with pytest.raises(ErroDeValidacao):
        criar_etiqueta_ods(sessao, operador=mestre, objetivo=4, trilha=trilha, missao=missao)
    assert sessao.query(EtiquetaOds).count() == 0


def test_mestre_que_nao_e_autor_e_recusado(sessao, criar_persona, criar_trilha):
    autor = criar_persona(Papel.mestre)
    outro_mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(autor)

    with pytest.raises(PermissaoNegada):
        criar_etiqueta_ods(sessao, operador=outro_mestre, objetivo=4, trilha=trilha)
    assert sessao.query(EtiquetaOds).count() == 0


def test_admin_e_recusado(sessao, criar_persona, criar_trilha, criar_missao):
    """Autoria estrita: o Admin não edita a trilha de um Mestre, nem a
    etiqueta dela nem a de uma missão dela (`RF-09-92`, design — decisão
    2)."""
    autor = criar_persona(Papel.mestre)
    admin = criar_persona(Papel.admin)
    trilha = criar_trilha(autor)
    missao = criar_missao(trilha, autor)

    with pytest.raises(PermissaoNegada):
        criar_etiqueta_ods(sessao, operador=admin, objetivo=4, trilha=trilha)
    with pytest.raises(PermissaoNegada):
        criar_etiqueta_ods(sessao, operador=admin, objetivo=4, missao=missao)
    assert sessao.query(EtiquetaOds).count() == 0


def test_missao_com_etiqueta_propria_prevalece_sobre_a_da_trilha(
    sessao, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    criar_etiqueta_ods(sessao, operador=mestre, objetivo=4, trilha=trilha)
    etiqueta_da_missao = criar_etiqueta_ods(sessao, operador=mestre, objetivo=13, missao=missao)
    sessao.commit()

    resolvidas = resolver_etiquetas_da_missao(sessao, missao)

    assert [e.id for e in resolvidas] == [etiqueta_da_missao.id]


def test_missao_sem_etiqueta_propria_herda_a_da_trilha(
    sessao, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    etiqueta_da_trilha = criar_etiqueta_ods(sessao, operador=mestre, objetivo=4, trilha=trilha)
    sessao.commit()

    resolvidas = resolver_etiquetas_da_missao(sessao, missao)

    assert [e.id for e in resolvidas] == [etiqueta_da_trilha.id]


def test_declarar_etiqueta_nao_credita_pontuacao(sessao, criar_persona, criar_trilha):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)

    criar_etiqueta_ods(sessao, operador=mestre, objetivo=4, trilha=trilha)
    sessao.commit()

    assert sessao.query(PontoRegular).count() == 0
    assert sessao.query(Nivel).count() == 0


def _objetivos_da_trilha(sessao, trilha):
    return sorted(
        objetivo
        for (objetivo,) in sessao.query(EtiquetaOds.objetivo).filter_by(trilha_id=trilha.id)
    )


def _objetivos_da_missao(sessao, missao):
    return sorted(
        objetivo
        for (objetivo,) in sessao.query(EtiquetaOds.objetivo).filter_by(missao_id=missao.id)
    )


def test_a_lista_recebida_substitui_o_conjunto_anterior(sessao, criar_persona, criar_trilha):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    criar_etiqueta_ods(sessao, operador=mestre, objetivo=11, trilha=trilha)
    criar_etiqueta_ods(sessao, operador=mestre, objetivo=4, trilha=trilha)
    sessao.commit()

    substituir_etiquetas_da_trilha(
        sessao,
        operador=mestre,
        trilha=trilha,
        etiquetas=[EtiquetaDeclarada(objetivo=4), EtiquetaDeclarada(objetivo=13, meta="13.3")],
    )
    sessao.commit()

    assert _objetivos_da_trilha(sessao, trilha) == [4, 13]


def test_lista_vazia_deixa_o_alvo_sem_etiqueta(sessao, criar_persona, criar_trilha):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    criar_etiqueta_ods(sessao, operador=mestre, objetivo=4, trilha=trilha)
    sessao.commit()

    substituir_etiquetas_da_trilha(sessao, operador=mestre, trilha=trilha, etiquetas=[])
    sessao.commit()

    assert _objetivos_da_trilha(sessao, trilha) == []


def test_a_substituicao_e_idempotente(sessao, criar_persona, criar_trilha):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    lista = [EtiquetaDeclarada(objetivo=4, meta="4.7"), EtiquetaDeclarada(objetivo=13)]

    substituir_etiquetas_da_trilha(sessao, operador=mestre, trilha=trilha, etiquetas=lista)
    sessao.commit()
    substituir_etiquetas_da_trilha(sessao, operador=mestre, trilha=trilha, etiquetas=lista)
    sessao.commit()

    assert _objetivos_da_trilha(sessao, trilha) == [4, 13]


def test_substituir_na_trilha_nao_toca_as_etiquetas_das_missoes(
    sessao, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    criar_etiqueta_ods(sessao, operador=mestre, objetivo=4, trilha=trilha)
    criar_etiqueta_ods(sessao, operador=mestre, objetivo=13, missao=missao)
    sessao.commit()

    substituir_etiquetas_da_trilha(
        sessao, operador=mestre, trilha=trilha, etiquetas=[EtiquetaDeclarada(objetivo=11)]
    )
    sessao.commit()

    assert _objetivos_da_missao(sessao, missao) == [13]
    assert [e.objetivo for e in resolver_etiquetas_da_missao(sessao, missao)] == [13]


def test_substituir_na_missao_nao_toca_as_etiquetas_da_trilha(
    sessao, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    criar_etiqueta_ods(sessao, operador=mestre, objetivo=4, trilha=trilha)
    criar_etiqueta_ods(sessao, operador=mestre, objetivo=13, missao=missao)
    sessao.commit()

    substituir_etiquetas_da_missao(
        sessao, operador=mestre, missao=missao, etiquetas=[EtiquetaDeclarada(objetivo=6)]
    )
    sessao.commit()

    assert _objetivos_da_trilha(sessao, trilha) == [4]
    assert _objetivos_da_missao(sessao, missao) == [6]


def test_uma_etiqueta_invalida_recusa_a_operacao_inteira(sessao, criar_persona, criar_trilha):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    criar_etiqueta_ods(sessao, operador=mestre, objetivo=4, trilha=trilha)
    sessao.commit()

    with pytest.raises(ErroDeValidacao):
        substituir_etiquetas_da_trilha(
            sessao,
            operador=mestre,
            trilha=trilha,
            etiquetas=[EtiquetaDeclarada(objetivo=11), EtiquetaDeclarada(objetivo=19)],
        )
    sessao.rollback()

    assert _objetivos_da_trilha(sessao, trilha) == [4]


def test_substituicao_recusa_quem_nao_e_o_mestre_autor(
    sessao, criar_persona, criar_trilha, criar_missao
):
    autor = criar_persona(Papel.mestre)
    outro_mestre = criar_persona(Papel.mestre)
    admin = criar_persona(Papel.admin)
    trilha = criar_trilha(autor)
    missao = criar_missao(trilha, autor)
    criar_etiqueta_ods(sessao, operador=autor, objetivo=4, trilha=trilha)
    sessao.commit()

    for operador in (outro_mestre, admin):
        with pytest.raises(PermissaoNegada):
            substituir_etiquetas_da_trilha(sessao, operador=operador, trilha=trilha, etiquetas=[])
        with pytest.raises(PermissaoNegada):
            substituir_etiquetas_da_missao(sessao, operador=operador, missao=missao, etiquetas=[])
    sessao.rollback()

    assert _objetivos_da_trilha(sessao, trilha) == [4]


def test_substituir_etiqueta_nao_reprocessa_pontuacao(
    sessao, criar_persona, criar_comunidade, criar_trilha, criar_missao
):
    """`RN-01-23`: a etiqueta não pontua, então trocá-la não recalcula,
    estorna nem credita nada sobre registros já creditados."""
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade("Comunidade da substituição")
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    criar_etiqueta_ods(sessao, operador=mestre, objetivo=4, trilha=trilha)
    sessao.commit()
    _lancar_resultado(sessao, mestre=mestre, guerreiro=guerreiro, missao=missao)

    pontos_antes = [(p.id, p.total) for p in sessao.query(PontoRegular).order_by(PontoRegular.id)]
    assert pontos_antes, "o cenário exige crédito já lançado para valer como regressão"
    niveis_antes = [(n.id, n.valor) for n in sessao.query(Nivel).order_by(Nivel.id)]

    substituir_etiquetas_da_trilha(
        sessao, operador=mestre, trilha=trilha, etiquetas=[EtiquetaDeclarada(objetivo=13)]
    )
    sessao.commit()

    assert [
        (p.id, p.total) for p in sessao.query(PontoRegular).order_by(PontoRegular.id)
    ] == pontos_antes
    assert [(n.id, n.valor) for n in sessao.query(Nivel).order_by(Nivel.id)] == niveis_antes


def test_cobertura_por_trilha_soma_trilha_e_missoes(
    sessao, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    criar_etiqueta_ods(sessao, operador=mestre, objetivo=4, trilha=trilha)
    criar_etiqueta_ods(sessao, operador=mestre, objetivo=13, missao=missao)
    sessao.commit()

    cobertura = cobertura_por_trilha(sessao, trilha.id)

    assert cobertura == {4, 13}


def test_cobertura_por_poder_soma_as_trilhas_do_poder(
    sessao, criar_persona, criar_poder, criar_trilha
):
    mestre = criar_persona(Papel.mestre)
    poder = criar_poder(mestre)
    trilha_1 = criar_trilha(mestre, poder=poder)
    trilha_2 = criar_trilha(mestre, poder=poder)
    criar_etiqueta_ods(sessao, operador=mestre, objetivo=4, trilha=trilha_1)
    criar_etiqueta_ods(sessao, operador=mestre, objetivo=13, trilha=trilha_2)
    sessao.commit()

    cobertura = cobertura_por_poder(sessao, poder.id)

    assert cobertura == {4, 13}


def test_cobertura_por_comunidade_soma_trilhas_em_curso(
    sessao, criar_persona, criar_comunidade, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    criar_etiqueta_ods(sessao, operador=mestre, objetivo=4, trilha=trilha)
    sessao.commit()

    _lancar_resultado(sessao, mestre=mestre, guerreiro=guerreiro, missao=missao)

    cobertura = cobertura_por_comunidade(sessao, comunidade.id)

    assert cobertura == {4}


def test_cobertura_por_comunidade_sem_resultado_e_vazia(
    sessao, criar_persona, criar_comunidade, criar_trilha
):
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    trilha = criar_trilha(mestre)
    criar_etiqueta_ods(sessao, operador=mestre, objetivo=4, trilha=trilha)
    sessao.commit()

    cobertura = cobertura_por_comunidade(sessao, comunidade.id)

    assert cobertura == set()


def _montar_desafio_etiquetado(
    sessao,
    *,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
    criar_desafio_de_coleta,
    objetivo: int = 11,
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    criar_etiqueta_ods(sessao, operador=mestre, objetivo=objetivo, missao=missao)
    sessao.commit()
    tipo = criar_tipo_de_coleta(mestre)
    desafio = criar_desafio_de_coleta(missao, mestre, tipo=tipo)
    return desafio


def test_cobertura_por_comunidade_soma_desafios_de_coleta_com_serie_aberta(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
    criar_desafio_de_coleta,
    criar_local,
    criar_serie_de_coleta,
):
    """4.10: `RF-08-26` soma trilha e coleta, e o objetivo etiquetado nas
    duas fontes aparece uma só vez."""
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    local = criar_local(comunidade)
    desafio = _montar_desafio_etiquetado(
        sessao,
        criar_persona=criar_persona,
        criar_trilha=criar_trilha,
        criar_missao=criar_missao,
        criar_tipo_de_coleta=criar_tipo_de_coleta,
        criar_desafio_de_coleta=criar_desafio_de_coleta,
        objetivo=11,
    )
    criar_serie_de_coleta(guerreiro, desafio, local)

    cobertura = cobertura_por_comunidade(sessao, comunidade.id)

    assert cobertura == {11}


def test_comunidade_so_com_coleta_cobre_o_objetivo_do_desafio(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
    criar_desafio_de_coleta,
    criar_local,
    criar_serie_de_coleta,
):
    """4.11: comunidade sem Resultado registrado e com série aberta sobre
    desafio etiquetado aparece na cobertura, com o objetivo do desafio."""
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    local = criar_local(comunidade)
    desafio = _montar_desafio_etiquetado(
        sessao,
        criar_persona=criar_persona,
        criar_trilha=criar_trilha,
        criar_missao=criar_missao,
        criar_tipo_de_coleta=criar_tipo_de_coleta,
        criar_desafio_de_coleta=criar_desafio_de_coleta,
        objetivo=6,
    )
    criar_serie_de_coleta(guerreiro, desafio, local)

    assert comunidade.id in comunidades_com_cobertura(sessao)
    assert cobertura_por_comunidade(sessao, comunidade.id) == {6}


def test_estado_da_serie_nao_altera_a_cobertura(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
    criar_desafio_de_coleta,
    criar_local,
    criar_serie_de_coleta,
):
    """4.12: série interrompida ou encerrada continua cobrindo o objetivo
    do desafio — a cobertura mede alcance declarado, não continuidade."""
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    local = criar_local(comunidade)
    desafio = _montar_desafio_etiquetado(
        sessao,
        criar_persona=criar_persona,
        criar_trilha=criar_trilha,
        criar_missao=criar_missao,
        criar_tipo_de_coleta=criar_tipo_de_coleta,
        criar_desafio_de_coleta=criar_desafio_de_coleta,
        objetivo=15,
    )
    criar_serie_de_coleta(guerreiro, desafio, local, estado=EstadoDaSerie.encerrada)

    assert cobertura_por_comunidade(sessao, comunidade.id) == {15}


def test_cobertura_de_comunidade_nunca_e_calculada_por_guerreiro(sessao):
    """4.13: nenhuma função do núcleo agrega cobertura de ODS por
    Guerreiro(a) — as agregações são por trilha, poder, comunidade e ciclo
    (`RN-08-22`, invariante 20 do documento 99 §6)."""
    import nucleo.ods.regra as modulo_de_regra

    nomes_das_funcoes_publicas = {nome for nome in dir(modulo_de_regra) if not nome.startswith("_")}
    assert not any("guerreiro" in nome.lower() for nome in nomes_das_funcoes_publicas)
