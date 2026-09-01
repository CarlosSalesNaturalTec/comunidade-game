from datetime import date
from decimal import Decimal

import pytest

from nucleo.aportes.modelo import (
    Aporte,
    AporteDeclarado,
    FormaDeAporte,
    OrigemDaEscolhaDoAporte,
    OrigemDoRegistro,
    SituacaoDaDeclaracao,
)
from nucleo.aportes.regra import declarar_aporte, recusar_declaracao_de_aporte, registrar_aporte
from nucleo.armazenamento.disco import ArmazenamentoEmDisco
from nucleo.aulas.modelo import SituacaoDaAula
from nucleo.erros import DeclaracaoDeAporteJaResolvida, ErroDeValidacao, PermissaoNegada
from nucleo.necessidades.regra import consultar_necessidades_publicas
from nucleo.personas.modelo import Papel
from nucleo.poder_sustentador.regra import poder_sustentador_de
from nucleo.recursos.modelo import NaturezaDoRecurso


@pytest.fixture
def cenario(sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio, criar_tipo_de_recurso):
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin, nome="Lanche", natureza=NaturezaDoRecurso.consumivel)
    return admin, apoiador, comunidade, ponto_de_apoio, tipo


def _armazenamento(tmp_path):
    return ArmazenamentoEmDisco(str(tmp_path), str(tmp_path / "sessoes"))


def test_declaracao_nasce_pendente_sem_lancamento_nem_poder_sustentador(sessao, cenario, tmp_path):
    admin, apoiador, comunidade, ponto_de_apoio, tipo = cenario

    declaracao = declarar_aporte(
        sessao,
        provedor=apoiador,
        valor_declarado=Decimal("100.00"),
        forma=FormaDeAporte.financeira,
        origem_da_escolha=OrigemDaEscolhaDoAporte.valor_livre,
        comprovante_conteudo=b"conteudo",
        comprovante_nome_original="comprovante.pdf",
        comprovante_tipo="application/pdf",
        armazenamento=_armazenamento(tmp_path),
    )
    sessao.commit()

    assert declaracao.situacao == SituacaoDaDeclaracao.pendente
    assert sessao.query(Aporte).count() == 0
    assert poder_sustentador_de(sessao, provedor_id=apoiador.id) == Decimal("0")


def test_declaracao_por_necessidade_nao_abate_o_que_falta(
    sessao,
    cenario,
    tmp_path,
    criar_aula,
    criar_recurso_declarado_da_aula,
):
    admin, apoiador, comunidade, ponto_de_apoio, tipo = cenario
    aula = criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)
    criar_recurso_declarado_da_aula(aula, tipo, quantidade=Decimal("2.00"))
    aula.situacao = SituacaoDaAula.pendente_de_lastro
    sessao.commit()

    antes = consultar_necessidades_publicas(sessao)
    assert antes[0].quantidade_faltante == Decimal("2.00")

    declarar_aporte(
        sessao,
        provedor=apoiador,
        valor_declarado=Decimal("50.00"),
        forma=FormaDeAporte.financeira,
        origem_da_escolha=OrigemDaEscolhaDoAporte.necessidade,
        aula=aula,
        tipo=tipo,
        comprovante_conteudo=b"conteudo",
        comprovante_nome_original="comprovante.pdf",
        comprovante_tipo="application/pdf",
        armazenamento=_armazenamento(tmp_path),
    )
    sessao.commit()

    depois = consultar_necessidades_publicas(sessao)
    assert depois[0].quantidade_faltante == Decimal("2.00")


def test_sem_comprovante_a_declaracao_e_recusada_com_422(sessao, cenario):
    admin, apoiador, comunidade, ponto_de_apoio, tipo = cenario

    with pytest.raises(ErroDeValidacao) as excinfo:
        declarar_aporte(
            sessao,
            provedor=apoiador,
            valor_declarado=Decimal("50.00"),
            forma=FormaDeAporte.financeira,
            origem_da_escolha=OrigemDaEscolhaDoAporte.valor_livre,
        )
    assert excinfo.value.campo == "comprovante"
    assert sessao.query(AporteDeclarado).count() == 0


def test_comprovante_em_formato_nao_aceito_e_recusado_com_422(sessao, cenario, tmp_path):
    admin, apoiador, comunidade, ponto_de_apoio, tipo = cenario

    with pytest.raises(ErroDeValidacao) as excinfo:
        declarar_aporte(
            sessao,
            provedor=apoiador,
            valor_declarado=Decimal("50.00"),
            forma=FormaDeAporte.financeira,
            origem_da_escolha=OrigemDaEscolhaDoAporte.valor_livre,
            comprovante_conteudo=b"conteudo",
            comprovante_nome_original="comprovante.txt",
            comprovante_tipo="text/plain",
            armazenamento=_armazenamento(tmp_path),
        )
    assert excinfo.value.campo == "comprovante"


def test_aporte_em_material_ou_servico_e_recusado_com_422(sessao, cenario, tmp_path):
    admin, apoiador, comunidade, ponto_de_apoio, tipo = cenario

    for forma in (FormaDeAporte.material, FormaDeAporte.servico, FormaDeAporte.absorcao):
        with pytest.raises(ErroDeValidacao) as excinfo:
            declarar_aporte(
                sessao,
                provedor=apoiador,
                valor_declarado=Decimal("50.00"),
                forma=forma,
                origem_da_escolha=OrigemDaEscolhaDoAporte.valor_livre,
                comprovante_conteudo=b"conteudo",
                comprovante_nome_original="comprovante.pdf",
                comprovante_tipo="application/pdf",
                armazenamento=_armazenamento(tmp_path),
            )
        assert excinfo.value.campo == "forma"
    assert sessao.query(AporteDeclarado).count() == 0


def test_homologacao_grava_aporte_com_origem_app_08_converte_e_credita(
    sessao, cenario, criar_valor_de_referencia, tmp_path
):
    admin, apoiador, comunidade, ponto_de_apoio, tipo = cenario
    criar_valor_de_referencia(admin, tipo, valor_em_moedas=Decimal("1.00"))

    declaracao = declarar_aporte(
        sessao,
        provedor=apoiador,
        valor_declarado=Decimal("100.00"),
        forma=FormaDeAporte.financeira,
        origem_da_escolha=OrigemDaEscolhaDoAporte.valor_livre,
        comprovante_conteudo=b"conteudo",
        comprovante_nome_original="comprovante.pdf",
        comprovante_tipo="application/pdf",
        armazenamento=_armazenamento(tmp_path),
    )
    sessao.commit()

    aporte = registrar_aporte(
        sessao,
        operador=admin,
        provedor=apoiador,
        tipo=tipo,
        quantidade=Decimal("2"),
        ponto_de_apoio=ponto_de_apoio,
        data_do_aporte=date(2026, 6, 1),
        forma=FormaDeAporte.financeira,
        valor_de_origem=Decimal("100.00"),
        aporte_declarado=declaracao,
    )
    sessao.commit()

    assert aporte.origem_do_registro == OrigemDoRegistro.app_08
    assert aporte.aporte_declarado_id == declaracao.id
    assert aporte.valor_em_moedas == Decimal("2.00")
    assert declaracao.situacao == SituacaoDaDeclaracao.homologada
    assert declaracao.resolvido_por_id == admin.id
    assert poder_sustentador_de(sessao, provedor_id=apoiador.id) == Decimal("2.00")


def test_segunda_homologacao_da_mesma_declaracao_e_422(
    sessao, cenario, criar_valor_de_referencia, tmp_path
):
    admin, apoiador, comunidade, ponto_de_apoio, tipo = cenario
    criar_valor_de_referencia(admin, tipo)

    declaracao = declarar_aporte(
        sessao,
        provedor=apoiador,
        valor_declarado=Decimal("100.00"),
        forma=FormaDeAporte.financeira,
        origem_da_escolha=OrigemDaEscolhaDoAporte.valor_livre,
        comprovante_conteudo=b"conteudo",
        comprovante_nome_original="comprovante.pdf",
        comprovante_tipo="application/pdf",
        armazenamento=_armazenamento(tmp_path),
    )
    sessao.commit()

    registrar_aporte(
        sessao,
        operador=admin,
        provedor=apoiador,
        tipo=tipo,
        quantidade=Decimal("1"),
        ponto_de_apoio=ponto_de_apoio,
        data_do_aporte=date(2026, 6, 1),
        forma=FormaDeAporte.financeira,
        aporte_declarado=declaracao,
    )
    sessao.commit()

    with pytest.raises(ErroDeValidacao) as excinfo:
        registrar_aporte(
            sessao,
            operador=admin,
            provedor=apoiador,
            tipo=tipo,
            quantidade=Decimal("1"),
            ponto_de_apoio=ponto_de_apoio,
            data_do_aporte=date(2026, 6, 1),
            forma=FormaDeAporte.financeira,
            aporte_declarado=declaracao,
        )
    assert excinfo.value.campo == "aporte_declarado_id"


def test_provedor_nao_homologa_a_propria_declaracao(
    sessao, cenario, criar_valor_de_referencia, tmp_path
):
    admin, apoiador, comunidade, ponto_de_apoio, tipo = cenario
    criar_valor_de_referencia(admin, tipo)

    declaracao = declarar_aporte(
        sessao,
        provedor=apoiador,
        valor_declarado=Decimal("100.00"),
        forma=FormaDeAporte.financeira,
        origem_da_escolha=OrigemDaEscolhaDoAporte.valor_livre,
        comprovante_conteudo=b"conteudo",
        comprovante_nome_original="comprovante.pdf",
        comprovante_tipo="application/pdf",
        armazenamento=_armazenamento(tmp_path),
    )
    sessao.commit()

    with pytest.raises(PermissaoNegada):
        registrar_aporte(
            sessao,
            operador=apoiador,
            provedor=apoiador,
            tipo=tipo,
            quantidade=Decimal("1"),
            ponto_de_apoio=ponto_de_apoio,
            data_do_aporte=date(2026, 6, 1),
            forma=FormaDeAporte.financeira,
            aporte_declarado=declaracao,
        )


def test_recusa_grava_motivo_sem_creditar(sessao, cenario, tmp_path):
    admin, apoiador, comunidade, ponto_de_apoio, tipo = cenario

    declaracao = declarar_aporte(
        sessao,
        provedor=apoiador,
        valor_declarado=Decimal("100.00"),
        forma=FormaDeAporte.financeira,
        origem_da_escolha=OrigemDaEscolhaDoAporte.valor_livre,
        comprovante_conteudo=b"conteudo",
        comprovante_nome_original="comprovante.pdf",
        comprovante_tipo="application/pdf",
        armazenamento=_armazenamento(tmp_path),
    )
    sessao.commit()

    declaracao = recusar_declaracao_de_aporte(
        sessao, declaracao, operador=admin, motivo="Comprovante ilegível."
    )
    sessao.commit()

    assert declaracao.situacao == SituacaoDaDeclaracao.recusada
    assert declaracao.motivo_da_recusa == "Comprovante ilegível."
    assert sessao.query(Aporte).count() == 0
    assert poder_sustentador_de(sessao, provedor_id=apoiador.id) == Decimal("0")


def test_recusa_de_declaracao_ja_resolvida_e_409(sessao, cenario, tmp_path):
    admin, apoiador, comunidade, ponto_de_apoio, tipo = cenario

    declaracao = declarar_aporte(
        sessao,
        provedor=apoiador,
        valor_declarado=Decimal("100.00"),
        forma=FormaDeAporte.financeira,
        origem_da_escolha=OrigemDaEscolhaDoAporte.valor_livre,
        comprovante_conteudo=b"conteudo",
        comprovante_nome_original="comprovante.pdf",
        comprovante_tipo="application/pdf",
        armazenamento=_armazenamento(tmp_path),
    )
    sessao.commit()
    recusar_declaracao_de_aporte(sessao, declaracao, operador=admin, motivo="Motivo qualquer.")
    sessao.commit()

    with pytest.raises(DeclaracaoDeAporteJaResolvida):
        recusar_declaracao_de_aporte(sessao, declaracao, operador=admin, motivo="Outro motivo.")


def test_recusa_sem_motivo_e_422(sessao, cenario, tmp_path):
    admin, apoiador, comunidade, ponto_de_apoio, tipo = cenario

    declaracao = declarar_aporte(
        sessao,
        provedor=apoiador,
        valor_declarado=Decimal("100.00"),
        forma=FormaDeAporte.financeira,
        origem_da_escolha=OrigemDaEscolhaDoAporte.valor_livre,
        comprovante_conteudo=b"conteudo",
        comprovante_nome_original="comprovante.pdf",
        comprovante_tipo="application/pdf",
        armazenamento=_armazenamento(tmp_path),
    )
    sessao.commit()

    with pytest.raises(ErroDeValidacao) as excinfo:
        recusar_declaracao_de_aporte(sessao, declaracao, operador=admin, motivo=None)
    assert excinfo.value.campo == "motivo"
    assert declaracao.situacao == SituacaoDaDeclaracao.pendente
