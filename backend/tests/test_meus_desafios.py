"""A porta HTTP dos dois conjuntos em aberto do Guerreiro(a) em sessão —
semanais e extras (`RF-05-19`, `RF-05-20`, `RF-05-21`, `RN-05-21`,
`RN-05-06`, `RN-14-20`), do PRD-05 §9."""

from datetime import UTC, date, datetime

from nucleo.desafios_extras.modelo import Modalidade, SituacaoDoDesafioExtra
from nucleo.personas.modelo import Papel
from nucleo.resultados.modelo import DesfechoDoResultado
from nucleo.resultados.regra import registrar_resultado
from nucleo.trilhas.modelo import SituacaoDaTrilha
from tests.conftest import criar_aula_para_resultado

MOMENTO_DO_FATO = datetime(2026, 8, 1, 10, 0, tzinfo=UTC)
VIGENCIA_CORRENTE = {"vigencia_inicio": date(2026, 1, 1), "vigencia_fim": date(2026, 12, 31)}


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
    assert len(corpo["semanais"]) == 1
    assert corpo["extras"] == []
    item = corpo["semanais"][0]
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
    assert resposta.json() == {"semanais": [], "extras": []}


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
    assert resposta.json() == {"semanais": [], "extras": []}


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
    assert resposta.json() == {"semanais": [], "extras": []}


def test_sem_nada_em_aberto_a_resposta_e_conjunto_vazio(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    guerreiro = criar_persona(Papel.guerreiro)
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.get("/v1/eu/desafios", headers=_cabecalhos(chave, token))

    assert resposta.status_code == 200
    assert resposta.json() == {"semanais": [], "extras": []}


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


def test_os_dois_conjuntos_vem_apartados_na_mesma_resposta(
    cliente,
    criar_chave,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_inscricao_na_trilha,
    criar_desbloqueio_da_missao,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
    criar_desafio_extra,
    criar_sessao_de_teste,
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    apoiador = criar_persona(Papel.apoiador)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    missao = criar_missao(trilha, mestre)
    atividade = criar_atividade(missao, mestre)
    criar_inscricao_na_trilha(guerreiro, trilha)
    criar_desbloqueio_da_missao(guerreiro, missao, aprovado=True)
    tipo = criar_tipo_de_recurso(mestre)
    ponto = criar_ponto_de_apoio(mestre, criar_comunidade())
    desafio_extra = criar_desafio_extra(
        apoiador,
        trilha,
        tipo,
        ponto,
        situacao=SituacaoDoDesafioExtra.publicado,
        **VIGENCIA_CORRENTE,
    )
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.get("/v1/eu/desafios", headers=_cabecalhos(chave, token))

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert [item["atividade"]["id"] for item in corpo["semanais"]] == [str(atividade.id)]
    assert [item["id"] for item in corpo["extras"]] == [str(desafio_extra.id)]


def test_saida_do_extra_traz_o_que_o_rf_05_21_pede_e_nada_do_tramite_da_proposta(
    cliente,
    criar_chave,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_inscricao_na_trilha,
    criar_nick,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
    criar_desafio_extra,
    criar_sessao_de_teste,
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    apoiador = criar_persona(Papel.apoiador)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    missao = criar_missao(trilha, mestre)
    criar_inscricao_na_trilha(guerreiro, trilha)
    criar_nick(guerreiro, "guerreira-zeferina")
    tipo = criar_tipo_de_recurso(mestre)
    ponto = criar_ponto_de_apoio(mestre, criar_comunidade())
    desafio_extra = criar_desafio_extra(
        apoiador,
        trilha,
        tipo,
        ponto,
        missao=missao,
        situacao=SituacaoDoDesafioExtra.publicado,
        modalidade=Modalidade.direcionado,
        nick_do_destinatario="Guerreira-Zeferina",
        justificativa_do_vinculo="É minha vizinha.",
        parecer_do_mestre="Parecer do mestre.",
        **VIGENCIA_CORRENTE,
    )
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.get("/v1/eu/desafios", headers=_cabecalhos(chave, token))

    assert resposta.status_code == 200
    item = resposta.json()["extras"][0]

    assert item["id"] == str(desafio_extra.id)
    assert item["trilha_id"] == str(trilha.id)
    assert item["trilha_nome"] == trilha.nome
    assert item["missao_id"] == str(missao.id)
    assert item["missao_titulo"] == missao.titulo
    assert item["modalidade"] == Modalidade.direcionado.value
    assert item["formato"] == desafio_extra.formato.value
    assert item["criterio_de_atribuicao"] == desafio_extra.criterio_de_atribuicao
    assert item["pontos_extras"] == desafio_extra.pontos_extras
    assert item["recompensa"] == {
        "tipo_de_recurso_nome": tipo.nome,
        "ponto_de_apoio_nome": ponto.nome,
    }
    assert item["quantidade_disponivel"] == desafio_extra.quantidade_disponivel
    assert item["quantidade_restante"] == desafio_extra.quantidade_disponivel

    campos_nunca_expostos = {
        "nick_do_destinatario",
        "justificativa_do_vinculo",
        "parecer_do_mestre",
        "motivo_da_recusa",
        "custeio",
        "aporte_id",
        "lastro_provido",
        "lastro_faltante",
    }
    assert campos_nunca_expostos.isdisjoint(item.keys())
