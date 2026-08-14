import uuid

import pytest

from nucleo.coletas.regra import abrir_serie_de_coleta
from nucleo.erros import ErroDeValidacao, PermissaoNegada
from nucleo.fila.modelo import EmAvaliacao
from nucleo.locais.modelo import (
    Local,
    NivelDoLocal,
    SituacaoDaSolicitacaoDeLocal,
    SolicitacaoDeLocal,
)
from nucleo.locais.regra import (
    avaliar_solicitacao_de_local,
    listar_solicitacoes_de_local_abertas,
    solicitar_local,
)
from nucleo.personas.modelo import Papel


def _solicitar(sessao, operador, desafio, comunidade, **sobrescritas):
    argumentos = {
        "operador": operador,
        "desafio": desafio,
        "comunidade_id": comunidade.id,
        "nivel": NivelDoLocal.bairro.value,
        "rotulo": "Bairro Novo",
        "justificativa": "Falta um local para registrar a coleta.",
    }
    argumentos.update(sobrescritas)
    return solicitar_local(sessao, **argumentos)


def test_guerreiro_solicita_local_na_propria_comunidade(
    sessao, criar_persona, criar_comunidade, criar_trilha, criar_missao, criar_desafio_de_coleta
):
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    desafio = criar_desafio_de_coleta(missao, mestre)

    solicitacao = _solicitar(sessao, guerreiro, desafio, comunidade)
    sessao.commit()

    assert solicitacao.situacao == SituacaoDaSolicitacaoDeLocal.recebida
    assert solicitacao.solicitante_id == guerreiro.id
    assert solicitacao.comunidade_virtual_id == comunidade.id
    assert solicitacao.desafio_de_coleta_id == desafio.id


def test_solicitacao_em_comunidade_diferente_da_do_guerreiro_e_recusada(
    sessao, criar_persona, criar_comunidade, criar_trilha, criar_missao, criar_desafio_de_coleta
):
    comunidade = criar_comunidade("Minha")
    outra_comunidade = criar_comunidade("Outra")
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    desafio = criar_desafio_de_coleta(missao, mestre)

    with pytest.raises(PermissaoNegada):
        _solicitar(sessao, guerreiro, desafio, outra_comunidade)
    assert sessao.query(SolicitacaoDeLocal).count() == 0


def test_persona_que_nao_e_guerreiro_nao_solicita_local(
    sessao, criar_persona, criar_comunidade, criar_trilha, criar_missao, criar_desafio_de_coleta
):
    comunidade = criar_comunidade()
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    desafio = criar_desafio_de_coleta(missao, mestre)

    with pytest.raises(PermissaoNegada):
        _solicitar(sessao, mestre, desafio, comunidade)
    assert sessao.query(SolicitacaoDeLocal).count() == 0


def test_solicitacao_sem_rotulo_e_recusada(
    sessao, criar_persona, criar_comunidade, criar_trilha, criar_missao, criar_desafio_de_coleta
):
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    desafio = criar_desafio_de_coleta(missao, mestre)

    with pytest.raises(ErroDeValidacao) as excinfo:
        _solicitar(sessao, guerreiro, desafio, comunidade, rotulo="")
    assert excinfo.value.campo == "rotulo"


def test_solicitacao_sem_justificativa_e_recusada(
    sessao, criar_persona, criar_comunidade, criar_trilha, criar_missao, criar_desafio_de_coleta
):
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    desafio = criar_desafio_de_coleta(missao, mestre)

    with pytest.raises(ErroDeValidacao) as excinfo:
        _solicitar(sessao, guerreiro, desafio, comunidade, justificativa="")
    assert excinfo.value.campo == "justificativa"


def test_solicitacao_com_nivel_fora_da_hierarquia_e_recusada(
    sessao, criar_persona, criar_comunidade, criar_trilha, criar_missao, criar_desafio_de_coleta
):
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    desafio = criar_desafio_de_coleta(missao, mestre)

    with pytest.raises(ErroDeValidacao) as excinfo:
        _solicitar(sessao, guerreiro, desafio, comunidade, nivel="municipio")
    assert excinfo.value.campo == "nivel"


def test_envio_da_solicitacao_nao_cria_local(
    sessao, criar_persona, criar_comunidade, criar_trilha, criar_missao, criar_desafio_de_coleta
):
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    desafio = criar_desafio_de_coleta(missao, mestre)

    _solicitar(sessao, guerreiro, desafio, comunidade)
    sessao.commit()

    assert sessao.query(Local).filter_by(comunidade_virtual_id=comunidade.id).count() == 0


def test_serie_nao_abre_no_local_ainda_pedido(
    sessao, criar_persona, criar_comunidade, criar_trilha, criar_missao, criar_desafio_de_coleta
):
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    desafio = criar_desafio_de_coleta(missao, mestre, granularidade_exigida=NivelDoLocal.bairro)

    with pytest.raises(ErroDeValidacao) as excinfo:
        abrir_serie_de_coleta(sessao, operador=guerreiro, desafio=desafio, local_id=uuid.uuid4())
    assert excinfo.value.campo == "local_id"


def _preparar_solicitacao(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
    nivel=NivelDoLocal.bairro,
):
    comunidade = criar_comunidade()
    raiz = criar_local(comunidade, nivel=NivelDoLocal.comunidade, rotulo="Raiz")
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    desafio = criar_desafio_de_coleta(missao, mestre, granularidade_exigida=nivel)
    solicitacao = _solicitar(sessao, guerreiro, desafio, comunidade, nivel=nivel.value)
    sessao.commit()
    return comunidade, raiz, guerreiro, mestre, desafio, solicitacao


def test_mestre_autor_avalia_solicitacao(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
):
    _, raiz, _, mestre, _, solicitacao = _preparar_solicitacao(
        sessao,
        criar_persona,
        criar_comunidade,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
    )

    avaliada = avaliar_solicitacao_de_local(
        sessao,
        solicitacao,
        operador=mestre,
        situacao=SituacaoDaSolicitacaoDeLocal.aprovada,
        local_pai_id=raiz.id,
    )
    sessao.commit()

    assert avaliada.situacao == SituacaoDaSolicitacaoDeLocal.aprovada
    assert avaliada.avaliador_id == mestre.id
    assert avaliada.avaliado_em is not None


def test_admin_avalia_qualquer_solicitacao(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
):
    _, raiz, _, _, _, solicitacao = _preparar_solicitacao(
        sessao,
        criar_persona,
        criar_comunidade,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
    )
    admin = criar_persona(Papel.admin)

    avaliada = avaliar_solicitacao_de_local(
        sessao,
        solicitacao,
        operador=admin,
        situacao=SituacaoDaSolicitacaoDeLocal.aprovada,
        local_pai_id=raiz.id,
    )
    sessao.commit()

    assert avaliada.situacao == SituacaoDaSolicitacaoDeLocal.aprovada
    assert avaliada.avaliador_id == admin.id


def test_mestre_de_outra_trilha_e_recusado(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
):
    _, raiz, _, _, _, solicitacao = _preparar_solicitacao(
        sessao,
        criar_persona,
        criar_comunidade,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
    )
    outro_mestre = criar_persona(Papel.mestre)

    with pytest.raises(PermissaoNegada):
        avaliar_solicitacao_de_local(
            sessao,
            solicitacao,
            operador=outro_mestre,
            situacao=SituacaoDaSolicitacaoDeLocal.aprovada,
            local_pai_id=raiz.id,
        )
    sessao.refresh(solicitacao)
    assert solicitacao.situacao == SituacaoDaSolicitacaoDeLocal.recebida


def test_guerreiro_nao_avalia_a_propria_solicitacao(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
):
    _, raiz, guerreiro, _, _, solicitacao = _preparar_solicitacao(
        sessao,
        criar_persona,
        criar_comunidade,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
    )

    with pytest.raises(PermissaoNegada):
        avaliar_solicitacao_de_local(
            sessao,
            solicitacao,
            operador=guerreiro,
            situacao=SituacaoDaSolicitacaoDeLocal.aprovada,
            local_pai_id=raiz.id,
        )


def test_aprovacao_cria_local_e_libera_abertura_da_serie(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
):
    """Critério de aceite do PRD-08 §12."""
    comunidade, raiz, guerreiro, mestre, desafio, solicitacao = _preparar_solicitacao(
        sessao,
        criar_persona,
        criar_comunidade,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
    )

    avaliada = avaliar_solicitacao_de_local(
        sessao,
        solicitacao,
        operador=mestre,
        situacao=SituacaoDaSolicitacaoDeLocal.aprovada,
        local_pai_id=raiz.id,
    )
    sessao.commit()

    local_criado = sessao.get(Local, avaliada.local_criado_id)
    assert local_criado is not None
    assert local_criado.nivel == NivelDoLocal.bairro
    assert local_criado.local_pai_id == raiz.id
    assert local_criado.comunidade_virtual_id == comunidade.id

    serie = abrir_serie_de_coleta(
        sessao, operador=guerreiro, desafio=desafio, local_id=local_criado.id
    )
    sessao.commit()
    assert serie.local_id == local_criado.id


def test_recusa_devolve_motivo_e_nao_cria_local(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
):
    comunidade, raiz, _, mestre, _, solicitacao = _preparar_solicitacao(
        sessao,
        criar_persona,
        criar_comunidade,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
    )

    avaliada = avaliar_solicitacao_de_local(
        sessao,
        solicitacao,
        operador=mestre,
        situacao=SituacaoDaSolicitacaoDeLocal.recusada,
        motivo="Já existe local equivalente na hierarquia.",
    )
    sessao.commit()

    assert avaliada.situacao == SituacaoDaSolicitacaoDeLocal.recusada
    assert avaliada.motivo_da_recusa == "Já existe local equivalente na hierarquia."
    assert avaliada.local_criado_id is None
    assert sessao.query(Local).filter_by(comunidade_virtual_id=comunidade.id).count() == 1


def test_recusa_sem_motivo_e_recusada(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
):
    _, _, _, mestre, _, solicitacao = _preparar_solicitacao(
        sessao,
        criar_persona,
        criar_comunidade,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
    )

    with pytest.raises(ErroDeValidacao) as excinfo:
        avaliar_solicitacao_de_local(
            sessao,
            solicitacao,
            operador=mestre,
            situacao=SituacaoDaSolicitacaoDeLocal.recusada,
            motivo="",
        )
    assert excinfo.value.campo == "motivo"
    sessao.refresh(solicitacao)
    assert solicitacao.situacao == SituacaoDaSolicitacaoDeLocal.recebida


def test_pai_de_nivel_que_nao_e_o_imediatamente_acima_nao_consome_solicitacao(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
):
    comunidade, raiz, _, mestre, _, solicitacao = _preparar_solicitacao(
        sessao,
        criar_persona,
        criar_comunidade,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
        nivel=NivelDoLocal.rua,
    )

    with pytest.raises(ErroDeValidacao) as excinfo:
        avaliar_solicitacao_de_local(
            sessao,
            solicitacao,
            operador=mestre,
            situacao=SituacaoDaSolicitacaoDeLocal.aprovada,
            local_pai_id=raiz.id,
        )
    assert excinfo.value.campo == "local_pai_id"
    sessao.refresh(solicitacao)
    assert solicitacao.situacao == SituacaoDaSolicitacaoDeLocal.recebida
    assert solicitacao.avaliador_id is None
    assert solicitacao.avaliado_em is None
    assert sessao.query(Local).filter_by(comunidade_virtual_id=comunidade.id).count() == 1


def test_pai_de_outra_comunidade_nao_consome_solicitacao(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
):
    comunidade, _, _, mestre, _, solicitacao = _preparar_solicitacao(
        sessao,
        criar_persona,
        criar_comunidade,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
    )
    outra_comunidade = criar_comunidade("Outra")
    raiz_de_outra = criar_local(
        outra_comunidade, nivel=NivelDoLocal.comunidade, rotulo="Outra Raiz"
    )

    with pytest.raises(ErroDeValidacao) as excinfo:
        avaliar_solicitacao_de_local(
            sessao,
            solicitacao,
            operador=mestre,
            situacao=SituacaoDaSolicitacaoDeLocal.aprovada,
            local_pai_id=raiz_de_outra.id,
        )
    assert excinfo.value.campo == "local_pai_id"
    sessao.refresh(solicitacao)
    assert solicitacao.situacao == SituacaoDaSolicitacaoDeLocal.recebida


def test_segunda_avaliacao_e_recusada_sem_criar_segundo_local(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
):
    comunidade, raiz, _, mestre, _, solicitacao = _preparar_solicitacao(
        sessao,
        criar_persona,
        criar_comunidade,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
    )
    avaliar_solicitacao_de_local(
        sessao,
        solicitacao,
        operador=mestre,
        situacao=SituacaoDaSolicitacaoDeLocal.aprovada,
        local_pai_id=raiz.id,
    )
    sessao.commit()
    local_criado_id = solicitacao.local_criado_id

    with pytest.raises(ErroDeValidacao) as excinfo:
        avaliar_solicitacao_de_local(
            sessao,
            solicitacao,
            operador=mestre,
            situacao=SituacaoDaSolicitacaoDeLocal.recusada,
            motivo="Mudei de ideia.",
        )
    assert excinfo.value.campo == "situacao"
    sessao.refresh(solicitacao)
    assert solicitacao.situacao == SituacaoDaSolicitacaoDeLocal.aprovada
    assert solicitacao.local_criado_id == local_criado_id
    assert sessao.query(Local).filter_by(comunidade_virtual_id=comunidade.id).count() == 2


def test_admin_ve_todas_as_solicitacoes_da_comunidade_filtrada(
    sessao, criar_persona, criar_comunidade, criar_trilha, criar_missao, criar_desafio_de_coleta
):
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    admin = criar_persona(Papel.admin)
    mestre_um = criar_persona(Papel.mestre)
    mestre_dois = criar_persona(Papel.mestre)
    trilha_um = criar_trilha(mestre_um)
    missao_um = criar_missao(trilha_um, mestre_um)
    desafio_um = criar_desafio_de_coleta(missao_um, mestre_um)
    trilha_dois = criar_trilha(mestre_dois)
    missao_dois = criar_missao(trilha_dois, mestre_dois)
    desafio_dois = criar_desafio_de_coleta(missao_dois, mestre_dois)

    _solicitar(sessao, guerreiro, desafio_um, comunidade, rotulo="Um")
    _solicitar(sessao, guerreiro, desafio_dois, comunidade, rotulo="Dois")
    sessao.commit()

    pagina = listar_solicitacoes_de_local_abertas(
        sessao, operador=admin, comunidade_id=comunidade.id, cursor=None, tamanho=10
    )

    assert len(pagina.itens) == 2


def test_mestre_ve_so_as_solicitacoes_das_suas_trilhas(
    sessao, criar_persona, criar_comunidade, criar_trilha, criar_missao, criar_desafio_de_coleta
):
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
    mestre_um = criar_persona(Papel.mestre)
    mestre_dois = criar_persona(Papel.mestre)
    trilha_um = criar_trilha(mestre_um)
    missao_um = criar_missao(trilha_um, mestre_um)
    desafio_um = criar_desafio_de_coleta(missao_um, mestre_um)
    trilha_dois = criar_trilha(mestre_dois)
    missao_dois = criar_missao(trilha_dois, mestre_dois)
    desafio_dois = criar_desafio_de_coleta(missao_dois, mestre_dois)

    _solicitar(sessao, guerreiro, desafio_um, comunidade, rotulo="Um")
    _solicitar(sessao, guerreiro, desafio_dois, comunidade, rotulo="Dois")
    sessao.commit()

    pagina = listar_solicitacoes_de_local_abertas(
        sessao, operador=mestre_um, comunidade_id=comunidade.id, cursor=None, tamanho=10
    )

    assert len(pagina.itens) == 1
    assert pagina.itens[0].rotulo == "Um"


def test_solicitacao_avaliada_sai_da_lista_de_abertas(
    sessao,
    criar_persona,
    criar_comunidade,
    criar_trilha,
    criar_missao,
    criar_desafio_de_coleta,
    criar_local,
):
    _, raiz, _, mestre, _, solicitacao = _preparar_solicitacao(
        sessao,
        criar_persona,
        criar_comunidade,
        criar_trilha,
        criar_missao,
        criar_desafio_de_coleta,
        criar_local,
    )

    pagina_antes = listar_solicitacoes_de_local_abertas(
        sessao,
        operador=mestre,
        comunidade_id=solicitacao.comunidade_virtual_id,
        cursor=None,
        tamanho=10,
    )
    assert len(pagina_antes.itens) == 1

    avaliar_solicitacao_de_local(
        sessao,
        solicitacao,
        operador=mestre,
        situacao=SituacaoDaSolicitacaoDeLocal.recusada,
        motivo="Não procede.",
    )
    sessao.commit()

    pagina_depois = listar_solicitacoes_de_local_abertas(
        sessao,
        operador=mestre,
        comunidade_id=solicitacao.comunidade_virtual_id,
        cursor=None,
        tamanho=10,
    )
    assert pagina_depois.itens == []


def test_persona_de_outro_papel_recebe_403_na_listagem(sessao, criar_persona, criar_comunidade):
    comunidade = criar_comunidade()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=comunidade)

    with pytest.raises(PermissaoNegada):
        listar_solicitacoes_de_local_abertas(
            sessao, operador=guerreiro, comunidade_id=comunidade.id, cursor=None, tamanho=10
        )


def test_solicitacao_de_local_nao_tem_prazo_nem_marca_de_atraso():
    """A solicitação de local fica fora do ciclo da fila única de
    avaliação: sem `EmAvaliacao`, sem `prazo`, sem atraso (`RN-08-18`)."""
    assert not issubclass(SolicitacaoDeLocal, EmAvaliacao)
    assert not hasattr(SolicitacaoDeLocal, "prazo")


def test_fila_das_quatro_naturezas_nao_devolve_solicitacao_de_local():
    from nucleo.fila.modelo import (
        SolicitacaoDeChave,
        SolicitacaoDeDados,
        SolicitacaoDeParticipacao,
        SugestaoOuProposta,
    )

    naturezas = (
        SolicitacaoDeParticipacao,
        SolicitacaoDeDados,
        SolicitacaoDeChave,
        SugestaoOuProposta,
    )
    assert SolicitacaoDeLocal not in naturezas
