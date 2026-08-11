import pytest

from nucleo.chaves.segredo import (
    ChaveMalFormada,
    calcular_resumo,
    decompor_chave,
    gerar_segredo,
    montar_chave_completa,
)


def test_dois_segredos_gerados_nunca_coincidem():
    gerados = {gerar_segredo() for _ in range(1000)}
    assert len(gerados) == 1000


def test_resumo_nao_e_reversivel():
    segredo = gerar_segredo()
    resumo = calcular_resumo(segredo)
    assert segredo not in resumo
    assert resumo != segredo
    # SHA-256 em hexadecimal tem sempre 64 caracteres, qualquer que seja a entrada.
    assert len(resumo) == 64


def test_resumo_e_deterministico_para_o_mesmo_segredo():
    segredo = gerar_segredo()
    assert calcular_resumo(segredo) == calcular_resumo(segredo)


def test_decompor_chave_extrai_ambiente_id_e_segredo():
    segredo = gerar_segredo()
    chave_completa = montar_chave_completa("producao", "algum-id", segredo)
    ambiente, id_da_chave, segredo_extraido = decompor_chave(chave_completa)
    assert ambiente == "producao"
    assert id_da_chave == "algum-id"
    assert segredo_extraido == segredo


@pytest.mark.parametrize(
    "malformada",
    ["sem-formato-nenhum", "cg_producao_id-sem-ponto-final", "outro_producao_id.segredo"],
)
def test_decompor_chave_mal_formada_levanta_erro(malformada):
    with pytest.raises(ChaveMalFormada):
        decompor_chave(malformada)
