from datetime import UTC, datetime

import pytest

from nucleo.ciclo.regra import encerrar_ciclo
from nucleo.erros import PermissaoNegada
from nucleo.ocorrencias_de_conduta.modelo import OcorrenciaDeConduta
from nucleo.ocorrencias_de_conduta.regra import (
    VALOR_DA_OCORRENCIA_DE_CONDUTA,
    lancar_ocorrencia_de_conduta,
)
from nucleo.personas.modelo import Papel
from nucleo.pontuacao.modelo import PontoRegular

MOMENTO_DO_FATO = datetime(2026, 8, 1, 10, 0, tzinfo=UTC)


def _lancar(sessao, *, operador, aula, atividade, guerreiro, motivo="Desrespeitou um colega."):
    return lancar_ocorrencia_de_conduta(
        sessao,
        operador=operador,
        aula=aula,
        atividade=atividade,
        guerreiro_id=guerreiro.id,
        motivo=motivo,
        momento_do_fato=MOMENTO_DO_FATO,
    )


def test_encerramento_expurga_motivo_preservando_valor_data_e_autor(
    sessao, criar_persona, criar_comunidade, criar_aula, criar_trilha, criar_missao, criar_atividade
):
    from nucleo.pontuacao.regra import creditar_ponto_regular

    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    atividade = criar_atividade(missao, mestre)
    aula = criar_aula(mestre, comunidade)

    creditar_ponto_regular(sessao, guerreiro_id=guerreiro.id, trilha_id=trilha.id, valor=20)
    sessao.commit()
    ocorrencia = _lancar(
        sessao, operador=mestre, aula=aula, atividade=atividade, guerreiro=guerreiro
    )
    sessao.commit()

    quantidade = encerrar_ciclo(sessao)

    assert quantidade == 1
    expurgada = sessao.get(OcorrenciaDeConduta, ocorrencia.id)
    sessao.refresh(expurgada)
    assert expurgada.motivo is None
    assert expurgada.encerrada_em is not None
    assert expurgada.valor == VALOR_DA_OCORRENCIA_DE_CONDUTA
    assert expurgada.valor_debitado == VALOR_DA_OCORRENCIA_DE_CONDUTA
    assert expurgada.autor_id == mestre.id
    assert expurgada.momento_do_fato == MOMENTO_DO_FATO


def test_encerramento_nao_desfaz_o_debito(
    sessao, criar_persona, criar_comunidade, criar_aula, criar_trilha, criar_missao, criar_atividade
):
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    atividade = criar_atividade(missao, mestre)
    aula = criar_aula(mestre, comunidade)

    from nucleo.pontuacao.regra import creditar_ponto_regular

    creditar_ponto_regular(sessao, guerreiro_id=guerreiro.id, trilha_id=trilha.id, valor=20)
    sessao.commit()
    _lancar(sessao, operador=mestre, aula=aula, atividade=atividade, guerreiro=guerreiro)
    sessao.commit()

    conta_antes = (
        sessao.query(PontoRegular).filter_by(guerreiro_id=guerreiro.id, trilha_id=trilha.id).one()
    )
    assert conta_antes.total == 15

    encerrar_ciclo(sessao)

    conta_depois = (
        sessao.query(PontoRegular).filter_by(guerreiro_id=guerreiro.id, trilha_id=trilha.id).one()
    )
    assert conta_depois.total == 15


def test_encerrar_duas_vezes_seguidas_nao_altera_nada_na_segunda(
    sessao, criar_persona, criar_comunidade, criar_aula, criar_trilha, criar_missao, criar_atividade
):
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    atividade = criar_atividade(missao, mestre)
    aula = criar_aula(mestre, comunidade)

    _lancar(sessao, operador=mestre, aula=aula, atividade=atividade, guerreiro=guerreiro)
    sessao.commit()

    primeira = encerrar_ciclo(sessao)
    segunda = encerrar_ciclo(sessao)

    assert primeira == 1
    assert segunda == 0


def test_encerramento_sem_ocorrencia_nova_nao_tem_o_que_fazer(sessao):
    assert encerrar_ciclo(sessao) == 0


def test_admin_encerra_o_ciclo_pela_rota(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_aula,
    criar_trilha,
    criar_missao,
    criar_atividade,
    sessao,
):
    mestre = criar_persona(Papel.mestre)
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    atividade = criar_atividade(missao, mestre)
    aula = criar_aula(mestre, comunidade)
    _lancar(sessao, operador=mestre, aula=aula, atividade=atividade, guerreiro=guerreiro)
    sessao.commit()

    chave, _ = criar_chave()
    token, _ = criar_sessao_de_teste(admin)
    resposta = cliente.post(
        "/v1/ciclo/encerramento",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 201
    assert resposta.json()["ocorrencias_expurgadas"] == 1


@pytest.mark.parametrize(
    "papel", [Papel.mestre, Papel.apoiador, Papel.responsavel, Papel.guerreiro]
)
def test_quem_nao_e_admin_nao_encerra_o_ciclo(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, papel
):
    persona = criar_persona(papel)
    chave, _ = criar_chave()
    token, _ = criar_sessao_de_teste(persona)

    resposta = cliente.post(
        "/v1/ciclo/encerramento",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == PermissaoNegada.status_code
