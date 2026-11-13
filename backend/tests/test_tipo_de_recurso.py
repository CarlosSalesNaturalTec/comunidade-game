from datetime import date
from decimal import Decimal

import pytest

from nucleo.erros import ErroDeValidacao, PermissaoNegada
from nucleo.personas.modelo import Papel
from nucleo.recursos.modelo import NaturezaDoRecurso, TipoDeRecurso, ValorDeReferencia
from nucleo.recursos.regra import (
    cadastrar_tipo_de_recurso,
    consultar_valor_de_referencia,
    listar_tipos_de_recurso,
    registrar_valor_de_referencia,
)


def test_admin_cadastra_tipo_de_recurso_com_autoria_gravada(sessao, criar_persona):
    admin = criar_persona(Papel.admin)

    tipo = cadastrar_tipo_de_recurso(
        sessao,
        operador=admin,
        nome="Lanche",
        natureza=NaturezaDoRecurso.consumivel.value,
        unidade="unidade",
    )
    sessao.commit()

    assert tipo.nome == "Lanche"
    assert tipo.natureza == NaturezaDoRecurso.consumivel
    assert tipo.unidade == "unidade"
    assert tipo.autor_id == admin.id
    assert tipo.papel_do_autor == Papel.admin.value


def test_tipo_nasce_sem_exigir_comprovante_quando_nao_declarado(sessao, criar_persona):
    admin = criar_persona(Papel.admin)

    tipo = cadastrar_tipo_de_recurso(
        sessao,
        operador=admin,
        nome="Lanche",
        natureza=NaturezaDoRecurso.consumivel.value,
        unidade="unidade",
    )
    sessao.commit()

    assert tipo.exige_comprovante is False


def test_tipo_cadastrado_exigindo_comprovante(sessao, criar_persona):
    admin = criar_persona(Papel.admin)

    tipo = cadastrar_tipo_de_recurso(
        sessao,
        operador=admin,
        nome="Cloud",
        natureza=NaturezaDoRecurso.financeiro.value,
        unidade="mês",
        exige_comprovante=True,
    )
    sessao.commit()

    assert tipo.exige_comprovante is True


def test_mestre_nao_cadastra_tipo_de_recurso(sessao, criar_persona):
    mestre = criar_persona(Papel.mestre)

    with pytest.raises(PermissaoNegada):
        cadastrar_tipo_de_recurso(
            sessao,
            operador=mestre,
            nome="Lanche",
            natureza=NaturezaDoRecurso.consumivel.value,
            unidade="unidade",
        )
    assert sessao.query(TipoDeRecurso).count() == 0


def test_mestre_le_o_catalogo_com_os_mesmos_campos_do_admin(
    sessao, criar_persona, criar_tipo_de_recurso
):
    admin = criar_persona(Papel.admin)
    tipo = criar_tipo_de_recurso(admin, exige_comprovante=True)
    mestre = criar_persona(Papel.mestre)

    tipos = listar_tipos_de_recurso(sessao, operador=mestre)

    assert tipos == [tipo]
    assert tipos[0].natureza == tipo.natureza
    assert tipos[0].exige_comprovante is True


def test_apoiador_nao_le_o_catalogo_de_tipos_de_recurso(sessao, criar_persona):
    apoiador = criar_persona(Papel.apoiador)

    with pytest.raises(PermissaoNegada):
        listar_tipos_de_recurso(sessao, operador=apoiador)


def test_tipo_de_recurso_sem_unidade_e_recusado(sessao, criar_persona):
    admin = criar_persona(Papel.admin)

    with pytest.raises(ErroDeValidacao) as excinfo:
        cadastrar_tipo_de_recurso(
            sessao,
            operador=admin,
            nome="Lanche",
            natureza=NaturezaDoRecurso.consumivel.value,
            unidade=None,
        )
    assert excinfo.value.campo == "unidade"
    assert sessao.query(TipoDeRecurso).count() == 0


def test_natureza_fora_das_quatro_previstas_e_recusada(sessao, criar_persona):
    admin = criar_persona(Papel.admin)

    with pytest.raises(ErroDeValidacao) as excinfo:
        cadastrar_tipo_de_recurso(
            sessao, operador=admin, nome="Lanche", natureza="voo_livre", unidade="unidade"
        )
    assert excinfo.value.campo == "natureza"
    assert sessao.query(TipoDeRecurso).count() == 0


def test_primeira_vigencia_nasce_sem_encerramento(sessao, criar_persona, criar_tipo_de_recurso):
    admin = criar_persona(Papel.admin)
    tipo = criar_tipo_de_recurso(admin)

    valor = registrar_valor_de_referencia(
        sessao,
        operador=admin,
        tipo=tipo,
        valor_em_moedas=Decimal("1.00"),
        vigencia_inicio=date(2026, 1, 1),
    )
    sessao.commit()

    assert valor.valor_em_moedas == Decimal("1.00")
    assert valor.vigencia_fim is None


def test_valor_novo_encerra_a_vigencia_anterior_sem_reescreve_la(
    sessao, criar_persona, criar_tipo_de_recurso
):
    admin = criar_persona(Papel.admin)
    tipo = criar_tipo_de_recurso(admin)

    primeiro = registrar_valor_de_referencia(
        sessao,
        operador=admin,
        tipo=tipo,
        valor_em_moedas=Decimal("1.00"),
        vigencia_inicio=date(2026, 1, 1),
    )
    sessao.commit()

    registrar_valor_de_referencia(
        sessao,
        operador=admin,
        tipo=tipo,
        valor_em_moedas=Decimal("2.00"),
        vigencia_inicio=date(2026, 6, 1),
    )
    sessao.commit()
    sessao.refresh(primeiro)

    assert primeiro.vigencia_fim == date(2026, 6, 1)
    assert primeiro.valor_em_moedas == Decimal("1.00")
    assert sessao.query(ValorDeReferencia).count() == 2


def test_consulta_dentro_da_vigencia_encerrada_devolve_o_valor_da_epoca(
    sessao, criar_persona, criar_tipo_de_recurso
):
    admin = criar_persona(Papel.admin)
    tipo = criar_tipo_de_recurso(admin)

    registrar_valor_de_referencia(
        sessao,
        operador=admin,
        tipo=tipo,
        valor_em_moedas=Decimal("1.00"),
        vigencia_inicio=date(2026, 1, 1),
    )
    registrar_valor_de_referencia(
        sessao,
        operador=admin,
        tipo=tipo,
        valor_em_moedas=Decimal("2.00"),
        vigencia_inicio=date(2026, 6, 1),
    )
    sessao.commit()

    valor = consultar_valor_de_referencia(sessao, tipo=tipo, data=date(2026, 3, 1))

    assert valor.valor_em_moedas == Decimal("1.00")


def test_consulta_no_dia_da_virada_devolve_o_valor_novo(
    sessao, criar_persona, criar_tipo_de_recurso
):
    admin = criar_persona(Papel.admin)
    tipo = criar_tipo_de_recurso(admin)

    registrar_valor_de_referencia(
        sessao,
        operador=admin,
        tipo=tipo,
        valor_em_moedas=Decimal("1.00"),
        vigencia_inicio=date(2026, 1, 1),
    )
    registrar_valor_de_referencia(
        sessao,
        operador=admin,
        tipo=tipo,
        valor_em_moedas=Decimal("2.00"),
        vigencia_inicio=date(2026, 6, 1),
    )
    sessao.commit()

    valor = consultar_valor_de_referencia(sessao, tipo=tipo, data=date(2026, 6, 1))

    assert valor.valor_em_moedas == Decimal("2.00")


def test_consulta_depois_da_ultima_abertura_devolve_o_valor_vigente(
    sessao, criar_persona, criar_tipo_de_recurso
):
    admin = criar_persona(Papel.admin)
    tipo = criar_tipo_de_recurso(admin)

    registrar_valor_de_referencia(
        sessao,
        operador=admin,
        tipo=tipo,
        valor_em_moedas=Decimal("1.00"),
        vigencia_inicio=date(2026, 1, 1),
    )
    registrar_valor_de_referencia(
        sessao,
        operador=admin,
        tipo=tipo,
        valor_em_moedas=Decimal("2.00"),
        vigencia_inicio=date(2026, 6, 1),
    )
    sessao.commit()

    valor = consultar_valor_de_referencia(sessao, tipo=tipo, data=date(2027, 1, 1))

    assert valor.valor_em_moedas == Decimal("2.00")


def test_duas_vigencias_abertas_no_mesmo_dia_a_consulta_devolve_a_registrada_por_ultimo(
    sessao, criar_persona, criar_tipo_de_recurso
):
    admin = criar_persona(Papel.admin)
    tipo = criar_tipo_de_recurso(admin)

    registrar_valor_de_referencia(
        sessao,
        operador=admin,
        tipo=tipo,
        valor_em_moedas=Decimal("1.00"),
        vigencia_inicio=date(2026, 1, 1),
    )
    sessao.commit()
    registrar_valor_de_referencia(
        sessao,
        operador=admin,
        tipo=tipo,
        valor_em_moedas=Decimal("3.00"),
        vigencia_inicio=date(2026, 1, 1),
    )
    sessao.commit()

    valor = consultar_valor_de_referencia(sessao, tipo=tipo, data=date(2026, 1, 1))

    assert valor.valor_em_moedas == Decimal("3.00")


def test_valor_negativo_e_recusado(sessao, criar_persona, criar_tipo_de_recurso):
    admin = criar_persona(Papel.admin)
    tipo = criar_tipo_de_recurso(admin)

    with pytest.raises(ErroDeValidacao) as excinfo:
        registrar_valor_de_referencia(
            sessao,
            operador=admin,
            tipo=tipo,
            valor_em_moedas=Decimal("-1.00"),
            vigencia_inicio=date(2026, 1, 1),
        )
    assert excinfo.value.campo == "valor_em_moedas"
    assert sessao.query(ValorDeReferencia).count() == 0


def test_valor_com_tres_casas_decimais_e_recusado(sessao, criar_persona, criar_tipo_de_recurso):
    admin = criar_persona(Papel.admin)
    tipo = criar_tipo_de_recurso(admin)

    with pytest.raises(ErroDeValidacao) as excinfo:
        registrar_valor_de_referencia(
            sessao,
            operador=admin,
            tipo=tipo,
            valor_em_moedas=Decimal("1.005"),
            vigencia_inicio=date(2026, 1, 1),
        )
    assert excinfo.value.campo == "valor_em_moedas"
    assert sessao.query(ValorDeReferencia).count() == 0


def test_mestre_nao_registra_valor_de_referencia(sessao, criar_persona, criar_tipo_de_recurso):
    admin = criar_persona(Papel.admin)
    tipo = criar_tipo_de_recurso(admin)
    mestre = criar_persona(Papel.mestre)

    with pytest.raises(PermissaoNegada):
        registrar_valor_de_referencia(
            sessao,
            operador=mestre,
            tipo=tipo,
            valor_em_moedas=Decimal("1.00"),
            vigencia_inicio=date(2026, 1, 1),
        )
    assert sessao.query(ValorDeReferencia).count() == 0


# --- Edição, desativação e exclusão (`RF-07-51`, `RF-07-52`, `RN-07-40`) ---

from nucleo.erros import TipoEmUso  # noqa: E402
from nucleo.recursos.modelo import PrecoDeReferencia  # noqa: E402
from nucleo.recursos.regra import (  # noqa: E402
    alterar_tipo_de_recurso,
    desativar_tipo_de_recurso,
    excluir_tipo_de_recurso,
    exigir_tipo_de_recurso_ativo,
    reativar_tipo_de_recurso,
)


def test_admin_altera_nome_unidade_e_comprovante_sem_tocar_vigencias(
    sessao,
    criar_persona,
    criar_tipo_de_recurso,
    criar_valor_de_referencia,
    criar_preco_de_referencia,
):
    admin = criar_persona(Papel.admin)
    tipo = criar_tipo_de_recurso(admin)
    valor = criar_valor_de_referencia(admin, tipo, valor_em_moedas=Decimal("2.00"))
    preco = criar_preco_de_referencia(admin, tipo, preco_em_pontos_extras=30)

    alterar_tipo_de_recurso(
        sessao,
        tipo,
        operador=admin,
        nome="Lanche da tarde",
        unidade="porção",
        exige_comprovante=True,
    )
    sessao.commit()

    assert (tipo.nome, tipo.unidade, tipo.exige_comprovante) == (
        "Lanche da tarde",
        "porção",
        True,
    )
    sessao.refresh(valor)
    sessao.refresh(preco)
    assert valor.valor_em_moedas == Decimal("2.00") and valor.vigencia_fim is None
    assert preco.preco_em_pontos_extras == 30 and preco.vigencia_fim is None


def test_natureza_nao_se_altera(sessao, criar_persona, criar_tipo_de_recurso):
    admin = criar_persona(Papel.admin)
    tipo = criar_tipo_de_recurso(admin)

    with pytest.raises(ErroDeValidacao) as erro:
        alterar_tipo_de_recurso(
            sessao, tipo, operador=admin, natureza=NaturezaDoRecurso.servico.value
        )

    assert erro.value.campo == "natureza"
    assert tipo.natureza == NaturezaDoRecurso.consumivel


def test_unidade_em_branco_e_recusada(sessao, criar_persona, criar_tipo_de_recurso):
    admin = criar_persona(Papel.admin)
    tipo = criar_tipo_de_recurso(admin)

    with pytest.raises(ErroDeValidacao) as erro:
        alterar_tipo_de_recurso(sessao, tipo, operador=admin, unidade="   ")

    assert erro.value.campo == "unidade"
    assert tipo.unidade == "unidade"


@pytest.mark.parametrize("papel", [Papel.mestre, Papel.apoiador])
def test_quem_nao_e_admin_nao_altera_desativa_nem_exclui(
    sessao, criar_persona, criar_tipo_de_recurso, papel
):
    admin = criar_persona(Papel.admin)
    outro = criar_persona(papel, criada_por=admin)
    tipo = criar_tipo_de_recurso(admin)

    with pytest.raises(PermissaoNegada):
        alterar_tipo_de_recurso(sessao, tipo, operador=outro, nome="Outro")
    with pytest.raises(PermissaoNegada):
        desativar_tipo_de_recurso(sessao, tipo, operador=outro)
    with pytest.raises(PermissaoNegada):
        reativar_tipo_de_recurso(sessao, tipo, operador=outro)
    with pytest.raises(PermissaoNegada):
        excluir_tipo_de_recurso(sessao, tipo, operador=outro)


def test_tipo_nasce_ativo_e_desativa_e_reativa_sem_efeito_repetido(
    sessao, criar_persona, criar_tipo_de_recurso
):
    admin = criar_persona(Papel.admin)
    tipo = criar_tipo_de_recurso(admin)
    assert tipo.ativo is True

    desativar_tipo_de_recurso(sessao, tipo, operador=admin)
    desativar_tipo_de_recurso(sessao, tipo, operador=admin)
    assert tipo.ativo is False
    with pytest.raises(ErroDeValidacao):
        exigir_tipo_de_recurso_ativo(tipo)

    reativar_tipo_de_recurso(sessao, tipo, operador=admin)
    reativar_tipo_de_recurso(sessao, tipo, operador=admin)
    assert tipo.ativo is True
    exigir_tipo_de_recurso_ativo(tipo)


def test_tipo_nunca_usado_e_excluido_com_as_vigencias(
    sessao,
    criar_persona,
    criar_tipo_de_recurso,
    criar_valor_de_referencia,
    criar_preco_de_referencia,
):
    admin = criar_persona(Papel.admin)
    tipo = criar_tipo_de_recurso(admin)
    criar_valor_de_referencia(admin, tipo)
    criar_preco_de_referencia(admin, tipo)
    id_do_tipo = tipo.id

    excluir_tipo_de_recurso(sessao, tipo, operador=admin)
    sessao.commit()

    assert sessao.get(TipoDeRecurso, id_do_tipo) is None
    assert sessao.query(ValorDeReferencia).filter_by(tipo_de_recurso_id=id_do_tipo).count() == 0
    assert sessao.query(PrecoDeReferencia).filter_by(tipo_de_recurso_id=id_do_tipo).count() == 0


@pytest.mark.parametrize("uso", ["lancamento", "recompensa", "item_avulso"])
def test_tipo_usado_nao_e_excluido(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_lancamento,
    criar_trilha,
    criar_missao,
    criar_recompensa_de_marco,
    criar_item_de_catalogo_avulso,
    uso,
):
    admin = criar_persona(Papel.admin)
    tipo = criar_tipo_de_recurso(admin)
    comunidade = criar_comunidade()
    ponto = criar_ponto_de_apoio(admin, comunidade)
    if uso == "lancamento":
        criar_lancamento(admin, tipo, ponto)
    elif uso == "recompensa":
        mestre = criar_persona(Papel.mestre, criada_por=admin)
        trilha = criar_trilha(mestre)
        criar_recompensa_de_marco(mestre, trilha, criar_missao(trilha, mestre), tipo)
    else:
        mestre = criar_persona(Papel.mestre, criada_por=admin)
        criar_item_de_catalogo_avulso(mestre, tipo, comunidade, ponto)

    with pytest.raises(TipoEmUso):
        excluir_tipo_de_recurso(sessao, tipo, operador=admin)

    sessao.rollback()
    assert sessao.get(TipoDeRecurso, tipo.id) is not None
