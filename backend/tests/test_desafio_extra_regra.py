from datetime import date
from decimal import Decimal

import pytest

from nucleo.desafios_extras.modelo import (
    CusteioDoDesafioExtra,
    FormatoDoDesafioExtra,
    Modalidade,
    SituacaoDoDesafioExtra,
)
from nucleo.desafios_extras.regra import (
    conferir_editavel,
    conferir_publicacao_com_lastro,
    lastro_provido,
    listar_desafios_do_proponente,
    propor_desafio_extra,
)
from nucleo.erros import EdicaoDeDesafioExtraPublicadoRecusada, ErroDeValidacao, PermissaoNegada
from nucleo.livro_razao.modelo import NaturezaDoLancamento
from nucleo.personas.modelo import Papel
from nucleo.trilhas.modelo import SituacaoDaTrilha


def _propor(
    sessao,
    *,
    apoiador,
    trilha,
    tipo,
    ponto,
    modalidade=Modalidade.aberto,
    nick_do_destinatario=None,
    justificativa_do_vinculo=None,
    quantidade_disponivel=5,
    pontos_extras=5,
    formato=FormatoDoDesafioExtra.on_line,
    custeio=CusteioDoDesafioExtra.saldo_de_recurso,
    aporte=None,
    missao=None,
):
    return propor_desafio_extra(
        sessao,
        operador=apoiador,
        trilha=trilha,
        missao=missao,
        modalidade=modalidade,
        nick_do_destinatario=nick_do_destinatario,
        justificativa_do_vinculo=justificativa_do_vinculo,
        tipo_de_recurso=tipo,
        ponto_de_apoio=ponto,
        quantidade_disponivel=quantidade_disponivel,
        criterio_de_atribuicao="Quem entregar primeiro.",
        pontos_extras=pontos_extras,
        formato=formato,
        custeio=custeio,
        aporte=aporte,
        vigencia_inicio=date(2026, 1, 1),
        vigencia_fim=date(2026, 12, 31),
    )


# --- 2.1 e 2.2 — a proposta ---------------------------------------------------


def test_proposta_completa_e_registrada(
    sessao,
    criar_persona,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
):
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    trilha = criar_trilha(admin, situacao=SituacaoDaTrilha.publicada)
    tipo = criar_tipo_de_recurso(admin)
    ponto = criar_ponto_de_apoio(admin, criar_comunidade())

    desafio = _propor(sessao, apoiador=apoiador, trilha=trilha, tipo=tipo, ponto=ponto)

    assert desafio.trilha_id == trilha.id
    assert desafio.autor_id == apoiador.id
    assert desafio.situacao == SituacaoDoDesafioExtra.em_validacao_do_mestre


def test_so_apoiador_propoe_desafio_extra(
    sessao,
    criar_persona,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
):
    admin = criar_persona(Papel.admin)
    trilha = criar_trilha(admin, situacao=SituacaoDaTrilha.publicada)
    tipo = criar_tipo_de_recurso(admin)
    ponto = criar_ponto_de_apoio(admin, criar_comunidade())

    with pytest.raises(PermissaoNegada):
        _propor(sessao, apoiador=admin, trilha=trilha, tipo=tipo, ponto=ponto)


def test_trilha_fora_de_andamento_e_recusada(
    sessao,
    criar_persona,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
):
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    trilha = criar_trilha(admin, situacao=SituacaoDaTrilha.rascunho)
    tipo = criar_tipo_de_recurso(admin)
    ponto = criar_ponto_de_apoio(admin, criar_comunidade())

    with pytest.raises(ErroDeValidacao):
        _propor(sessao, apoiador=apoiador, trilha=trilha, tipo=tipo, ponto=ponto)


def test_ausencia_de_formato_e_recusada(
    sessao,
    criar_persona,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
):
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    trilha = criar_trilha(admin, situacao=SituacaoDaTrilha.publicada)
    tipo = criar_tipo_de_recurso(admin)
    ponto = criar_ponto_de_apoio(admin, criar_comunidade())

    with pytest.raises(ErroDeValidacao):
        propor_desafio_extra(
            sessao,
            operador=apoiador,
            trilha=trilha,
            missao=None,
            modalidade=Modalidade.aberto,
            nick_do_destinatario=None,
            justificativa_do_vinculo=None,
            tipo_de_recurso=tipo,
            ponto_de_apoio=ponto,
            quantidade_disponivel=5,
            criterio_de_atribuicao="Quem entregar primeiro.",
            pontos_extras=5,
            formato=None,
            custeio=CusteioDoDesafioExtra.saldo_de_recurso,
            aporte=None,
            vigencia_inicio=date(2026, 1, 1),
            vigencia_fim=date(2026, 12, 31),
        )


def test_ausencia_de_custeio_e_recusada(
    sessao,
    criar_persona,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
):
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    trilha = criar_trilha(admin, situacao=SituacaoDaTrilha.publicada)
    tipo = criar_tipo_de_recurso(admin)
    ponto = criar_ponto_de_apoio(admin, criar_comunidade())

    with pytest.raises(ErroDeValidacao):
        propor_desafio_extra(
            sessao,
            operador=apoiador,
            trilha=trilha,
            missao=None,
            modalidade=Modalidade.aberto,
            nick_do_destinatario=None,
            justificativa_do_vinculo=None,
            tipo_de_recurso=tipo,
            ponto_de_apoio=ponto,
            quantidade_disponivel=5,
            criterio_de_atribuicao="Quem entregar primeiro.",
            pontos_extras=5,
            formato=FormatoDoDesafioExtra.presencial,
            custeio=None,
            aporte=None,
            vigencia_inicio=date(2026, 1, 1),
            vigencia_fim=date(2026, 12, 31),
        )


def test_teto_de_10_pontos_extras(
    sessao,
    criar_persona,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
):
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    trilha = criar_trilha(admin, situacao=SituacaoDaTrilha.publicada)
    tipo = criar_tipo_de_recurso(admin)
    ponto = criar_ponto_de_apoio(admin, criar_comunidade())

    with pytest.raises(ErroDeValidacao):
        _propor(sessao, apoiador=apoiador, trilha=trilha, tipo=tipo, ponto=ponto, pontos_extras=11)


def test_nao_ha_teto_de_propostas_simultaneas(
    sessao,
    criar_persona,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
):
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    trilha = criar_trilha(admin, situacao=SituacaoDaTrilha.publicada)
    tipo = criar_tipo_de_recurso(admin)
    ponto = criar_ponto_de_apoio(admin, criar_comunidade())

    primeiro = _propor(sessao, apoiador=apoiador, trilha=trilha, tipo=tipo, ponto=ponto)
    segundo = _propor(sessao, apoiador=apoiador, trilha=trilha, tipo=tipo, ponto=ponto)

    assert primeiro.id != segundo.id
    assert len(listar_desafios_do_proponente(sessao, proponente_id=apoiador.id)) == 2


# --- 2.3 — modalidade direcionada --------------------------------------------


def test_direcionado_sem_justificativa_e_recusado(
    sessao,
    criar_persona,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
):
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    trilha = criar_trilha(admin, situacao=SituacaoDaTrilha.publicada)
    tipo = criar_tipo_de_recurso(admin)
    ponto = criar_ponto_de_apoio(admin, criar_comunidade())

    with pytest.raises(ErroDeValidacao):
        _propor(
            sessao,
            apoiador=apoiador,
            trilha=trilha,
            tipo=tipo,
            ponto=ponto,
            modalidade=Modalidade.direcionado,
            nick_do_destinatario="guerreira-fantasma",
            justificativa_do_vinculo=None,
        )


def test_direcionado_com_nick_inexistente_e_aceito(
    sessao,
    criar_persona,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
):
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    trilha = criar_trilha(admin, situacao=SituacaoDaTrilha.publicada)
    tipo = criar_tipo_de_recurso(admin)
    ponto = criar_ponto_de_apoio(admin, criar_comunidade())

    desafio = _propor(
        sessao,
        apoiador=apoiador,
        trilha=trilha,
        tipo=tipo,
        ponto=ponto,
        modalidade=Modalidade.direcionado,
        nick_do_destinatario="nick-que-nao-existe",
        justificativa_do_vinculo="É minha vizinha.",
    )

    assert desafio.nick_do_destinatario == "nick-que-nao-existe"


# --- 2.4 — lastro provido e a guarda da publicação ---------------------------


def _com_saldo(sessao, criar_lancamento, autor, tipo, ponto, quantidade):
    criar_lancamento(
        autor, tipo, ponto, natureza=NaturezaDoLancamento.credito, quantidade=Decimal(quantidade)
    )


def test_lastro_provido_por_saldo_suficiente(
    sessao,
    criar_persona,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
    criar_lancamento,
):
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    trilha = criar_trilha(admin, situacao=SituacaoDaTrilha.publicada)
    tipo = criar_tipo_de_recurso(admin)
    ponto = criar_ponto_de_apoio(admin, criar_comunidade())
    _com_saldo(sessao, criar_lancamento, admin, tipo, ponto, "10")

    desafio = _propor(
        sessao, apoiador=apoiador, trilha=trilha, tipo=tipo, ponto=ponto, quantidade_disponivel=5
    )

    assert lastro_provido(sessao, desafio=desafio) is True


def test_lastro_nao_provido_por_saldo_insuficiente(
    sessao,
    criar_persona,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
):
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    trilha = criar_trilha(admin, situacao=SituacaoDaTrilha.publicada)
    tipo = criar_tipo_de_recurso(admin)
    ponto = criar_ponto_de_apoio(admin, criar_comunidade())

    desafio = _propor(
        sessao, apoiador=apoiador, trilha=trilha, tipo=tipo, ponto=ponto, quantidade_disponivel=5
    )

    assert lastro_provido(sessao, desafio=desafio) is False


def test_lastro_provido_por_aporte_homologado(
    sessao,
    criar_persona,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
    criar_lancamento,
    criar_aporte,
):
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    trilha = criar_trilha(admin, situacao=SituacaoDaTrilha.publicada)
    tipo = criar_tipo_de_recurso(admin)
    ponto = criar_ponto_de_apoio(admin, criar_comunidade())
    lancamento = criar_lancamento(admin, tipo, ponto, natureza=NaturezaDoLancamento.credito)
    aporte = criar_aporte(admin, apoiador, tipo, ponto, lancamento, admin_homologador=admin)

    desafio = _propor(
        sessao,
        apoiador=apoiador,
        trilha=trilha,
        tipo=tipo,
        ponto=ponto,
        custeio=CusteioDoDesafioExtra.aporte_do_proponente,
        aporte=aporte,
    )

    assert lastro_provido(sessao, desafio=desafio) is True


def test_lastro_nao_provido_por_aporte_de_outro_proponente(
    sessao,
    criar_persona,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
    criar_lancamento,
    criar_aporte,
):
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    outro_apoiador = criar_persona(Papel.apoiador)
    trilha = criar_trilha(admin, situacao=SituacaoDaTrilha.publicada)
    tipo = criar_tipo_de_recurso(admin)
    ponto = criar_ponto_de_apoio(admin, criar_comunidade())
    lancamento = criar_lancamento(admin, tipo, ponto, natureza=NaturezaDoLancamento.credito)
    criar_aporte(admin, outro_apoiador, tipo, ponto, lancamento, admin_homologador=admin)

    with pytest.raises(ErroDeValidacao):
        _propor(
            sessao,
            apoiador=apoiador,
            trilha=trilha,
            tipo=tipo,
            ponto=ponto,
            custeio=CusteioDoDesafioExtra.aporte_do_proponente,
            aporte=criar_aporte(
                admin, outro_apoiador, tipo, ponto, lancamento, admin_homologador=admin
            ),
        )


def test_publicacao_sem_lastro_provido_e_recusada(
    sessao,
    criar_persona,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
):
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    trilha = criar_trilha(admin, situacao=SituacaoDaTrilha.publicada)
    tipo = criar_tipo_de_recurso(admin)
    ponto = criar_ponto_de_apoio(admin, criar_comunidade())

    desafio = _propor(sessao, apoiador=apoiador, trilha=trilha, tipo=tipo, ponto=ponto)

    with pytest.raises(ErroDeValidacao):
        conferir_publicacao_com_lastro(sessao, desafio=desafio)


# --- 2.5 — imutabilidade do publicado -----------------------------------------


def test_alteracao_de_publicado_e_recusada_com_405(
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
    trilha = criar_trilha(admin, situacao=SituacaoDaTrilha.publicada)
    tipo = criar_tipo_de_recurso(admin)
    ponto = criar_ponto_de_apoio(admin, criar_comunidade())
    desafio = criar_desafio_extra(
        apoiador, trilha, tipo, ponto, situacao=SituacaoDoDesafioExtra.publicado
    )

    with pytest.raises(EdicaoDeDesafioExtraPublicadoRecusada):
        conferir_editavel(desafio)


def test_desafio_nao_publicado_e_editavel(
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
    trilha = criar_trilha(admin, situacao=SituacaoDaTrilha.publicada)
    tipo = criar_tipo_de_recurso(admin)
    ponto = criar_ponto_de_apoio(admin, criar_comunidade())
    desafio = criar_desafio_extra(
        apoiador, trilha, tipo, ponto, situacao=SituacaoDoDesafioExtra.em_aprovacao_do_admin
    )

    conferir_editavel(desafio)
