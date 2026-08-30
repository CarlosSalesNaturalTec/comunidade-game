import pytest

from nucleo.erros import ErroDeValidacao, PermissaoNegada
from nucleo.livro_razao.modelo import Lancamento
from nucleo.personas.modelo import Papel
from nucleo.template_de_missao.local import TemplateDeMissaoLocal
from nucleo.template_de_missao.modelo import SituacaoDaSugestaoDeEstrutura, SugestaoDeEstrutura
from nucleo.template_de_missao.porta import EstruturaSugerida, PortaDoTemplateDeMissao
from nucleo.template_de_missao.regra import (
    calcular_lacunas,
    pedir_estrutura_da_missao,
    registrar_desfecho_da_sugestao,
)


class _PortaIndisponivel(PortaDoTemplateDeMissao):
    def sugerir_estrutura(self, *, topico, exigir_atividade_desplugada):
        return None


@pytest.fixture
def porta_local():
    return TemplateDeMissaoLocal()


# --- 3.1, 3.4 O pedido de estrutura ---------------------------------------


def test_mestre_autor_pede_estrutura_e_grava_sugestao(
    sessao, criar_persona, criar_trilha, criar_missao, porta_local
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    resultado = pedir_estrutura_da_missao(
        sessao, operador=mestre, missao=missao, topico="Robótica básica", porta=porta_local
    )
    sessao.commit()

    assert resultado.disponivel is True
    assert resultado.atividades
    assert resultado.cadencia_de_retomada == [2, 7, 21]
    sugestao = sessao.get(SugestaoDeEstrutura, resultado.sugestao.id)
    assert sugestao.topico == "Robótica básica"
    assert sugestao.situacao == SituacaoDaSugestaoDeEstrutura.proposta
    assert sugestao.missao_id == missao.id


def test_quem_nao_e_autor_nao_pede_estrutura(
    sessao, criar_persona, criar_trilha, criar_missao, porta_local
):
    autor = criar_persona(Papel.mestre)
    outro_mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(autor)
    missao = criar_missao(trilha, autor)

    with pytest.raises(PermissaoNegada):
        pedir_estrutura_da_missao(
            sessao, operador=outro_mestre, missao=missao, topico="Robótica", porta=porta_local
        )
    assert sessao.query(SugestaoDeEstrutura).count() == 0


def test_pedido_sem_topico_e_recusado(
    sessao, criar_persona, criar_trilha, criar_missao, porta_local
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    with pytest.raises(ErroDeValidacao) as excinfo:
        pedir_estrutura_da_missao(
            sessao, operador=mestre, missao=missao, topico="   ", porta=porta_local
        )
    assert excinfo.value.campo == "topico"
    assert sessao.query(SugestaoDeEstrutura).count() == 0


def test_pedir_de_novo_nao_apaga_a_sugestao_anterior(
    sessao, criar_persona, criar_trilha, criar_missao, porta_local
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    primeira = pedir_estrutura_da_missao(
        sessao, operador=mestre, missao=missao, topico="Robótica", porta=porta_local
    )
    sessao.commit()
    segunda = pedir_estrutura_da_missao(
        sessao, operador=mestre, missao=missao, topico="Programação", porta=porta_local
    )
    sessao.commit()

    assert primeira.sugestao.id != segunda.sugestao.id
    assert sessao.query(SugestaoDeEstrutura).filter_by(missao_id=missao.id).count() == 2


def test_nenhum_lancamento_e_emitido_pelo_pedido(
    sessao, criar_persona, criar_trilha, criar_missao, porta_local
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    pedir_estrutura_da_missao(
        sessao, operador=mestre, missao=missao, topico="Robótica", porta=porta_local
    )
    sessao.commit()

    assert sessao.query(Lancamento).count() == 0


# --- 3.3 As lacunas --------------------------------------------------------


def test_missao_sem_atividade_e_apontada(sessao, criar_persona, criar_trilha, criar_missao):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre, cadencia_de_retomada=[2, 7, 21])

    lacunas = calcular_lacunas(sessao, missao=missao, trilha=trilha)

    assert any("nenhuma atividade" in lacuna for lacuna in lacunas)


def test_atividade_sem_producao_e_apontada(
    sessao, criar_persona, criar_trilha, criar_missao, criar_atividade
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre, cadencia_de_retomada=[2, 7, 21])
    criar_atividade(missao, mestre, titulo="Atividade sem produção", producao_esperada="")

    lacunas = calcular_lacunas(sessao, missao=missao, trilha=trilha)

    assert any("Atividade sem produção" in lacuna for lacuna in lacunas)


def test_atividade_com_producao_nao_vira_lacuna(
    sessao, criar_persona, criar_trilha, criar_missao, criar_atividade
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre, cadencia_de_retomada=[2, 7, 21])
    criar_atividade(missao, mestre, producao_esperada="Uma produção qualquer.")

    lacunas = calcular_lacunas(sessao, missao=missao, trilha=trilha)

    assert not any("produção" in lacuna for lacuna in lacunas)


def test_retomada_nao_declarada_e_apontada(
    sessao, criar_persona, criar_trilha, criar_missao, criar_atividade
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre, cadencia_de_retomada=None)
    criar_atividade(missao, mestre)

    lacunas = calcular_lacunas(sessao, missao=missao, trilha=trilha)

    assert any("retomada" in lacuna for lacuna in lacunas)


def test_missao_completa_devolve_lista_vazia(
    sessao, criar_persona, criar_poder, criar_trilha, criar_missao, criar_atividade
):
    mestre = criar_persona(Papel.mestre)
    poder = criar_poder(mestre, tecnico=True)
    trilha = criar_trilha(mestre, poder=poder)
    missao = criar_missao(trilha, mestre, cadencia_de_retomada=[2, 7, 21])
    criar_atividade(missao, mestre, natureza="desplugada", producao_esperada="Produção.")

    lacunas = calcular_lacunas(sessao, missao=missao, trilha=trilha)

    assert lacunas == []


def test_lacuna_nao_altera_a_missao(sessao, criar_persona, criar_trilha, criar_missao):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    calcular_lacunas(sessao, missao=missao, trilha=trilha)
    sessao.refresh(missao)

    assert missao.cadencia_de_retomada is None


# --- Trilha de poder técnico exige atividade desplugada --------------------


def test_trilha_de_poder_tecnico_comeca_desplugada(
    sessao, criar_persona, criar_poder, criar_trilha, criar_missao, porta_local
):
    mestre = criar_persona(Papel.mestre)
    poder = criar_poder(mestre, tecnico=True)
    trilha = criar_trilha(mestre, poder=poder)
    missao = criar_missao(trilha, mestre)

    resultado = pedir_estrutura_da_missao(
        sessao, operador=mestre, missao=missao, topico="Sensores", porta=porta_local
    )
    sessao.commit()

    assert resultado.atividades[0].desplugada is True


def test_trilha_nao_tecnica_nao_exige_desplugada(
    sessao, criar_persona, criar_trilha, criar_missao, porta_local
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    resultado = pedir_estrutura_da_missao(
        sessao, operador=mestre, missao=missao, topico="Redação", porta=porta_local
    )
    sessao.commit()

    assert not any(atividade.desplugada for atividade in resultado.atividades)


def test_missao_de_trilha_tecnica_sem_desplugada_e_apontada(
    sessao, criar_persona, criar_poder, criar_trilha, criar_missao, criar_atividade
):
    mestre = criar_persona(Papel.mestre)
    poder = criar_poder(mestre, tecnico=True)
    trilha = criar_trilha(mestre, poder=poder)
    missao = criar_missao(trilha, mestre, cadencia_de_retomada=[2, 7, 21])
    criar_atividade(missao, mestre, natureza="construcao", producao_esperada="Produção.")

    lacunas = calcular_lacunas(sessao, missao=missao, trilha=trilha)

    assert any("desplugada" in lacuna for lacuna in lacunas)


# --- 3.2, decisão 3: indisponibilidade -------------------------------------


def test_indisponibilidade_do_modelo_nao_trava_e_devolve_lacunas(
    sessao, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    resultado = pedir_estrutura_da_missao(
        sessao,
        operador=mestre,
        missao=missao,
        topico="Robótica",
        porta=_PortaIndisponivel(),
    )
    sessao.commit()

    assert resultado.disponivel is False
    assert resultado.atividades == []
    assert any("nenhuma atividade" in lacuna for lacuna in resultado.lacunas)
    assert resultado.cadencia_de_retomada == [2, 7, 21]


def test_tópico_sem_ods_derivavel_nao_recebe_objetivo(
    sessao, criar_persona, criar_trilha, criar_missao, porta_local
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    resultado = pedir_estrutura_da_missao(
        sessao,
        operador=mestre,
        missao=missao,
        topico="xyz sem sentido algum",
        porta=porta_local,
    )
    sessao.commit()

    assert resultado.objetivo_ods is None


def test_topico_com_ods_derivavel_traz_o_objetivo(
    sessao, criar_persona, criar_trilha, criar_missao, porta_local
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    resultado = pedir_estrutura_da_missao(
        sessao,
        operador=mestre,
        missao=missao,
        topico="Como cuidar da água da nossa comunidade",
        porta=porta_local,
    )
    sessao.commit()

    assert resultado.objetivo_ods == 6


# --- 3.6 O desfecho da sugestão --------------------------------------------


def test_registrar_desfecho_aceita(sessao, criar_persona, criar_trilha, criar_missao, porta_local):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    resultado = pedir_estrutura_da_missao(
        sessao, operador=mestre, missao=missao, topico="Robótica", porta=porta_local
    )
    sessao.commit()

    registrar_desfecho_da_sugestao(
        sessao,
        operador=mestre,
        sugestao=resultado.sugestao,
        situacao=SituacaoDaSugestaoDeEstrutura.aceita,
    )
    sessao.commit()
    sessao.refresh(resultado.sugestao)

    assert resultado.sugestao.situacao == SituacaoDaSugestaoDeEstrutura.aceita


def test_recusar_a_sugestao_nao_altera_a_missao(
    sessao, criar_persona, criar_trilha, criar_missao, porta_local
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre, cadencia_de_retomada=None)
    resultado = pedir_estrutura_da_missao(
        sessao, operador=mestre, missao=missao, topico="Robótica", porta=porta_local
    )
    sessao.commit()

    registrar_desfecho_da_sugestao(
        sessao,
        operador=mestre,
        sugestao=resultado.sugestao,
        situacao=SituacaoDaSugestaoDeEstrutura.recusada,
    )
    sessao.commit()
    sessao.refresh(missao)
    sessao.refresh(resultado.sugestao)

    assert resultado.sugestao.situacao == SituacaoDaSugestaoDeEstrutura.recusada
    assert missao.cadencia_de_retomada is None
    from nucleo.trilhas.modelo import Atividade

    assert sessao.query(Atividade).filter_by(missao_id=missao.id).count() == 0


def test_desfecho_com_situacao_invalida_e_recusado(
    sessao, criar_persona, criar_trilha, criar_missao, porta_local
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    resultado = pedir_estrutura_da_missao(
        sessao, operador=mestre, missao=missao, topico="Robótica", porta=porta_local
    )
    sessao.commit()

    with pytest.raises(ErroDeValidacao) as excinfo:
        registrar_desfecho_da_sugestao(
            sessao,
            operador=mestre,
            sugestao=resultado.sugestao,
            situacao=SituacaoDaSugestaoDeEstrutura.proposta,
        )
    assert excinfo.value.campo == "situacao"


def test_desfecho_por_quem_nao_e_autor_e_recusado(
    sessao, criar_persona, criar_trilha, criar_missao, porta_local
):
    mestre = criar_persona(Papel.mestre)
    outro_mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    resultado = pedir_estrutura_da_missao(
        sessao, operador=mestre, missao=missao, topico="Robótica", porta=porta_local
    )
    sessao.commit()

    with pytest.raises(PermissaoNegada):
        registrar_desfecho_da_sugestao(
            sessao,
            operador=outro_mestre,
            sugestao=resultado.sugestao,
            situacao=SituacaoDaSugestaoDeEstrutura.aceita,
        )


# --- Adaptador local (contrato, não a redação do modelo) -------------------


def test_adaptador_local_nunca_chama_rede(porta_local):
    resultado = porta_local.sugerir_estrutura(
        topico="Qualquer tópico", exigir_atividade_desplugada=False
    )

    assert isinstance(resultado, EstruturaSugerida)
    assert resultado.atividades
