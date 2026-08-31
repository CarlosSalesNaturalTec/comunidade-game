"""As retomadas em aberto do Guerreiro(a) — `RF-05-79`, `RF-05-80`,
`RN-05-38`, `RN-05-05`, `RN-05-21`, do PRD-05 §9."""

from datetime import UTC, datetime, timedelta

from nucleo.livro_razao.modelo import Lancamento
from nucleo.personas.modelo import Papel
from nucleo.producoes.modelo import FormaDeEntregaDaProducao, ProducaoDaMissao
from nucleo.resultados.modelo import Resultado
from nucleo.trilhas.modelo import SituacaoDaTrilha
from nucleo.trilhas.regra import retomadas_em_aberto_do_guerreiro


def _cabecalhos(chave, token):
    return {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}


def _montar_missao_com_cadencia(
    *,
    criar_persona,
    criar_trilha,
    criar_missao,
    cadencia_de_retomada,
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    missao = criar_missao(trilha, mestre, cadencia_de_retomada=cadencia_de_retomada)
    return mestre, trilha, missao


def _desbloquear_ha(sessao, *, guerreiro, missao, criar_inscricao_na_trilha, dias_atras):
    from nucleo.trilhas.modelo import Trilha

    trilha = sessao.get(Trilha, missao.trilha_id)
    criar_inscricao_na_trilha(guerreiro, trilha)
    from nucleo.trilhas.modelo import DesbloqueioDaMissao

    desbloqueio = DesbloqueioDaMissao(guerreiro_id=guerreiro.id, missao_id=missao.id, aprovado=True)
    sessao.add(desbloqueio)
    sessao.flush()
    desbloqueio.momento = datetime.now(UTC) - timedelta(days=dias_atras)
    sessao.commit()
    sessao.refresh(desbloqueio)
    return desbloqueio


def _registrar_producao(sessao, *, guerreiro, missao, atividade, momento):
    producao = ProducaoDaMissao(
        equipe_id=None,
        guerreiro_id=guerreiro.id,
        missao_id=missao.id,
        atividade_id=atividade.id,
        forma=FormaDeEntregaDaProducao.texto,
        transcricao="Produção de teste.",
        devolutiva="Devolutiva de teste.",
        autor_id=guerreiro.id,
        papel_do_autor=guerreiro.papel.value,
    )
    sessao.add(producao)
    sessao.flush()
    producao.registrado_em = momento
    sessao.commit()
    sessao.refresh(producao)
    return producao


def test_cadencia_declarada_vira_agendamentos_contados_do_desbloqueio(
    sessao, criar_persona, criar_trilha, criar_missao, criar_inscricao_na_trilha
):
    guerreiro = criar_persona(Papel.guerreiro)
    _, _, missao = _montar_missao_com_cadencia(
        criar_persona=criar_persona,
        criar_trilha=criar_trilha,
        criar_missao=criar_missao,
        cadencia_de_retomada=[2, 7, 21],
    )
    desbloqueio = _desbloquear_ha(
        sessao,
        guerreiro=guerreiro,
        missao=missao,
        criar_inscricao_na_trilha=criar_inscricao_na_trilha,
        dias_atras=30,
    )

    retomadas = retomadas_em_aberto_do_guerreiro(sessao, guerreiro_id=guerreiro.id)

    prazos = sorted(item.prazo for item in retomadas)
    esperados = sorted(desbloqueio.momento + timedelta(days=d) for d in (2, 7, 21))
    assert prazos == esperados


def test_so_o_agendamento_vencido_aparece_em_aberto(
    sessao, criar_persona, criar_trilha, criar_missao, criar_inscricao_na_trilha
):
    guerreiro = criar_persona(Papel.guerreiro)
    _, _, missao = _montar_missao_com_cadencia(
        criar_persona=criar_persona,
        criar_trilha=criar_trilha,
        criar_missao=criar_missao,
        cadencia_de_retomada=[2, 7, 21],
    )
    _desbloquear_ha(
        sessao,
        guerreiro=guerreiro,
        missao=missao,
        criar_inscricao_na_trilha=criar_inscricao_na_trilha,
        dias_atras=3,
    )

    retomadas = retomadas_em_aberto_do_guerreiro(sessao, guerreiro_id=guerreiro.id)

    assert len(retomadas) == 1


def test_missao_sem_cadencia_declarada_nao_gera_retomada(
    sessao, criar_persona, criar_trilha, criar_missao, criar_inscricao_na_trilha
):
    guerreiro = criar_persona(Papel.guerreiro)
    _, _, missao = _montar_missao_com_cadencia(
        criar_persona=criar_persona,
        criar_trilha=criar_trilha,
        criar_missao=criar_missao,
        cadencia_de_retomada=None,
    )
    _desbloquear_ha(
        sessao,
        guerreiro=guerreiro,
        missao=missao,
        criar_inscricao_na_trilha=criar_inscricao_na_trilha,
        dias_atras=30,
    )

    assert retomadas_em_aberto_do_guerreiro(sessao, guerreiro_id=guerreiro.id) == []


def test_missao_nao_desbloqueada_nao_gera_retomada(
    sessao, criar_persona, criar_trilha, criar_missao, criar_inscricao_na_trilha
):
    guerreiro = criar_persona(Papel.guerreiro)
    _, trilha, _missao = _montar_missao_com_cadencia(
        criar_persona=criar_persona,
        criar_trilha=criar_trilha,
        criar_missao=criar_missao,
        cadencia_de_retomada=[2],
    )
    criar_inscricao_na_trilha(guerreiro, trilha)

    assert retomadas_em_aberto_do_guerreiro(sessao, guerreiro_id=guerreiro.id) == []


def test_desbloqueio_pratico_nao_julgado_nao_abre_agendamento(
    sessao, criar_persona, criar_trilha, criar_missao, criar_inscricao_na_trilha
):
    guerreiro = criar_persona(Papel.guerreiro)
    _, trilha, missao = _montar_missao_com_cadencia(
        criar_persona=criar_persona,
        criar_trilha=criar_trilha,
        criar_missao=criar_missao,
        cadencia_de_retomada=[2],
    )
    criar_inscricao_na_trilha(guerreiro, trilha)
    from nucleo.trilhas.modelo import DesbloqueioDaMissao

    desbloqueio = DesbloqueioDaMissao(guerreiro_id=guerreiro.id, missao_id=missao.id, aprovado=None)
    sessao.add(desbloqueio)
    sessao.flush()
    desbloqueio.momento = datetime.now(UTC) - timedelta(days=30)
    sessao.commit()

    assert retomadas_em_aberto_do_guerreiro(sessao, guerreiro_id=guerreiro.id) == []


def test_retomada_e_de_cada_guerreiro_pelo_desbloqueio_dele(
    sessao, criar_persona, criar_trilha, criar_missao, criar_inscricao_na_trilha
):
    guerreiro_1 = criar_persona(Papel.guerreiro)
    guerreiro_2 = criar_persona(Papel.guerreiro)
    _, _, missao = _montar_missao_com_cadencia(
        criar_persona=criar_persona,
        criar_trilha=criar_trilha,
        criar_missao=criar_missao,
        cadencia_de_retomada=[2],
    )
    desbloqueio_1 = _desbloquear_ha(
        sessao,
        guerreiro=guerreiro_1,
        missao=missao,
        criar_inscricao_na_trilha=criar_inscricao_na_trilha,
        dias_atras=10,
    )
    desbloqueio_2 = _desbloquear_ha(
        sessao,
        guerreiro=guerreiro_2,
        missao=missao,
        criar_inscricao_na_trilha=criar_inscricao_na_trilha,
        dias_atras=5,
    )

    retomadas_1 = retomadas_em_aberto_do_guerreiro(sessao, guerreiro_id=guerreiro_1.id)
    retomadas_2 = retomadas_em_aberto_do_guerreiro(sessao, guerreiro_id=guerreiro_2.id)

    assert retomadas_1[0].prazo == desbloqueio_1.momento + timedelta(days=2)
    assert retomadas_2[0].prazo == desbloqueio_2.momento + timedelta(days=2)
    assert retomadas_1[0].prazo != retomadas_2[0].prazo


def test_producao_entregue_fecha_o_agendamento_vencido(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_inscricao_na_trilha,
):
    guerreiro = criar_persona(Papel.guerreiro)
    mestre, _, missao = _montar_missao_com_cadencia(
        criar_persona=criar_persona,
        criar_trilha=criar_trilha,
        criar_missao=criar_missao,
        cadencia_de_retomada=[2],
    )
    atividade = criar_atividade(missao, mestre)
    desbloqueio = _desbloquear_ha(
        sessao,
        guerreiro=guerreiro,
        missao=missao,
        criar_inscricao_na_trilha=criar_inscricao_na_trilha,
        dias_atras=5,
    )
    _registrar_producao(
        sessao,
        guerreiro=guerreiro,
        missao=missao,
        atividade=atividade,
        momento=desbloqueio.momento + timedelta(days=3),
    )

    assert retomadas_em_aberto_do_guerreiro(sessao, guerreiro_id=guerreiro.id) == []


def test_segunda_entrega_nao_reabre_nem_duplica_o_agendamento(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_inscricao_na_trilha,
):
    guerreiro = criar_persona(Papel.guerreiro)
    mestre, _, missao = _montar_missao_com_cadencia(
        criar_persona=criar_persona,
        criar_trilha=criar_trilha,
        criar_missao=criar_missao,
        cadencia_de_retomada=[2],
    )
    atividade = criar_atividade(missao, mestre)
    desbloqueio = _desbloquear_ha(
        sessao,
        guerreiro=guerreiro,
        missao=missao,
        criar_inscricao_na_trilha=criar_inscricao_na_trilha,
        dias_atras=5,
    )
    _registrar_producao(
        sessao,
        guerreiro=guerreiro,
        missao=missao,
        atividade=atividade,
        momento=desbloqueio.momento + timedelta(days=3),
    )
    _registrar_producao(
        sessao,
        guerreiro=guerreiro,
        missao=missao,
        atividade=atividade,
        momento=desbloqueio.momento + timedelta(days=4),
    )

    assert retomadas_em_aberto_do_guerreiro(sessao, guerreiro_id=guerreiro.id) == []


def test_refazer_antes_do_prazo_nao_consome_agendamento(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_inscricao_na_trilha,
):
    guerreiro = criar_persona(Papel.guerreiro)
    mestre, _, missao = _montar_missao_com_cadencia(
        criar_persona=criar_persona,
        criar_trilha=criar_trilha,
        criar_missao=criar_missao,
        cadencia_de_retomada=[2],
    )
    atividade = criar_atividade(missao, mestre)
    desbloqueio = _desbloquear_ha(
        sessao,
        guerreiro=guerreiro,
        missao=missao,
        criar_inscricao_na_trilha=criar_inscricao_na_trilha,
        dias_atras=1,
    )
    _registrar_producao(
        sessao,
        guerreiro=guerreiro,
        missao=missao,
        atividade=atividade,
        momento=desbloqueio.momento + timedelta(hours=1),
    )

    assert retomadas_em_aberto_do_guerreiro(sessao, guerreiro_id=guerreiro.id) == []


def test_agendamento_seguinte_vence_normalmente(
    sessao, criar_persona, criar_trilha, criar_missao, criar_inscricao_na_trilha
):
    guerreiro = criar_persona(Papel.guerreiro)
    _, _, missao = _montar_missao_com_cadencia(
        criar_persona=criar_persona,
        criar_trilha=criar_trilha,
        criar_missao=criar_missao,
        cadencia_de_retomada=[2, 7],
    )
    _desbloquear_ha(
        sessao,
        guerreiro=guerreiro,
        missao=missao,
        criar_inscricao_na_trilha=criar_inscricao_na_trilha,
        dias_atras=8,
    )

    retomadas = retomadas_em_aberto_do_guerreiro(sessao, guerreiro_id=guerreiro.id)

    assert len(retomadas) == 2


def test_retomada_nao_credita_ponto(
    cliente,
    criar_chave,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_inscricao_na_trilha,
    criar_sessao_de_teste,
    sessao,
):
    chave, _ = criar_chave()
    mestre, _, missao = _montar_missao_com_cadencia(
        criar_persona=criar_persona,
        criar_trilha=criar_trilha,
        criar_missao=criar_missao,
        cadencia_de_retomada=[2],
    )
    atividade = criar_atividade(missao, mestre, producao_esperada="Um texto sobre o tema.")
    guerreiro = criar_persona(Papel.guerreiro)
    _desbloquear_ha(
        sessao,
        guerreiro=guerreiro,
        missao=missao,
        criar_inscricao_na_trilha=criar_inscricao_na_trilha,
        dias_atras=5,
    )
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.post(
        f"/v1/eu/missoes/{missao.id}/producao",
        data={"forma": "texto", "texto": "Refazendo.", "atividade_id": str(atividade.id)},
        headers=_cabecalhos(chave, token),
    )

    assert resposta.status_code == 201
    assert sessao.query(Resultado).count() == 0
    assert sessao.query(Lancamento).count() == 0
    assert retomadas_em_aberto_do_guerreiro(sessao, guerreiro_id=guerreiro.id) == []


# --- Os cenários HTTP de `GET /v1/eu/retomadas` — `RF-05-79`, `RN-05-21` ---


def test_guerreiro_le_as_proprias_retomadas(
    cliente,
    criar_chave,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_inscricao_na_trilha,
    criar_sessao_de_teste,
    sessao,
):
    chave, _ = criar_chave()
    guerreiro = criar_persona(Papel.guerreiro)
    _, trilha, missao = _montar_missao_com_cadencia(
        criar_persona=criar_persona,
        criar_trilha=criar_trilha,
        criar_missao=criar_missao,
        cadencia_de_retomada=[2],
    )
    _desbloquear_ha(
        sessao,
        guerreiro=guerreiro,
        missao=missao,
        criar_inscricao_na_trilha=criar_inscricao_na_trilha,
        dias_atras=5,
    )
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.get("/v1/eu/retomadas", headers=_cabecalhos(chave, token))

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert len(corpo) == 1
    assert corpo[0]["missao_id"] == str(missao.id)
    assert corpo[0]["trilha_id"] == str(trilha.id)
    assert "prazo" in corpo[0]


def test_sem_retomada_em_aberto_a_lista_vem_vazia(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    guerreiro = criar_persona(Papel.guerreiro)
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.get("/v1/eu/retomadas", headers=_cabecalhos(chave, token))

    assert resposta.status_code == 200
    assert resposta.json() == []


def test_retomada_de_terceiro_nao_aparece(
    cliente,
    criar_chave,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_inscricao_na_trilha,
    criar_sessao_de_teste,
    sessao,
):
    chave, _ = criar_chave()
    _, _, missao = _montar_missao_com_cadencia(
        criar_persona=criar_persona,
        criar_trilha=criar_trilha,
        criar_missao=criar_missao,
        cadencia_de_retomada=[2],
    )
    outro_guerreiro = criar_persona(Papel.guerreiro)
    _desbloquear_ha(
        sessao,
        guerreiro=outro_guerreiro,
        missao=missao,
        criar_inscricao_na_trilha=criar_inscricao_na_trilha,
        dias_atras=5,
    )
    guerreiro_em_sessao = criar_persona(Papel.guerreiro)
    token, _ = criar_sessao_de_teste(guerreiro_em_sessao)

    resposta = cliente.get("/v1/eu/retomadas", headers=_cabecalhos(chave, token))

    assert resposta.status_code == 200
    assert resposta.json() == []


def test_gestao_nao_le_retomadas_por_esta_porta(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    for operador in (criar_persona(Papel.mestre), criar_persona(Papel.admin)):
        token, _ = criar_sessao_de_teste(operador)
        resposta = cliente.get("/v1/eu/retomadas", headers=_cabecalhos(chave, token))
        assert resposta.status_code == 403
