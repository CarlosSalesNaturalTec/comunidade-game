import pytest

from nucleo.erros import ErroDeValidacao
from nucleo.personas.modelo import Nick, Papel, Persona
from nucleo.personas.regra import (
    conferir_disponibilidade_de_nick,
    criar_persona,
    definir_ou_trocar_nick,
    sugerir_variacoes_de_nick,
)


def _criar_guerreiro_com_nick(sessao, criar_comunidade, criar_aula, nick: str) -> Persona:
    admin = Persona(papel=Papel.admin)
    sessao.add(admin)
    sessao.flush()
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade)
    guerreiro = criar_persona(sessao, papel=Papel.guerreiro, criada_por=None, aula=aula, nick=nick)
    sessao.commit()
    return guerreiro


def test_nick_livre_esta_disponivel(sessao):
    assert conferir_disponibilidade_de_nick(sessao, "NickQueNinguemUsa") is True


def test_nick_de_apoiador_esta_indisponivel(sessao):
    admin = Persona(papel=Papel.admin)
    sessao.add(admin)
    sessao.flush()
    criar_persona(sessao, papel=Papel.apoiador, criada_por=admin, nick="ApoiadoraDeTeste")
    sessao.commit()

    assert conferir_disponibilidade_de_nick(sessao, "ApoiadoraDeTeste") is False


def test_nick_de_mestre_esta_indisponivel(sessao):
    admin = Persona(papel=Papel.admin)
    sessao.add(admin)
    sessao.flush()
    criar_persona(sessao, papel=Papel.mestre, criada_por=admin, nick="MestreDeTeste")
    sessao.commit()

    assert conferir_disponibilidade_de_nick(sessao, "MestreDeTeste") is False


def test_nick_de_guerreiro_esta_disponivel_na_conferencia_de_adulto(
    sessao, criar_comunidade, criar_aula
):
    _criar_guerreiro_com_nick(sessao, criar_comunidade, criar_aula, "GuerreiraDeTeste")

    assert conferir_disponibilidade_de_nick(sessao, "GuerreiraDeTeste") is True


def test_variacoes_sugeridas_nao_colidem_com_adulto(sessao):
    admin = Persona(papel=Papel.admin)
    sessao.add(admin)
    sessao.flush()
    criar_persona(sessao, papel=Papel.apoiador, criada_por=admin, nick="Fulana2")
    sessao.commit()

    sugestoes = sugerir_variacoes_de_nick(sessao, "Fulana")
    assert "Fulana2" not in sugestoes
    for sugestao in sugestoes:
        assert conferir_disponibilidade_de_nick(sessao, sugestao) is True


def test_variacao_pode_coincidir_com_nick_de_guerreiro(sessao, criar_comunidade, criar_aula):
    """A conferência não enxerga nick de Guerreiro(a), então a sugestão pode
    devolver uma variação que colide com ele — a colisão é resolvida na
    gravação, não na sugestão (`RN-01-22`)."""
    _criar_guerreiro_com_nick(sessao, criar_comunidade, criar_aula, "Fulana2")

    sugestoes = sugerir_variacoes_de_nick(sessao, "Fulana")
    assert "Fulana2" in sugestoes


def test_conferencia_disponivel_nao_garante_a_gravacao(sessao, criar_comunidade, criar_aula):
    _criar_guerreiro_com_nick(sessao, criar_comunidade, criar_aula, "NickEmprestado")
    admin = Persona(papel=Papel.admin)
    sessao.add(admin)
    sessao.flush()

    assert conferir_disponibilidade_de_nick(sessao, "NickEmprestado") is True

    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_persona(sessao, papel=Papel.apoiador, criada_por=admin, nick="NickEmprestado")
    assert excinfo.value.campo == "nick"


def test_mestre_define_o_proprio_nick_no_primeiro_acesso(sessao):
    admin = Persona(papel=Papel.admin)
    sessao.add(admin)
    sessao.flush()
    mestre = criar_persona(sessao, papel=Papel.mestre, criada_por=admin)
    sessao.commit()

    definir_ou_trocar_nick(sessao, mestre, "MestreNovo")
    sessao.commit()

    nick = sessao.query(Nick).filter_by(persona_id=mestre.id).one()
    assert nick.valor == "MestreNovo"


def test_apoiador_troca_o_proprio_nick(sessao):
    admin = Persona(papel=Papel.admin)
    sessao.add(admin)
    sessao.flush()
    apoiador = criar_persona(sessao, papel=Papel.apoiador, criada_por=admin, nick="NickAntigo")
    sessao.commit()

    definir_ou_trocar_nick(sessao, apoiador, "NickNovo")
    sessao.commit()

    assert sessao.query(Nick).filter_by(valor="NickAntigo").first() is None
    nick = sessao.query(Nick).filter_by(persona_id=apoiador.id).one()
    assert nick.valor == "NickNovo"


def test_definir_nick_ja_usado_e_recusado(sessao):
    admin = Persona(papel=Papel.admin)
    sessao.add(admin)
    sessao.flush()
    criar_persona(sessao, papel=Papel.apoiador, criada_por=admin, nick="NickOcupado")
    mestre = criar_persona(sessao, papel=Papel.mestre, criada_por=admin)
    sessao.commit()

    with pytest.raises(ErroDeValidacao) as excinfo:
        definir_ou_trocar_nick(sessao, mestre, "NickOcupado")
    assert excinfo.value.campo == "nick"


def test_definir_nick_em_branco_e_recusado(sessao):
    admin = Persona(papel=Papel.admin)
    sessao.add(admin)
    sessao.flush()
    mestre = criar_persona(sessao, papel=Papel.mestre, criada_por=admin)
    sessao.commit()

    with pytest.raises(ErroDeValidacao) as excinfo:
        definir_ou_trocar_nick(sessao, mestre, "   ")
    assert excinfo.value.campo == "nick"


# --- Rotas ---


def test_rota_de_disponibilidade_devolve_disponivel_para_nick_de_guerreiro(
    cliente, criar_chave, criar_comunidade, criar_aula, sessao
):
    _criar_guerreiro_com_nick(sessao, criar_comunidade, criar_aula, "GuerreiraPublica")
    chave, _ = criar_chave()

    resposta = cliente.get(
        "/v1/nicks/disponibilidade",
        params={"nick": "GuerreiraPublica"},
        headers={"X-Chave-Aplicacao": chave},
    )
    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["disponivel"] is True
    assert corpo["sugestoes"] == []


def test_rota_de_disponibilidade_devolve_indisponivel_com_sugestoes(
    cliente, criar_chave, criar_persona, sessao
):
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador, criada_por=admin)
    definir_ou_trocar_nick(sessao, apoiador, "NickJaUsadoPelaRota")
    sessao.commit()
    chave, _ = criar_chave()

    resposta = cliente.get(
        "/v1/nicks/disponibilidade",
        params={"nick": "NickJaUsadoPelaRota"},
        headers={"X-Chave-Aplicacao": chave},
    )
    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["disponivel"] is False
    assert len(corpo["sugestoes"]) > 0
    assert "NickJaUsadoPelaRota" not in corpo["sugestoes"]


def test_mestre_define_o_proprio_nick_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.put(
        "/v1/eu/mestre/identidade",
        json={"nick": "MestreNovoPelaRota"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 200
    assert resposta.json()["nick"] == "MestreNovoPelaRota"


def test_apoiador_troca_o_proprio_nick_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, sessao
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador, criada_por=admin)
    definir_ou_trocar_nick(sessao, apoiador, "NickAntigoDaRota")
    sessao.commit()
    token, _ = criar_sessao_de_teste(apoiador)

    resposta = cliente.put(
        "/v1/eu/apoiador/identidade",
        json={"nick": "NickNovoDaRota"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 200
    assert resposta.json()["nick"] == "NickNovoDaRota"


def test_guerreiro_recebe_403_na_rota_de_identidade_do_adulto(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    guerreiro = criar_persona(Papel.guerreiro)
    token, _ = criar_sessao_de_teste(guerreiro)

    resposta = cliente.put(
        "/v1/eu/apoiador/identidade",
        json={"nick": "NickQualquer"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 403


def test_apoiador_recebe_403_na_rota_do_mestre(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador, criada_por=admin)
    token, _ = criar_sessao_de_teste(apoiador)

    resposta = cliente.put(
        "/v1/eu/mestre/identidade",
        json={"nick": "NickQualquer"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 403


def test_mestre_recebe_403_na_rota_do_apoiador(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    mestre = criar_persona(Papel.mestre, criada_por=admin)
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.put(
        "/v1/eu/apoiador/identidade",
        json={"nick": "NickQualquer"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 403


def test_nick_ja_usado_e_recusado_na_troca_pela_rota(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste
):
    chave, _ = criar_chave()
    admin = criar_persona(Papel.admin)
    primeiro_mestre = criar_persona(Papel.mestre, criada_por=admin)
    segundo_mestre = criar_persona(Papel.mestre, criada_por=admin)
    token_do_primeiro, _ = criar_sessao_de_teste(primeiro_mestre)
    token_do_segundo, _ = criar_sessao_de_teste(segundo_mestre)

    resposta = cliente.put(
        "/v1/eu/mestre/identidade",
        json={"nick": "NickQualquerDaRota"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token_do_primeiro}"},
    )
    assert resposta.status_code == 200

    resposta_repetida = cliente.put(
        "/v1/eu/mestre/identidade",
        json={"nick": "NickQualquerDaRota"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token_do_segundo}"},
    )
    assert resposta_repetida.status_code == 422
    assert resposta_repetida.json()["campo"] == "nick"
