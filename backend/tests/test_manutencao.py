from datetime import UTC, datetime, timedelta

from sqlalchemy.orm import sessionmaker

from nucleo.biometria.modelo import ApagamentoDeTemplate, GatilhoDeApagamento
from nucleo.biometria.regra import marcar_apagamento
from nucleo.manutencao import executar_manutencao
from nucleo.personas.modelo import Credencial, Papel, TipoDeCredencial
from nucleo.vinculo_do_guerreiro.modelo import FimDeVinculo
from nucleo.vinculo_do_guerreiro.regra import MESES_SEM_ATIVIDADE_PARA_VARREDURA


def _executar_com_a_sessao_do_teste(monkeypatch, conexao):
    fabrica = sessionmaker(
        bind=conexao, expire_on_commit=False, join_transaction_mode="create_savepoint"
    )
    monkeypatch.setattr("nucleo.manutencao.obter_fabrica_de_sessao", lambda: fabrica)
    return fabrica


def test_comando_encerra_e_apaga_o_que_venceu(
    monkeypatch, conexao, sessao, criar_persona, criar_template_biometrico, capsys
):
    fabrica = _executar_com_a_sessao_do_teste(monkeypatch, conexao)

    guerreiro_sem_atividade = criar_persona(Papel.guerreiro)
    guerreiro_sem_atividade.criada_em = datetime.now(UTC) - timedelta(
        days=(MESES_SEM_ATIVIDADE_PARA_VARREDURA + 1) * 31
    )
    sessao.commit()

    guerreiro_com_template_vencido = criar_persona(Papel.guerreiro)
    criar_template_biometrico(guerreiro_com_template_vencido)
    marcar_apagamento(
        sessao,
        guerreiro_id=guerreiro_com_template_vencido.id,
        gatilho=GatilhoDeApagamento.recusa_biometria,
    )
    marca = (
        sessao.query(ApagamentoDeTemplate)
        .filter_by(guerreiro_id=guerreiro_com_template_vencido.id)
        .one()
    )
    marca.apagar_em = datetime.now(UTC) - timedelta(seconds=1)
    sessao.commit()

    executar_manutencao()

    with fabrica() as verificacao:
        assert (
            verificacao.query(FimDeVinculo)
            .filter_by(guerreiro_id=guerreiro_sem_atividade.id)
            .count()
            == 1
        )
        assert (
            verificacao.query(Credencial)
            .filter_by(
                persona_id=guerreiro_com_template_vencido.id,
                tipo=TipoDeCredencial.biometria,
                ativa=True,
            )
            .count()
            == 0
        )

    saida = capsys.readouterr().out
    assert "1 vínculo" in saida
    assert "1 template" in saida


def test_comando_nao_toca_no_que_ainda_nao_venceu(
    monkeypatch, conexao, sessao, criar_persona, criar_template_biometrico
):
    fabrica = _executar_com_a_sessao_do_teste(monkeypatch, conexao)

    guerreiro = criar_persona(Papel.guerreiro)
    criar_template_biometrico(guerreiro)
    marcar_apagamento(
        sessao, guerreiro_id=guerreiro.id, gatilho=GatilhoDeApagamento.recusa_biometria
    )
    sessao.commit()

    executar_manutencao()

    with fabrica() as verificacao:
        assert (
            verificacao.query(Credencial)
            .filter_by(persona_id=guerreiro.id, tipo=TipoDeCredencial.biometria, ativa=True)
            .count()
            == 1
        )


def test_comando_e_repetivel(
    monkeypatch, conexao, sessao, criar_persona, criar_template_biometrico, capsys
):
    _executar_com_a_sessao_do_teste(monkeypatch, conexao)

    guerreiro = criar_persona(Papel.guerreiro)
    criar_template_biometrico(guerreiro)
    marcar_apagamento(
        sessao, guerreiro_id=guerreiro.id, gatilho=GatilhoDeApagamento.recusa_biometria
    )
    marca = sessao.query(ApagamentoDeTemplate).filter_by(guerreiro_id=guerreiro.id).one()
    marca.apagar_em = datetime.now(UTC) - timedelta(seconds=1)
    sessao.commit()

    executar_manutencao()
    capsys.readouterr()
    executar_manutencao()
    segunda_saida = capsys.readouterr().out

    assert "0 vínculo" in segunda_saida
    assert "0 template" in segunda_saida
