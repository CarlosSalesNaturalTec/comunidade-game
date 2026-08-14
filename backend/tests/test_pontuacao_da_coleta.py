from datetime import UTC, datetime

import pytest

from nucleo.coletas.modelo import FormaDeRegistro, OrigemDoRegistro, RegistroDeColeta
from nucleo.coletas.regra import (
    abrir_serie_de_coleta,
    cadastrar_tipo_de_coleta,
    gravar_registro_de_coleta,
)
from nucleo.comunidades.modelo import ComunidadeVirtual, VinculoJogador
from nucleo.erros import PoderDoTerritorioNaoDeclarado
from nucleo.locais.modelo import ORDEM_DOS_NIVEIS, NivelDoLocal
from nucleo.personas.modelo import Papel
from nucleo.pontuacao.modelo import PontoRegular

INICIO_DO_VINCULO = datetime(2025, 1, 1, tzinfo=UTC)


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
    *,
    declarar_poder_do_territorio=True,
    criar_poder_do_territorio=None,
    registros_que_pontuam_por_periodo=1,
):
    comunidade = _criar_comunidade(sessao)
    admin = criar_persona(Papel.admin)
    if declarar_poder_do_territorio:
        criar_poder_do_territorio(admin)
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    tipo = cadastrar_tipo_de_coleta(
        sessao,
        operador=admin,
        nome="Temperatura",
        forma_de_registro=FormaDeRegistro.numero.value,
        unidade="°C",
        faixa_minima=-10.0,
        faixa_maxima=55.0,
    )
    sessao.commit()
    desafio = criar_desafio_de_coleta(
        missao,
        mestre,
        tipo=tipo,
        granularidade_exigida=NivelDoLocal.rua,
        registros_que_pontuam_por_periodo=registros_que_pontuam_por_periodo,
        vigencia_inicio=datetime(2026, 1, 1, tzinfo=UTC),
        vigencia_fim=datetime(2026, 12, 31, tzinfo=UTC),
    )
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    vinculo = sessao.query(VinculoJogador).filter_by(guerreiro_id=guerreiro.id).one()
    vinculo.data_inicio = INICIO_DO_VINCULO
    sessao.commit()
    local = _criar_local_no_nivel(criar_local, comunidade, NivelDoLocal.rua)
    serie = abrir_serie_de_coleta(sessao, operador=guerreiro, desafio=desafio, local_id=local.id)
    sessao.commit()
    return guerreiro, serie, desafio, trilha


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


def test_registro_valido_credita_5_ao_poder_do_territorio_e_nada_a_trilha(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
):
    guerreiro, serie, _, trilha = _preparar_serie(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio=criar_poder_do_territorio,
    )

    registro = _gravar(sessao, guerreiro, serie, datetime(2026, 7, 8, 14, 0, tzinfo=UTC))

    assert registro.pontos_creditados == 5
    conta_da_trilha = (
        sessao.query(PontoRegular).filter_by(guerreiro_id=guerreiro.id, trilha_id=trilha.id).first()
    )
    assert conta_da_trilha is None
    conta_do_poder = (
        sessao.query(PontoRegular)
        .filter_by(guerreiro_id=guerreiro.id)
        .filter(PontoRegular.poder_id.isnot(None))
        .one()
    )
    assert conta_do_poder.total == 5


def test_valor_nao_varia_com_o_tipo_de_coleta(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
):
    guerreiro_1, serie_1, _, _ = _preparar_serie(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio=criar_poder_do_territorio,
    )
    registro_1 = _gravar(sessao, guerreiro_1, serie_1, datetime(2026, 7, 8, 14, 0, tzinfo=UTC))

    guerreiro_2, serie_2, _, _ = _preparar_serie(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
        declarar_poder_do_territorio=False,
    )
    registro_2 = _gravar(sessao, guerreiro_2, serie_2, datetime(2026, 7, 8, 14, 0, tzinfo=UTC))

    assert registro_1.pontos_creditados == registro_2.pontos_creditados == 5


def test_quatro_registros_do_periodo_creditam_os_quatro_quando_o_desafio_declara(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
):
    guerreiro, serie, _, _ = _preparar_serie(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio=criar_poder_do_territorio,
        registros_que_pontuam_por_periodo=4,
    )
    # Segunda-feira 2026-07-06 até domingo 2026-07-12, mesma semana civil.
    momentos = [
        datetime(2026, 7, 6, 10, 0, tzinfo=UTC),
        datetime(2026, 7, 7, 10, 0, tzinfo=UTC),
        datetime(2026, 7, 8, 10, 0, tzinfo=UTC),
        datetime(2026, 7, 9, 10, 0, tzinfo=UTC),
    ]

    creditos = [
        _gravar(sessao, guerreiro, serie, momento).pontos_creditados for momento in momentos
    ]

    assert creditos == [5, 5, 5, 5]


def test_segundo_registro_do_periodo_credita_zero_quando_so_um_pontua(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
):
    guerreiro, serie, _, _ = _preparar_serie(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio=criar_poder_do_territorio,
        registros_que_pontuam_por_periodo=1,
    )

    primeiro = _gravar(sessao, guerreiro, serie, datetime(2026, 7, 6, 10, 0, tzinfo=UTC))
    segundo = _gravar(sessao, guerreiro, serie, datetime(2026, 7, 7, 10, 0, tzinfo=UTC))

    assert primeiro.pontos_creditados == 5
    assert segundo.pontos_creditados == 0
    assert segundo.situacao.value == "valida"
    assert sessao.query(RegistroDeColeta).count() == 2


def test_primeiro_registro_do_periodo_seguinte_volta_a_pontuar(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
):
    guerreiro, serie, _, _ = _preparar_serie(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio=criar_poder_do_territorio,
        registros_que_pontuam_por_periodo=1,
    )

    _gravar(sessao, guerreiro, serie, datetime(2026, 7, 6, 10, 0, tzinfo=UTC))  # semana 1
    proximo = _gravar(
        sessao, guerreiro, serie, datetime(2026, 7, 13, 10, 0, tzinfo=UTC)
    )  # semana 2

    assert proximo.pontos_creditados == 5


def test_contagem_do_periodo_segue_a_data_da_medicao_nao_do_envio(
    sessao,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    criar_poder_do_territorio,
):
    """O segundo registro, enviado já na semana seguinte, tem `momento_do_
    fato` ainda na semana anterior — conta para aquele período, que já
    tinha um registro que pontuou."""
    guerreiro, serie, _, _ = _preparar_serie(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
        criar_poder_do_territorio=criar_poder_do_territorio,
        registros_que_pontuam_por_periodo=1,
    )

    _gravar(sessao, guerreiro, serie, datetime(2026, 7, 6, 10, 0, tzinfo=UTC))
    tardio_da_mesma_semana = _gravar(
        sessao, guerreiro, serie, datetime(2026, 7, 12, 23, 0, tzinfo=UTC)
    )

    assert tardio_da_mesma_semana.pontos_creditados == 0


def test_sem_poder_do_territorio_declarado_a_gravacao_e_recusada(
    sessao, criar_persona, criar_trilha, criar_missao, criar_desafio_de_coleta, criar_local
):
    guerreiro, serie, _, _ = _preparar_serie(
        sessao,
        criar_persona,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
        declarar_poder_do_territorio=False,
    )

    with pytest.raises(PoderDoTerritorioNaoDeclarado):
        gravar_registro_de_coleta(
            sessao,
            operador=guerreiro,
            serie=serie,
            momento_do_fato=datetime(2026, 7, 8, 14, 0, tzinfo=UTC),
            origem=OrigemDoRegistro.manual.value,
            valor=25.0,
            unidade="°C",
        )
    # A recusa acontece depois do `flush` do registro, dentro da mesma
    # transação (design — riscos: "o crédito e o registro precisam cair
    # juntos"). Sem o `commit` que a rota só chama ao final, é o `rollback`
    # — que a rota recebe de graça ao fechar a sessão sem commitar — quem
    # garante que nada persiste (`RN-08-10`, spec de `catalogo-de-poderes`).
    sessao.rollback()
    assert sessao.query(RegistroDeColeta).count() == 0


def test_nenhuma_rota_do_contrato_de_leitura_dos_jogos_credita_ponto_de_coleta():
    """`RN-08-17`, invariante 8 do documento 99 §6: o contrato de leitura
    dos jogos (App 04 e terceiros) não expõe nenhuma escrita — só GET."""
    from nucleo.jogos.rotas import roteador

    for rota in roteador.routes:
        assert rota.methods <= {"GET", "HEAD", "OPTIONS"}
