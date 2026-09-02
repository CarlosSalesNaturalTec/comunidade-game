from datetime import UTC, datetime
from decimal import Decimal

import pytest

from nucleo.aportes.modelo import AporteDeclarado, OrigemDaEscolhaDoAporte
from nucleo.consentimentos.modelo import DecisaoDeConsentimento
from nucleo.desafios_extras.modelo import Modalidade, SituacaoDoDesafioExtra
from nucleo.desafios_extras.regra import registrar_conclusao_de_desafio_extra
from nucleo.efetividade_do_apoio.regra import montar_painel_de_efetividade
from nucleo.efetividade_do_apoio.rotas import roteador
from nucleo.erros import ErroDeValidacao
from nucleo.livro_razao.modelo import NaturezaDoLancamento
from nucleo.missoes_do_apoiador.modelo import MissaoDoApoiador, NivelDeNecessidade
from nucleo.ods.regra import criar_etiqueta_ods
from nucleo.personas.modelo import Papel
from nucleo.selos_do_apoiador.modelo import FamiliaDeSelo
from nucleo.tempo import agora


def _montar(sessao, proponente):
    return montar_painel_de_efetividade(sessao, proponente=proponente, ciclo_rotulo="Ciclo 01")


def _concluir(sessao, *, desafio, guerreiro, momento=None, recompensa_entregue=True, pontos=5):
    return registrar_conclusao_de_desafio_extra(
        sessao,
        desafio=desafio,
        guerreiro_id=guerreiro.id,
        momento_do_fato=momento or agora(),
        recompensa_entregue=recompensa_entregue,
        pontos_extras_creditados=pontos,
    )


def _autorizar_divulgacao(sessao, criar_persona, criar_consentimento, criar_nick, *, nick):
    responsavel = criar_persona(Papel.responsavel)
    guerreiro = criar_persona(Papel.guerreiro)
    criar_nick(guerreiro, nick)
    criar_consentimento(responsavel, guerreiro, decisao=DecisaoDeConsentimento.concede)
    return responsavel, guerreiro


# --- 2.7 — o painel é vivo -----------------------------------------------


def test_painel_e_vivo_contabiliza_conclusao_do_mesmo_dia(
    sessao,
    criar_persona,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
    criar_desafio_extra,
):
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(admin)
    tipo = criar_tipo_de_recurso(admin)
    ponto = criar_ponto_de_apoio(admin, criar_comunidade())
    desafio = criar_desafio_extra(
        apoiador, trilha, tipo, ponto, situacao=SituacaoDoDesafioExtra.publicado
    )

    antes = _montar(sessao, apoiador)
    assert len(antes.desafios.publicados) == 1
    assert len(antes.desafios.concluidos) == 0

    _concluir(sessao, desafio=desafio, guerreiro=guerreiro)

    depois = _montar(sessao, apoiador)
    assert len(depois.desafios.publicados) == 0
    assert len(depois.desafios.concluidos) == 1
    assert depois.desafios.concluidos[0].quantidade_de_conclusoes == 1


def test_nenhuma_rota_de_relatorio_fechado_existe():
    """Uma única leitura: o painel vivo, sem rota de fechamento nem
    periodicidade (`RF-14-40`, `RN-14-21`)."""
    rotas = [rota.path for rota in roteador.routes]
    assert rotas == ["/eu/desafios-extras/efetividade"]


# --- 2.7 — desafios por situação -----------------------------------------


def test_desafios_separados_por_situacao_e_nenhum_de_outro_proponente(
    sessao,
    criar_persona,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
    criar_desafio_extra,
):
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    outro_apoiador = criar_persona(Papel.apoiador)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(admin)
    tipo = criar_tipo_de_recurso(admin)
    ponto = criar_ponto_de_apoio(admin, criar_comunidade())

    proposto = criar_desafio_extra(
        apoiador, trilha, tipo, ponto, situacao=SituacaoDoDesafioExtra.em_validacao_do_mestre
    )
    publicado = criar_desafio_extra(
        apoiador, trilha, tipo, ponto, situacao=SituacaoDoDesafioExtra.publicado
    )
    concluido = criar_desafio_extra(
        apoiador, trilha, tipo, ponto, situacao=SituacaoDoDesafioExtra.publicado
    )
    criar_desafio_extra(apoiador, trilha, tipo, ponto, situacao=SituacaoDoDesafioExtra.recusado)
    criar_desafio_extra(
        outro_apoiador, trilha, tipo, ponto, situacao=SituacaoDoDesafioExtra.publicado
    )
    _concluir(sessao, desafio=concluido, guerreiro=guerreiro)

    painel = _montar(sessao, apoiador)

    assert [item.id for item in painel.desafios.propostos] == [proposto.id]
    assert [item.id for item in painel.desafios.publicados] == [publicado.id]
    assert [item.id for item in painel.desafios.concluidos] == [concluido.id]
    todos_os_ids = (
        {item.id for item in painel.desafios.propostos}
        | {item.id for item in painel.desafios.publicados}
        | {item.id for item in painel.desafios.concluidos}
    )
    assert len(todos_os_ids) == 3  # nenhum desafio de outro proponente, nenhum recusado


# --- 2.7 — contagem, trilha e período -------------------------------------


def test_contagem_trilha_e_periodo_do_desafio_concluido(
    sessao,
    criar_persona,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
    criar_desafio_extra,
):
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    primeiro_guerreiro = criar_persona(Papel.guerreiro)
    segundo_guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(admin, nome="Trilha das Águas")
    tipo = criar_tipo_de_recurso(admin)
    ponto = criar_ponto_de_apoio(admin, criar_comunidade())
    desafio = criar_desafio_extra(
        apoiador, trilha, tipo, ponto, situacao=SituacaoDoDesafioExtra.publicado
    )

    primeiro_momento = datetime(2026, 6, 1, 12, 0, tzinfo=UTC)
    ultimo_momento = datetime(2026, 6, 10, 12, 0, tzinfo=UTC)
    _concluir(sessao, desafio=desafio, guerreiro=primeiro_guerreiro, momento=primeiro_momento)
    _concluir(sessao, desafio=desafio, guerreiro=segundo_guerreiro, momento=ultimo_momento)

    painel = _montar(sessao, apoiador)
    item = painel.desafios.concluidos[0]

    assert item.trilha_id == trilha.id
    assert item.trilha_nome == "Trilha das Águas"
    assert item.quantidade_de_conclusoes == 2
    assert item.primeira_conclusao_em == primeiro_momento.date()
    assert item.ultima_conclusao_em == ultimo_momento.date()


def test_desafio_sem_conclusao_traz_contagem_zero(
    sessao,
    criar_persona,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
    criar_desafio_extra,
):
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    trilha = criar_trilha(admin)
    tipo = criar_tipo_de_recurso(admin)
    ponto = criar_ponto_de_apoio(admin, criar_comunidade())
    criar_desafio_extra(apoiador, trilha, tipo, ponto, situacao=SituacaoDoDesafioExtra.publicado)

    painel = _montar(sessao, apoiador)
    item = painel.desafios.publicados[0]

    assert item.quantidade_de_conclusoes == 0
    assert item.primeira_conclusao_em is None
    assert item.ultima_conclusao_em is None


# --- 2.7 — moedas aportadas ------------------------------------------------


def test_aporte_pendente_fora_do_painel_e_nenhum_valor_em_reais(
    sessao,
    criar_persona,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
    criar_lancamento,
    criar_aporte,
):
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    tipo = criar_tipo_de_recurso(admin)
    ponto = criar_ponto_de_apoio(admin, criar_comunidade())
    lancamento = criar_lancamento(admin, tipo, ponto, natureza=NaturezaDoLancamento.credito)

    criar_aporte(
        admin,
        apoiador,
        tipo,
        ponto,
        lancamento,
        valor_em_moedas=Decimal("20.00"),
        valor_de_origem=Decimal("100.00"),
        admin_homologador=admin,
    )
    # Declarado e ainda pendente: sem homologador, fora do painel.
    criar_aporte(admin, apoiador, tipo, ponto, lancamento, valor_em_moedas=Decimal("999.00"))

    painel = _montar(sessao, apoiador)

    assert painel.moedas.total_em_moedas == Decimal("20.00")
    assert len(painel.moedas.aportes) == 1
    campos = vars(painel.moedas.aportes[0])
    assert "valor_de_origem" not in campos
    assert all("real" not in nome_do_campo for nome_do_campo in campos)


def test_aporte_mostra_a_missao_ou_o_desafio_extra_que_custeou(
    sessao,
    criar_persona,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
    criar_aula,
    criar_lancamento,
    criar_aporte,
    criar_desafio_extra,
):
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    comunidade = criar_comunidade()
    tipo = criar_tipo_de_recurso(admin)
    ponto = criar_ponto_de_apoio(admin, comunidade)
    aula = criar_aula(admin, comunidade, ponto_de_apoio=ponto)
    trilha = criar_trilha(admin)

    missao = MissaoDoApoiador(
        aula_id=aula.id,
        tipo_de_recurso_id=tipo.id,
        nivel_de_necessidade=NivelDeNecessidade.acontecer,
        titulo="O lanche do encontro",
        o_que_se_pede="Um lanche para vinte crianças",
        quantidade=Decimal("100.00"),
        prazo=agora().date(),
        selo_nome="Lanche garantido",
        selo_familia=FamiliaDeSelo.frente,
        autor_id=admin.id,
        papel_do_autor=admin.papel.value,
    )
    sessao.add(missao)
    sessao.flush()
    declaracao = AporteDeclarado(
        provedor_id=apoiador.id,
        valor_declarado=Decimal("20.00"),
        origem_da_escolha=OrigemDaEscolhaDoAporte.missao,
        missao_do_apoiador_id=missao.id,
        autor_id=apoiador.id,
        papel_do_autor=apoiador.papel.value,
    )
    sessao.add(declaracao)
    sessao.flush()

    lancamento = criar_lancamento(admin, tipo, ponto, natureza=NaturezaDoLancamento.credito)
    aporte_da_missao = criar_aporte(
        admin,
        apoiador,
        tipo,
        ponto,
        lancamento,
        valor_em_moedas=Decimal("20.00"),
        admin_homologador=admin,
    )
    aporte_da_missao.aporte_declarado_id = declaracao.id
    sessao.commit()

    aporte_do_desafio = criar_aporte(
        admin,
        apoiador,
        tipo,
        ponto,
        lancamento,
        valor_em_moedas=Decimal("5.00"),
        admin_homologador=admin,
    )
    criar_desafio_extra(
        apoiador,
        trilha,
        tipo,
        ponto,
        situacao=SituacaoDoDesafioExtra.em_validacao_do_mestre,
        aporte=aporte_do_desafio,
    )

    painel = _montar(sessao, apoiador)
    por_id = {aporte.id: aporte for aporte in painel.moedas.aportes}

    assert por_id[aporte_da_missao.id].custeio_tipo == "missao"
    assert por_id[aporte_da_missao.id].custeio_descricao == "O lanche do encontro"
    assert por_id[aporte_do_desafio.id].custeio_tipo == "desafio_extra"
    assert por_id[aporte_do_desafio.id].custeio_descricao == trilha.nome


# --- 2.7 — cobertura de ODS -------------------------------------------------


def test_cobertura_por_comunidade_e_ciclo_e_etiquetas_herdadas_sem_conclusao(
    sessao,
    criar_persona,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
    criar_desafio_extra,
):
    mestre = criar_persona(Papel.mestre)
    apoiador = criar_persona(Papel.apoiador)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    trilha = criar_trilha(mestre)
    criar_etiqueta_ods(sessao, operador=mestre, objetivo=4, trilha=trilha)
    tipo = criar_tipo_de_recurso(mestre)
    ponto = criar_ponto_de_apoio(mestre, comunidade)
    desafio = criar_desafio_extra(
        apoiador, trilha, tipo, ponto, situacao=SituacaoDoDesafioExtra.publicado
    )

    sem_conclusao = _montar(sessao, apoiador)
    item_publicado = sem_conclusao.desafios.publicados[0]
    assert item_publicado.etiquetas_ods == [4]
    assert sem_conclusao.cobertura_de_ods.por_comunidade == []

    _concluir(sessao, desafio=desafio, guerreiro=guerreiro)

    com_conclusao = _montar(sessao, apoiador)
    cobertura = com_conclusao.cobertura_de_ods.por_comunidade
    assert len(cobertura) == 1
    assert cobertura[0].comunidade_virtual_id == comunidade.id
    assert cobertura[0].objetivos == [4]
    assert cobertura[0].ciclo_rotulo == "Ciclo 01"
    assert not hasattr(cobertura[0], "guerreiro_id")


# --- 2.7 — avatar e nick só com divulgação autorizada -----------------------


def test_avatar_e_nick_so_com_divulgacao_autorizada_e_revogacao(
    sessao,
    criar_persona,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
    criar_desafio_extra,
    criar_consentimento,
    criar_nick,
):
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    trilha = criar_trilha(admin)
    tipo = criar_tipo_de_recurso(admin)
    ponto = criar_ponto_de_apoio(admin, criar_comunidade())
    desafio = criar_desafio_extra(
        apoiador, trilha, tipo, ponto, situacao=SituacaoDoDesafioExtra.publicado
    )

    responsavel, autorizado = _autorizar_divulgacao(
        sessao, criar_persona, criar_consentimento, criar_nick, nick="guerreira-autorizada"
    )
    nao_autorizado = criar_persona(Papel.guerreiro)

    _concluir(sessao, desafio=desafio, guerreiro=autorizado)
    _concluir(sessao, desafio=desafio, guerreiro=nao_autorizado)

    painel = _montar(sessao, apoiador)
    item = painel.desafios.concluidos[0]
    assert item.quantidade_de_conclusoes == 2
    assert [c.nick for c in item.concluintes_exibiveis] == ["guerreira-autorizada"]
    assert item.concluintes_nao_identificados == 1

    # Revogação: a leitura seguinte deixa de exibir o avatar e o nick,
    # mantendo a contagem (`RN-14-22`).
    criar_consentimento(responsavel, autorizado, decisao=DecisaoDeConsentimento.nega)

    painel_apos_revogacao = _montar(sessao, apoiador)
    item_apos = painel_apos_revogacao.desafios.concluidos[0]
    assert item_apos.quantidade_de_conclusoes == 2
    assert item_apos.concluintes_exibiveis == []
    assert item_apos.concluintes_nao_identificados == 2


# --- 2.7 — direcionado -------------------------------------------------------


def test_direcionado_mostra_apenas_houve_conclusao(
    sessao,
    criar_persona,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
    criar_desafio_extra,
):
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    comunidade = criar_comunidade()
    destinatario = criar_persona(Papel.guerreiro, comunidade=comunidade)
    trilha = criar_trilha(admin)
    tipo = criar_tipo_de_recurso(admin)
    ponto = criar_ponto_de_apoio(admin, comunidade)
    desafio = criar_desafio_extra(
        apoiador,
        trilha,
        tipo,
        ponto,
        situacao=SituacaoDoDesafioExtra.publicado,
        modalidade=Modalidade.direcionado,
        nick_do_destinatario="nick-do-destinatario",
        justificativa_do_vinculo="É meu vizinho.",
    )

    ainda_nao_concluido = _montar(sessao, apoiador)
    item = ainda_nao_concluido.desafios.publicados[0]
    assert item.houve_conclusao is False
    assert item.quantidade_de_conclusoes is None
    assert item.concluintes_exibiveis is None

    _concluir(sessao, desafio=desafio, guerreiro=destinatario)

    concluido = _montar(sessao, apoiador)
    item_concluido = concluido.desafios.concluidos[0]
    assert item_concluido.houve_conclusao is True
    assert item_concluido.quantidade_de_conclusoes is None
    assert item_concluido.concluintes_exibiveis is None
    # O direcionado nunca entra na agregação por comunidade (design — decisão 6).
    assert concluido.cobertura_de_ods.por_comunidade == []


# --- 2.7 — restrição de papel e sessão --------------------------------------


def test_outro_papel_e_recusado_pela_rota(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
):
    chave, _ = criar_chave()
    mestre = criar_persona(Papel.mestre)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.get(
        "/v1/eu/desafios-extras/efetividade",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 403


def test_apoiador_le_o_proprio_painel_pela_rota(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
    criar_desafio_extra,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    token, _ = criar_sessao_de_teste(apoiador)
    trilha = criar_trilha(admin)
    tipo = criar_tipo_de_recurso(admin)
    ponto = criar_ponto_de_apoio(admin, criar_comunidade())
    criar_desafio_extra(apoiador, trilha, tipo, ponto, situacao=SituacaoDoDesafioExtra.publicado)

    resposta = cliente.get(
        "/v1/eu/desafios-extras/efetividade",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert len(corpo["desafios"]["publicados"]) == 1
    assert corpo["moedas"]["total_em_moedas"] == "0"
    assert corpo["cobertura_de_ods"]["por_comunidade"] == []


def test_desafio_nao_publicado_nao_recebe_conclusao_ainda_que_solicitado(
    sessao,
    criar_persona,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
    criar_desafio_extra,
):
    """Guarda-cerca: garante que a leitura da efetividade não some conclusão
    para desafio não publicado — cenário que a regra de 1.3 já recusa."""
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(admin)
    tipo = criar_tipo_de_recurso(admin)
    ponto = criar_ponto_de_apoio(admin, criar_comunidade())
    desafio = criar_desafio_extra(
        apoiador, trilha, tipo, ponto, situacao=SituacaoDoDesafioExtra.em_aprovacao_do_admin
    )

    with pytest.raises(ErroDeValidacao):
        _concluir(sessao, desafio=desafio, guerreiro=guerreiro)

    sessao.rollback()
    painel = _montar(sessao, apoiador)
    assert painel.desafios.propostos[0].id == desafio.id
