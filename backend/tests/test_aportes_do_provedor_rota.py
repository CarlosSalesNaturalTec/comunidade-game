"""`GET /provedores/{id}/aportes` — a seção Aportes da ficha do adulto na
gestão (`RF-02-117`, `RN-02-34`, `RN-07-06`, `RN-07-22`, `RN-14-07`)."""

import uuid
from datetime import date
from decimal import Decimal

import pytest

from nucleo.aportes.modelo import (
    AporteDeclarado,
    FormaDeAporte,
    OrigemDaEscolhaDoAporte,
    SituacaoDaDeclaracao,
)
from nucleo.livro_razao.modelo import NaturezaDoLancamento
from nucleo.personas.modelo import Papel


@pytest.fixture
def cenario(
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
    tipo = criar_tipo_de_recurso(admin, nome="Doação em dinheiro", unidade="R$")

    def cabecalhos(persona):
        token, _ = criar_sessao_de_teste(persona)
        return {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}

    return admin, ponto, tipo, cabecalhos


def _aportar(criar_lancamento, criar_aporte, admin, provedor, tipo, ponto, **kw):
    moedas = kw.pop("valor_em_moedas", Decimal("1.00"))
    credito = criar_lancamento(
        admin, tipo, ponto, natureza=NaturezaDoLancamento.credito, valor_em_moedas=moedas
    )
    return criar_aporte(admin, provedor, tipo, ponto, credito, valor_em_moedas=moedas, **kw)


def _declarar(sessao, apoiador, situacao=SituacaoDaDeclaracao.pendente, valor="30.00"):
    declaracao = AporteDeclarado(
        provedor_id=apoiador.id,
        valor_declarado=Decimal(valor),
        origem_da_escolha=OrigemDaEscolhaDoAporte.valor_livre,
        situacao=situacao,
        autor_id=apoiador.id,
        papel_do_autor=apoiador.papel.value,
    )
    sessao.add(declaracao)
    sessao.flush()
    return declaracao


def test_o_admin_le_os_aportes_de_um_apoiador_em_ordem(
    cliente, cenario, criar_persona, criar_lancamento, criar_aporte
):
    admin, ponto, tipo, cabecalhos = cenario
    apoiador = criar_persona(Papel.apoiador)
    _aportar(
        criar_lancamento,
        criar_aporte,
        admin,
        apoiador,
        tipo,
        ponto,
        data_do_aporte=date(2026, 3, 1),
        valor_em_moedas=Decimal("2.00"),
    )
    _aportar(
        criar_lancamento,
        criar_aporte,
        admin,
        apoiador,
        tipo,
        ponto,
        data_do_aporte=date(2026, 11, 10),
        quantidade=Decimal("150.00"),
        valor_em_moedas=Decimal("15.00"),
        forma=FormaDeAporte.financeira,
    )

    resposta = cliente.get(f"/v1/provedores/{apoiador.id}/aportes", headers=cabecalhos(admin))

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert [a["data_do_aporte"] for a in corpo["aportes"]] == ["2026-11-10", "2026-03-01"]
    primeiro = corpo["aportes"][0]
    assert primeiro["tipo_de_recurso_nome"] == "Doação em dinheiro"
    assert primeiro["tipo_de_recurso_unidade"] == "R$"
    assert primeiro["quantidade"] == "150.00"
    assert primeiro["valor_em_moedas"] == "15.00"
    assert primeiro["ponto_de_apoio_nome"] == ponto.nome
    assert primeiro["forma"] == "financeira"
    assert primeiro["destinacao"] == "lastro"
    assert Decimal(corpo["poder_sustentador_em_moedas"]) > 0


def test_o_valor_de_origem_em_reais_sai_ao_admin(
    cliente, cenario, criar_persona, criar_lancamento, criar_aporte
):
    admin, ponto, tipo, cabecalhos = cenario
    apoiador = criar_persona(Papel.apoiador)
    _aportar(
        criar_lancamento,
        criar_aporte,
        admin,
        apoiador,
        tipo,
        ponto,
        valor_de_origem=Decimal("50.00"),
        valor_em_moedas=Decimal("5.00"),
    )

    corpo = cliente.get(f"/v1/provedores/{apoiador.id}/aportes", headers=cabecalhos(admin)).json()

    assert corpo["aportes"][0]["valor_de_origem"] == "50.00"
    assert corpo["aportes"][0]["valor_em_moedas"] == "5.00"


def test_o_comprovante_aparece_so_como_marca(
    cliente, sessao, cenario, criar_persona, criar_lancamento, criar_aporte
):
    admin, ponto, tipo, cabecalhos = cenario
    apoiador = criar_persona(Papel.apoiador)
    com = _aportar(criar_lancamento, criar_aporte, admin, apoiador, tipo, ponto)
    com.comprovante_referencia = "aportes/segredo/comprovante.pdf"
    _aportar(criar_lancamento, criar_aporte, admin, apoiador, tipo, ponto)
    sessao.flush()

    resposta = cliente.get(f"/v1/provedores/{apoiador.id}/aportes", headers=cabecalhos(admin))

    marcas = sorted(a["tem_comprovante"] for a in resposta.json()["aportes"])
    assert marcas == [False, True]
    assert "segredo" not in resposta.text
    assert "comprovante_referencia" not in resposta.text


def test_a_declaracao_pendente_sai_separada_e_nao_soma(
    cliente, sessao, cenario, criar_persona, criar_lancamento, criar_aporte
):
    admin, ponto, tipo, cabecalhos = cenario
    apoiador = criar_persona(Papel.apoiador)
    _aportar(
        criar_lancamento, criar_aporte, admin, apoiador, tipo, ponto, valor_em_moedas=Decimal("3")
    )
    pendente = _declarar(sessao, apoiador, valor="30.00")
    _declarar(sessao, apoiador, situacao=SituacaoDaDeclaracao.recusada, valor="99.00")

    sem_pendente = cliente.get(
        f"/v1/provedores/{apoiador.id}/poder-sustentador",
        headers=cabecalhos(admin),
    ).json()["poder_sustentador_em_moedas"]
    corpo = cliente.get(f"/v1/provedores/{apoiador.id}/aportes", headers=cabecalhos(admin)).json()

    assert [d["id"] for d in corpo["declaracoes_pendentes"]] == [str(pendente.id)]
    assert corpo["declaracoes_pendentes"][0]["valor_declarado"] == "30.00"
    assert corpo["declaracoes_pendentes"][0]["origem_da_escolha"] == "valor_livre"
    assert len(corpo["aportes"]) == 1
    assert corpo["poder_sustentador_em_moedas"] == sem_pendente


def test_o_mestre_provedor_tambem_e_lido(
    cliente, cenario, criar_persona, criar_lancamento, criar_aporte
):
    admin, ponto, tipo, cabecalhos = cenario
    mestre = criar_persona(Papel.mestre)
    _aportar(
        criar_lancamento,
        criar_aporte,
        admin,
        mestre,
        tipo,
        ponto,
        forma=FormaDeAporte.absorcao,
    )

    corpo = cliente.get(f"/v1/provedores/{mestre.id}/aportes", headers=cabecalhos(admin)).json()

    assert [a["forma"] for a in corpo["aportes"]] == ["absorcao"]


@pytest.mark.parametrize("papel", [Papel.mestre, Papel.apoiador])
def test_outro_papel_e_recusado(cliente, cenario, criar_persona, papel):
    _, _, _, cabecalhos = cenario
    apoiador = criar_persona(Papel.apoiador)
    leitor = apoiador if papel == Papel.apoiador else criar_persona(papel)

    resposta = cliente.get(f"/v1/provedores/{apoiador.id}/aportes", headers=cabecalhos(leitor))

    assert resposta.status_code == 403
    assert "aportes" not in resposta.json()


def test_a_rota_nao_serve_guerreiro_nem_inexistente(
    cliente, cenario, criar_persona, criar_comunidade
):
    admin, _, _, cabecalhos = cenario
    guerreiro = criar_persona(Papel.guerreiro, comunidade=criar_comunidade())

    do_guerreiro = cliente.get(f"/v1/provedores/{guerreiro.id}/aportes", headers=cabecalhos(admin))
    inexistente = cliente.get(f"/v1/provedores/{uuid.uuid4()}/aportes", headers=cabecalhos(admin))

    assert do_guerreiro.status_code == 404
    assert inexistente.status_code == 404
    assert do_guerreiro.json() == inexistente.json()
