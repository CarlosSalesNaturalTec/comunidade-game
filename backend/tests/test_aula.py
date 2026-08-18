from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from nucleo.aulas.modelo import Aula, ModoDeComprovacao, Presenca, SituacaoDaAula
from nucleo.aulas.regra import (
    RecursoDeclaradoEntrada,
    agendar_aula,
    aulas_vigentes,
    cancelar_aula,
    registrar_presenca,
    tentar_reservar_aula_pendente,
)
from nucleo.erros import ErroDeValidacao, PermissaoNegada
from nucleo.personas.modelo import Papel
from nucleo.reservas.modelo import EstadoDaReserva, Reserva

INICIO = datetime(2026, 8, 1, 10, 0, tzinfo=UTC)
FIM = datetime(2026, 8, 1, 12, 0, tzinfo=UTC)


def test_admin_agenda_aula_com_autoria_gravada(
    sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)

    aula = agendar_aula(
        sessao,
        operador=admin,
        comunidade=comunidade,
        ponto_de_apoio=ponto_de_apoio,
        inicio_em=INICIO,
        fim_em=FIM,
    )
    sessao.commit()

    assert aula.comunidade_virtual_id == comunidade.id
    assert aula.ponto_de_apoio_id == ponto_de_apoio.id
    assert aula.inicio_em == INICIO
    assert aula.fim_em == FIM
    assert aula.autor_id == admin.id
    assert aula.papel_do_autor == Papel.admin.value


def test_mestre_nao_agenda_aula(sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio):
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)

    with pytest.raises(PermissaoNegada):
        agendar_aula(
            sessao,
            operador=mestre,
            comunidade=comunidade,
            ponto_de_apoio=ponto_de_apoio,
            inicio_em=INICIO,
            fim_em=FIM,
        )
    assert sessao.query(Aula).count() == 0


def test_aula_sem_comunidade_e_recusada(
    sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)

    with pytest.raises(ErroDeValidacao) as excinfo:
        agendar_aula(
            sessao,
            operador=admin,
            comunidade=None,
            ponto_de_apoio=ponto_de_apoio,
            inicio_em=INICIO,
            fim_em=FIM,
        )
    assert excinfo.value.campo == "comunidade_virtual_id"
    assert sessao.query(Aula).count() == 0


def test_aula_sem_ponto_de_apoio_e_recusada(sessao, criar_persona, criar_comunidade):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()

    with pytest.raises(ErroDeValidacao) as excinfo:
        agendar_aula(
            sessao,
            operador=admin,
            comunidade=comunidade,
            ponto_de_apoio=None,
            inicio_em=INICIO,
            fim_em=FIM,
        )
    assert excinfo.value.campo == "ponto_de_apoio_id"
    assert sessao.query(Aula).count() == 0


def test_aula_com_ponto_de_apoio_de_outra_comunidade_e_recusada(
    sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio
):
    admin = criar_persona(Papel.admin)
    comunidade_da_aula = criar_comunidade("Comunidade da Aula")
    comunidade_do_ponto = criar_comunidade("Comunidade do Ponto")
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade_do_ponto)

    with pytest.raises(ErroDeValidacao) as excinfo:
        agendar_aula(
            sessao,
            operador=admin,
            comunidade=comunidade_da_aula,
            ponto_de_apoio=ponto_de_apoio,
            inicio_em=INICIO,
            fim_em=FIM,
        )
    assert excinfo.value.campo == "ponto_de_apoio_id"
    assert sessao.query(Aula).count() == 0


def test_aula_sem_horario_inicial_e_recusada(
    sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)

    with pytest.raises(ErroDeValidacao) as excinfo:
        agendar_aula(
            sessao,
            operador=admin,
            comunidade=comunidade,
            ponto_de_apoio=ponto_de_apoio,
            inicio_em=None,
            fim_em=FIM,
        )
    assert excinfo.value.campo == "inicio_em"
    assert sessao.query(Aula).count() == 0


def test_aula_sem_horario_final_e_recusada(
    sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)

    with pytest.raises(ErroDeValidacao) as excinfo:
        agendar_aula(
            sessao,
            operador=admin,
            comunidade=comunidade,
            ponto_de_apoio=ponto_de_apoio,
            inicio_em=INICIO,
            fim_em=None,
        )
    assert excinfo.value.campo == "fim_em"
    assert sessao.query(Aula).count() == 0


def test_horario_final_anterior_ao_inicial_e_recusado(
    sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)

    with pytest.raises(ErroDeValidacao) as excinfo:
        agendar_aula(
            sessao,
            operador=admin,
            comunidade=comunidade,
            ponto_de_apoio=ponto_de_apoio,
            inicio_em=FIM,
            fim_em=INICIO,
        )
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


def test_aula_sem_recursos_declarados_nasce_confirmada(
    sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)

    aula = agendar_aula(
        sessao,
        operador=admin,
        comunidade=comunidade,
        ponto_de_apoio=ponto_de_apoio,
        inicio_em=INICIO,
        fim_em=FIM,
    )
    sessao.commit()

    assert aula.situacao == SituacaoDaAula.confirmada
    assert sessao.query(Reserva).filter_by(aula_id=aula.id).count() == 0


def test_saldo_suficiente_reserva_e_confirma_a_aula(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_lancamento,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    criar_lancamento(admin, tipo, ponto_de_apoio, quantidade=Decimal("10.00"))

    aula = agendar_aula(
        sessao,
        operador=admin,
        comunidade=comunidade,
        ponto_de_apoio=ponto_de_apoio,
        inicio_em=INICIO,
        fim_em=FIM,
        recursos_declarados=[RecursoDeclaradoEntrada(tipo=tipo, quantidade=Decimal("4.00"))],
    )
    sessao.commit()

    assert aula.situacao == SituacaoDaAula.confirmada
    reservas = sessao.query(Reserva).filter_by(aula_id=aula.id).all()
    assert len(reservas) == 1
    assert reservas[0].quantidade == Decimal("4.00")
    assert reservas[0].estado == EstadoDaReserva.reservada


def test_falta_em_um_tipo_deixa_a_aula_pendente_de_lastro(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_lancamento,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo_com_saldo = criar_tipo_de_recurso(admin, nome="Lanche")
    tipo_sem_saldo = criar_tipo_de_recurso(admin, nome="Kit")
    criar_lancamento(admin, tipo_com_saldo, ponto_de_apoio, quantidade=Decimal("10.00"))

    aula = agendar_aula(
        sessao,
        operador=admin,
        comunidade=comunidade,
        ponto_de_apoio=ponto_de_apoio,
        inicio_em=INICIO,
        fim_em=FIM,
        recursos_declarados=[
            RecursoDeclaradoEntrada(tipo=tipo_com_saldo, quantidade=Decimal("3.00")),
            RecursoDeclaradoEntrada(tipo=tipo_sem_saldo, quantidade=Decimal("1.00")),
        ],
    )
    sessao.commit()

    assert aula.situacao == SituacaoDaAula.pendente_de_lastro
    assert sessao.query(Reserva).filter_by(aula_id=aula.id).count() == 0


def test_aula_pendente_de_lastro_e_agendada_com_sucesso(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)

    aula = agendar_aula(
        sessao,
        operador=admin,
        comunidade=comunidade,
        ponto_de_apoio=ponto_de_apoio,
        inicio_em=INICIO,
        fim_em=FIM,
        recursos_declarados=[RecursoDeclaradoEntrada(tipo=tipo, quantidade=Decimal("1.00"))],
    )
    sessao.commit()

    assert aula.situacao == SituacaoDaAula.pendente_de_lastro
    assert sessao.query(Aula).filter_by(id=aula.id).count() == 1


def test_recurso_com_quantidade_zero_e_recusado(
    sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio, criar_tipo_de_recurso
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)

    with pytest.raises(ErroDeValidacao) as excinfo:
        agendar_aula(
            sessao,
            operador=admin,
            comunidade=comunidade,
            ponto_de_apoio=ponto_de_apoio,
            inicio_em=INICIO,
            fim_em=FIM,
            recursos_declarados=[RecursoDeclaradoEntrada(tipo=tipo, quantidade=Decimal("0"))],
        )
    assert excinfo.value.campo == "recursos_declarados"
    assert sessao.query(Aula).count() == 0


def test_recurso_de_tipo_inexistente_e_recusado(
    sessao, criar_persona, criar_comunidade, criar_ponto_de_apoio
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)

    with pytest.raises(ErroDeValidacao) as excinfo:
        agendar_aula(
            sessao,
            operador=admin,
            comunidade=comunidade,
            ponto_de_apoio=ponto_de_apoio,
            inicio_em=INICIO,
            fim_em=FIM,
            recursos_declarados=[RecursoDeclaradoEntrada(tipo=None, quantidade=Decimal("1.00"))],
        )
    assert excinfo.value.campo == "recursos_declarados"
    assert sessao.query(Aula).count() == 0


def test_tentar_reservar_aula_pendente_confirma_quando_ha_saldo(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_lancamento,
    criar_aula,
    criar_recurso_declarado_da_aula,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    aula = criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)
    criar_recurso_declarado_da_aula(aula, tipo, quantidade=Decimal("2.00"))
    aula.situacao = SituacaoDaAula.pendente_de_lastro
    sessao.commit()

    criar_lancamento(admin, tipo, ponto_de_apoio, quantidade=Decimal("2.00"))

    aula = tentar_reservar_aula_pendente(sessao, operador=admin, aula=aula)
    sessao.commit()

    assert aula.situacao == SituacaoDaAula.confirmada
    assert sessao.query(Reserva).filter_by(aula_id=aula.id).count() == 1


def test_tentar_reservar_aula_ja_confirmada_e_idempotente(
    sessao, criar_persona, criar_comunidade, criar_aula
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade)
    assert aula.situacao == SituacaoDaAula.confirmada

    aula_devolvida = tentar_reservar_aula_pendente(sessao, operador=admin, aula=aula)

    assert aula_devolvida.situacao == SituacaoDaAula.confirmada
    assert sessao.query(Reserva).filter_by(aula_id=aula.id).count() == 0


def test_mestre_da_comunidade_cancela_a_aula(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_vinculo_jogador,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    mestre = criar_persona(Papel.mestre)
    criar_vinculo_jogador(mestre, comunidade)
    aula = criar_aula(admin, comunidade)

    cancelada = cancelar_aula(sessao, operador=mestre, aula=aula, motivo="Chuva forte.")
    sessao.commit()

    assert cancelada.situacao == SituacaoDaAula.cancelada
    assert cancelada.cancelamento_motivo == "Chuva forte."


def test_mestre_de_outra_comunidade_e_recusado(
    sessao, criar_persona, criar_comunidade, criar_aula, criar_vinculo_jogador
):
    admin = criar_persona(Papel.admin)
    comunidade_da_aula = criar_comunidade("Comunidade da Aula")
    outra_comunidade = criar_comunidade("Outra Comunidade")
    mestre = criar_persona(Papel.mestre)
    criar_vinculo_jogador(mestre, outra_comunidade)
    aula = criar_aula(admin, comunidade_da_aula)

    with pytest.raises(PermissaoNegada):
        cancelar_aula(sessao, operador=mestre, aula=aula, motivo="Chuva forte.")
    sessao.refresh(aula)
    assert aula.situacao == SituacaoDaAula.confirmada


def test_cancelamento_sem_motivo_e_recusado(sessao, criar_persona, criar_comunidade, criar_aula):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade)

    with pytest.raises(ErroDeValidacao) as excinfo:
        cancelar_aula(sessao, operador=admin, aula=aula, motivo=None)
    assert excinfo.value.campo == "motivo"


def test_guerreiro_nao_cancela_aula(sessao, criar_persona, criar_comunidade, criar_aula):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(admin, comunidade)

    with pytest.raises(PermissaoNegada):
        cancelar_aula(sessao, operador=guerreiro, aula=aula, motivo="Não pode.")


def test_cancelamento_libera_as_reservas(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_ponto_de_apoio,
    criar_tipo_de_recurso,
    criar_lancamento,
    criar_aula,
    criar_reserva,
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    criar_lancamento(admin, tipo, ponto_de_apoio, quantidade=Decimal("10.00"))
    aula = criar_aula(admin, comunidade, ponto_de_apoio=ponto_de_apoio)
    reserva = criar_reserva(admin, aula, tipo, ponto_de_apoio, quantidade=Decimal("4.00"))

    cancelar_aula(sessao, operador=admin, aula=aula, motivo="Cancelada.")
    sessao.commit()

    sessao.refresh(reserva)
    assert reserva.estado == EstadoDaReserva.liberada


def test_cancelamento_de_aula_ja_cancelada_e_recusado(
    sessao, criar_persona, criar_comunidade, criar_aula
):
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade)
    cancelar_aula(sessao, operador=admin, aula=aula, motivo="Primeira vez.")
    sessao.commit()

    with pytest.raises(ErroDeValidacao) as excinfo:
        cancelar_aula(sessao, operador=admin, aula=aula, motivo="Segunda vez.")
    assert excinfo.value.campo == "situacao"
