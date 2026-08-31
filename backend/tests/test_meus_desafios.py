"""A porta HTTP dos desafios em aberto do Guerreiro(a) em sessão —
`RF-05-19`, `RN-05-21`, `RN-05-06`, do PRD-05 §9."""

from datetime import UTC, datetime

from nucleo.personas.modelo import Papel
from nucleo.resultados.modelo import DesfechoDoResultado
from nucleo.resultados.regra import registrar_resultado
from nucleo.trilhas.modelo import SituacaoDaTrilha
from tests.conftest import criar_aula_para_resultado

MOMENTO_DO_FATO = datetime(2026, 8, 1, 10, 0, tzinfo=UTC)


def _cabecalhos(chave, token):
    return {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}


def test_atividade_de_missao_desbloqueada_e_devolvida_com_modalidade_e_formato(
    cliente,
    criar_chave,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_inscricao_na_trilha,
    criar_desbloqueio_da_missao,
    criar_sessao_de_teste,
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    missao = criar_missao(trilha, mestre)
    atividade = criar_atividade(missao, mestre)
    criar_inscricao_na_trilha(guerreiro, trilha)
    criar_desbloqueio_da_missao(guerreiro, missao, aprovado=True)
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.get("/v1/eu/desafios", headers=_cabecalhos(chave, token))

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert len(corpo) == 1
    item = corpo[0]
    assert item["atividade"]["id"] == str(atividade.id)
    assert item["atividade"]["modalidade"] == atividade.modalidade.value
    assert item["atividade"]["formato"] == atividade.formato.value
    assert item["missao_id"] == str(missao.id)
    assert item["trilha_id"] == str(trilha.id)


def test_atividade_de_missao_ainda_bloqueada_nao_aparece(
    cliente,
    criar_chave,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_inscricao_na_trilha,
    criar_sessao_de_teste,
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    missao = criar_missao(trilha, mestre)
    criar_atividade(missao, mestre)
    criar_inscricao_na_trilha(guerreiro, trilha)
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.get("/v1/eu/desafios", headers=_cabecalhos(chave, token))

    assert resposta.status_code == 200
    assert resposta.json() == []


def test_atividade_ja_lancada_pelo_mestre_sai_da_lista(
    sessao,
    cliente,
    criar_chave,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_inscricao_na_trilha,
    criar_desbloqueio_da_missao,
    criar_sessao_de_teste,
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    missao = criar_missao(trilha, mestre)
    atividade = criar_atividade(missao, mestre)
    criar_inscricao_na_trilha(guerreiro, trilha)
    criar_desbloqueio_da_missao(guerreiro, missao, aprovado=True)
    aula = criar_aula_para_resultado(sessao, mestre)
    registrar_resultado(
        sessao,
        operador=mestre,
        aula=aula,
        guerreiro_id=guerreiro.id,
        atividade=atividade,
        momento_do_fato=MOMENTO_DO_FATO,
        producao="Fez a atividade.",
        desfecho=DesfechoDoResultado.realizada,
    )
    sessao.commit()
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.get("/v1/eu/desafios", headers=_cabecalhos(chave, token))

    assert resposta.status_code == 200
    assert resposta.json() == []


def test_atividade_de_trilha_nao_inscrita_nao_aparece(
    cliente,
    criar_chave,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_desbloqueio_da_missao,
    criar_sessao_de_teste,
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    missao = criar_missao(trilha, mestre)
    criar_atividade(missao, mestre)
    criar_desbloqueio_da_missao(guerreiro, missao, aprovado=True)
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.get("/v1/eu/desafios", headers=_cabecalhos(chave, token))

    assert resposta.status_code == 200
    assert resposta.json() == []


def test_sem_nada_em_aberto_a_resposta_e_conjunto_vazio(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    guerreiro = criar_persona(Papel.guerreiro)
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.get("/v1/eu/desafios", headers=_cabecalhos(chave, token))

    assert resposta.status_code == 200
    assert resposta.json() == []


def test_persona_que_nao_e_guerreiro_nao_le(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()

    for operador in (
        criar_persona(Papel.mestre),
        criar_persona(Papel.admin),
        criar_persona(Papel.apoiador),
        criar_persona(Papel.responsavel),
    ):
        token, _ = criar_sessao_de_teste(operador)
        resposta = cliente.get("/v1/eu/desafios", headers=_cabecalhos(chave, token))
        assert resposta.status_code == 403
