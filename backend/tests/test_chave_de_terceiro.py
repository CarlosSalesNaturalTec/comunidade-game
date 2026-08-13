from datetime import timedelta

import pytest

from nucleo.chaves.modelo import ChaveDeAplicacao, NaturezaDaChave, SituacaoDaChave
from nucleo.chaves.regra import (
    aplicar_decurso_se_vencido,
    apresentar_url,
    emitir_chave_de_terceiro,
    revogar,
)
from nucleo.erros import (
    ErroDeValidacao,
    NaoEncontrado,
    PrazoDeApresentacaoVencido,
    SolicitacaoDeChaveNaoDisponivelParaEmissao,
    UrlJaApresentada,
)
from nucleo.fila.modelo import SituacaoDaSolicitacao
from nucleo.personas.modelo import Papel
from nucleo.tempo import agora

# --- Emissão (RF-01-50) ---------------------------------------------------


def test_solicitacao_aprovada_rende_chave_presa_a_ela(
    sessao, configuracao, criar_solicitacao_de_chave
):
    solicitacao = criar_solicitacao_de_chave()

    chave, segredo = emitir_chave_de_terceiro(
        sessao, solicitacao, emitida_por="admin-de-teste", configuracao=configuracao
    )
    sessao.commit()

    assert chave.natureza == NaturezaDaChave.de_terceiro
    assert chave.solicitacao_de_chave_id == solicitacao.id
    assert solicitacao.chave_id == chave.id
    assert segredo


def test_segunda_leitura_da_chave_de_terceiro_nao_recupera_o_segredo(
    sessao, configuracao, criar_solicitacao_de_chave
):
    solicitacao = criar_solicitacao_de_chave()
    chave, _ = emitir_chave_de_terceiro(
        sessao, solicitacao, emitida_por="admin", configuracao=configuracao
    )
    sessao.commit()

    lida_de_novo = sessao.get(ChaveDeAplicacao, chave.id)
    campos = {campo.name for campo in ChaveDeAplicacao.__table__.columns}
    assert "segredo" not in campos
    assert lida_de_novo.resumo_do_segredo == chave.resumo_do_segredo


@pytest.mark.parametrize(
    "situacao",
    [
        SituacaoDaSolicitacao.recebida,
        SituacaoDaSolicitacao.em_avaliacao,
        SituacaoDaSolicitacao.recusada,
    ],
)
def test_emissao_recusa_solicitacao_nao_aprovada(
    sessao, configuracao, criar_solicitacao_de_chave, situacao
):
    solicitacao = criar_solicitacao_de_chave(situacao=situacao)

    with pytest.raises(SolicitacaoDeChaveNaoDisponivelParaEmissao):
        emitir_chave_de_terceiro(
            sessao, solicitacao, emitida_por="admin", configuracao=configuracao
        )

    assert (
        sessao.query(ChaveDeAplicacao).filter_by(natureza=NaturezaDaChave.de_terceiro).count() == 0
    )


def test_emissao_recusa_solicitacao_que_ja_rendeu_chave(
    sessao, configuracao, criar_solicitacao_de_chave
):
    solicitacao = criar_solicitacao_de_chave()
    emitir_chave_de_terceiro(sessao, solicitacao, emitida_por="admin", configuracao=configuracao)
    sessao.commit()

    with pytest.raises(SolicitacaoDeChaveNaoDisponivelParaEmissao):
        emitir_chave_de_terceiro(
            sessao, solicitacao, emitida_por="admin", configuracao=configuracao
        )

    assert (
        sessao.query(ChaveDeAplicacao).filter_by(natureza=NaturezaDaChave.de_terceiro).count() == 1
    )


def test_duas_solicitacoes_com_mesmo_nome_rendem_duas_chaves(
    sessao, configuracao, criar_solicitacao_de_chave
):
    primeira = criar_solicitacao_de_chave(solicitante="Desenvolvedora de Tal")
    segunda = criar_solicitacao_de_chave(solicitante="Desenvolvedora de Tal")

    chave_1, _ = emitir_chave_de_terceiro(
        sessao, primeira, emitida_por="admin", configuracao=configuracao
    )
    chave_2, _ = emitir_chave_de_terceiro(
        sessao, segunda, emitida_por="admin", configuracao=configuracao
    )
    sessao.commit()

    assert chave_1.id != chave_2.id
    assert chave_1.aplicacao == chave_2.aplicacao == "Desenvolvedora de Tal"


def test_emissao_produz_sempre_chave_de_producao(sessao, configuracao, criar_solicitacao_de_chave):
    assert configuracao.ambiente == "desenvolvimento"
    solicitacao = criar_solicitacao_de_chave()

    chave, _ = emitir_chave_de_terceiro(
        sessao, solicitacao, emitida_por="admin", configuracao=configuracao
    )
    sessao.commit()

    assert chave.ambiente == "producao"


def test_mudar_configuracao_nao_altera_prazo_ja_emitido(
    sessao, configuracao, criar_solicitacao_de_chave
):
    solicitacao = criar_solicitacao_de_chave()
    chave, _ = emitir_chave_de_terceiro(
        sessao, solicitacao, emitida_por="admin", configuracao=configuracao
    )
    sessao.commit()
    prazo_original = chave.prazo_de_apresentacao

    nova_configuracao = configuracao.model_copy(update={"prazo_de_apresentacao_dias": 90})
    outra_solicitacao = criar_solicitacao_de_chave(solicitante="Outra Desenvolvedora")
    emitir_chave_de_terceiro(
        sessao, outra_solicitacao, emitida_por="admin", configuracao=nova_configuracao
    )
    sessao.commit()

    assert chave.prazo_de_apresentacao == prazo_original


# --- Apresentação da URL (RF-01-51) ---------------------------------------


def test_url_apresentada_dentro_do_prazo_mantem_a_chave_vigente(sessao, criar_chave):
    _, chave = criar_chave(
        natureza=NaturezaDaChave.de_terceiro, prazo_de_apresentacao=agora() + timedelta(days=30)
    )

    apresentar_url(sessao, chave.id, "https://exemplo.org/painel")
    sessao.commit()

    assert chave.situacao == SituacaoDaChave.vigente
    assert chave.url_apresentada == "https://exemplo.org/painel"


def test_url_apresentada_segue_vigente_apos_passar_o_prazo_original(sessao, criar_chave):
    _, chave = criar_chave(
        natureza=NaturezaDaChave.de_terceiro, prazo_de_apresentacao=agora() + timedelta(days=30)
    )
    apresentar_url(sessao, chave.id, "https://exemplo.org/painel")
    sessao.commit()

    chave.prazo_de_apresentacao = agora() - timedelta(days=1)
    sessao.commit()

    assert not aplicar_decurso_se_vencido(chave)
    assert chave.situacao == SituacaoDaChave.vigente


def test_apresentacao_depois_do_prazo_e_recusada_e_orienta_nova_chave(sessao, criar_chave):
    _, chave = criar_chave(
        natureza=NaturezaDaChave.de_terceiro, prazo_de_apresentacao=agora() - timedelta(seconds=1)
    )

    with pytest.raises(PrazoDeApresentacaoVencido) as excinfo:
        apresentar_url(sessao, chave.id, "https://exemplo.org/painel")

    assert "nova chave" in excinfo.value.mensagem
    assert chave.situacao == SituacaoDaChave.revogada
    assert chave.url_apresentada is None


def test_segunda_apresentacao_e_recusada_e_url_original_permanece(sessao, criar_chave):
    _, chave = criar_chave(
        natureza=NaturezaDaChave.de_terceiro, prazo_de_apresentacao=agora() + timedelta(days=30)
    )
    apresentar_url(sessao, chave.id, "https://exemplo.org/primeira")
    sessao.commit()

    with pytest.raises(UrlJaApresentada):
        apresentar_url(sessao, chave.id, "https://exemplo.org/segunda")

    assert chave.url_apresentada == "https://exemplo.org/primeira"


def test_apresentacao_com_id_desconhecido_e_recusada_sem_revelar_existencia(sessao):
    with pytest.raises(NaoEncontrado):
        apresentar_url(sessao, "11111111-1111-4111-8111-111111111111", "https://exemplo.org")


def test_apresentacao_para_chave_do_projeto_e_recusada_igual_a_desconhecida(sessao, criar_chave):
    _, chave_do_projeto = criar_chave(natureza=NaturezaDaChave.do_projeto)

    with pytest.raises(NaoEncontrado):
        apresentar_url(sessao, chave_do_projeto.id, "https://exemplo.org")


# --- Revogação por decurso (RF-01-52) -------------------------------------


def test_decurso_transicao_e_idempotente_entre_conferencia_e_leitura_de_gestao(sessao, criar_chave):
    _, chave = criar_chave(
        natureza=NaturezaDaChave.de_terceiro, prazo_de_apresentacao=agora() - timedelta(seconds=1)
    )

    primeira_chamada = aplicar_decurso_se_vencido(chave)
    segunda_chamada = aplicar_decurso_se_vencido(chave)

    assert primeira_chamada is True
    assert segunda_chamada is False
    assert chave.situacao == SituacaoDaChave.revogada


def test_revogacao_por_decurso_grava_motivo_sem_autoria_de_pessoa(sessao, criar_chave):
    _, chave = criar_chave(
        natureza=NaturezaDaChave.de_terceiro, prazo_de_apresentacao=agora() - timedelta(seconds=1)
    )

    aplicar_decurso_se_vencido(chave)

    assert chave.motivo_da_revogacao
    assert chave.revogada_por is None
    assert chave.revogada_em is not None


def test_revogada_por_decurso_nova_solicitacao_e_sempre_possivel(
    sessao, configuracao, criar_chave, criar_solicitacao_de_chave
):
    _, chave_vencida = criar_chave(
        natureza=NaturezaDaChave.de_terceiro, prazo_de_apresentacao=agora() - timedelta(seconds=1)
    )
    aplicar_decurso_se_vencido(chave_vencida)
    sessao.commit()

    nova_solicitacao = criar_solicitacao_de_chave()
    nova_chave, _ = emitir_chave_de_terceiro(
        sessao, nova_solicitacao, emitida_por="admin", configuracao=configuracao
    )
    sessao.commit()

    assert nova_chave.id != chave_vencida.id
    assert nova_chave.situacao == SituacaoDaChave.vigente


# --- Revogação por Admin (RF-01-53) ---------------------------------------


def test_revogacao_por_admin_grava_motivo_autoria_e_data(sessao, criar_chave):
    _, chave = criar_chave(natureza=NaturezaDaChave.de_terceiro)

    revogar(sessao, chave, motivo="Uso indevido detectado.", revogada_por="admin-de-teste")

    assert chave.situacao == SituacaoDaChave.revogada
    assert chave.motivo_da_revogacao == "Uso indevido detectado."
    assert chave.revogada_por == "admin-de-teste"
    assert chave.revogada_em is not None


def test_revogacao_sem_motivo_e_recusada_e_chave_permanece_vigente(sessao, criar_chave):
    _, chave = criar_chave(natureza=NaturezaDaChave.de_terceiro)

    with pytest.raises(ErroDeValidacao):
        revogar(sessao, chave, motivo="   ", revogada_por="admin-de-teste")

    assert chave.situacao == SituacaoDaChave.vigente


def test_revogacao_nao_altera_nenhum_outro_registro(sessao, criar_persona, criar_chave):
    outra_persona = criar_persona(Papel.admin)
    _, chave_alvo = criar_chave(natureza=NaturezaDaChave.de_terceiro)
    _, outra_chave = criar_chave(aplicacao="app-08-apoiador")

    estado_da_outra_chave_antes = (
        outra_chave.situacao,
        outra_chave.url_apresentada,
        outra_chave.revogada_por,
    )

    revogar(
        sessao, chave_alvo, motivo="Encerramento do projeto.", revogada_por=str(outra_persona.id)
    )
    sessao.commit()

    assert (
        outra_chave.situacao,
        outra_chave.url_apresentada,
        outra_chave.revogada_por,
    ) == estado_da_outra_chave_antes
