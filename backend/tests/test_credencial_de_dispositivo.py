from datetime import UTC, datetime

import pytest
from sqlalchemy.exc import IntegrityError

from nucleo.coletas.modelo import OrigemDoRegistro, RegistroDeColeta
from nucleo.coletas.regra import (
    abrir_serie_de_coleta,
    emitir_credencial_de_dispositivo,
    gravar_registro_de_coleta,
    revogar_credencial_de_dispositivo,
)
from nucleo.comunidades.modelo import ComunidadeVirtual, VinculoJogador
from nucleo.erros import (
    CredencialDeDispositivoJaAtiva,
    ErroDeValidacao,
    NaoEncontrado,
    PermissaoNegada,
)
from nucleo.locais.modelo import ORDEM_DOS_NIVEIS, NivelDoLocal
from nucleo.personas.modelo import Credencial, Papel, TipoDeCredencial

# O vínculo do Guerreiro(a) nasce no instante real do teste (server_default);
# recuar o início garante que a medição, datada no passado simulado, caia
# dentro do intervalo vigente (`RN-08-03`), como em test_registro_de_coleta.py.
INICIO_DO_VINCULO = datetime(2025, 1, 1, tzinfo=UTC)
MOMENTO_DA_MEDICAO = datetime(2026, 8, 12, 14, 0, tzinfo=UTC)


def _criar_comunidade(sessao) -> ComunidadeVirtual:
    comunidade = ComunidadeVirtual(
        nome="Comunidade de Teste", localizacao="Bairro de teste", granularidade_maxima="quadra"
    )
    sessao.add(comunidade)
    sessao.commit()
    sessao.refresh(comunidade)
    return comunidade


def _criar_local_no_nivel(criar_local, comunidade, nivel: NivelDoLocal, rotulo: str | None = None):
    indice = ORDEM_DOS_NIVEIS.index(nivel)
    pai = None
    local = None
    for indice_atual in range(indice + 1):
        nivel_atual = ORDEM_DOS_NIVEIS[indice_atual]
        ultimo = indice_atual == indice
        local = criar_local(
            comunidade,
            nivel=nivel_atual,
            rotulo=(rotulo if ultimo and rotulo else f"{nivel_atual.value} de teste"),
            local_pai=pai,
        )
        pai = local
    return local


def _preparar_serie(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
):
    """Trilha com Mestre autor, série ativa de um Guerreiro(a) coletor —
    o estado de que emissão, conferência e revogação partem."""
    comunidade = _criar_comunidade(sessao)
    admin = criar_persona(Papel.admin)
    criar_poder_do_territorio(admin)
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    desafio = criar_desafio_de_coleta(missao, mestre, granularidade_exigida=NivelDoLocal.rua)
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    vinculo = sessao.query(VinculoJogador).filter_by(guerreiro_id=guerreiro.id).one()
    vinculo.data_inicio = INICIO_DO_VINCULO
    sessao.commit()
    local = _criar_local_no_nivel(criar_local, comunidade, NivelDoLocal.rua)
    serie = abrir_serie_de_coleta(sessao, operador=guerreiro, desafio=desafio, local_id=local.id)
    sessao.commit()
    return {
        "comunidade": comunidade,
        "admin": admin,
        "mestre": mestre,
        "trilha": trilha,
        "desafio": desafio,
        "guerreiro": guerreiro,
        "local": local,
        "serie": serie,
    }


@pytest.fixture
def cenario(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
):
    return _preparar_serie(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
    )


# --- Emissão (RF-01-67) ---------------------------------------------------


def test_admin_emite_credencial_de_dispositivo(sessao, cenario):
    credencial, segredo = emitir_credencial_de_dispositivo(
        sessao,
        operador=cenario["admin"],
        serie=cenario["serie"],
        identificador="sensor-01",
        trilha_id=cenario["trilha"].id,
    )
    sessao.commit()

    assert credencial.tipo == TipoDeCredencial.dispositivo
    assert credencial.persona_id == cenario["guerreiro"].id
    assert credencial.serie_de_coleta_id == cenario["serie"].id
    assert credencial.trilha_id == cenario["trilha"].id
    assert credencial.ativa is True
    assert credencial.segredo != segredo
    assert segredo not in credencial.segredo


def test_mestre_autor_do_desafio_tambem_emite(sessao, cenario):
    credencial, _ = emitir_credencial_de_dispositivo(
        sessao,
        operador=cenario["mestre"],
        serie=cenario["serie"],
        identificador="sensor-01",
        trilha_id=cenario["trilha"].id,
    )

    assert credencial.tipo == TipoDeCredencial.dispositivo


def test_mestre_que_nao_e_autor_recebe_403(sessao, cenario, criar_persona):
    outro_mestre = criar_persona(Papel.mestre)

    with pytest.raises(PermissaoNegada):
        emitir_credencial_de_dispositivo(
            sessao,
            operador=outro_mestre,
            serie=cenario["serie"],
            identificador="sensor-01",
            trilha_id=cenario["trilha"].id,
        )
    assert sessao.query(Credencial).filter_by(tipo=TipoDeCredencial.dispositivo).count() == 0


@pytest.mark.parametrize("papel", [Papel.guerreiro, Papel.responsavel, Papel.apoiador])
def test_quem_nao_e_admin_nem_mestre_recebe_403(sessao, cenario, criar_persona, papel):
    outro = criar_persona(papel)

    with pytest.raises(PermissaoNegada):
        emitir_credencial_de_dispositivo(
            sessao,
            operador=outro,
            serie=cenario["serie"],
            identificador="sensor-01",
            trilha_id=cenario["trilha"].id,
        )


def test_segunda_credencial_ativa_na_mesma_serie_e_recusada(sessao, cenario):
    emitir_credencial_de_dispositivo(
        sessao,
        operador=cenario["mestre"],
        serie=cenario["serie"],
        identificador="sensor-01",
        trilha_id=cenario["trilha"].id,
    )
    sessao.commit()

    with pytest.raises(CredencialDeDispositivoJaAtiva):
        emitir_credencial_de_dispositivo(
            sessao,
            operador=cenario["mestre"],
            serie=cenario["serie"],
            identificador="sensor-02",
            trilha_id=cenario["trilha"].id,
        )


def test_mesmo_identificador_em_series_distintas_e_aceito(sessao, cenario, criar_local):
    emitir_credencial_de_dispositivo(
        sessao,
        operador=cenario["mestre"],
        serie=cenario["serie"],
        identificador="sensor-repetido",
        trilha_id=cenario["trilha"].id,
    )
    sessao.commit()

    outro_local = _criar_local_no_nivel(
        criar_local, cenario["comunidade"], NivelDoLocal.rua, rotulo="Outra rua de teste"
    )
    outra_serie = abrir_serie_de_coleta(
        sessao, operador=cenario["guerreiro"], desafio=cenario["desafio"], local_id=outro_local.id
    )
    sessao.commit()

    credencial_nova, _ = emitir_credencial_de_dispositivo(
        sessao,
        operador=cenario["mestre"],
        serie=outra_serie,
        identificador="sensor-repetido",
        trilha_id=cenario["trilha"].id,
    )

    assert credencial_nova.identificador == "sensor-repetido"
    assert credencial_nova.serie_de_coleta_id == outra_serie.id


def test_revogada_a_anterior_a_serie_aceita_credencial_nova(sessao, cenario):
    primeira, _ = emitir_credencial_de_dispositivo(
        sessao,
        operador=cenario["mestre"],
        serie=cenario["serie"],
        identificador="sensor-01",
        trilha_id=cenario["trilha"].id,
    )
    sessao.commit()
    revogar_credencial_de_dispositivo(
        sessao, primeira, operador=cenario["mestre"], motivo="Aparelho trocado."
    )
    sessao.commit()

    nova, _ = emitir_credencial_de_dispositivo(
        sessao,
        operador=cenario["mestre"],
        serie=cenario["serie"],
        identificador="sensor-02",
        trilha_id=cenario["trilha"].id,
    )
    sessao.commit()

    assert nova.ativa is True
    sessao.refresh(primeira)
    assert primeira.ativa is False


# --- Índice único da série ativa (RN-01-53) --------------------------------


def test_indice_recusa_duas_credenciais_ativas_na_mesma_serie(sessao, cenario):
    """Defesa em profundidade: mesmo contornando `emitir_credencial_de_dispositivo`,
    o índice único parcial sobre `serie_de_coleta_id` recusa a segunda linha."""
    sessao.add(
        Credencial(
            persona_id=cenario["guerreiro"].id,
            tipo=TipoDeCredencial.dispositivo,
            identificador="sensor-01",
            segredo="resumo-1",
            serie_de_coleta_id=cenario["serie"].id,
            ativa=True,
        )
    )
    sessao.commit()

    sessao.add(
        Credencial(
            persona_id=cenario["guerreiro"].id,
            tipo=TipoDeCredencial.dispositivo,
            identificador="sensor-02",
            segredo="resumo-2",
            serie_de_coleta_id=cenario["serie"].id,
            ativa=True,
        )
    )
    with pytest.raises(IntegrityError):
        sessao.commit()


# --- Revogação (RF-01-68) --------------------------------------------------


def test_admin_revoga_gravando_motivo_e_autoria(sessao, cenario):
    credencial, _ = emitir_credencial_de_dispositivo(
        sessao,
        operador=cenario["mestre"],
        serie=cenario["serie"],
        identificador="sensor-01",
        trilha_id=cenario["trilha"].id,
    )
    sessao.commit()

    revogar_credencial_de_dispositivo(
        sessao, credencial, operador=cenario["admin"], motivo="Aparelho danificado."
    )
    sessao.commit()

    assert credencial.ativa is False
    assert credencial.motivo_da_revogacao == "Aparelho danificado."
    assert credencial.revogada_por == str(cenario["admin"].id)
    assert credencial.revogada_em is not None


def test_mestre_que_nao_e_autor_nao_revoga(sessao, cenario, criar_persona):
    credencial, _ = emitir_credencial_de_dispositivo(
        sessao,
        operador=cenario["mestre"],
        serie=cenario["serie"],
        identificador="sensor-01",
        trilha_id=cenario["trilha"].id,
    )
    sessao.commit()
    outro_mestre = criar_persona(Papel.mestre)

    with pytest.raises(PermissaoNegada):
        revogar_credencial_de_dispositivo(
            sessao, credencial, operador=outro_mestre, motivo="Qualquer motivo."
        )
    sessao.refresh(credencial)
    assert credencial.ativa is True


def test_revogacao_sem_motivo_e_recusada(sessao, cenario):
    credencial, _ = emitir_credencial_de_dispositivo(
        sessao,
        operador=cenario["mestre"],
        serie=cenario["serie"],
        identificador="sensor-01",
        trilha_id=cenario["trilha"].id,
    )
    sessao.commit()

    with pytest.raises(ErroDeValidacao) as excinfo:
        revogar_credencial_de_dispositivo(sessao, credencial, operador=cenario["admin"], motivo="")
    assert excinfo.value.campo == "motivo"
    sessao.refresh(credencial)
    assert credencial.ativa is True


def test_revogar_credencial_inexistente_e_404(sessao, cenario):
    with pytest.raises(NaoEncontrado):
        revogar_credencial_de_dispositivo(
            sessao, None, operador=cenario["admin"], motivo="Motivo qualquer."
        )


def test_revogar_nao_desfaz_registros_ja_gravados(sessao, cenario):
    credencial, segredo = emitir_credencial_de_dispositivo(
        sessao,
        operador=cenario["mestre"],
        serie=cenario["serie"],
        identificador="sensor-01",
        trilha_id=cenario["trilha"].id,
    )
    sessao.commit()
    registro = gravar_registro_de_coleta(
        sessao,
        operador=cenario["guerreiro"],
        serie=cenario["serie"],
        momento_do_fato=MOMENTO_DA_MEDICAO,
        origem=OrigemDoRegistro.sensor.value,
        credencial_de_dispositivo_id=credencial.id,
        valor=25.0,
        unidade="°C",
    )
    sessao.commit()

    revogar_credencial_de_dispositivo(
        sessao, credencial, operador=cenario["admin"], motivo="Fim da coleta."
    )
    sessao.commit()
    sessao.refresh(registro)

    assert registro.valor == 25.0
    assert registro.credencial_id == credencial.id


def test_transferencia_de_comunidade_nao_derruba_a_credencial(sessao, cenario):
    credencial, _ = emitir_credencial_de_dispositivo(
        sessao,
        operador=cenario["mestre"],
        serie=cenario["serie"],
        identificador="sensor-01",
        trilha_id=cenario["trilha"].id,
    )
    sessao.commit()

    vinculo = sessao.query(VinculoJogador).filter_by(guerreiro_id=cenario["guerreiro"].id).one()
    vinculo.data_fim = datetime.now(UTC)
    sessao.commit()
    sessao.refresh(credencial)

    assert credencial.ativa is True


# --- Registro de coleta por dispositivo (RF-08-14) -------------------------


def test_sensor_grava_registro_com_origem_sensor_e_aponta_a_credencial(sessao, cenario):
    credencial, _ = emitir_credencial_de_dispositivo(
        sessao,
        operador=cenario["mestre"],
        serie=cenario["serie"],
        identificador="sensor-01",
        trilha_id=cenario["trilha"].id,
    )
    sessao.commit()

    registro = gravar_registro_de_coleta(
        sessao,
        operador=cenario["guerreiro"],
        serie=cenario["serie"],
        momento_do_fato=MOMENTO_DA_MEDICAO,
        origem=OrigemDoRegistro.sensor.value,
        credencial_de_dispositivo_id=credencial.id,
        valor=25.0,
        unidade="°C",
    )
    sessao.commit()

    assert registro.origem == OrigemDoRegistro.sensor
    assert registro.credencial_id == credencial.id
    assert registro.autor_id == cenario["guerreiro"].id
    assert registro.papel_do_autor == Papel.guerreiro.value
    assert registro.comunidade_virtual_id == cenario["comunidade"].id
    assert registro.pontos_creditados == 5
    assert registro.momento_do_fato == MOMENTO_DA_MEDICAO
    assert registro.momento_do_registro != registro.momento_do_fato


def test_credencial_de_dispositivo_so_grava_origem_sensor(sessao, cenario):
    credencial, _ = emitir_credencial_de_dispositivo(
        sessao,
        operador=cenario["mestre"],
        serie=cenario["serie"],
        identificador="sensor-01",
        trilha_id=cenario["trilha"].id,
    )
    sessao.commit()

    with pytest.raises(ErroDeValidacao) as excinfo:
        gravar_registro_de_coleta(
            sessao,
            operador=cenario["guerreiro"],
            serie=cenario["serie"],
            momento_do_fato=MOMENTO_DA_MEDICAO,
            origem=OrigemDoRegistro.manual.value,
            credencial_de_dispositivo_id=credencial.id,
            valor=25.0,
            unidade="°C",
        )
    assert excinfo.value.campo == "origem"
    assert sessao.query(RegistroDeColeta).count() == 0


def test_manual_e_voz_nao_gravam_credencial(sessao, cenario):
    registro = gravar_registro_de_coleta(
        sessao,
        operador=cenario["guerreiro"],
        serie=cenario["serie"],
        momento_do_fato=MOMENTO_DA_MEDICAO,
        origem=OrigemDoRegistro.manual.value,
        valor=25.0,
        unidade="°C",
    )
    sessao.commit()

    assert registro.credencial_id is None


def test_valor_fora_da_faixa_do_sensor_entra_a_conferir(sessao, cenario):
    credencial, _ = emitir_credencial_de_dispositivo(
        sessao,
        operador=cenario["mestre"],
        serie=cenario["serie"],
        identificador="sensor-01",
        trilha_id=cenario["trilha"].id,
    )
    sessao.commit()

    registro = gravar_registro_de_coleta(
        sessao,
        operador=cenario["guerreiro"],
        serie=cenario["serie"],
        momento_do_fato=MOMENTO_DA_MEDICAO,
        origem=OrigemDoRegistro.sensor.value,
        credencial_de_dispositivo_id=credencial.id,
        valor=999.0,
        unidade="°C",
    )
    sessao.commit()

    assert registro.a_conferir is True
    assert registro.pontos_creditados == 5
