from datetime import UTC, date, datetime
from decimal import Decimal

import pytest

from nucleo.erros import ErroDeValidacao, PermissaoNegada
from nucleo.livro_razao.modelo import Lancamento, NaturezaDoLancamento
from nucleo.livro_razao.regra import saldo_de
from nucleo.personas.modelo import Papel
from nucleo.ponto_extra.modelo import PontoExtra
from nucleo.pontuacao.modelo import PontoRegular
from nucleo.recompensas_de_marco.modelo import EntregaDeRecompensa
from nucleo.recompensas_de_marco.regra import listar_entregas, registrar_entrega
from nucleo.recursos.modelo import NaturezaDoRecurso, ValorDeReferencia
from nucleo.resultados.regra import registrar_resultado
from nucleo.trilhas.modelo import FormatoDeAtividade, ModalidadeDeAtividade
from nucleo.trilhas.regra import criar_atividade
from tests.conftest import criar_aula_para_resultado

MOMENTO_DO_FATO = datetime(2026, 8, 1, 10, 0, tzinfo=UTC)


def _marcar_marco_alcancado(sessao, *, mestre, guerreiro, missao):
    atividade = criar_atividade(
        sessao,
        operador=mestre,
        missao=missao,
        titulo="Atividade de Teste",
        modalidade=ModalidadeDeAtividade.individual,
        formato=FormatoDeAtividade.presencial,
        natureza="construcao",
        producao_esperada="Produção esperada.",
    )
    aula = criar_aula_para_resultado(sessao, mestre)
    sessao.commit()
    registrar_resultado(
        sessao,
        operador=mestre,
        aula=aula,
        guerreiro_id=guerreiro.id,
        atividade=atividade,
        momento_do_fato=MOMENTO_DO_FATO,
        producao="Produção do Guerreiro(a).",
        desfecho="realizada",
    )
    sessao.commit()


@pytest.fixture
def cenario(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_valor_de_referencia,
    criar_lancamento,
    criar_vinculo_jogador,
    criar_trilha,
    criar_missao,
    criar_recompensa_de_marco,
):
    def _montar(
        *,
        quantidade=Decimal("1"),
        lastro=Decimal("10"),
        natureza=NaturezaDoRecurso.consumivel,
        marco_alcancado=True,
    ):
        admin = criar_persona(Papel.admin)
        comunidade = criar_comunidade()
        ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
        tipo = criar_tipo_de_recurso(admin, natureza=natureza)
        criar_valor_de_referencia(admin, tipo, valor_em_moedas=Decimal("1.00"))
        criar_lancamento(
            admin, tipo, ponto_de_apoio, natureza=NaturezaDoLancamento.credito, quantidade=lastro
        )

        mestre = criar_persona(Papel.mestre)
        criar_vinculo_jogador(mestre, comunidade)

        trilha = criar_trilha(mestre)
        missao = criar_missao(trilha, mestre)
        recompensa = criar_recompensa_de_marco(mestre, trilha, missao, tipo, quantidade=quantidade)

        guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)

        if marco_alcancado:
            _marcar_marco_alcancado(sessao, mestre=mestre, guerreiro=guerreiro, missao=missao)

        return {
            "admin": admin,
            "comunidade": comunidade,
            "ponto_de_apoio": ponto_de_apoio,
            "tipo": tipo,
            "mestre": mestre,
            "trilha": trilha,
            "missao": missao,
            "recompensa": recompensa,
            "guerreiro": guerreiro,
        }

    return _montar


# --- 5.2 As cinco recusas -----------------------------------------------------


def test_recompensa_de_tipo_duravel_nao_e_entregue(sessao, cenario):
    c = cenario(natureza=NaturezaDoRecurso.duravel)

    with pytest.raises(ErroDeValidacao) as excinfo:
        registrar_entrega(
            sessao,
            operador=c["mestre"],
            recompensa=c["recompensa"],
            guerreiro=c["guerreiro"],
            ponto_de_apoio=c["ponto_de_apoio"],
        )
    assert excinfo.value.campo == "recompensa_de_marco_id"
    assert sessao.query(EntregaDeRecompensa).count() == 0
    assert sessao.query(Lancamento).filter_by(natureza=NaturezaDoLancamento.debito).count() == 0


def test_lastro_insuficiente_recusa_a_entrega(sessao, cenario):
    c = cenario(lastro=Decimal("0"))

    with pytest.raises(ErroDeValidacao) as excinfo:
        registrar_entrega(
            sessao,
            operador=c["mestre"],
            recompensa=c["recompensa"],
            guerreiro=c["guerreiro"],
            ponto_de_apoio=c["ponto_de_apoio"],
        )
    assert excinfo.value.campo == "ponto_de_apoio_id"
    assert sessao.query(EntregaDeRecompensa).count() == 0


def test_quantidade_esgotada_recusa_a_entrega(sessao, cenario, criar_persona):
    c = cenario(quantidade=Decimal("1"), lastro=Decimal("10"))
    registrar_entrega(
        sessao,
        operador=c["mestre"],
        recompensa=c["recompensa"],
        guerreiro=c["guerreiro"],
        ponto_de_apoio=c["ponto_de_apoio"],
    )
    sessao.commit()

    outro_guerreiro = criar_persona(Papel.guerreiro, comunidade=c["comunidade"])
    _marcar_marco_alcancado(
        sessao, mestre=c["mestre"], guerreiro=outro_guerreiro, missao=c["missao"]
    )

    with pytest.raises(ErroDeValidacao) as excinfo:
        registrar_entrega(
            sessao,
            operador=c["mestre"],
            recompensa=c["recompensa"],
            guerreiro=outro_guerreiro,
            ponto_de_apoio=c["ponto_de_apoio"],
        )
    assert excinfo.value.campo == "recompensa_de_marco_id"
    assert sessao.query(EntregaDeRecompensa).count() == 1


def test_mestre_de_outra_comunidade_nao_entrega(
    sessao, cenario, criar_persona, criar_comunidade, criar_vinculo_jogador
):
    c = cenario()
    outra_comunidade = criar_comunidade("Outra Comunidade")
    outro_mestre = criar_persona(Papel.mestre)
    criar_vinculo_jogador(outro_mestre, outra_comunidade)

    with pytest.raises(ErroDeValidacao) as excinfo:
        registrar_entrega(
            sessao,
            operador=outro_mestre,
            recompensa=c["recompensa"],
            guerreiro=c["guerreiro"],
            ponto_de_apoio=c["ponto_de_apoio"],
        )
    assert excinfo.value.campo == "guerreiro_id"
    assert sessao.query(EntregaDeRecompensa).count() == 0


def test_marco_nao_alcancado_recusa_a_entrega(sessao, cenario):
    c = cenario(marco_alcancado=False)

    with pytest.raises(ErroDeValidacao) as excinfo:
        registrar_entrega(
            sessao,
            operador=c["mestre"],
            recompensa=c["recompensa"],
            guerreiro=c["guerreiro"],
            ponto_de_apoio=c["ponto_de_apoio"],
        )
    assert excinfo.value.campo == "guerreiro_id"
    assert sessao.query(EntregaDeRecompensa).count() == 0


def test_admin_nao_confirma_a_entrega(sessao, cenario):
    c = cenario()

    with pytest.raises(PermissaoNegada):
        registrar_entrega(
            sessao,
            operador=c["admin"],
            recompensa=c["recompensa"],
            guerreiro=c["guerreiro"],
            ponto_de_apoio=c["ponto_de_apoio"],
        )
    assert sessao.query(EntregaDeRecompensa).count() == 0


# --- 5.3 Entrega feliz ---------------------------------------------------------


def test_entrega_debita_saldo_e_nao_toca_pontos_do_guerreiro(sessao, cenario):
    c = cenario(quantidade=Decimal("2"), lastro=Decimal("10"))

    conta_extra_antes = sessao.query(PontoExtra).filter_by(guerreiro_id=c["guerreiro"].id).first()
    conta_regular_antes = (
        sessao.query(PontoRegular)
        .filter_by(guerreiro_id=c["guerreiro"].id, trilha_id=c["trilha"].id)
        .first()
    )
    saldo_disponivel_antes = conta_extra_antes.saldo_disponivel if conta_extra_antes else 0
    acumulado_antes = conta_extra_antes.acumulado if conta_extra_antes else 0
    regular_antes = conta_regular_antes.total if conta_regular_antes else 0

    entrega = registrar_entrega(
        sessao,
        operador=c["mestre"],
        recompensa=c["recompensa"],
        guerreiro=c["guerreiro"],
        ponto_de_apoio=c["ponto_de_apoio"],
    )
    sessao.commit()

    assert entrega.recompensa_de_marco_id == c["recompensa"].id
    assert entrega.guerreiro_id == c["guerreiro"].id
    assert entrega.ponto_de_apoio_id == c["ponto_de_apoio"].id
    assert entrega.autor_id == c["mestre"].id
    assert entrega.papel_do_autor == Papel.mestre.value

    lancamento = sessao.get(Lancamento, entrega.lancamento_id)
    assert lancamento.natureza == NaturezaDoLancamento.debito
    assert lancamento.aula_id is None
    assert lancamento.quantidade == Decimal("2")
    assert lancamento.valor_em_moedas == Decimal("2.00")

    saldo_do_tipo = saldo_de(
        sessao, tipo_de_recurso_id=c["tipo"].id, ponto_de_apoio_id=c["ponto_de_apoio"].id
    )
    assert saldo_do_tipo == Decimal("8")

    # PRD-07 §12: a entrega em si nunca toca o livro de pontos do
    # Guerreiro(a) — nem no ato, nem em qualquer perda ou dano posterior do
    # que foi entregue, porque não existe caminho de código que ligue a
    # entrega ao ponto regular ou ao ponto extra.
    conta_extra_depois = sessao.query(PontoExtra).filter_by(guerreiro_id=c["guerreiro"].id).first()
    conta_regular_depois = (
        sessao.query(PontoRegular)
        .filter_by(guerreiro_id=c["guerreiro"].id, trilha_id=c["trilha"].id)
        .first()
    )
    saldo_disponivel_depois = conta_extra_depois.saldo_disponivel if conta_extra_depois else 0
    acumulado_depois = conta_extra_depois.acumulado if conta_extra_depois else 0
    regular_depois = conta_regular_depois.total if conta_regular_depois else 0

    assert saldo_disponivel_depois == saldo_disponivel_antes
    assert acumulado_depois == acumulado_antes
    assert regular_depois == regular_antes


# --- 5.4 Atomicidade e histórico -----------------------------------------------


def test_falha_no_lancamento_desfaz_a_entrega(sessao, cenario):
    c = cenario()
    sessao.query(ValorDeReferencia).filter_by(tipo_de_recurso_id=c["tipo"].id).update(
        {"vigencia_fim": date(2026, 1, 2)}
    )
    sessao.commit()

    with pytest.raises(ErroDeValidacao):
        registrar_entrega(
            sessao,
            operador=c["mestre"],
            recompensa=c["recompensa"],
            guerreiro=c["guerreiro"],
            ponto_de_apoio=c["ponto_de_apoio"],
        )
    sessao.rollback()

    assert sessao.query(EntregaDeRecompensa).count() == 0
    assert sessao.query(Lancamento).filter_by(natureza=NaturezaDoLancamento.debito).count() == 0


def test_duas_entregas_da_mesma_recompensa_convivem(sessao, cenario, criar_persona):
    c = cenario(quantidade=Decimal("5"), lastro=Decimal("10"))
    outro_guerreiro = criar_persona(Papel.guerreiro, comunidade=c["comunidade"])
    _marcar_marco_alcancado(
        sessao, mestre=c["mestre"], guerreiro=outro_guerreiro, missao=c["missao"]
    )

    entrega1 = registrar_entrega(
        sessao,
        operador=c["mestre"],
        recompensa=c["recompensa"],
        guerreiro=c["guerreiro"],
        ponto_de_apoio=c["ponto_de_apoio"],
    )
    sessao.commit()
    entrega2 = registrar_entrega(
        sessao,
        operador=c["mestre"],
        recompensa=c["recompensa"],
        guerreiro=outro_guerreiro,
        ponto_de_apoio=c["ponto_de_apoio"],
    )
    sessao.commit()

    assert entrega1.id != entrega2.id
    assert (
        sessao.query(EntregaDeRecompensa)
        .filter_by(recompensa_de_marco_id=c["recompensa"].id)
        .count()
        == 2
    )


def test_guerreiro_le_apenas_as_proprias_entregas(sessao, cenario, criar_persona):
    c = cenario(quantidade=Decimal("5"), lastro=Decimal("10"))
    outro_guerreiro = criar_persona(Papel.guerreiro, comunidade=c["comunidade"])
    _marcar_marco_alcancado(
        sessao, mestre=c["mestre"], guerreiro=outro_guerreiro, missao=c["missao"]
    )

    entrega_propria = registrar_entrega(
        sessao,
        operador=c["mestre"],
        recompensa=c["recompensa"],
        guerreiro=c["guerreiro"],
        ponto_de_apoio=c["ponto_de_apoio"],
    )
    entrega_de_outro = registrar_entrega(
        sessao,
        operador=c["mestre"],
        recompensa=c["recompensa"],
        guerreiro=outro_guerreiro,
        ponto_de_apoio=c["ponto_de_apoio"],
    )
    sessao.commit()

    entregas = listar_entregas(sessao, operador=c["guerreiro"])

    assert [e.id for e in entregas] == [entrega_propria.id]
    assert entrega_de_outro.id not in [e.id for e in entregas]


def test_mestre_le_entregas_da_sua_comunidade(sessao, cenario):
    c1 = cenario()
    c2 = cenario()

    entrega1 = registrar_entrega(
        sessao,
        operador=c1["mestre"],
        recompensa=c1["recompensa"],
        guerreiro=c1["guerreiro"],
        ponto_de_apoio=c1["ponto_de_apoio"],
    )
    registrar_entrega(
        sessao,
        operador=c2["mestre"],
        recompensa=c2["recompensa"],
        guerreiro=c2["guerreiro"],
        ponto_de_apoio=c2["ponto_de_apoio"],
    )
    sessao.commit()

    entregas_do_mestre1 = listar_entregas(sessao, operador=c1["mestre"])

    assert [e.id for e in entregas_do_mestre1] == [entrega1.id]


def test_admin_le_entregas_da_comunidade_vinculada(sessao, cenario, criar_vinculo_jogador):
    c1 = cenario()
    c2 = cenario()
    criar_vinculo_jogador(c1["admin"], c1["comunidade"])

    entrega1 = registrar_entrega(
        sessao,
        operador=c1["mestre"],
        recompensa=c1["recompensa"],
        guerreiro=c1["guerreiro"],
        ponto_de_apoio=c1["ponto_de_apoio"],
    )
    registrar_entrega(
        sessao,
        operador=c2["mestre"],
        recompensa=c2["recompensa"],
        guerreiro=c2["guerreiro"],
        ponto_de_apoio=c2["ponto_de_apoio"],
    )
    sessao.commit()

    entregas_do_admin = listar_entregas(sessao, operador=c1["admin"])

    assert [e.id for e in entregas_do_admin] == [entrega1.id]


def test_leitura_por_rota_nao_traz_moedas_nem_reais(
    sessao, cliente, criar_chave, criar_sessao_de_teste, cenario
):
    c = cenario()
    registrar_entrega(
        sessao,
        operador=c["mestre"],
        recompensa=c["recompensa"],
        guerreiro=c["guerreiro"],
        ponto_de_apoio=c["ponto_de_apoio"],
    )
    sessao.commit()

    chave, _ = criar_chave()
    token, _ = criar_sessao_de_teste(c["guerreiro"])

    resposta = cliente.get(
        "/v1/entregas",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert len(corpo) == 1
    for item in corpo:
        assert "valor_em_moedas" not in item
        assert "valor_em_reais" not in item
        assert "recompensa_de_marco_id" in item
        assert "missao_id" in item
        assert "trilha_id" in item
        assert item["tipo_de_recurso_id"] == str(c["tipo"].id)
        assert item["quantidade"] == "1.00"
        assert "lancamento_id" in item


def test_leitura_por_rota_traz_tipo_de_recurso_quantidade_e_lancamento_para_o_admin(
    sessao, cliente, criar_chave, criar_sessao_de_teste, cenario, criar_vinculo_jogador
):
    c = cenario()
    criar_vinculo_jogador(c["admin"], c["comunidade"])
    entrega = registrar_entrega(
        sessao,
        operador=c["mestre"],
        recompensa=c["recompensa"],
        guerreiro=c["guerreiro"],
        ponto_de_apoio=c["ponto_de_apoio"],
    )
    sessao.commit()

    chave, _ = criar_chave()
    token, _ = criar_sessao_de_teste(c["admin"])

    resposta = cliente.get(
        "/v1/entregas",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert len(corpo) == 1
    item = corpo[0]
    assert item["tipo_de_recurso_id"] == str(c["tipo"].id)
    assert item["lancamento_id"] == str(entrega.lancamento_id)
    for chave_do_item in item:
        assert "moeda" not in chave_do_item and "real" not in chave_do_item
