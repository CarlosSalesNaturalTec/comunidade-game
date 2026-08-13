from datetime import UTC, datetime, timedelta
from types import SimpleNamespace

import pytest
from sqlalchemy import text

from nucleo.equipes.modelo import IntegranteDaEquipe
from nucleo.erros import (
    DebitoDePontoRegularRecusado,
    ErroDeValidacao,
    PermissaoNegada,
)
from nucleo.personas.modelo import Papel
from nucleo.pontuacao.modelo import PontoRegular
from nucleo.pontuacao.regra import apurar_partida_de_quiz
from nucleo.quiz.modelo import (
    EquipeNaPartida,
    PerguntaAnuladaNaPartida,
    PerguntaDeQuiz,
    RespostaDeQuiz,
    SituacaoDaPartida,
)
from nucleo.quiz.regra import (
    NATUREZA_DE_COMPETICAO_AO_VIVO,
    abrir_partida,
    anular_pergunta,
    cadastrar_pergunta,
    encerrar_partida,
    registrar_resposta,
)

ALTERNATIVAS = ["Salvador", "Recife", "Cachoeira", "Ilhéus"]
CORRETA = 3
ERRADA = 1

# Momentos fixos para a ordem de chegada não depender da resolução do
# relógio da máquina que roda a suíte — o carimbo do núcleo é exercitado
# à parte, em `test_resposta_grava_equipe_alternativa_e_momento`.
BASE = datetime(2026, 8, 13, 14, 0, tzinfo=UTC)


@pytest.fixture
def cenario(
    criar_persona,
    criar_comunidade,
    criar_aula,
    criar_trilha,
    criar_missao,
    criar_atividade,
    criar_equipe,
    adicionar_integrante,
):
    """Monta aula, trilha com atividade de competição ao vivo e as equipes
    da aula que vão disputar, cada uma com o tamanho pedido."""

    def _montar(
        natureza: str = NATUREZA_DE_COMPETICAO_AO_VIVO,
        tamanhos: tuple[int, ...] = (1, 1),
    ) -> SimpleNamespace:
        admin = criar_persona(Papel.admin)
        mestre = criar_persona(Papel.mestre)
        comunidade = criar_comunidade()
        aula = criar_aula(admin, comunidade)
        trilha = criar_trilha(mestre)
        missao = criar_missao(trilha, mestre)
        atividade = criar_atividade(missao, mestre, natureza=natureza)

        equipes = []
        integrantes: dict = {}
        for tamanho in tamanhos:
            primeiro = criar_persona(Papel.guerreiro, comunidade=comunidade)
            equipe = criar_equipe(primeiro, aula=aula)
            pessoas = [primeiro]
            for _ in range(tamanho - 1):
                outro = criar_persona(Papel.guerreiro, comunidade=comunidade)
                adicionar_integrante(equipe, outro)
                pessoas.append(outro)
            equipes.append(equipe)
            integrantes[equipe.id] = pessoas

        return SimpleNamespace(
            admin=admin,
            mestre=mestre,
            comunidade=comunidade,
            aula=aula,
            trilha=trilha,
            missao=missao,
            atividade=atividade,
            equipes=equipes,
            integrantes=integrantes,
        )

    return _montar


def _cadastrar(sessao, mestre, correta: int = CORRETA) -> PerguntaDeQuiz:
    return cadastrar_pergunta(
        sessao,
        operador=mestre,
        enunciado="Qual é a primeira capital do Brasil?",
        alternativas=list(ALTERNATIVAS),
        alternativa_correta=correta,
    )


def _responder(sessao, cen, *, partida, pergunta, equipe, alternativa, momento=None):
    resposta = registrar_resposta(
        sessao,
        operador=cen.integrantes[equipe.id][0],
        partida=partida,
        pergunta=pergunta,
        equipe=equipe,
        alternativa_escolhida=alternativa,
    )
    if momento is not None:
        resposta.momento_de_chegada = momento
        sessao.flush()
    return resposta


def _saldo(sessao, persona, trilha) -> int:
    conta = (
        sessao.query(PontoRegular).filter_by(guerreiro_id=persona.id, trilha_id=trilha.id).first()
    )
    return 0 if conta is None else conta.total


# ---------------------------------------------------------------- pergunta


def test_pergunta_com_quatro_alternativas_e_correta_grava_com_autoria(sessao, cenario):
    cen = cenario()

    pergunta = _cadastrar(sessao, cen.mestre)
    sessao.commit()

    assert pergunta.alternativa_1 == "Salvador"
    assert pergunta.alternativa_4 == "Ilhéus"
    assert pergunta.alternativa_correta == CORRETA
    assert pergunta.autor_id == cen.mestre.id
    assert pergunta.papel_do_autor == Papel.mestre.value
    assert pergunta.registrado_em is not None


def test_pergunta_com_tres_alternativas_e_recusada(sessao, cenario):
    cen = cenario()

    with pytest.raises(ErroDeValidacao) as excinfo:
        cadastrar_pergunta(
            sessao,
            operador=cen.mestre,
            enunciado="Enunciado.",
            alternativas=ALTERNATIVAS[:3],
            alternativa_correta=1,
        )
    assert excinfo.value.campo == "alternativas"
    assert sessao.query(PerguntaDeQuiz).count() == 0


def test_pergunta_sem_alternativa_correta_e_recusada(sessao, cenario):
    cen = cenario()

    with pytest.raises(ErroDeValidacao) as excinfo:
        cadastrar_pergunta(
            sessao,
            operador=cen.mestre,
            enunciado="Enunciado.",
            alternativas=list(ALTERNATIVAS),
            alternativa_correta=None,
        )
    assert excinfo.value.campo == "alternativa_correta"
    assert sessao.query(PerguntaDeQuiz).count() == 0


def test_pergunta_nao_guarda_tempo_limite():
    """Documento 05 §5: sem tempo por pergunta — o ritmo é de quem conduz, e
    o núcleo não cronometra."""
    nomes = set(PerguntaDeQuiz.__table__.columns.keys())
    assert not {nome for nome in nomes if "tempo" in nome or "limite" in nome}
    assert not {nome for nome in nomes if "duracao" in nome or "segundos" in nome}


def test_guerreiro_nao_cadastra_pergunta(sessao, cenario):
    cen = cenario()
    guerreiro = cen.integrantes[cen.equipes[0].id][0]

    with pytest.raises(PermissaoNegada):
        _cadastrar(sessao, guerreiro)
    assert sessao.query(PerguntaDeQuiz).count() == 0


# ----------------------------------------------------------------- partida


def test_mestre_da_aula_abre_a_partida_com_autoria(sessao, cenario):
    cen = cenario()

    partida = abrir_partida(
        sessao,
        operador=cen.mestre,
        aula=cen.aula,
        atividade=cen.atividade,
        equipes=cen.equipes,
    )
    sessao.commit()

    assert partida.aula_id == cen.aula.id
    assert partida.atividade_id == cen.atividade.id
    assert partida.situacao == SituacaoDaPartida.aberta
    assert partida.autor_id == cen.mestre.id
    assert partida.papel_do_autor == Papel.mestre.value
    assert partida.encerrada_em is None
    assert sessao.query(EquipeNaPartida).filter_by(partida_id=partida.id).count() == 2


def test_mestre_de_outra_aula_recebe_403(sessao, cenario, criar_persona):
    cen = cenario()
    outro_mestre = criar_persona(Papel.mestre)

    with pytest.raises(PermissaoNegada):
        abrir_partida(
            sessao,
            operador=outro_mestre,
            aula=cen.aula,
            atividade=cen.atividade,
            equipes=cen.equipes,
        )
    assert sessao.query(EquipeNaPartida).count() == 0


def test_admin_abre_partida_em_qualquer_aula(sessao, cenario):
    cen = cenario()

    partida = abrir_partida(
        sessao,
        operador=cen.admin,
        aula=cen.aula,
        atividade=cen.atividade,
        equipes=cen.equipes,
    )
    sessao.commit()

    assert partida.autor_id == cen.admin.id
    assert partida.papel_do_autor == Papel.admin.value


def test_partida_sem_atividade_e_recusada(sessao, cenario):
    cen = cenario()

    with pytest.raises(ErroDeValidacao) as excinfo:
        abrir_partida(
            sessao, operador=cen.mestre, aula=cen.aula, atividade=None, equipes=cen.equipes
        )
    assert excinfo.value.campo == "atividade_id"


def test_partida_sobre_atividade_de_outra_natureza_e_recusada(sessao, cenario):
    cen = cenario(natureza="construcao")

    with pytest.raises(ErroDeValidacao) as excinfo:
        abrir_partida(
            sessao,
            operador=cen.mestre,
            aula=cen.aula,
            atividade=cen.atividade,
            equipes=cen.equipes,
        )
    assert excinfo.value.campo == "atividade_id"


def test_duas_partidas_de_trilhas_diferentes_convivem_na_mesma_aula(
    sessao, cenario, criar_trilha, criar_missao, criar_atividade
):
    cen = cenario()
    outra_trilha = criar_trilha(cen.mestre, nome="Trilha do Território")
    outra_missao = criar_missao(outra_trilha, cen.mestre)
    outra_atividade = criar_atividade(
        outra_missao, cen.mestre, natureza=NATUREZA_DE_COMPETICAO_AO_VIVO
    )

    primeira = abrir_partida(
        sessao,
        operador=cen.mestre,
        aula=cen.aula,
        atividade=cen.atividade,
        equipes=[cen.equipes[0]],
    )
    segunda = abrir_partida(
        sessao,
        operador=cen.mestre,
        aula=cen.aula,
        atividade=outra_atividade,
        equipes=[cen.equipes[1]],
    )
    sessao.commit()

    assert primeira.aula_id == segunda.aula_id
    assert primeira.atividade_id != segunda.atividade_id
    # A aula segue sem trilha: cada partida traz a sua pela atividade.
    assert not hasattr(cen.aula, "trilha_id")


def test_equipes_com_integrante_em_comum_recusam_a_partida(sessao, cenario, adicionar_integrante):
    cen = cenario()
    compartilhado = cen.integrantes[cen.equipes[0].id][0]
    adicionar_integrante(cen.equipes[1], compartilhado)

    with pytest.raises(ErroDeValidacao) as excinfo:
        abrir_partida(
            sessao,
            operador=cen.mestre,
            aula=cen.aula,
            atividade=cen.atividade,
            equipes=cen.equipes,
        )
    assert excinfo.value.campo == "equipes"
    sessao.rollback()
    assert sessao.query(EquipeNaPartida).count() == 0


def test_cada_equipe_do_guerreiro_disputa_uma_partida_diferente(
    sessao, cenario, adicionar_integrante
):
    """`RF-01-39`: o Guerreiro(a) integra duas equipes da aula; em nenhuma
    das duas partidas ele aparece duas vezes, e as duas são aceitas."""
    cen = cenario()
    compartilhado = cen.integrantes[cen.equipes[0].id][0]
    adicionar_integrante(cen.equipes[1], compartilhado)

    primeira = abrir_partida(
        sessao,
        operador=cen.mestre,
        aula=cen.aula,
        atividade=cen.atividade,
        equipes=[cen.equipes[0]],
    )
    segunda = abrir_partida(
        sessao,
        operador=cen.mestre,
        aula=cen.aula,
        atividade=cen.atividade,
        equipes=[cen.equipes[1]],
    )
    sessao.commit()

    assert primeira.id != segunda.id
    assert sessao.query(EquipeNaPartida).count() == 2


def test_tres_equipes_sem_integrante_em_comum_abrem_a_partida(sessao, cenario):
    cen = cenario(tamanhos=(2, 3, 1))

    partida = abrir_partida(
        sessao,
        operador=cen.mestre,
        aula=cen.aula,
        atividade=cen.atividade,
        equipes=cen.equipes,
    )
    sessao.commit()

    assert sessao.query(EquipeNaPartida).filter_by(partida_id=partida.id).count() == 3


def test_equipe_da_trilha_nao_disputa(sessao, cenario, criar_persona, criar_equipe):
    cen = cenario()
    guerreiro = criar_persona(Papel.guerreiro, comunidade=cen.comunidade)
    equipe_da_trilha = criar_equipe(guerreiro, trilha=cen.trilha)

    with pytest.raises(ErroDeValidacao) as excinfo:
        abrir_partida(
            sessao,
            operador=cen.mestre,
            aula=cen.aula,
            atividade=cen.atividade,
            equipes=[equipe_da_trilha],
        )
    assert excinfo.value.campo == "equipes"
    sessao.rollback()
    assert sessao.query(EquipeNaPartida).count() == 0


def test_equipe_de_outra_aula_nao_disputa(sessao, cenario, criar_persona, criar_aula, criar_equipe):
    cen = cenario()
    outra_aula = criar_aula(cen.admin, cen.comunidade)
    guerreiro = criar_persona(Papel.guerreiro, comunidade=cen.comunidade)
    equipe_de_fora = criar_equipe(guerreiro, aula=outra_aula)

    with pytest.raises(ErroDeValidacao) as excinfo:
        abrir_partida(
            sessao,
            operador=cen.mestre,
            aula=cen.aula,
            atividade=cen.atividade,
            equipes=[equipe_de_fora],
        )
    assert excinfo.value.campo == "equipes"


# ---------------------------------------------------------------- resposta


@pytest.fixture
def partida_aberta(sessao, cenario):
    def _abrir(tamanhos: tuple[int, ...] = (1, 1)):
        cen = cenario(tamanhos=tamanhos)
        partida = abrir_partida(
            sessao,
            operador=cen.mestre,
            aula=cen.aula,
            atividade=cen.atividade,
            equipes=cen.equipes,
        )
        sessao.commit()
        return cen, partida

    return _abrir


def test_resposta_grava_equipe_alternativa_e_momento(sessao, partida_aberta):
    cen, partida = partida_aberta()
    pergunta = _cadastrar(sessao, cen.mestre)
    equipe = cen.equipes[0]
    antes = datetime.now(UTC)

    resposta = _responder(
        sessao, cen, partida=partida, pergunta=pergunta, equipe=equipe, alternativa=CORRETA
    )
    sessao.commit()

    assert resposta.equipe_id == equipe.id
    assert resposta.alternativa_escolhida == CORRETA
    assert antes <= resposta.momento_de_chegada <= datetime.now(UTC)
    assert resposta.autor_id == cen.integrantes[equipe.id][0].id
    assert resposta.papel_do_autor == Papel.guerreiro.value
    assert resposta.anulada_em is None


def test_momento_declarado_pelo_chamador_e_ignorado(sessao, partida_aberta):
    cen, partida = partida_aberta()
    pergunta = _cadastrar(sessao, cen.mestre)
    equipe = cen.equipes[0]
    declarado = datetime(2020, 1, 1, tzinfo=UTC)

    resposta = registrar_resposta(
        sessao,
        operador=cen.integrantes[equipe.id][0],
        partida=partida,
        pergunta=pergunta,
        equipe=equipe,
        alternativa_escolhida=CORRETA,
        momento_declarado=declarado,
    )
    sessao.commit()

    assert resposta.momento_de_chegada != declarado
    assert resposta.momento_de_chegada > declarado


def test_reenvio_mantem_um_registro_e_o_momento_da_primeira(sessao, partida_aberta):
    cen, partida = partida_aberta()
    pergunta = _cadastrar(sessao, cen.mestre)
    equipe = cen.equipes[0]

    primeira = _responder(
        sessao, cen, partida=partida, pergunta=pergunta, equipe=equipe, alternativa=CORRETA
    )
    momento_da_primeira = primeira.momento_de_chegada
    reenvio = _responder(
        sessao, cen, partida=partida, pergunta=pergunta, equipe=equipe, alternativa=CORRETA
    )
    sessao.commit()

    assert reenvio.id == primeira.id
    assert reenvio.momento_de_chegada == momento_da_primeira
    assert sessao.query(RespostaDeQuiz).count() == 1


def test_segunda_alternativa_da_mesma_equipe_e_recusada(sessao, partida_aberta):
    cen, partida = partida_aberta()
    pergunta = _cadastrar(sessao, cen.mestre)
    equipe = cen.equipes[0]
    _responder(sessao, cen, partida=partida, pergunta=pergunta, equipe=equipe, alternativa=CORRETA)
    sessao.commit()

    with pytest.raises(ErroDeValidacao) as excinfo:
        _responder(
            sessao, cen, partida=partida, pergunta=pergunta, equipe=equipe, alternativa=ERRADA
        )
    assert excinfo.value.campo == "alternativa_escolhida"
    assert sessao.query(RespostaDeQuiz).count() == 1
    assert sessao.query(RespostaDeQuiz).first().alternativa_escolhida == CORRETA


def test_resposta_a_partida_encerrada_e_recusada(sessao, partida_aberta):
    cen, partida = partida_aberta()
    pergunta = _cadastrar(sessao, cen.mestre)
    encerrar_partida(sessao, operador=cen.mestre, partida=partida)
    sessao.commit()

    with pytest.raises(ErroDeValidacao) as excinfo:
        _responder(
            sessao,
            cen,
            partida=partida,
            pergunta=pergunta,
            equipe=cen.equipes[0],
            alternativa=CORRETA,
        )
    assert excinfo.value.campo == "partida_id"
    assert sessao.query(RespostaDeQuiz).count() == 0


def test_equipe_que_nao_disputa_a_partida_e_recusada(
    sessao, partida_aberta, criar_persona, criar_equipe, adicionar_integrante
):
    cen, partida = partida_aberta()
    pergunta = _cadastrar(sessao, cen.mestre)
    de_fora = criar_persona(Papel.guerreiro, comunidade=cen.comunidade)
    equipe_de_fora = criar_equipe(de_fora, aula=cen.aula)

    with pytest.raises(ErroDeValidacao) as excinfo:
        registrar_resposta(
            sessao,
            operador=de_fora,
            partida=partida,
            pergunta=pergunta,
            equipe=equipe_de_fora,
            alternativa_escolhida=CORRETA,
        )
    assert excinfo.value.campo == "equipe_id"
    assert sessao.query(RespostaDeQuiz).count() == 0


def test_mestre_nao_responde_pela_equipe(sessao, partida_aberta):
    """A matriz do PRD-01 §4 dá `resposta_de_quiz_da_equipe` ao Guerreiro(a);
    o Mestre conduz, mas não responde."""
    cen, partida = partida_aberta()
    pergunta = _cadastrar(sessao, cen.mestre)

    with pytest.raises(PermissaoNegada):
        registrar_resposta(
            sessao,
            operador=cen.mestre,
            partida=partida,
            pergunta=pergunta,
            equipe=cen.equipes[0],
            alternativa_escolhida=CORRETA,
        )
    assert sessao.query(RespostaDeQuiz).count() == 0


# ---------------------------------------------------------------- anulação


def test_anulacao_grava_autoria_e_marca_as_respostas(sessao, partida_aberta):
    cen, partida = partida_aberta()
    pergunta = _cadastrar(sessao, cen.mestre)
    _responder(
        sessao, cen, partida=partida, pergunta=pergunta, equipe=cen.equipes[0], alternativa=CORRETA
    )
    sessao.commit()

    anulacao = anular_pergunta(sessao, operador=cen.mestre, partida=partida, pergunta=pergunta)
    sessao.commit()

    assert anulacao.autor_id == cen.mestre.id
    assert anulacao.papel_do_autor == Papel.mestre.value
    assert anulacao.registrado_em is not None
    # A resposta segue consultável, marcada como de pergunta anulada.
    resposta = sessao.query(RespostaDeQuiz).one()
    assert resposta.anulada_em is not None


def test_mestre_que_nao_conduz_nao_anula(sessao, partida_aberta, criar_persona):
    cen, partida = partida_aberta()
    pergunta = _cadastrar(sessao, cen.mestre)
    outro_mestre = criar_persona(Papel.mestre)

    with pytest.raises(PermissaoNegada):
        anular_pergunta(sessao, operador=outro_mestre, partida=partida, pergunta=pergunta)
    assert sessao.query(PerguntaAnuladaNaPartida).count() == 0


def test_pergunta_anulada_nao_credita_a_nenhuma_equipe(sessao, partida_aberta):
    cen, partida = partida_aberta()
    pergunta = _cadastrar(sessao, cen.mestre)
    for equipe in cen.equipes:
        _responder(
            sessao, cen, partida=partida, pergunta=pergunta, equipe=equipe, alternativa=CORRETA
        )
    anular_pergunta(sessao, operador=cen.mestre, partida=partida, pergunta=pergunta)
    encerrar_partida(sessao, operador=cen.mestre, partida=partida)
    sessao.commit()

    assert sessao.query(PontoRegular).count() == 0


def test_resposta_que_chega_depois_da_anulacao_nao_credita(sessao, partida_aberta):
    """A partida segue aberta depois da anulação: a resposta que chega
    então nasce marcada e fica fora da apuração (design — decisão 6)."""
    cen, partida = partida_aberta()
    pergunta = _cadastrar(sessao, cen.mestre)
    anular_pergunta(sessao, operador=cen.mestre, partida=partida, pergunta=pergunta)
    sessao.commit()

    tardia = _responder(
        sessao, cen, partida=partida, pergunta=pergunta, equipe=cen.equipes[0], alternativa=CORRETA
    )
    encerrar_partida(sessao, operador=cen.mestre, partida=partida)
    sessao.commit()

    assert tardia.anulada_em is not None
    assert sessao.query(PontoRegular).count() == 0


def test_anulacao_nunca_debita_ponto_regular(sessao, partida_aberta):
    """A equipe já creditou por outra partida; a anulação nesta não reduz
    saldo nenhum (`RN-01-38`)."""
    cen, primeira = partida_aberta()
    pergunta = _cadastrar(sessao, cen.mestre)
    equipe = cen.equipes[0]
    guerreiro = cen.integrantes[equipe.id][0]

    _responder(sessao, cen, partida=primeira, pergunta=pergunta, equipe=equipe, alternativa=CORRETA)
    encerrar_partida(sessao, operador=cen.mestre, partida=primeira)
    sessao.commit()
    saldo_antes = _saldo(sessao, guerreiro, cen.trilha)
    assert saldo_antes > 0

    segunda = abrir_partida(
        sessao,
        operador=cen.mestre,
        aula=cen.aula,
        atividade=cen.atividade,
        equipes=[equipe],
    )
    _responder(sessao, cen, partida=segunda, pergunta=pergunta, equipe=equipe, alternativa=CORRETA)
    anular_pergunta(sessao, operador=cen.mestre, partida=segunda, pergunta=pergunta)
    encerrar_partida(sessao, operador=cen.mestre, partida=segunda)
    sessao.commit()

    assert _saldo(sessao, guerreiro, cen.trilha) >= saldo_antes


def test_anulacao_depois_do_encerramento_e_recusada(sessao, partida_aberta):
    cen, partida = partida_aberta()
    pergunta = _cadastrar(sessao, cen.mestre)
    _responder(
        sessao, cen, partida=partida, pergunta=pergunta, equipe=cen.equipes[0], alternativa=CORRETA
    )
    encerrar_partida(sessao, operador=cen.mestre, partida=partida)
    sessao.commit()
    saldo_antes = _saldo(sessao, cen.integrantes[cen.equipes[0].id][0], cen.trilha)

    with pytest.raises(ErroDeValidacao) as excinfo:
        anular_pergunta(sessao, operador=cen.mestre, partida=partida, pergunta=pergunta)
    assert excinfo.value.campo == "partida_id"
    sessao.rollback()

    assert sessao.query(PerguntaAnuladaNaPartida).count() == 0
    assert _saldo(sessao, cen.integrantes[cen.equipes[0].id][0], cen.trilha) == saldo_antes


# ------------------------------------------------- apuração e encerramento


def test_acerto_credita_1_por_integrante(sessao, partida_aberta):
    cen, partida = partida_aberta(tamanhos=(1, 4))
    pergunta = _cadastrar(sessao, cen.mestre)
    veloz, lenta = cen.equipes

    _responder(
        sessao,
        cen,
        partida=partida,
        pergunta=pergunta,
        equipe=veloz,
        alternativa=CORRETA,
        momento=BASE,
    )
    _responder(
        sessao,
        cen,
        partida=partida,
        pergunta=pergunta,
        equipe=lenta,
        alternativa=CORRETA,
        momento=BASE + timedelta(seconds=5),
    )
    encerrar_partida(sessao, operador=cen.mestre, partida=partida)
    sessao.commit()

    # A que não chegou primeiro recebe 1 a cada um dos quatro integrantes.
    for integrante in cen.integrantes[lenta.id]:
        assert _saldo(sessao, integrante, cen.trilha) == 1


def test_primeira_a_acertar_recebe_o_bonus(sessao, partida_aberta):
    cen, partida = partida_aberta()
    pergunta = _cadastrar(sessao, cen.mestre)
    veloz, lenta = cen.equipes

    _responder(
        sessao,
        cen,
        partida=partida,
        pergunta=pergunta,
        equipe=veloz,
        alternativa=CORRETA,
        momento=BASE,
    )
    _responder(
        sessao,
        cen,
        partida=partida,
        pergunta=pergunta,
        equipe=lenta,
        alternativa=CORRETA,
        momento=BASE + timedelta(seconds=5),
    )
    encerrar_partida(sessao, operador=cen.mestre, partida=partida)
    sessao.commit()

    assert _saldo(sessao, cen.integrantes[veloz.id][0], cen.trilha) == 2
    assert _saldo(sessao, cen.integrantes[lenta.id][0], cen.trilha) == 1


def test_o_teto_de_10_por_partida_e_respeitado(sessao, partida_aberta):
    """Sete perguntas: a equipe A acerta todas, e só na primeira delas a
    equipe B chega antes — apuração de 13, creditada como 10."""
    cen, partida = partida_aberta()
    equipe_a, equipe_b = cen.equipes
    perguntas = [_cadastrar(sessao, cen.mestre) for _ in range(7)]

    _responder(
        sessao,
        cen,
        partida=partida,
        pergunta=perguntas[0],
        equipe=equipe_b,
        alternativa=CORRETA,
        momento=BASE,
    )
    for indice, pergunta in enumerate(perguntas):
        _responder(
            sessao,
            cen,
            partida=partida,
            pergunta=pergunta,
            equipe=equipe_a,
            alternativa=CORRETA,
            momento=BASE + timedelta(seconds=10 + indice),
        )

    apuracao = apurar_partida_de_quiz(sessao, partida=partida)
    encerrar_partida(sessao, operador=cen.mestre, partida=partida)
    sessao.commit()

    assert apuracao[equipe_a.id] == 10
    assert _saldo(sessao, cen.integrantes[equipe_a.id][0], cen.trilha) == 10


def test_o_valor_da_partida_nao_se_divide_pela_equipe(sessao, partida_aberta):
    cen, partida = partida_aberta(tamanhos=(2, 5))
    pergunta = _cadastrar(sessao, cen.mestre)
    pequena, grande = cen.equipes

    _responder(
        sessao,
        cen,
        partida=partida,
        pergunta=pergunta,
        equipe=pequena,
        alternativa=CORRETA,
        momento=BASE + timedelta(seconds=5),
    )
    _responder(
        sessao,
        cen,
        partida=partida,
        pergunta=pergunta,
        equipe=grande,
        alternativa=CORRETA,
        momento=BASE + timedelta(seconds=9),
    )
    encerrar_partida(sessao, operador=cen.mestre, partida=partida)
    sessao.commit()

    # A pequena chegou antes e leva o bônus; dentro de cada equipe, todos
    # recebem o mesmo, sem rateio pelo tamanho.
    assert {_saldo(sessao, p, cen.trilha) for p in cen.integrantes[pequena.id]} == {2}
    assert {_saldo(sessao, p, cen.trilha) for p in cen.integrantes[grande.id]} == {1}


def test_erro_nao_credita_nem_reduz_saldo(sessao, partida_aberta):
    cen, partida = partida_aberta()
    pergunta = _cadastrar(sessao, cen.mestre)

    _responder(
        sessao, cen, partida=partida, pergunta=pergunta, equipe=cen.equipes[0], alternativa=ERRADA
    )
    encerrar_partida(sessao, operador=cen.mestre, partida=partida)
    sessao.commit()

    assert sessao.query(PontoRegular).count() == 0


def test_partida_credita_a_trilha_da_atividade(
    sessao, partida_aberta, criar_trilha, criar_missao, criar_atividade
):
    cen, partida = partida_aberta()
    outra_trilha = criar_trilha(cen.mestre, nome="Trilha 2")
    criar_atividade(
        criar_missao(outra_trilha, cen.mestre),
        cen.mestre,
        natureza=NATUREZA_DE_COMPETICAO_AO_VIVO,
    )
    pergunta = _cadastrar(sessao, cen.mestre)
    equipe = cen.equipes[0]

    _responder(sessao, cen, partida=partida, pergunta=pergunta, equipe=equipe, alternativa=CORRETA)
    encerrar_partida(sessao, operador=cen.mestre, partida=partida)
    sessao.commit()

    conta = sessao.query(PontoRegular).one()
    assert conta.trilha_id == cen.trilha.id
    assert conta.trilha_id != outra_trilha.id
    # Nada é creditado à aula: o ponto regular é por trilha (`RN-01-42`).
    assert _saldo(sessao, cen.integrantes[equipe.id][0], outra_trilha) == 0


def test_segundo_encerramento_e_recusado_sem_creditar_de_novo(sessao, partida_aberta):
    cen, partida = partida_aberta()
    pergunta = _cadastrar(sessao, cen.mestre)
    equipe = cen.equipes[0]

    _responder(sessao, cen, partida=partida, pergunta=pergunta, equipe=equipe, alternativa=CORRETA)
    encerrar_partida(sessao, operador=cen.mestre, partida=partida)
    sessao.commit()
    saldo_depois_do_primeiro = _saldo(sessao, cen.integrantes[equipe.id][0], cen.trilha)

    with pytest.raises(ErroDeValidacao) as excinfo:
        encerrar_partida(sessao, operador=cen.mestre, partida=partida)
    assert excinfo.value.campo == "situacao"
    sessao.rollback()

    assert _saldo(sessao, cen.integrantes[equipe.id][0], cen.trilha) == saldo_depois_do_primeiro


def test_apuracao_parcial_e_leitura_sem_creditar(sessao, partida_aberta):
    """O placar ao vivo da App 03 sai das respostas, não de `PontoRegular`
    (design — riscos): com a partida aberta, a apuração já existe e nada
    foi creditado."""
    cen, partida = partida_aberta()
    pergunta = _cadastrar(sessao, cen.mestre)
    equipe = cen.equipes[0]

    _responder(sessao, cen, partida=partida, pergunta=pergunta, equipe=equipe, alternativa=CORRETA)
    sessao.commit()

    apuracao = apurar_partida_de_quiz(sessao, partida=partida)

    assert apuracao[equipe.id] == 2
    assert apuracao[cen.equipes[1].id] == 0
    assert partida.situacao == SituacaoDaPartida.aberta
    assert sessao.query(PontoRegular).count() == 0


def test_partida_nunca_encerrada_nunca_credita(sessao, partida_aberta):
    cen, partida = partida_aberta()
    pergunta = _cadastrar(sessao, cen.mestre)
    _responder(
        sessao, cen, partida=partida, pergunta=pergunta, equipe=cen.equipes[0], alternativa=CORRETA
    )
    sessao.commit()

    assert sessao.query(PontoRegular).count() == 0


def test_gatilho_recusa_debito_com_o_quiz_no_caminho(sessao, partida_aberta, engine):
    """`RN-01-38`, `RF-01-57`: o ponto creditado pela partida é ponto regular
    como qualquer outro — o evento do ORM e o gatilho do Postgres recusam
    reduzi-lo."""
    cen, partida = partida_aberta()
    pergunta = _cadastrar(sessao, cen.mestre)
    _responder(
        sessao, cen, partida=partida, pergunta=pergunta, equipe=cen.equipes[0], alternativa=CORRETA
    )
    encerrar_partida(sessao, operador=cen.mestre, partida=partida)
    sessao.commit()

    conta = sessao.query(PontoRegular).one()
    conta.total -= 1
    with pytest.raises(DebitoDePontoRegularRecusado):
        sessao.flush()
    sessao.rollback()

    with pytest.raises(Exception, match="ponto regular nunca é debitado"):
        with engine.begin() as conexao:
            conexao.execute(
                text("UPDATE ponto_regular SET total = 0 WHERE id = :id"), {"id": str(conta.id)}
            )

    with pytest.raises(Exception, match="ponto regular nunca é debitado"):
        with engine.begin() as conexao:
            conexao.execute(text("DELETE FROM ponto_regular WHERE id = :id"), {"id": str(conta.id)})


def test_integrante_que_entra_depois_do_encerramento_nao_recebe(
    sessao, partida_aberta, criar_persona, adicionar_integrante
):
    """A equipe disputante é fixada na abertura, mas o crédito lê a
    composição no encerramento — quem entrou depois dele não recebe."""
    cen, partida = partida_aberta()
    pergunta = _cadastrar(sessao, cen.mestre)
    equipe = cen.equipes[0]

    _responder(sessao, cen, partida=partida, pergunta=pergunta, equipe=equipe, alternativa=CORRETA)
    encerrar_partida(sessao, operador=cen.mestre, partida=partida)
    sessao.commit()

    tardio = criar_persona(Papel.guerreiro, comunidade=cen.comunidade)
    adicionar_integrante(equipe, tardio)

    assert _saldo(sessao, tardio, cen.trilha) == 0
    assert sessao.query(IntegranteDaEquipe).filter_by(equipe_id=equipe.id).count() == 2
