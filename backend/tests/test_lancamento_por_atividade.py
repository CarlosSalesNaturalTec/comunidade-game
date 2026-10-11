from datetime import UTC, datetime

import pytest

from nucleo.aulas.modelo import SituacaoDaAula
from nucleo.erros import ErroDeValidacao, PermissaoNegada
from nucleo.personas.modelo import Papel
from nucleo.pontuacao.modelo import PontoRegular
from nucleo.pontuacao.regra import VALOR_BASE_EM_EQUIPE_COM_FAMILIAR
from nucleo.reservas.modelo import EstadoDaReserva
from nucleo.resultados.modelo import DesfechoDoResultado, Resultado
from nucleo.resultados.regra import (
    ResultadoDaEquipe,
    ResultadoDeclarado,
    lancar_resultados_da_atividade,
)
from nucleo.trilhas.modelo import ModalidadeDeAtividade

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

    gravados, fora = lancar_resultados_da_atividade(
        sessao, operador=mestre, aula=aula, atividade=atividade, resultados=resultados
    )
    sessao.commit()

    assert fora == []

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

    gravados, _ = lancar_resultados_da_atividade(
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
    assert len(corpo["resultados"]) == 1
    assert corpo["resultados"][0]["guerreiro_id"] == str(guerreiro.id)
    assert corpo["resultados"][0]["atividade_id"] == str(atividade.id)
    assert corpo["fora_por_falta_de_presenca"] == []


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


# `RF-02-112`, `RN-02-32`, `RN-02-33`: o mesmo ato por atividade é o
# caminho da atividade avulsa — por aluno ou pela equipe da aula.


def _avulsa(criar_atividade_avulsa, admin, aula, modalidade):
    return criar_atividade_avulsa(admin, aula=aula, modalidade=modalidade)


def test_admin_lanca_a_avulsa_sem_tocar_reserva_nem_situacao_da_aula(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_lancamento,
    criar_aula,
    criar_reserva,
    criar_atividade_avulsa,
):
    from decimal import Decimal

    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    criar_lancamento(admin, tipo, ponto_de_apoio, quantidade=Decimal("10.00"))
    aula = criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)
    reserva = criar_reserva(admin, aula, tipo, ponto_de_apoio, quantidade=Decimal("3.00"))
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    atividade = _avulsa(criar_atividade_avulsa, admin, aula, ModalidadeDeAtividade.individual)

    gravados, fora = lancar_resultados_da_atividade(
        sessao,
        operador=admin,
        aula=aula,
        atividade=atividade,
        resultados=[_entrada(guerreiro, atividade=atividade)],
    )
    sessao.commit()

    assert len(gravados) == 1
    assert fora == []
    sessao.refresh(aula)
    sessao.refresh(reserva)
    assert aula.situacao != SituacaoDaAula.realizada
    assert reserva.estado == EstadoDaReserva.reservada


def test_duas_avulsas_da_mesma_aula_sao_lancadas(
    sessao, criar_persona, criar_comunidade, criar_aula, criar_atividade_avulsa
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade)
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    uma = _avulsa(criar_atividade_avulsa, admin, aula, ModalidadeDeAtividade.individual)
    outra = _avulsa(criar_atividade_avulsa, admin, aula, ModalidadeDeAtividade.individual)

    for atividade in (uma, outra):
        lancar_resultados_da_atividade(
            sessao,
            operador=admin,
            aula=aula,
            atividade=atividade,
            resultados=[_entrada(guerreiro, atividade=atividade)],
        )
    sessao.commit()

    assert sessao.query(Resultado).count() == 2


def test_mestre_nao_lanca_a_avulsa(
    sessao, criar_persona, criar_comunidade, criar_aula, criar_atividade_avulsa
):
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade)
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    atividade = _avulsa(criar_atividade_avulsa, admin, aula, ModalidadeDeAtividade.individual)

    with pytest.raises(PermissaoNegada):
        lancar_resultados_da_atividade(
            sessao,
            operador=mestre,
            aula=aula,
            atividade=atividade,
            resultados=[_entrada(guerreiro, atividade=atividade)],
        )
    assert sessao.query(Resultado).count() == 0


def test_lancamento_por_equipe_vale_integral_a_cada_presente(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_atividade_avulsa,
    criar_equipe,
    adicionar_integrante,
    criar_presenca,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade)
    atividade = _avulsa(criar_atividade_avulsa, admin, aula, ModalidadeDeAtividade.em_equipe)
    integrantes = [criar_persona(Papel.guerreiro, comunidade=comunidade) for _ in range(3)]
    equipe = criar_equipe(integrantes[0], aula=aula)
    for guerreiro in integrantes[1:]:
        adicionar_integrante(equipe, guerreiro)
    for guerreiro in integrantes:
        criar_presenca(aula, guerreiro)

    gravados, fora = lancar_resultados_da_atividade(
        sessao,
        operador=admin,
        aula=aula,
        atividade=atividade,
        resultados=[],
        equipe=ResultadoDaEquipe(
            equipe_id=equipe.id,
            momento_do_fato=MOMENTO_DO_FATO,
            producao="Produção da equipe.",
            desfecho=DesfechoDoResultado.realizada,
        ),
    )
    sessao.commit()

    assert fora == []
    assert len(gravados) == 3
    assert {g.guerreiro_id for g in gravados} == {g.id for g in integrantes}
    assert {g.desfecho for g in gravados} == {DesfechoDoResultado.realizada}
    assert {g.producao for g in gravados} == {"Produção da equipe."}


def test_integrante_sem_presenca_fica_de_fora(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_atividade_avulsa,
    criar_equipe,
    adicionar_integrante,
    criar_presenca,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade)
    atividade = _avulsa(criar_atividade_avulsa, admin, aula, ModalidadeDeAtividade.em_equipe)
    integrantes = [criar_persona(Papel.guerreiro, comunidade=comunidade) for _ in range(4)]
    equipe = criar_equipe(integrantes[0], aula=aula)
    for guerreiro in integrantes[1:]:
        adicionar_integrante(equipe, guerreiro)
    for guerreiro in integrantes[:3]:
        criar_presenca(aula, guerreiro)

    gravados, fora = lancar_resultados_da_atividade(
        sessao,
        operador=admin,
        aula=aula,
        atividade=atividade,
        resultados=[],
        equipe=ResultadoDaEquipe(
            equipe_id=equipe.id,
            momento_do_fato=MOMENTO_DO_FATO,
            producao="Produção da equipe.",
            desfecho=DesfechoDoResultado.realizada,
        ),
    )
    sessao.commit()

    assert len(gravados) == 3
    assert fora == [integrantes[3].id]


def test_presenca_anulada_nao_conta_como_presenca(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_atividade_avulsa,
    criar_equipe,
    adicionar_integrante,
    criar_presenca,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade)
    atividade = _avulsa(criar_atividade_avulsa, admin, aula, ModalidadeDeAtividade.em_equipe)
    presente = criar_persona(Papel.guerreiro, comunidade=comunidade)
    anulado = criar_persona(Papel.guerreiro, comunidade=comunidade)
    equipe = criar_equipe(presente, aula=aula)
    adicionar_integrante(equipe, anulado)
    criar_presenca(aula, presente)
    criar_presenca(aula, anulado, anulada=True)

    gravados, fora = lancar_resultados_da_atividade(
        sessao,
        operador=admin,
        aula=aula,
        atividade=atividade,
        resultados=[],
        equipe=ResultadoDaEquipe(
            equipe_id=equipe.id,
            momento_do_fato=MOMENTO_DO_FATO,
            producao="Produção da equipe.",
            desfecho=DesfechoDoResultado.realizada,
        ),
    )
    sessao.commit()

    assert [g.guerreiro_id for g in gravados] == [presente.id]
    assert fora == [anulado.id]


def test_o_familiar_nao_recebe_resultado(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_atividade_avulsa,
    criar_equipe,
    adicionar_integrante,
    criar_presenca,
):
    """O integrante que não é Guerreiro(a) é pulado em silêncio — nunca
    recebeu Resultado para ficar de fora dele (`RN-02-32`)."""
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade)
    atividade = _avulsa(
        criar_atividade_avulsa, admin, aula, ModalidadeDeAtividade.em_equipe_com_familiar
    )
    guerreiros = [criar_persona(Papel.guerreiro, comunidade=comunidade) for _ in range(2)]
    familiar = criar_persona(Papel.responsavel)
    equipe = criar_equipe(guerreiros[0], aula=aula)
    adicionar_integrante(equipe, guerreiros[1])
    adicionar_integrante(equipe, familiar)
    for guerreiro in guerreiros:
        criar_presenca(aula, guerreiro)

    gravados, fora = lancar_resultados_da_atividade(
        sessao,
        operador=admin,
        aula=aula,
        atividade=atividade,
        resultados=[],
        equipe=ResultadoDaEquipe(
            equipe_id=equipe.id,
            momento_do_fato=MOMENTO_DO_FATO,
            producao="Produção da equipe.",
            desfecho=DesfechoDoResultado.realizada,
        ),
    )
    sessao.commit()

    assert {g.guerreiro_id for g in gravados} == {g.id for g in guerreiros}
    assert familiar.id not in fora
    pontos = sessao.query(PontoRegular).filter(PontoRegular.poder_id == atividade.poder_id)
    assert {ponto.guerreiro_id for ponto in pontos} == {g.id for g in guerreiros}
    assert {ponto.total for ponto in pontos} == {VALOR_BASE_EM_EQUIPE_COM_FAMILIAR}


def test_equipe_sem_nenhum_presente_e_recusada(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_atividade_avulsa,
    criar_equipe,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade)
    atividade = _avulsa(criar_atividade_avulsa, admin, aula, ModalidadeDeAtividade.em_equipe)
    equipe = criar_equipe(criar_persona(Papel.guerreiro, comunidade=comunidade), aula=aula)

    with pytest.raises(ErroDeValidacao) as excinfo:
        lancar_resultados_da_atividade(
            sessao,
            operador=admin,
            aula=aula,
            atividade=atividade,
            resultados=[],
            equipe=ResultadoDaEquipe(
                equipe_id=equipe.id,
                momento_do_fato=MOMENTO_DO_FATO,
                producao="Produção da equipe.",
                desfecho=DesfechoDoResultado.realizada,
            ),
        )
    assert excinfo.value.campo == "equipe_id"
    assert sessao.query(Resultado).count() == 0


def test_sem_equipe_e_sem_participantes_e_recusado(
    sessao, criar_persona, criar_comunidade, criar_aula, criar_atividade_avulsa
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade)
    atividade = _avulsa(criar_atividade_avulsa, admin, aula, ModalidadeDeAtividade.individual)

    with pytest.raises(ErroDeValidacao):
        lancar_resultados_da_atividade(
            sessao, operador=admin, aula=aula, atividade=atividade, resultados=[]
        )
    assert sessao.query(Resultado).count() == 0


def test_equipe_e_participantes_ao_mesmo_tempo_e_recusado(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_atividade_avulsa,
    criar_equipe,
    criar_presenca,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade)
    atividade = _avulsa(criar_atividade_avulsa, admin, aula, ModalidadeDeAtividade.em_equipe)
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    equipe = criar_equipe(guerreiro, aula=aula)
    criar_presenca(aula, guerreiro)

    with pytest.raises(ErroDeValidacao):
        lancar_resultados_da_atividade(
            sessao,
            operador=admin,
            aula=aula,
            atividade=atividade,
            resultados=[_entrada(guerreiro, atividade=atividade)],
            equipe=ResultadoDaEquipe(
                equipe_id=equipe.id,
                momento_do_fato=MOMENTO_DO_FATO,
                producao="Produção da equipe.",
                desfecho=DesfechoDoResultado.realizada,
            ),
        )
    assert sessao.query(Resultado).count() == 0


def test_atividade_individual_nao_se_lanca_por_equipe(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_atividade_avulsa,
    criar_equipe,
    criar_presenca,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade)
    atividade = _avulsa(criar_atividade_avulsa, admin, aula, ModalidadeDeAtividade.individual)
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    equipe = criar_equipe(guerreiro, aula=aula)
    criar_presenca(aula, guerreiro)

    with pytest.raises(ErroDeValidacao) as excinfo:
        lancar_resultados_da_atividade(
            sessao,
            operador=admin,
            aula=aula,
            atividade=atividade,
            resultados=[],
            equipe=ResultadoDaEquipe(
                equipe_id=equipe.id,
                momento_do_fato=MOMENTO_DO_FATO,
                producao="Produção da equipe.",
                desfecho=DesfechoDoResultado.realizada,
            ),
        )
    assert excinfo.value.campo == "equipe_id"
    assert sessao.query(Resultado).count() == 0


def test_atividade_em_equipe_nao_se_lanca_por_participante(
    sessao, criar_persona, criar_comunidade, criar_aula, criar_atividade_avulsa
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade)
    atividade = _avulsa(criar_atividade_avulsa, admin, aula, ModalidadeDeAtividade.em_equipe)
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)

    with pytest.raises(ErroDeValidacao) as excinfo:
        lancar_resultados_da_atividade(
            sessao,
            operador=admin,
            aula=aula,
            atividade=atividade,
            resultados=[_entrada(guerreiro, atividade=atividade)],
        )
    assert excinfo.value.campo == "participantes"
    assert sessao.query(Resultado).count() == 0


def test_segundo_resultado_do_mesmo_par_e_recusado(
    sessao, criar_persona, criar_comunidade, criar_aula, criar_atividade_avulsa
):
    """Antes de gravar qualquer um da lista: o ato roda várias vezes e o
    Resultado não se edita nem se remove (`RN-02-33`)."""
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade)
    atividade = _avulsa(criar_atividade_avulsa, admin, aula, ModalidadeDeAtividade.individual)
    repetido = criar_persona(Papel.guerreiro, comunidade=comunidade)
    novo = criar_persona(Papel.guerreiro, comunidade=comunidade)

    lancar_resultados_da_atividade(
        sessao,
        operador=admin,
        aula=aula,
        atividade=atividade,
        resultados=[_entrada(repetido, atividade=atividade)],
    )
    sessao.commit()

    with pytest.raises(ErroDeValidacao) as excinfo:
        lancar_resultados_da_atividade(
            sessao,
            operador=admin,
            aula=aula,
            atividade=atividade,
            resultados=[
                _entrada(novo, atividade=atividade),
                _entrada(repetido, atividade=atividade),
            ],
        )
    assert excinfo.value.campo == "guerreiro_id"
    sessao.rollback()
    assert sessao.query(Resultado).count() == 1


def test_lancamento_por_equipe_pela_rota_diz_quem_ficou_de_fora(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_aula,
    criar_atividade_avulsa,
    criar_equipe,
    adicionar_integrante,
    criar_presenca,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade)
    atividade = _avulsa(criar_atividade_avulsa, admin, aula, ModalidadeDeAtividade.em_equipe)
    presente = criar_persona(Papel.guerreiro, comunidade=comunidade)
    ausente = criar_persona(Papel.guerreiro, comunidade=comunidade)
    equipe = criar_equipe(presente, aula=aula)
    adicionar_integrante(equipe, ausente)
    criar_presenca(aula, presente)

    resposta = cliente.post(
        f"/v1/atividades/{atividade.id}/lancamentos",
        json={
            "aula_id": str(aula.id),
            "equipe": {
                "equipe_id": str(equipe.id),
                "momento_do_fato": MOMENTO_DO_FATO.isoformat(),
                "producao": "Produção da equipe.",
                "desfecho": "realizada",
            },
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert [item["guerreiro_id"] for item in corpo["resultados"]] == [str(presente.id)]
    assert corpo["fora_por_falta_de_presenca"] == [str(ausente.id)]


def test_atividade_de_trilha_nao_se_lanca_pela_equipe(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_equipe,
    criar_presenca,
):
    """O lançamento por equipe é da avulsa: `RN-02-33` é regra do PRD-02, e
    o ato por atividade de trilha, do Mestre na App 09, segue como está."""
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    atividade = criar_atividade(missao, mestre, modalidade=ModalidadeDeAtividade.em_equipe)
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    equipe = criar_equipe(guerreiro, aula=aula)
    criar_presenca(aula, guerreiro)

    with pytest.raises(ErroDeValidacao) as excinfo:
        lancar_resultados_da_atividade(
            sessao,
            operador=admin,
            aula=aula,
            atividade=atividade,
            resultados=[],
            equipe=ResultadoDaEquipe(
                equipe_id=equipe.id,
                momento_do_fato=MOMENTO_DO_FATO,
                producao="Produção da equipe.",
                desfecho=DesfechoDoResultado.realizada,
            ),
        )
    assert excinfo.value.campo == "equipe_id"

    # E a lista de participantes segue aceita na atividade de trilha em
    # equipe, como antes desta fatia.
    gravados, fora = lancar_resultados_da_atividade(
        sessao,
        operador=admin,
        aula=aula,
        atividade=atividade,
        resultados=[_entrada(guerreiro, atividade=atividade)],
    )
    sessao.commit()

    assert len(gravados) == 1
    assert fora == []
