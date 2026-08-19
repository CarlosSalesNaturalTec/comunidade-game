import pytest
from sqlalchemy import func, text
from sqlalchemy.exc import DBAPIError

from nucleo.erros import ErroDeValidacao, FichaDeVidaImutavel, PermissaoNegada
from nucleo.livro_razao.modelo import Lancamento
from nucleo.patrimonio.modelo import AnotacaoDaFichaDeVida, TeorDaAnotacao
from nucleo.patrimonio.regra import anotar_ficha_de_vida, listar_ficha_de_vida
from nucleo.personas.modelo import Papel
from nucleo.ponto_extra.modelo import PontoExtra


@pytest.fixture
def cenario(sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio, criar_item_patrimonial):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    item = criar_item_patrimonial(admin, ponto_de_apoio)
    return admin, item


def test_anotacao_entra_na_ficha_e_nao_sai(sessao, cenario, criar_persona):
    admin, item = cenario
    mestre = criar_persona(Papel.mestre, criada_por=admin)

    anotacao = anotar_ficha_de_vida(
        sessao,
        operador=mestre,
        item=item,
        teor=TeorDaAnotacao.cuidado.value,
        estado_de_conservacao="bom",
    )
    sessao.commit()

    assert anotacao.autor_id == mestre.id
    assert anotacao.teor == TeorDaAnotacao.cuidado
    sessao.refresh(item)
    assert item.estado_de_conservacao == "bom"


def test_guerreiro_nao_anota_na_ficha_de_vida(sessao, cenario, criar_persona):
    admin, item = cenario
    guerreiro = criar_persona(Papel.guerreiro)

    with pytest.raises(PermissaoNegada):
        anotar_ficha_de_vida(
            sessao,
            operador=guerreiro,
            item=item,
            teor=TeorDaAnotacao.cuidado.value,
            estado_de_conservacao="bom",
        )
    assert sessao.query(AnotacaoDaFichaDeVida).count() == 0


def test_ficha_de_vida_e_lida_na_ordem_do_tempo(sessao, cenario):
    admin, item = cenario
    primeira = anotar_ficha_de_vida(
        sessao,
        operador=admin,
        item=item,
        teor=TeorDaAnotacao.cuidado.value,
        estado_de_conservacao="bom",
    )
    sessao.commit()
    segunda = anotar_ficha_de_vida(
        sessao,
        operador=admin,
        item=item,
        teor=TeorDaAnotacao.dano.value,
        estado_de_conservacao="regular",
    )
    sessao.commit()

    ficha = listar_ficha_de_vida(sessao, item_patrimonial_id=item.id)

    assert [anotacao.id for anotacao in ficha] == [primeira.id, segunda.id]


def test_update_e_delete_sao_recusados_no_orm(sessao, cenario):
    admin, item = cenario
    anotacao = anotar_ficha_de_vida(
        sessao,
        operador=admin,
        item=item,
        teor=TeorDaAnotacao.cuidado.value,
        estado_de_conservacao="bom",
    )
    sessao.commit()

    anotacao.estado_de_conservacao = "ruim"
    with pytest.raises(FichaDeVidaImutavel):
        sessao.commit()
    sessao.rollback()

    intacta = sessao.get(AnotacaoDaFichaDeVida, anotacao.id)
    assert intacta.estado_de_conservacao == "bom"

    sessao.delete(intacta)
    with pytest.raises(FichaDeVidaImutavel):
        sessao.commit()
    sessao.rollback()

    assert sessao.get(AnotacaoDaFichaDeVida, anotacao.id) is not None


def test_update_e_delete_sao_recusados_direto_no_banco(conexao, sessao, cenario):
    admin, item = cenario
    anotacao = anotar_ficha_de_vida(
        sessao,
        operador=admin,
        item=item,
        teor=TeorDaAnotacao.cuidado.value,
        estado_de_conservacao="bom",
    )
    sessao.commit()

    with pytest.raises(DBAPIError), conexao.begin_nested():
        conexao.execute(
            text(
                "UPDATE anotacao_da_ficha_de_vida SET estado_de_conservacao = 'ruim' WHERE id = :id"
            ),
            {"id": str(anotacao.id)},
        )

    with pytest.raises(DBAPIError), conexao.begin_nested():
        conexao.execute(
            text("DELETE FROM anotacao_da_ficha_de_vida WHERE id = :id"), {"id": str(anotacao.id)}
        )

    ainda_existe = sessao.get(AnotacaoDaFichaDeVida, anotacao.id)
    assert ainda_existe is not None
    assert ainda_existe.estado_de_conservacao == "bom"


def test_exemplar_dado_como_perdido_nao_gera_debito(sessao, cenario):
    admin, item = cenario
    lancamentos_antes = sessao.query(func.count(Lancamento.id)).scalar()
    pontos_extras_antes = sessao.query(func.count(PontoExtra.id)).scalar()

    anotar_ficha_de_vida(
        sessao,
        operador=admin,
        item=item,
        teor=TeorDaAnotacao.perda.value,
        estado_de_conservacao="perdido",
    )
    sessao.commit()

    assert sessao.query(func.count(Lancamento.id)).scalar() == lancamentos_antes
    assert sessao.query(func.count(PontoExtra.id)).scalar() == pontos_extras_antes


def test_anotacao_de_dano_nao_identifica_culpado(sessao, cenario):
    admin, item = cenario

    anotacao = anotar_ficha_de_vida(
        sessao,
        operador=admin,
        item=item,
        teor=TeorDaAnotacao.dano.value,
        estado_de_conservacao="danificado",
    )
    sessao.commit()

    assert anotacao.teor == TeorDaAnotacao.dano


def test_teor_invalido_e_recusado(sessao, cenario):
    admin, item = cenario

    with pytest.raises(ErroDeValidacao) as excinfo:
        anotar_ficha_de_vida(
            sessao, operador=admin, item=item, teor="extraviado", estado_de_conservacao="bom"
        )
    assert excinfo.value.campo == "teor"
    assert sessao.query(AnotacaoDaFichaDeVida).count() == 0
