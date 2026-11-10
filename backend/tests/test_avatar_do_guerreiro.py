"""O Guerreiro(a) em sessão troca o próprio avatar por `PATCH /v1/eu/avatar`
(`RF-05-51`, `RN-05-21`, `RF-01-76`, PRD-05 §9)."""

import pytest

from nucleo.personas.modelo import Papel, Persona

ROTA = "/v1/eu/avatar"


def _cabecalhos(chave: str, token: str) -> dict[str, str]:
    return {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}


def test_guerreiro_troca_o_proprio_avatar_e_a_sessao_devolve_o_novo(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    guerreiro = criar_persona(Papel.guerreiro, avatar="avatar-antigo")
    token, _ = criar_sessao_de_teste(guerreiro, origem="app-05-guerreiro")
    cabecalhos = _cabecalhos(chave, token)

    resposta = cliente.patch(ROTA, json={"avatar": "avatar-novo"}, headers=cabecalhos)
    assert resposta.status_code == 200
    assert resposta.json() == {"avatar": "avatar-novo"}

    assert cliente.get("/v1/eu", headers=cabecalhos).json()["avatar"] == "avatar-novo"


def test_segunda_troca_grava_como_a_primeira(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    guerreiro = criar_persona(Papel.guerreiro, avatar="avatar-antigo")
    token, _ = criar_sessao_de_teste(guerreiro, origem="app-05-guerreiro")
    cabecalhos = _cabecalhos(chave, token)

    cliente.patch(ROTA, json={"avatar": "primeira-troca"}, headers=cabecalhos)
    resposta = cliente.patch(ROTA, json={"avatar": "segunda-troca"}, headers=cabecalhos)

    assert resposta.status_code == 200
    assert resposta.json()["avatar"] == "segunda-troca"


@pytest.mark.parametrize("papel", [Papel.mestre, Papel.apoiador, Papel.admin, Papel.responsavel])
def test_outro_papel_recebe_403_e_nada_muda(
    cliente, sessao, criar_chave, criar_persona, criar_sessao_de_teste, papel
):
    chave, _ = criar_chave()
    persona = criar_persona(papel, avatar="avatar-do-adulto")
    token, _ = criar_sessao_de_teste(persona)

    resposta = cliente.patch(
        ROTA, json={"avatar": "avatar-invasor"}, headers=_cabecalhos(chave, token)
    )

    assert resposta.status_code == 403
    sessao.expire_all()
    assert sessao.get(Persona, persona.id).avatar == "avatar-do-adulto"


def test_a_troca_alcanca_so_a_persona_da_sessao(
    cliente, sessao, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    quem_troca = criar_persona(Papel.guerreiro, avatar="avatar-de-quem-troca")
    outro = criar_persona(Papel.guerreiro, avatar="avatar-do-outro")
    token, _ = criar_sessao_de_teste(quem_troca, origem="app-05-guerreiro")

    cliente.patch(ROTA, json={"avatar": "avatar-trocado"}, headers=_cabecalhos(chave, token))

    sessao.expire_all()
    assert sessao.get(Persona, outro.id).avatar == "avatar-do-outro"


def test_avatar_vazio_e_recusado_e_o_vigente_permanece(
    cliente, sessao, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    guerreiro = criar_persona(Papel.guerreiro, avatar="avatar-vigente")
    token, _ = criar_sessao_de_teste(guerreiro, origem="app-05-guerreiro")

    resposta = cliente.patch(ROTA, json={"avatar": ""}, headers=_cabecalhos(chave, token))

    assert resposta.status_code == 422
    sessao.expire_all()
    assert sessao.get(Persona, guerreiro.id).avatar == "avatar-vigente"


def test_sem_sessao_nao_ha_troca(cliente, sessao, criar_chave, criar_persona):
    chave, _ = criar_chave()
    guerreiro = criar_persona(Papel.guerreiro, avatar="avatar-vigente")

    resposta = cliente.patch(
        ROTA, json={"avatar": "avatar-sem-sessao"}, headers={"X-Chave-Aplicacao": chave}
    )

    assert resposta.status_code == 401
    sessao.expire_all()
    assert sessao.get(Persona, guerreiro.id).avatar == "avatar-vigente"
