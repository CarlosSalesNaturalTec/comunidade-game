"""O vínculo do Mestre com a Comunidade Virtual.

Entidade própria, separada do `VinculoJogador`: o Mestre pode estar
vinculado a **mais de uma** comunidade, o vínculo **não encerra** no Ciclo
01 e quem o abre é o **agendamento da aula** (`RF-02-30`, decisão do
fundador de 2026-10-30, documento 09 §1).

Antes desta fatia a suíte gravava `VinculoJogador` com o `guerreiro_id` de
um Mestre, por fora de `abrir_vinculo` — provava um estado que o núcleo
recusa criar, e por isso ficava verde enquanto a produção saía vazia.
"""

from datetime import UTC, datetime, timedelta

import pytest

from nucleo.aulas.modelo import MestreDaAula, SituacaoDaAula
from nucleo.aulas.regra import agendar_aula, cancelar_aula
from nucleo.comunidades.modelo import VinculoDoMestre
from nucleo.comunidades.regra import abrir_vinculo, comunidades_do_mestre
from nucleo.erros import ErroDeValidacao
from nucleo.patrimonio.regra import listar_acervo
from nucleo.personas.modelo import Papel

INICIO = datetime(2026, 8, 1, 10, 0, tzinfo=UTC)
FIM = datetime(2026, 8, 1, 12, 0, tzinfo=UTC)


def test_mestre_e_vinculado_a_mais_de_uma_comunidade(
    sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio
):
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre)
    comunidade_a = criar_comunidade("Comunidade A")
    comunidade_b = criar_comunidade("Comunidade B")

    for comunidade in (comunidade_a, comunidade_b):
        agendar_aula(
            sessao,
            operador=admin,
            comunidade=comunidade,
            ponto_de_apoio=criar_ponto_de_apoio(admin, comunidade),
            mestres=[mestre],
            inicio_em=INICIO,
            fim_em=FIM,
        )
    sessao.commit()

    assert comunidades_do_mestre(sessao, mestre=mestre) == {comunidade_a.id, comunidade_b.id}


def test_vinculo_do_guerreiro_recusa_mestre(sessao, criar_persona, criar_comunidade):
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()

    with pytest.raises(ErroDeValidacao):
        abrir_vinculo(sessao, guerreiro=mestre, comunidade_id=comunidade.id)

    assert sessao.query(VinculoDoMestre).count() == 0


def test_mestre_sem_vinculo_le_vazio_e_nunca_erro(sessao, criar_persona):
    mestre = criar_persona(Papel.mestre)

    assert comunidades_do_mestre(sessao, mestre=mestre) == set()
    assert listar_acervo(sessao, operador=mestre, comunidade_virtual_id=None) == []


def test_aula_cancelada_nao_desfaz_o_vinculo(
    sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio
):
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()

    aula = agendar_aula(
        sessao,
        operador=admin,
        comunidade=comunidade,
        ponto_de_apoio=criar_ponto_de_apoio(admin, comunidade),
        mestres=[mestre],
        inicio_em=INICIO,
        fim_em=FIM,
    )
    sessao.commit()

    cancelar_aula(sessao, operador=admin, aula=aula, motivo="Chuva forte")
    sessao.commit()

    assert aula.situacao == SituacaoDaAula.cancelada
    assert comunidades_do_mestre(sessao, mestre=mestre) == {comunidade.id}


def test_agendamento_abre_o_vinculo_de_cada_mestre_escalado(
    sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio
):
    admin = criar_persona(Papel.admin)
    mestre_a = criar_persona(Papel.mestre)
    mestre_b = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()

    aula = agendar_aula(
        sessao,
        operador=admin,
        comunidade=comunidade,
        ponto_de_apoio=criar_ponto_de_apoio(admin, comunidade),
        mestres=[mestre_a, mestre_b],
        inicio_em=INICIO,
        fim_em=FIM,
    )
    sessao.commit()

    escalados = {linha.mestre_id for linha in sessao.query(MestreDaAula).filter_by(aula_id=aula.id)}
    assert escalados == {mestre_a.id, mestre_b.id}
    assert comunidades_do_mestre(sessao, mestre=mestre_a) == {comunidade.id}
    assert comunidades_do_mestre(sessao, mestre=mestre_b) == {comunidade.id}


def test_mestre_ja_vinculado_nao_ganha_vinculo_repetido(
    sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio
):
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)

    for dia in (1, 2):
        agendar_aula(
            sessao,
            operador=admin,
            comunidade=comunidade,
            ponto_de_apoio=ponto_de_apoio,
            mestres=[mestre],
            inicio_em=INICIO + timedelta(days=dia),
            fim_em=FIM + timedelta(days=dia),
        )
    sessao.commit()

    vinculos = sessao.query(VinculoDoMestre).filter_by(mestre_id=mestre.id).all()
    assert len(vinculos) == 1


def test_aula_sem_mestre_e_recusada(sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()

    with pytest.raises(ErroDeValidacao) as excinfo:
        agendar_aula(
            sessao,
            operador=admin,
            comunidade=comunidade,
            ponto_de_apoio=criar_ponto_de_apoio(admin, comunidade),
            mestres=[],
            inicio_em=INICIO,
            fim_em=FIM,
        )

    assert excinfo.value.campo == "mestres"


def test_persona_que_nao_e_mestre_e_recusada_na_escalacao(
    sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio
):
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    comunidade = criar_comunidade()

    with pytest.raises(ErroDeValidacao) as excinfo:
        agendar_aula(
            sessao,
            operador=admin,
            comunidade=comunidade,
            ponto_de_apoio=criar_ponto_de_apoio(admin, comunidade),
            mestres=[apoiador],
            inicio_em=INICIO,
            fim_em=FIM,
        )

    assert excinfo.value.campo == "mestres"


def test_o_vinculo_do_mestre_nao_tem_como_ser_encerrado(sessao, criar_persona, criar_comunidade):
    """O "nunca encerra" é garantido pela **estrutura**, não por disciplina:
    a tabela não tem `data_fim`, e o módulo de regra não expõe função que
    encerre o vínculo — diferente do Guerreiro(a), que tem
    `fim-de-vinculo` (`RF-13-44`). Se algum dia houver encerramento, é
    decisão do fundador e este teste é o que a obriga a passar por aqui.
    """
    from nucleo.comunidades import regra as regra_de_comunidades

    assert "data_fim" not in VinculoDoMestre.__table__.columns

    encerramentos = [
        nome
        for nome in dir(regra_de_comunidades)
        if "encerrar" in nome and "mestre" in nome.lower()
    ]
    assert encerramentos == []
