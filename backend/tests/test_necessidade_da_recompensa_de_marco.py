"""Necessidade da recompensa de marco — fatia 14 do PRD-07 (change
`necessidade-da-recompensa-de-marco`): derivação por comunidade, ponto de apoio,
tipo e trilha; ordem entre trilhas; rotas; absorção, missão e declaração que a
apontam (`RF-07-54`, `RF-07-18`, `RF-07-27`, `RF-07-28`, `RF-09-56`, `RF-02-102`,
`RF-02-103`, `RF-14-25`)."""

from datetime import UTC, date, datetime, timedelta
from decimal import Decimal

import pytest

from nucleo.aportes.modelo import FormaDeAporte, OrigemDaEscolhaDoAporte, SituacaoDaDeclaracao
from nucleo.aportes.regra import (
    _validar_necessidade_da_recompensa,
    declarar_aporte,
    registrar_aporte_por_absorcao,
)
from nucleo.armazenamento.disco import ArmazenamentoEmDisco
from nucleo.aulas.modelo import SituacaoDaAula
from nucleo.erros import ErroDeValidacao
from nucleo.livro_razao.modelo import NaturezaDoLancamento
from nucleo.missoes_do_apoiador.modelo import NivelDeNecessidade, SituacaoDaMissao
from nucleo.missoes_do_apoiador.regra import missoes_abertas_e_visiveis, publicar_missao
from nucleo.necessidades.regra import (
    EspecieDaNecessidade,
    consultar_necessidades_do_mestre,
    derivar_necessidades,
)
from nucleo.personas.modelo import Papel
from nucleo.recursos.modelo import FinalidadeDoRecurso
from nucleo.selos_do_apoiador.modelo import FamiliaDeSelo
from nucleo.tempo import agora

_AGORA = datetime.now(UTC)


def _da_recompensa(necessidades):
    return [n for n in necessidades if n.especie == EspecieDaNecessidade.recompensa_de_marco]


@pytest.fixture
def montar(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_valor_de_referencia,
    criar_aula,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_recompensa_de_marco,
):
    """Uma comunidade com aula anterior no ponto de apoio, uma trilha com
    atividade nessa aula e uma recompensa de 1 kit; `guerreiros` com vínculo
    vigente."""

    def _montar(guerreiros: int = 12, quantidade: Decimal = Decimal("1")):
        admin = criar_persona(Papel.admin)
        comunidade = criar_comunidade(nome="Comunidade Alfa")
        ponto = criar_ponto_de_apoio(admin, comunidade)
        kit = criar_tipo_de_recurso(
            admin, nome="Kit em MDF", finalidade=FinalidadeDoRecurso.recompensa
        )
        criar_valor_de_referencia(admin, kit, valor_em_moedas=Decimal("2.00"))
        aula = criar_aula(
            admin,
            comunidade,
            ponto_de_apoio=ponto,
            inicio_em=_AGORA - timedelta(days=2),
            fim_em=_AGORA - timedelta(days=2) + timedelta(hours=2),
        )
        trilha = criar_trilha(admin, nome="Robótica")
        missao = criar_missao(trilha, admin)
        criar_atividade(missao, admin, aula=aula)
        recompensa = criar_recompensa_de_marco(admin, trilha, missao, kit, quantidade=quantidade)
        alunos = []
        for _ in range(guerreiros):
            alunos.append(criar_persona(Papel.guerreiro, comunidade=comunidade))
        return {
            "admin": admin,
            "comunidade": comunidade,
            "ponto": ponto,
            "kit": kit,
            "aula": aula,
            "trilha": trilha,
            "missao": missao,
            "recompensa": recompensa,
            "alunos": alunos,
        }

    return _montar


def _entregar(criar_lancamento, criar_entrega_de_recompensa, c, aluno):
    lancamento = criar_lancamento(
        c["admin"],
        c["kit"],
        c["ponto"],
        natureza=NaturezaDoLancamento.credito,
        quantidade=Decimal("1"),
    )
    # O crédito acima só existe para a entrega ter lançamento; um débito igual
    # devolve o saldo ao que era, como a entrega real faz.
    criar_lancamento(
        c["admin"], c["kit"], c["ponto"], natureza=NaturezaDoLancamento.debito, quantidade=1
    )
    criar_entrega_de_recompensa(c["admin"], c["recompensa"], aluno, c["ponto"], lancamento)


# --- derivação (`RF-07-54`, `RF-07-18`) -------------------------------------


def test_falta_da_recompensa_vira_necessidade(
    sessao, montar, criar_lancamento, criar_entrega_de_recompensa
):
    c = montar(guerreiros=12)
    for aluno in c["alunos"][:2]:
        _entregar(criar_lancamento, criar_entrega_de_recompensa, c, aluno)
    criar_lancamento(c["admin"], c["kit"], c["ponto"], quantidade=Decimal("4"))

    [necessidade] = _da_recompensa(derivar_necessidades(sessao))

    assert necessidade.comunidade_virtual_id == c["comunidade"].id
    assert necessidade.ponto_de_apoio_id == c["ponto"].id
    assert necessidade.tipo_de_recurso_id == c["kit"].id
    assert necessidade.trilha_id == c["trilha"].id
    assert necessidade.trilha_nome == "Robótica"
    assert necessidade.quantidade_faltante == Decimal("6")
    assert necessidade.valor_em_moedas == Decimal("12.00")
    assert necessidade.aula_id is None
    assert necessidade.inicio_em is None


def test_duas_recompensas_do_mesmo_tipo_somam(
    sessao, montar, criar_missao, criar_recompensa_de_marco
):
    c = montar(guerreiros=3)
    outra_missao = criar_missao(c["trilha"], c["admin"], posicao=2)
    criar_recompensa_de_marco(
        c["admin"], c["trilha"], outra_missao, c["kit"], quantidade=Decimal("2")
    )

    [necessidade] = _da_recompensa(derivar_necessidades(sessao))

    assert necessidade.quantidade_faltante == Decimal("9")


def test_vinculo_encerrado_nao_conta(sessao, montar, criar_persona, criar_vinculo_jogador):
    c = montar(guerreiros=2)
    antigo = criar_persona(Papel.guerreiro)
    criar_vinculo_jogador(antigo, c["comunidade"], data_fim=_AGORA - timedelta(days=1))

    [necessidade] = _da_recompensa(derivar_necessidades(sessao))

    assert necessidade.quantidade_faltante == Decimal("2")


def test_recompensa_coberta_nao_aparece(sessao, montar, criar_lancamento):
    c = montar(guerreiros=3)
    criar_lancamento(c["admin"], c["kit"], c["ponto"], quantidade=Decimal("3"))

    assert _da_recompensa(derivar_necessidades(sessao)) == []


# --- trilhas que contam -----------------------------------------------------


def test_trilha_sem_atividade_em_aula_da_comunidade_fica_de_fora(
    sessao, montar, criar_trilha, criar_missao, criar_recompensa_de_marco
):
    c = montar(guerreiros=2)
    sem_aula = criar_trilha(c["admin"], nome="Sem aula")
    missao = criar_missao(sem_aula, c["admin"])
    criar_recompensa_de_marco(c["admin"], sem_aula, missao, c["kit"])

    trilhas = {n.trilha_id for n in _da_recompensa(derivar_necessidades(sessao))}

    assert trilhas == {c["trilha"].id}


def test_atividade_em_aula_passada_conta(sessao, montar):
    montar(guerreiros=1)  # a única aula da comunidade já terminou

    assert len(_da_recompensa(derivar_necessidades(sessao))) == 1


def test_atividade_em_aula_cancelada_nao_conta(
    sessao,
    montar,
    criar_aula,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_recompensa_de_marco,
):
    c = montar(guerreiros=1)
    cancelada = criar_aula(c["admin"], c["comunidade"], ponto_de_apoio=c["ponto"])
    cancelada.situacao = SituacaoDaAula.cancelada
    sessao.commit()
    trilha = criar_trilha(c["admin"], nome="Só cancelada")
    missao = criar_missao(trilha, c["admin"])
    criar_atividade(missao, c["admin"], aula=cancelada)
    criar_recompensa_de_marco(c["admin"], trilha, missao, c["kit"])

    trilhas = {n.trilha_id for n in _da_recompensa(derivar_necessidades(sessao))}

    assert trilha.id not in trilhas


# --- ponto de apoio da aula anterior ----------------------------------------


def test_a_necessidade_sai_no_ponto_da_aula_anterior(
    sessao, montar, criar_ponto_de_apoio, criar_aula
):
    c = montar(guerreiros=1)
    outro_ponto = criar_ponto_de_apoio(c["admin"], c["comunidade"])
    criar_aula(
        c["admin"],
        c["comunidade"],
        ponto_de_apoio=outro_ponto,
        inicio_em=_AGORA - timedelta(hours=3),
        fim_em=_AGORA - timedelta(hours=1),
    )

    [necessidade] = _da_recompensa(derivar_necessidades(sessao))

    assert necessidade.ponto_de_apoio_id == outro_ponto.id


def test_comunidade_sem_aula_anterior_nao_gera_necessidade(sessao, montar):
    c = montar(guerreiros=2)
    c["aula"].inicio_em = _AGORA + timedelta(days=3)
    c["aula"].fim_em = _AGORA + timedelta(days=3, hours=2)
    sessao.commit()

    assert _da_recompensa(derivar_necessidades(sessao)) == []


# --- ordem entre trilhas ----------------------------------------------------


def test_a_trilha_de_atividade_mais_antiga_conta_primeiro(
    sessao,
    montar,
    criar_aula,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_recompensa_de_marco,
    criar_lancamento,
):
    c = montar(guerreiros=10)  # trilha A, atividade há 2 dias
    aula_recente = criar_aula(
        c["admin"],
        c["comunidade"],
        ponto_de_apoio=c["ponto"],
        inicio_em=_AGORA - timedelta(days=1),
        fim_em=_AGORA - timedelta(days=1) + timedelta(hours=2),
    )
    trilha_b = criar_trilha(c["admin"], nome="Arte")
    missao_b = criar_missao(trilha_b, c["admin"])
    criar_atividade(missao_b, c["admin"], aula=aula_recente)
    criar_recompensa_de_marco(c["admin"], trilha_b, missao_b, c["kit"])
    criar_lancamento(c["admin"], c["kit"], c["ponto"], quantidade=Decimal("6"))

    faltas = {
        n.trilha_id: n.quantidade_faltante for n in _da_recompensa(derivar_necessidades(sessao))
    }

    assert faltas == {c["trilha"].id: Decimal("4"), trilha_b.id: Decimal("10")}


# --- saída e filtro do Mestre (`RF-07-27`, `RF-09-56`) -----------------------


def test_aula_primeiro_e_recompensa_depois(
    sessao, montar, criar_tipo_de_recurso, criar_aula, criar_recurso_declarado_da_aula
):
    c = montar(guerreiros=1)
    lanche = criar_tipo_de_recurso(c["admin"], nome="Lanche")
    futura = criar_aula(
        c["admin"],
        c["comunidade"],
        ponto_de_apoio=c["ponto"],
        inicio_em=_AGORA + timedelta(days=5),
        fim_em=_AGORA + timedelta(days=5, hours=2),
    )
    criar_recurso_declarado_da_aula(futura, lanche, quantidade=Decimal("2"))
    futura.situacao = SituacaoDaAula.pendente_de_lastro
    sessao.commit()

    especies = [n.especie for n in derivar_necessidades(sessao)]

    assert especies == [EspecieDaNecessidade.aula, EspecieDaNecessidade.recompensa_de_marco]


def test_mestre_ve_so_a_recompensa_das_comunidades_dele(
    sessao, montar, criar_persona, criar_comunidade, criar_vinculo_do_mestre
):
    c = montar(guerreiros=1)
    mestre = criar_persona(Papel.mestre)
    criar_vinculo_do_mestre(mestre, c["comunidade"])
    alheio = criar_persona(Papel.mestre)
    criar_vinculo_do_mestre(alheio, criar_comunidade(nome="Outra"))

    assert len(_da_recompensa(consultar_necessidades_do_mestre(sessao, operador=mestre))) == 1
    assert consultar_necessidades_do_mestre(sessao, operador=alheio) == []


def test_rota_publica_traz_a_trilha_sem_reais_nem_pessoa(cliente, montar, criar_chave):
    montar(guerreiros=1)
    chave, _ = criar_chave()

    resposta = cliente.get("/v1/vitrine/necessidades", headers={"X-Chave-Aplicacao": chave})

    assert resposta.status_code == 200
    [item] = resposta.json()
    assert item["especie"] == "recompensa_de_marco"
    assert item["trilha_nome"] == "Robótica"
    assert item["aula_id"] is None and item["inicio_em"] is None
    assert not any("reais" in campo or "origem" in campo for campo in item)
    assert not any("guerreiro" in campo or "provedor" in campo for campo in item)


# --- absorção (`RF-07-28`, `RF-09-57`) ---------------------------------------


def _absorver(sessao, c, operador, **mudancas):
    dados = {
        "tipo": c["kit"],
        "quantidade": Decimal("3"),
        "ponto_de_apoio": c["ponto"],
        "data_do_aporte": date.today(),
        "comunidade": c["comunidade"],
        "trilha": c["trilha"],
        "valor_de_origem": Decimal("30.00"),
    }
    dados.update(mudancas)
    return registrar_aporte_por_absorcao(sessao, operador=operador, **dados)


def test_absorcao_abate_a_falta_da_recompensa(sessao, montar, criar_persona):
    c = montar(guerreiros=6)
    mestre = criar_persona(Papel.mestre)

    aporte = _absorver(sessao, c, mestre)
    sessao.commit()

    assert aporte.comunidade_virtual_id == c["comunidade"].id
    assert aporte.trilha_id == c["trilha"].id
    assert aporte.aula_id is None
    [necessidade] = _da_recompensa(derivar_necessidades(sessao))
    assert necessidade.quantidade_faltante == Decimal("3")


def test_absorcao_em_ponto_diferente_do_da_aula_anterior_e_recusada(
    sessao, montar, criar_persona, criar_ponto_de_apoio
):
    c = montar(guerreiros=6)
    outro = criar_ponto_de_apoio(c["admin"], c["comunidade"])

    with pytest.raises(ErroDeValidacao) as erro:
        _absorver(sessao, c, criar_persona(Papel.mestre), ponto_de_apoio=outro)
    assert erro.value.campo == "ponto_de_apoio_id"


def test_absorcao_com_aula_e_trilha_juntas_e_recusada(sessao, montar, criar_persona):
    c = montar(guerreiros=6)

    with pytest.raises(ErroDeValidacao):
        _absorver(sessao, c, criar_persona(Papel.mestre), aula=c["aula"])


def test_absorcao_de_trilha_sem_recompensa_do_tipo_e_recusada(
    sessao, montar, criar_persona, criar_tipo_de_recurso
):
    c = montar(guerreiros=6)
    camisa = criar_tipo_de_recurso(
        c["admin"], nome="Camisa", finalidade=FinalidadeDoRecurso.recompensa
    )

    with pytest.raises(ErroDeValidacao) as erro:
        _absorver(sessao, c, criar_persona(Papel.mestre), tipo=camisa)
    assert erro.value.campo == "trilha_id"


def test_aporte_da_gestao_nao_declara_trilha(sessao, montar):
    # A rota da gestão não aceita comunidade nem trilha; a regra comum a
    # todas as formas recusa também por dentro.
    c = montar(guerreiros=6)

    with pytest.raises(ErroDeValidacao) as erro:
        _validar_necessidade_da_recompensa(
            sessao,
            forma=FormaDeAporte.material,
            aula=None,
            comunidade=c["comunidade"],
            trilha=c["trilha"],
            tipo=c["kit"],
            ponto_de_apoio=c["ponto"],
        )
    assert erro.value.campo == "trilha_id"


# --- missão do Apoiador (`RF-02-102`, `RF-02-103`) ---------------------------


def _publicar(sessao, c, **mudancas):
    dados = {
        "operador": c["admin"],
        "aula": None,
        "comunidade": c["comunidade"],
        "trilha": c["trilha"],
        "tipo": c["kit"],
        "nivel_de_necessidade": NivelDeNecessidade.reconhecer,
        "titulo": "Kits da turma",
        "o_que_se_pede": "Kits em MDF para quem alcançar o marco",
        "quantidade": Decimal("20.00"),
        "prazo": agora().date() + timedelta(days=30),
        "selo_nome": "Kit garantido",
        "selo_familia": FamiliaDeSelo.frente,
    }
    dados.update(mudancas)
    return publicar_missao(sessao, **dados)


def test_missao_aponta_a_necessidade_da_recompensa(sessao, montar):
    c = montar(guerreiros=4)

    missao = _publicar(sessao, c)
    sessao.commit()

    assert missao.situacao == SituacaoDaMissao.aberta
    assert missao.aula_id is None
    assert (missao.comunidade_virtual_id, missao.trilha_id) == (
        c["comunidade"].id,
        c["trilha"].id,
    )
    assert [d.missao.id for d in missoes_abertas_e_visiveis(sessao)] == [missao.id]


def test_missao_sem_necessidade_da_recompensa_e_recusada(sessao, montar, criar_lancamento):
    c = montar(guerreiros=2)
    criar_lancamento(c["admin"], c["kit"], c["ponto"], quantidade=Decimal("2"))

    with pytest.raises(ErroDeValidacao):
        _publicar(sessao, c)


def test_missao_some_quando_a_falta_da_recompensa_fecha(sessao, montar, criar_lancamento):
    c = montar(guerreiros=2)
    _publicar(sessao, c)
    sessao.commit()

    criar_lancamento(c["admin"], c["kit"], c["ponto"], quantidade=Decimal("2"))

    assert missoes_abertas_e_visiveis(sessao) == []


# --- declaração do Apoiador (`RF-14-25`) -------------------------------------


def _declarar(sessao, apoiador, tmp_path, **mudancas):
    dados = {
        "provedor": apoiador,
        "valor_declarado": Decimal("50.00"),
        "forma": FormaDeAporte.financeira,
        "origem_da_escolha": OrigemDaEscolhaDoAporte.necessidade,
        "comprovante_conteudo": b"conteudo",
        "comprovante_nome_original": "comprovante.pdf",
        "comprovante_tipo": "application/pdf",
        "armazenamento": ArmazenamentoEmDisco(str(tmp_path), str(tmp_path / "sessoes")),
    }
    dados.update(mudancas)
    return declarar_aporte(sessao, **dados)


def test_declaracao_pela_recompensa_nasce_pendente_sem_abater(
    sessao, montar, criar_persona, tmp_path
):
    c = montar(guerreiros=4)

    declaracao = _declarar(
        sessao,
        criar_persona(Papel.apoiador),
        tmp_path,
        comunidade=c["comunidade"],
        trilha=c["trilha"],
        tipo=c["kit"],
    )
    sessao.commit()

    assert declaracao.situacao == SituacaoDaDeclaracao.pendente
    assert (declaracao.comunidade_virtual_id, declaracao.trilha_id) == (
        c["comunidade"].id,
        c["trilha"].id,
    )
    [necessidade] = _da_recompensa(derivar_necessidades(sessao))
    assert necessidade.quantidade_faltante == Decimal("4")


def test_declaracao_por_necessidade_sem_aula_nem_trilha_e_recusada(
    sessao, montar, criar_persona, tmp_path
):
    c = montar(guerreiros=4)

    with pytest.raises(ErroDeValidacao):
        _declarar(sessao, criar_persona(Papel.apoiador), tmp_path, tipo=c["kit"])
