from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy import func

from nucleo.armazenamento.disco import ArmazenamentoEmDisco
from nucleo.coletas.modelo import (
    EstadoDaSerie,
    FormaDeRegistro,
    OrigemDoRegistro,
    RegistroDeColeta,
)
from nucleo.coletas.regra import (
    abrir_serie_de_coleta,
    apurar_estado_da_serie,
    gravar_registro_de_coleta,
    periodo_de_cadencia,
)
from nucleo.comunidades.modelo import ComunidadeVirtual, VinculoJogador
from nucleo.erros import ErroDeValidacao, PermissaoNegada
from nucleo.locais.modelo import ORDEM_DOS_NIVEIS, NivelDoLocal
from nucleo.personas.modelo import Papel
from nucleo.tempo import agora

# Todos os cenários gravam medição em 2026, mas o vínculo do Guerreiro(a)
# nasce no instante real do teste (server_default) — recuar o início do
# vínculo garante que a data da medição, no passado simulado, sempre caia
# dentro do intervalo vigente (`RN-08-03`).
INICIO_DO_VINCULO = datetime(2025, 1, 1, tzinfo=UTC)

MOMENTO_DA_MEDICAO = datetime(2026, 8, 12, 14, 0, tzinfo=UTC)  # quarta-feira


def _ancora_ha_n_periodos_completos(referencia: datetime, cadencia, n: int) -> datetime:
    """Mesma régua de `test_serie_de_coleta.py`: um instante dentro do
    período que está `n` períodos completos antes do período de
    `referencia`, andando pelas bordas de `periodo_de_cadencia`."""
    limite = referencia
    for _ in range(n):
        inicio_do_periodo, _ = periodo_de_cadencia(limite, cadencia)
        limite = inicio_do_periodo - timedelta(microseconds=1)
    return limite


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


def _preparar_serie(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
    *,
    forma_de_registro=FormaDeRegistro.numero,
    unidade="°C",
    faixa_minima=-10.0,
    faixa_maxima=55.0,
    registros_que_pontuam_por_periodo=1,
    vigencia_inicio=None,
    vigencia_fim=None,
):
    comunidade = _criar_comunidade(sessao)
    admin = criar_persona(Papel.admin)
    criar_poder_do_territorio(admin)
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    tipo = _cadastrar_tipo(sessao, admin, forma_de_registro, unidade, faixa_minima, faixa_maxima)
    desafio = criar_desafio_de_coleta(
        missao,
        mestre,
        tipo=tipo,
        granularidade_exigida=NivelDoLocal.rua,
        registros_que_pontuam_por_periodo=registros_que_pontuam_por_periodo,
        vigencia_inicio=vigencia_inicio or datetime(2026, 1, 1, tzinfo=UTC),
        vigencia_fim=vigencia_fim or datetime(2026, 12, 31, tzinfo=UTC),
    )
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    vinculo = sessao.query(VinculoJogador).filter_by(guerreiro_id=guerreiro.id).one()
    vinculo.data_inicio = INICIO_DO_VINCULO
    sessao.commit()
    local = _criar_local_no_nivel(criar_local, comunidade, NivelDoLocal.rua)
    serie = abrir_serie_de_coleta(sessao, operador=guerreiro, desafio=desafio, local_id=local.id)
    sessao.commit()
    return comunidade, guerreiro, serie, desafio, tipo


def _cadastrar_tipo(sessao, admin, forma, unidade, faixa_minima, faixa_maxima):
    from nucleo.coletas.regra import cadastrar_tipo_de_coleta

    if forma == FormaDeRegistro.numero:
        tipo = cadastrar_tipo_de_coleta(
            sessao,
            operador=admin,
            nome="Temperatura",
            forma_de_registro=forma.value,
            unidade=unidade,
            faixa_minima=faixa_minima,
            faixa_maxima=faixa_maxima,
        )
    else:
        tipo = cadastrar_tipo_de_coleta(
            sessao, operador=admin, nome="Foto do ponto de coleta", forma_de_registro=forma.value
        )
    sessao.commit()
    return tipo


def test_coletor_grava_medicao_na_sua_serie(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
):
    _, guerreiro, serie, _, _ = _preparar_serie(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
    )

    registro = gravar_registro_de_coleta(
        sessao,
        operador=guerreiro,
        serie=serie,
        momento_do_fato=MOMENTO_DA_MEDICAO,
        origem=OrigemDoRegistro.manual.value,
        valor=25.0,
        unidade="°C",
    )
    sessao.commit()

    assert registro.autor_id == guerreiro.id
    assert registro.momento_do_fato == MOMENTO_DA_MEDICAO
    assert registro.momento_do_registro is not None
    assert registro.momento_do_registro != registro.momento_do_fato


def test_guerreiro_que_nao_e_o_coletor_e_recusado(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
):
    _, _, serie, _, _ = _preparar_serie(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
    )
    outro_guerreiro = criar_persona(Papel.guerreiro)

    with pytest.raises(PermissaoNegada):
        gravar_registro_de_coleta(
            sessao,
            operador=outro_guerreiro,
            serie=serie,
            momento_do_fato=MOMENTO_DA_MEDICAO,
            origem=OrigemDoRegistro.manual.value,
            valor=25.0,
            unidade="°C",
        )
    assert sessao.query(RegistroDeColeta).count() == 0


def test_medicao_fora_da_vigencia_do_desafio_e_recusada(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
    criar_serie_de_coleta,
):
    """A série é montada direto pelo fixture (`criar_serie_de_coleta`), sem
    passar por `abrir_serie_de_coleta` — abrir uma série sobre um desafio já
    fora da vigência seria recusado ali, e o que este teste isola é só a
    conferência da medição contra `desafio.vigencia_fim` (`RF-08-08`)."""
    comunidade = _criar_comunidade(sessao)
    admin = criar_persona(Papel.admin)
    criar_poder_do_territorio(admin)
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    tipo = _cadastrar_tipo(sessao, admin, FormaDeRegistro.numero, "°C", -10.0, 55.0)
    desafio = criar_desafio_de_coleta(
        missao,
        mestre,
        tipo=tipo,
        granularidade_exigida=NivelDoLocal.rua,
        vigencia_inicio=datetime(2020, 1, 1, tzinfo=UTC),
        vigencia_fim=datetime(2020, 6, 30, tzinfo=UTC),
    )
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    vinculo = sessao.query(VinculoJogador).filter_by(guerreiro_id=guerreiro.id).one()
    vinculo.data_inicio = INICIO_DO_VINCULO
    sessao.commit()
    local = _criar_local_no_nivel(criar_local, comunidade, NivelDoLocal.rua)
    serie = criar_serie_de_coleta(guerreiro, desafio, local)

    with pytest.raises(ErroDeValidacao) as excinfo:
        gravar_registro_de_coleta(
            sessao,
            operador=guerreiro,
            serie=serie,
            momento_do_fato=datetime(2020, 8, 1, tzinfo=UTC),
            origem=OrigemDoRegistro.manual.value,
            valor=25.0,
            unidade="°C",
        )
    assert excinfo.value.campo == "momento_do_fato"
    assert sessao.query(RegistroDeColeta).count() == 0


def test_medicao_com_data_no_futuro_e_recusada(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
):
    _, guerreiro, serie, _, _ = _preparar_serie(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
    )
    no_futuro = datetime.now(UTC) + timedelta(days=1)

    with pytest.raises(ErroDeValidacao) as excinfo:
        gravar_registro_de_coleta(
            sessao,
            operador=guerreiro,
            serie=serie,
            momento_do_fato=no_futuro,
            origem=OrigemDoRegistro.manual.value,
            valor=25.0,
            unidade="°C",
        )
    assert excinfo.value.campo == "momento_do_fato"


def test_periodo_e_apurado_pela_hora_da_medicao_nao_pelo_envio(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
):
    """Medição do último dia de um período, enviada já no período seguinte,
    conta para o período em que a medição aconteceu (`RF-08-15`)."""
    _, guerreiro, serie, _, _ = _preparar_serie(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
    )
    medicao_de_domingo = datetime(2026, 8, 9, 23, 0, tzinfo=UTC)  # domingo, fim da semana civil

    registro = gravar_registro_de_coleta(
        sessao,
        operador=guerreiro,
        serie=serie,
        momento_do_fato=medicao_de_domingo,
        origem=OrigemDoRegistro.manual.value,
        valor=25.0,
        unidade="°C",
    )
    sessao.commit()

    assert registro.momento_do_fato == medicao_de_domingo
    assert registro.pontos_creditados == 5


def test_origem_sensor_e_recusada_na_rota_de_sessao(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
):
    _, guerreiro, serie, _, _ = _preparar_serie(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
    )

    with pytest.raises(ErroDeValidacao) as excinfo:
        gravar_registro_de_coleta(
            sessao,
            operador=guerreiro,
            serie=serie,
            momento_do_fato=MOMENTO_DA_MEDICAO,
            origem=OrigemDoRegistro.sensor.value,
            valor=25.0,
            unidade="°C",
        )
    assert excinfo.value.campo == "origem"
    assert sessao.query(RegistroDeColeta).count() == 0


def test_midia_e_aceita_como_o_proprio_registro(
    sessao,
    tmp_path,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
):
    _, guerreiro, serie, _, _ = _preparar_serie(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
        forma_de_registro=FormaDeRegistro.foto,
    )
    armazenamento = ArmazenamentoEmDisco(str(tmp_path))

    registro = gravar_registro_de_coleta(
        sessao,
        operador=guerreiro,
        serie=serie,
        momento_do_fato=MOMENTO_DA_MEDICAO,
        origem=OrigemDoRegistro.manual.value,
        midia_conteudo=b"conteudo-da-foto",
        armazenamento=armazenamento,
    )
    sessao.commit()

    assert registro.valor is None
    assert registro.midia_referencia is not None
    assert armazenamento.ler(referencia=registro.midia_referencia) == b"conteudo-da-foto"
    assert registro.pontos_creditados == 5
    # Tipo de forma `foto` nunca declara faixa esperada (constraint do
    # catálogo) — é o caso real de "tipo sem faixa declarada" da spec.
    assert registro.a_conferir is False


def test_forma_foto_sem_midia_e_recusado(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
):
    _, guerreiro, serie, _, _ = _preparar_serie(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
        forma_de_registro=FormaDeRegistro.foto,
    )

    with pytest.raises(ErroDeValidacao) as excinfo:
        gravar_registro_de_coleta(
            sessao,
            operador=guerreiro,
            serie=serie,
            momento_do_fato=MOMENTO_DA_MEDICAO,
            origem=OrigemDoRegistro.manual.value,
        )
    assert excinfo.value.campo == "midia"
    assert sessao.query(RegistroDeColeta).count() == 0


def test_forma_numero_sem_valor_e_recusado(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
):
    _, guerreiro, serie, _, _ = _preparar_serie(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
    )

    with pytest.raises(ErroDeValidacao) as excinfo:
        gravar_registro_de_coleta(
            sessao,
            operador=guerreiro,
            serie=serie,
            momento_do_fato=MOMENTO_DA_MEDICAO,
            origem=OrigemDoRegistro.manual.value,
            unidade="°C",
        )
    assert excinfo.value.campo == "valor"
    assert sessao.query(RegistroDeColeta).count() == 0


def test_valor_acima_da_faixa_entra_a_conferir_e_credita_zero(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
):
    _, guerreiro, serie, _, _ = _preparar_serie(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
        faixa_minima=-10.0,
        faixa_maxima=55.0,
    )

    registro = gravar_registro_de_coleta(
        sessao,
        operador=guerreiro,
        serie=serie,
        momento_do_fato=MOMENTO_DA_MEDICAO,
        origem=OrigemDoRegistro.manual.value,
        valor=999.0,
        unidade="°C",
    )
    sessao.commit()

    assert registro.a_conferir is True
    assert registro.pontos_creditados == 0


def test_valor_abaixo_da_faixa_entra_a_conferir(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
):
    _, guerreiro, serie, _, _ = _preparar_serie(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
        faixa_minima=-10.0,
        faixa_maxima=55.0,
    )

    registro = gravar_registro_de_coleta(
        sessao,
        operador=guerreiro,
        serie=serie,
        momento_do_fato=MOMENTO_DA_MEDICAO,
        origem=OrigemDoRegistro.manual.value,
        valor=-999.0,
        unidade="°C",
    )
    sessao.commit()

    assert registro.a_conferir is True
    assert registro.pontos_creditados == 0


def test_valor_dentro_da_faixa_nao_recebe_a_marca(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
):
    _, guerreiro, serie, _, _ = _preparar_serie(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
    )

    registro = gravar_registro_de_coleta(
        sessao,
        operador=guerreiro,
        serie=serie,
        momento_do_fato=MOMENTO_DA_MEDICAO,
        origem=OrigemDoRegistro.manual.value,
        valor=25.0,
        unidade="°C",
    )
    sessao.commit()

    assert registro.a_conferir is False


def test_comunidade_gravada_e_a_da_data_da_medicao(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
    criar_vinculo_jogador,
):
    comunidade_a, guerreiro, serie, _, _ = _preparar_serie(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
    )
    comunidade_b = _criar_comunidade(sessao)
    # Encerra o vínculo com A e abre um novo com B — o registro retroativo à
    # data em que o coletor ainda estava em A precisa apontar para A.
    vinculo_a = (
        sessao.query(VinculoJogador)
        .filter_by(guerreiro_id=guerreiro.id, comunidade_virtual_id=comunidade_a.id)
        .one()
    )
    vinculo_a.data_fim = datetime(2026, 8, 13, tzinfo=UTC)
    sessao.commit()
    criar_vinculo_jogador(guerreiro, comunidade_b, data_fim=None)

    registro = gravar_registro_de_coleta(
        sessao,
        operador=guerreiro,
        serie=serie,
        momento_do_fato=MOMENTO_DA_MEDICAO,  # antes do fim do vínculo com A
        origem=OrigemDoRegistro.manual.value,
        valor=25.0,
        unidade="°C",
    )
    sessao.commit()

    assert registro.comunidade_virtual_id == comunidade_a.id


def test_registro_por_midia_credita_como_o_registro_por_numero(
    sessao,
    tmp_path,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
):
    _, guerreiro, serie, _, _ = _preparar_serie(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
        forma_de_registro=FormaDeRegistro.foto,
    )
    armazenamento = ArmazenamentoEmDisco(str(tmp_path))

    registro = gravar_registro_de_coleta(
        sessao,
        operador=guerreiro,
        serie=serie,
        momento_do_fato=MOMENTO_DA_MEDICAO,
        origem=OrigemDoRegistro.manual.value,
        midia_conteudo=b"conteudo",
        armazenamento=armazenamento,
    )
    sessao.commit()

    assert registro.pontos_creditados == 5


def test_alteracao_e_exclusao_de_registro_nao_tem_rota(cliente, criar_chave, criar_sessao_de_teste):
    """Não há rota declarada para alteração nem exclusão — o roteador
    responde 405 sozinho ao método não declarado no caminho existente
    (`RN-08-10`, design — decisões)."""
    chave, _ = criar_chave()

    resposta_put = cliente.put("/v1/registros-de-coleta", headers={"X-Chave-Aplicacao": chave})
    resposta_delete = cliente.delete(
        "/v1/registros-de-coleta", headers={"X-Chave-Aplicacao": chave}
    )

    assert resposta_put.status_code == 405
    assert resposta_delete.status_code == 405


def test_coletor_permanece_no_registro_apos_saida_do_vinculo(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
):
    _, guerreiro, serie, _, _ = _preparar_serie(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
    )
    registro = gravar_registro_de_coleta(
        sessao,
        operador=guerreiro,
        serie=serie,
        momento_do_fato=MOMENTO_DA_MEDICAO,
        origem=OrigemDoRegistro.manual.value,
        valor=25.0,
        unidade="°C",
    )
    sessao.commit()

    vinculo = sessao.query(VinculoJogador).filter_by(guerreiro_id=guerreiro.id).one()
    vinculo.data_fim = datetime.now(UTC)
    sessao.commit()
    sessao.refresh(registro)

    assert registro.autor_id == guerreiro.id


def test_medicao_mais_antiga_enviada_depois_nao_move_o_campo_para_tras(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
):
    """`ultima_medicao_valida_em` é a data da **última** medição válida, não
    da última gravada (PRD-08 §8)."""
    _, guerreiro, serie, _, _ = _preparar_serie(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
    )
    medicao_recente = MOMENTO_DA_MEDICAO
    medicao_antiga = MOMENTO_DA_MEDICAO - timedelta(days=3)

    gravar_registro_de_coleta(
        sessao,
        operador=guerreiro,
        serie=serie,
        momento_do_fato=medicao_recente,
        origem=OrigemDoRegistro.manual.value,
        valor=25.0,
        unidade="°C",
    )
    sessao.commit()
    gravar_registro_de_coleta(
        sessao,
        operador=guerreiro,
        serie=serie,
        momento_do_fato=medicao_antiga,
        origem=OrigemDoRegistro.manual.value,
        valor=20.0,
        unidade="°C",
    )
    sessao.commit()
    sessao.refresh(serie)

    assert sessao.query(RegistroDeColeta).count() == 2
    assert serie.ultima_medicao_valida_em == medicao_recente


def test_medicao_mais_recente_avanca_o_campo(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
):
    _, guerreiro, serie, _, _ = _preparar_serie(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
    )

    gravar_registro_de_coleta(
        sessao,
        operador=guerreiro,
        serie=serie,
        momento_do_fato=MOMENTO_DA_MEDICAO,
        origem=OrigemDoRegistro.manual.value,
        valor=25.0,
        unidade="°C",
    )
    sessao.commit()
    sessao.refresh(serie)

    assert serie.ultima_medicao_valida_em == MOMENTO_DA_MEDICAO


def test_registro_em_serie_interrompida_credita_e_retoma_para_ativa(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
):
    """O crédito não consulta o estado: o registro que retoma credita como
    qualquer outro, e a retomada é consequência de a âncora ter avançado
    (`RF-08-11`, `RN-08-05`)."""
    _, guerreiro, serie, _, _ = _preparar_serie(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
    )
    agora_do_teste = agora()
    serie.aberta_em = _ancora_ha_n_periodos_completos(agora_do_teste, serie.cadencia, 2)
    sessao.commit()
    assert apurar_estado_da_serie(sessao, serie) == EstadoDaSerie.interrompida

    registro = gravar_registro_de_coleta(
        sessao,
        operador=guerreiro,
        serie=serie,
        momento_do_fato=agora_do_teste,
        origem=OrigemDoRegistro.manual.value,
        valor=25.0,
        unidade="°C",
    )
    sessao.commit()

    assert registro.pontos_creditados == 5
    assert serie.estado == EstadoDaSerie.ativa


def test_retomada_nao_recupera_pontos_dos_periodos_parados(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
):
    _, guerreiro, serie, _, _ = _preparar_serie(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
    )
    agora_do_teste = agora()
    serie.aberta_em = _ancora_ha_n_periodos_completos(agora_do_teste, serie.cadencia, 2)
    sessao.commit()

    gravar_registro_de_coleta(
        sessao,
        operador=guerreiro,
        serie=serie,
        momento_do_fato=agora_do_teste,
        origem=OrigemDoRegistro.manual.value,
        valor=25.0,
        unidade="°C",
    )
    sessao.commit()

    total_creditado = (
        sessao.query(func.sum(RegistroDeColeta.pontos_creditados))
        .filter_by(serie_de_coleta_id=serie.id)
        .scalar()
    )
    assert total_creditado == 5


def test_interrupcao_nao_estorna_pontos_ja_creditados(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
):
    _, guerreiro, serie, _, _ = _preparar_serie(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio,
    )
    agora_do_teste = agora()
    registro = gravar_registro_de_coleta(
        sessao,
        operador=guerreiro,
        serie=serie,
        momento_do_fato=agora_do_teste,
        origem=OrigemDoRegistro.manual.value,
        valor=25.0,
        unidade="°C",
    )
    sessao.commit()
    pontos_antes = registro.pontos_creditados
    assert pontos_antes == 5

    # Simula o decurso de dois períodos sem novo registro — a interrupção
    # deriva na leitura seguinte, sem estornar o que já foi creditado.
    serie.ultima_medicao_valida_em = _ancora_ha_n_periodos_completos(
        agora_do_teste, serie.cadencia, 2
    )
    sessao.commit()
    apurar_estado_da_serie(sessao, serie)
    sessao.commit()
    sessao.refresh(registro)

    assert serie.estado == EstadoDaSerie.interrompida
    assert registro.pontos_creditados == pontos_antes
