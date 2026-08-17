from datetime import UTC, datetime, timedelta

import pytest

from nucleo.coletas.modelo import OrigemDoRegistro, RegistroDeColeta, SituacaoDoRegistro
from nucleo.coletas.regra import (
    abrir_serie_de_coleta,
    compor_amostra_de_auditoria,
    confirmar_registro_de_coleta,
    gravar_registro_de_coleta,
    invalidar_registro_de_coleta,
)
from nucleo.comunidades.modelo import ComunidadeVirtual, VinculoJogador
from nucleo.erros import (
    ConfirmacaoDeRegistroInvalidadoRecusada,
    ErroDeValidacao,
    NaoEncontrado,
    PermissaoNegada,
)
from nucleo.locais.modelo import ORDEM_DOS_NIVEIS, NivelDoLocal
from nucleo.personas.modelo import Papel
from nucleo.pontuacao.modelo import PontoRegular
from nucleo.tempo import agora

# O vínculo do Guerreiro(a) nasce bem no passado para que qualquer data de
# medição usada nos testes — passada ou "agora" — caia dentro do intervalo
# vigente (`RN-08-03`), como em test_registro_de_coleta.py.
INICIO_DO_VINCULO = datetime(2020, 1, 1, tzinfo=UTC)


def _criar_comunidade(sessao) -> ComunidadeVirtual:
    comunidade = ComunidadeVirtual(
        nome="Comunidade de Teste", localizacao="Bairro de teste", granularidade_maxima="quadra"
    )
    sessao.add(comunidade)
    sessao.commit()
    sessao.refresh(comunidade)
    return comunidade


def _criar_local_no_nivel(criar_local, comunidade, nivel: NivelDoLocal):
    indice = ORDEM_DOS_NIVEIS.index(nivel)
    pai = None
    local = None
    for indice_atual in range(indice + 1):
        nivel_atual = ORDEM_DOS_NIVEIS[indice_atual]
        local = criar_local(
            comunidade, nivel=nivel_atual, rotulo=f"{nivel_atual.value} de teste", local_pai=pai
        )
        pai = local
    return local


def _preparar_cenario(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
    *,
    registros_que_pontuam_por_periodo=1,
    mestre=None,
    declarar_poder_do_territorio=True,
):
    comunidade = _criar_comunidade(sessao)
    admin = criar_persona(Papel.admin)
    if declarar_poder_do_territorio:
        criar_poder_do_territorio(admin)
    mestre = mestre or criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    desafio = criar_desafio_de_coleta(
        missao,
        mestre,
        granularidade_exigida=NivelDoLocal.rua,
        registros_que_pontuam_por_periodo=registros_que_pontuam_por_periodo,
        vigencia_inicio=agora() - timedelta(days=3650),
        vigencia_fim=agora() + timedelta(days=3650),
    )
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


def _gravar(sessao, guerreiro, serie, momento, valor=25.0):
    registro = gravar_registro_de_coleta(
        sessao,
        operador=guerreiro,
        serie=serie,
        momento_do_fato=momento,
        origem=OrigemDoRegistro.manual.value,
        valor=valor,
        unidade="°C",
    )
    sessao.commit()
    return registro


# --- Composição da amostra (RN-08-20) --------------------------------------


def test_amostra_com_trinta_registros_na_semana_rende_tres(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
    criar_registro_de_coleta,
):
    cen = _preparar_cenario(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
    )
    for indice in range(30):
        criar_registro_de_coleta(
            cen["serie"],
            cen["guerreiro"],
            cen["comunidade"].id,
            momento_do_fato=agora() - timedelta(hours=indice),
        )

    amostra = compor_amostra_de_auditoria(sessao, operador=cen["mestre"])

    assert len(amostra) == 3
    assert all(registro.serie_de_coleta_id == cen["serie"].id for registro in amostra)


def test_amostra_com_quatro_registros_na_semana_rende_um_pelo_piso(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
    criar_registro_de_coleta,
):
    cen = _preparar_cenario(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
    )
    for indice in range(4):
        criar_registro_de_coleta(
            cen["serie"],
            cen["guerreiro"],
            cen["comunidade"].id,
            momento_do_fato=agora() - timedelta(hours=indice),
        )

    amostra = compor_amostra_de_auditoria(sessao, operador=cen["mestre"])

    assert len(amostra) == 1


def test_amostra_inclui_todo_a_conferir_alem_do_percentual(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
    criar_registro_de_coleta,
):
    cen = _preparar_cenario(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
    )
    a_conferir_ids = set()
    for indice in range(5):
        registro = criar_registro_de_coleta(
            cen["serie"],
            cen["guerreiro"],
            cen["comunidade"].id,
            momento_do_fato=agora() - timedelta(hours=indice),
            a_conferir=True,
            pontos_creditados=0,
        )
        a_conferir_ids.add(registro.id)
    for indice in range(25):
        criar_registro_de_coleta(
            cen["serie"],
            cen["guerreiro"],
            cen["comunidade"].id,
            momento_do_fato=agora() - timedelta(hours=10 + indice),
        )

    amostra = compor_amostra_de_auditoria(sessao, operador=cen["mestre"])

    assert len(amostra) == 8
    ids_da_amostra = {registro.id for registro in amostra}
    assert a_conferir_ids <= ids_da_amostra
    assert len(ids_da_amostra - a_conferir_ids) == 3


def test_amostra_de_serie_so_com_a_conferir_entrega_todos(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
    criar_registro_de_coleta,
):
    cen = _preparar_cenario(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
    )
    for indice in range(2):
        criar_registro_de_coleta(
            cen["serie"],
            cen["guerreiro"],
            cen["comunidade"].id,
            momento_do_fato=agora() - timedelta(hours=indice),
            a_conferir=True,
            pontos_creditados=0,
        )

    amostra = compor_amostra_de_auditoria(sessao, operador=cen["mestre"])

    assert len(amostra) == 2


def test_amostra_nao_traz_a_conferir_ja_auditado(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
    criar_registro_de_coleta,
):
    cen = _preparar_cenario(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
    )
    ja_auditado = criar_registro_de_coleta(
        cen["serie"],
        cen["guerreiro"],
        cen["comunidade"].id,
        momento_do_fato=agora() - timedelta(hours=1),
        a_conferir=True,
        pontos_creditados=0,
    )
    ja_auditado.auditado_em = agora()
    ja_auditado.auditado_por_id = cen["mestre"].id
    sessao.commit()

    amostra = compor_amostra_de_auditoria(sessao, operador=cen["mestre"])

    assert amostra == []


def test_amostra_nao_alcanca_serie_sem_registro_na_semana(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
):
    cen = _preparar_cenario(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
    )

    amostra = compor_amostra_de_auditoria(sessao, operador=cen["mestre"])

    assert amostra == []


def test_amostra_nao_alcanca_serie_de_desafio_alheio(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
    criar_registro_de_coleta,
):
    cen_1 = _preparar_cenario(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
        declarar_poder_do_territorio=True,
    )
    cen_2 = _preparar_cenario(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
        declarar_poder_do_territorio=False,
    )
    criar_registro_de_coleta(
        cen_2["serie"], cen_2["guerreiro"], cen_2["comunidade"].id, momento_do_fato=agora()
    )

    amostra = compor_amostra_de_auditoria(sessao, operador=cen_1["mestre"])

    assert amostra == []


def test_amostra_nao_alcanca_serie_interrompida(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
    criar_registro_de_coleta,
):
    cen = _preparar_cenario(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
    )
    # Cadência semanal: uma âncora a 30 dias derruba a série para
    # interrompida, ainda que haja registro dentro da semana do pedido.
    cen["serie"].ultima_medicao_valida_em = agora() - timedelta(days=30)
    sessao.commit()
    criar_registro_de_coleta(
        cen["serie"], cen["guerreiro"], cen["comunidade"].id, momento_do_fato=agora()
    )

    amostra = compor_amostra_de_auditoria(sessao, operador=cen["mestre"])

    assert amostra == []


def test_amostra_nao_alcanca_serie_encerrada(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
    criar_registro_de_coleta,
):
    cen = _preparar_cenario(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
    )
    cen["desafio"].vigencia_fim = agora() - timedelta(days=1)
    sessao.commit()
    criar_registro_de_coleta(
        cen["serie"], cen["guerreiro"], cen["comunidade"].id, momento_do_fato=agora()
    )

    amostra = compor_amostra_de_auditoria(sessao, operador=cen["mestre"])

    assert amostra == []


def test_amostra_recusada_para_quem_nao_e_mestre(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
):
    cen = _preparar_cenario(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
    )

    with pytest.raises(PermissaoNegada):
        compor_amostra_de_auditoria(sessao, operador=cen["guerreiro"])


# --- Confirmação (RF-08-29, RN-08-26) ---------------------------------------


def test_confirmar_a_conferir_credita_pela_regua_do_registro_valido(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
    criar_registro_de_coleta,
):
    cen = _preparar_cenario(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
    )
    registro = criar_registro_de_coleta(
        cen["serie"],
        cen["guerreiro"],
        cen["comunidade"].id,
        momento_do_fato=datetime(2026, 7, 6, 10, 0, tzinfo=UTC),
        a_conferir=True,
        pontos_creditados=0,
    )

    confirmado = confirmar_registro_de_coleta(sessao, registro, operador=cen["mestre"])
    sessao.commit()

    assert confirmado.pontos_creditados == 5
    assert confirmado.situacao == SituacaoDoRegistro.valida
    assert confirmado.auditado_em is not None
    assert confirmado.auditado_por_id == cen["mestre"].id
    conta = (
        sessao.query(PontoRegular)
        .filter_by(guerreiro_id=cen["guerreiro"].id)
        .filter(PontoRegular.poder_id.isnot(None))
        .one()
    )
    assert conta.total == 5


def test_confirmar_registro_ja_valido_nao_credita_de_novo(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
    criar_registro_de_coleta,
):
    cen = _preparar_cenario(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
    )
    registro = criar_registro_de_coleta(
        cen["serie"],
        cen["guerreiro"],
        cen["comunidade"].id,
        momento_do_fato=datetime(2026, 7, 6, 10, 0, tzinfo=UTC),
        a_conferir=False,
        pontos_creditados=5,
    )

    confirmado = confirmar_registro_de_coleta(sessao, registro, operador=cen["mestre"])
    sessao.commit()

    assert confirmado.pontos_creditados == 5
    assert confirmado.auditado_em is not None
    assert sessao.query(PontoRegular).count() == 0


def test_confirmar_a_conferir_fora_da_quantidade_do_periodo_credita_zero(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
    criar_registro_de_coleta,
):
    cen = _preparar_cenario(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
        registros_que_pontuam_por_periodo=1,
    )
    # Mesma semana civil: o primeiro já pontuou, esgotando a única vaga.
    criar_registro_de_coleta(
        cen["serie"],
        cen["guerreiro"],
        cen["comunidade"].id,
        momento_do_fato=datetime(2026, 7, 6, 10, 0, tzinfo=UTC),
        pontos_creditados=5,
    )
    a_conferir = criar_registro_de_coleta(
        cen["serie"],
        cen["guerreiro"],
        cen["comunidade"].id,
        momento_do_fato=datetime(2026, 7, 7, 10, 0, tzinfo=UTC),
        a_conferir=True,
        pontos_creditados=0,
    )

    confirmado = confirmar_registro_de_coleta(sessao, a_conferir, operador=cen["mestre"])
    sessao.commit()

    assert confirmado.pontos_creditados == 0
    assert confirmado.situacao == SituacaoDoRegistro.valida
    assert confirmado.auditado_em is not None


def test_confirmar_duas_vezes_nao_credita_duas_vezes(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
    criar_registro_de_coleta,
):
    cen = _preparar_cenario(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
    )
    registro = criar_registro_de_coleta(
        cen["serie"],
        cen["guerreiro"],
        cen["comunidade"].id,
        momento_do_fato=datetime(2026, 7, 6, 10, 0, tzinfo=UTC),
        a_conferir=True,
        pontos_creditados=0,
    )

    confirmar_registro_de_coleta(sessao, registro, operador=cen["mestre"])
    sessao.commit()
    confirmar_registro_de_coleta(sessao, registro, operador=cen["mestre"])
    sessao.commit()

    conta = sessao.query(PontoRegular).filter_by(guerreiro_id=cen["guerreiro"].id).one()
    assert conta.total == 5


def test_confirmar_registro_inexistente_e_404(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
):
    cen = _preparar_cenario(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
    )

    with pytest.raises(NaoEncontrado):
        confirmar_registro_de_coleta(sessao, None, operador=cen["mestre"])


# --- Invalidação (RF-08-13, RN-08-09, RN-08-10) -----------------------------


def test_invalidar_registro_que_creditou_estorna_o_valor_exato(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
):
    cen = _preparar_cenario(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
    )
    registro = _gravar(sessao, cen["guerreiro"], cen["serie"], agora() - timedelta(days=1))
    assert registro.pontos_creditados == 5
    conta_antes = (
        sessao.query(PontoRegular)
        .filter_by(guerreiro_id=cen["guerreiro"].id)
        .filter(PontoRegular.poder_id.isnot(None))
        .one()
    )
    assert conta_antes.total == 5

    invalidado = invalidar_registro_de_coleta(
        sessao, registro, operador=cen["mestre"], motivo="Medição implausível."
    )
    sessao.commit()

    assert invalidado.situacao == SituacaoDoRegistro.invalidada
    assert invalidado.motivo_da_invalidacao == "Medição implausível."
    assert invalidado.auditado_por_id == cen["mestre"].id
    assert invalidado.auditado_em is not None
    conta_depois = sessao.query(PontoRegular).filter_by(id=conta_antes.id).one()
    assert conta_depois.total == 0


def test_invalidar_a_conferir_nao_confirmado_estorna_zero(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
    criar_registro_de_coleta,
):
    cen = _preparar_cenario(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
        declarar_poder_do_territorio=False,
    )
    registro = criar_registro_de_coleta(
        cen["serie"],
        cen["guerreiro"],
        cen["comunidade"].id,
        a_conferir=True,
        pontos_creditados=0,
    )

    invalidado = invalidar_registro_de_coleta(
        sessao, registro, operador=cen["mestre"], motivo="Foto não corresponde ao local."
    )
    sessao.commit()

    assert invalidado.situacao == SituacaoDoRegistro.invalidada
    assert sessao.query(PontoRegular).count() == 0


def test_invalidar_excedente_do_periodo_estorna_zero(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
    criar_registro_de_coleta,
):
    cen = _preparar_cenario(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
        declarar_poder_do_territorio=False,
    )
    registro = criar_registro_de_coleta(
        cen["serie"],
        cen["guerreiro"],
        cen["comunidade"].id,
        a_conferir=False,
        pontos_creditados=0,
    )

    invalidado = invalidar_registro_de_coleta(
        sessao, registro, operador=cen["mestre"], motivo="Excedente do período."
    )
    sessao.commit()

    assert invalidado.situacao == SituacaoDoRegistro.invalidada
    assert sessao.query(PontoRegular).count() == 0


def test_invalidacao_sem_motivo_e_recusada(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
    criar_registro_de_coleta,
):
    cen = _preparar_cenario(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
        declarar_poder_do_territorio=False,
    )
    registro = criar_registro_de_coleta(cen["serie"], cen["guerreiro"], cen["comunidade"].id)

    with pytest.raises(ErroDeValidacao) as excinfo:
        invalidar_registro_de_coleta(sessao, registro, operador=cen["mestre"], motivo="   ")
    assert excinfo.value.campo == "motivo"

    intacto = sessao.query(RegistroDeColeta).filter_by(id=registro.id).one()
    assert intacto.situacao == SituacaoDoRegistro.valida


def test_registro_invalidado_continua_consultavel(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
    criar_registro_de_coleta,
):
    cen = _preparar_cenario(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
        declarar_poder_do_territorio=False,
    )
    registro = criar_registro_de_coleta(
        cen["serie"], cen["guerreiro"], cen["comunidade"].id, pontos_creditados=0
    )

    invalidar_registro_de_coleta(
        sessao, registro, operador=cen["mestre"], motivo="Motivo qualquer."
    )
    sessao.commit()

    consultado = sessao.query(RegistroDeColeta).filter_by(id=registro.id).one()
    assert consultado.situacao == SituacaoDoRegistro.invalidada
    assert consultado.motivo_da_invalidacao == "Motivo qualquer."
    assert consultado.auditado_por_id == cen["mestre"].id


def test_vaga_liberada_pela_invalidacao_nao_credita_outro_registro(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
):
    cen = _preparar_cenario(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
        registros_que_pontuam_por_periodo=1,
    )
    primeiro = _gravar(
        sessao, cen["guerreiro"], cen["serie"], datetime(2026, 7, 6, 10, 0, tzinfo=UTC)
    )
    segundo = _gravar(
        sessao, cen["guerreiro"], cen["serie"], datetime(2026, 7, 7, 10, 0, tzinfo=UTC)
    )
    assert primeiro.pontos_creditados == 5
    assert segundo.pontos_creditados == 0

    invalidar_registro_de_coleta(
        sessao, primeiro, operador=cen["mestre"], motivo="Motivo qualquer."
    )
    sessao.commit()

    segundo_apos = sessao.query(RegistroDeColeta).filter_by(id=segundo.id).one()
    assert segundo_apos.pontos_creditados == 0
    assert segundo_apos.situacao == SituacaoDoRegistro.valida


def test_confirmar_registro_invalidado_e_recusado(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
    criar_registro_de_coleta,
):
    cen = _preparar_cenario(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
        declarar_poder_do_territorio=False,
    )
    registro = criar_registro_de_coleta(
        cen["serie"], cen["guerreiro"], cen["comunidade"].id, pontos_creditados=0
    )
    invalidar_registro_de_coleta(
        sessao, registro, operador=cen["mestre"], motivo="Motivo qualquer."
    )
    sessao.commit()

    with pytest.raises(ConfirmacaoDeRegistroInvalidadoRecusada):
        confirmar_registro_de_coleta(sessao, registro, operador=cen["mestre"])

    intacto = sessao.query(RegistroDeColeta).filter_by(id=registro.id).one()
    assert intacto.situacao == SituacaoDoRegistro.invalidada


def test_invalidar_de_novo_nao_estorna_de_novo(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
):
    cen = _preparar_cenario(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
    )
    registro = _gravar(sessao, cen["guerreiro"], cen["serie"], agora() - timedelta(days=1))

    invalidar_registro_de_coleta(
        sessao, registro, operador=cen["mestre"], motivo="Primeiro motivo."
    )
    sessao.commit()
    invalidar_registro_de_coleta(sessao, registro, operador=cen["mestre"], motivo="Segundo motivo.")
    sessao.commit()

    conta = sessao.query(PontoRegular).filter_by(guerreiro_id=cen["guerreiro"].id).one()
    assert conta.total == 0


# --- Permissões (RF-08-13, RF-08-29) ----------------------------------------


def test_confirmar_recusado_para_mestre_que_nao_e_autor_do_desafio(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
    criar_registro_de_coleta,
):
    cen = _preparar_cenario(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
        declarar_poder_do_territorio=False,
    )
    outro_mestre = criar_persona(Papel.mestre)
    registro = criar_registro_de_coleta(
        cen["serie"], cen["guerreiro"], cen["comunidade"].id, a_conferir=True, pontos_creditados=0
    )

    with pytest.raises(PermissaoNegada):
        confirmar_registro_de_coleta(sessao, registro, operador=outro_mestre)

    intacto = sessao.query(RegistroDeColeta).filter_by(id=registro.id).one()
    assert intacto.pontos_creditados == 0
    assert intacto.auditado_em is None


def test_invalidar_recusado_para_guerreiro_sobre_o_proprio_registro(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
    criar_registro_de_coleta,
):
    cen = _preparar_cenario(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
        declarar_poder_do_territorio=False,
    )
    registro = criar_registro_de_coleta(cen["serie"], cen["guerreiro"], cen["comunidade"].id)

    with pytest.raises(PermissaoNegada):
        invalidar_registro_de_coleta(
            sessao, registro, operador=cen["guerreiro"], motivo="Motivo qualquer."
        )

    intacto = sessao.query(RegistroDeColeta).filter_by(id=registro.id).one()
    assert intacto.situacao == SituacaoDoRegistro.valida


def test_admin_nao_audita_no_lugar_do_mestre(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
    criar_registro_de_coleta,
):
    """Spec — auditoria-da-coleta: a auditoria é mais estreita que a posse
    geral da trilha, e nem o Admin audita no lugar do Mestre autor."""
    cen = _preparar_cenario(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
        declarar_poder_do_territorio=False,
    )
    registro = criar_registro_de_coleta(cen["serie"], cen["guerreiro"], cen["comunidade"].id)

    with pytest.raises(PermissaoNegada):
        invalidar_registro_de_coleta(
            sessao, registro, operador=cen["admin"], motivo="Motivo qualquer."
        )
