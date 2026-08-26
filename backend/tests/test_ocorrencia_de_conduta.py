from datetime import UTC, datetime

import pytest
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError

from nucleo.erros import ErroDeValidacao, OcorrenciaDeCondutaImutavel, PermissaoNegada
from nucleo.ocorrencias_de_conduta.modelo import OcorrenciaDeConduta
from nucleo.ocorrencias_de_conduta.regra import (
    TETO_POR_GUERREIRO_E_AULA,
    VALOR_DA_OCORRENCIA_DE_CONDUTA,
    lancar_ocorrencia_de_conduta,
)
from nucleo.personas.modelo import Papel
from nucleo.pontuacao.modelo import Badge, Nivel, PontoRegular, TipoDeBadge
from nucleo.trilhas.modelo import FormatoDeAtividade

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


def test_ocorrencia_debita_exatamente_5_pontos_sem_valor_informado(
    sessao, criar_persona, criar_comunidade, criar_aula, criar_trilha, criar_missao, criar_atividade
):
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    atividade = criar_atividade(missao, mestre)
    aula = criar_aula(mestre, comunidade)

    ocorrencia = _lancar(
        sessao, operador=mestre, aula=aula, atividade=atividade, guerreiro=guerreiro
    )
    sessao.commit()

    assert ocorrencia.valor == VALOR_DA_OCORRENCIA_DE_CONDUTA == 5
    conta = (
        sessao.query(PontoRegular).filter_by(guerreiro_id=guerreiro.id, trilha_id=trilha.id).one()
    )
    assert conta.total == 0  # já nasce em zero: o crédito zero-base debitado vira zero (piso)


def test_terceira_ocorrencia_na_mesma_aula_e_recusada(
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
    _lancar(sessao, operador=mestre, aula=aula, atividade=atividade, guerreiro=guerreiro)
    sessao.commit()

    with pytest.raises(ErroDeValidacao) as excinfo:
        _lancar(sessao, operador=mestre, aula=aula, atividade=atividade, guerreiro=guerreiro)
    assert excinfo.value.campo == "guerreiro_id"
    assert sessao.query(OcorrenciaDeConduta).count() == 2


def test_teto_de_um_guerreiro_nao_alcanca_o_outro(
    sessao, criar_persona, criar_comunidade, criar_aula, criar_trilha, criar_missao, criar_atividade
):
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    guerreiro_um = criar_persona(Papel.guerreiro, comunidade=comunidade)
    guerreiro_dois = criar_persona(Papel.guerreiro, comunidade=comunidade)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    atividade = criar_atividade(missao, mestre)
    aula = criar_aula(mestre, comunidade)

    _lancar(sessao, operador=mestre, aula=aula, atividade=atividade, guerreiro=guerreiro_um)
    sessao.commit()
    _lancar(sessao, operador=mestre, aula=aula, atividade=atividade, guerreiro=guerreiro_um)
    sessao.commit()

    ocorrencia = _lancar(
        sessao, operador=mestre, aula=aula, atividade=atividade, guerreiro=guerreiro_dois
    )
    sessao.commit()

    assert ocorrencia.guerreiro_id == guerreiro_dois.id
    assert sessao.query(OcorrenciaDeConduta).filter_by(guerreiro_id=guerreiro_dois.id).count() == 1


def test_debito_vai_a_trilha_da_atividade_e_nenhuma_outra(
    sessao, criar_persona, criar_comunidade, criar_aula, criar_trilha, criar_missao, criar_atividade
):
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    trilha_um = criar_trilha(mestre, nome="Trilha 1")
    trilha_dois = criar_trilha(mestre, nome="Trilha 2")
    missao_um = criar_missao(trilha_um, mestre)
    atividade_um = criar_atividade(missao_um, mestre)
    aula = criar_aula(mestre, comunidade)

    # Crédito inicial na trilha 1, para o débito ter o que consumir.
    from nucleo.pontuacao.regra import creditar_ponto_regular

    creditar_ponto_regular(sessao, guerreiro_id=guerreiro.id, trilha_id=trilha_um.id, valor=20)
    sessao.commit()

    _lancar(sessao, operador=mestre, aula=aula, atividade=atividade_um, guerreiro=guerreiro)
    sessao.commit()

    conta_um = (
        sessao.query(PontoRegular)
        .filter_by(guerreiro_id=guerreiro.id, trilha_id=trilha_um.id)
        .one()
    )
    conta_dois = (
        sessao.query(PontoRegular)
        .filter_by(guerreiro_id=guerreiro.id, trilha_id=trilha_dois.id)
        .first()
    )
    assert conta_um.total == 15
    assert conta_dois is None


def test_mestre_que_nao_e_autor_e_recusado(
    sessao, criar_persona, criar_comunidade, criar_aula, criar_trilha, criar_missao, criar_atividade
):
    mestre_autor = criar_persona(Papel.mestre)
    outro_mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    trilha = criar_trilha(mestre_autor)
    missao = criar_missao(trilha, mestre_autor)
    atividade = criar_atividade(missao, mestre_autor)
    aula = criar_aula(mestre_autor, comunidade)

    with pytest.raises(PermissaoNegada):
        _lancar(sessao, operador=outro_mestre, aula=aula, atividade=atividade, guerreiro=guerreiro)
    assert sessao.query(OcorrenciaDeConduta).count() == 0


def test_admin_lanca_mesmo_sem_ser_o_autor(
    sessao, criar_persona, criar_comunidade, criar_aula, criar_trilha, criar_missao, criar_atividade
):
    mestre_autor = criar_persona(Papel.mestre)
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    trilha = criar_trilha(mestre_autor)
    missao = criar_missao(trilha, mestre_autor)
    atividade = criar_atividade(missao, mestre_autor)
    aula = criar_aula(admin, comunidade)

    ocorrencia = _lancar(
        sessao, operador=admin, aula=aula, atividade=atividade, guerreiro=guerreiro
    )
    sessao.commit()

    assert ocorrencia.autor_id == admin.id


def test_ocorrencia_sem_motivo_e_recusada(
    sessao, criar_persona, criar_comunidade, criar_aula, criar_trilha, criar_missao, criar_atividade
):
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    atividade = criar_atividade(missao, mestre)
    aula = criar_aula(mestre, comunidade)

    with pytest.raises(ErroDeValidacao) as excinfo:
        _lancar(
            sessao, operador=mestre, aula=aula, atividade=atividade, guerreiro=guerreiro, motivo=""
        )
    assert excinfo.value.campo == "motivo"
    assert sessao.query(OcorrenciaDeConduta).count() == 0


def test_atividade_on_line_nao_pertence_a_aula_e_e_recusada(
    sessao, criar_persona, criar_comunidade, criar_aula, criar_trilha, criar_missao, criar_atividade
):
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    atividade = criar_atividade(missao, mestre, formato=FormatoDeAtividade.on_line_assincrona)
    aula = criar_aula(mestre, comunidade)

    with pytest.raises(ErroDeValidacao) as excinfo:
        _lancar(sessao, operador=mestre, aula=aula, atividade=atividade, guerreiro=guerreiro)
    assert excinfo.value.campo == "atividade_id"
    assert sessao.query(OcorrenciaDeConduta).count() == 0


def test_debito_maior_que_o_saldo_para_em_zero(
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

    creditar_ponto_regular(sessao, guerreiro_id=guerreiro.id, trilha_id=trilha.id, valor=3)
    sessao.commit()

    _lancar(sessao, operador=mestre, aula=aula, atividade=atividade, guerreiro=guerreiro)
    sessao.commit()

    conta = (
        sessao.query(PontoRegular).filter_by(guerreiro_id=guerreiro.id, trilha_id=trilha.id).one()
    )
    assert conta.total == 0


def test_nivel_e_badge_permanecem_apos_o_debito(
    sessao, criar_persona, criar_comunidade, criar_aula, criar_trilha, criar_missao, criar_atividade
):
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    atividade = criar_atividade(missao, mestre)
    aula = criar_aula(mestre, comunidade)

    sessao.add(Nivel(guerreiro_id=guerreiro.id, trilha_id=trilha.id, valor=1))
    sessao.add(Badge(guerreiro_id=guerreiro.id, trilha_id=trilha.id, tipo=TipoDeBadge.de_nivel))
    sessao.commit()

    _lancar(sessao, operador=mestre, aula=aula, atividade=atividade, guerreiro=guerreiro)
    sessao.commit()

    assert (
        sessao.query(Nivel).filter_by(guerreiro_id=guerreiro.id, trilha_id=trilha.id).count() == 1
    )
    assert (
        sessao.query(Badge).filter_by(guerreiro_id=guerreiro.id, trilha_id=trilha.id).count() == 1
    )


def test_ocorrencia_nao_alcanca_o_ponto_extra(
    sessao, criar_persona, criar_comunidade, criar_aula, criar_trilha, criar_missao, criar_atividade
):
    from nucleo.ponto_extra.modelo import PontoExtra

    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    atividade = criar_atividade(missao, mestre)
    aula = criar_aula(mestre, comunidade)

    conta_extra = PontoExtra(guerreiro_id=guerreiro.id, acumulado=30, saldo_disponivel=30)
    sessao.add(conta_extra)
    sessao.commit()

    _lancar(sessao, operador=mestre, aula=aula, atividade=atividade, guerreiro=guerreiro)
    sessao.commit()

    sessao.refresh(conta_extra)
    assert conta_extra.acumulado == 30
    assert conta_extra.saldo_disponivel == 30


def test_ocorrencia_gravada_nao_se_altera(
    sessao, criar_persona, criar_comunidade, criar_aula, criar_trilha, criar_missao, criar_atividade
):
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    atividade = criar_atividade(missao, mestre)
    aula = criar_aula(mestre, comunidade)

    ocorrencia = _lancar(
        sessao, operador=mestre, aula=aula, atividade=atividade, guerreiro=guerreiro
    )
    sessao.commit()

    ocorrencia.motivo = "Outro motivo."
    with pytest.raises(OcorrenciaDeCondutaImutavel):
        sessao.commit()
    sessao.rollback()

    intacta = sessao.get(OcorrenciaDeConduta, ocorrencia.id)
    assert intacta.motivo == "Desrespeitou um colega."

    sessao.delete(intacta)
    with pytest.raises(OcorrenciaDeCondutaImutavel):
        sessao.commit()
    sessao.rollback()

    assert sessao.get(OcorrenciaDeConduta, ocorrencia.id) is not None


def test_ocorrencia_sem_motivo_guardado_nao_o_devolve(
    sessao, criar_persona, criar_comunidade, criar_aula, criar_trilha, criar_missao, criar_atividade
):
    """O expurgo em si — quem apaga o motivo e quando — é pendência de
    decisão que a fatia devolve ao documento 09; nenhuma rota de expurgo
    existe aqui, e a tabela permanece somente inserção (`ocorrencia gravada
    não se altera`, acima). O que esta fatia prepara é a coluna anulável e a
    leitura que já lida com o motivo ausente sem devolvê-lo — por isso o
    cenário grava a ocorrência **já** sem motivo, no lugar de tentar um
    `UPDATE` que o gatilho de imutabilidade recusaria (`RN-01-52`)."""
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    atividade = criar_atividade(missao, mestre)
    aula = criar_aula(mestre, comunidade)

    ocorrencia = OcorrenciaDeConduta(
        guerreiro_id=guerreiro.id,
        aula_id=aula.id,
        atividade_id=atividade.id,
        valor=VALOR_DA_OCORRENCIA_DE_CONDUTA,
        valor_debitado=VALOR_DA_OCORRENCIA_DE_CONDUTA,
        motivo=None,
        momento_do_fato=MOMENTO_DO_FATO,
        autor_id=mestre.id,
        papel_do_autor=mestre.papel.value,
    )
    sessao.add(ocorrencia)
    sessao.commit()

    lida = sessao.get(OcorrenciaDeConduta, ocorrencia.id)
    assert lida.motivo is None
    assert lida.valor == VALOR_DA_OCORRENCIA_DE_CONDUTA
    assert lida.autor_id == mestre.id
    assert lida.momento_do_fato == MOMENTO_DO_FATO


def test_requisicao_com_valor_e_recusada_pela_rota(
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
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    token, _ = criar_sessao_de_teste(mestre)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    atividade = criar_atividade(missao, mestre)
    aula = criar_aula(mestre, comunidade)

    resposta = cliente.post(
        "/v1/ocorrencias-de-conduta",
        json={
            "guerreiro_id": str(guerreiro.id),
            "aula_id": str(aula.id),
            "atividade_id": str(atividade.id),
            "motivo": "Desrespeitou um colega.",
            "momento_do_fato": MOMENTO_DO_FATO.isoformat(),
            "valor": 999,
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 422
    assert sessao.query(OcorrenciaDeConduta).count() == 0


def test_lancamento_pela_rota_debita_e_confirma_teto(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_aula,
    criar_trilha,
    criar_missao,
    criar_atividade,
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    token, _ = criar_sessao_de_teste(mestre)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    atividade = criar_atividade(missao, mestre)
    aula = criar_aula(mestre, comunidade)

    resposta = cliente.post(
        "/v1/ocorrencias-de-conduta",
        json={
            "guerreiro_id": str(guerreiro.id),
            "aula_id": str(aula.id),
            "atividade_id": str(atividade.id),
            "motivo": "Desrespeitou um colega.",
            "momento_do_fato": MOMENTO_DO_FATO.isoformat(),
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["valor"] == VALOR_DA_OCORRENCIA_DE_CONDUTA
    assert corpo["motivo"] == "Desrespeitou um colega."


def test_teto_por_guerreiro_e_dez(sessao):
    assert TETO_POR_GUERREIRO_E_AULA == 10


def test_valor_debitado_e_menor_que_o_nominal_quando_o_saldo_e_pequeno(
    sessao, criar_persona, criar_comunidade, criar_aula, criar_trilha, criar_missao, criar_atividade
):
    """`valor` continua o nominal do documento 11 §5; `valor_debitado` é o
    que o débito tirou de fato depois do aparo em zero — os dois divergem
    quando o saldo da trilha era menor que 5 (design — decisão 3,
    `RF-02-100`)."""
    from nucleo.pontuacao.regra import creditar_ponto_regular

    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    atividade = criar_atividade(missao, mestre)
    aula = criar_aula(mestre, comunidade)

    creditar_ponto_regular(sessao, guerreiro_id=guerreiro.id, trilha_id=trilha.id, valor=3)
    sessao.commit()

    ocorrencia = _lancar(
        sessao, operador=mestre, aula=aula, atividade=atividade, guerreiro=guerreiro
    )
    sessao.commit()

    assert ocorrencia.valor == VALOR_DA_OCORRENCIA_DE_CONDUTA == 5
    assert ocorrencia.valor_debitado == 3


def test_valor_debitado_igual_ao_nominal_quando_ha_saldo_suficiente(
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

    assert ocorrencia.valor_debitado == VALOR_DA_OCORRENCIA_DE_CONDUTA == 5


def test_expurgo_do_fim_de_ciclo_e_a_unica_alteracao_admitida_pelo_gatilho(
    conexao,
    sessao,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_trilha,
    criar_missao,
    criar_atividade,
):
    """O _trigger_ estreitado admite exatamente o `UPDATE` que anula
    `motivo` e carimba `encerrada_em`, sem tocar mais nada — a mesma forma
    que `nucleo.ciclo.regra.encerrar_ciclo` emite (design — decisão 2,
    `RF-02-100`)."""
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

    conexao.execute(
        text("UPDATE ocorrencia_de_conduta SET motivo = NULL, encerrada_em = now() WHERE id = :id"),
        {"id": str(ocorrencia.id)},
    )

    expurgada = sessao.get(OcorrenciaDeConduta, ocorrencia.id)
    sessao.refresh(expurgada)
    assert expurgada.motivo is None
    assert expurgada.encerrada_em is not None
    assert expurgada.valor == VALOR_DA_OCORRENCIA_DE_CONDUTA
    assert expurgada.valor_debitado == VALOR_DA_OCORRENCIA_DE_CONDUTA
    assert expurgada.guerreiro_id == guerreiro.id


def test_update_de_outra_coluna_e_recusado_mesmo_anulando_o_motivo_junto(
    conexao,
    sessao,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_trilha,
    criar_missao,
    criar_atividade,
):
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    atividade = criar_atividade(missao, mestre)
    aula = criar_aula(mestre, comunidade)

    ocorrencia = _lancar(
        sessao, operador=mestre, aula=aula, atividade=atividade, guerreiro=guerreiro
    )
    sessao.commit()

    with pytest.raises(DBAPIError), conexao.begin_nested():
        conexao.execute(
            text(
                "UPDATE ocorrencia_de_conduta "
                "SET motivo = NULL, encerrada_em = now(), valor = 999 WHERE id = :id"
            ),
            {"id": str(ocorrencia.id)},
        )

    with pytest.raises(DBAPIError), conexao.begin_nested():
        conexao.execute(
            text("UPDATE ocorrencia_de_conduta SET valor = 999 WHERE id = :id"),
            {"id": str(ocorrencia.id)},
        )

    with pytest.raises(DBAPIError), conexao.begin_nested():
        conexao.execute(
            text("DELETE FROM ocorrencia_de_conduta WHERE id = :id"), {"id": str(ocorrencia.id)}
        )

    intacta = sessao.get(OcorrenciaDeConduta, ocorrencia.id)
    assert intacta.motivo == "Desrespeitou um colega."
    assert intacta.valor == VALOR_DA_OCORRENCIA_DE_CONDUTA
    assert intacta.encerrada_em is None
