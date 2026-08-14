from datetime import UTC, datetime, timedelta

import pytest

from nucleo.coletas.modelo import EstadoDaSerie, SerieDeColeta
from nucleo.coletas.regra import abrir_serie_de_coleta
from nucleo.comunidades.modelo import ComunidadeVirtual
from nucleo.erros import ErroDeValidacao, PermissaoNegada, SerieDeColetaJaAberta
from nucleo.locais.modelo import ORDEM_DOS_NIVEIS, NivelDoLocal
from nucleo.personas.modelo import Papel


def _criar_comunidade(sessao, granularidade_maxima: str = "quadra") -> ComunidadeVirtual:
    comunidade = ComunidadeVirtual(
        nome="Comunidade de Teste",
        localizacao="Bairro de teste",
        granularidade_maxima=granularidade_maxima,
    )
    sessao.add(comunidade)
    sessao.commit()
    sessao.refresh(comunidade)
    return comunidade


def _criar_local_no_nivel(criar_local, comunidade, nivel: NivelDoLocal):
    """A hierarquia territorial exige o pai do nível imediatamente acima
    (`RF-08-04`) — monta a cadeia até `nivel`, começando em `comunidade`."""
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


def _preparar(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    *,
    granularidade_maxima="quadra",
    granularidade_exigida=NivelDoLocal.rua,
):
    comunidade = _criar_comunidade(sessao, granularidade_maxima)
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    desafio = criar_desafio_de_coleta(missao, mestre, granularidade_exigida=granularidade_exigida)
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    local = _criar_local_no_nivel(criar_local, comunidade, granularidade_exigida)
    return comunidade, guerreiro, desafio, local


def test_guerreiro_abre_serie_sobre_desafio_vigente_e_local_da_comunidade(
    sessao, criar_persona, criar_trilha, criar_missao, criar_desafio_de_coleta, criar_local
):
    _, guerreiro, desafio, local = _preparar(
        sessao, criar_persona, criar_trilha, criar_missao, criar_desafio_de_coleta, criar_local
    )

    serie = abrir_serie_de_coleta(sessao, operador=guerreiro, desafio=desafio, local_id=local.id)
    sessao.commit()

    assert serie.estado == EstadoDaSerie.ativa
    assert serie.coletor_id == guerreiro.id
    assert serie.local_id == local.id
    assert serie.cadencia == desafio.cadencia
    assert serie.aberta_em is not None


def test_local_de_outra_comunidade_e_recusado(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
):
    _, guerreiro, desafio, _ = _preparar(
        sessao, criar_persona, criar_trilha, criar_missao, criar_desafio_de_coleta, criar_local
    )
    outra_comunidade = _criar_comunidade(sessao)
    local_de_outra = _criar_local_no_nivel(criar_local, outra_comunidade, NivelDoLocal.rua)

    with pytest.raises(PermissaoNegada):
        abrir_serie_de_coleta(
            sessao, operador=guerreiro, desafio=desafio, local_id=local_de_outra.id
        )
    assert sessao.query(SerieDeColeta).count() == 0


def test_desafio_fora_da_vigencia_e_recusado(
    sessao, criar_persona, criar_trilha, criar_missao, criar_desafio_de_coleta, criar_local
):
    comunidade = _criar_comunidade(sessao)
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    desafio = criar_desafio_de_coleta(
        missao,
        mestre,
        vigencia_inicio=datetime(2020, 1, 1, tzinfo=UTC),
        vigencia_fim=datetime(2020, 12, 31, tzinfo=UTC),
    )
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    local = _criar_local_no_nivel(criar_local, comunidade, NivelDoLocal.rua)

    with pytest.raises(ErroDeValidacao) as excinfo:
        abrir_serie_de_coleta(sessao, operador=guerreiro, desafio=desafio, local_id=local.id)
    assert excinfo.value.campo == "desafio_de_coleta_id"
    assert sessao.query(SerieDeColeta).count() == 0


def test_mestre_nao_abre_serie(
    sessao, criar_persona, criar_trilha, criar_missao, criar_desafio_de_coleta, criar_local
):
    _, _, desafio, local = _preparar(
        sessao, criar_persona, criar_trilha, criar_missao, criar_desafio_de_coleta, criar_local
    )
    mestre_qualquer = criar_persona(Papel.mestre)

    with pytest.raises(PermissaoNegada):
        abrir_serie_de_coleta(sessao, operador=mestre_qualquer, desafio=desafio, local_id=local.id)
    assert sessao.query(SerieDeColeta).count() == 0


def test_granularidade_exigida_mais_fina_que_o_teto_e_recusada(
    sessao, criar_persona, criar_trilha, criar_missao, criar_desafio_de_coleta, criar_local
):
    comunidade = _criar_comunidade(sessao, granularidade_maxima="rua")
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    desafio = criar_desafio_de_coleta(missao, mestre, granularidade_exigida=NivelDoLocal.quadra)
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    local = _criar_local_no_nivel(criar_local, comunidade, NivelDoLocal.quadra)

    with pytest.raises(ErroDeValidacao) as excinfo:
        abrir_serie_de_coleta(sessao, operador=guerreiro, desafio=desafio, local_id=local.id)
    assert excinfo.value.campo == "desafio_de_coleta_id"
    assert sessao.query(SerieDeColeta).count() == 0


def test_granularidade_exigida_dentro_do_teto_e_aceita(
    sessao, criar_persona, criar_trilha, criar_missao, criar_desafio_de_coleta, criar_local
):
    comunidade = _criar_comunidade(sessao, granularidade_maxima="quadra")
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    desafio = criar_desafio_de_coleta(missao, mestre, granularidade_exigida=NivelDoLocal.rua)
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    local = _criar_local_no_nivel(criar_local, comunidade, NivelDoLocal.rua)

    serie = abrir_serie_de_coleta(sessao, operador=guerreiro, desafio=desafio, local_id=local.id)
    sessao.commit()

    assert serie.id is not None


def test_local_de_nivel_diferente_da_granularidade_exigida_e_recusado(
    sessao, criar_persona, criar_trilha, criar_missao, criar_desafio_de_coleta, criar_local
):
    comunidade = _criar_comunidade(sessao)
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    desafio = criar_desafio_de_coleta(missao, mestre, granularidade_exigida=NivelDoLocal.rua)
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    local_de_bairro = _criar_local_no_nivel(criar_local, comunidade, NivelDoLocal.bairro)

    with pytest.raises(ErroDeValidacao) as excinfo:
        abrir_serie_de_coleta(
            sessao, operador=guerreiro, desafio=desafio, local_id=local_de_bairro.id
        )
    assert excinfo.value.campo == "local_id"
    assert sessao.query(SerieDeColeta).count() == 0


def test_coletor_informado_no_corpo_e_ignorado(
    sessao, criar_persona, criar_trilha, criar_missao, criar_desafio_de_coleta, criar_local
):
    """A `abrir_serie_de_coleta` nem sequer aceita coletor por parâmetro —
    quem chama a rota informando outro coletor no corpo tem esse campo
    ignorado no schema de entrada (`RN-08-04`); aqui a regra prova que a
    série sempre nasce do `operador`."""
    _, guerreiro, desafio, local = _preparar(
        sessao, criar_persona, criar_trilha, criar_missao, criar_desafio_de_coleta, criar_local
    )

    serie = abrir_serie_de_coleta(sessao, operador=guerreiro, desafio=desafio, local_id=local.id)
    sessao.commit()

    assert serie.coletor_id == guerreiro.id


def test_serie_duplicada_do_mesmo_par_e_recusada(
    sessao, criar_persona, criar_trilha, criar_missao, criar_desafio_de_coleta, criar_local
):
    _, guerreiro, desafio, local = _preparar(
        sessao, criar_persona, criar_trilha, criar_missao, criar_desafio_de_coleta, criar_local
    )
    abrir_serie_de_coleta(sessao, operador=guerreiro, desafio=desafio, local_id=local.id)
    sessao.commit()

    with pytest.raises(SerieDeColetaJaAberta):
        abrir_serie_de_coleta(sessao, operador=guerreiro, desafio=desafio, local_id=local.id)
    assert sessao.query(SerieDeColeta).count() == 1


def test_dois_guerreiros_abrem_series_independentes_sobre_o_mesmo_par(
    sessao, criar_persona, criar_trilha, criar_missao, criar_desafio_de_coleta, criar_local
):
    comunidade, primeiro, desafio, local = _preparar(
        sessao, criar_persona, criar_trilha, criar_missao, criar_desafio_de_coleta, criar_local
    )
    segundo = criar_persona(Papel.guerreiro, comunidade=comunidade)

    serie_1 = abrir_serie_de_coleta(sessao, operador=primeiro, desafio=desafio, local_id=local.id)
    sessao.commit()
    serie_2 = abrir_serie_de_coleta(sessao, operador=segundo, desafio=desafio, local_id=local.id)
    sessao.commit()

    assert serie_1.id != serie_2.id
    assert sessao.query(SerieDeColeta).count() == 2


def test_serie_permanece_ativa_apos_dois_periodos_sem_registro(
    sessao, criar_persona, criar_trilha, criar_missao, criar_desafio_de_coleta, criar_local
):
    """A transição para `interrompida` é `RF-08-10`, de entrega posterior —
    nesta fatia a série não muda de estado."""
    _, guerreiro, desafio, local = _preparar(
        sessao, criar_persona, criar_trilha, criar_missao, criar_desafio_de_coleta, criar_local
    )

    serie = abrir_serie_de_coleta(sessao, operador=guerreiro, desafio=desafio, local_id=local.id)
    sessao.commit()
    serie.aberta_em = datetime.now(UTC) - timedelta(weeks=3)
    sessao.commit()
    sessao.refresh(serie)

    assert serie.estado == EstadoDaSerie.ativa


def test_data_da_ultima_medicao_valida_acompanha_a_serie(
    sessao, criar_persona, criar_trilha, criar_missao, criar_desafio_de_coleta, criar_local
):
    _, guerreiro, desafio, local = _preparar(
        sessao, criar_persona, criar_trilha, criar_missao, criar_desafio_de_coleta, criar_local
    )

    serie = abrir_serie_de_coleta(sessao, operador=guerreiro, desafio=desafio, local_id=local.id)
    sessao.commit()

    assert serie.ultima_medicao_valida_em is None


def test_serie_sem_local_e_recusada(
    sessao, criar_persona, criar_trilha, criar_missao, criar_desafio_de_coleta, criar_local
):
    _, guerreiro, desafio, _ = _preparar(
        sessao, criar_persona, criar_trilha, criar_missao, criar_desafio_de_coleta, criar_local
    )

    with pytest.raises(ErroDeValidacao) as excinfo:
        abrir_serie_de_coleta(sessao, operador=guerreiro, desafio=desafio, local_id=None)
    assert excinfo.value.campo == "local_id"


def test_serie_sem_desafio_e_recusada(sessao, criar_persona):
    guerreiro = criar_persona(Papel.guerreiro)

    with pytest.raises(ErroDeValidacao) as excinfo:
        abrir_serie_de_coleta(sessao, operador=guerreiro, desafio=None, local_id=None)
    assert excinfo.value.campo == "desafio_de_coleta_id"
