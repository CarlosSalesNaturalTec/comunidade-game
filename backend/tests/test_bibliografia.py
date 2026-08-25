import pytest

from nucleo.bibliografias.modelo import BibliografiaDaMissao
from nucleo.bibliografias.regra import (
    criar_bibliografia,
    ler_disponibilidade_e_credito,
)
from nucleo.erros import ErroDeValidacao, PermissaoNegada
from nucleo.personas.modelo import Papel
from nucleo.poderes.modelo import NaturezaDoPoder


def _missao_do_mestre(criar_persona, criar_poder, criar_trilha, criar_missao):
    mestre = criar_persona(Papel.mestre)
    poder = criar_poder(mestre, natureza=NaturezaDoPoder.de_guerreiro)
    trilha = criar_trilha(mestre, poder=poder)
    missao = criar_missao(trilha, mestre)
    return mestre, missao


def test_mestre_autor_declara_bibliografia_sem_exemplar(
    sessao, criar_persona, criar_poder, criar_trilha, criar_missao
):
    mestre, missao = _missao_do_mestre(criar_persona, criar_poder, criar_trilha, criar_missao)

    bibliografia = criar_bibliografia(
        sessao,
        operador=mestre,
        missao=missao,
        titulo="Robótica Educativa — Eletrônica",
        capitulo="Capítulo 3 — Sensores",
        item_patrimonial_id=None,
    )
    sessao.commit()

    assert bibliografia.missao_id == missao.id
    assert bibliografia.item_patrimonial_id is None


def test_bibliografia_sem_capitulo_e_recusada(
    sessao, criar_persona, criar_poder, criar_trilha, criar_missao
):
    mestre, missao = _missao_do_mestre(criar_persona, criar_poder, criar_trilha, criar_missao)

    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_bibliografia(
            sessao,
            operador=mestre,
            missao=missao,
            titulo="Robótica Educativa",
            capitulo=None,
            item_patrimonial_id=None,
        )
    assert excinfo.value.campo == "capitulo"
    assert sessao.query(BibliografiaDaMissao).count() == 0


def test_mestre_que_nao_e_autor_e_recusado(
    sessao, criar_persona, criar_poder, criar_trilha, criar_missao
):
    mestre_autor, missao = _missao_do_mestre(criar_persona, criar_poder, criar_trilha, criar_missao)
    outro_mestre = criar_persona(Papel.mestre)

    with pytest.raises(PermissaoNegada):
        criar_bibliografia(
            sessao,
            operador=outro_mestre,
            missao=missao,
            titulo="Robótica Educativa",
            capitulo="Capítulo 3",
            item_patrimonial_id=None,
        )
    assert sessao.query(BibliografiaDaMissao).count() == 0


def test_missao_admite_mais_de_uma_entrada(
    sessao, criar_persona, criar_poder, criar_trilha, criar_missao
):
    mestre, missao = _missao_do_mestre(criar_persona, criar_poder, criar_trilha, criar_missao)

    criar_bibliografia(
        sessao,
        operador=mestre,
        missao=missao,
        titulo="Título 1",
        capitulo="Cap. 1",
        item_patrimonial_id=None,
    )
    criar_bibliografia(
        sessao,
        operador=mestre,
        missao=missao,
        titulo="Título 2",
        capitulo="Cap. 2",
        item_patrimonial_id=None,
    )
    sessao.commit()

    assert sessao.query(BibliografiaDaMissao).filter_by(missao_id=missao.id).count() == 2


def test_bibliografia_com_exemplar_existente_e_aceita(
    sessao,
    criar_persona,
    criar_poder,
    criar_trilha,
    criar_missao,
    criar_ponto_de_apoio,
    criar_item_patrimonial,
):
    mestre, missao = _missao_do_mestre(criar_persona, criar_poder, criar_trilha, criar_missao)
    admin = criar_persona(Papel.admin)
    ponto_de_apoio = criar_ponto_de_apoio(admin, _comunidade(sessao))
    item = criar_item_patrimonial(admin, ponto_de_apoio)

    bibliografia = criar_bibliografia(
        sessao,
        operador=mestre,
        missao=missao,
        titulo="Robótica Educativa",
        capitulo="Capítulo 3",
        item_patrimonial_id=item.id,
    )
    sessao.commit()

    assert bibliografia.item_patrimonial_id == item.id


def _comunidade(sessao):
    from nucleo.comunidades.modelo import ComunidadeVirtual

    comunidade = ComunidadeVirtual(
        nome="Comunidade de Teste", localizacao="Bairro de Teste", granularidade_maxima="rua"
    )
    sessao.add(comunidade)
    sessao.commit()
    sessao.refresh(comunidade)
    return comunidade


def test_exemplar_inexistente_e_recusado(
    sessao, criar_persona, criar_poder, criar_trilha, criar_missao
):
    import uuid

    mestre, missao = _missao_do_mestre(criar_persona, criar_poder, criar_trilha, criar_missao)

    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_bibliografia(
            sessao,
            operador=mestre,
            missao=missao,
            titulo="Robótica Educativa",
            capitulo="Capítulo 3",
            item_patrimonial_id=uuid.uuid4(),
        )
    assert excinfo.value.campo == "item_patrimonial_id"
    assert sessao.query(BibliografiaDaMissao).count() == 0


# --- Leitura: disponibilidade e crédito ao Apoiador -------------------------


def test_entrada_sem_vinculo_nada_afirma(
    sessao, criar_persona, criar_poder, criar_trilha, criar_missao, criar_bibliografia_da_missao
):
    mestre, missao = _missao_do_mestre(criar_persona, criar_poder, criar_trilha, criar_missao)
    bibliografia = criar_bibliografia_da_missao(missao, mestre, item_patrimonial=None)

    disponivel, apoiador = ler_disponibilidade_e_credito(
        sessao, bibliografia, ponto_de_apoio_id=None
    )

    assert disponivel is None
    assert apoiador is None


def test_entrada_vinculada_informa_disponibilidade_no_proprio_ponto(
    sessao,
    criar_persona,
    criar_poder,
    criar_trilha,
    criar_missao,
    criar_bibliografia_da_missao,
    criar_ponto_de_apoio,
    criar_item_patrimonial,
):
    mestre, missao = _missao_do_mestre(criar_persona, criar_poder, criar_trilha, criar_missao)
    admin = criar_persona(Papel.admin)
    ponto_de_apoio = criar_ponto_de_apoio(admin, _comunidade(sessao))
    item = criar_item_patrimonial(admin, ponto_de_apoio)
    bibliografia = criar_bibliografia_da_missao(missao, mestre, item_patrimonial=item)

    disponivel, _ = ler_disponibilidade_e_credito(
        sessao, bibliografia, ponto_de_apoio_id=ponto_de_apoio.id
    )

    assert disponivel is True


def test_exemplar_tombado_em_outro_ponto_de_apoio(
    sessao,
    criar_persona,
    criar_poder,
    criar_trilha,
    criar_missao,
    criar_bibliografia_da_missao,
    criar_ponto_de_apoio,
    criar_item_patrimonial,
):
    mestre, missao = _missao_do_mestre(criar_persona, criar_poder, criar_trilha, criar_missao)
    admin = criar_persona(Papel.admin)
    comunidade = _comunidade(sessao)
    ponto_do_exemplar = criar_ponto_de_apoio(admin, comunidade, nome="Ponto A")
    outro_ponto = criar_ponto_de_apoio(admin, comunidade, nome="Ponto B")
    item = criar_item_patrimonial(admin, ponto_do_exemplar)
    bibliografia = criar_bibliografia_da_missao(missao, mestre, item_patrimonial=item)

    disponivel, _ = ler_disponibilidade_e_credito(
        sessao, bibliografia, ponto_de_apoio_id=outro_ponto.id
    )

    assert disponivel is False


def test_exemplar_com_aporte_de_origem_credita_o_apoiador(
    sessao,
    criar_persona,
    criar_poder,
    criar_trilha,
    criar_missao,
    criar_bibliografia_da_missao,
    criar_ponto_de_apoio,
    criar_item_patrimonial,
    criar_tipo_de_recurso,
    criar_lancamento,
    criar_aporte,
):
    mestre, missao = _missao_do_mestre(criar_persona, criar_poder, criar_trilha, criar_missao)
    admin = criar_persona(Papel.admin)
    apoiador = criar_persona(Papel.apoiador)
    comunidade = _comunidade(sessao)
    ponto_de_apoio = criar_ponto_de_apoio(admin, comunidade)
    tipo = criar_tipo_de_recurso(admin)
    lancamento = criar_lancamento(admin, tipo, ponto_de_apoio)
    aporte = criar_aporte(admin, apoiador, tipo, ponto_de_apoio, lancamento)
    item = criar_item_patrimonial(admin, ponto_de_apoio, aporte_de_origem=aporte)
    bibliografia = criar_bibliografia_da_missao(missao, mestre, item_patrimonial=item)

    _, apoiador_creditado = ler_disponibilidade_e_credito(
        sessao, bibliografia, ponto_de_apoio_id=ponto_de_apoio.id
    )

    assert apoiador_creditado is not None
    assert apoiador_creditado.id == apoiador.id


def test_exemplar_sem_aporte_de_origem_nao_credita_ninguem(
    sessao,
    criar_persona,
    criar_poder,
    criar_trilha,
    criar_missao,
    criar_bibliografia_da_missao,
    criar_ponto_de_apoio,
    criar_item_patrimonial,
):
    mestre, missao = _missao_do_mestre(criar_persona, criar_poder, criar_trilha, criar_missao)
    admin = criar_persona(Papel.admin)
    ponto_de_apoio = criar_ponto_de_apoio(admin, _comunidade(sessao))
    item = criar_item_patrimonial(admin, ponto_de_apoio, aporte_de_origem=None)
    bibliografia = criar_bibliografia_da_missao(missao, mestre, item_patrimonial=item)

    _, apoiador_creditado = ler_disponibilidade_e_credito(
        sessao, bibliografia, ponto_de_apoio_id=ponto_de_apoio.id
    )

    assert apoiador_creditado is None


def test_mestre_nao_digita_o_credito(
    sessao, criar_persona, criar_poder, criar_trilha, criar_missao
):
    """`RF-09-23`: `criar_bibliografia` nem sequer aceita um parâmetro de
    Apoiador — o crédito só existe na leitura, nunca gravado."""
    import inspect

    from nucleo.bibliografias.regra import criar_bibliografia as funcao

    assinatura = inspect.signature(funcao)
    assert "apoiador" not in assinatura.parameters
    assert "apoiador_id" not in assinatura.parameters
