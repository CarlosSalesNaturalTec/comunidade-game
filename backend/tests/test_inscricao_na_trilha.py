import pytest

from nucleo.erros import ErroDeValidacao
from nucleo.personas.modelo import Papel
from nucleo.trilhas.modelo import SituacaoDaTrilha
from nucleo.trilhas.regra import consultar_inscricoes_do_guerreiro, inscrever_na_trilha


def test_inscricao_em_trilha_publicada_e_gravada(sessao, criar_persona, criar_trilha):
    guerreiro = criar_persona(Papel.guerreiro)
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)

    inscricao = inscrever_na_trilha(sessao, guerreiro=guerreiro, trilha=trilha)
    sessao.commit()

    assert inscricao.guerreiro_id == guerreiro.id
    assert inscricao.trilha_id == trilha.id
    assert inscricao.momento is not None


def test_inscricao_em_trilha_em_rascunho_e_recusada(sessao, criar_persona, criar_trilha):
    guerreiro = criar_persona(Papel.guerreiro)
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.rascunho)

    with pytest.raises(ErroDeValidacao):
        inscrever_na_trilha(sessao, guerreiro=guerreiro, trilha=trilha)


def test_inscricao_em_trilha_despublicada_e_recusada(sessao, criar_persona, criar_trilha):
    guerreiro = criar_persona(Papel.guerreiro)
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.despublicada)

    with pytest.raises(ErroDeValidacao):
        inscrever_na_trilha(sessao, guerreiro=guerreiro, trilha=trilha)


def test_segunda_inscricao_na_mesma_trilha_nao_cria_vinculo_novo(
    sessao, criar_persona, criar_trilha
):
    guerreiro = criar_persona(Papel.guerreiro)
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)

    primeira = inscrever_na_trilha(sessao, guerreiro=guerreiro, trilha=trilha)
    sessao.commit()
    segunda = inscrever_na_trilha(sessao, guerreiro=guerreiro, trilha=trilha)
    sessao.commit()

    assert primeira.id == segunda.id
    assert consultar_inscricoes_do_guerreiro(sessao, guerreiro_id=guerreiro.id) == [primeira]


def test_varias_trilhas_ao_mesmo_tempo(sessao, criar_persona, criar_trilha):
    guerreiro = criar_persona(Papel.guerreiro)
    mestre = criar_persona(Papel.mestre)
    trilha_1 = criar_trilha(mestre, nome="Trilha 1", situacao=SituacaoDaTrilha.publicada)
    trilha_2 = criar_trilha(mestre, nome="Trilha 2", situacao=SituacaoDaTrilha.publicada)

    inscrever_na_trilha(sessao, guerreiro=guerreiro, trilha=trilha_1)
    inscrever_na_trilha(sessao, guerreiro=guerreiro, trilha=trilha_2)
    sessao.commit()

    inscricoes = consultar_inscricoes_do_guerreiro(sessao, guerreiro_id=guerreiro.id)
    assert {inscricao.trilha_id for inscricao in inscricoes} == {trilha_1.id, trilha_2.id}


def test_nao_ha_desinscricao(sessao, criar_persona, criar_trilha):
    """`RN-05-44`: a inscrição é fato com data, sem situação nem função de
    remoção — o núcleo não expõe nenhuma forma de desfazê-la."""
    import nucleo.trilhas.regra as trilhas_regra

    guerreiro = criar_persona(Papel.guerreiro)
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)

    inscrever_na_trilha(sessao, guerreiro=guerreiro, trilha=trilha)
    sessao.commit()

    assert not hasattr(trilhas_regra, "desinscrever_da_trilha")
    assert len(consultar_inscricoes_do_guerreiro(sessao, guerreiro_id=guerreiro.id)) == 1


def test_sem_inscricao_a_lista_sai_vazia(sessao, criar_persona):
    guerreiro = criar_persona(Papel.guerreiro)
    assert consultar_inscricoes_do_guerreiro(sessao, guerreiro_id=guerreiro.id) == []


def test_terceiro_nao_inscreve_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha
):
    """`RN-05-21`: só o Guerreiro(a) em sessão executa a própria
    inscrição — outro papel na rota `/eu/*` é recusado."""
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.post(
        f"/v1/eu/trilhas/{trilha.id}/inscricao",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 403


def test_guerreiro_inscreve_se_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_trilha
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.post(
        f"/v1/eu/trilhas/{trilha.id}/inscricao",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 201
    assert resposta.json()["trilha_id"] == str(trilha.id)
