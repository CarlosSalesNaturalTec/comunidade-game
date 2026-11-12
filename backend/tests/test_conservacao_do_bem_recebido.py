"""Conservação do bem recebido, a regra de uma pontuação por bem e por
encontro e a fila do cuidado (`RF-01-87`, `RF-09-113`, `RF-04-81`,
`RF-04-84`, `RN-01-66`, `RN-09-62`)."""

import pytest
from sqlalchemy.exc import IntegrityError

from nucleo.cuidado_do_bem.modelo import FonteDaPontuacaoDoBem, PontuacaoDoBem
from nucleo.personas.modelo import Papel
from tests.test_customizacao_do_kit import _extras, _julgar, _registrar_com_midia


def _validar(cliente, cenario, entrega=None, aula=None, cabecalhos=None, guerreiro=None):
    return cliente.post(
        f"/v1/aulas/{(aula or cenario.aula).id}/conservacoes",
        json={
            "guerreiro_id": str((guerreiro or cenario.guerreiro).id),
            "entrega_de_recompensa_id": str((entrega or cenario.entrega_do_livro).id),
        },
        headers=cabecalhos or cenario.do_mestre,
    )


# ---------------------------------------------------------------------------
# Validação da conservação
# ---------------------------------------------------------------------------


def test_a_conservacao_validada_credita_1_extra(cliente, sessao, cenario):
    resposta = _validar(cliente, cenario)

    assert resposta.status_code == 201, resposta.text
    assert resposta.json()["fonte"] == "conservacao"
    assert _extras(sessao, cenario.guerreiro) == (1, 1)


def test_entrega_de_outro_guerreiro_e_recusada(cliente, sessao, cenario, criar_persona):
    outro = criar_persona(Papel.guerreiro, comunidade=cenario.comunidade)

    resposta = _validar(cliente, cenario, guerreiro=outro)

    assert resposta.status_code == 422
    assert sessao.query(PontuacaoDoBem).count() == 0


def test_sem_presenca_na_aula_sem_validacao(cliente, sessao, cenario, criar_aula):
    outra_aula = criar_aula(cenario.mestre, cenario.comunidade, ponto_de_apoio=cenario.ponto)

    resposta = _validar(cliente, cenario, aula=outra_aula)

    assert resposta.status_code == 422
    assert _extras(sessao, cenario.guerreiro) == (0, 0)


@pytest.mark.parametrize("papel", [Papel.admin, Papel.guerreiro])
def test_quem_nao_e_mestre_nao_valida(cliente, sessao, cenario, criar_persona, papel):
    persona = criar_persona(papel, comunidade=cenario.comunidade)

    resposta = _validar(cliente, cenario, cabecalhos=cenario.cabecalhos(persona))

    assert resposta.status_code == 403
    assert sessao.query(PontuacaoDoBem).count() == 0


def test_mestre_de_outra_comunidade_nao_valida(
    cliente, cenario, criar_persona, criar_comunidade, criar_vinculo_do_mestre
):
    alheio = criar_persona(Papel.mestre)
    criar_vinculo_do_mestre(alheio, criar_comunidade("Outra"))

    resposta = _validar(cliente, cenario, cabecalhos=cenario.cabecalhos(alheio))

    assert resposta.status_code == 403


# ---------------------------------------------------------------------------
# Uma pontuação por bem e por encontro
# ---------------------------------------------------------------------------


def test_conservacao_depois_da_customizacao_e_recusada(cliente, sessao, cenario):
    registro = _registrar_com_midia(cliente, cenario)
    _julgar(cliente, cenario, registro["id"])

    resposta = _validar(cliente, cenario, entrega=cenario.entrega_do_kit)

    assert resposta.status_code == 422
    assert "customização" in resposta.json()["mensagem"]
    assert _extras(sessao, cenario.guerreiro) == (1, 1)


def test_customizacao_depois_da_conservacao_e_recusada(cliente, sessao, cenario):
    _validar(cliente, cenario, entrega=cenario.entrega_do_kit)
    registro = _registrar_com_midia(cliente, cenario)

    resposta = _julgar(cliente, cenario, registro["id"])

    assert resposta.status_code == 422
    assert "conservação" in resposta.json()["mensagem"]
    assert _extras(sessao, cenario.guerreiro) == (1, 1)
    corpo = cliente.get("/v1/eu/customizacoes", headers=cenario.do_guerreiro).json()
    assert corpo["registros"][0]["situacao"] == "pendente"


def test_a_mesma_conservacao_nao_pontua_duas_vezes(cliente, sessao, cenario):
    assert _validar(cliente, cenario).status_code == 201

    segunda = _validar(cliente, cenario)

    assert segunda.status_code == 422
    assert _extras(sessao, cenario.guerreiro) == (1, 1)


def test_outro_encontro_pontua_de_novo(cliente, sessao, cenario, criar_aula, criar_presenca):
    _validar(cliente, cenario)
    seguinte = criar_aula(cenario.mestre, cenario.comunidade, ponto_de_apoio=cenario.ponto)
    criar_presenca(seguinte, cenario.guerreiro)

    resposta = _validar(cliente, cenario, aula=seguinte)

    assert resposta.status_code == 201
    assert _extras(sessao, cenario.guerreiro) == (2, 2)


def test_bens_diferentes_no_mesmo_encontro_somam(cliente, sessao, cenario):
    assert _validar(cliente, cenario, entrega=cenario.entrega_do_livro).status_code == 201
    assert _validar(cliente, cenario, entrega=cenario.entrega_do_kit).status_code == 201

    assert _extras(sessao, cenario.guerreiro) == (2, 2)


def test_o_banco_recusa_o_mesmo_bem_duas_vezes_no_encontro(sessao, cenario):
    for fonte in (FonteDaPontuacaoDoBem.conservacao, FonteDaPontuacaoDoBem.customizacao):
        sessao.add(
            PontuacaoDoBem(
                aula_id=cenario.aula.id,
                entrega_de_recompensa_id=cenario.entrega_do_kit.id,
                guerreiro_id=cenario.guerreiro.id,
                fonte=fonte,
                autor_id=cenario.mestre.id,
                papel_do_autor="mestre",
            )
        )
    with pytest.raises(IntegrityError):
        sessao.commit()
    sessao.rollback()


# ---------------------------------------------------------------------------
# Fila do cuidado no encontro
# ---------------------------------------------------------------------------


def test_a_fila_traz_os_presentes_e_os_bens(cliente, cenario):
    registro = _registrar_com_midia(cliente, cenario)
    _validar(cliente, cenario, entrega=cenario.entrega_do_livro)

    fila = cliente.get(f"/v1/aulas/{cenario.aula.id}/fila-do-cuidado", headers=cenario.do_mestre)

    assert fila.status_code == 200, fila.text
    corpo = fila.json()
    assert [item["guerreiro_id"] for item in corpo] == [str(cenario.guerreiro.id)]
    bens = {bem["entrega_de_recompensa_id"]: bem for bem in corpo[0]["bens"]}
    kit = bens[str(cenario.entrega_do_kit.id)]
    livro = bens[str(cenario.entrega_do_livro.id)]
    assert kit["customizacao_aberta"] is True
    assert kit["pendente"]["id"] == registro["id"]
    assert kit["ultimo_aprovado"]["fonte"] == "comprovacao_do_pratico"
    assert kit["pontuado_na_aula"] is None
    assert livro["customizacao_aberta"] is False
    assert livro["pontuado_na_aula"] == "conservacao"


def test_quem_nao_registrou_presenca_fica_fora_da_fila(cliente, cenario, criar_aula):
    _registrar_com_midia(cliente, cenario)
    outra_aula = criar_aula(cenario.mestre, cenario.comunidade, ponto_de_apoio=cenario.ponto)

    fila = cliente.get(f"/v1/aulas/{outra_aula.id}/fila-do-cuidado", headers=cenario.do_mestre)

    assert fila.status_code == 200
    assert fila.json() == []


def test_mestre_de_outra_comunidade_nao_le_a_fila(
    cliente, cenario, criar_persona, criar_comunidade, criar_vinculo_do_mestre
):
    alheio = criar_persona(Papel.mestre)
    criar_vinculo_do_mestre(alheio, criar_comunidade("Outra"))

    fila = cliente.get(
        f"/v1/aulas/{cenario.aula.id}/fila-do-cuidado", headers=cenario.cabecalhos(alheio)
    )

    assert fila.status_code == 403
