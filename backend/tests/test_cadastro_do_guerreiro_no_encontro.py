from datetime import date

import pytest

from nucleo.aulas.modelo import ModoDeComprovacao, Presenca
from nucleo.aulas.regra import registrar_presenca
from nucleo.erros import ErroDeValidacao
from nucleo.personas.modelo import Papel, Persona
from nucleo.personas.regra import cadastrar_guerreiro_no_encontro, cadastrar_guerreiro_pela_gestao
from nucleo.tempo import agora

_HOJE = agora().date()


def _nascimento_com_idade(idade: int) -> date:
    return date(_HOJE.year - idade, _HOJE.month, _HOJE.day)


# 4.1 — a faixa de 6 a 16 anos, nos dois caminhos (RN-04-11)


def test_idade_abaixo_da_faixa_e_recusada_no_encontro(sessao, criar_comunidade, criar_aula):
    admin = Persona(papel=Papel.admin)
    sessao.add(admin)
    sessao.flush()
    aula = criar_aula(admin, criar_comunidade())

    with pytest.raises(ErroDeValidacao) as excinfo:
        cadastrar_guerreiro_no_encontro(
            sessao,
            nome="Muito Nova",
            nascimento=_nascimento_com_idade(5),
            nick="MuitoNova",
            avatar="avatar",
            aula=aula,
        )
    assert excinfo.value.campo == "nascimento"
    assert sessao.query(Persona).filter_by(papel=Papel.guerreiro).count() == 0


def test_idade_acima_da_faixa_e_recusada_no_encontro(sessao, criar_comunidade, criar_aula):
    admin = Persona(papel=Papel.admin)
    sessao.add(admin)
    sessao.flush()
    aula = criar_aula(admin, criar_comunidade())

    with pytest.raises(ErroDeValidacao) as excinfo:
        cadastrar_guerreiro_no_encontro(
            sessao,
            nome="Muito Velha",
            nascimento=_nascimento_com_idade(17),
            nick="MuitoVelha",
            avatar="avatar",
            aula=aula,
        )
    assert excinfo.value.campo == "nascimento"
    assert sessao.query(Persona).filter_by(papel=Papel.guerreiro).count() == 0


@pytest.mark.parametrize("idade", [6, 16])
def test_extremos_da_faixa_sao_aceitos_no_encontro(idade, sessao, criar_comunidade, criar_aula):
    admin = Persona(papel=Papel.admin)
    sessao.add(admin)
    sessao.flush()
    aula = criar_aula(admin, criar_comunidade())

    guerreiro = cadastrar_guerreiro_no_encontro(
        sessao,
        nome="No Extremo",
        nascimento=_nascimento_com_idade(idade),
        nick=f"NoExtremo{idade}",
        avatar="avatar",
        aula=aula,
    )
    sessao.commit()
    assert guerreiro.papel == Papel.guerreiro


def test_idade_fora_da_faixa_e_recusada_tambem_pela_gestao(sessao, criar_comunidade, criar_aula):
    admin = Persona(papel=Papel.admin)
    sessao.add(admin)
    sessao.flush()
    aula = criar_aula(admin, criar_comunidade())

    with pytest.raises(ErroDeValidacao) as excinfo:
        cadastrar_guerreiro_pela_gestao(
            sessao,
            operador=admin,
            nome="Fora da Faixa",
            nascimento=_nascimento_com_idade(17),
            nick="ForaDaFaixa",
            avatar="avatar",
            aula=aula,
        )
    assert excinfo.value.campo == "nascimento"
    assert sessao.query(Persona).filter_by(papel=Papel.guerreiro).count() == 0


# 4.2 — só o Guerreiro(a) tem autocadastro: o caminho do encontro não tem autor


def test_guerreiro_do_encontro_nasce_sem_criador(sessao, criar_comunidade, criar_aula):
    admin = Persona(papel=Papel.admin)
    sessao.add(admin)
    sessao.flush()
    aula = criar_aula(admin, criar_comunidade())

    guerreiro = cadastrar_guerreiro_no_encontro(
        sessao,
        nome="Zeferina",
        nascimento=_nascimento_com_idade(10),
        nick="ZeferinaDoEncontro",
        avatar="avatar",
        aula=aula,
    )
    sessao.commit()
    assert guerreiro.criada_por is None


def test_mestre_cadastra_guerreiro_pela_chave_do_encontro(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_comunidade, criar_aula, sessao
):
    chave, _ = criar_chave(aplicacao="app-01-aula-presencial")
    mestre = criar_persona(Papel.mestre)
    token, _ = criar_sessao_de_teste(mestre)
    comunidade = criar_comunidade()
    aula = criar_aula(mestre, comunidade)

    resposta = cliente.post(
        "/v1/guerreiros",
        json={
            "nome": "Zeferina",
            "nascimento": _nascimento_com_idade(10).isoformat(),
            "nick": "ZeferinaPeloEncontro",
            "avatar": "avatar-opaco",
            "aula_id": str(aula.id),
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 201
    corpo = resposta.json()

    guerreiro = sessao.query(Persona).filter_by(id=corpo["id"]).one()
    assert guerreiro.criada_por is None
    assert guerreiro.vinculo_vigente.comunidade_virtual_id == comunidade.id


def test_admin_cadastra_pela_chave_do_encontro_tambem_sem_criador(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_comunidade, criar_aula, sessao
):
    """Design — decisão 1: um Admin operando o aparelho cai no caminho do
    encontro, que é o correto — quem se cadastra ali é a criança."""
    chave, _ = criar_chave(aplicacao="app-01-aula-presencial")
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade)

    resposta = cliente.post(
        "/v1/guerreiros",
        json={
            "nome": "Zeferina",
            "nascimento": _nascimento_com_idade(10).isoformat(),
            "nick": "ZeferinaComAdmin",
            "avatar": "avatar-opaco",
            "aula_id": str(aula.id),
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 201
    guerreiro = sessao.query(Persona).filter_by(id=resposta.json()["id"]).one()
    assert guerreiro.criada_por is None


def test_sem_sessao_nao_ha_autocadastro_no_encontro(
    cliente, criar_chave, criar_comunidade, criar_aula, criar_persona
):
    chave, _ = criar_chave(aplicacao="app-01-aula-presencial")
    admin = criar_persona(Papel.admin)
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade)

    resposta = cliente.post(
        "/v1/guerreiros",
        json={
            "nome": "Zeferina",
            "nascimento": _nascimento_com_idade(10).isoformat(),
            "nick": "SemSessao",
            "avatar": "avatar-opaco",
            "aula_id": str(aula.id),
        },
        headers={"X-Chave-Aplicacao": chave},
    )
    assert resposta.status_code == 401


# 4.3 — a recusa de nick, com as variações de alcance total só no encontro


def test_recusa_de_nick_no_encontro_traz_variacoes_de_alcance_total(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_comunidade, criar_aula
):
    chave, _ = criar_chave(aplicacao="app-01-aula-presencial")
    mestre = criar_persona(Papel.mestre)
    token, _ = criar_sessao_de_teste(mestre)
    comunidade = criar_comunidade()
    aula = criar_aula(mestre, comunidade)

    # Ocupa o nick primeiro, pelo próprio caminho do encontro.
    cliente.post(
        "/v1/guerreiros",
        json={
            "nome": "Primeira",
            "nascimento": _nascimento_com_idade(10).isoformat(),
            "nick": "NickDisputado",
            "avatar": "avatar",
            "aula_id": str(aula.id),
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    resposta = cliente.post(
        "/v1/guerreiros",
        json={
            "nome": "Segunda",
            "nascimento": _nascimento_com_idade(9).isoformat(),
            "nick": "NickDisputado",
            "avatar": "avatar",
            "aula_id": str(aula.id),
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 422
    corpo = resposta.json()
    assert corpo["campo"] == "nick"
    assert 1 <= len(corpo["sugestoes"]) <= 3
    assert "NickDisputado" not in corpo["sugestoes"]
    assert "primeira" not in corpo["mensagem"].lower()
    assert "guerreiro" not in corpo["mensagem"].lower()


def test_recusa_de_nick_na_gestao_nao_traz_variacoes(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_comunidade, criar_aula
):
    chave, _ = criar_chave()  # aplicação padrão, fora da App 01 — caminho da gestão
    admin = criar_persona(Papel.admin)
    token, _ = criar_sessao_de_teste(admin)
    comunidade = criar_comunidade()
    aula = criar_aula(admin, comunidade)

    cliente.post(
        "/v1/guerreiros",
        json={
            "nome": "Primeira",
            "nascimento": "2015-01-01",
            "nick": "NickDaGestao",
            "avatar": "avatar",
            "aula_id": str(aula.id),
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )

    resposta = cliente.post(
        "/v1/guerreiros",
        json={
            "nome": "Segunda",
            "nascimento": "2015-01-01",
            "nick": "NickDaGestao",
            "avatar": "avatar",
            "aula_id": str(aula.id),
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 422
    assert "sugestoes" not in resposta.json()


# 4.4 — cadastro e presença no mesmo ato (RF-04-15, RF-04-17)


def test_cadastro_no_encontro_registra_presenca_no_mesmo_ato(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_comunidade, criar_aula, sessao
):
    chave, _ = criar_chave(aplicacao="app-01-aula-presencial")
    mestre = criar_persona(Papel.mestre)
    token, _ = criar_sessao_de_teste(mestre)
    comunidade = criar_comunidade()
    aula = criar_aula(mestre, comunidade)

    resposta = cliente.post(
        "/v1/guerreiros",
        json={
            "nome": "Zeferina",
            "nascimento": _nascimento_com_idade(10).isoformat(),
            "nick": "ZeferinaComPresenca",
            "avatar": "avatar",
            "aula_id": str(aula.id),
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 201
    guerreiro_id = resposta.json()["id"]

    presenca = sessao.query(Presenca).filter_by(aula_id=aula.id, guerreiro_id=guerreiro_id).one()
    assert presenca.modo == ModoDeComprovacao.confirmacao
    assert presenca.confirmador_id == mestre.id


def test_cadastro_recusado_no_encontro_nao_deixa_presenca_orfa(
    cliente, criar_chave, criar_persona, criar_sessao_de_teste, criar_comunidade, criar_aula, sessao
):
    chave, _ = criar_chave(aplicacao="app-01-aula-presencial")
    mestre = criar_persona(Papel.mestre)
    token, _ = criar_sessao_de_teste(mestre)
    comunidade = criar_comunidade()
    aula = criar_aula(mestre, comunidade)

    # Idade fora da faixa: recusado antes de qualquer gravação.
    resposta = cliente.post(
        "/v1/guerreiros",
        json={
            "nome": "Fora da Faixa",
            "nascimento": _nascimento_com_idade(17).isoformat(),
            "nick": "ForaDaFaixaNoEncontro",
            "avatar": "avatar",
            "aula_id": str(aula.id),
        },
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 422
    assert sessao.query(Persona).filter_by(papel=Papel.guerreiro).count() == 0
    assert sessao.query(Presenca).count() == 0


def test_segunda_confirmacao_do_mesmo_guerreiro_na_aula_nao_duplica_presenca(
    sessao, criar_comunidade, criar_aula
):
    admin = Persona(papel=Papel.admin)
    sessao.add(admin)
    sessao.flush()
    aula = criar_aula(admin, criar_comunidade())
    guerreiro = cadastrar_guerreiro_no_encontro(
        sessao,
        nome="Zeferina",
        nascimento=_nascimento_com_idade(10),
        nick="ZeferinaReenviada",
        avatar="avatar",
        aula=aula,
    )
    sessao.commit()

    primeira = registrar_presenca(
        sessao,
        operador=admin,
        aula=aula,
        guerreiro=guerreiro,
        modo=ModoDeComprovacao.confirmacao.value,
        confirmador=admin,
        momento_do_fato=agora(),
    )
    sessao.commit()
    segunda = registrar_presenca(
        sessao,
        operador=admin,
        aula=aula,
        guerreiro=guerreiro,
        modo=ModoDeComprovacao.confirmacao.value,
        confirmador=admin,
        momento_do_fato=agora(),
    )
    sessao.commit()

    assert primeira.id == segunda.id
    assert sessao.query(Presenca).filter_by(aula_id=aula.id, guerreiro_id=guerreiro.id).count() == 1
