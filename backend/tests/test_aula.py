from datetime import UTC, datetime, timedelta

import pytest

from nucleo.aulas.modelo import Aula, ModoDeComprovacao, Presenca
from nucleo.aulas.regra import agendar_aula, aulas_vigentes, registrar_presenca
from nucleo.erros import ErroDeValidacao, PermissaoNegada
from nucleo.personas.modelo import Papel

INICIO = datetime(2026, 8, 1, 10, 0, tzinfo=UTC)
FIM = datetime(2026, 8, 1, 12, 0, tzinfo=UTC)


def test_admin_agenda_aula_com_autoria_gravada(sessao, criar_persona, criar_comunidade):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()

    aula = agendar_aula(sessao, operador=admin, comunidade=comunidade, inicio_em=INICIO, fim_em=FIM)
    sessao.commit()

    assert aula.comunidade_virtual_id == comunidade.id
    assert aula.inicio_em == INICIO
    assert aula.fim_em == FIM
    assert aula.autor_id == admin.id
    assert aula.papel_do_autor == Papel.admin.value


def test_mestre_nao_agenda_aula(sessao, criar_persona, criar_comunidade):
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()

    with pytest.raises(PermissaoNegada):
        agendar_aula(sessao, operador=mestre, comunidade=comunidade, inicio_em=INICIO, fim_em=FIM)
    assert sessao.query(Aula).count() == 0


def test_aula_sem_comunidade_e_recusada(sessao, criar_persona):
    admin = criar_persona(Papel.admin)

    with pytest.raises(ErroDeValidacao) as excinfo:
        agendar_aula(sessao, operador=admin, comunidade=None, inicio_em=INICIO, fim_em=FIM)
    assert excinfo.value.campo == "comunidade_virtual_id"
    assert sessao.query(Aula).count() == 0


def test_aula_sem_horario_inicial_e_recusada(sessao, criar_persona, criar_comunidade):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()

    with pytest.raises(ErroDeValidacao) as excinfo:
        agendar_aula(sessao, operador=admin, comunidade=comunidade, inicio_em=None, fim_em=FIM)
    assert excinfo.value.campo == "inicio_em"
    assert sessao.query(Aula).count() == 0


def test_aula_sem_horario_final_e_recusada(sessao, criar_persona, criar_comunidade):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()

    with pytest.raises(ErroDeValidacao) as excinfo:
        agendar_aula(sessao, operador=admin, comunidade=comunidade, inicio_em=INICIO, fim_em=None)
    assert excinfo.value.campo == "fim_em"
    assert sessao.query(Aula).count() == 0


def test_horario_final_anterior_ao_inicial_e_recusado(sessao, criar_persona, criar_comunidade):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()

    with pytest.raises(ErroDeValidacao) as excinfo:
        agendar_aula(sessao, operador=admin, comunidade=comunidade, inicio_em=FIM, fim_em=INICIO)
    assert excinfo.value.campo == "fim_em"
    assert sessao.query(Aula).count() == 0


def test_aula_em_curso_e_devolvida_como_vigente(
    sessao, criar_persona, criar_aula, criar_comunidade
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    agora = datetime.now(UTC)
    aula = criar_aula(
        admin, comunidade, inicio_em=agora - timedelta(hours=1), fim_em=agora + timedelta(hours=1)
    )

    vigentes = aulas_vigentes(sessao)
    assert aula.id in {a.id for a in vigentes}


def test_aula_fora_do_horario_nao_e_vigente(sessao, criar_persona, criar_aula, criar_comunidade):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade, inicio_em=INICIO, fim_em=FIM)

    vigentes = aulas_vigentes(sessao)
    assert aula.id not in {a.id for a in vigentes}


def test_duas_comunidades_no_mesmo_horario_devolvem_duas_aulas(
    sessao, criar_persona, criar_aula, criar_comunidade
):
    admin = criar_persona(Papel.admin)
    comunidade_um = criar_comunidade("Comunidade Um")
    comunidade_dois = criar_comunidade("Comunidade Dois")
    agora = datetime.now(UTC)
    aula_um = criar_aula(
        admin,
        comunidade_um,
        inicio_em=agora - timedelta(hours=1),
        fim_em=agora + timedelta(hours=1),
    )
    aula_dois = criar_aula(
        admin,
        comunidade_dois,
        inicio_em=agora - timedelta(hours=1),
        fim_em=agora + timedelta(hours=1),
    )

    vigentes = {a.id for a in aulas_vigentes(sessao)}
    assert {aula_um.id, aula_dois.id} <= vigentes


def test_sem_aula_agendada_a_derivacao_devolve_vazio(sessao):
    assert aulas_vigentes(sessao) == []


def test_presenca_por_reconhecimento_dispensa_confirmador(
    sessao, criar_persona, criar_aula, criar_comunidade
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(admin, comunidade)

    presenca = registrar_presenca(
        sessao,
        operador=guerreiro,
        aula=aula,
        guerreiro=guerreiro,
        modo=ModoDeComprovacao.reconhecimento.value,
        confirmador=None,
        momento_do_fato=INICIO,
    )
    sessao.commit()

    assert presenca.modo == ModoDeComprovacao.reconhecimento
    assert presenca.confirmador_id is None


def test_presenca_por_confirmacao_grava_quem_confirmou(
    sessao, criar_persona, criar_aula, criar_comunidade
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(admin, comunidade)

    presenca = registrar_presenca(
        sessao,
        operador=mestre,
        aula=aula,
        guerreiro=guerreiro,
        modo=ModoDeComprovacao.confirmacao.value,
        confirmador=mestre,
        momento_do_fato=INICIO,
    )
    sessao.commit()

    assert presenca.modo == ModoDeComprovacao.confirmacao
    assert presenca.confirmador_id == mestre.id


def test_confirmacao_sem_confirmador_e_recusada(
    sessao, criar_persona, criar_aula, criar_comunidade
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(admin, comunidade)

    with pytest.raises(ErroDeValidacao) as excinfo:
        registrar_presenca(
            sessao,
            operador=mestre,
            aula=aula,
            guerreiro=guerreiro,
            modo=ModoDeComprovacao.confirmacao.value,
            confirmador=None,
            momento_do_fato=INICIO,
        )
    assert excinfo.value.campo == "confirmador_id"
    assert sessao.query(Presenca).count() == 0


def test_presenca_em_comunidade_alheia_e_recusada(
    sessao, criar_persona, criar_aula, criar_comunidade
):
    admin = criar_persona(Papel.admin)
    comunidade_da_aula = criar_comunidade("Comunidade da Aula")
    comunidade_do_guerreiro = criar_comunidade("Comunidade do Guerreiro")
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade_do_guerreiro)
    aula = criar_aula(admin, comunidade_da_aula)

    with pytest.raises(ErroDeValidacao) as excinfo:
        registrar_presenca(
            sessao,
            operador=guerreiro,
            aula=aula,
            guerreiro=guerreiro,
            modo=ModoDeComprovacao.reconhecimento.value,
            confirmador=None,
            momento_do_fato=INICIO,
        )
    assert excinfo.value.campo == "aula_id"
    assert sessao.query(Presenca).count() == 0


def test_presenca_sem_aula_e_recusada(sessao, criar_persona, criar_comunidade):
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)

    with pytest.raises(ErroDeValidacao) as excinfo:
        registrar_presenca(
            sessao,
            operador=guerreiro,
            aula=None,
            guerreiro=guerreiro,
            modo=ModoDeComprovacao.reconhecimento.value,
            confirmador=None,
            momento_do_fato=INICIO,
        )
    assert excinfo.value.campo == "aula_id"


def test_presenca_sem_guerreiro_e_recusada(sessao, criar_persona, criar_aula, criar_comunidade):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade)

    with pytest.raises(ErroDeValidacao) as excinfo:
        registrar_presenca(
            sessao,
            operador=admin,
            aula=aula,
            guerreiro=None,
            modo=ModoDeComprovacao.reconhecimento.value,
            confirmador=None,
            momento_do_fato=INICIO,
        )
    assert excinfo.value.campo == "guerreiro_id"


def test_presenca_com_modo_invalido_e_recusada(sessao, criar_persona, criar_aula, criar_comunidade):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(admin, comunidade)

    with pytest.raises(ErroDeValidacao) as excinfo:
        registrar_presenca(
            sessao,
            operador=guerreiro,
            aula=aula,
            guerreiro=guerreiro,
            modo="voo_livre",
            confirmador=None,
            momento_do_fato=INICIO,
        )
    assert excinfo.value.campo == "modo"


def test_presenca_sem_momento_do_fato_e_recusada(
    sessao, criar_persona, criar_aula, criar_comunidade
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(admin, comunidade)

    with pytest.raises(ErroDeValidacao) as excinfo:
        registrar_presenca(
            sessao,
            operador=guerreiro,
            aula=aula,
            guerreiro=guerreiro,
            modo=ModoDeComprovacao.reconhecimento.value,
            confirmador=None,
            momento_do_fato=None,
        )
    assert excinfo.value.campo == "momento_do_fato"


def test_reenvio_da_mesma_presenca_nao_duplica(sessao, criar_persona, criar_aula, criar_comunidade):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(admin, comunidade)

    primeira = registrar_presenca(
        sessao,
        operador=mestre,
        aula=aula,
        guerreiro=guerreiro,
        modo=ModoDeComprovacao.confirmacao.value,
        confirmador=mestre,
        momento_do_fato=INICIO,
    )
    sessao.commit()

    segunda = registrar_presenca(
        sessao,
        operador=guerreiro,
        aula=aula,
        guerreiro=guerreiro,
        modo=ModoDeComprovacao.reconhecimento.value,
        confirmador=None,
        momento_do_fato=INICIO + timedelta(minutes=5),
    )

    assert segunda.id == primeira.id
    assert segunda.modo == ModoDeComprovacao.confirmacao
    assert segunda.confirmador_id == mestre.id
    assert segunda.momento_do_fato == INICIO
    assert sessao.query(Presenca).filter_by(aula_id=aula.id, guerreiro_id=guerreiro.id).count() == 1
