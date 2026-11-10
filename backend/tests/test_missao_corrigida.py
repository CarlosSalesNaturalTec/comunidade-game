"""Fatia 28 do PRD-09: a missão se corrige em qualquer situação da trilha,
só pelo Mestre autor, e desmarcar a sondagem de trilha publicada a
despublica (`RF-09-136`, `RN-09-56`, `RN-09-57`, `RN-09-59`)."""

import pytest

from nucleo.erros import ErroDeValidacao, PermissaoNegada
from nucleo.personas.modelo import Papel
from nucleo.trilhas.modelo import DesbloqueioDaMissao, EtapaDoCiclo, SituacaoDaTrilha
from nucleo.trilhas.regra import corrigir_missao, publicar_trilha


def _cabecalhos(criar_chave, criar_sessao_de_teste, persona):
    chave, _ = criar_chave()
    token, _ = criar_sessao_de_teste(persona)
    return {"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token}"}


def _trilha_publicavel(
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_culminancia,
    mestre,
    situacao=SituacaoDaTrilha.publicada,
):
    trilha = criar_trilha(mestre, situacao=situacao)
    sondagem = criar_missao(trilha, mestre, titulo="Sondagem", posicao=1, e_sondagem=True)
    segunda = criar_missao(trilha, mestre, titulo="Segunda", posicao=2)
    criar_desafio_de_coleta(segunda, mestre)
    criar_culminancia(trilha, mestre)
    return trilha, sondagem, segunda


def test_mestre_autor_corrige_os_campos_da_missao(
    sessao, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre, titulo="Titulo errado", posicao=3)

    corrigir_missao(
        sessao,
        operador=mestre,
        missao=missao,
        campos={
            "titulo": "Título certo",
            "nivel_de_dificuldade": 3,
            "obrigatoria": False,
            "etapa_do_ciclo": "marcos",
        },
    )

    assert missao.titulo == "Título certo"
    assert missao.nivel_de_dificuldade == 3
    assert missao.obrigatoria is False
    assert missao.etapa_do_ciclo == EtapaDoCiclo.marcos
    assert missao.posicao == 3


def test_campo_ausente_conserva_o_valor(sessao, criar_persona, criar_trilha, criar_missao):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre, titulo="Original", nivel_de_dificuldade=2)

    corrigir_missao(sessao, operador=mestre, missao=missao, campos={"obrigatoria": False})

    assert missao.titulo == "Original"
    assert missao.nivel_de_dificuldade == 2


def test_correcao_em_trilha_publicada_nao_despublica(
    sessao, criar_persona, criar_trilha, criar_missao, criar_desafio_de_coleta, criar_culminancia
):
    mestre = criar_persona(Papel.mestre)
    trilha, _, segunda = _trilha_publicavel(
        criar_trilha, criar_missao, criar_desafio_de_coleta, criar_culminancia, mestre
    )

    corrigir_missao(
        sessao,
        operador=mestre,
        missao=segunda,
        campos={"titulo": "Novo título", "nivel_de_dificuldade": 4, "etapa_do_ciclo": "marcos"},
    )

    assert trilha.situacao == SituacaoDaTrilha.publicada


def test_desbloqueio_ja_gravado_permanece(sessao, criar_persona, criar_trilha, criar_missao):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    missao = criar_missao(trilha, mestre, obrigatoria=False)
    sessao.add(DesbloqueioDaMissao(guerreiro_id=guerreiro.id, missao_id=missao.id, cumpriu=True))
    sessao.commit()

    corrigir_missao(sessao, operador=mestre, missao=missao, campos={"obrigatoria": True})

    assert sessao.query(DesbloqueioDaMissao).filter_by(missao_id=missao.id).count() == 1


@pytest.mark.parametrize(
    "campos, campo",
    [
        ({"titulo": "  "}, "titulo"),
        ({"etapa_do_ciclo": "meio"}, "etapa_do_ciclo"),
        ({"obrigatoria": None}, "obrigatoria"),
        ({"nivel_de_dificuldade": None}, "nivel_de_dificuldade"),
    ],
)
def test_recusas_da_criacao_valem_na_correcao(
    sessao, criar_persona, criar_trilha, criar_missao, campos, campo
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre, titulo="Original")

    with pytest.raises(ErroDeValidacao) as erro:
        corrigir_missao(sessao, operador=mestre, missao=missao, campos=campos)

    assert erro.value.campo == campo
    assert missao.titulo == "Original"


def test_sondagem_fora_da_primeira_posicao_e_recusada(
    sessao, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre, posicao=3)

    with pytest.raises(ErroDeValidacao):
        corrigir_missao(sessao, operador=mestre, missao=missao, campos={"e_sondagem": True})

    assert missao.e_sondagem is False


def test_segunda_sondagem_e_recusada(sessao, criar_persona, criar_trilha, criar_missao):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    sondagem = criar_missao(trilha, mestre, posicao=1, e_sondagem=True)
    segunda = criar_missao(trilha, mestre, posicao=2)

    with pytest.raises(ErroDeValidacao):
        corrigir_missao(sessao, operador=mestre, missao=segunda, campos={"e_sondagem": True})

    assert segunda.e_sondagem is False
    assert sondagem.e_sondagem is True


def test_a_propria_sondagem_nao_conta_como_segunda(
    sessao, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    sondagem = criar_missao(trilha, mestre, posicao=1, e_sondagem=True)

    corrigir_missao(
        sessao, operador=mestre, missao=sondagem, campos={"e_sondagem": True, "titulo": "Novo"}
    )

    assert sondagem.e_sondagem is True


@pytest.mark.parametrize("papel", [Papel.mestre, Papel.admin])
def test_quem_nao_e_o_autor_e_recusado(sessao, criar_persona, criar_trilha, criar_missao, papel):
    mestre = criar_persona(Papel.mestre)
    outro = criar_persona(papel)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre, titulo="Original")

    with pytest.raises(PermissaoNegada):
        corrigir_missao(sessao, operador=outro, missao=missao, campos={"titulo": "Alheio"})

    assert missao.titulo == "Original"


def test_desmarcar_sondagem_de_trilha_publicada_despublica(
    sessao, criar_persona, criar_trilha, criar_missao, criar_desafio_de_coleta, criar_culminancia
):
    mestre = criar_persona(Papel.mestre)
    trilha, sondagem, _ = _trilha_publicavel(
        criar_trilha, criar_missao, criar_desafio_de_coleta, criar_culminancia, mestre
    )

    corrigir_missao(sessao, operador=mestre, missao=sondagem, campos={"e_sondagem": False})

    assert trilha.situacao == SituacaoDaTrilha.despublicada
    assert trilha.autor_da_situacao_id == mestre.id
    assert trilha.papel_do_autor_da_situacao == Papel.mestre.value
    assert trilha.situacao_alterada_em is not None
    assert '"Sondagem"' in trilha.motivo_da_situacao
    assert "a missão de sondagem" in trilha.motivo_da_situacao


def test_desmarcar_sondagem_de_rascunho_nao_muda_situacao(
    sessao, criar_persona, criar_trilha, criar_missao, criar_desafio_de_coleta, criar_culminancia
):
    mestre = criar_persona(Papel.mestre)
    trilha, sondagem, _ = _trilha_publicavel(
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_culminancia,
        mestre,
        situacao=SituacaoDaTrilha.rascunho,
    )

    corrigir_missao(sessao, operador=mestre, missao=sondagem, campos={"e_sondagem": False})

    assert trilha.situacao == SituacaoDaTrilha.rascunho
    assert trilha.motivo_da_situacao is None


def test_autor_republica_depois_de_remarcar_a_sondagem(
    sessao, criar_persona, criar_trilha, criar_missao, criar_desafio_de_coleta, criar_culminancia
):
    mestre = criar_persona(Papel.mestre)
    trilha, sondagem, _ = _trilha_publicavel(
        criar_trilha, criar_missao, criar_desafio_de_coleta, criar_culminancia, mestre
    )
    corrigir_missao(sessao, operador=mestre, missao=sondagem, campos={"e_sondagem": False})
    corrigir_missao(sessao, operador=mestre, missao=sondagem, campos={"e_sondagem": True})

    publicar_trilha(sessao, trilha, operador=mestre)

    assert trilha.situacao == SituacaoDaTrilha.publicada
    assert trilha.motivo_da_situacao is None


def test_rota_corrige_e_devolve_a_situacao_da_trilha(
    cliente,
    sessao,
    criar_chave,
    criar_sessao_de_teste,
    criar_persona,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_culminancia,
):
    mestre = criar_persona(Papel.mestre)
    trilha, sondagem, segunda = _trilha_publicavel(
        criar_trilha, criar_missao, criar_desafio_de_coleta, criar_culminancia, mestre
    )
    cabecalhos = _cabecalhos(criar_chave, criar_sessao_de_teste, mestre)

    comum = cliente.patch(
        f"/v1/missoes/{segunda.id}", json={"titulo": "Corrigida"}, headers=cabecalhos
    )
    assert comum.status_code == 200
    assert comum.json()["missao"]["titulo"] == "Corrigida"
    assert comum.json()["situacao_da_trilha"] == "publicada"
    assert comum.json()["motivo_da_situacao"] is None

    despublicando = cliente.patch(
        f"/v1/missoes/{sondagem.id}", json={"e_sondagem": False}, headers=cabecalhos
    )
    assert despublicando.status_code == 200
    assert despublicando.json()["situacao_da_trilha"] == "despublicada"
    assert "sondagem" in despublicando.json()["motivo_da_situacao"]


def test_rota_recusa_a_posicao_no_corpo(
    cliente, criar_chave, criar_sessao_de_teste, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre, posicao=2)

    resposta = cliente.patch(
        f"/v1/missoes/{missao.id}",
        json={"posicao": 1},
        headers=_cabecalhos(criar_chave, criar_sessao_de_teste, mestre),
    )

    assert resposta.status_code == 422


def test_rota_recusa_o_admin(
    cliente, criar_chave, criar_sessao_de_teste, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    admin = criar_persona(Papel.admin)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    resposta = cliente.patch(
        f"/v1/missoes/{missao.id}",
        json={"titulo": "Do Admin"},
        headers=_cabecalhos(criar_chave, criar_sessao_de_teste, admin),
    )

    assert resposta.status_code == 403


def test_correcao_so_dos_materiais_em_trilha_publicada(
    sessao, criar_persona, criar_trilha, criar_missao, criar_desafio_de_coleta, criar_culminancia
):
    """`RF-09-140`, `RN-09-61`: substitui a lista, conserva o resto e não
    mexe na situação da trilha."""
    mestre = criar_persona(Papel.mestre)
    trilha, _, segunda = _trilha_publicavel(
        criar_trilha, criar_missao, criar_desafio_de_coleta, criar_culminancia, mestre
    )

    corrigir_missao(
        sessao, operador=mestre, missao=segunda, campos={"materiais": ["papel ", "cola"]}
    )

    assert segunda.materiais == ["papel", "cola"]
    assert segunda.titulo == "Segunda"
    assert trilha.situacao == SituacaoDaTrilha.publicada


def test_lista_vazia_apaga_os_materiais(sessao, criar_persona, criar_trilha, criar_missao):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre, materiais=["papel"])

    corrigir_missao(sessao, operador=mestre, missao=missao, campos={"materiais": []})

    assert missao.materiais == []


@pytest.mark.parametrize("materiais", [None, ["cola", ""]])
def test_materiais_nulos_ou_vazios_sao_recusados(
    sessao, criar_persona, criar_trilha, criar_missao, materiais
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre, materiais=["papel"])

    with pytest.raises(ErroDeValidacao) as erro:
        corrigir_missao(sessao, operador=mestre, missao=missao, campos={"materiais": materiais})

    assert erro.value.campo == "materiais"
    assert missao.materiais == ["papel"]


def test_publicacao_sem_materiais_confere_so_as_travas_antigas(
    sessao, criar_persona, criar_trilha, criar_missao, criar_desafio_de_coleta, criar_culminancia
):
    mestre = criar_persona(Papel.mestre)
    trilha, _, _ = _trilha_publicavel(
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_culminancia,
        mestre,
        situacao=SituacaoDaTrilha.rascunho,
    )

    publicar_trilha(sessao, trilha, operador=mestre)

    assert trilha.situacao == SituacaoDaTrilha.publicada


def test_rota_corrige_os_materiais_e_recusa_o_admin(
    cliente, criar_chave, criar_sessao_de_teste, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    admin = criar_persona(Papel.admin)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    chave, _ = criar_chave()
    token_do_mestre, _ = criar_sessao_de_teste(mestre)
    token_do_admin, _ = criar_sessao_de_teste(admin)

    resposta = cliente.patch(
        f"/v1/missoes/{missao.id}",
        json={"materiais": ["cola", "jumpers"]},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token_do_mestre}"},
    )
    assert resposta.status_code == 200
    assert resposta.json()["missao"]["materiais"] == ["cola", "jumpers"]

    recusa = cliente.patch(
        f"/v1/missoes/{missao.id}",
        json={"materiais": []},
        headers={"X-Chave-Aplicacao": chave, "Authorization": f"Bearer {token_do_admin}"},
    )
    assert recusa.status_code == 403
