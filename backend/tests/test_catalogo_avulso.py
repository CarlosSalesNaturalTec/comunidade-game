from decimal import Decimal

import pytest

from nucleo.catalogo_avulso.modelo import (
    ItemDeCatalogoAvulso,
    OrigemDoCadastroDoItem,
    SituacaoDeHomologacao,
)
from nucleo.catalogo_avulso.regra import (
    alterar_estoque,
    ativar_item,
    cadastrar_item,
    contar_trocas_por_item,
    falta_de_lastro,
    homologar_item,
    listar_catalogo,
    listar_ofertas_do_apoiador,
    retirar_item,
)
from nucleo.erros import ErroDeValidacao, PermissaoNegada
from nucleo.livro_razao.modelo import NaturezaDoLancamento
from nucleo.personas.modelo import Papel


def _cadastrar_lastro(criar_lancamento, autor, tipo, ponto_de_apoio, quantidade):
    return criar_lancamento(
        autor,
        tipo,
        ponto_de_apoio,
        natureza=NaturezaDoLancamento.credito,
        quantidade=Decimal(quantidade),
    )


# --- 4.3 Cadastro -----------------------------------------------------------


def test_mestre_cadastra_item_na_sua_comunidade(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_vinculo_jogador,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    mestre = criar_persona(Papel.mestre)
    criar_vinculo_jogador(mestre, comunidade)

    item = cadastrar_item(
        sessao,
        operador=mestre,
        nome="Kit de Robótica",
        tipo=tipo,
        estoque=Decimal("1"),
        comunidade=comunidade,
        ponto_de_apoio=ponto,
    )
    sessao.commit()

    assert item.origem_do_cadastro == OrigemDoCadastroDoItem.mestre
    assert item.situacao_de_homologacao == SituacaoDeHomologacao.nao_se_aplica
    assert item.autor_id == mestre.id


def test_apoiador_oferta_item_ao_catalogo(
    sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio, criar_tipo_de_recurso
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    apoiador = criar_persona(Papel.apoiador)

    item = cadastrar_item(
        sessao,
        operador=apoiador,
        nome="Kit de Robótica",
        tipo=tipo,
        estoque=Decimal("1"),
        comunidade=comunidade,
        ponto_de_apoio=ponto,
    )
    sessao.commit()

    assert item.origem_do_cadastro == OrigemDoCadastroDoItem.apoiador
    assert item.situacao_de_homologacao == SituacaoDeHomologacao.pendente


def test_ponto_de_apoio_de_outra_comunidade_e_recusado(
    sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio, criar_tipo_de_recurso
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    outra_comunidade = criar_comunidade("Outra Comunidade")
    ponto_de_outra = criar_ponto_de_apoio(admin, outra_comunidade)
    tipo = criar_tipo_de_recurso(admin)
    apoiador = criar_persona(Papel.apoiador)

    with pytest.raises(ErroDeValidacao) as excinfo:
        cadastrar_item(
            sessao,
            operador=apoiador,
            nome="Kit de Robótica",
            tipo=tipo,
            estoque=Decimal("1"),
            comunidade=comunidade,
            ponto_de_apoio=ponto_de_outra,
        )
    assert excinfo.value.campo == "ponto_de_apoio_id"
    assert sessao.query(ItemDeCatalogoAvulso).count() == 0


def test_mestre_fora_do_vinculo_nao_cadastra(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_vinculo_jogador,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    outra_comunidade = criar_comunidade("Outra Comunidade")
    ponto = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    mestre = criar_persona(Papel.mestre)
    criar_vinculo_jogador(mestre, outra_comunidade)

    with pytest.raises(PermissaoNegada):
        cadastrar_item(
            sessao,
            operador=mestre,
            nome="Kit de Robótica",
            tipo=tipo,
            estoque=Decimal("1"),
            comunidade=comunidade,
            ponto_de_apoio=ponto,
        )
    assert sessao.query(ItemDeCatalogoAvulso).count() == 0


def test_guerreiro_nao_cadastra_item(
    sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio, criar_tipo_de_recurso
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)

    with pytest.raises(PermissaoNegada):
        cadastrar_item(
            sessao,
            operador=guerreiro,
            nome="Kit de Robótica",
            tipo=tipo,
            estoque=Decimal("1"),
            comunidade=comunidade,
            ponto_de_apoio=ponto,
        )
    assert sessao.query(ItemDeCatalogoAvulso).count() == 0


def test_estoque_menor_que_um_e_recusado(
    sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio, criar_tipo_de_recurso
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    apoiador = criar_persona(Papel.apoiador)

    with pytest.raises(ErroDeValidacao) as excinfo:
        cadastrar_item(
            sessao,
            operador=apoiador,
            nome="Kit de Robótica",
            tipo=tipo,
            estoque=Decimal("0"),
            comunidade=comunidade,
            ponto_de_apoio=ponto,
        )
    assert excinfo.value.campo == "estoque"
    assert sessao.query(ItemDeCatalogoAvulso).count() == 0


def test_cadastro_com_preco_declarado_e_recusado(
    sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio, criar_tipo_de_recurso
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    apoiador = criar_persona(Papel.apoiador)

    with pytest.raises(ErroDeValidacao) as excinfo:
        cadastrar_item(
            sessao,
            operador=apoiador,
            nome="Kit de Robótica",
            tipo=tipo,
            estoque=Decimal("1"),
            comunidade=comunidade,
            ponto_de_apoio=ponto,
            preco_em_pontos_extras=20,
        )
    assert excinfo.value.campo == "preco_em_pontos_extras"
    assert sessao.query(ItemDeCatalogoAvulso).count() == 0


# --- 4.4 Homologação ---------------------------------------------------------


def test_item_de_mestre_dispensa_homologacao(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_vinculo_jogador,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    mestre = criar_persona(Papel.mestre)
    criar_vinculo_jogador(mestre, comunidade)

    item = cadastrar_item(
        sessao,
        operador=mestre,
        nome="Kit",
        tipo=tipo,
        estoque=Decimal("1"),
        comunidade=comunidade,
        ponto_de_apoio=ponto,
    )
    sessao.commit()

    assert item.situacao_de_homologacao == SituacaoDeHomologacao.nao_se_aplica


def test_item_de_apoiador_nasce_pendente_e_inativo_mesmo_com_lastro(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_preco_de_referencia,
    criar_lancamento,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    criar_preco_de_referencia(admin, tipo)
    _cadastrar_lastro(criar_lancamento, admin, tipo, ponto, "10")
    apoiador = criar_persona(Papel.apoiador)

    item = cadastrar_item(
        sessao,
        operador=apoiador,
        nome="Kit",
        tipo=tipo,
        estoque=Decimal("5"),
        comunidade=comunidade,
        ponto_de_apoio=ponto,
    )
    sessao.commit()

    assert item.situacao_de_homologacao == SituacaoDeHomologacao.pendente
    assert item.ativo is False


def test_admin_homologa_item_pendente_com_lastro_e_ativa(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_preco_de_referencia,
    criar_lancamento,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    criar_preco_de_referencia(admin, tipo)
    _cadastrar_lastro(criar_lancamento, admin, tipo, ponto, "10")
    apoiador = criar_persona(Papel.apoiador)
    item = cadastrar_item(
        sessao,
        operador=apoiador,
        nome="Kit",
        tipo=tipo,
        estoque=Decimal("5"),
        comunidade=comunidade,
        ponto_de_apoio=ponto,
    )
    sessao.commit()

    item = homologar_item(
        sessao, operador=admin, item=item, decisao=SituacaoDeHomologacao.homologado.value
    )
    sessao.commit()

    assert item.situacao_de_homologacao == SituacaoDeHomologacao.homologado
    assert item.ativo is True


def test_admin_recusa_item_pendente_com_motivo(
    sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio, criar_tipo_de_recurso
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    apoiador = criar_persona(Papel.apoiador)
    item = cadastrar_item(
        sessao,
        operador=apoiador,
        nome="Kit",
        tipo=tipo,
        estoque=Decimal("1"),
        comunidade=comunidade,
        ponto_de_apoio=ponto,
    )
    sessao.commit()

    item = homologar_item(
        sessao,
        operador=admin,
        item=item,
        decisao=SituacaoDeHomologacao.recusado.value,
        motivo="Item fora da política de recompensas.",
    )
    sessao.commit()

    assert item.situacao_de_homologacao == SituacaoDeHomologacao.recusado
    assert item.homologacao_motivo == "Item fora da política de recompensas."
    assert item.ativo is False


def test_mestre_nao_homologa_item_de_apoiador(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_vinculo_jogador,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    apoiador = criar_persona(Papel.apoiador)
    item = cadastrar_item(
        sessao,
        operador=apoiador,
        nome="Kit",
        tipo=tipo,
        estoque=Decimal("1"),
        comunidade=comunidade,
        ponto_de_apoio=ponto,
    )
    sessao.commit()
    mestre = criar_persona(Papel.mestre)
    criar_vinculo_jogador(mestre, comunidade)

    with pytest.raises(PermissaoNegada):
        homologar_item(
            sessao,
            operador=mestre,
            item=item,
            decisao=SituacaoDeHomologacao.homologado.value,
        )
    sessao.refresh(item)
    assert item.situacao_de_homologacao == SituacaoDeHomologacao.pendente


# --- 4.5 Lastro ---------------------------------------------------------------


def test_item_com_saldo_igual_ao_estoque_nasce_ativo(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_preco_de_referencia,
    criar_lancamento,
    criar_vinculo_jogador,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    criar_preco_de_referencia(admin, tipo)
    _cadastrar_lastro(criar_lancamento, admin, tipo, ponto, "10")
    mestre = criar_persona(Papel.mestre)
    criar_vinculo_jogador(mestre, comunidade)

    item = cadastrar_item(
        sessao,
        operador=mestre,
        nome="Kit",
        tipo=tipo,
        estoque=Decimal("10"),
        comunidade=comunidade,
        ponto_de_apoio=ponto,
    )
    sessao.commit()

    assert item.ativo is True


def test_item_sem_lastro_suficiente_nasce_inativo_dizendo_o_que_falta(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_preco_de_referencia,
    criar_lancamento,
    criar_vinculo_jogador,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    criar_preco_de_referencia(admin, tipo)
    _cadastrar_lastro(criar_lancamento, admin, tipo, ponto, "4")
    mestre = criar_persona(Papel.mestre)
    criar_vinculo_jogador(mestre, comunidade)

    item = cadastrar_item(
        sessao,
        operador=mestre,
        nome="Kit",
        tipo=tipo,
        estoque=Decimal("10"),
        comunidade=comunidade,
        ponto_de_apoio=ponto,
    )
    sessao.commit()

    assert item.ativo is False
    assert falta_de_lastro(sessao, item=item) == Decimal("6")


def test_saldo_de_outro_ponto_de_apoio_nao_lastreia_o_item(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_preco_de_referencia,
    criar_lancamento,
    criar_vinculo_jogador,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto = criar_ponto_de_apoio(admin, comunidade, nome="Ponto A")
    outro_ponto = criar_ponto_de_apoio(admin, comunidade, nome="Ponto B")
    tipo = criar_tipo_de_recurso(admin)
    criar_preco_de_referencia(admin, tipo)
    _cadastrar_lastro(criar_lancamento, admin, tipo, outro_ponto, "10")
    mestre = criar_persona(Papel.mestre)
    criar_vinculo_jogador(mestre, comunidade)

    item = cadastrar_item(
        sessao,
        operador=mestre,
        nome="Kit",
        tipo=tipo,
        estoque=Decimal("5"),
        comunidade=comunidade,
        ponto_de_apoio=ponto,
    )
    sessao.commit()

    assert item.ativo is False


def test_ativacao_reverifica_o_lastro(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_preco_de_referencia,
    criar_lancamento,
    criar_vinculo_jogador,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    criar_preco_de_referencia(admin, tipo)
    _cadastrar_lastro(criar_lancamento, admin, tipo, ponto, "4")
    mestre = criar_persona(Papel.mestre)
    criar_vinculo_jogador(mestre, comunidade)
    item = cadastrar_item(
        sessao,
        operador=mestre,
        nome="Kit",
        tipo=tipo,
        estoque=Decimal("10"),
        comunidade=comunidade,
        ponto_de_apoio=ponto,
    )
    sessao.commit()
    assert item.ativo is False

    _cadastrar_lastro(criar_lancamento, admin, tipo, ponto, "6")
    item = ativar_item(sessao, operador=mestre, item=item)
    sessao.commit()

    assert item.ativo is True


def test_ativacao_sem_lastro_e_recusada(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_preco_de_referencia,
    criar_vinculo_jogador,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    criar_preco_de_referencia(admin, tipo)
    mestre = criar_persona(Papel.mestre)
    criar_vinculo_jogador(mestre, comunidade)
    item = cadastrar_item(
        sessao,
        operador=mestre,
        nome="Kit",
        tipo=tipo,
        estoque=Decimal("10"),
        comunidade=comunidade,
        ponto_de_apoio=ponto,
    )
    sessao.commit()

    with pytest.raises(ErroDeValidacao):
        ativar_item(sessao, operador=mestre, item=item)
    sessao.refresh(item)
    assert item.ativo is False


def test_item_pendente_de_homologacao_nao_ativa(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_preco_de_referencia,
    criar_lancamento,
    criar_vinculo_jogador,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    criar_preco_de_referencia(admin, tipo)
    _cadastrar_lastro(criar_lancamento, admin, tipo, ponto, "10")
    apoiador = criar_persona(Papel.apoiador)
    item = cadastrar_item(
        sessao,
        operador=apoiador,
        nome="Kit",
        tipo=tipo,
        estoque=Decimal("10"),
        comunidade=comunidade,
        ponto_de_apoio=ponto,
    )
    sessao.commit()
    mestre = criar_persona(Papel.mestre)
    criar_vinculo_jogador(mestre, comunidade)

    with pytest.raises(ErroDeValidacao):
        ativar_item(sessao, operador=mestre, item=item)
    sessao.refresh(item)
    assert item.ativo is False


def test_tipo_sem_preco_vigente_nasce_inativo(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_lancamento,
    criar_vinculo_jogador,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    _cadastrar_lastro(criar_lancamento, admin, tipo, ponto, "10")
    mestre = criar_persona(Papel.mestre)
    criar_vinculo_jogador(mestre, comunidade)

    item = cadastrar_item(
        sessao,
        operador=mestre,
        nome="Kit",
        tipo=tipo,
        estoque=Decimal("10"),
        comunidade=comunidade,
        ponto_de_apoio=ponto,
    )
    sessao.commit()

    assert item.ativo is False


# --- 4.6 Manutenção e leitura --------------------------------------------------


def test_mestre_altera_estoque_dentro_do_lastro(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_preco_de_referencia,
    criar_lancamento,
    criar_vinculo_jogador,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    criar_preco_de_referencia(admin, tipo)
    _cadastrar_lastro(criar_lancamento, admin, tipo, ponto, "10")
    mestre = criar_persona(Papel.mestre)
    criar_vinculo_jogador(mestre, comunidade)
    item = cadastrar_item(
        sessao,
        operador=mestre,
        nome="Kit",
        tipo=tipo,
        estoque=Decimal("10"),
        comunidade=comunidade,
        ponto_de_apoio=ponto,
    )
    sessao.commit()
    assert item.ativo is True

    item = alterar_estoque(sessao, operador=mestre, item=item, estoque=Decimal("5"))
    sessao.commit()

    assert item.estoque == Decimal("5")
    assert item.ativo is True


def test_estoque_acima_do_lastro_desativa_o_item(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_preco_de_referencia,
    criar_lancamento,
    criar_vinculo_jogador,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    criar_preco_de_referencia(admin, tipo)
    _cadastrar_lastro(criar_lancamento, admin, tipo, ponto, "10")
    mestre = criar_persona(Papel.mestre)
    criar_vinculo_jogador(mestre, comunidade)
    item = cadastrar_item(
        sessao,
        operador=mestre,
        nome="Kit",
        tipo=tipo,
        estoque=Decimal("10"),
        comunidade=comunidade,
        ponto_de_apoio=ponto,
    )
    sessao.commit()
    assert item.ativo is True

    item = alterar_estoque(sessao, operador=mestre, item=item, estoque=Decimal("20"))
    sessao.commit()

    assert item.estoque == Decimal("20")
    assert item.ativo is False
    assert falta_de_lastro(sessao, item=item) == Decimal("10")


def test_mestre_retira_o_item_do_catalogo(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_preco_de_referencia,
    criar_lancamento,
    criar_vinculo_jogador,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    criar_preco_de_referencia(admin, tipo)
    _cadastrar_lastro(criar_lancamento, admin, tipo, ponto, "10")
    mestre = criar_persona(Papel.mestre)
    criar_vinculo_jogador(mestre, comunidade)
    item = cadastrar_item(
        sessao,
        operador=mestre,
        nome="Kit",
        tipo=tipo,
        estoque=Decimal("10"),
        comunidade=comunidade,
        ponto_de_apoio=ponto,
    )
    sessao.commit()
    assert item.ativo is True

    item = retirar_item(sessao, operador=mestre, item=item)
    sessao.commit()

    assert item.ativo is False
    assert sessao.query(ItemDeCatalogoAvulso).filter_by(id=item.id).count() == 1


def test_apoiador_nao_altera_item_ja_cadastrado(
    sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio, criar_tipo_de_recurso
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    apoiador = criar_persona(Papel.apoiador)
    item = cadastrar_item(
        sessao,
        operador=apoiador,
        nome="Kit",
        tipo=tipo,
        estoque=Decimal("1"),
        comunidade=comunidade,
        ponto_de_apoio=ponto,
    )
    sessao.commit()

    with pytest.raises(PermissaoNegada):
        alterar_estoque(sessao, operador=apoiador, item=item, estoque=Decimal("2"))
    sessao.refresh(item)
    assert item.estoque == Decimal("1")


def test_catalogo_filtrado_pela_comunidade_do_guerreiro(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_preco_de_referencia,
    criar_lancamento,
    criar_vinculo_jogador,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    outra_comunidade = criar_comunidade("Outra Comunidade")
    ponto = criar_ponto_de_apoio(admin, comunidade)
    ponto_de_outra = criar_ponto_de_apoio(admin, outra_comunidade)
    tipo = criar_tipo_de_recurso(admin)
    criar_preco_de_referencia(admin, tipo)
    _cadastrar_lastro(criar_lancamento, admin, tipo, ponto, "10")
    _cadastrar_lastro(criar_lancamento, admin, tipo, ponto_de_outra, "10")
    mestre = criar_persona(Papel.mestre)
    criar_vinculo_jogador(mestre, comunidade)
    outro_mestre = criar_persona(Papel.mestre)
    criar_vinculo_jogador(outro_mestre, outra_comunidade)
    cadastrar_item(
        sessao,
        operador=mestre,
        nome="Kit da Comunidade",
        tipo=tipo,
        estoque=Decimal("10"),
        comunidade=comunidade,
        ponto_de_apoio=ponto,
    )
    cadastrar_item(
        sessao,
        operador=outro_mestre,
        nome="Kit de Outra Comunidade",
        tipo=tipo,
        estoque=Decimal("10"),
        comunidade=outra_comunidade,
        ponto_de_apoio=ponto_de_outra,
    )
    sessao.commit()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)

    itens = listar_catalogo(sessao, operador=guerreiro, comunidade=None)

    assert [item.nome for item in itens] == ["Kit da Comunidade"]


def test_inativos_so_para_admin_e_mestre_vinculado(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_item_de_catalogo_avulso,
    criar_vinculo_jogador,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    criar_item_de_catalogo_avulso(admin, tipo, comunidade, ponto, ativo=False)
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    mestre = criar_persona(Papel.mestre)
    criar_vinculo_jogador(mestre, comunidade)

    itens_do_guerreiro = listar_catalogo(
        sessao, operador=guerreiro, comunidade=None, incluir_inativos=True
    )
    itens_do_mestre = listar_catalogo(
        sessao, operador=mestre, comunidade=None, incluir_inativos=True
    )
    itens_do_admin = listar_catalogo(
        sessao, operador=admin, comunidade=comunidade, incluir_inativos=True
    )

    assert itens_do_guerreiro == []
    assert len(itens_do_mestre) == 1
    assert len(itens_do_admin) == 1


def test_saida_do_catalogo_pela_rota_nao_traz_moedas_nem_reais(
    sessao,
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_preco_de_referencia,
    criar_lancamento,
    criar_vinculo_jogador,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    criar_preco_de_referencia(admin, tipo, preco_em_pontos_extras=25)
    _cadastrar_lastro(criar_lancamento, admin, tipo, ponto, "10")
    mestre = criar_persona(Papel.mestre)
    criar_vinculo_jogador(mestre, comunidade)
    cadastrar_item(
        sessao,
        operador=mestre,
        nome="Kit",
        tipo=tipo,
        estoque=Decimal("5"),
        comunidade=comunidade,
        ponto_de_apoio=ponto,
    )
    sessao.commit()

    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.get(
        "/v1/catalogo-avulso",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    for item in corpo:
        assert "valor_em_moedas" not in item
        assert "valor_em_reais" not in item


# --- 4.7 Leitura das próprias ofertas -------------------------------------------


def test_listar_ofertas_do_apoiador_recusa_persona_de_outro_papel(sessao, criar_persona):
    mestre = criar_persona(Papel.mestre)

    with pytest.raises(PermissaoNegada):
        listar_ofertas_do_apoiador(sessao, operador=mestre)


def test_apoiador_le_os_proprios_itens_em_qualquer_situacao(
    sessao,
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_preco_de_referencia,
    criar_lancamento,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto = criar_ponto_de_apoio(admin, comunidade)
    tipo_com_preco = criar_tipo_de_recurso(admin, nome="Tipo com preço")
    criar_preco_de_referencia(admin, tipo_com_preco)
    tipo_sem_preco = criar_tipo_de_recurso(admin, nome="Tipo sem preço")
    _cadastrar_lastro(criar_lancamento, admin, tipo_com_preco, ponto, "10")
    apoiador = criar_persona(Papel.apoiador)
    outro_apoiador = criar_persona(Papel.apoiador)

    pendente = cadastrar_item(
        sessao,
        operador=apoiador,
        nome="Item pendente",
        tipo=tipo_com_preco,
        estoque=Decimal("1"),
        comunidade=comunidade,
        ponto_de_apoio=ponto,
    )
    recusado = cadastrar_item(
        sessao,
        operador=apoiador,
        nome="Item recusado",
        tipo=tipo_com_preco,
        estoque=Decimal("1"),
        comunidade=comunidade,
        ponto_de_apoio=ponto,
    )
    sem_lastro = cadastrar_item(
        sessao,
        operador=apoiador,
        nome="Item sem lastro",
        tipo=tipo_com_preco,
        estoque=Decimal("100"),
        comunidade=comunidade,
        ponto_de_apoio=ponto,
    )
    sem_preco = cadastrar_item(
        sessao,
        operador=apoiador,
        nome="Item sem preço",
        tipo=tipo_sem_preco,
        estoque=Decimal("1"),
        comunidade=comunidade,
        ponto_de_apoio=ponto,
    )
    sessao.commit()
    homologar_item(
        sessao,
        operador=admin,
        item=recusado,
        decisao=SituacaoDeHomologacao.recusado.value,
        motivo="Fora da política.",
    )
    homologar_item(
        sessao, operador=admin, item=sem_lastro, decisao=SituacaoDeHomologacao.homologado.value
    )
    homologar_item(
        sessao, operador=admin, item=sem_preco, decisao=SituacaoDeHomologacao.homologado.value
    )
    sessao.commit()
    cadastrar_item(
        sessao,
        operador=outro_apoiador,
        nome="Item de outro Apoiador",
        tipo=tipo_com_preco,
        estoque=Decimal("1"),
        comunidade=comunidade,
        ponto_de_apoio=ponto,
    )
    sessao.commit()

    assert {item.nome for item in listar_ofertas_do_apoiador(sessao, operador=apoiador)} == {
        pendente.nome,
        recusado.nome,
        sem_lastro.nome,
        sem_preco.nome,
    }

    token, _ = criar_sessao_de_teste(apoiador)
    resposta = cliente.get(
        "/v1/eu/catalogo-avulso",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    nomes = {item["nome"] for item in corpo}
    assert nomes == {"Item pendente", "Item recusado", "Item sem lastro", "Item sem preço"}

    por_nome = {item["nome"]: item for item in corpo}
    assert por_nome["Item pendente"]["situacao_de_homologacao"] == "pendente"
    assert por_nome["Item pendente"]["ativo"] is False
    assert por_nome["Item recusado"]["situacao_de_homologacao"] == "recusado"
    assert por_nome["Item recusado"]["homologacao_motivo"] == "Fora da política."
    assert por_nome["Item sem lastro"]["ativo"] is False
    assert por_nome["Item sem lastro"]["quantidade_faltante"] is not None
    assert por_nome["Item sem preço"]["ativo"] is False
    assert por_nome["Item sem preço"]["preco_de_referencia_ausente"] is True
    for item in corpo:
        assert "valor_em_moedas" not in item
        assert "valor_em_reais" not in item


def test_persona_de_outro_papel_recebe_403_na_leitura_das_proprias_ofertas(
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_vinculo_jogador,
):
    chave, _ = criar_chave()
    comunidade = criar_comunidade()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre)
    criar_vinculo_jogador(mestre, comunidade)
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    responsavel = criar_persona(Papel.responsavel)

    for persona in (admin, mestre, guerreiro, responsavel):
        token, _ = criar_sessao_de_teste(persona)
        resposta = cliente.get(
            "/v1/eu/catalogo-avulso",
            headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
        )
        assert resposta.status_code == 403


# --- 4.8 Contagem de trocas ------------------------------------------------------


def test_item_sem_troca_traz_contagem_zero(
    sessao,
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    apoiador = criar_persona(Papel.apoiador)
    item = cadastrar_item(
        sessao,
        operador=apoiador,
        nome="Kit",
        tipo=tipo,
        estoque=Decimal("1"),
        comunidade=comunidade,
        ponto_de_apoio=ponto,
    )
    sessao.commit()

    assert contar_trocas_por_item(sessao, item=item) == 0

    token, _ = criar_sessao_de_teste(apoiador)
    resposta = cliente.get(
        "/v1/eu/catalogo-avulso",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.json()[0]["quantidade_de_trocas"] == 0


def test_item_com_tres_trocas_traz_a_contagem_agregada_sem_identificar_quem_trocou(
    sessao,
    cliente,
    criar_chave,
    criar_persona,
    criar_sessao_de_teste,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_aula,
    criar_troca,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    apoiador = criar_persona(Papel.apoiador)
    item = cadastrar_item(
        sessao,
        operador=apoiador,
        nome="Kit",
        tipo=tipo,
        estoque=Decimal("1"),
        comunidade=comunidade,
        ponto_de_apoio=ponto,
    )
    sessao.commit()
    mestre = criar_persona(Papel.mestre)
    aula = criar_aula(mestre, comunidade, ponto)
    guerreiro_1 = criar_persona(Papel.guerreiro, comunidade=comunidade)
    guerreiro_2 = criar_persona(Papel.guerreiro, comunidade=comunidade)
    guerreiro_3 = criar_persona(Papel.guerreiro, comunidade=comunidade)
    criar_troca(mestre, item, guerreiro_1, aula)
    criar_troca(mestre, item, guerreiro_2, aula)
    criar_troca(mestre, item, guerreiro_3, aula)

    assert contar_trocas_por_item(sessao, item=item) == 3

    token, _ = criar_sessao_de_teste(apoiador)
    resposta = cliente.get(
        "/v1/eu/catalogo-avulso",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    corpo = resposta.json()
    assert corpo[0]["quantidade_de_trocas"] == 3
    for chave_do_campo in ("persona", "nick", "guerreiro_id", "aula_id", "data_da_troca"):
        assert chave_do_campo not in corpo[0]
