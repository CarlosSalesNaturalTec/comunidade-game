from datetime import date
from decimal import Decimal

import pytest

from nucleo.aportes.modelo import Aporte, FormaDeAporte, SituacaoDeRessarcimento
from nucleo.armazenamento.disco import ArmazenamentoEmDisco
from nucleo.erros import ErroDeValidacao, PermissaoNegada
from nucleo.livro_razao.modelo import DestinacaoDoAporte, NaturezaDoLancamento
from nucleo.personas.modelo import Papel
from nucleo.recursos.modelo import NaturezaDoRecurso
from nucleo.ressarcimentos.modelo import Ressarcimento
from nucleo.ressarcimentos.regra import registrar_ressarcimento


@pytest.fixture
def cenario(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_lancamento,
    criar_aporte,
):
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    apoiador = criar_persona(Papel.apoiador)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin, nome="Lanche", natureza=NaturezaDoRecurso.consumivel)

    lancamento_da_absorcao = criar_lancamento(
        admin, tipo, ponto_de_apoio, natureza=NaturezaDoLancamento.credito
    )
    absorcao = criar_aporte(
        admin,
        mestre,
        tipo,
        ponto_de_apoio,
        lancamento_da_absorcao,
        valor_de_origem=Decimal("10.00"),
        forma=FormaDeAporte.absorcao,
        ressarcivel=True,
        situacao_de_ressarcimento=SituacaoDeRessarcimento.em_aberto,
    )

    lancamento_da_receita = criar_lancamento(
        admin, tipo, ponto_de_apoio, natureza=NaturezaDoLancamento.credito
    )
    receita = criar_aporte(
        admin,
        apoiador,
        tipo,
        ponto_de_apoio,
        lancamento_da_receita,
        valor_de_origem=Decimal("100.00"),
        forma=FormaDeAporte.financeira,
        destinacao=DestinacaoDoAporte.ressarcimento,
    )
    return admin, mestre, apoiador, ponto_de_apoio, tipo, absorcao, receita


def test_admin_ressarce_uma_absorcao_com_comprovante(sessao, cenario, tmp_path):
    admin, _mestre, _apoiador, _ponto_de_apoio, _tipo, absorcao, receita = cenario
    armazenamento = ArmazenamentoEmDisco(str(tmp_path))

    ressarcimento = registrar_ressarcimento(
        sessao,
        operador=admin,
        aporte=absorcao,
        receita_destinada=receita,
        data=date(2026, 7, 1),
        comprovante_conteudo=b"comprovante",
        comprovante_nome_original="comprovante.pdf",
        comprovante_tipo="application/pdf",
        armazenamento=armazenamento,
    )
    sessao.commit()

    assert ressarcimento.aporte_id == absorcao.id
    assert ressarcimento.receita_destinada_id == receita.id
    assert ressarcimento.valor_em_reais == Decimal("10.00")
    assert ressarcimento.admin_pagador_id == admin.id
    assert armazenamento.ler(referencia=ressarcimento.comprovante_referencia) == b"comprovante"


def test_ressarcimento_sem_comprovante_e_recusado(sessao, cenario):
    admin, _mestre, _apoiador, _ponto_de_apoio, _tipo, absorcao, receita = cenario

    with pytest.raises(ErroDeValidacao) as excinfo:
        registrar_ressarcimento(
            sessao,
            operador=admin,
            aporte=absorcao,
            receita_destinada=receita,
            data=date(2026, 7, 1),
            comprovante_conteudo=None,
            comprovante_nome_original=None,
            comprovante_tipo=None,
            armazenamento=None,
        )
    assert excinfo.value.campo == "comprovante"
    assert sessao.query(Ressarcimento).count() == 0


def test_aporte_nao_ressarcivel_nao_se_ressarce(
    sessao, cenario, criar_lancamento, criar_aporte, tmp_path
):
    admin, _mestre, apoiador, ponto_de_apoio, tipo, _absorcao, receita = cenario
    armazenamento = ArmazenamentoEmDisco(str(tmp_path))
    lancamento = criar_lancamento(admin, tipo, ponto_de_apoio)
    aporte_da_gestao = criar_aporte(
        admin,
        apoiador,
        tipo,
        ponto_de_apoio,
        lancamento,
        forma=FormaDeAporte.material,
        ressarcivel=False,
        situacao_de_ressarcimento=SituacaoDeRessarcimento.nao_se_aplica,
    )

    with pytest.raises(ErroDeValidacao) as excinfo:
        registrar_ressarcimento(
            sessao,
            operador=admin,
            aporte=aporte_da_gestao,
            receita_destinada=receita,
            data=date(2026, 7, 1),
            comprovante_conteudo=b"comprovante",
            comprovante_nome_original="c.pdf",
            comprovante_tipo="application/pdf",
            armazenamento=armazenamento,
        )
    assert excinfo.value.campo == "aporte_id"


def test_aporte_ja_ressarcido_nao_se_ressarce_de_novo(sessao, cenario, tmp_path):
    admin, _mestre, _apoiador, _ponto_de_apoio, _tipo, absorcao, receita = cenario
    armazenamento = ArmazenamentoEmDisco(str(tmp_path))
    absorcao.situacao_de_ressarcimento = SituacaoDeRessarcimento.ressarcido
    sessao.commit()

    with pytest.raises(ErroDeValidacao) as excinfo:
        registrar_ressarcimento(
            sessao,
            operador=admin,
            aporte=absorcao,
            receita_destinada=receita,
            data=date(2026, 7, 1),
            comprovante_conteudo=b"comprovante",
            comprovante_nome_original="c.pdf",
            comprovante_tipo="application/pdf",
            armazenamento=armazenamento,
        )
    assert excinfo.value.campo == "aporte_id"


def test_receita_de_destinacao_lastro_nao_financia_ressarcimento(
    sessao, cenario, criar_lancamento, criar_aporte, tmp_path
):
    admin, _mestre, apoiador, ponto_de_apoio, tipo, absorcao, _receita = cenario
    armazenamento = ArmazenamentoEmDisco(str(tmp_path))
    lancamento = criar_lancamento(admin, tipo, ponto_de_apoio)
    aporte_de_lastro = criar_aporte(
        admin,
        apoiador,
        tipo,
        ponto_de_apoio,
        lancamento,
        valor_de_origem=Decimal("100.00"),
        forma=FormaDeAporte.financeira,
        destinacao=DestinacaoDoAporte.lastro,
    )

    with pytest.raises(ErroDeValidacao) as excinfo:
        registrar_ressarcimento(
            sessao,
            operador=admin,
            aporte=absorcao,
            receita_destinada=aporte_de_lastro,
            data=date(2026, 7, 1),
            comprovante_conteudo=b"comprovante",
            comprovante_nome_original="c.pdf",
            comprovante_tipo="application/pdf",
            armazenamento=armazenamento,
        )
    assert excinfo.value.campo == "receita_destinada_id"


def test_valor_acima_do_que_a_receita_cobre_e_recusado(
    sessao, cenario, criar_lancamento, criar_aporte, tmp_path
):
    admin, mestre, _apoiador, ponto_de_apoio, tipo, _absorcao, receita = cenario
    armazenamento = ArmazenamentoEmDisco(str(tmp_path))
    receita.valor_de_origem = Decimal("5.00")
    sessao.commit()

    lancamento = criar_lancamento(admin, tipo, ponto_de_apoio)
    absorcao_cara = criar_aporte(
        admin,
        mestre,
        tipo,
        ponto_de_apoio,
        lancamento,
        valor_de_origem=Decimal("10.00"),
        forma=FormaDeAporte.absorcao,
        ressarcivel=True,
        situacao_de_ressarcimento=SituacaoDeRessarcimento.em_aberto,
    )

    with pytest.raises(ErroDeValidacao) as excinfo:
        registrar_ressarcimento(
            sessao,
            operador=admin,
            aporte=absorcao_cara,
            receita_destinada=receita,
            data=date(2026, 7, 1),
            comprovante_conteudo=b"comprovante",
            comprovante_nome_original="c.pdf",
            comprovante_tipo="application/pdf",
            armazenamento=armazenamento,
        )
    assert excinfo.value.campo == "receita_destinada_id"
    assert sessao.query(Ressarcimento).count() == 0
    sessao.refresh(absorcao_cara)
    assert absorcao_cara.situacao_de_ressarcimento == SituacaoDeRessarcimento.em_aberto


def test_nenhum_campo_da_entidade_guarda_dado_bancario():
    nomes_das_colunas = {coluna.name for coluna in Ressarcimento.__table__.columns}
    proibidos = {"chave_pix", "banco", "agencia", "conta"}
    assert nomes_das_colunas.isdisjoint(proibidos)


def test_mestre_nao_registra_ressarcimento(sessao, cenario, tmp_path):
    _admin, mestre, _apoiador, _ponto_de_apoio, _tipo, absorcao, receita = cenario
    armazenamento = ArmazenamentoEmDisco(str(tmp_path))

    with pytest.raises(PermissaoNegada):
        registrar_ressarcimento(
            sessao,
            operador=mestre,
            aporte=absorcao,
            receita_destinada=receita,
            data=date(2026, 7, 1),
            comprovante_conteudo=b"comprovante",
            comprovante_nome_original="c.pdf",
            comprovante_tipo="application/pdf",
            armazenamento=armazenamento,
        )
    assert sessao.query(Ressarcimento).count() == 0


def test_mesmo_aporte_nao_tem_dois_ressarcimentos_no_banco(sessao, cenario, tmp_path):
    """A unicidade de `aporte_id` é reforçada também pela restrição do
    banco, não só pela checagem de situação (`RF-07-22`)."""
    admin, _mestre, _apoiador, _ponto_de_apoio, _tipo, absorcao, receita = cenario
    armazenamento = ArmazenamentoEmDisco(str(tmp_path))

    registrar_ressarcimento(
        sessao,
        operador=admin,
        aporte=absorcao,
        receita_destinada=receita,
        data=date(2026, 7, 1),
        comprovante_conteudo=b"comprovante",
        comprovante_nome_original="c.pdf",
        comprovante_tipo="application/pdf",
        armazenamento=armazenamento,
    )
    sessao.commit()

    aporte_persistido = sessao.get(Aporte, absorcao.id)
    assert aporte_persistido.situacao_de_ressarcimento == SituacaoDeRessarcimento.ressarcido
