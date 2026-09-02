from datetime import UTC, datetime

import pytest
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError

from nucleo.desafios_extras.modelo import ConclusaoDeDesafioExtra, SituacaoDoDesafioExtra
from nucleo.desafios_extras.regra import quantidade_restante, registrar_conclusao_de_desafio_extra
from nucleo.erros import ConclusaoDeDesafioExtraImutavel, ErroDeValidacao
from nucleo.personas.modelo import Papel

MOMENTO = datetime(2026, 6, 1, 12, 0, tzinfo=UTC)


def _registrar(sessao, *, desafio, guerreiro, recompensa_entregue=True, pontos_extras=5):
    return registrar_conclusao_de_desafio_extra(
        sessao,
        desafio=desafio,
        guerreiro_id=guerreiro.id,
        momento_do_fato=MOMENTO,
        recompensa_entregue=recompensa_entregue,
        pontos_extras_creditados=pontos_extras,
    )


def test_conclusao_guarda_quem_quando_e_quanto_rendeu(
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

    conclusao = _registrar(sessao, desafio=desafio, guerreiro=guerreiro, pontos_extras=7)

    assert conclusao.desafio_id == desafio.id
    assert conclusao.guerreiro_id == guerreiro.id
    assert conclusao.momento_do_fato == MOMENTO
    assert conclusao.recompensa_entregue is True
    assert conclusao.pontos_extras_creditados == 7


def test_segunda_conclusao_do_mesmo_guerreiro_e_recusada(
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
    _registrar(sessao, desafio=desafio, guerreiro=guerreiro)

    with pytest.raises(ErroDeValidacao):
        _registrar(sessao, desafio=desafio, guerreiro=guerreiro)


def test_conclusao_de_desafio_nao_publicado_e_recusada(
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
        apoiador, trilha, tipo, ponto, situacao=SituacaoDoDesafioExtra.em_aprovacao_do_admin
    )

    with pytest.raises(ErroDeValidacao):
        _registrar(sessao, desafio=desafio, guerreiro=guerreiro)


def test_conclusao_gravada_nao_e_editada_nem_apagada_no_orm(
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
    conclusao = _registrar(sessao, desafio=desafio, guerreiro=guerreiro)
    sessao.commit()

    conclusao.pontos_extras_creditados = 99
    with pytest.raises(ConclusaoDeDesafioExtraImutavel):
        sessao.commit()
    sessao.rollback()

    intacta = sessao.get(ConclusaoDeDesafioExtra, conclusao.id)
    assert intacta.pontos_extras_creditados == 5

    sessao.delete(intacta)
    with pytest.raises(ConclusaoDeDesafioExtraImutavel):
        sessao.commit()
    sessao.rollback()

    assert sessao.get(ConclusaoDeDesafioExtra, conclusao.id) is not None


def test_update_e_delete_em_conclusao_sao_recusados_direto_no_banco(
    conexao,
    sessao,
    criar_persona,
    criar_trilha,
    criar_tipo_de_recurso,
    criar_ponto_de_apoio,
    criar_comunidade,
    criar_desafio_extra,
):
    """Fora do ORM — direto no banco — o gatilho da migração recusa também
    (design — decisão 2)."""
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(admin)
    tipo = criar_tipo_de_recurso(admin)
    ponto = criar_ponto_de_apoio(admin, criar_comunidade())
    desafio = criar_desafio_extra(
        apoiador, trilha, tipo, ponto, situacao=SituacaoDoDesafioExtra.publicado
    )
    conclusao = _registrar(sessao, desafio=desafio, guerreiro=guerreiro)
    sessao.commit()

    with pytest.raises(DBAPIError), conexao.begin_nested():
        conexao.execute(
            text(
                "UPDATE conclusao_de_desafio_extra SET pontos_extras_creditados = 99 WHERE id = :id"
            ),
            {"id": str(conclusao.id)},
        )

    with pytest.raises(DBAPIError), conexao.begin_nested():
        conexao.execute(
            text("DELETE FROM conclusao_de_desafio_extra WHERE id = :id"),
            {"id": str(conclusao.id)},
        )

    ainda_existe = sessao.get(ConclusaoDeDesafioExtra, conclusao.id)
    assert ainda_existe is not None
    assert ainda_existe.pontos_extras_creditados == 5


def test_quantidade_restante_descontada_e_nunca_negativa(
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
    terceiro_guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(admin)
    tipo = criar_tipo_de_recurso(admin)
    ponto = criar_ponto_de_apoio(admin, criar_comunidade())
    desafio = criar_desafio_extra(
        apoiador,
        trilha,
        tipo,
        ponto,
        situacao=SituacaoDoDesafioExtra.publicado,
        quantidade_disponivel=2,
    )

    assert quantidade_restante(sessao, desafio=desafio) == 2

    _registrar(sessao, desafio=desafio, guerreiro=primeiro_guerreiro, recompensa_entregue=True)
    assert quantidade_restante(sessao, desafio=desafio) == 1

    # Conclusão sem recompensa entregue não desconta (`RF-14-37`).
    _registrar(sessao, desafio=desafio, guerreiro=segundo_guerreiro, recompensa_entregue=False)
    assert quantidade_restante(sessao, desafio=desafio) == 1

    _registrar(sessao, desafio=desafio, guerreiro=terceiro_guerreiro, recompensa_entregue=True)
    assert quantidade_restante(sessao, desafio=desafio) == 0
