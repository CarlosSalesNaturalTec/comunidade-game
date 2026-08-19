from decimal import Decimal

import pytest

from nucleo.catalogo_avulso.modelo import ItemDeCatalogoAvulso
from nucleo.erros import ErroDeValidacao, PermissaoNegada
from nucleo.livro_razao.modelo import Lancamento, NaturezaDoLancamento
from nucleo.personas.modelo import Papel
from nucleo.ponto_extra.modelo import PontoExtra
from nucleo.reservas.modelo import Reserva
from nucleo.trocas.modelo import Troca
from nucleo.trocas.regra import listar_trocas, registrar_troca


def _preparar(
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
    *,
    preco=20,
    estoque=Decimal("5"),
    lastro=Decimal("10"),
    saldo_disponivel=100,
    acumulado=None,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    criar_preco_de_referencia(admin, tipo, preco_em_pontos_extras=preco)
    criar_valor_de_referencia(admin, tipo, valor_em_moedas=Decimal("1.00"))
    criar_lancamento(
        admin,
        tipo,
        ponto_de_apoio,
        natureza=NaturezaDoLancamento.credito,
        quantidade=lastro,
    )
    mestre = criar_persona(Papel.mestre)
    criar_vinculo_jogador(mestre, comunidade)
    item = criar_item_de_catalogo_avulso(
        admin, tipo, comunidade, ponto_de_apoio, estoque=estoque, ativo=True
    )
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    criar_ponto_extra(
        guerreiro,
        acumulado=acumulado if acumulado is not None else saldo_disponivel,
        saldo_disponivel=saldo_disponivel,
    )
    aula = criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)
    return {
        "admin": admin,
        "comunidade": comunidade,
        "ponto_de_apoio": ponto_de_apoio,
        "tipo": tipo,
        "mestre": mestre,
        "item": item,
        "guerreiro": guerreiro,
        "aula": aula,
    }


_FIXTURES = (
    "criar_persona",
    "criar_comunidade",
    "criar_ponto_de_apoio",
    "criar_tipo_de_recurso",
    "criar_preco_de_referencia",
    "criar_valor_de_referencia",
    "criar_lancamento",
    "criar_vinculo_jogador",
    "criar_item_de_catalogo_avulso",
    "criar_ponto_extra",
    "criar_aula",
)


@pytest.fixture
def cenario(request):
    def _montar(**kwargs):
        fixtures = [request.getfixturevalue(nome) for nome in _FIXTURES]
        return _preparar(*fixtures, **kwargs)

    return _montar


# --- 5.1 Registro e permissões ----------------------------------------------


def test_mestre_registra_troca_com_os_seis_atributos(sessao, cenario):
    c = cenario(preco=25)

    troca = registrar_troca(
        sessao, operador=c["mestre"], aula=c["aula"], item=c["item"], guerreiro=c["guerreiro"]
    )
    sessao.commit()

    assert troca.item_de_catalogo_avulso_id == c["item"].id
    assert troca.guerreiro_id == c["guerreiro"].id
    assert troca.preco_cobrado == 25
    assert troca.aula_id == c["aula"].id
    assert troca.autor_id == c["mestre"].id
    assert troca.papel_do_autor == Papel.mestre.value
    assert troca.registrado_em is not None


def test_aula_nao_realizada_nao_impede_troca(sessao, cenario):
    from nucleo.aulas.modelo import SituacaoDaAula

    c = cenario()
    c["aula"].situacao = SituacaoDaAula.prevista
    sessao.commit()

    troca = registrar_troca(
        sessao, operador=c["mestre"], aula=c["aula"], item=c["item"], guerreiro=c["guerreiro"]
    )
    sessao.commit()

    assert troca.id is not None


def test_guerreiro_sem_presenca_nao_impede_troca(sessao, cenario):
    c = cenario()

    troca = registrar_troca(
        sessao, operador=c["mestre"], aula=c["aula"], item=c["item"], guerreiro=c["guerreiro"]
    )
    sessao.commit()

    assert troca.id is not None


def test_mestre_de_outra_comunidade_nao_registra_troca(
    sessao, cenario, criar_persona, criar_vinculo_jogador, criar_comunidade
):
    c = cenario()
    outra_comunidade = criar_comunidade("Outra Comunidade")
    outro_mestre = criar_persona(Papel.mestre)
    criar_vinculo_jogador(outro_mestre, outra_comunidade)

    with pytest.raises(PermissaoNegada):
        registrar_troca(
            sessao, operador=outro_mestre, aula=c["aula"], item=c["item"], guerreiro=c["guerreiro"]
        )
    assert sessao.query(Troca).count() == 0


def test_guerreiro_nao_registra_a_propria_troca(sessao, cenario):
    c = cenario()

    with pytest.raises(PermissaoNegada):
        registrar_troca(
            sessao,
            operador=c["guerreiro"],
            aula=c["aula"],
            item=c["item"],
            guerreiro=c["guerreiro"],
        )
    assert sessao.query(Troca).count() == 0


def test_registro_sem_item_e_recusado(sessao, cenario):
    c = cenario()

    with pytest.raises(ErroDeValidacao) as excinfo:
        registrar_troca(
            sessao, operador=c["mestre"], aula=c["aula"], item=None, guerreiro=c["guerreiro"]
        )
    assert excinfo.value.campo == "item_id"
    assert sessao.query(Troca).count() == 0


# --- 5.2 Preço ---------------------------------------------------------------


def test_troca_cobra_preco_da_vigencia_corrente(sessao, cenario):
    c = cenario(preco=40)

    troca = registrar_troca(
        sessao, operador=c["mestre"], aula=c["aula"], item=c["item"], guerreiro=c["guerreiro"]
    )
    sessao.commit()

    assert troca.preco_cobrado == 40


def test_mudanca_posterior_do_preco_nao_altera_troca_gravada(
    sessao, cenario, criar_preco_de_referencia
):
    from datetime import date

    c = cenario(preco=40)

    troca = registrar_troca(
        sessao, operador=c["mestre"], aula=c["aula"], item=c["item"], guerreiro=c["guerreiro"]
    )
    sessao.commit()

    criar_preco_de_referencia(
        c["admin"], c["tipo"], preco_em_pontos_extras=60, vigencia_inicio=date(2026, 6, 1)
    )
    sessao.commit()
    sessao.refresh(troca)

    assert troca.preco_cobrado == 40


def test_item_de_tipo_sem_preco_vigente_nao_e_trocado(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
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
    criar_lancamento(
        admin, tipo, ponto_de_apoio, natureza=NaturezaDoLancamento.credito, quantidade=Decimal("10")
    )
    mestre = criar_persona(Papel.mestre)
    criar_vinculo_jogador(mestre, comunidade)
    item = criar_item_de_catalogo_avulso(
        admin, tipo, comunidade, ponto_de_apoio, estoque=Decimal("5"), ativo=True
    )
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    criar_ponto_extra(guerreiro, acumulado=100, saldo_disponivel=100)
    aula = criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)

    with pytest.raises(ErroDeValidacao) as excinfo:
        registrar_troca(sessao, operador=mestre, aula=aula, item=item, guerreiro=guerreiro)
    assert excinfo.value.campo == "item_id"
    assert sessao.query(Troca).count() == 0


# --- 5.3 Recusas --------------------------------------------------------------


def test_item_inativo_nao_e_trocado(sessao, cenario):
    c = cenario()
    c["item"].ativo = False
    sessao.commit()

    with pytest.raises(ErroDeValidacao) as excinfo:
        registrar_troca(
            sessao, operador=c["mestre"], aula=c["aula"], item=c["item"], guerreiro=c["guerreiro"]
        )
    assert excinfo.value.campo == "item_id"
    assert sessao.query(Troca).count() == 0


def test_lastro_caido_desde_a_ativacao_e_reverificado(sessao, cenario, criar_lancamento):
    c = cenario(lastro=Decimal("5"), estoque=Decimal("5"))
    # O item nasceu ativo com lastro 5 = estoque 5. Um débito posterior derruba o
    # saldo disponível a zero, sem que o item seja recadastrado.
    from nucleo.livro_razao.regra import lancar_debito

    lancar_debito(
        sessao,
        tipo_de_recurso_id=c["tipo"].id,
        ponto_de_apoio_id=c["ponto_de_apoio"].id,
        quantidade=Decimal("5"),
        valor_em_moedas=Decimal("5.00"),
        operador=c["admin"],
    )
    sessao.commit()

    with pytest.raises(ErroDeValidacao) as excinfo:
        registrar_troca(
            sessao, operador=c["mestre"], aula=c["aula"], item=c["item"], guerreiro=c["guerreiro"]
        )
    assert excinfo.value.campo == "item_id"
    assert sessao.query(Troca).count() == 0


def test_item_sem_estoque_nao_e_trocado(sessao, cenario):
    c = cenario()
    c["item"].estoque = Decimal("0")
    sessao.commit()

    with pytest.raises(ErroDeValidacao) as excinfo:
        registrar_troca(
            sessao, operador=c["mestre"], aula=c["aula"], item=c["item"], guerreiro=c["guerreiro"]
        )
    assert excinfo.value.campo == "item_id"
    assert sessao.query(Troca).count() == 0


def test_guerreiro_de_outra_comunidade_nao_troca(
    sessao, cenario, criar_persona, criar_comunidade, criar_vinculo_jogador
):
    c = cenario()
    outra_comunidade = criar_comunidade("Outra Comunidade")
    guerreiro_de_fora = criar_persona(Papel.guerreiro, comunidade=outra_comunidade)

    with pytest.raises(ErroDeValidacao) as excinfo:
        registrar_troca(
            sessao,
            operador=c["mestre"],
            aula=c["aula"],
            item=c["item"],
            guerreiro=guerreiro_de_fora,
        )
    assert excinfo.value.campo == "guerreiro_id"
    assert sessao.query(Troca).count() == 0


def test_saldo_menor_que_preco_recusa_a_troca(sessao, cenario):
    c = cenario(preco=40, saldo_disponivel=25, acumulado=25)

    with pytest.raises(ErroDeValidacao) as excinfo:
        registrar_troca(
            sessao, operador=c["mestre"], aula=c["aula"], item=c["item"], guerreiro=c["guerreiro"]
        )
    assert excinfo.value.campo == "guerreiro_id"

    conta = sessao.query(PontoExtra).filter_by(guerreiro_id=c["guerreiro"].id).one()
    item_atual = sessao.get(ItemDeCatalogoAvulso, c["item"].id)
    assert conta.saldo_disponivel == 25
    assert item_atual.estoque == Decimal("5")
    assert sessao.query(Troca).count() == 0
    assert sessao.query(Lancamento).filter_by(natureza=NaturezaDoLancamento.debito).count() == 0


# --- 5.4 Entrega --------------------------------------------------------------


def test_troca_move_as_quatro_coisas_juntas(sessao, cenario):
    c = cenario(
        preco=40, estoque=Decimal("5"), lastro=Decimal("5"), saldo_disponivel=100, acumulado=300
    )

    registrar_troca(
        sessao, operador=c["mestre"], aula=c["aula"], item=c["item"], guerreiro=c["guerreiro"]
    )
    sessao.commit()

    conta = sessao.query(PontoExtra).filter_by(guerreiro_id=c["guerreiro"].id).one()
    item_atual = sessao.get(ItemDeCatalogoAvulso, c["item"].id)
    from nucleo.livro_razao.regra import saldo_de

    saldo_do_tipo = saldo_de(
        sessao, tipo_de_recurso_id=c["tipo"].id, ponto_de_apoio_id=c["ponto_de_apoio"].id
    )

    assert conta.saldo_disponivel == 60
    assert conta.acumulado == 300
    assert item_atual.estoque == Decimal("4")
    assert saldo_do_tipo == Decimal("4")


def test_falha_no_lancamento_desfaz_tudo(sessao, cenario):
    from datetime import date

    from nucleo.recursos.modelo import ValorDeReferencia

    c = cenario()
    # Encerra a vigência do valor de referência antes da data da troca, para
    # que `lancar_debito` falhe por falta de vigência que cubra a data.
    sessao.query(ValorDeReferencia).filter_by(tipo_de_recurso_id=c["tipo"].id).update(
        {"vigencia_fim": date(2026, 1, 2)}
    )
    sessao.commit()

    with pytest.raises(ErroDeValidacao):
        registrar_troca(
            sessao, operador=c["mestre"], aula=c["aula"], item=c["item"], guerreiro=c["guerreiro"]
        )
    sessao.rollback()

    conta = sessao.query(PontoExtra).filter_by(guerreiro_id=c["guerreiro"].id).one()
    item_atual = sessao.get(ItemDeCatalogoAvulso, c["item"].id)
    assert conta.saldo_disponivel == 100
    assert item_atual.estoque == Decimal("5")
    assert sessao.query(Troca).count() == 0


def test_troca_nao_reserva_item(sessao, cenario):
    c = cenario()

    registrar_troca(
        sessao, operador=c["mestre"], aula=c["aula"], item=c["item"], guerreiro=c["guerreiro"]
    )
    sessao.commit()

    assert sessao.query(Reserva).count() == 0


def test_estoque_zerado_por_troca_mantem_item_cadastrado_e_ativo(sessao, cenario):
    c = cenario(estoque=Decimal("1"), lastro=Decimal("1"))

    registrar_troca(
        sessao, operador=c["mestre"], aula=c["aula"], item=c["item"], guerreiro=c["guerreiro"]
    )
    sessao.commit()

    item_atual = sessao.get(ItemDeCatalogoAvulso, c["item"].id)
    assert item_atual.estoque == Decimal("0")
    assert item_atual.ativo is True

    with pytest.raises(ErroDeValidacao) as excinfo:
        registrar_troca(
            sessao, operador=c["mestre"], aula=c["aula"], item=item_atual, guerreiro=c["guerreiro"]
        )
    assert excinfo.value.campo == "item_id"


# --- 5.5 Histórico -------------------------------------------------------------


def test_guerreiro_le_apenas_as_proprias_trocas(sessao, cenario, criar_persona, criar_ponto_extra):
    c = cenario()
    outro_guerreiro = criar_persona(Papel.guerreiro, comunidade=c["comunidade"])
    criar_ponto_extra(outro_guerreiro, acumulado=100, saldo_disponivel=100)
    troca_propria = registrar_troca(
        sessao, operador=c["mestre"], aula=c["aula"], item=c["item"], guerreiro=c["guerreiro"]
    )
    troca_de_outro = registrar_troca(
        sessao, operador=c["mestre"], aula=c["aula"], item=c["item"], guerreiro=outro_guerreiro
    )
    sessao.commit()

    trocas = listar_trocas(sessao, operador=c["guerreiro"])

    assert [t.id for t in trocas] == [troca_propria.id]
    assert troca_de_outro.id not in [t.id for t in trocas]


def test_mestre_le_trocas_das_suas_comunidades(
    sessao,
    cenario,
    criar_persona,
    criar_comunidade,
    criar_vinculo_jogador,
    criar_ponto_de_apoio,
    criar_item_de_catalogo_avulso,
    criar_aula,
    criar_ponto_extra,
    criar_lancamento,
):
    c = cenario()
    troca_da_comunidade = registrar_troca(
        sessao, operador=c["mestre"], aula=c["aula"], item=c["item"], guerreiro=c["guerreiro"]
    )
    sessao.commit()

    outra_comunidade = criar_comunidade("Outra Comunidade")
    outro_ponto = criar_ponto_de_apoio(c["admin"], outra_comunidade)
    criar_lancamento(
        c["admin"],
        c["tipo"],
        outro_ponto,
        natureza=NaturezaDoLancamento.credito,
        quantidade=Decimal("10"),
    )
    outro_item = criar_item_de_catalogo_avulso(
        c["admin"], c["tipo"], outra_comunidade, outro_ponto, estoque=Decimal("5"), ativo=True
    )
    outro_guerreiro = criar_persona(Papel.guerreiro, comunidade=outra_comunidade)
    criar_ponto_extra(outro_guerreiro, acumulado=100, saldo_disponivel=100)
    outra_aula = criar_aula(c["admin"], outra_comunidade, ponto_de_apoio=outro_ponto)
    outro_mestre = criar_persona(Papel.mestre)
    criar_vinculo_jogador(outro_mestre, outra_comunidade)

    registrar_troca(
        sessao, operador=outro_mestre, aula=outra_aula, item=outro_item, guerreiro=outro_guerreiro
    )
    sessao.commit()

    trocas_do_mestre = listar_trocas(sessao, operador=c["mestre"])

    assert [t.id for t in trocas_do_mestre] == [troca_da_comunidade.id]


def test_apoiador_nao_le_trocas(sessao, cenario, criar_persona):
    cenario()
    apoiador = criar_persona(Papel.apoiador)

    with pytest.raises(PermissaoNegada):
        listar_trocas(sessao, operador=apoiador)


def test_saida_do_historico_pela_rota_nao_traz_moedas_nem_reais(
    sessao,
    cliente,
    criar_chave,
    criar_sessao_de_teste,
    cenario,
):
    c = cenario()
    registrar_troca(
        sessao, operador=c["mestre"], aula=c["aula"], item=c["item"], guerreiro=c["guerreiro"]
    )
    sessao.commit()

    chave, _ = criar_chave()
    token, _ = criar_sessao_de_teste(c["guerreiro"])

    resposta = cliente.get(
        "/v1/trocas",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert len(corpo) == 1
    for troca in corpo:
        assert "valor_em_moedas" not in troca
        assert "valor_em_reais" not in troca
        assert "preco_cobrado" in troca


def test_preco_declarado_no_corpo_e_recusado_pela_rota(
    sessao, cliente, criar_chave, criar_sessao_de_teste, cenario
):
    c = cenario()
    chave, _ = criar_chave()
    token, _ = criar_sessao_de_teste(c["mestre"], origem="app-03-gestao")

    resposta = cliente.post(
        f"/v1/aulas/{c['aula'].id}/trocas",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
        json={
            "item_de_catalogo_avulso_id": str(c["item"].id),
            "guerreiro_id": str(c["guerreiro"].id),
            "preco_em_pontos_extras": 40,
        },
    )

    assert resposta.status_code == 422
    assert sessao.query(Troca).count() == 0
