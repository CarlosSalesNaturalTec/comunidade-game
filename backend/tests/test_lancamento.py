from decimal import Decimal

import pytest
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError

from nucleo.erros import ErroDeValidacao, LancamentoImutavel, PermissaoNegada
from nucleo.livro_razao.modelo import Lancamento, NaturezaDoLancamento
from nucleo.livro_razao.regra import lancar_ajuste, lancar_credito, saldo_de
from nucleo.personas.modelo import Papel


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
