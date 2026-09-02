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
    aprovar_desafio_extra,
    conferir_editavel,
    conferir_publicacao_com_lastro,
    encerrar_desafio_extra,
    lastro_provido,
    listar_desafios_a_validar_do_mestre,
    listar_desafios_do_proponente,
    listar_desafios_em_aprovacao_do_admin,
    listar_desafios_publicados,
    propor_desafio_extra,
    recusar_desafio_extra,
    recusar_desafio_extra_pelo_mestre,
    validar_desafio_extra,
)
from nucleo.erros import (
    EdicaoDeDesafioExtraPublicadoRecusada,
    ErroDeValidacao,
    PermissaoNegada,
    SituacaoDoDesafioExtraIncompativel,
)
from nucleo.livro_razao.modelo import NaturezaDoLancamento
from nucleo.livro_razao.regra import saldo_de
from nucleo.personas.modelo import Papel
from nucleo.recursos.modelo import NaturezaDoRecurso
from nucleo.reservas.modelo import EstadoDaReserva, Reserva
from nucleo.reservas.regra import disponivel_de
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


# --- 2.1, 2.3, 2.4, 2.5 — o Mestre como proponente e como validador ----------


def test_mestre_autor_propoe_e_nasce_em_aprovacao_do_admin(
    sessao,
    criar_persona,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
):
    mestre_autor = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre_autor, situacao=SituacaoDaTrilha.publicada)
    tipo = criar_tipo_de_recurso(mestre_autor)
    ponto = criar_ponto_de_apoio(mestre_autor, criar_comunidade())

    desafio = _propor(sessao, apoiador=mestre_autor, trilha=trilha, tipo=tipo, ponto=ponto)

    assert desafio.autor_id == mestre_autor.id
    assert desafio.situacao == SituacaoDoDesafioExtra.em_aprovacao_do_admin
    assert desafio.mestre_validador_id is None


def test_outro_mestre_propoe_e_nasce_em_validacao_e_aparece_na_fila_do_autor(
    sessao,
    criar_persona,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
):
    mestre_autor = criar_persona(Papel.mestre)
    outro_mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre_autor, situacao=SituacaoDaTrilha.publicada)
    tipo = criar_tipo_de_recurso(mestre_autor)
    ponto = criar_ponto_de_apoio(mestre_autor, criar_comunidade())

    desafio = _propor(sessao, apoiador=outro_mestre, trilha=trilha, tipo=tipo, ponto=ponto)

    assert desafio.situacao == SituacaoDoDesafioExtra.em_validacao_do_mestre
    fila = listar_desafios_a_validar_do_mestre(sessao, operador=mestre_autor)
    assert [d.id for d in fila] == [desafio.id]
    assert listar_desafios_a_validar_do_mestre(sessao, operador=outro_mestre) == []


def test_direcionado_do_mestre_sem_justificativa_e_recusado(
    sessao,
    criar_persona,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
):
    mestre_autor = criar_persona(Papel.mestre)
    outro_mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre_autor, situacao=SituacaoDaTrilha.publicada)
    tipo = criar_tipo_de_recurso(mestre_autor)
    ponto = criar_ponto_de_apoio(mestre_autor, criar_comunidade())

    with pytest.raises(ErroDeValidacao):
        _propor(
            sessao,
            apoiador=outro_mestre,
            trilha=trilha,
            tipo=tipo,
            ponto=ponto,
            modalidade=Modalidade.direcionado,
            nick_do_destinatario="guerreiro-qualquer",
            justificativa_do_vinculo=None,
        )


def test_direcionado_do_mestre_com_nick_inexistente_e_aceito(
    sessao,
    criar_persona,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
):
    mestre_autor = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre_autor, situacao=SituacaoDaTrilha.publicada)
    tipo = criar_tipo_de_recurso(mestre_autor)
    ponto = criar_ponto_de_apoio(mestre_autor, criar_comunidade())

    desafio = _propor(
        sessao,
        apoiador=mestre_autor,
        trilha=trilha,
        tipo=tipo,
        ponto=ponto,
        modalidade=Modalidade.direcionado,
        nick_do_destinatario="nick-que-nao-existe",
        justificativa_do_vinculo="Aluno com dificuldade em matemática.",
    )

    assert desafio.nick_do_destinatario == "nick-que-nao-existe"


def test_validacao_com_parecer_leva_o_desafio_ao_admin(
    sessao,
    criar_persona,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
    criar_desafio_extra,
):
    mestre_autor = criar_persona(Papel.mestre)
    apoiador = criar_persona(Papel.apoiador)
    trilha = criar_trilha(mestre_autor, situacao=SituacaoDaTrilha.publicada)
    tipo = criar_tipo_de_recurso(mestre_autor)
    ponto = criar_ponto_de_apoio(mestre_autor, criar_comunidade())
    desafio = criar_desafio_extra(
        apoiador, trilha, tipo, ponto, situacao=SituacaoDoDesafioExtra.em_validacao_do_mestre
    )

    validado = validar_desafio_extra(
        sessao, operador=mestre_autor, desafio=desafio, parecer="Boa proposta pedagógica."
    )

    assert validado.situacao == SituacaoDoDesafioExtra.em_aprovacao_do_admin
    assert validado.parecer_do_mestre == "Boa proposta pedagógica."
    assert validado.mestre_validador_id == mestre_autor.id


def test_validacao_sem_parecer_nao_passa(
    sessao,
    criar_persona,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
    criar_desafio_extra,
):
    mestre_autor = criar_persona(Papel.mestre)
    apoiador = criar_persona(Papel.apoiador)
    trilha = criar_trilha(mestre_autor, situacao=SituacaoDaTrilha.publicada)
    tipo = criar_tipo_de_recurso(mestre_autor)
    ponto = criar_ponto_de_apoio(mestre_autor, criar_comunidade())
    desafio = criar_desafio_extra(
        apoiador, trilha, tipo, ponto, situacao=SituacaoDoDesafioExtra.em_validacao_do_mestre
    )

    with pytest.raises(ErroDeValidacao):
        validar_desafio_extra(sessao, operador=mestre_autor, desafio=desafio, parecer=None)
    assert desafio.situacao == SituacaoDoDesafioExtra.em_validacao_do_mestre


def test_mestre_de_outra_trilha_nao_valida(
    sessao,
    criar_persona,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
    criar_desafio_extra,
):
    mestre_autor = criar_persona(Papel.mestre)
    outro_mestre = criar_persona(Papel.mestre)
    apoiador = criar_persona(Papel.apoiador)
    trilha = criar_trilha(mestre_autor, situacao=SituacaoDaTrilha.publicada)
    tipo = criar_tipo_de_recurso(mestre_autor)
    ponto = criar_ponto_de_apoio(mestre_autor, criar_comunidade())
    desafio = criar_desafio_extra(
        apoiador, trilha, tipo, ponto, situacao=SituacaoDoDesafioExtra.em_validacao_do_mestre
    )

    with pytest.raises(PermissaoNegada):
        validar_desafio_extra(sessao, operador=outro_mestre, desafio=desafio, parecer="Ok.")
    assert desafio.situacao == SituacaoDoDesafioExtra.em_validacao_do_mestre


def test_validacao_de_desafio_em_outra_situacao_da_409(
    sessao,
    criar_persona,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
    criar_desafio_extra,
):
    mestre_autor = criar_persona(Papel.mestre)
    apoiador = criar_persona(Papel.apoiador)
    trilha = criar_trilha(mestre_autor, situacao=SituacaoDaTrilha.publicada)
    tipo = criar_tipo_de_recurso(mestre_autor)
    ponto = criar_ponto_de_apoio(mestre_autor, criar_comunidade())
    desafio = criar_desafio_extra(
        apoiador, trilha, tipo, ponto, situacao=SituacaoDoDesafioExtra.em_aprovacao_do_admin
    )

    with pytest.raises(SituacaoDoDesafioExtraIncompativel):
        validar_desafio_extra(sessao, operador=mestre_autor, desafio=desafio, parecer="Ok.")


def test_recusa_do_mestre_sem_motivo_nao_passa(
    sessao,
    criar_persona,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
    criar_desafio_extra,
):
    mestre_autor = criar_persona(Papel.mestre)
    apoiador = criar_persona(Papel.apoiador)
    trilha = criar_trilha(mestre_autor, situacao=SituacaoDaTrilha.publicada)
    tipo = criar_tipo_de_recurso(mestre_autor)
    ponto = criar_ponto_de_apoio(mestre_autor, criar_comunidade())
    desafio = criar_desafio_extra(
        apoiador, trilha, tipo, ponto, situacao=SituacaoDoDesafioExtra.em_validacao_do_mestre
    )

    with pytest.raises(ErroDeValidacao):
        recusar_desafio_extra_pelo_mestre(
            sessao, operador=mestre_autor, desafio=desafio, motivo=None
        )
    assert desafio.situacao == SituacaoDoDesafioExtra.em_validacao_do_mestre


def test_recusa_do_mestre_grava_o_motivo_e_nao_chega_a_fila_do_admin(
    sessao,
    criar_persona,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
    criar_desafio_extra,
):
    mestre_autor = criar_persona(Papel.mestre)
    apoiador = criar_persona(Papel.apoiador)
    trilha = criar_trilha(mestre_autor, situacao=SituacaoDaTrilha.publicada)
    tipo = criar_tipo_de_recurso(mestre_autor)
    ponto = criar_ponto_de_apoio(mestre_autor, criar_comunidade())
    desafio = criar_desafio_extra(
        apoiador, trilha, tipo, ponto, situacao=SituacaoDoDesafioExtra.em_validacao_do_mestre
    )

    recusado = recusar_desafio_extra_pelo_mestre(
        sessao, operador=mestre_autor, desafio=desafio, motivo="Sem mérito pedagógico."
    )

    assert recusado.situacao == SituacaoDoDesafioExtra.recusado
    assert recusado.motivo_da_recusa == "Sem mérito pedagógico."
    assert recusado.mestre_validador_id == mestre_autor.id
    assert listar_desafios_em_aprovacao_do_admin(sessao) == []
    assert sessao.query(Reserva).filter_by(desafio_extra_id=desafio.id).count() == 0


def test_fila_do_mestre_so_traz_as_proprias_trilhas(
    sessao,
    criar_persona,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
    criar_desafio_extra,
):
    mestre_autor = criar_persona(Papel.mestre)
    outro_mestre = criar_persona(Papel.mestre)
    apoiador = criar_persona(Papel.apoiador)
    trilha_do_autor = criar_trilha(mestre_autor, situacao=SituacaoDaTrilha.publicada)
    trilha_do_outro = criar_trilha(outro_mestre, situacao=SituacaoDaTrilha.publicada)
    tipo = criar_tipo_de_recurso(mestre_autor)
    ponto = criar_ponto_de_apoio(mestre_autor, criar_comunidade())
    esperado = criar_desafio_extra(
        apoiador,
        trilha_do_autor,
        tipo,
        ponto,
        situacao=SituacaoDoDesafioExtra.em_validacao_do_mestre,
    )
    criar_desafio_extra(
        apoiador,
        trilha_do_outro,
        tipo,
        ponto,
        situacao=SituacaoDoDesafioExtra.em_validacao_do_mestre,
    )
    criar_desafio_extra(
        apoiador,
        trilha_do_autor,
        tipo,
        ponto,
        situacao=SituacaoDoDesafioExtra.em_aprovacao_do_admin,
    )

    fila = listar_desafios_a_validar_do_mestre(sessao, operador=mestre_autor)

    assert [d.id for d in fila] == [esperado.id]


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


# --- 4.1 e 4.2 — fila, aprovação, recusa, reserva e encerramento --------------


def test_desafio_em_validacao_do_mestre_nao_aparece_na_fila_e_aprovacao_da_409(
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
        apoiador, trilha, tipo, ponto, situacao=SituacaoDoDesafioExtra.em_validacao_do_mestre
    )

    assert listar_desafios_em_aprovacao_do_admin(sessao) == []

    with pytest.raises(SituacaoDoDesafioExtraIncompativel):
        aprovar_desafio_extra(sessao, desafio, admin=admin)


def test_aprovacao_sem_lastro_e_recusada_e_desafio_segue_na_fila(
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

    with pytest.raises(ErroDeValidacao):
        aprovar_desafio_extra(sessao, desafio, admin=admin)

    assert desafio.situacao == SituacaoDoDesafioExtra.em_aprovacao_do_admin
    assert [d.id for d in listar_desafios_em_aprovacao_do_admin(sessao)] == [desafio.id]


def test_aprovacao_com_lastro_publica_e_grava_o_aprovador(
    sessao,
    criar_persona,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
    criar_desafio_extra,
    criar_lancamento,
):
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    trilha = criar_trilha(admin, situacao=SituacaoDaTrilha.publicada)
    tipo = criar_tipo_de_recurso(admin)
    ponto = criar_ponto_de_apoio(admin, criar_comunidade())
    criar_lancamento(
        admin, tipo, ponto, natureza=NaturezaDoLancamento.credito, quantidade=Decimal("5")
    )
    desafio = criar_desafio_extra(
        apoiador,
        trilha,
        tipo,
        ponto,
        situacao=SituacaoDoDesafioExtra.em_aprovacao_do_admin,
        quantidade_disponivel=5,
    )

    aprovado = aprovar_desafio_extra(sessao, desafio, admin=admin)

    assert aprovado.situacao == SituacaoDoDesafioExtra.publicado
    assert aprovado.admin_aprovador_id == admin.id
    assert listar_desafios_em_aprovacao_do_admin(sessao) == []
    assert [d.id for d in listar_desafios_publicados(sessao)] == [desafio.id]


def test_recusa_sem_motivo_e_recusada(
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

    with pytest.raises(ErroDeValidacao):
        recusar_desafio_extra(sessao, desafio, admin=admin, motivo=None)
    with pytest.raises(ErroDeValidacao):
        recusar_desafio_extra(sessao, desafio, admin=admin, motivo="   ")


def test_recusa_grava_o_motivo_e_nao_deixa_reserva(
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

    recusado = recusar_desafio_extra(sessao, desafio, admin=admin, motivo="Sem mérito pedagógico.")

    assert recusado.situacao == SituacaoDoDesafioExtra.recusado
    assert recusado.motivo_da_recusa == "Sem mérito pedagógico."
    assert sessao.query(Reserva).filter_by(desafio_extra_id=desafio.id).count() == 0


def test_publicacao_grava_a_reserva_e_reduz_a_disponivel_sem_mexer_no_saldo(
    sessao,
    criar_persona,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
    criar_desafio_extra,
    criar_lancamento,
):
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    trilha = criar_trilha(admin, situacao=SituacaoDaTrilha.publicada)
    tipo = criar_tipo_de_recurso(admin)
    ponto = criar_ponto_de_apoio(admin, criar_comunidade())
    criar_lancamento(
        admin, tipo, ponto, natureza=NaturezaDoLancamento.credito, quantidade=Decimal("10")
    )
    desafio = criar_desafio_extra(
        apoiador,
        trilha,
        tipo,
        ponto,
        situacao=SituacaoDoDesafioExtra.em_aprovacao_do_admin,
        quantidade_disponivel=4,
    )

    aprovar_desafio_extra(sessao, desafio, admin=admin)
    sessao.commit()

    saldo = saldo_de(sessao, tipo_de_recurso_id=tipo.id, ponto_de_apoio_id=ponto.id)
    disponivel = disponivel_de(sessao, tipo_de_recurso_id=tipo.id, ponto_de_apoio_id=ponto.id)
    reserva = sessao.query(Reserva).filter_by(desafio_extra_id=desafio.id).one()
    assert saldo == Decimal("10.00")
    assert disponivel == Decimal("6.00")
    assert reserva.quantidade == Decimal("4.00")
    assert reserva.estado == EstadoDaReserva.reservada
    assert reserva.aula_id is None


def test_recompensa_que_nao_cabe_na_disponivel_e_recusada_sem_publicar(
    sessao,
    criar_persona,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
    criar_desafio_extra,
    criar_lancamento,
):
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    trilha = criar_trilha(admin, situacao=SituacaoDaTrilha.publicada)
    tipo = criar_tipo_de_recurso(admin)
    ponto = criar_ponto_de_apoio(admin, criar_comunidade())
    criar_lancamento(
        admin, tipo, ponto, natureza=NaturezaDoLancamento.credito, quantidade=Decimal("2")
    )
    desafio = criar_desafio_extra(
        apoiador,
        trilha,
        tipo,
        ponto,
        situacao=SituacaoDoDesafioExtra.em_aprovacao_do_admin,
        quantidade_disponivel=5,
    )

    with pytest.raises(ErroDeValidacao):
        aprovar_desafio_extra(sessao, desafio, admin=admin)

    assert desafio.situacao == SituacaoDoDesafioExtra.em_aprovacao_do_admin
    assert sessao.query(Reserva).filter_by(desafio_extra_id=desafio.id).count() == 0


def test_recompensa_de_tipo_duravel_e_recusada(
    sessao,
    criar_persona,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
    criar_desafio_extra,
    criar_lancamento,
):
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    trilha = criar_trilha(admin, situacao=SituacaoDaTrilha.publicada)
    tipo = criar_tipo_de_recurso(admin, natureza=NaturezaDoRecurso.duravel)
    ponto = criar_ponto_de_apoio(admin, criar_comunidade())
    desafio = criar_desafio_extra(
        apoiador,
        trilha,
        tipo,
        ponto,
        situacao=SituacaoDoDesafioExtra.em_aprovacao_do_admin,
        custeio=CusteioDoDesafioExtra.aporte_do_proponente,
    )

    with pytest.raises(ErroDeValidacao):
        aprovar_desafio_extra(sessao, desafio, admin=admin)

    assert sessao.query(Reserva).filter_by(desafio_extra_id=desafio.id).count() == 0


def test_encerramento_libera_a_reserva_e_devolve_a_disponivel(
    sessao,
    criar_persona,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
    criar_desafio_extra,
    criar_lancamento,
):
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    trilha = criar_trilha(admin, situacao=SituacaoDaTrilha.publicada)
    tipo = criar_tipo_de_recurso(admin)
    ponto = criar_ponto_de_apoio(admin, criar_comunidade())
    criar_lancamento(
        admin, tipo, ponto, natureza=NaturezaDoLancamento.credito, quantidade=Decimal("5")
    )
    desafio = criar_desafio_extra(
        apoiador,
        trilha,
        tipo,
        ponto,
        situacao=SituacaoDoDesafioExtra.em_aprovacao_do_admin,
        quantidade_disponivel=5,
    )
    aprovar_desafio_extra(sessao, desafio, admin=admin)
    sessao.commit()

    encerrado = encerrar_desafio_extra(sessao, desafio, admin=admin)
    sessao.commit()

    assert encerrado.admin_encerrador_id == admin.id
    assert encerrado.encerrado_em is not None
    reserva = sessao.query(Reserva).filter_by(desafio_extra_id=desafio.id).one()
    assert reserva.estado == EstadoDaReserva.liberada
    disponivel = disponivel_de(sessao, tipo_de_recurso_id=tipo.id, ponto_de_apoio_id=ponto.id)
    assert disponivel == Decimal("5.00")
    # O encerramento não é um quinto estado: o desafio segue `publicado`,
    # com `encerrado_em` como o fato gravado (design — decisão 1).
    assert [d.id for d in listar_desafios_publicados(sessao)] == [desafio.id]


def test_encerrar_fora_de_publicado_ou_duas_vezes_da_409(
    sessao,
    criar_persona,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
    criar_desafio_extra,
    criar_lancamento,
):
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    trilha = criar_trilha(admin, situacao=SituacaoDaTrilha.publicada)
    tipo = criar_tipo_de_recurso(admin)
    ponto = criar_ponto_de_apoio(admin, criar_comunidade())
    desafio_nao_publicado = criar_desafio_extra(
        apoiador, trilha, tipo, ponto, situacao=SituacaoDoDesafioExtra.em_aprovacao_do_admin
    )

    with pytest.raises(SituacaoDoDesafioExtraIncompativel):
        encerrar_desafio_extra(sessao, desafio_nao_publicado, admin=admin)

    criar_lancamento(
        admin, tipo, ponto, natureza=NaturezaDoLancamento.credito, quantidade=Decimal("5")
    )
    desafio_publicado = criar_desafio_extra(
        apoiador,
        trilha,
        tipo,
        ponto,
        situacao=SituacaoDoDesafioExtra.em_aprovacao_do_admin,
        quantidade_disponivel=5,
    )
    aprovar_desafio_extra(sessao, desafio_publicado, admin=admin)
    sessao.commit()
    encerrar_desafio_extra(sessao, desafio_publicado, admin=admin)
    sessao.commit()

    with pytest.raises(SituacaoDoDesafioExtraIncompativel):
        encerrar_desafio_extra(sessao, desafio_publicado, admin=admin)


def test_vigencia_vencida_sem_encerramento_mantem_a_reserva(
    sessao,
    criar_persona,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
    criar_desafio_extra,
    criar_lancamento,
):
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    trilha = criar_trilha(admin, situacao=SituacaoDaTrilha.publicada)
    tipo = criar_tipo_de_recurso(admin)
    ponto = criar_ponto_de_apoio(admin, criar_comunidade())
    criar_lancamento(
        admin, tipo, ponto, natureza=NaturezaDoLancamento.credito, quantidade=Decimal("5")
    )
    desafio = criar_desafio_extra(
        apoiador,
        trilha,
        tipo,
        ponto,
        situacao=SituacaoDoDesafioExtra.em_aprovacao_do_admin,
        quantidade_disponivel=5,
        vigencia_inicio=date(2020, 1, 1),
        vigencia_fim=date(2020, 1, 31),
    )
    aprovar_desafio_extra(sessao, desafio, admin=admin)
    sessao.commit()

    # Vigência vencida há muito, sem que ato algum de encerramento tenha
    # acontecido: nada no núcleo observa o relógio (`RF-07-09`, PRD-07 §5.3).
    reserva = sessao.query(Reserva).filter_by(desafio_extra_id=desafio.id).one()
    assert reserva.estado == EstadoDaReserva.reservada
    disponivel = disponivel_de(sessao, tipo_de_recurso_id=tipo.id, ponto_de_apoio_id=ponto.id)
    assert disponivel == Decimal("0.00")
