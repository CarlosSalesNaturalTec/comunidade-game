from datetime import UTC, datetime, timedelta
from unittest.mock import patch

import pytest

from nucleo.coletas.modelo import Cadencia, EstadoDaSerie, SerieDeColeta
from nucleo.coletas.regra import (
    abrir_serie_de_coleta,
    apurar_estado_da_serie,
    consultar_series_do_guerreiro,
    gravar_registro_de_coleta,
    periodo_de_cadencia,
)
from nucleo.comunidades.modelo import ComunidadeVirtual
from nucleo.erros import ErroDeValidacao, PermissaoNegada, SerieDeColetaJaAberta
from nucleo.locais.modelo import ORDEM_DOS_NIVEIS, NivelDoLocal
from nucleo.personas.modelo import Papel
from nucleo.tempo import agora


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


def _ancora_ha_n_periodos_completos(referencia: datetime, cadencia: Cadencia, n: int) -> datetime:
    """Um instante dentro do período que está `n` períodos completos antes
    do período de `referencia`, andando pelas bordas de `periodo_de_cadencia`
    em vez de subtrair datas — a mesma régua que a derivação usa (design —
    a régua dos períodos)."""
    limite = referencia
    for _ in range(n):
        inicio_do_periodo, _ = periodo_de_cadencia(limite, cadencia)
        limite = inicio_do_periodo - timedelta(microseconds=1)
    return limite


@pytest.mark.parametrize("cadencia", [Cadencia.diaria, Cadencia.semanal, Cadencia.mensal])
def test_um_periodo_vazio_nao_interrompe(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    cadencia,
):
    """Uma falha isolada não interrompe — só o segundo período completo sem
    registro interrompe (`RN-08-07`)."""
    _, guerreiro, desafio, local = _preparar(
        sessao, criar_persona, criar_trilha, criar_missao, criar_desafio_de_coleta, criar_local
    )
    desafio.cadencia = cadencia
    sessao.commit()

    serie = abrir_serie_de_coleta(sessao, operador=guerreiro, desafio=desafio, local_id=local.id)
    sessao.commit()
    agora_do_teste = agora()
    serie.aberta_em = _ancora_ha_n_periodos_completos(agora_do_teste, cadencia, 1)
    sessao.commit()

    assert apurar_estado_da_serie(sessao, serie) == EstadoDaSerie.ativa


@pytest.mark.parametrize("cadencia", [Cadencia.diaria, Cadencia.semanal, Cadencia.mensal])
def test_dois_periodos_vazios_interrompem_contados_da_abertura(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    cadencia,
):
    """Série sem nenhum registro conta os períodos a partir da data de
    abertura (`RF-08-10`)."""
    _, guerreiro, desafio, local = _preparar(
        sessao, criar_persona, criar_trilha, criar_missao, criar_desafio_de_coleta, criar_local
    )
    desafio.cadencia = cadencia
    sessao.commit()

    serie = abrir_serie_de_coleta(sessao, operador=guerreiro, desafio=desafio, local_id=local.id)
    sessao.commit()
    agora_do_teste = agora()
    serie.aberta_em = _ancora_ha_n_periodos_completos(agora_do_teste, cadencia, 2)
    sessao.commit()

    assert apurar_estado_da_serie(sessao, serie) == EstadoDaSerie.interrompida


def test_encerrada_prevalece_sobre_interrompida_e_nao_retoma(
    sessao, criar_persona, criar_trilha, criar_missao, criar_desafio_de_coleta, criar_local
):
    """A vigência terminada decide primeiro; `encerrada` é terminal (PRD-08
    §§3.1, 8)."""
    _, guerreiro, desafio, local = _preparar(
        sessao, criar_persona, criar_trilha, criar_missao, criar_desafio_de_coleta, criar_local
    )

    serie = abrir_serie_de_coleta(sessao, operador=guerreiro, desafio=desafio, local_id=local.id)
    sessao.commit()
    agora_do_teste = agora()
    serie.aberta_em = _ancora_ha_n_periodos_completos(agora_do_teste, serie.cadencia, 2)
    desafio.vigencia_fim = agora_do_teste - timedelta(days=1)
    sessao.commit()

    assert apurar_estado_da_serie(sessao, serie) == EstadoDaSerie.encerrada

    with pytest.raises(ErroDeValidacao):
        gravar_registro_de_coleta(
            sessao,
            operador=guerreiro,
            serie=serie,
            momento_do_fato=agora_do_teste,
            origem="manual",
            valor=1.0,
            unidade="unidade",
        )
    assert apurar_estado_da_serie(sessao, serie) == EstadoDaSerie.encerrada


def test_leitura_sem_transicao_nao_escreve(
    sessao, criar_persona, criar_trilha, criar_missao, criar_desafio_de_coleta, criar_local
):
    """A guarda de divergência: leitura que não muda o estado não grava o
    espelho (design — Decisions)."""
    _, guerreiro, desafio, local = _preparar(
        sessao, criar_persona, criar_trilha, criar_missao, criar_desafio_de_coleta, criar_local
    )
    serie = abrir_serie_de_coleta(sessao, operador=guerreiro, desafio=desafio, local_id=local.id)
    sessao.commit()

    with patch.object(sessao, "flush", wraps=sessao.flush) as flush_espionado:
        assert apurar_estado_da_serie(sessao, serie) == EstadoDaSerie.ativa
        assert flush_espionado.call_count == 0


def test_leitura_no_instante_da_transicao_grava_o_espelho_uma_unica_vez(
    sessao, criar_persona, criar_trilha, criar_missao, criar_desafio_de_coleta, criar_local
):
    _, guerreiro, desafio, local = _preparar(
        sessao, criar_persona, criar_trilha, criar_missao, criar_desafio_de_coleta, criar_local
    )
    serie = abrir_serie_de_coleta(sessao, operador=guerreiro, desafio=desafio, local_id=local.id)
    sessao.commit()
    agora_do_teste = agora()
    serie.aberta_em = _ancora_ha_n_periodos_completos(agora_do_teste, serie.cadencia, 2)
    sessao.commit()

    with patch.object(sessao, "flush", wraps=sessao.flush) as flush_espionado:
        assert apurar_estado_da_serie(sessao, serie) == EstadoDaSerie.interrompida
        assert flush_espionado.call_count == 1

        flush_espionado.reset_mock()
        assert apurar_estado_da_serie(sessao, serie) == EstadoDaSerie.interrompida
        assert flush_espionado.call_count == 0


def test_consulta_devolve_so_as_series_do_guerreiro_da_sessao(
    sessao, criar_persona, criar_trilha, criar_missao, criar_desafio_de_coleta, criar_local
):
    """A consulta nunca alcança série de outro coletor, mesmo havendo série
    de outro sobre o mesmo desafio e local (`RN-08-04`, `RF-08-17`)."""
    comunidade, primeiro, desafio, local = _preparar(
        sessao, criar_persona, criar_trilha, criar_missao, criar_desafio_de_coleta, criar_local
    )
    segundo = criar_persona(Papel.guerreiro, comunidade=comunidade)

    serie_1 = abrir_serie_de_coleta(sessao, operador=primeiro, desafio=desafio, local_id=local.id)
    sessao.commit()
    abrir_serie_de_coleta(sessao, operador=segundo, desafio=desafio, local_id=local.id)
    sessao.commit()

    pagina = consultar_series_do_guerreiro(sessao, operador=primeiro, cursor=None, tamanho=50)

    assert [item.id for item in pagina.itens] == [serie_1.id]


def test_consulta_apresenta_interrompida_sem_escrita_anterior(
    sessao, criar_persona, criar_trilha, criar_missao, criar_desafio_de_coleta, criar_local
):
    """A consulta apura o estado no próprio ato — não depende de nenhuma
    escrita anterior ter acontecido (`RF-08-10`, `RF-08-17`)."""
    _, guerreiro, desafio, local = _preparar(
        sessao, criar_persona, criar_trilha, criar_missao, criar_desafio_de_coleta, criar_local
    )
    serie = abrir_serie_de_coleta(sessao, operador=guerreiro, desafio=desafio, local_id=local.id)
    sessao.commit()
    agora_do_teste = agora()
    serie.aberta_em = _ancora_ha_n_periodos_completos(agora_do_teste, serie.cadencia, 2)
    sessao.commit()

    pagina = consultar_series_do_guerreiro(sessao, operador=guerreiro, cursor=None, tamanho=50)

    assert len(pagina.itens) == 1
    assert pagina.itens[0].id == serie.id
    assert pagina.itens[0].pontos == 0
    assert pagina.itens[0].estado == EstadoDaSerie.interrompida.value
    assert serie.estado == EstadoDaSerie.interrompida


def test_mestre_nao_consulta_series_do_guerreiro(
    sessao, criar_persona, criar_trilha, criar_missao, criar_desafio_de_coleta, criar_local
):
    _, _, desafio, local = _preparar(
        sessao, criar_persona, criar_trilha, criar_missao, criar_desafio_de_coleta, criar_local
    )
    mestre_qualquer = criar_persona(Papel.mestre)

    with pytest.raises(PermissaoNegada):
        consultar_series_do_guerreiro(sessao, operador=mestre_qualquer, cursor=None, tamanho=50)


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
