"""Fatia 28 do PRD-09: a missão troca a posição com a vizinha, em qualquer
situação da trilha e só pelo Mestre autor; a sondagem fica na primeira
posição (`RF-09-137`, `RN-09-56`, `RN-09-57`)."""

import pytest

from nucleo.erros import ErroDeValidacao, PermissaoNegada
from nucleo.personas.modelo import Papel
from nucleo.trilhas.modelo import DesbloqueioDaMissao, SituacaoDaTrilha
from nucleo.trilhas.regra import derivar_percurso, inscrever_na_trilha, mover_missao


def _cabecalhos(criar_chave, criar_sessao_de_teste, persona):
    chave, _ = criar_chave()
    token, _ = criar_sessao_de_teste(persona)
    return {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}


def _tres_missoes(
    criar_trilha,
    criar_missao,
    mestre,
    situacao=SituacaoDaTrilha.rascunho,
    posicoes=(1, 2, 3),
    sondagem=False,
):
    trilha = criar_trilha(mestre, situacao=situacao)
    missoes = [
        criar_missao(trilha, mestre, titulo=f"M{p}", posicao=p, e_sondagem=sondagem and indice == 0)
        for indice, p in enumerate(posicoes)
    ]
    return trilha, missoes


def test_subir_troca_so_com_a_vizinha(sessao, criar_persona, criar_trilha, criar_missao):
    mestre = criar_persona(Papel.mestre)
    _, (m1, m2, m3) = _tres_missoes(criar_trilha, criar_missao, mestre)

    trocadas = mover_missao(sessao, operador=mestre, missao=m3, direcao="cima")
    sessao.commit()

    assert (m1.posicao, m2.posicao, m3.posicao) == (1, 3, 2)
    assert {missao.id for missao in trocadas} == {m2.id, m3.id}


def test_descer_com_lacuna_troca_os_valores(sessao, criar_persona, criar_trilha, criar_missao):
    mestre = criar_persona(Papel.mestre)
    _, (m1, m2, m3) = _tres_missoes(criar_trilha, criar_missao, mestre, posicoes=(1, 4, 9))

    mover_missao(sessao, operador=mestre, missao=m2, direcao="baixo")
    sessao.commit()

    assert (m1.posicao, m2.posicao, m3.posicao) == (1, 9, 4)


def test_movimento_em_trilha_publicada_nao_muda_a_situacao(
    sessao, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    trilha, (_, m2, _) = _tres_missoes(
        criar_trilha, criar_missao, mestre, situacao=SituacaoDaTrilha.publicada
    )

    mover_missao(sessao, operador=mestre, missao=m2, direcao="baixo")

    assert m2.posicao == 3
    assert trilha.situacao == SituacaoDaTrilha.publicada


@pytest.mark.parametrize(
    "indice, direcao",
    [(0, "cima"), (2, "baixo"), (1, "lado")],
)
def test_recusas_sem_alterar_nada(
    sessao, criar_persona, criar_trilha, criar_missao, indice, direcao
):
    mestre = criar_persona(Papel.mestre)
    _, missoes = _tres_missoes(criar_trilha, criar_missao, mestre)

    with pytest.raises(ErroDeValidacao):
        mover_missao(sessao, operador=mestre, missao=missoes[indice], direcao=direcao)

    assert [missao.posicao for missao in missoes] == [1, 2, 3]


@pytest.mark.parametrize("indice, direcao", [(0, "baixo"), (1, "cima")])
def test_sondagem_fica_na_primeira_posicao(
    sessao, criar_persona, criar_trilha, criar_missao, indice, direcao
):
    mestre = criar_persona(Papel.mestre)
    _, missoes = _tres_missoes(criar_trilha, criar_missao, mestre, sondagem=True)

    with pytest.raises(ErroDeValidacao) as erro:
        mover_missao(sessao, operador=mestre, missao=missoes[indice], direcao=direcao)

    assert "sondagem" in erro.value.mensagem
    assert [missao.posicao for missao in missoes] == [1, 2, 3]


@pytest.mark.parametrize("papel", [Papel.mestre, Papel.admin])
def test_quem_nao_e_o_autor_e_recusado(sessao, criar_persona, criar_trilha, criar_missao, papel):
    mestre = criar_persona(Papel.mestre)
    outro = criar_persona(papel)
    _, missoes = _tres_missoes(criar_trilha, criar_missao, mestre)

    with pytest.raises(PermissaoNegada):
        mover_missao(sessao, operador=outro, missao=missoes[1], direcao="cima")

    assert [missao.posicao for missao in missoes] == [1, 2, 3]


def test_desbloqueio_permanece_e_o_percurso_segue_a_nova_ordem(
    sessao, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha, (m1, m2, m3) = _tres_missoes(
        criar_trilha, criar_missao, mestre, situacao=SituacaoDaTrilha.publicada
    )
    inscrever_na_trilha(sessao, guerreiro=guerreiro, trilha=trilha)
    sessao.add(DesbloqueioDaMissao(guerreiro_id=guerreiro.id, missao_id=m1.id, cumpriu=True))
    sessao.commit()

    mover_missao(sessao, operador=mestre, missao=m3, direcao="cima")
    sessao.commit()

    percurso = derivar_percurso(sessao, guerreiro_id=guerreiro.id, trilha_id=trilha.id)
    proxima = next(item for item in percurso if item.e_proxima)
    assert proxima.missao.id == m3.id
    assert sessao.query(DesbloqueioDaMissao).filter_by(missao_id=m1.id).count() == 1


def test_rota_move_e_devolve_as_duas(
    cliente, criar_chave, criar_sessao_de_teste, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    _, (_, m2, m3) = _tres_missoes(criar_trilha, criar_missao, mestre)

    resposta = cliente.post(
        f"/v1/missoes/{m3.id}/ordem",
        json={"direcao": "cima"},
        headers=_cabecalhos(criar_chave, criar_sessao_de_teste, mestre),
    )

    assert resposta.status_code == 200
    posicoes = {missao["id"]: missao["posicao"] for missao in resposta.json()["missoes"]}
    assert posicoes == {str(m3.id): 2, str(m2.id): 3}


def test_rota_recusa_o_admin_e_a_direcao_invalida(
    cliente, criar_chave, criar_sessao_de_teste, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    admin = criar_persona(Papel.admin)
    _, (_, m2, _) = _tres_missoes(criar_trilha, criar_missao, mestre)

    chave, _ = criar_chave()
    token_do_admin, _ = criar_sessao_de_teste(admin)
    token_do_mestre, _ = criar_sessao_de_teste(mestre)

    do_admin = cliente.post(
        f"/v1/missoes/{m2.id}/ordem",
        json={"direcao": "cima"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token_do_admin}"},
    )
    invalida = cliente.post(
        f"/v1/missoes/{m2.id}/ordem",
        json={"direcao": "lado"},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token_do_mestre}"},
    )

    assert do_admin.status_code == 403
    assert invalida.status_code == 422


@pytest.mark.banco_compartilhado
def test_a_troca_passa_pela_unicidade_no_commit_real(
    sessao, criar_persona, criar_trilha, criar_missao
):
    """Fora da transação de teste: o `COMMIT` confere a unicidade adiada de
    `uq_missao_trilha_id_posicao` sobre as duas posições trocadas (design —
    decisão 5)."""
    mestre = criar_persona(Papel.mestre)
    _, (m1, m2, _) = _tres_missoes(criar_trilha, criar_missao, mestre)

    mover_missao(sessao, operador=mestre, missao=m1, direcao="baixo")
    sessao.commit()
    sessao.expire_all()

    assert (m1.posicao, m2.posicao) == (2, 1)
