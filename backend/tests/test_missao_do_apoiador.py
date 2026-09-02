from datetime import timedelta
from decimal import Decimal

import pytest

from nucleo.aulas.modelo import SituacaoDaAula
from nucleo.erros import DespublicacaoDeMissaoConcluidaRecusada, ErroDeValidacao, PermissaoNegada
from nucleo.missoes_do_apoiador.modelo import NivelDeNecessidade, SituacaoDaMissao
from nucleo.missoes_do_apoiador.regra import (
    derivar_missoes,
    despublicar_missao,
    missoes_abertas_e_visiveis,
    publicar_missao,
)
from nucleo.personas.modelo import Papel
from nucleo.selos_do_apoiador.modelo import FamiliaDeSelo
from nucleo.tempo import agora


@pytest.fixture
def cenario(sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio, criar_tipo_de_recurso):
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin, nome="Lanche")
    return admin, apoiador, comunidade, ponto_de_apoio, tipo


def _tornar_pendente(sessao, aula):
    aula.situacao = SituacaoDaAula.pendente_de_lastro
    sessao.commit()


def _publicar(sessao, admin, aula, tipo, **mudancas):
    dados = {
        "nivel_de_necessidade": NivelDeNecessidade.acontecer,
        "titulo": "O lanche do encontro",
        "o_que_se_pede": "Um lanche para vinte crianças",
        "quantidade": Decimal("100.00"),
        "prazo": agora().date() + timedelta(days=30),
        "selo_nome": "Lanche garantido",
        "selo_familia": FamiliaDeSelo.frente,
    }
    dados.update(mudancas)
    return publicar_missao(sessao, operador=admin, aula=aula, tipo=tipo, **dados)


def test_publicacao_com_necessidade_por_tras_grava_aberta(
    sessao, cenario, criar_aula, criar_recurso_declarado_da_aula
):
    admin, apoiador, comunidade, ponto_de_apoio, tipo = cenario
    aula = criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)
    criar_recurso_declarado_da_aula(aula, tipo, quantidade=Decimal("2.00"))
    _tornar_pendente(sessao, aula)

    missao = _publicar(sessao, admin, aula, tipo)
    sessao.commit()

    assert missao.situacao == SituacaoDaMissao.aberta
    assert missao.autor_id == admin.id


def test_publicacao_sem_necessidade_por_tras_e_422(sessao, cenario, criar_aula):
    admin, apoiador, comunidade, ponto_de_apoio, tipo = cenario
    aula = criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)

    with pytest.raises(ErroDeValidacao) as excinfo:
        _publicar(sessao, admin, aula, tipo)
    assert excinfo.value.campo == "aula_id"


def test_apoiador_nao_publica_missao(sessao, cenario, criar_aula, criar_recurso_declarado_da_aula):
    admin, apoiador, comunidade, ponto_de_apoio, tipo = cenario
    aula = criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)
    criar_recurso_declarado_da_aula(aula, tipo, quantidade=Decimal("2.00"))
    _tornar_pendente(sessao, aula)

    with pytest.raises(PermissaoNegada):
        _publicar(sessao, apoiador, aula, tipo)


def test_despublicacao_nao_estorna_e_sai_das_listas(
    sessao, cenario, criar_aula, criar_recurso_declarado_da_aula
):
    admin, apoiador, comunidade, ponto_de_apoio, tipo = cenario
    aula = criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)
    criar_recurso_declarado_da_aula(aula, tipo, quantidade=Decimal("2.00"))
    _tornar_pendente(sessao, aula)
    missao = _publicar(sessao, admin, aula, tipo)
    sessao.commit()

    despublicar_missao(sessao, missao, operador=admin)
    sessao.commit()

    assert missao.situacao == SituacaoDaMissao.despublicada
    assert missoes_abertas_e_visiveis(sessao) == []


def test_despublicacao_de_missao_concluida_e_409(
    sessao, cenario, criar_aula, criar_recurso_declarado_da_aula
):
    admin, apoiador, comunidade, ponto_de_apoio, tipo = cenario
    aula = criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)
    criar_recurso_declarado_da_aula(aula, tipo, quantidade=Decimal("2.00"))
    _tornar_pendente(sessao, aula)
    missao = _publicar(sessao, admin, aula, tipo)
    missao.situacao = SituacaoDaMissao.concluida
    sessao.commit()

    with pytest.raises(DespublicacaoDeMissaoConcluidaRecusada):
        despublicar_missao(sessao, missao, operador=admin)


def test_missoes_agrupadas_por_nivel(sessao, cenario, criar_aula, criar_recurso_declarado_da_aula):
    admin, apoiador, comunidade, ponto_de_apoio, tipo = cenario
    aula_existir = criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)
    criar_recurso_declarado_da_aula(aula_existir, tipo, quantidade=Decimal("2.00"))
    _tornar_pendente(sessao, aula_existir)
    aula_permanecer = criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)
    criar_recurso_declarado_da_aula(aula_permanecer, tipo, quantidade=Decimal("3.00"))
    _tornar_pendente(sessao, aula_permanecer)

    _publicar(sessao, admin, aula_existir, tipo, nivel_de_necessidade=NivelDeNecessidade.existir)
    _publicar(
        sessao, admin, aula_permanecer, tipo, nivel_de_necessidade=NivelDeNecessidade.permanecer
    )
    sessao.commit()

    visiveis = missoes_abertas_e_visiveis(sessao)
    niveis = {derivada.missao.nivel_de_necessidade for derivada in visiveis}
    assert niveis == {NivelDeNecessidade.existir, NivelDeNecessidade.permanecer}


def test_missao_vencida_sai_da_lista(sessao, cenario, criar_aula, criar_recurso_declarado_da_aula):
    admin, apoiador, comunidade, ponto_de_apoio, tipo = cenario
    aula = criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)
    criar_recurso_declarado_da_aula(aula, tipo, quantidade=Decimal("2.00"))
    _tornar_pendente(sessao, aula)
    missao = _publicar(sessao, admin, aula, tipo, prazo=agora().date() - timedelta(days=1))
    sessao.commit()

    visiveis = missoes_abertas_e_visiveis(sessao)

    assert visiveis == []
    admin_view = derivar_missoes(sessao)
    derivada = next(d for d in admin_view if d.missao.id == missao.id)
    assert derivada.vencida is True
    assert derivada.missao.situacao == SituacaoDaMissao.aberta


def test_missao_sem_necessidade_por_tras_some_da_lista_publica(
    sessao,
    cenario,
    criar_aula,
    criar_recurso_declarado_da_aula,
    criar_valor_de_referencia,
    criar_lancamento,
):
    admin, apoiador, comunidade, ponto_de_apoio, tipo = cenario
    aula = criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)
    criar_recurso_declarado_da_aula(aula, tipo, quantidade=Decimal("2.00"))
    _tornar_pendente(sessao, aula)
    missao = _publicar(sessao, admin, aula, tipo)
    sessao.commit()

    # A necessidade fecha por fora, sem passar pela missão — o par some das
    # necessidades derivadas, e a missão some da lista pública sem virar
    # concluída (design — Decisions 1, 3).
    criar_lancamento(admin, tipo, ponto_de_apoio, quantidade=Decimal("2.00"))
    sessao.commit()

    assert missoes_abertas_e_visiveis(sessao) == []
    assert missao.situacao == SituacaoDaMissao.aberta
