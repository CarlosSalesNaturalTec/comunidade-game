"""O painel do dia — leitura agregada do encontro em andamento (`RF-02-41`
a `RF-02-47`, `RF-02-69`, `RN-02-20`)."""

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nucleo.aulas.modelo import ModoDeComprovacao, SituacaoDaAula
from nucleo.aulas.regra import registrar_presenca
from nucleo.equipes.regra import declarar_escolha_da_equipe
from nucleo.painel_do_dia.regra import montar_painel_do_dia
from nucleo.personas.modelo import Papel
from nucleo.trilhas.modelo import SituacaoDaTrilha


def _cabecalhos(chave, token):
    return {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}


@pytest.fixture
def cenario(criar_persona, criar_comunidade, criar_ponto_de_apoio, criar_aula):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    aula = criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)
    return admin, comunidade, ponto_de_apoio, aula


def test_painel_devolve_o_encontro_em_andamento_numa_leitura(sessao, cenario):
    admin, _comunidade, _ponto, aula = cenario

    painel = montar_painel_do_dia(sessao, operador=admin)

    assert painel.aula_id == aula.id
    assert painel.presencas == []
    assert painel.equipes == []


def test_fora_de_qualquer_janela_o_painel_volta_vazio(
    sessao, criar_persona, criar_comunidade, criar_aula
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    agora = datetime.now(UTC)
    criar_aula(
        admin,
        comunidade,
        inicio_em=agora - timedelta(days=1, hours=2),
        fim_em=agora - timedelta(days=1),
    )

    painel = montar_painel_do_dia(sessao, operador=admin)

    assert painel.aula_id is None
    assert painel.presencas == []
    assert painel.pendencias == []


def test_mestre_le_apenas_o_encontro_da_sua_comunidade(
    sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio, criar_aula, criar_vinculo_jogador
):
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre)
    comunidade_do_mestre = criar_comunidade("Comunidade do Mestre")
    criar_vinculo_jogador(mestre, comunidade_do_mestre)
    outra_comunidade = criar_comunidade("Outra Comunidade")
    criar_aula(admin, outra_comunidade)

    painel = montar_painel_do_dia(sessao, operador=mestre)

    assert painel.aula_id is None


def test_guerreiro_recebe_403(sessao, criar_persona, cenario):
    _admin, _comunidade, _ponto, _aula = cenario
    guerreiro = criar_persona(Papel.guerreiro)

    from nucleo.erros import PermissaoNegada

    with pytest.raises(PermissaoNegada):
        montar_painel_do_dia(sessao, operador=guerreiro)


def test_presenca_do_reconhecimento_aparece_sem_lancamento_manual(
    sessao, criar_persona, cenario, criar_nick
):
    admin, comunidade, _ponto, aula = cenario
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    criar_nick(guerreiro, "zeferina")
    registrar_presenca(
        sessao,
        operador=guerreiro,
        aula=aula,
        guerreiro=guerreiro,
        modo=ModoDeComprovacao.reconhecimento.value,
        confirmador=None,
        momento_do_fato=datetime.now(UTC),
    )
    sessao.commit()

    painel = montar_painel_do_dia(sessao, operador=admin)

    assert len(painel.presencas) == 1
    assert painel.presencas[0].guerreiro_id == guerreiro.id
    assert painel.presencas[0].modo == "reconhecimento"
    assert painel.presencas[0].confirmador_id is None


def test_presenca_confirmada_mostra_quem_confirmou(sessao, criar_persona, cenario, criar_nick):
    admin, comunidade, _ponto, aula = cenario
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    criar_nick(guerreiro, "zeferina")
    registrar_presenca(
        sessao,
        operador=admin,
        aula=aula,
        guerreiro=guerreiro,
        modo=ModoDeComprovacao.confirmacao.value,
        confirmador=admin,
        momento_do_fato=datetime.now(UTC),
    )
    sessao.commit()

    painel = montar_painel_do_dia(sessao, operador=admin)

    assert painel.presencas[0].confirmador_id == admin.id


def test_presente_sem_equipe_aguarda_aparelho_e_sai_ao_entrar_numa_equipe(
    sessao, criar_persona, cenario, criar_nick, criar_equipe
):
    admin, comunidade, _ponto, aula = cenario
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    criar_nick(guerreiro, "zeferina")
    registrar_presenca(
        sessao,
        operador=guerreiro,
        aula=aula,
        guerreiro=guerreiro,
        modo=ModoDeComprovacao.reconhecimento.value,
        confirmador=None,
        momento_do_fato=datetime.now(UTC),
    )
    sessao.commit()

    painel = montar_painel_do_dia(sessao, operador=admin)
    assert len(painel.aguardando_aparelho) == 1
    assert painel.aguardando_aparelho[0].guerreiro_id == guerreiro.id

    criar_equipe(guerreiro, aula=aula)

    painel = montar_painel_do_dia(sessao, operador=admin)
    assert painel.aguardando_aparelho == []


def test_quem_nao_chegou_nao_aparece_em_lista_alguma(sessao, criar_persona, cenario):
    admin, comunidade, _ponto, _aula = cenario
    criar_persona(Papel.guerreiro, comunidade=comunidade)

    painel = montar_painel_do_dia(sessao, operador=admin)

    assert painel.presencas == []
    assert painel.aguardando_aparelho == []


def test_equipe_com_e_sem_missao(
    sessao, criar_persona, cenario, criar_equipe, criar_trilha, criar_missao, criar_atividade
):
    admin, comunidade, _ponto, aula = cenario
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    missao = criar_missao(trilha, mestre)
    atividade = criar_atividade(missao, mestre, aula=aula)

    guerreiro_com_missao = criar_persona(Papel.guerreiro, comunidade=comunidade)
    equipe_com_missao = criar_equipe(guerreiro_com_missao, aula=aula)
    declarar_escolha_da_equipe(
        sessao, operador=guerreiro_com_missao, equipe=equipe_com_missao, atividade=atividade
    )
    guerreiro_sem_missao = criar_persona(Papel.guerreiro, comunidade=comunidade)
    criar_equipe(guerreiro_sem_missao, aula=aula)
    sessao.commit()

    painel = montar_painel_do_dia(sessao, operador=admin)

    por_id = {equipe.id: equipe for equipe in painel.equipes}
    assert por_id[equipe_com_missao.id].missao_id == missao.id
    assert por_id[equipe_com_missao.id].missao_titulo == missao.titulo
    sem_missao = [e for e in painel.equipes if e.id != equipe_com_missao.id][0]
    assert sem_missao.missao_id is None


def test_saldo_pelo_ponto_de_apoio_da_aula_e_tipo_novo_aparece(
    sessao, criar_persona, cenario, criar_tipo_de_recurso, criar_lancamento
):
    admin, _comunidade, ponto_de_apoio, _aula = cenario

    painel_antes = montar_painel_do_dia(sessao, operador=admin)
    assert painel_antes.saldo_do_ponto_de_apoio == []

    tipo = criar_tipo_de_recurso(admin, nome="Kit MDF")
    criar_lancamento(admin, tipo, ponto_de_apoio, quantidade=Decimal("5.00"))

    painel = montar_painel_do_dia(sessao, operador=admin)

    saldos = {s.tipo_de_recurso_id: s.saldo for s in painel.saldo_do_ponto_de_apoio}
    assert saldos[tipo.id] == Decimal("5.00")


def test_previsto_e_provido_saem_juntos(
    sessao,
    criar_persona,
    cenario,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_tipo_de_recurso,
    criar_reserva,
):
    admin, _comunidade, ponto_de_apoio, aula = cenario
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    missao = criar_missao(trilha, mestre)
    atividade = criar_atividade(missao, mestre, aula=aula)
    tipo = criar_tipo_de_recurso(admin, nome="Lanche")
    criar_reserva(admin, aula, tipo, ponto_de_apoio, quantidade=Decimal("2.00"))

    painel = montar_painel_do_dia(sessao, operador=admin)

    assert len(painel.atividades_previstas) == 1
    assert painel.atividades_previstas[0].id == atividade.id
    assert len(painel.recursos_providos) == 1
    assert painel.recursos_providos[0].tipo_de_recurso_id == tipo.id
    assert painel.recursos_providos[0].quantidade == Decimal("2.00")


def test_lancamento_pendente_entra_e_sai(sessao, cenario):
    admin, _comunidade, _ponto, aula = cenario

    painel = montar_painel_do_dia(sessao, operador=admin)
    assert any(p.tipo == "lancamento_da_atividade_realizada" for p in painel.pendencias)

    aula.situacao = SituacaoDaAula.realizada
    sessao.commit()

    painel = montar_painel_do_dia(sessao, operador=admin)
    assert all(p.tipo != "lancamento_da_atividade_realizada" for p in painel.pendencias)


def test_termo_de_biometria_sem_digitalizacao_entra_e_sai_com_anexo(
    sessao,
    criar_persona,
    cenario,
    criar_nick,
    criar_vinculo,
    conceder_consentimento_biometrico,
    tmp_path,
):
    from nucleo.armazenamento.disco import ArmazenamentoEmDisco
    from nucleo.consentimentos.modelo import OrigemDoConsentimento
    from nucleo.consentimentos.regra import anexar_digitalizacao_do_termo

    admin, comunidade, _ponto, aula = cenario
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    criar_nick(guerreiro, "zeferina")
    responsavel = criar_persona(Papel.responsavel, criada_por=admin)
    criar_vinculo(responsavel, guerreiro, cadastrado_por=admin)
    consentimento = conceder_consentimento_biometrico(
        responsavel, guerreiro, operado_por=admin, origem=OrigemDoConsentimento.impressa
    )
    registrar_presenca(
        sessao,
        operador=guerreiro,
        aula=aula,
        guerreiro=guerreiro,
        modo=ModoDeComprovacao.reconhecimento.value,
        confirmador=None,
        momento_do_fato=datetime.now(UTC),
    )
    sessao.commit()

    painel = montar_painel_do_dia(sessao, operador=admin)
    pendencia = [p for p in painel.pendencias if p.tipo == "digitalizacao_do_termo"]
    assert len(pendencia) == 1
    assert pendencia[0].guerreiro_id == guerreiro.id
    assert pendencia[0].nick == "zeferina"
    assert pendencia[0].consentimento_id == consentimento.id

    armazenamento = ArmazenamentoEmDisco(str(tmp_path), str(tmp_path / "sessoes"))
    anexar_digitalizacao_do_termo(
        sessao,
        operador=admin,
        consentimento=consentimento,
        conteudo=b"conteudo",
        nome_original="termo.pdf",
        tipo_mime="application/pdf",
        armazenamento=armazenamento,
    )
    sessao.commit()

    painel = montar_painel_do_dia(sessao, operador=admin)
    assert all(p.tipo != "digitalizacao_do_termo" for p in painel.pendencias)


def test_painel_nao_lanca(sessao, cenario):
    admin, _comunidade, _ponto, aula = cenario

    montar_painel_do_dia(sessao, operador=admin)
    montar_painel_do_dia(sessao, operador=admin)

    assert aula.situacao == SituacaoDaAula.confirmada


def test_recusas_por_persona_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, cenario
):
    chave, _ = criar_chave()
    _admin, _comunidade, _ponto, _aula = cenario
    responsavel = criar_persona(Papel.responsavel)
    apoiador = criar_persona(Papel.apoiador)

    for persona in (responsavel, apoiador):
        token, _ = criar_sessao_de_teste(persona)
        resposta = cliente.get("/v1/painel-do-dia", headers=_cabecalhos(chave, token))
        assert resposta.status_code == 403


def test_painel_pela_rota_mostra_saldo_e_pendencias(
    cliente,
    criar_chave,
    criar_sessao_de_teste,
    criar_persona,
    cenario,
    criar_tipo_de_recurso,
    criar_lancamento,
):
    chave, _ = criar_chave()
    admin, _comunidade, ponto_de_apoio, _aula = cenario
    tipo = criar_tipo_de_recurso(admin, nome="Kit MDF")
    criar_lancamento(admin, tipo, ponto_de_apoio, quantidade=Decimal("3.00"))
    token, _ = criar_sessao_de_teste(admin)

    resposta = cliente.get("/v1/painel-do-dia", headers=_cabecalhos(chave, token))

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["saldo_do_ponto_de_apoio"][0]["tipo_de_recurso_id"] == str(tipo.id)
    assert any(p["tipo"] == "lancamento_da_atividade_realizada" for p in corpo["pendencias"])


def test_rota_do_painel_esta_no_openapi_sob_v1(cliente):
    schema = cliente.get("/openapi.json").json()

    assert "/v1/painel-do-dia" in schema["paths"]
    assert "get" in schema["paths"]["/v1/painel-do-dia"]
