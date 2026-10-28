import uuid
from datetime import UTC, datetime

import pytest

from nucleo.atividades.regra import cadastrar_atividade_avulsa
from nucleo.erros import ErroDeValidacao, NaoEncontrado, PermissaoNegada
from nucleo.personas.modelo import Papel
from nucleo.quiz.modelo import PartidaDeQuiz, SituacaoDaPartida
from nucleo.resultados.modelo import DesfechoDoResultado, Resultado
from nucleo.trilhas.modelo import (
    Atividade,
    FormatoDeAtividade,
    ModalidadeDeAtividade,
    SituacaoDaTrilha,
)
from nucleo.trilhas.regra import (
    FatosDaAtividade,
    atividade_vigente,
    corrigir_atividade,
    criar_atividade,
    fatos_da_atividade,
    remover_atividade,
)

# `RF-09-69`, `RF-09-73`: a atividade presencial declara a aula em que
# acontece — cenários do delta `atividade-de-trilha`.


def test_mestre_autor_declara_a_aula_da_atividade_presencial(
    sessao, criar_persona, criar_trilha, criar_missao, criar_comunidade, criar_aula
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    comunidade = criar_comunidade()
    aula = criar_aula(mestre, comunidade)

    atividade = criar_atividade(
        sessao,
        operador=mestre,
        missao=missao,
        titulo="Montagem do robô",
        modalidade=ModalidadeDeAtividade.individual,
        formato=FormatoDeAtividade.presencial,
        natureza="construcao",
        producao_esperada="Construir o próprio robô.",
        aula_id=aula.id,
    )
    sessao.commit()

    assert atividade.aula_id == aula.id


def test_atividade_sem_aula_declarada_segue_valida(
    sessao, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    atividade = criar_atividade(
        sessao,
        operador=mestre,
        missao=missao,
        titulo="Montagem do robô",
        modalidade=ModalidadeDeAtividade.individual,
        formato=FormatoDeAtividade.presencial,
        natureza="construcao",
        producao_esperada="Construir o próprio robô.",
    )
    sessao.commit()

    assert atividade.aula_id is None


def test_atividade_on_line_ou_assincrona_que_declara_aula_e_recusada(
    sessao, criar_persona, criar_trilha, criar_missao, criar_comunidade, criar_aula
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    comunidade = criar_comunidade()
    aula = criar_aula(mestre, comunidade)

    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_atividade(
            sessao,
            operador=mestre,
            missao=missao,
            titulo="Fórum de discussão",
            modalidade=ModalidadeDeAtividade.individual,
            formato=FormatoDeAtividade.on_line_assincrona,
            natureza="reflexao",
            producao_esperada="Escrever uma reflexão.",
            aula_id=aula.id,
        )
    assert excinfo.value.campo == "aula_id"
    assert sessao.query(Atividade).count() == 0


def test_mestre_que_nao_e_autor_nao_declara_a_aula(
    sessao, criar_persona, criar_trilha, criar_missao, criar_comunidade, criar_aula
):
    mestre_autor = criar_persona(Papel.mestre)
    outro_mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre_autor)
    missao = criar_missao(trilha, mestre_autor)
    comunidade = criar_comunidade()
    aula = criar_aula(mestre_autor, comunidade)

    with pytest.raises(PermissaoNegada):
        criar_atividade(
            sessao,
            operador=outro_mestre,
            missao=missao,
            titulo="Montagem do robô",
            modalidade=ModalidadeDeAtividade.individual,
            formato=FormatoDeAtividade.presencial,
            natureza="construcao",
            producao_esperada="Construir o próprio robô.",
            aula_id=aula.id,
        )
    assert sessao.query(Atividade).count() == 0


def test_aula_inexistente_e_recusada(sessao, criar_persona, criar_trilha, criar_missao):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_atividade(
            sessao,
            operador=mestre,
            missao=missao,
            titulo="Montagem do robô",
            modalidade=ModalidadeDeAtividade.individual,
            formato=FormatoDeAtividade.presencial,
            natureza="construcao",
            producao_esperada="Construir o próprio robô.",
            aula_id=uuid.uuid4(),
        )
    assert excinfo.value.campo == "aula_id"
    assert sessao.query(Atividade).count() == 0


def test_atividade_criada_com_titulo_e_descricao(sessao, criar_persona, criar_trilha, criar_missao):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    atividade = criar_atividade(
        sessao,
        operador=mestre,
        missao=missao,
        titulo="Montagem do robô",
        descricao="Montar o chassi e conectar os sensores.",
        modalidade=ModalidadeDeAtividade.individual,
        formato=FormatoDeAtividade.presencial,
        natureza="construcao",
        producao_esperada="Construir o próprio robô.",
    )
    sessao.commit()

    assert atividade.missao_id == missao.id
    assert atividade.titulo == "Montagem do robô"
    assert atividade.descricao == "Montar o chassi e conectar os sensores."
    assert atividade.autor_id == mestre.id
    assert atividade.registrado_em is not None


def test_atividade_sem_descricao_e_aceita(sessao, criar_persona, criar_trilha, criar_missao):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    atividade = criar_atividade(
        sessao,
        operador=mestre,
        missao=missao,
        titulo="Montagem do robô",
        modalidade=ModalidadeDeAtividade.individual,
        formato=FormatoDeAtividade.presencial,
        natureza="construcao",
        producao_esperada="Construir o próprio robô.",
    )
    sessao.commit()

    assert atividade.descricao is None


def test_atividade_sem_titulo_e_recusada(sessao, criar_persona, criar_trilha, criar_missao):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_atividade(
            sessao,
            operador=mestre,
            missao=missao,
            titulo=None,
            modalidade=ModalidadeDeAtividade.individual,
            formato=FormatoDeAtividade.presencial,
            natureza="construcao",
            producao_esperada="Construir algo.",
        )
    assert excinfo.value.campo == "titulo"
    assert sessao.query(Atividade).count() == 0


def test_atividade_sem_missao_e_recusada(sessao, criar_persona):
    mestre = criar_persona(Papel.mestre)

    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_atividade(
            sessao,
            operador=mestre,
            missao=None,
            titulo="Atividade",
            modalidade=ModalidadeDeAtividade.individual,
            formato=FormatoDeAtividade.presencial,
            natureza="construcao",
            producao_esperada="Construir algo.",
        )
    assert excinfo.value.campo == "missao_id"
    assert sessao.query(Atividade).count() == 0


def test_mestre_que_nao_e_autor_e_recusado(sessao, criar_persona, criar_trilha, criar_missao):
    mestre_autor = criar_persona(Papel.mestre)
    outro_mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre_autor)
    missao = criar_missao(trilha, mestre_autor)

    with pytest.raises(PermissaoNegada):
        criar_atividade(
            sessao,
            operador=outro_mestre,
            missao=missao,
            titulo="Atividade",
            modalidade=ModalidadeDeAtividade.individual,
            formato=FormatoDeAtividade.presencial,
            natureza="construcao",
            producao_esperada="Construir algo.",
        )
    assert sessao.query(Atividade).count() == 0


def test_eixos_se_combinam_livremente(sessao, criar_persona, criar_trilha, criar_missao):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    atividade = criar_atividade(
        sessao,
        operador=mestre,
        missao=missao,
        titulo="Batalha",
        modalidade=ModalidadeDeAtividade.em_equipe,
        formato=FormatoDeAtividade.presencial,
        natureza="construcao",
        producao_esperada="Construir atacante, escudo e torre.",
    )
    sessao.commit()

    assert atividade.modalidade == ModalidadeDeAtividade.em_equipe
    assert atividade.formato == FormatoDeAtividade.presencial
    assert atividade.natureza == "construcao"


def test_atividade_sem_modalidade_e_recusada(sessao, criar_persona, criar_trilha, criar_missao):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_atividade(
            sessao,
            operador=mestre,
            missao=missao,
            titulo="Atividade",
            modalidade=None,
            formato=FormatoDeAtividade.presencial,
            natureza="construcao",
            producao_esperada="Construir algo.",
        )
    assert excinfo.value.campo == "modalidade"
    assert sessao.query(Atividade).count() == 0


def test_atividade_sem_formato_e_recusada(sessao, criar_persona, criar_trilha, criar_missao):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_atividade(
            sessao,
            operador=mestre,
            missao=missao,
            titulo="Atividade",
            modalidade=ModalidadeDeAtividade.individual,
            formato=None,
            natureza="construcao",
            producao_esperada="Construir algo.",
        )
    assert excinfo.value.campo == "formato"
    assert sessao.query(Atividade).count() == 0


def test_natureza_nova_e_aceita(sessao, criar_persona, criar_trilha, criar_missao):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    atividade = criar_atividade(
        sessao,
        operador=mestre,
        missao=missao,
        titulo="Atividade",
        modalidade=ModalidadeDeAtividade.individual,
        formato=FormatoDeAtividade.presencial,
        natureza="expressao_artistica",
        producao_esperada="Declamar uma rima.",
    )
    sessao.commit()

    assert atividade.natureza == "expressao_artistica"


def test_natureza_e_normalizada_antes_de_gravar(sessao, criar_persona, criar_trilha, criar_missao):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    atividade = criar_atividade(
        sessao,
        operador=mestre,
        missao=missao,
        titulo="Atividade",
        modalidade=ModalidadeDeAtividade.individual,
        formato=FormatoDeAtividade.presencial,
        natureza="  Construção  ",
        producao_esperada="Construir algo.",
    )
    sessao.commit()

    assert atividade.natureza == "construção"


def test_modalidade_fora_dos_valores_previstos_e_recusada(
    sessao, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_atividade(
            sessao,
            operador=mestre,
            missao=missao,
            titulo="Atividade",
            modalidade="modalidade-inexistente",
            formato=FormatoDeAtividade.presencial,
            natureza="construcao",
            producao_esperada="Construir algo.",
        )
    assert excinfo.value.campo == "modalidade"
    assert sessao.query(Atividade).count() == 0


def test_formato_fora_dos_valores_previstos_e_recusada(
    sessao, criar_persona, criar_trilha, criar_missao
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_atividade(
            sessao,
            operador=mestre,
            missao=missao,
            titulo="Atividade",
            modalidade=ModalidadeDeAtividade.individual,
            formato="formato-inexistente",
            natureza="construcao",
            producao_esperada="Construir algo.",
        )
    assert excinfo.value.campo == "formato"
    assert sessao.query(Atividade).count() == 0


def test_atividade_sem_natureza_e_recusada(sessao, criar_persona, criar_trilha, criar_missao):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_atividade(
            sessao,
            operador=mestre,
            missao=missao,
            titulo="Atividade",
            modalidade=ModalidadeDeAtividade.individual,
            formato=FormatoDeAtividade.presencial,
            natureza="",
            producao_esperada="Construir algo.",
        )
    assert excinfo.value.campo == "natureza"
    assert sessao.query(Atividade).count() == 0


def test_atividade_com_producao_declarada(sessao, criar_persona, criar_trilha, criar_missao):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    atividade = criar_atividade(
        sessao,
        operador=mestre,
        missao=missao,
        titulo="Atividade",
        modalidade=ModalidadeDeAtividade.individual,
        formato=FormatoDeAtividade.presencial,
        natureza="construcao",
        producao_esperada="Construir o próprio robô.",
    )
    sessao.commit()

    assert atividade.producao_esperada == "Construir o próprio robô."


def test_atividade_sem_producao_e_recusada(sessao, criar_persona, criar_trilha, criar_missao):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)

    with pytest.raises(ErroDeValidacao) as excinfo:
        criar_atividade(
            sessao,
            operador=mestre,
            missao=missao,
            titulo="Atividade",
            modalidade=ModalidadeDeAtividade.individual,
            formato=FormatoDeAtividade.presencial,
            natureza="construcao",
            producao_esperada=None,
        )
    assert excinfo.value.campo == "producao_esperada"
    assert sessao.query(Atividade).count() == 0


# `RF-09-127`, `RN-09-48`, `RN-09-49`: o Mestre autor corrige a atividade que
# já criou — cenários do delta `atividade-de-trilha`.


@pytest.fixture
def atividade_gravada(sessao, criar_missao):
    def _criar(mestre, trilha, **campos) -> Atividade:
        missao = campos.pop("missao", None) or criar_missao(trilha, mestre)
        padroes = {
            "titulo": "Montagem do robô",
            "modalidade": ModalidadeDeAtividade.individual,
            "formato": FormatoDeAtividade.presencial,
            "natureza": "construcao",
            "producao_esperada": "Construir o próprio robô.",
        }
        atividade = criar_atividade(sessao, operador=mestre, missao=missao, **(padroes | campos))
        sessao.commit()
        return atividade

    return _criar


def test_mestre_autor_corrige_o_titulo_da_atividade(
    sessao, criar_persona, criar_trilha, atividade_gravada
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    atividade = atividade_gravada(mestre, trilha)
    missao_id = atividade.missao_id

    corrigida = corrigir_atividade(
        sessao, operador=mestre, atividade=atividade, campos={"titulo": "Montagem da ponte"}
    )
    sessao.commit()

    assert corrigida.titulo == "Montagem da ponte"
    assert corrigida.missao_id == missao_id


def test_a_correcao_alcanca_a_trilha_publicada(
    sessao, criar_persona, criar_trilha, atividade_gravada
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    atividade = atividade_gravada(mestre, trilha)

    corrigir_atividade(
        sessao,
        operador=mestre,
        atividade=atividade,
        campos={"producao_esperada": "Construir a ponte em dupla."},
    )
    sessao.commit()

    assert atividade.producao_esperada == "Construir a ponte em dupla."
    assert trilha.situacao == SituacaoDaTrilha.publicada


def test_o_resultado_ja_lancado_nao_e_tocado_pela_correcao(
    sessao,
    criar_persona,
    criar_trilha,
    criar_comunidade,
    criar_aula,
    atividade_gravada,
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    atividade = atividade_gravada(mestre, trilha)
    aula = criar_aula(mestre, criar_comunidade())
    resultado = Resultado(
        guerreiro_id=guerreiro.id,
        atividade_id=atividade.id,
        aula_id=aula.id,
        producao="Robô montado.",
        desfecho=DesfechoDoResultado.realizada,
        momento_do_fato=datetime.now(UTC),
        autor_id=mestre.id,
        papel_do_autor=mestre.papel.value,
    )
    sessao.add(resultado)
    sessao.commit()

    corrigir_atividade(
        sessao,
        operador=mestre,
        atividade=atividade,
        campos={"modalidade": ModalidadeDeAtividade.em_equipe_com_familiar},
    )
    sessao.commit()

    assert atividade.modalidade == ModalidadeDeAtividade.em_equipe_com_familiar
    assert sessao.query(Resultado).count() == 1
    assert resultado.desfecho == DesfechoDoResultado.realizada


def test_correcao_sem_titulo_e_recusada(sessao, criar_persona, criar_trilha, atividade_gravada):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    atividade = atividade_gravada(mestre, trilha)

    with pytest.raises(ErroDeValidacao) as excinfo:
        corrigir_atividade(sessao, operador=mestre, atividade=atividade, campos={"titulo": "  "})
    assert excinfo.value.campo == "titulo"
    sessao.rollback()
    assert sessao.query(Atividade).one().titulo == "Montagem do robô"


def test_modalidade_fora_dos_valores_previstos_e_recusada_na_correcao(
    sessao, criar_persona, criar_trilha, atividade_gravada
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    atividade = atividade_gravada(mestre, trilha)

    with pytest.raises(ErroDeValidacao) as excinfo:
        corrigir_atividade(
            sessao, operador=mestre, atividade=atividade, campos={"modalidade": "em_trio"}
        )
    assert excinfo.value.campo == "modalidade"
    sessao.rollback()
    assert sessao.query(Atividade).one().modalidade == ModalidadeDeAtividade.individual


def test_mestre_que_nao_e_autor_nao_corrige_a_atividade(
    sessao, criar_persona, criar_trilha, atividade_gravada
):
    mestre_autor = criar_persona(Papel.mestre)
    outro_mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre_autor)
    atividade = atividade_gravada(mestre_autor, trilha)

    with pytest.raises(PermissaoNegada):
        corrigir_atividade(
            sessao, operador=outro_mestre, atividade=atividade, campos={"titulo": "Outro"}
        )
    sessao.rollback()
    assert sessao.query(Atividade).one().titulo == "Montagem do robô"


def test_admin_nao_corrige_atividade_de_trilha(
    sessao, criar_persona, criar_trilha, atividade_gravada
):
    mestre = criar_persona(Papel.mestre)
    admin = criar_persona(Papel.admin)
    trilha = criar_trilha(mestre)
    atividade = atividade_gravada(mestre, trilha)

    with pytest.raises(PermissaoNegada):
        corrigir_atividade(
            sessao, operador=admin, atividade=atividade, campos={"titulo": "Auditado"}
        )
    sessao.rollback()
    assert sessao.query(Atividade).one().titulo == "Montagem do robô"


def test_a_natureza_gravada_sobrevive_a_correcao_dos_demais_campos(
    sessao, criar_persona, criar_trilha, atividade_gravada
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    atividade = atividade_gravada(mestre, trilha, natureza="competicao ao vivo")

    corrigir_atividade(
        sessao,
        operador=mestre,
        atividade=atividade,
        campos={"titulo": "Torneio de perguntas", "formato": FormatoDeAtividade.presencial},
    )
    sessao.commit()

    assert atividade.natureza == "competicao ao vivo"
    assert atividade.titulo == "Torneio de perguntas"


def test_o_formato_sai_do_presencial_e_a_aula_e_limpa(
    sessao, criar_persona, criar_trilha, criar_comunidade, criar_aula, atividade_gravada
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    aula = criar_aula(mestre, criar_comunidade())
    atividade = atividade_gravada(mestre, trilha, aula_id=aula.id)
    assert atividade.aula_id == aula.id

    corrigir_atividade(
        sessao,
        operador=mestre,
        atividade=atividade,
        campos={"formato": FormatoDeAtividade.on_line_assincrona},
    )
    sessao.commit()

    assert atividade.formato == FormatoDeAtividade.on_line_assincrona
    assert atividade.aula_id is None


def test_o_formato_segue_presencial_e_a_aula_permanece(
    sessao, criar_persona, criar_trilha, criar_comunidade, criar_aula, atividade_gravada
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    aula = criar_aula(mestre, criar_comunidade())
    atividade = atividade_gravada(mestre, trilha, aula_id=aula.id)

    corrigir_atividade(
        sessao, operador=mestre, atividade=atividade, campos={"titulo": "Montagem revisada"}
    )
    sessao.commit()

    assert atividade.aula_id == aula.id


def test_correcao_de_atividade_avulsa_e_recusada(
    sessao, criar_persona, criar_comunidade, criar_aula, criar_poder
):
    admin = criar_persona(Papel.admin)
    aula = criar_aula(admin, criar_comunidade())
    avulsa = cadastrar_atividade_avulsa(
        sessao,
        operador=admin,
        titulo="Mutirão de limpeza",
        modalidade=ModalidadeDeAtividade.em_equipe,
        formato=FormatoDeAtividade.presencial,
        natureza="cuidado",
        producao_esperada="Limpar o quintal.",
        poder_id=criar_poder(admin).id,
        aula_id=aula.id,
    )
    sessao.commit()

    with pytest.raises(ErroDeValidacao) as excinfo:
        corrigir_atividade(
            sessao, operador=admin, atividade=avulsa, campos={"titulo": "Outro mutirão"}
        )
    assert excinfo.value.campo == "atividade_id"
    sessao.rollback()
    assert sessao.query(Atividade).one().titulo == "Mutirão de limpeza"


# `RF-09-128`, `RN-09-47`: a remoção carimba, trata o estado vivo e conta os
# fatos — cenários do delta `atividade-de-trilha`.


@pytest.fixture
def resultado_gravado(sessao):
    def _criar(mestre, guerreiro, atividade, aula) -> Resultado:
        resultado = Resultado(
            guerreiro_id=guerreiro.id,
            atividade_id=atividade.id,
            aula_id=aula.id,
            producao="Robô montado.",
            desfecho=DesfechoDoResultado.realizada,
            momento_do_fato=datetime.now(UTC),
            autor_id=mestre.id,
            papel_do_autor=mestre.papel.value,
        )
        sessao.add(resultado)
        sessao.commit()
        return resultado

    return _criar


@pytest.fixture
def partida_gravada(sessao):
    def _criar(mestre, atividade, aula, encerrada: bool = False) -> PartidaDeQuiz:
        partida = PartidaDeQuiz(
            aula_id=aula.id,
            atividade_id=atividade.id,
            situacao=SituacaoDaPartida.encerrada if encerrada else SituacaoDaPartida.aberta,
            autor_id=mestre.id,
            papel_do_autor=mestre.papel.value,
        )
        if encerrada:
            partida.encerrada_por_id = mestre.id
            partida.encerrada_em = datetime.now(UTC)
        sessao.add(partida)
        sessao.commit()
        return partida

    return _criar


def test_a_atividade_removida_sai_da_leitura_e_permanece_guardada(
    sessao,
    criar_persona,
    criar_trilha,
    criar_comunidade,
    criar_aula,
    atividade_gravada,
    resultado_gravado,
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre)
    atividade = atividade_gravada(mestre, trilha)
    aula = criar_aula(mestre, criar_comunidade())
    resultado_gravado(mestre, guerreiro, atividade, aula)

    remover_atividade(sessao, operador=mestre, atividade=atividade)
    sessao.commit()

    assert atividade.removida_em is not None
    assert atividade_vigente(sessao.query(Atividade)).count() == 0
    assert sessao.query(Atividade).count() == 1
    assert sessao.query(Resultado).count() == 1


def test_a_remocao_alcanca_a_trilha_publicada(
    sessao, criar_persona, criar_trilha, atividade_gravada
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    atividade = atividade_gravada(mestre, trilha)

    remover_atividade(sessao, operador=mestre, atividade=atividade)
    sessao.commit()

    assert atividade.removida_em is not None
    assert trilha.situacao == SituacaoDaTrilha.publicada


def test_a_missao_pode_ficar_sem_atividade_alguma(
    sessao, criar_persona, criar_trilha, criar_missao, atividade_gravada
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    missao = criar_missao(trilha, mestre)
    atividade = atividade_gravada(mestre, trilha, missao=missao)

    remover_atividade(sessao, operador=mestre, atividade=atividade)
    sessao.commit()

    vigentes = atividade_vigente(sessao.query(Atividade).filter_by(missao_id=missao.id)).all()
    assert vigentes == []


def test_mestre_que_nao_e_autor_nao_remove_a_atividade(
    sessao, criar_persona, criar_trilha, atividade_gravada
):
    mestre_autor = criar_persona(Papel.mestre)
    outro_mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre_autor)
    atividade = atividade_gravada(mestre_autor, trilha)

    with pytest.raises(PermissaoNegada):
        remover_atividade(sessao, operador=outro_mestre, atividade=atividade)
    sessao.rollback()
    assert sessao.query(Atividade).one().removida_em is None


def test_admin_nao_remove_atividade_de_trilha(
    sessao, criar_persona, criar_trilha, atividade_gravada
):
    mestre = criar_persona(Papel.mestre)
    admin = criar_persona(Papel.admin)
    trilha = criar_trilha(mestre)
    atividade = atividade_gravada(mestre, trilha)

    with pytest.raises(PermissaoNegada):
        remover_atividade(sessao, operador=admin, atividade=atividade)
    sessao.rollback()
    assert sessao.query(Atividade).one().removida_em is None


def test_remocao_de_atividade_avulsa_e_recusada(
    sessao, criar_persona, criar_comunidade, criar_aula, criar_poder
):
    admin = criar_persona(Papel.admin)
    aula = criar_aula(admin, criar_comunidade())
    avulsa = cadastrar_atividade_avulsa(
        sessao,
        operador=admin,
        titulo="Mutirão de limpeza",
        modalidade=ModalidadeDeAtividade.em_equipe,
        formato=FormatoDeAtividade.presencial,
        natureza="cuidado",
        producao_esperada="Limpar o quintal.",
        poder_id=criar_poder(admin).id,
        aula_id=aula.id,
    )
    sessao.commit()

    with pytest.raises(ErroDeValidacao) as excinfo:
        remover_atividade(sessao, operador=admin, atividade=avulsa)
    assert excinfo.value.campo == "atividade_id"
    sessao.rollback()
    assert sessao.query(Atividade).one().removida_em is None


def test_atividade_inexistente_e_404(sessao, criar_persona):
    mestre = criar_persona(Papel.mestre)

    with pytest.raises(NaoEncontrado):
        remover_atividade(sessao, operador=mestre, atividade=None)


def test_partida_de_quiz_aberta_impede_a_remocao(
    sessao,
    criar_persona,
    criar_trilha,
    criar_comunidade,
    criar_aula,
    atividade_gravada,
    partida_gravada,
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    atividade = atividade_gravada(mestre, trilha, natureza="competicao ao vivo")
    aula = criar_aula(mestre, criar_comunidade())
    partida_gravada(mestre, atividade, aula)

    with pytest.raises(ErroDeValidacao) as excinfo:
        remover_atividade(sessao, operador=mestre, atividade=atividade)
    assert excinfo.value.campo == "atividade_id"
    assert "partida" in excinfo.value.mensagem.lower()
    sessao.rollback()
    assert sessao.query(Atividade).one().removida_em is None


def test_partida_encerrada_nao_impede_a_remocao(
    sessao,
    criar_persona,
    criar_trilha,
    criar_comunidade,
    criar_aula,
    atividade_gravada,
    partida_gravada,
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    atividade = atividade_gravada(mestre, trilha, natureza="competicao ao vivo")
    aula = criar_aula(mestre, criar_comunidade())
    partida = partida_gravada(mestre, atividade, aula, encerrada=True)

    remover_atividade(sessao, operador=mestre, atividade=atividade)
    sessao.commit()

    assert atividade.removida_em is not None
    assert sessao.get(PartidaDeQuiz, partida.id).atividade_id == atividade.id


def test_a_escolha_corrente_da_equipe_e_zerada(
    sessao,
    criar_persona,
    criar_trilha,
    criar_comunidade,
    criar_aula,
    criar_equipe,
    atividade_gravada,
):
    mestre = criar_persona(Papel.mestre)
    guerreiro = criar_persona(Papel.guerreiro)
    trilha = criar_trilha(mestre, situacao=SituacaoDaTrilha.publicada)
    aula = criar_aula(mestre, criar_comunidade())
    atividade = atividade_gravada(mestre, trilha, aula_id=aula.id)
    equipe = criar_equipe(guerreiro, aula=aula)
    equipe.atividade_corrente_id = atividade.id
    sessao.commit()

    remover_atividade(sessao, operador=mestre, atividade=atividade)
    sessao.commit()
    sessao.refresh(equipe)

    assert equipe.atividade_corrente_id is None


def test_o_mestre_autor_le_os_fatos_da_atividade(
    sessao,
    criar_persona,
    criar_trilha,
    criar_comunidade,
    criar_aula,
    atividade_gravada,
    resultado_gravado,
    partida_gravada,
):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    atividade = atividade_gravada(mestre, trilha)
    aula = criar_aula(mestre, criar_comunidade())
    for _ in range(2):
        resultado_gravado(mestre, criar_persona(Papel.guerreiro), atividade, aula)
    partida_gravada(mestre, atividade, aula, encerrada=True)

    fatos = fatos_da_atividade(sessao, operador=mestre, atividade=atividade)

    assert fatos.resultados == 2
    assert fatos.partidas_de_quiz == 1
    assert fatos.partidas_abertas == 0
    assert fatos.producoes == 0
    assert fatos.ocorrencias_de_conduta == 0
    assert fatos.equipes_com_ela_corrente == 0


def test_atividade_sem_fato_algum(sessao, criar_persona, criar_trilha, atividade_gravada):
    mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre)
    atividade = atividade_gravada(mestre, trilha)

    fatos = fatos_da_atividade(sessao, operador=mestre, atividade=atividade)

    assert fatos == FatosDaAtividade(0, 0, 0, 0, 0, 0)


def test_mestre_que_nao_e_autor_nao_le_os_fatos(
    sessao, criar_persona, criar_trilha, atividade_gravada
):
    mestre_autor = criar_persona(Papel.mestre)
    outro_mestre = criar_persona(Papel.mestre)
    trilha = criar_trilha(mestre_autor)
    atividade = atividade_gravada(mestre_autor, trilha)

    with pytest.raises(PermissaoNegada):
        fatos_da_atividade(sessao, operador=outro_mestre, atividade=atividade)
