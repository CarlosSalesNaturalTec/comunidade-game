from datetime import date, timedelta
from decimal import Decimal

import pytest

from nucleo.aportes.modelo import FormaDeAporte, OrigemDaEscolhaDoAporte
from nucleo.aportes.regra import declarar_aporte, registrar_aporte
from nucleo.armazenamento.disco import ArmazenamentoEmDisco
from nucleo.aulas.modelo import SituacaoDaAula
from nucleo.erros import MissaoDoApoiadorFechada
from nucleo.missoes_do_apoiador.modelo import NivelDeNecessidade, SituacaoDaMissao
from nucleo.missoes_do_apoiador.regra import derivar_missoes, publicar_missao
from nucleo.personas.modelo import Papel
from nucleo.poder_sustentador.regra import poder_sustentador_de
from nucleo.selos_do_apoiador.modelo import FamiliaDeSelo, SeloDoApoiador
from nucleo.tempo import agora


@pytest.fixture
def cenario(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_valor_de_referencia,
    criar_aula,
    criar_recurso_declarado_da_aula,
):
    admin = criar_persona(Papel.admin)
    apoiador_um = criar_persona(Papel.apoiador)
    apoiador_dois = criar_persona(Papel.apoiador)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin, nome="Lanche")
    criar_valor_de_referencia(admin, tipo, valor_em_moedas=Decimal("1.00"))
    aula = criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)
    criar_recurso_declarado_da_aula(aula, tipo, quantidade=Decimal("10.00"))
    aula.situacao = SituacaoDaAula.pendente_de_lastro
    sessao.commit()

    missao = publicar_missao(
        sessao,
        operador=admin,
        aula=aula,
        tipo=tipo,
        nivel_de_necessidade=NivelDeNecessidade.acontecer,
        titulo="O lanche do encontro",
        o_que_se_pede="Um lanche para vinte crianças",
        quantidade=Decimal("10.00"),
        prazo=agora().date() + timedelta(days=30),
        selo_nome="Lanche garantido",
        selo_familia=FamiliaDeSelo.frente,
    )
    sessao.commit()

    return admin, apoiador_um, apoiador_dois, ponto_de_apoio, tipo, missao


def _armazenamento(tmp_path):
    return ArmazenamentoEmDisco(str(tmp_path), str(tmp_path / "sessoes"))


def _declarar(sessao, apoiador, missao, tmp_path, valor=Decimal("50.00")):
    return declarar_aporte(
        sessao,
        provedor=apoiador,
        valor_declarado=valor,
        forma=FormaDeAporte.financeira,
        origem_da_escolha=OrigemDaEscolhaDoAporte.missao,
        missao=missao,
        comprovante_conteudo=b"conteudo",
        comprovante_nome_original="comprovante.pdf",
        comprovante_tipo="application/pdf",
        armazenamento=_armazenamento(tmp_path),
    )


def _falta_de(sessao, missao_id):
    derivada = next(d for d in derivar_missoes(sessao) if d.missao.id == missao_id)
    return derivada.falta


def test_declaracao_pendente_nao_abate(sessao, cenario, tmp_path):
    admin, apoiador_um, apoiador_dois, ponto_de_apoio, tipo, missao = cenario

    _declarar(sessao, apoiador_um, missao, tmp_path)
    sessao.commit()

    assert _falta_de(sessao, missao.id) == Decimal("10.00")


def test_homologacao_parcial_abate_e_nao_credita_selo(sessao, cenario, tmp_path):
    admin, apoiador_um, apoiador_dois, ponto_de_apoio, tipo, missao = cenario

    declaracao = _declarar(sessao, apoiador_um, missao, tmp_path)
    sessao.commit()

    registrar_aporte(
        sessao,
        operador=admin,
        provedor=apoiador_um,
        tipo=tipo,
        quantidade=Decimal("5.00"),
        ponto_de_apoio=ponto_de_apoio,
        data_do_aporte=date(2026, 6, 1),
        forma=FormaDeAporte.financeira,
        aporte_declarado=declaracao,
    )
    sessao.commit()
    sessao.refresh(missao)

    assert missao.situacao == SituacaoDaMissao.aberta
    assert _falta_de(sessao, missao.id) == Decimal("5.00")
    assert sessao.query(SeloDoApoiador).count() == 0


def test_homologacao_que_fecha_conclui_e_credita_selo_e_mutirao(sessao, cenario, tmp_path):
    admin, apoiador_um, apoiador_dois, ponto_de_apoio, tipo, missao = cenario

    declaracao_um = _declarar(sessao, apoiador_um, missao, tmp_path)
    declaracao_dois = _declarar(sessao, apoiador_dois, missao, tmp_path)
    sessao.commit()

    registrar_aporte(
        sessao,
        operador=admin,
        provedor=apoiador_um,
        tipo=tipo,
        quantidade=Decimal("5.00"),
        ponto_de_apoio=ponto_de_apoio,
        data_do_aporte=date(2026, 6, 1),
        forma=FormaDeAporte.financeira,
        aporte_declarado=declaracao_um,
    )
    sessao.commit()
    sessao.refresh(missao)
    assert missao.situacao == SituacaoDaMissao.aberta

    registrar_aporte(
        sessao,
        operador=admin,
        provedor=apoiador_dois,
        tipo=tipo,
        quantidade=Decimal("5.00"),
        ponto_de_apoio=ponto_de_apoio,
        data_do_aporte=date(2026, 6, 1),
        forma=FormaDeAporte.financeira,
        aporte_declarado=declaracao_dois,
    )
    sessao.commit()
    sessao.refresh(missao)

    assert missao.situacao == SituacaoDaMissao.concluida
    assert poder_sustentador_de(sessao, provedor_id=apoiador_um.id) == Decimal("5.00")
    assert poder_sustentador_de(sessao, provedor_id=apoiador_dois.id) == Decimal("5.00")

    selos_um = sessao.query(SeloDoApoiador).filter_by(apoiador_id=apoiador_um.id).all()
    selos_dois = sessao.query(SeloDoApoiador).filter_by(apoiador_id=apoiador_dois.id).all()
    assert {s.selo_nome for s in selos_um} == {"Lanche garantido", "Mutirão"}
    assert {s.selo_nome for s in selos_dois} == {"Lanche garantido", "Mutirão"}
    mutirao_um = next(s for s in selos_um if s.selo_nome == "Mutirão")
    assert mutirao_um.familia == FamiliaDeSelo.ato


def test_participante_unico_nao_recebe_mutirao(sessao, cenario, tmp_path):
    admin, apoiador_um, apoiador_dois, ponto_de_apoio, tipo, missao = cenario

    declaracao = _declarar(sessao, apoiador_um, missao, tmp_path)
    sessao.commit()

    registrar_aporte(
        sessao,
        operador=admin,
        provedor=apoiador_um,
        tipo=tipo,
        quantidade=Decimal("10.00"),
        ponto_de_apoio=ponto_de_apoio,
        data_do_aporte=date(2026, 6, 1),
        forma=FormaDeAporte.financeira,
        aporte_declarado=declaracao,
    )
    sessao.commit()
    sessao.refresh(missao)

    assert missao.situacao == SituacaoDaMissao.concluida
    selos = sessao.query(SeloDoApoiador).filter_by(apoiador_id=apoiador_um.id).all()
    assert {s.selo_nome for s in selos} == {"Lanche garantido"}


def test_missao_concluida_recusa_nova_declaracao_com_409(sessao, cenario, tmp_path):
    admin, apoiador_um, apoiador_dois, ponto_de_apoio, tipo, missao = cenario
    declaracao = _declarar(sessao, apoiador_um, missao, tmp_path)
    sessao.commit()
    registrar_aporte(
        sessao,
        operador=admin,
        provedor=apoiador_um,
        tipo=tipo,
        quantidade=Decimal("10.00"),
        ponto_de_apoio=ponto_de_apoio,
        data_do_aporte=date(2026, 6, 1),
        forma=FormaDeAporte.financeira,
        aporte_declarado=declaracao,
    )
    sessao.commit()
    sessao.refresh(missao)
    assert missao.situacao == SituacaoDaMissao.concluida

    with pytest.raises(MissaoDoApoiadorFechada):
        _declarar(sessao, apoiador_dois, missao, tmp_path)


def test_missao_vencida_recusa_declaracao_com_409(sessao, cenario, tmp_path):
    admin, apoiador_um, apoiador_dois, ponto_de_apoio, tipo, missao = cenario
    missao.prazo = agora().date() - timedelta(days=1)
    sessao.commit()

    with pytest.raises(MissaoDoApoiadorFechada):
        _declarar(sessao, apoiador_um, missao, tmp_path)


def test_missao_inexistente_e_409(sessao, cenario, tmp_path):
    admin, apoiador_um, apoiador_dois, ponto_de_apoio, tipo, missao = cenario

    with pytest.raises(MissaoDoApoiadorFechada):
        declarar_aporte(
            sessao,
            provedor=apoiador_um,
            valor_declarado=Decimal("50.00"),
            forma=FormaDeAporte.financeira,
            origem_da_escolha=OrigemDaEscolhaDoAporte.missao,
            missao=None,
            comprovante_conteudo=b"conteudo",
            comprovante_nome_original="comprovante.pdf",
            comprovante_tipo="application/pdf",
            armazenamento=_armazenamento(tmp_path),
        )
