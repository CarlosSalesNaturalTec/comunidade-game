from datetime import UTC, datetime

import pytest

from nucleo.aulas.modelo import SituacaoDaAula
from nucleo.erros import ErroDeValidacao, PermissaoNegada
from nucleo.personas.modelo import Papel
from nucleo.reservas.modelo import EstadoDaReserva
from nucleo.resultados.modelo import DesfechoDoResultado, Resultado
from nucleo.resultados.regra import ResultadoDeclarado, lancar_resultados_da_atividade

MOMENTO_DO_FATO = datetime(2026, 8, 1, 10, 0, tzinfo=UTC)


def _entrada(guerreiro, atividade=None, desfecho=DesfechoDoResultado.realizada):
    return ResultadoDeclarado(
        guerreiro_id=guerreiro.id,
        atividade=atividade,
        momento_do_fato=MOMENTO_DO_FATO,
        producao="Produção do Guerreiro(a).",
        desfecho=desfecho,
    )


def test_mestre_autor_lanca_varios_participantes_num_ato_so(
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

    resultados = [
        ResultadoDeclarado(
            guerreiro_id=guerreiro_um.id,
            atividade=atividade,
            momento_do_fato=MOMENTO_DO_FATO,
            producao="Produção 1.",
            desfecho=DesfechoDoResultado.realizada,
        ),
        ResultadoDeclarado(
            guerreiro_id=guerreiro_dois.id,
            atividade=atividade,
            momento_do_fato=MOMENTO_DO_FATO,
            producao="Produção 2.",
            desfecho=DesfechoDoResultado.realizada_com_merito,
        ),
    ]

    gravados = lancar_resultados_da_atividade(
        sessao, operador=mestre, aula=aula, atividade=atividade, resultados=resultados
    )
    sessao.commit()

    assert len(gravados) == 2
    assert {g.guerreiro_id for g in gravados} == {guerreiro_um.id, guerreiro_dois.id}
    assert sessao.query(Resultado).filter_by(atividade_id=atividade.id).count() == 2


def test_lancamento_por_atividade_nao_mexe_na_aula_nem_nas_reservas(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_lancamento,
    criar_aula,
    criar_reserva,
    criar_trilha,
    criar_missao,
    criar_atividade,
):
    from decimal import Decimal

    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(mestre, comunidade)
    tipo = criar_tipo_de_recurso(mestre)
    criar_lancamento(mestre, tipo, ponto_de_apoio, quantidade=Decimal("10.00"))
    aula = criar_aula(mestre, comunidade, ponto_de_apoio=ponto_de_apoio)
    reserva = criar_reserva(mestre, aula, tipo, ponto_de_apoio, quantidade=Decimal("3.00"))
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    atividade = criar_atividade(missao, mestre)

    lancar_resultados_da_atividade(
        sessao,
        operador=mestre,
        aula=aula,
        atividade=atividade,
        resultados=[
            ResultadoDeclarado(
                guerreiro_id=guerreiro.id,
                atividade=atividade,
                momento_do_fato=MOMENTO_DO_FATO,
                producao="Produção.",
                desfecho=DesfechoDoResultado.realizada,
            )
        ],
    )
    sessao.commit()

    sessao.refresh(aula)
    sessao.refresh(reserva)
    assert aula.situacao != SituacaoDaAula.realizada
    assert reserva.estado == EstadoDaReserva.reservada


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
        lancar_resultados_da_atividade(
            sessao,
            operador=outro_mestre,
            aula=aula,
            atividade=atividade,
            resultados=[_entrada(guerreiro, atividade=atividade)],
        )
    assert sessao.query(Resultado).count() == 0


def test_mestre_que_nao_e_autor_e_recusado_mesmo_com_lista_vazia(
    sessao, criar_persona, criar_comunidade, criar_aula, criar_trilha, criar_missao, criar_atividade
):
    mestre_autor = criar_persona(Papel.mestre)
    outro_mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    trilha = criar_trilha(mestre_autor)
    missao = criar_missao(trilha, mestre_autor)
    atividade = criar_atividade(missao, mestre_autor)
    aula = criar_aula(mestre_autor, comunidade)

    with pytest.raises(PermissaoNegada):
        lancar_resultados_da_atividade(
            sessao, operador=outro_mestre, aula=aula, atividade=atividade, resultados=[]
        )


def test_participante_invalido_recusa_o_lancamento_inteiro(
    sessao, criar_persona, criar_comunidade, criar_aula, criar_trilha, criar_missao, criar_atividade
):
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    guerreiro_valido = criar_persona(Papel.guerreiro, comunidade=comunidade)
    guerreiro_invalido = criar_persona(Papel.guerreiro, comunidade=comunidade)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    atividade = criar_atividade(missao, mestre)
    aula = criar_aula(mestre, comunidade)

    resultados = [
        ResultadoDeclarado(
            guerreiro_id=guerreiro_valido.id,
            atividade=atividade,
            momento_do_fato=MOMENTO_DO_FATO,
            producao="Produção.",
            desfecho=DesfechoDoResultado.realizada,
        ),
        ResultadoDeclarado(
            guerreiro_id=guerreiro_invalido.id,
            atividade=atividade,
            momento_do_fato=MOMENTO_DO_FATO,
            producao="Produção.",
            desfecho="desfecho-inexistente",
        ),
    ]

    with pytest.raises(ErroDeValidacao):
        lancar_resultados_da_atividade(
            sessao, operador=mestre, aula=aula, atividade=atividade, resultados=resultados
        )
    sessao.rollback()
    assert sessao.query(Resultado).count() == 0


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

    gravados = lancar_resultados_da_atividade(
        sessao,
        operador=admin,
        aula=aula,
        atividade=atividade,
        resultados=[_entrada(guerreiro, atividade=atividade)],
    )
    sessao.commit()

    assert gravados[0].autor_id == admin.id


def test_lancamento_pela_rota_grava_os_resultados(
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
        f"/v1/atividades/{atividade.id}/lancamentos",
        json={
            "aula_id": str(aula.id),
            "participantes": [
                {
                    "guerreiro_id": str(guerreiro.id),
                    "momento_do_fato": MOMENTO_DO_FATO.isoformat(),
                    "producao": "Produção do Guerreiro(a).",
                    "desfecho": "realizada",
                }
            ],
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert len(corpo) == 1
    assert corpo[0]["guerreiro_id"] == str(guerreiro.id)
    assert corpo[0]["atividade_id"] == str(atividade.id)


def test_mestre_que_nao_e_autor_e_recusado_pela_rota(
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
    mestre_autor = criar_persona(Papel.mestre)
    outro_mestre = criar_persona(Papel.mestre)
    token, _ = criar_sessao_de_teste(outro_mestre)
    comunidade = criar_comunidade()
    trilha = criar_trilha(mestre_autor)
    missao = criar_missao(trilha, mestre_autor)
    atividade = criar_atividade(missao, mestre_autor)
    aula = criar_aula(mestre_autor, comunidade)

    resposta = cliente.post(
        f"/v1/atividades/{atividade.id}/lancamentos",
        json={"aula_id": str(aula.id), "participantes": []},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 403


def test_edicao_de_lancamento_por_atividade_responde_405(
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
    """Não há `PUT` nem `PATCH` declarados sobre o lançamento por atividade:
    o FastAPI responde 405 sozinho ao método não previsto (`RF-09-47`)."""
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    token, _ = criar_sessao_de_teste(mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    atividade = criar_atividade(missao, mestre)

    resposta = cliente.put(
        f"/v1/atividades/{atividade.id}/lancamentos",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 405
