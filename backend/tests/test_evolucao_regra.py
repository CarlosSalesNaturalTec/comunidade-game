from datetime import UTC, datetime

from nucleo.aulas.modelo import ModoDeComprovacao, Presenca
from nucleo.criacoes_originais.modelo import SituacaoDaCriacaoOriginal
from nucleo.evolucao.regra import listar_ocorrencias_do_guerreiro, montar_evolucao
from nucleo.ocorrencias_de_conduta.modelo import OcorrenciaDeConduta
from nucleo.personas.modelo import Papel
from nucleo.resultados.modelo import DesfechoDoResultado
from nucleo.resultados.regra import registrar_resultado
from nucleo.trilhas.modelo import SituacaoDaTrilha
from tests.conftest import criar_aula_para_resultado

MOMENTO = datetime(2026, 8, 1, 10, 0, tzinfo=UTC)


def test_evolucao_com_historico_traz_presenca_atividades_pontos_poderes_badges_e_nivel(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_ponto_regular,
    criar_inscricao_na_trilha,
    criar_criacao_original,
    criar_poder,
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    missao = criar_missao(trilha, mestre, titulo="Missão 1")
    atividade = criar_atividade(missao, mestre, titulo="Atividade 1")
    aula = criar_aula_para_resultado(sessao, mestre)
    criar_inscricao_na_trilha(guerreiro, trilha)

    # `registrar_resultado` já credita ponto regular, reavalia nível e badge
    # da trilha — a evolução só reproduz o que essa apuração já gravou
    # (design — decisão 2), sem recalcular nada por conta própria.
    registrar_resultado(
        sessao,
        operador=mestre,
        aula=aula,
        guerreiro_id=guerreiro.id,
        atividade=atividade,
        momento_do_fato=MOMENTO,
        producao="Produção do Guerreiro(a).",
        desfecho=DesfechoDoResultado.realizada,
    )
    sessao.add(
        Presenca(
            aula_id=aula.id,
            guerreiro_id=guerreiro.id,
            modo=ModoDeComprovacao.confirmacao,
            confirmador_id=mestre.id,
            momento_do_fato=MOMENTO,
            autor_id=mestre.id,
            papel_do_autor=mestre.papel.value,
        )
    )
    poder_do_territorio = criar_poder(mestre, nome="Poder do Território")
    criar_ponto_regular(guerreiro, poder=poder_do_territorio, total=15)
    criar_criacao_original(
        trilha, guerreiro, guerreiro=guerreiro, situacao=SituacaoDaCriacaoOriginal.validada
    )
    sessao.commit()

    evolucao = montar_evolucao(sessao, guerreiro_id=guerreiro.id)

    assert len(evolucao.presencas) == 1
    assert evolucao.presencas[0].aula_id == aula.id

    assert len(evolucao.atividades) == 1
    assert evolucao.atividades[0].atividade_titulo == "Atividade 1"
    assert evolucao.atividades[0].desfecho == DesfechoDoResultado.realizada

    assert len(evolucao.progresso_das_trilhas) == 1
    assert evolucao.progresso_das_trilhas[0].nivel_atual is not None
    assert evolucao.progresso_das_trilhas[0].badges != []

    assert len(evolucao.pontos_por_poder) == 1
    assert evolucao.pontos_por_poder[0].poder_id == poder_do_territorio.id
    assert evolucao.pontos_por_poder[0].total == 15

    assert len(evolucao.criacoes_validadas) == 1
    assert evolucao.criacoes_validadas[0].trilha_titulo == trilha.nome


def test_evolucao_de_recem_cadastrado_vem_vazia_sem_falhar(sessao, criar_persona):
    guerreiro = criar_persona(Papel.guerreiro)

    evolucao = montar_evolucao(sessao, guerreiro_id=guerreiro.id)

    assert evolucao.presencas == []
    assert evolucao.atividades == []
    assert evolucao.progresso_das_trilhas == []
    assert evolucao.pontos_por_poder == []
    assert evolucao.criacoes_validadas == []


def test_percurso_da_trilha_vem_em_missoes_concluidas_e_faltantes_nunca_como_saldo(
    sessao, criar_persona, criar_trilha, criar_missao, criar_inscricao_na_trilha
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    criar_missao(trilha, mestre, posicao=1, obrigatoria=True)
    criar_missao(trilha, mestre, posicao=2, obrigatoria=True)
    criar_inscricao_na_trilha(guerreiro, trilha)
    sessao.commit()

    evolucao = montar_evolucao(sessao, guerreiro_id=guerreiro.id)

    item = evolucao.progresso_das_trilhas[0]
    assert item.obrigatorias_desbloqueadas == 0
    assert item.obrigatorias_totais == 2


def test_criacao_validada_aparece_e_a_nao_validada_nao(
    sessao, criar_persona, criar_trilha, criar_criacao_original
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha_validada = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada, nome="Validada")
    trilha_entregue = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada, nome="Entregue")
    criar_criacao_original(
        trilha_validada,
        guerreiro,
        guerreiro=guerreiro,
        situacao=SituacaoDaCriacaoOriginal.validada,
    )
    criar_criacao_original(
        trilha_entregue,
        guerreiro,
        guerreiro=guerreiro,
        situacao=SituacaoDaCriacaoOriginal.entregue,
    )
    sessao.commit()

    evolucao = montar_evolucao(sessao, guerreiro_id=guerreiro.id)

    titulos = [item.trilha_titulo for item in evolucao.criacoes_validadas]
    assert titulos == ["Validada"]


def test_ocorrencia_com_motivo_e_ocorrencia_ja_expurgada(
    sessao, criar_persona, criar_trilha, criar_missao, criar_atividade
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    missao = criar_missao(trilha, mestre)
    atividade = criar_atividade(missao, mestre)
    aula = criar_aula_para_resultado(sessao, mestre)

    com_motivo = OcorrenciaDeConduta(
        guerreiro_id=guerreiro.id,
        aula_id=aula.id,
        atividade_id=atividade.id,
        valor=5,
        valor_debitado=5,
        motivo="Desrespeitou um colega.",
        momento_do_fato=MOMENTO,
        autor_id=mestre.id,
        papel_do_autor=mestre.papel.value,
    )
    expurgada = OcorrenciaDeConduta(
        guerreiro_id=guerreiro.id,
        aula_id=aula.id,
        atividade_id=atividade.id,
        valor=5,
        valor_debitado=5,
        motivo=None,
        momento_do_fato=MOMENTO,
        autor_id=mestre.id,
        papel_do_autor=mestre.papel.value,
    )
    sessao.add_all([com_motivo, expurgada])
    sessao.commit()

    ocorrencias = listar_ocorrencias_do_guerreiro(sessao, guerreiro_id=guerreiro.id)

    assert len(ocorrencias) == 2
    motivos = {ocorrencia.motivo for ocorrencia in ocorrencias}
    assert motivos == {"Desrespeitou um colega.", None}
