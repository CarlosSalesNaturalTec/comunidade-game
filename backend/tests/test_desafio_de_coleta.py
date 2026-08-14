from datetime import UTC, datetime

import pytest
from sqlalchemy import event

from nucleo.coletas.modelo import Cadencia, DesafioDeColeta
from nucleo.coletas.regra import criar_desafio_de_coleta
from nucleo.erros import ErroDeValidacao, PermissaoNegada
from nucleo.locais.modelo import NivelDoLocal
from nucleo.personas.modelo import Papel

INICIO = datetime(2026, 1, 1, tzinfo=UTC)
FIM = datetime(2026, 12, 31, tzinfo=UTC)


def _argumentos_validos(missao, tipo, **sobrescritas):
    argumentos = {
        "missao": missao,
        "tipo_de_coleta_id": tipo.id,
        "cadencia": Cadencia.semanal.value,
        "vigencia_inicio": INICIO,
        "vigencia_fim": FIM,
        "granularidade_exigida": NivelDoLocal.rua.value,
        "registros_que_pontuam_por_periodo": 1,
    }
    argumentos.update(sobrescritas)
    return argumentos


def test_mestre_autor_cria_desafio_na_propria_trilha(
    sessao, criar_persona, criar_trilha, criar_missao, criar_tipo_de_coleta
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    tipo = criar_tipo_de_coleta(mestre)

    desafio = criar_desafio_de_coleta(sessao, operador=mestre, **_argumentos_validos(missao, tipo))
    sessao.commit()

    assert desafio.missao_id == missao.id
    assert desafio.tipo_de_coleta_id == tipo.id
    assert desafio.cadencia == Cadencia.semanal
    assert desafio.autor_id == mestre.id
    assert desafio.papel_do_autor == Papel.mestre.value
    assert desafio.registrado_em is not None


def test_admin_cria_desafio_em_trilha_de_qualquer_mestre(
    sessao, criar_persona, criar_trilha, criar_missao, criar_tipo_de_coleta
):
    autor = criar_persona(Papel.mestre)
    admin = criar_persona(Papel.admin)
    trilha = criar_trilha(autor)
    missao = criar_missao(trilha, autor)
    tipo = criar_tipo_de_coleta(admin)

    desafio = criar_desafio_de_coleta(sessao, operador=admin, **_argumentos_validos(missao, tipo))
    sessao.commit()

    assert desafio.autor_id == admin.id


def test_mestre_que_nao_e_autor_e_recusado(
    sessao, criar_persona, criar_trilha, criar_missao, criar_tipo_de_coleta
):
    autor = criar_persona(Papel.mestre)
    outro_mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(autor)
    missao = criar_missao(trilha, autor)
    tipo = criar_tipo_de_coleta(autor)

    with pytest.raises(PermissaoNegada):
        criar_desafio_de_coleta(sessao, operador=outro_mestre, **_argumentos_validos(missao, tipo))
    assert sessao.query(DesafioDeColeta).count() == 0


def test_missao_inexistente_e_recusada(sessao, criar_persona, criar_tipo_de_coleta):
    mestre = criar_persona(Papel.mestre)
    tipo = criar_tipo_de_coleta(mestre)

    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_desafio_de_coleta(sessao, operador=mestre, **_argumentos_validos(None, tipo))
    assert excinfo.value.campo == "missao_id"
    assert sessao.query(DesafioDeColeta).count() == 0


def test_desafio_sem_tipo_e_recusado(sessao, criar_persona, criar_trilha, criar_missao):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_desafio_de_coleta(
            sessao,
            operador=mestre,
            missao=missao,
            tipo_de_coleta_id=None,
            cadencia=Cadencia.semanal.value,
            vigencia_inicio=INICIO,
            vigencia_fim=FIM,
            granularidade_exigida=NivelDoLocal.rua.value,
            registros_que_pontuam_por_periodo=1,
        )
    assert excinfo.value.campo == "tipo_de_coleta_id"


def test_desafio_sem_cadencia_e_recusado(
    sessao, criar_persona, criar_trilha, criar_missao, criar_tipo_de_coleta
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    tipo = criar_tipo_de_coleta(mestre)

    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_desafio_de_coleta(
            sessao, operador=mestre, **_argumentos_validos(missao, tipo, cadencia=None)
        )
    assert excinfo.value.campo == "cadencia"
    assert sessao.query(DesafioDeColeta).count() == 0


def test_cadencia_fora_das_tres_e_recusada(
    sessao, criar_persona, criar_trilha, criar_missao, criar_tipo_de_coleta
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    tipo = criar_tipo_de_coleta(mestre)

    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_desafio_de_coleta(
            sessao, operador=mestre, **_argumentos_validos(missao, tipo, cadencia="anual")
        )
    assert excinfo.value.campo == "cadencia"


def test_desafio_sem_vigencia_e_recusado(
    sessao, criar_persona, criar_trilha, criar_missao, criar_tipo_de_coleta
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    tipo = criar_tipo_de_coleta(mestre)

    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_desafio_de_coleta(
            sessao, operador=mestre, **_argumentos_validos(missao, tipo, vigencia_inicio=None)
        )
    assert excinfo.value.campo == "vigencia_inicio"


def test_vigencia_invertida_e_recusada(
    sessao, criar_persona, criar_trilha, criar_missao, criar_tipo_de_coleta
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    tipo = criar_tipo_de_coleta(mestre)

    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_desafio_de_coleta(
            sessao,
            operador=mestre,
            **_argumentos_validos(missao, tipo, vigencia_inicio=FIM, vigencia_fim=INICIO),
        )
    assert excinfo.value.campo == "vigencia_fim"


def test_desafio_sem_granularidade_e_recusado(
    sessao, criar_persona, criar_trilha, criar_missao, criar_tipo_de_coleta
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    tipo = criar_tipo_de_coleta(mestre)

    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_desafio_de_coleta(
            sessao,
            operador=mestre,
            **_argumentos_validos(missao, tipo, granularidade_exigida=None),
        )
    assert excinfo.value.campo == "granularidade_exigida"


def test_granularidade_fora_da_hierarquia_e_recusada(
    sessao, criar_persona, criar_trilha, criar_missao, criar_tipo_de_coleta
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    tipo = criar_tipo_de_coleta(mestre)

    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_desafio_de_coleta(
            sessao,
            operador=mestre,
            **_argumentos_validos(missao, tipo, granularidade_exigida="municipio"),
        )
    assert excinfo.value.campo == "granularidade_exigida"


def test_registros_que_pontuam_sem_declaracao_e_recusado(
    sessao, criar_persona, criar_trilha, criar_missao, criar_tipo_de_coleta
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    tipo = criar_tipo_de_coleta(mestre)

    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_desafio_de_coleta(
            sessao,
            operador=mestre,
            **_argumentos_validos(missao, tipo, registros_que_pontuam_por_periodo=None),
        )
    assert excinfo.value.campo == "registros_que_pontuam_por_periodo"


def test_registros_que_pontuam_menor_que_1_e_recusado(
    sessao, criar_persona, criar_trilha, criar_missao, criar_tipo_de_coleta
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    tipo = criar_tipo_de_coleta(mestre)

    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_desafio_de_coleta(
            sessao,
            operador=mestre,
            **_argumentos_validos(missao, tipo, registros_que_pontuam_por_periodo=0),
        )
    assert excinfo.value.campo == "registros_que_pontuam_por_periodo"


def test_granularidade_mais_fina_que_a_de_uma_comunidade_e_aceita(
    sessao, criar_persona, criar_trilha, criar_missao, criar_tipo_de_coleta, criar_comunidade
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    tipo = criar_tipo_de_coleta(mestre)
    criar_comunidade()  # granularidade máxima "bairro", mais grosseira que "quadra"

    desafio = criar_desafio_de_coleta(
        sessao,
        operador=mestre,
        **_argumentos_validos(missao, tipo, granularidade_exigida=NivelDoLocal.quadra.value),
    )
    sessao.commit()

    assert desafio.granularidade_exigida == NivelDoLocal.quadra


def test_criacao_do_desafio_nao_consulta_comunidade(
    sessao, engine, criar_persona, criar_trilha, criar_missao, criar_tipo_de_coleta
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    tipo = criar_tipo_de_coleta(mestre)

    instrucoes_com_comunidade = []

    def _capturar(conexao, cursor, instrucao, parametros, contexto, executemany):
        if "comunidade_virtual" in instrucao.lower():
            instrucoes_com_comunidade.append(instrucao)

    event.listen(engine, "before_cursor_execute", _capturar)
    try:
        criar_desafio_de_coleta(sessao, operador=mestre, **_argumentos_validos(missao, tipo))
    finally:
        event.remove(engine, "before_cursor_execute", _capturar)

    assert instrucoes_com_comunidade == []


def test_desafio_com_tipo_desativado_e_recusado(
    sessao, criar_persona, criar_trilha, criar_missao, criar_tipo_de_coleta
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    tipo = criar_tipo_de_coleta(mestre, ativo=False)

    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_desafio_de_coleta(sessao, operador=mestre, **_argumentos_validos(missao, tipo))
    assert excinfo.value.campo == "tipo_de_coleta_id"
    assert sessao.query(DesafioDeColeta).count() == 0


def test_desativar_tipo_nao_altera_desafio_ja_criado(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_tipo_de_coleta,
    criar_desafio_de_coleta,
):
    from nucleo.coletas.regra import desativar_tipo_de_coleta

    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    tipo = criar_tipo_de_coleta(admin)
    desafio = criar_desafio_de_coleta(missao, mestre, tipo=tipo)

    desativar_tipo_de_coleta(sessao, tipo, operador=admin)
    sessao.commit()
    sessao.refresh(desafio)

    assert desafio.tipo_de_coleta_id == tipo.id


def test_trilha_em_rascunho_sem_desafio_de_coleta_e_aceita(sessao, criar_persona, criar_trilha):
    from nucleo.trilhas.modelo import SituacaoDaTrilha

    mestre = criar_persona(Papel.mestre)

    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.rascunho)

    assert trilha.situacao == SituacaoDaTrilha.rascunho
    assert sessao.query(DesafioDeColeta).filter_by(missao_id=None).count() == 0
