from datetime import UTC, datetime

import pytest
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError

from nucleo.criacoes_originais.regra import (
    devolver_criacao_original,
    entregar_criacao_original,
    validar_criacao_original,
)
from nucleo.equipes.regra import entrar_na_equipe
from nucleo.erros import DebitoDePontoRegularRecusado, ErroDeValidacao
from nucleo.personas.modelo import Papel
from nucleo.pontuacao.modelo import Badge, Nivel, PontoRegular, TipoDeBadge
from nucleo.pontuacao.regra import creditar_ponto_regular, debitar_ponto_regular
from nucleo.resultados.modelo import DesfechoDoResultado, Resultado
from nucleo.resultados.regra import registrar_resultado
from nucleo.trilhas.modelo import FormatoDeAtividade, ModalidadeDeAtividade

MOMENTO_DO_FATO = datetime(2026, 8, 1, 10, 0, tzinfo=UTC)


def _lancar(sessao, *, mestre, guerreiro, missao, desfecho=DesfechoDoResultado.realizada, **kwargs):
    from nucleo.trilhas.regra import criar_atividade
    from tests.conftest import criar_aula_para_resultado

    atividade = criar_atividade(
        sessao,
        operador=mestre,
        missao=missao,
        modalidade=kwargs.pop("modalidade", ModalidadeDeAtividade.individual),
        formato=FormatoDeAtividade.presencial,
        natureza=kwargs.pop("natureza", "construcao"),
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
        desfecho=desfecho,
    )
    sessao.commit()
    return resultado


def test_resultado_realizada_credita_o_valor_base_pela_modalidade(
    sessao, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    _lancar(
        sessao,
        mestre=mestre,
        guerreiro=guerreiro,
        missao=missao,
        modalidade=ModalidadeDeAtividade.individual,
    )

    conta = (
        sessao.query(PontoRegular).filter_by(guerreiro_id=guerreiro.id, trilha_id=trilha.id).one()
    )
    assert conta.total == 10


def test_resultado_em_equipe_com_familiar_credita_vinte(
    sessao, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    _lancar(
        sessao,
        mestre=mestre,
        guerreiro=guerreiro,
        missao=missao,
        modalidade=ModalidadeDeAtividade.em_equipe_com_familiar,
    )

    conta = (
        sessao.query(PontoRegular).filter_by(guerreiro_id=guerreiro.id, trilha_id=trilha.id).one()
    )
    assert conta.total == 20


def test_resultado_realizada_com_merito_credita_o_valor_base_mais_cinco(
    sessao, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    _lancar(
        sessao,
        mestre=mestre,
        guerreiro=guerreiro,
        missao=missao,
        desfecho=DesfechoDoResultado.realizada_com_merito,
    )

    conta = (
        sessao.query(PontoRegular).filter_by(guerreiro_id=guerreiro.id, trilha_id=trilha.id).one()
    )
    assert conta.total == 15


def test_resultado_merito_extra_por_auxilio_credita_o_valor_base_mais_dez(
    sessao, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    _lancar(
        sessao,
        mestre=mestre,
        guerreiro=guerreiro,
        missao=missao,
        desfecho=DesfechoDoResultado.merito_extra_por_auxilio,
    )

    conta = (
        sessao.query(PontoRegular).filter_by(guerreiro_id=guerreiro.id, trilha_id=trilha.id).one()
    )
    assert conta.total == 20


def test_credito_de_ponto_regular_com_valor_nao_positivo_e_recusado(
    sessao, criar_persona, criar_trilha
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)

    with pytest.raises(ErroDeValidacao) as excinfo:
        creditar_ponto_regular(sessao, guerreiro_id=guerreiro.id, trilha_id=trilha.id, valor=0)
    assert excinfo.value.campo == "valor"
    assert sessao.query(PontoRegular).count() == 0


def test_ponto_regular_recusa_ficar_negativo_pelo_orm(sessao, criar_persona, criar_trilha):
    """`RF-01-57`, `RF-01-69`, `RN-01-55`: a redução em si é aceita — só o
    total negativo é recusado."""
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)

    conta = creditar_ponto_regular(sessao, guerreiro_id=guerreiro.id, trilha_id=trilha.id, valor=10)
    sessao.commit()

    conta.total = 5
    sessao.commit()
    assert sessao.get(PontoRegular, conta.id).total == 5

    conta.total = -1
    with pytest.raises(DebitoDePontoRegularRecusado):
        sessao.commit()
    sessao.rollback()

    conta_intacta = sessao.get(PontoRegular, conta.id)
    assert conta_intacta.total == 5


def test_ponto_regular_recusa_negativo_e_remocao_direto_no_banco(
    engine, sessao, criar_persona, criar_trilha
):
    """Fora do ORM — direto no banco — o gatilho da migração recusa também
    (`RF-01-57`, `RN-01-38`, `RN-01-55`, mesmo padrão de `RN-01-12`)."""
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)

    conta = creditar_ponto_regular(sessao, guerreiro_id=guerreiro.id, trilha_id=trilha.id, valor=10)
    sessao.commit()

    with engine.connect() as conexao:
        conexao.execute(
            text("UPDATE ponto_regular SET total = 5 WHERE id = :id"), {"id": str(conta.id)}
        )
        conexao.commit()
    sessao.refresh(conta)

    with engine.connect() as conexao, pytest.raises(DBAPIError):
        conexao.execute(
            text("UPDATE ponto_regular SET total = -1 WHERE id = :id"), {"id": str(conta.id)}
        )
        conexao.commit()

    with engine.connect() as conexao, pytest.raises(DBAPIError):
        conexao.execute(text("DELETE FROM ponto_regular WHERE id = :id"), {"id": str(conta.id)})
        conexao.commit()

    conta_intacta = sessao.get(PontoRegular, conta.id)
    assert conta_intacta is not None
    assert conta_intacta.total == 5


def test_debito_de_ponto_regular_com_valor_nao_positivo_e_recusado(
    sessao, criar_persona, criar_trilha
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    creditar_ponto_regular(sessao, guerreiro_id=guerreiro.id, trilha_id=trilha.id, valor=5)
    sessao.commit()

    with pytest.raises(ErroDeValidacao) as excinfo:
        debitar_ponto_regular(sessao, guerreiro_id=guerreiro.id, trilha_id=trilha.id, valor=0)
    assert excinfo.value.campo == "valor"


def test_debito_maior_que_o_saldo_para_em_zero(sessao, criar_persona, criar_trilha):
    """`RF-01-57`, `RF-01-69`, `RN-01-55`: o débito por fato desfeito nunca
    deixa o saldo negativo."""
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    creditar_ponto_regular(sessao, guerreiro_id=guerreiro.id, trilha_id=trilha.id, valor=5)
    sessao.commit()

    conta = debitar_ponto_regular(sessao, guerreiro_id=guerreiro.id, trilha_id=trilha.id, valor=10)
    sessao.commit()

    assert conta.total == 0


def test_debito_nao_derruba_nivel_nem_badge_ja_conquistados(
    sessao, criar_persona, criar_trilha, criar_missao
):
    """`RF-01-70`, `RN-01-55`: nível e badge persistem mesmo que o saldo
    caia depois de certificados."""
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre, obrigatoria=False)
    _lancar(sessao, mestre=mestre, guerreiro=guerreiro, missao=missao)

    nivel_antes = (
        sessao.query(Nivel).filter_by(guerreiro_id=guerreiro.id, trilha_id=trilha.id).one()
    )
    badge_antes = (
        sessao.query(Badge)
        .filter_by(guerreiro_id=guerreiro.id, trilha_id=trilha.id, tipo=TipoDeBadge.de_nivel)
        .one()
    )

    debitar_ponto_regular(sessao, guerreiro_id=guerreiro.id, trilha_id=trilha.id, valor=10)
    sessao.commit()

    conta = (
        sessao.query(PontoRegular).filter_by(guerreiro_id=guerreiro.id, trilha_id=trilha.id).one()
    )
    assert conta.total == 0
    nivel_depois = (
        sessao.query(Nivel).filter_by(guerreiro_id=guerreiro.id, trilha_id=trilha.id).one()
    )
    badge_depois = (
        sessao.query(Badge)
        .filter_by(guerreiro_id=guerreiro.id, trilha_id=trilha.id, tipo=TipoDeBadge.de_nivel)
        .one()
    )
    assert nivel_depois.id == nivel_antes.id
    assert badge_depois.id == badge_antes.id


def test_primeira_atividade_realizada_certifica_nivel_1(
    sessao, criar_persona, criar_trilha, criar_missao
):
    """Missão opcional: só o nível 1 entra em jogo, sem a trilha ter
    obrigatória para também disparar o nível 2 nesta única missão."""
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre, obrigatoria=False)

    _lancar(sessao, mestre=mestre, guerreiro=guerreiro, missao=missao)

    nivel = sessao.query(Nivel).filter_by(guerreiro_id=guerreiro.id, trilha_id=trilha.id).one()
    assert nivel.valor == 1


def test_um_terco_das_obrigatorias_desbloqueadas_certifica_nivel_2(
    sessao, criar_persona, criar_trilha, criar_missao
):
    """Quatro obrigatórias, arredondando 1/3 para cima: exige duas
    concluídas — uma só basta para o nível 1, não para o nível 2."""
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    missoes = [
        criar_missao(trilha, mestre, posicao=posicao, obrigatoria=True) for posicao in range(1, 5)
    ]

    _lancar(sessao, mestre=mestre, guerreiro=guerreiro, missao=missoes[0])
    niveis = {
        n.valor
        for n in sessao.query(Nivel).filter_by(guerreiro_id=guerreiro.id, trilha_id=trilha.id)
    }
    assert niveis == {1}

    _lancar(sessao, mestre=mestre, guerreiro=guerreiro, missao=missoes[1])
    niveis = {
        n.valor
        for n in sessao.query(Nivel).filter_by(guerreiro_id=guerreiro.id, trilha_id=trilha.id)
    }
    assert niveis == {1, 2}


def test_missao_opcional_nao_conta_para_o_nivel_2(
    sessao, criar_persona, criar_trilha, criar_missao
):
    """Só a missão obrigatória conta no percurso (11 §6): completar as
    opcionais não aproxima do limiar de nível 2."""
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    obrigatorias = [
        criar_missao(trilha, mestre, posicao=posicao, obrigatoria=True) for posicao in range(1, 5)
    ]
    opcionais = [
        criar_missao(trilha, mestre, posicao=posicao, obrigatoria=False) for posicao in range(5, 8)
    ]

    _lancar(sessao, mestre=mestre, guerreiro=guerreiro, missao=obrigatorias[0])
    for opcional in opcionais:
        _lancar(sessao, mestre=mestre, guerreiro=guerreiro, missao=opcional)

    niveis = {
        n.valor
        for n in sessao.query(Nivel).filter_by(guerreiro_id=guerreiro.id, trilha_id=trilha.id)
    }
    assert niveis == {1}


def test_todas_obrigatorias_mais_merito_de_auxilio_certificam_nivel_4(
    sessao, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    missoes = [
        criar_missao(trilha, mestre, posicao=posicao, obrigatoria=True) for posicao in range(1, 3)
    ]

    _lancar(sessao, mestre=mestre, guerreiro=guerreiro, missao=missoes[0])
    niveis = {
        n.valor
        for n in sessao.query(Nivel).filter_by(guerreiro_id=guerreiro.id, trilha_id=trilha.id)
    }
    assert 4 not in niveis

    _lancar(
        sessao,
        mestre=mestre,
        guerreiro=guerreiro,
        missao=missoes[1],
        desfecho=DesfechoDoResultado.merito_extra_por_auxilio,
    )
    niveis = {
        n.valor
        for n in sessao.query(Nivel).filter_by(guerreiro_id=guerreiro.id, trilha_id=trilha.id)
    }
    assert niveis == {1, 2, 4}


def test_todas_obrigatorias_sem_merito_de_auxilio_nao_certifica_nivel_4(
    sessao, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    missoes = [
        criar_missao(trilha, mestre, posicao=posicao, obrigatoria=True) for posicao in range(1, 3)
    ]

    for missao in missoes:
        _lancar(sessao, mestre=mestre, guerreiro=guerreiro, missao=missao)

    niveis = {
        n.valor
        for n in sessao.query(Nivel).filter_by(guerreiro_id=guerreiro.id, trilha_id=trilha.id)
    }
    assert 4 not in niveis


def test_nivel_certificado_nao_regride(sessao, criar_persona, criar_trilha, criar_missao):
    """Nível conquistado nunca regride, mesmo que o critério deixe de
    valer depois (`RF-01-21`, 11 §6): o registro nasce e nunca é apagado."""
    from nucleo.pontuacao.regra import avaliar_niveis

    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    resultado = _lancar(sessao, mestre=mestre, guerreiro=guerreiro, missao=missao)
    assert (
        sessao.query(Nivel)
        .filter_by(guerreiro_id=guerreiro.id, trilha_id=trilha.id, valor=1)
        .first()
        is not None
    )

    sessao.query(Resultado).filter_by(id=resultado.id).delete()
    sessao.commit()

    avaliar_niveis(sessao, guerreiro_id=guerreiro.id, trilha_id=trilha.id)
    sessao.commit()

    nivel_ainda_certificado = (
        sessao.query(Nivel)
        .filter_by(guerreiro_id=guerreiro.id, trilha_id=trilha.id, valor=1)
        .first()
    )
    assert nivel_ainda_certificado is not None


def test_badge_de_nivel_concedido_ao_certificar_um_nivel(
    sessao, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre, obrigatoria=False)

    _lancar(sessao, mestre=mestre, guerreiro=guerreiro, missao=missao)

    badge = (
        sessao.query(Badge)
        .filter_by(guerreiro_id=guerreiro.id, trilha_id=trilha.id, tipo=TipoDeBadge.de_nivel)
        .one()
    )
    assert badge.trilha_id == trilha.id
    assert badge.poder_id is None


def test_badge_de_valores_e_causas_concedido_por_natureza_da_atividade(
    sessao, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    _lancar(
        sessao,
        mestre=mestre,
        guerreiro=guerreiro,
        missao=missao,
        natureza="Valores e Temas Transversais",
    )

    badge = (
        sessao.query(Badge)
        .filter_by(
            guerreiro_id=guerreiro.id, trilha_id=trilha.id, tipo=TipoDeBadge.de_valores_e_causas
        )
        .one()
    )
    assert badge.trilha_id == trilha.id


def test_atividade_de_outra_natureza_nao_concede_badge_de_valores_e_causas(
    sessao, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    _lancar(sessao, mestre=mestre, guerreiro=guerreiro, missao=missao, natureza="construcao")

    assert (
        sessao.query(Badge)
        .filter_by(
            guerreiro_id=guerreiro.id, trilha_id=trilha.id, tipo=TipoDeBadge.de_valores_e_causas
        )
        .first()
        is None
    )


def test_validar_criacao_original_credita_cinquenta_pontos_regulares_ao_autor(
    sessao, criar_persona, criar_trilha, criar_equipe
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    equipe = criar_equipe(guerreiro, trilha=trilha)
    criacao = entregar_criacao_original(
        sessao, guerreiro=guerreiro, equipe=equipe, producao="Produção."
    )
    sessao.commit()

    validar_criacao_original(sessao, operador=mestre, criacao=criacao)
    sessao.commit()

    conta = (
        sessao.query(PontoRegular).filter_by(guerreiro_id=guerreiro.id, trilha_id=trilha.id).one()
    )
    assert conta.total == 50


def test_validar_criacao_original_certifica_o_nivel_5_uma_unica_vez(
    sessao, criar_persona, criar_trilha, criar_equipe
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    equipe = criar_equipe(guerreiro, trilha=trilha)
    criacao = entregar_criacao_original(
        sessao, guerreiro=guerreiro, equipe=equipe, producao="Produção."
    )
    sessao.commit()

    validar_criacao_original(sessao, operador=mestre, criacao=criacao)
    sessao.commit()

    niveis = sessao.query(Nivel).filter_by(guerreiro_id=guerreiro.id, trilha_id=trilha.id, valor=5)
    assert niveis.count() == 1


def test_validar_criacao_original_concede_o_badge_de_autoria(
    sessao, criar_persona, criar_trilha, criar_equipe
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    equipe = criar_equipe(guerreiro, trilha=trilha)
    criacao = entregar_criacao_original(
        sessao, guerreiro=guerreiro, equipe=equipe, producao="Produção."
    )
    sessao.commit()

    validar_criacao_original(sessao, operador=mestre, criacao=criacao)
    sessao.commit()

    badge = (
        sessao.query(Badge)
        .filter_by(guerreiro_id=guerreiro.id, trilha_id=trilha.id, tipo=TipoDeBadge.de_autoria)
        .one()
    )
    assert badge.trilha_id == trilha.id


def test_devolver_criacao_original_nao_credita_nada(
    sessao, criar_persona, criar_trilha, criar_equipe
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    equipe = criar_equipe(guerreiro, trilha=trilha)
    criacao = entregar_criacao_original(
        sessao, guerreiro=guerreiro, equipe=equipe, producao="Produção."
    )
    sessao.commit()

    devolver_criacao_original(sessao, operador=mestre, criacao=criacao)
    sessao.commit()

    assert sessao.query(PontoRegular).filter_by(guerreiro_id=guerreiro.id).count() == 0
    assert sessao.query(Nivel).filter_by(guerreiro_id=guerreiro.id).count() == 0
    assert sessao.query(Badge).filter_by(guerreiro_id=guerreiro.id).count() == 0


def test_validar_criacao_original_credita_cada_integrante_da_equipe(
    sessao, criar_persona, criar_trilha, criar_equipe
):
    """`RF-01-64`: os 50 pontos, o nível 5 e o badge de autoria alcançam
    cada integrante — sem rateio pelo tamanho da equipe."""
    mestre = criar_persona(Papel.mestre)
    autor = criar_persona(Papel.guerreiro)
    colega_um = criar_persona(Papel.guerreiro)
    colega_dois = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    equipe = criar_equipe(autor, trilha=trilha)
    entrar_na_equipe(sessao, operador=colega_um, equipe=equipe)
    entrar_na_equipe(sessao, operador=colega_dois, equipe=equipe)
    sessao.commit()

    criacao = entregar_criacao_original(
        sessao, guerreiro=autor, equipe=equipe, producao="Produção da equipe."
    )
    sessao.commit()

    validar_criacao_original(sessao, operador=mestre, criacao=criacao)
    sessao.commit()

    for integrante in (autor, colega_um, colega_dois):
        conta = (
            sessao.query(PontoRegular)
            .filter_by(guerreiro_id=integrante.id, trilha_id=trilha.id)
            .one()
        )
        assert conta.total == 50
        assert (
            sessao.query(Nivel)
            .filter_by(guerreiro_id=integrante.id, trilha_id=trilha.id, valor=5)
            .count()
            == 1
        )
        assert (
            sessao.query(Badge)
            .filter_by(guerreiro_id=integrante.id, trilha_id=trilha.id, tipo=TipoDeBadge.de_autoria)
            .count()
            == 1
        )


def test_equipes_de_tamanhos_diferentes_creditam_os_mesmos_cinquenta_por_integrante(
    sessao, criar_persona, criar_trilha, criar_equipe
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)

    autor_solo = criar_persona(Papel.guerreiro)
    equipe_solo = criar_equipe(autor_solo, trilha=trilha)
    criacao_solo = entregar_criacao_original(
        sessao, guerreiro=autor_solo, equipe=equipe_solo, producao="Produção solo."
    )
    sessao.commit()
    validar_criacao_original(sessao, operador=mestre, criacao=criacao_solo)
    sessao.commit()

    trilha_dois = criar_trilha(mestre, nome="Outra Trilha")
    autor_trio = criar_persona(Papel.guerreiro)
    equipe_trio = criar_equipe(autor_trio, trilha=trilha_dois)
    colega_um = criar_persona(Papel.guerreiro)
    colega_dois = criar_persona(Papel.guerreiro)
    entrar_na_equipe(sessao, operador=colega_um, equipe=equipe_trio)
    entrar_na_equipe(sessao, operador=colega_dois, equipe=equipe_trio)
    sessao.commit()
    criacao_trio = entregar_criacao_original(
        sessao, guerreiro=autor_trio, equipe=equipe_trio, producao="Produção em trio."
    )
    sessao.commit()
    validar_criacao_original(sessao, operador=mestre, criacao=criacao_trio)
    sessao.commit()

    conta_solo = (
        sessao.query(PontoRegular).filter_by(guerreiro_id=autor_solo.id, trilha_id=trilha.id).one()
    )
    conta_trio = (
        sessao.query(PontoRegular)
        .filter_by(guerreiro_id=autor_trio.id, trilha_id=trilha_dois.id)
        .one()
    )
    assert conta_solo.total == conta_trio.total == 50
