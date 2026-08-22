from decimal import Decimal

import pytest
from sqlalchemy import func, text
from sqlalchemy.exc import DBAPIError

from nucleo.erros import ErroDeValidacao, LancamentoImutavel, PermissaoNegada
from nucleo.livro_razao.modelo import Lancamento, NaturezaDoLancamento
from nucleo.livro_razao.regra import (
    lancar_ajuste,
    lancar_credito,
    lancar_debito,
    saldo_de,
    transferir_saldo,
)
from nucleo.personas.modelo import Papel
from nucleo.pontos_de_apoio.regra import desativar_ponto_de_apoio
from nucleo.trocas.regra import registrar_troca


def test_lancamento_de_credito_nasce_com_autoria_e_momento(
    sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio, criar_tipo_de_recurso
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)

    lancamento = lancar_credito(
        sessao,
        tipo_de_recurso_id=tipo.id,
        ponto_de_apoio_id=ponto_de_apoio.id,
        quantidade=Decimal("3.00"),
        valor_em_moedas=Decimal("1.50"),
        operador=admin,
    )
    sessao.commit()

    assert lancamento.natureza == NaturezaDoLancamento.credito
    assert lancamento.autor_id == admin.id
    assert lancamento.papel_do_autor == Papel.admin.value
    assert lancamento.registrado_em is not None


def test_saldo_soma_os_lancamentos_do_par_tipo_e_ponto_de_apoio(
    sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio, criar_tipo_de_recurso
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)

    lancar_credito(
        sessao,
        tipo_de_recurso_id=tipo.id,
        ponto_de_apoio_id=ponto_de_apoio.id,
        quantidade=Decimal("3.00"),
        valor_em_moedas=Decimal("1.50"),
        operador=admin,
    )
    lancar_credito(
        sessao,
        tipo_de_recurso_id=tipo.id,
        ponto_de_apoio_id=ponto_de_apoio.id,
        quantidade=Decimal("2.00"),
        valor_em_moedas=Decimal("1.00"),
        operador=admin,
    )
    sessao.commit()

    saldo = saldo_de(sessao, tipo_de_recurso_id=tipo.id, ponto_de_apoio_id=ponto_de_apoio.id)

    assert saldo == Decimal("5.00")


def test_ponto_de_apoio_nao_empresta_saldo_a_outro(
    sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio, criar_tipo_de_recurso
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_a = criar_ponto_de_apoio(admin, comunidade, nome="Ponto A")
    ponto_b = criar_ponto_de_apoio(admin, comunidade, nome="Ponto B")
    tipo = criar_tipo_de_recurso(admin)

    lancar_credito(
        sessao,
        tipo_de_recurso_id=tipo.id,
        ponto_de_apoio_id=ponto_a.id,
        quantidade=Decimal("4.00"),
        valor_em_moedas=Decimal("4.00"),
        operador=admin,
    )
    sessao.commit()

    assert saldo_de(sessao, tipo_de_recurso_id=tipo.id, ponto_de_apoio_id=ponto_a.id) == Decimal(
        "4.00"
    )
    assert saldo_de(sessao, tipo_de_recurso_id=tipo.id, ponto_de_apoio_id=ponto_b.id) == Decimal(
        "0"
    )


def test_recontagem_devolve_o_mesmo_saldo(
    sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio, criar_tipo_de_recurso
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)

    lancar_credito(
        sessao,
        tipo_de_recurso_id=tipo.id,
        ponto_de_apoio_id=ponto_de_apoio.id,
        quantidade=Decimal("7.00"),
        valor_em_moedas=Decimal("7.00"),
        operador=admin,
    )
    sessao.commit()

    primeira_leitura = saldo_de(
        sessao, tipo_de_recurso_id=tipo.id, ponto_de_apoio_id=ponto_de_apoio.id
    )
    segunda_leitura = saldo_de(
        sessao, tipo_de_recurso_id=tipo.id, ponto_de_apoio_id=ponto_de_apoio.id
    )

    assert primeira_leitura == segunda_leitura == Decimal("7.00")


def test_ajuste_entra_na_conta_do_saldo(
    sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio, criar_tipo_de_recurso
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)

    credito = lancar_credito(
        sessao,
        tipo_de_recurso_id=tipo.id,
        ponto_de_apoio_id=ponto_de_apoio.id,
        quantidade=Decimal("3.00"),
        valor_em_moedas=Decimal("3.00"),
        operador=admin,
    )
    sessao.commit()

    lancar_ajuste(
        sessao,
        operador=admin,
        lancamento_original=credito,
        quantidade=Decimal("-1.00"),
        valor_em_moedas=Decimal("-1.00"),
        motivo="Corrige lançamento a maior.",
    )
    sessao.commit()

    saldo = saldo_de(sessao, tipo_de_recurso_id=tipo.id, ponto_de_apoio_id=ponto_de_apoio.id)

    assert saldo == Decimal("2.00")


def test_ajuste_referencia_o_original_sem_altera_lo(
    sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio, criar_tipo_de_recurso
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)

    credito = lancar_credito(
        sessao,
        tipo_de_recurso_id=tipo.id,
        ponto_de_apoio_id=ponto_de_apoio.id,
        quantidade=Decimal("3.00"),
        valor_em_moedas=Decimal("3.00"),
        operador=admin,
    )
    sessao.commit()

    ajuste = lancar_ajuste(
        sessao,
        operador=admin,
        lancamento_original=credito,
        quantidade=Decimal("-1.00"),
        valor_em_moedas=Decimal("-1.00"),
        motivo="Corrige lançamento a maior.",
    )
    sessao.commit()
    sessao.refresh(credito)

    assert ajuste.lancamento_original_id == credito.id
    assert ajuste.motivo_do_ajuste == "Corrige lançamento a maior."
    assert ajuste.autor_id == admin.id
    assert credito.quantidade == Decimal("3.00")


def test_ajuste_sem_motivo_e_recusado(
    sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio, criar_tipo_de_recurso
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)

    credito = lancar_credito(
        sessao,
        tipo_de_recurso_id=tipo.id,
        ponto_de_apoio_id=ponto_de_apoio.id,
        quantidade=Decimal("3.00"),
        valor_em_moedas=Decimal("3.00"),
        operador=admin,
    )
    sessao.commit()

    with pytest.raises(ErroDeValidacao) as excinfo:
        lancar_ajuste(
            sessao,
            operador=admin,
            lancamento_original=credito,
            quantidade=Decimal("-1.00"),
            valor_em_moedas=Decimal("-1.00"),
            motivo=None,
        )
    assert excinfo.value.campo == "motivo"


def test_ajuste_sobre_lancamento_inexistente_e_recusado(sessao, criar_persona):
    admin = criar_persona(Papel.admin)

    with pytest.raises(ErroDeValidacao) as excinfo:
        lancar_ajuste(
            sessao,
            operador=admin,
            lancamento_original=None,
            quantidade=Decimal("-1.00"),
            valor_em_moedas=Decimal("-1.00"),
            motivo="Corrige.",
        )
    assert excinfo.value.campo == "lancamento_original_id"


def test_mestre_nao_lanca_ajuste(
    sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio, criar_tipo_de_recurso
):
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)

    credito = lancar_credito(
        sessao,
        tipo_de_recurso_id=tipo.id,
        ponto_de_apoio_id=ponto_de_apoio.id,
        quantidade=Decimal("3.00"),
        valor_em_moedas=Decimal("3.00"),
        operador=admin,
    )
    sessao.commit()

    with pytest.raises(PermissaoNegada):
        lancar_ajuste(
            sessao,
            operador=mestre,
            lancamento_original=credito,
            quantidade=Decimal("-1.00"),
            valor_em_moedas=Decimal("-1.00"),
            motivo="Corrige.",
        )


def test_edicao_de_lancamento_e_recusada_pelo_orm(
    sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio, criar_tipo_de_recurso
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)

    lancamento = lancar_credito(
        sessao,
        tipo_de_recurso_id=tipo.id,
        ponto_de_apoio_id=ponto_de_apoio.id,
        quantidade=Decimal("3.00"),
        valor_em_moedas=Decimal("3.00"),
        operador=admin,
    )
    sessao.commit()

    lancamento.quantidade = Decimal("30.00")
    with pytest.raises(LancamentoImutavel):
        sessao.commit()
    sessao.rollback()

    intacto = sessao.get(Lancamento, lancamento.id)
    assert intacto.quantidade == Decimal("3.00")

    sessao.delete(intacto)
    with pytest.raises(LancamentoImutavel):
        sessao.commit()
    sessao.rollback()

    assert sessao.get(Lancamento, lancamento.id) is not None


def test_update_e_delete_em_lancamento_sao_recusados_direto_no_banco(
    conexao, sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio, criar_tipo_de_recurso
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)

    lancamento = lancar_credito(
        sessao,
        tipo_de_recurso_id=tipo.id,
        ponto_de_apoio_id=ponto_de_apoio.id,
        quantidade=Decimal("3.00"),
        valor_em_moedas=Decimal("3.00"),
        operador=admin,
    )
    sessao.commit()

    with pytest.raises(DBAPIError), conexao.begin_nested():
        conexao.execute(
            text("UPDATE lancamento SET quantidade = 30 WHERE id = :id"),
            {"id": str(lancamento.id)},
        )

    with pytest.raises(DBAPIError), conexao.begin_nested():
        conexao.execute(text("DELETE FROM lancamento WHERE id = :id"), {"id": str(lancamento.id)})

    ainda_existe = sessao.get(Lancamento, lancamento.id)
    assert ainda_existe is not None
    assert ainda_existe.quantidade == Decimal("3.00")


def test_a_baixa_grava_a_aula_no_debito(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_aula,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    aula = criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)

    debito = lancar_debito(
        sessao,
        tipo_de_recurso_id=tipo.id,
        ponto_de_apoio_id=ponto_de_apoio.id,
        quantidade=Decimal("2.00"),
        valor_em_moedas=Decimal("1.00"),
        operador=admin,
        aula_id=aula.id,
    )
    sessao.commit()

    assert debito.natureza == NaturezaDoLancamento.debito
    assert debito.aula_id == aula.id


def test_o_credito_do_aporte_nao_declara_aula(
    sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio, criar_tipo_de_recurso
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)

    credito = lancar_credito(
        sessao,
        tipo_de_recurso_id=tipo.id,
        ponto_de_apoio_id=ponto_de_apoio.id,
        quantidade=Decimal("3.00"),
        valor_em_moedas=Decimal("3.00"),
        operador=admin,
    )
    sessao.commit()

    assert credito.aula_id is None


def test_a_aula_do_lancamento_nao_muda_depois(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_aula,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    aula = criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)
    outra_aula = criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)

    debito = lancar_debito(
        sessao,
        tipo_de_recurso_id=tipo.id,
        ponto_de_apoio_id=ponto_de_apoio.id,
        quantidade=Decimal("2.00"),
        valor_em_moedas=Decimal("1.00"),
        operador=admin,
        aula_id=aula.id,
    )
    sessao.commit()

    debito.aula_id = outra_aula.id
    with pytest.raises(LancamentoImutavel):
        sessao.commit()
    sessao.rollback()

    intacto = sessao.get(Lancamento, debito.id)
    assert intacto.aula_id == aula.id


def test_o_consumo_da_aula_e_derivavel_do_ledger(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_aula,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo_a = criar_tipo_de_recurso(admin, nome="Lanche")
    tipo_b = criar_tipo_de_recurso(admin, nome="Material")
    aula = criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)

    lancar_debito(
        sessao,
        tipo_de_recurso_id=tipo_a.id,
        ponto_de_apoio_id=ponto_de_apoio.id,
        quantidade=Decimal("2.00"),
        valor_em_moedas=Decimal("1.00"),
        operador=admin,
        aula_id=aula.id,
    )
    lancar_debito(
        sessao,
        tipo_de_recurso_id=tipo_b.id,
        ponto_de_apoio_id=ponto_de_apoio.id,
        quantidade=Decimal("1.00"),
        valor_em_moedas=Decimal("0.50"),
        operador=admin,
        aula_id=aula.id,
    )
    sessao.commit()

    consumo = (
        sessao.query(func.coalesce(func.sum(Lancamento.valor_em_moedas), 0))
        .filter(Lancamento.aula_id == aula.id, Lancamento.natureza == NaturezaDoLancamento.debito)
        .scalar()
    )

    assert Decimal(consumo) == Decimal("1.50")


def _preparar_troca(
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_preco_de_referencia,
    criar_valor_de_referencia,
    criar_lancamento,
    criar_vinculo_jogador,
    criar_item_de_catalogo_avulso,
    criar_ponto_extra,
    criar_aula,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    criar_preco_de_referencia(admin, tipo, preco_em_pontos_extras=20)
    criar_valor_de_referencia(admin, tipo, valor_em_moedas=Decimal("1.00"))
    criar_lancamento(
        admin,
        tipo,
        ponto_de_apoio,
        natureza=NaturezaDoLancamento.credito,
        quantidade=Decimal("10.00"),
    )
    mestre = criar_persona(Papel.mestre)
    criar_vinculo_jogador(mestre, comunidade)
    item = criar_item_de_catalogo_avulso(
        admin, tipo, comunidade, ponto_de_apoio, estoque=Decimal("5"), ativo=True
    )
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    criar_ponto_extra(guerreiro, acumulado=100, saldo_disponivel=100)
    aula = criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)
    return admin, mestre, guerreiro, item, ponto_de_apoio, tipo, aula


def test_o_debito_da_troca_nao_declara_aula(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_preco_de_referencia,
    criar_valor_de_referencia,
    criar_lancamento,
    criar_vinculo_jogador,
    criar_item_de_catalogo_avulso,
    criar_ponto_extra,
    criar_aula,
):
    _, mestre, guerreiro, item, ponto_de_apoio, tipo, aula = _preparar_troca(
        criar_persona,
        criar_comunidade,
        criar_ponto_de_apoio,
        criar_tipo_de_recurso,
        criar_preco_de_referencia,
        criar_valor_de_referencia,
        criar_lancamento,
        criar_vinculo_jogador,
        criar_item_de_catalogo_avulso,
        criar_ponto_extra,
        criar_aula,
    )

    registrar_troca(sessao, operador=mestre, aula=aula, item=item, guerreiro=guerreiro)
    sessao.commit()

    debito = (
        sessao.query(Lancamento)
        .filter_by(natureza=NaturezaDoLancamento.debito, tipo_de_recurso_id=tipo.id)
        .order_by(Lancamento.registrado_em.desc())
        .first()
    )

    assert debito is not None
    assert debito.aula_id is None
    assert debito.ponto_de_apoio_id == ponto_de_apoio.id
    assert debito.quantidade == Decimal("1.00")


def test_a_troca_nao_entra_no_consumo_por_aula(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_preco_de_referencia,
    criar_valor_de_referencia,
    criar_lancamento,
    criar_vinculo_jogador,
    criar_item_de_catalogo_avulso,
    criar_ponto_extra,
    criar_aula,
):
    admin, mestre, guerreiro, item, ponto_de_apoio, tipo, aula = _preparar_troca(
        criar_persona,
        criar_comunidade,
        criar_ponto_de_apoio,
        criar_tipo_de_recurso,
        criar_preco_de_referencia,
        criar_valor_de_referencia,
        criar_lancamento,
        criar_vinculo_jogador,
        criar_item_de_catalogo_avulso,
        criar_ponto_extra,
        criar_aula,
    )

    lancar_debito(
        sessao,
        tipo_de_recurso_id=tipo.id,
        ponto_de_apoio_id=ponto_de_apoio.id,
        quantidade=Decimal("2.00"),
        valor_em_moedas=Decimal("2.00"),
        operador=admin,
        aula_id=aula.id,
    )
    registrar_troca(sessao, operador=mestre, aula=aula, item=item, guerreiro=guerreiro)
    sessao.commit()

    consumo = (
        sessao.query(func.coalesce(func.sum(Lancamento.valor_em_moedas), 0))
        .filter(Lancamento.aula_id == aula.id, Lancamento.natureza == NaturezaDoLancamento.debito)
        .scalar()
    )

    assert Decimal(consumo) == Decimal("2.00")


def _preparar_transferencia(
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_valor_de_referencia,
    sessao,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    origem = criar_ponto_de_apoio(admin, comunidade, nome="Origem")
    destino = criar_ponto_de_apoio(admin, comunidade, nome="Destino")
    tipo = criar_tipo_de_recurso(admin)
    criar_valor_de_referencia(admin, tipo, valor_em_moedas=Decimal("1.00"))
    lancar_credito(
        sessao,
        tipo_de_recurso_id=tipo.id,
        ponto_de_apoio_id=origem.id,
        quantidade=Decimal("10.00"),
        valor_em_moedas=Decimal("10.00"),
        operador=admin,
    )
    sessao.commit()
    return admin, comunidade, origem, destino, tipo


def test_transferencia_grava_debito_e_credito_com_mesmo_motivo_autoria_e_momento(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_valor_de_referencia,
):
    admin, _, origem, destino, tipo = _preparar_transferencia(
        criar_persona,
        criar_comunidade,
        criar_ponto_de_apoio,
        criar_tipo_de_recurso,
        criar_valor_de_referencia,
        sessao,
    )

    debito, credito = transferir_saldo(
        sessao,
        operador=admin,
        tipo_de_recurso=tipo,
        ponto_de_apoio_origem=origem,
        ponto_de_apoio_destino=destino,
        quantidade=Decimal("5.00"),
        motivo="Redistribuição de acervo.",
    )
    sessao.commit()

    assert debito.natureza == NaturezaDoLancamento.debito
    assert debito.ponto_de_apoio_id == origem.id
    assert credito.natureza == NaturezaDoLancamento.credito
    assert credito.ponto_de_apoio_id == destino.id
    for lancamento in (debito, credito):
        assert lancamento.tipo_de_recurso_id == tipo.id
        assert lancamento.quantidade == Decimal("5.00")
        assert lancamento.valor_em_moedas == Decimal("5.00")
        assert lancamento.autor_id == admin.id
        assert lancamento.papel_do_autor == Papel.admin.value
    assert debito.registrado_em == credito.registrado_em
    assert debito.lancamento_relacionado_id == credito.id
    assert credito.lancamento_relacionado_id == debito.id


def test_saldo_dos_dois_pontos_acompanha_a_transferencia(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_valor_de_referencia,
):
    admin, _, origem, destino, tipo = _preparar_transferencia(
        criar_persona,
        criar_comunidade,
        criar_ponto_de_apoio,
        criar_tipo_de_recurso,
        criar_valor_de_referencia,
        sessao,
    )
    lancar_credito(
        sessao,
        tipo_de_recurso_id=tipo.id,
        ponto_de_apoio_id=destino.id,
        quantidade=Decimal("2.00"),
        valor_em_moedas=Decimal("2.00"),
        operador=admin,
    )
    sessao.commit()

    transferir_saldo(
        sessao,
        operador=admin,
        tipo_de_recurso=tipo,
        ponto_de_apoio_origem=origem,
        ponto_de_apoio_destino=destino,
        quantidade=Decimal("4.00"),
        motivo="Redistribuição de acervo.",
    )
    sessao.commit()

    assert saldo_de(sessao, tipo_de_recurso_id=tipo.id, ponto_de_apoio_id=origem.id) == Decimal(
        "6.00"
    )
    assert saldo_de(sessao, tipo_de_recurso_id=tipo.id, ponto_de_apoio_id=destino.id) == Decimal(
        "6.00"
    )


def test_transferencia_de_mais_do_que_ha_e_recusada(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_valor_de_referencia,
):
    admin, _, origem, destino, tipo = _preparar_transferencia(
        criar_persona,
        criar_comunidade,
        criar_ponto_de_apoio,
        criar_tipo_de_recurso,
        criar_valor_de_referencia,
        sessao,
    )

    with pytest.raises(ErroDeValidacao) as excinfo:
        transferir_saldo(
            sessao,
            operador=admin,
            tipo_de_recurso=tipo,
            ponto_de_apoio_origem=origem,
            ponto_de_apoio_destino=destino,
            quantidade=Decimal("20.00"),
            motivo="Redistribuição de acervo.",
        )
    assert excinfo.value.campo == "quantidade"
    assert sessao.query(Lancamento).filter_by(ponto_de_apoio_id=destino.id).count() == 0


def test_transferencia_com_origem_igual_ao_destino_e_recusada(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_valor_de_referencia,
):
    admin, _, origem, _destino, tipo = _preparar_transferencia(
        criar_persona,
        criar_comunidade,
        criar_ponto_de_apoio,
        criar_tipo_de_recurso,
        criar_valor_de_referencia,
        sessao,
    )

    with pytest.raises(ErroDeValidacao) as excinfo:
        transferir_saldo(
            sessao,
            operador=admin,
            tipo_de_recurso=tipo,
            ponto_de_apoio_origem=origem,
            ponto_de_apoio_destino=origem,
            quantidade=Decimal("1.00"),
            motivo="Redistribuição de acervo.",
        )
    assert excinfo.value.campo == "ponto_de_apoio_destino_id"


def test_transferencia_para_destino_inativo_e_recusada(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_valor_de_referencia,
):
    admin, _, origem, destino, tipo = _preparar_transferencia(
        criar_persona,
        criar_comunidade,
        criar_ponto_de_apoio,
        criar_tipo_de_recurso,
        criar_valor_de_referencia,
        sessao,
    )
    desativar_ponto_de_apoio(sessao, destino, operador=admin, motivo="Fechou o espaço.")
    sessao.commit()

    with pytest.raises(ErroDeValidacao) as excinfo:
        transferir_saldo(
            sessao,
            operador=admin,
            tipo_de_recurso=tipo,
            ponto_de_apoio_origem=origem,
            ponto_de_apoio_destino=destino,
            quantidade=Decimal("1.00"),
            motivo="Redistribuição de acervo.",
        )
    assert excinfo.value.campo == "ponto_de_apoio_destino_id"


def test_mestre_nao_transfere(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_valor_de_referencia,
):
    admin, _, origem, destino, tipo = _preparar_transferencia(
        criar_persona,
        criar_comunidade,
        criar_ponto_de_apoio,
        criar_tipo_de_recurso,
        criar_valor_de_referencia,
        sessao,
    )
    mestre = criar_persona(Papel.mestre, criada_por=admin)

    with pytest.raises(PermissaoNegada):
        transferir_saldo(
            sessao,
            operador=mestre,
            tipo_de_recurso=tipo,
            ponto_de_apoio_origem=origem,
            ponto_de_apoio_destino=destino,
            quantidade=Decimal("1.00"),
            motivo="Redistribuição de acervo.",
        )
    assert sessao.query(Lancamento).filter_by(ponto_de_apoio_id=destino.id).count() == 0


def test_transferencia_nao_usa_ajuste(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_valor_de_referencia,
):
    admin, _, origem, destino, tipo = _preparar_transferencia(
        criar_persona,
        criar_comunidade,
        criar_ponto_de_apoio,
        criar_tipo_de_recurso,
        criar_valor_de_referencia,
        sessao,
    )

    debito, credito = transferir_saldo(
        sessao,
        operador=admin,
        tipo_de_recurso=tipo,
        ponto_de_apoio_origem=origem,
        ponto_de_apoio_destino=destino,
        quantidade=Decimal("1.00"),
        motivo="Redistribuição de acervo.",
    )
    sessao.commit()

    assert {debito.natureza, credito.natureza} == {
        NaturezaDoLancamento.debito,
        NaturezaDoLancamento.credito,
    }
    assert debito.natureza != NaturezaDoLancamento.ajuste
    assert credito.natureza != NaturezaDoLancamento.ajuste
    assert debito.lancamento_original_id is None
    assert credito.lancamento_original_id is None
