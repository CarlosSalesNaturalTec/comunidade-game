"""A escolha da equipe sobre a atividade da programação do encontro —
`RF-02-42`, `RF-04-35`, decisão do fundador de 2026-08-25."""

import pytest

from nucleo.equipes.regra import declarar_escolha_da_equipe
from nucleo.erros import ErroDeValidacao, PermissaoNegada
from nucleo.personas.modelo import Papel
from nucleo.trilhas.modelo import SituacaoDaTrilha


def _cabecalhos(chave, token):
    return {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}


def _montar_atividade(criar_trilha, criar_missao, criar_atividade, mestre, aula):
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    missao = criar_missao(trilha, mestre)
    return criar_atividade(missao, mestre, aula=aula)


def test_integrante_declara_a_escolha(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_equipe,
    criar_trilha,
    criar_missao,
    criar_atividade,
):
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(admin, comunidade)
    atividade = _montar_atividade(criar_trilha, criar_missao, criar_atividade, mestre, aula)
    equipe = criar_equipe(guerreiro, aula=aula)

    declarar_escolha_da_equipe(sessao, operador=guerreiro, equipe=equipe, atividade=atividade)
    sessao.commit()

    assert equipe.atividade_corrente_id == atividade.id


def test_trocar_de_atividade_substitui_a_escolha(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_equipe,
    criar_trilha,
    criar_missao,
    criar_atividade,
):
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(admin, comunidade)
    primeira = _montar_atividade(criar_trilha, criar_missao, criar_atividade, mestre, aula)
    segunda = _montar_atividade(criar_trilha, criar_missao, criar_atividade, mestre, aula)
    equipe = criar_equipe(guerreiro, aula=aula)

    declarar_escolha_da_equipe(sessao, operador=guerreiro, equipe=equipe, atividade=primeira)
    sessao.commit()
    declarar_escolha_da_equipe(sessao, operador=guerreiro, equipe=equipe, atividade=segunda)
    sessao.commit()

    assert equipe.atividade_corrente_id == segunda.id


def test_atividade_fora_da_programacao_e_recusada(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_equipe,
    criar_trilha,
    criar_missao,
    criar_atividade,
):
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(admin, comunidade)
    outra_aula = criar_aula(admin, comunidade)
    atividade_de_outra_aula = _montar_atividade(
        criar_trilha, criar_missao, criar_atividade, mestre, outra_aula
    )
    equipe = criar_equipe(guerreiro, aula=aula)

    with pytest.raises(ErroDeValidacao) as excinfo:
        declarar_escolha_da_equipe(
            sessao, operador=guerreiro, equipe=equipe, atividade=atividade_de_outra_aula
        )
    assert excinfo.value.campo == "atividade_id"
    assert equipe.atividade_corrente_id is None


def test_nao_integrante_nao_declara(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_equipe,
    criar_trilha,
    criar_missao,
    criar_atividade,
):
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    outro_guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(admin, comunidade)
    atividade = _montar_atividade(criar_trilha, criar_missao, criar_atividade, mestre, aula)
    equipe = criar_equipe(guerreiro, aula=aula)

    with pytest.raises(PermissaoNegada):
        declarar_escolha_da_equipe(
            sessao, operador=outro_guerreiro, equipe=equipe, atividade=atividade
        )
    assert equipe.atividade_corrente_id is None


def test_leitura_da_programacao_nao_grava_escolha(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_equipe,
    criar_trilha,
    criar_missao,
    criar_atividade,
):
    from nucleo.equipes.regra import programacao_do_encontro

    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(admin, comunidade)
    _montar_atividade(criar_trilha, criar_missao, criar_atividade, mestre, aula)
    equipe = criar_equipe(guerreiro, aula=aula)

    programacao_do_encontro(sessao, operador=guerreiro, equipe=equipe)

    assert equipe.atividade_corrente_id is None


def test_escolha_nao_sobrevive_a_aula(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_equipe,
    criar_trilha,
    criar_missao,
    criar_atividade,
):
    """A escolha é coluna da equipe da aula, que nasce sem escolha alguma —
    equipe nova, de outra aula, nunca herda a declaração de outra."""
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(admin, comunidade)
    atividade = _montar_atividade(criar_trilha, criar_missao, criar_atividade, mestre, aula)
    equipe = criar_equipe(guerreiro, aula=aula)
    declarar_escolha_da_equipe(sessao, operador=guerreiro, equipe=equipe, atividade=atividade)
    sessao.commit()

    outra_aula = criar_aula(admin, comunidade)
    outra_equipe = criar_equipe(guerreiro, aula=outra_aula)

    assert outra_equipe.atividade_corrente_id is None


def test_declarar_e_ler_pela_rota(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_equipe,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
    criar_atividade,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(admin, comunidade)
    atividade = _montar_atividade(criar_trilha, criar_missao, criar_atividade, mestre, aula)
    equipe = criar_equipe(guerreiro, aula=aula)
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.post(
        f"/v1/equipes/{equipe.id}/atividade-corrente",
        json={"atividade_id": str(atividade.id)},
        headers=_cabecalhos(chave, token),
    )
    assert resposta.status_code == 200
    assert resposta.json()["atividade_corrente_id"] == str(atividade.id)

    leitura = cliente.get(f"/v1/equipes/{equipe.id}/missao", headers=_cabecalhos(chave, token))
    corpo = leitura.json()
    assert len(corpo) == 1
    assert corpo[0]["corrente"] is True


def test_mestre_recebe_403_ao_declarar_pela_rota(
    cliente,
    criar_chave,
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_equipe,
    criar_sessao_de_teste,
    criar_trilha,
    criar_missao,
    criar_atividade,
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre)
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    aula = criar_aula(admin, comunidade)
    atividade = _montar_atividade(criar_trilha, criar_missao, criar_atividade, mestre, aula)
    equipe = criar_equipe(guerreiro, aula=aula)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.post(
        f"/v1/equipes/{equipe.id}/atividade-corrente",
        json={"atividade_id": str(atividade.id)},
        headers=_cabecalhos(chave, token),
    )
    assert resposta.status_code == 403


def test_rota_de_declaracao_esta_no_openapi_sob_v1(cliente):
    schema = cliente.get("/openapi.json").json()

    assert "/v1/equipes/{id_da_equipe}/atividade-corrente" in schema["paths"]
    assert "post" in schema["paths"]["/v1/equipes/{id_da_equipe}/atividade-corrente"]
