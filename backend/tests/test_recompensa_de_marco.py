from decimal import Decimal

import pytest

from nucleo.erros import ErroDeValidacao, PermissaoNegada
from nucleo.personas.modelo import Papel
from nucleo.recompensas_de_marco.modelo import RecompensaDeMarco
from nucleo.recompensas_de_marco.regra import declarar_recompensa_de_marco


def test_mestre_autor_declara_recompensa_de_marco(
    sessao, criar_persona, criar_trilha, criar_missao, criar_tipo_de_recurso
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    tipo = criar_tipo_de_recurso(mestre)

    recompensa = declarar_recompensa_de_marco(
        sessao,
        operador=mestre,
        trilha=trilha,
        missao=missao,
        tipo=tipo,
        quantidade=Decimal("30"),
    )
    sessao.commit()

    assert recompensa.trilha_id == trilha.id
    assert recompensa.missao_id == missao.id
    assert recompensa.tipo_de_recurso_id == tipo.id
    assert recompensa.quantidade == Decimal("30")
    assert recompensa.autor_id == mestre.id
    assert recompensa.papel_do_autor == Papel.mestre.value


def test_mestre_que_nao_e_autor_nao_declara(
    sessao, criar_persona, criar_trilha, criar_missao, criar_tipo_de_recurso
):
    mestre = criar_persona(Papel.mestre)
    outro_mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    tipo = criar_tipo_de_recurso(mestre)

    with pytest.raises(PermissaoNegada):
        declarar_recompensa_de_marco(
            sessao,
            operador=outro_mestre,
            trilha=trilha,
            missao=missao,
            tipo=tipo,
            quantidade=Decimal("1"),
        )
    assert sessao.query(RecompensaDeMarco).count() == 0


def test_marco_que_nao_e_missao_da_trilha_e_recusado(
    sessao, criar_persona, criar_trilha, criar_missao, criar_tipo_de_recurso
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    outra_trilha = criar_trilha(mestre, nome="Outra Trilha")
    missao_de_outra_trilha = criar_missao(outra_trilha, mestre)
    tipo = criar_tipo_de_recurso(mestre)

    with pytest.raises(ErroDeValidacao) as excinfo:
        declarar_recompensa_de_marco(
            sessao,
            operador=mestre,
            trilha=trilha,
            missao=missao_de_outra_trilha,
            tipo=tipo,
            quantidade=Decimal("1"),
        )
    assert excinfo.value.campo == "missao_id"
    assert sessao.query(RecompensaDeMarco).count() == 0


def test_declaracao_sem_marco_e_recusada(
    sessao, criar_persona, criar_trilha, criar_tipo_de_recurso
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    tipo = criar_tipo_de_recurso(mestre)

    with pytest.raises(ErroDeValidacao) as excinfo:
        declarar_recompensa_de_marco(
            sessao, operador=mestre, trilha=trilha, missao=None, tipo=tipo, quantidade=Decimal("1")
        )
    assert excinfo.value.campo == "missao_id"
    assert sessao.query(RecompensaDeMarco).count() == 0


def test_declaracao_com_preco_e_recusada_pela_rota(
    sessao,
    cliente,
    criar_chave,
    criar_sessao_de_teste,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_tipo_de_recurso,
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    tipo = criar_tipo_de_recurso(mestre)
    sessao.commit()

    chave, _ = criar_chave()
    token, _ = criar_sessao_de_teste(mestre)

    resposta = cliente.post(
        f"/v1/trilhas/{trilha.id}/recompensas-de-marco",
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"},
        json={
            "missao_id": str(missao.id),
            "tipo_de_recurso_id": str(tipo.id),
            "quantidade": "30",
            "preco_em_pontos_extras": 40,
        },
    )

    assert resposta.status_code == 422
    assert sessao.query(RecompensaDeMarco).count() == 0
