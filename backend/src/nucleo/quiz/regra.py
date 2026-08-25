import uuid
from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import func, tuple_
from sqlalchemy.orm import Session

from ..aulas.modelo import Aula
from ..equipes.modelo import Equipe, IntegranteDaEquipe
from ..erros import ErroDeValidacao, PermissaoNegada
from ..paginacao import PaginaDeResultado, codificar_cursor, decodificar_cursor
from ..permissoes import Acesso, Operacao, conferir_permissao
from ..personas.modelo import Papel, Persona
from ..pontuacao.regra import creditar_pontuacao_da_partida_de_quiz
from ..tempo import agora
from ..trilhas.modelo import Atividade, Missao, Trilha
from ..trilhas.regra import conferir_posse_da_trilha
from .modelo import (
    PRIMEIRA_ALTERNATIVA,
    TOTAL_DE_ALTERNATIVAS,
    EquipeNaPartida,
    PartidaDeQuiz,
    PerguntaAnuladaNaPartida,
    PerguntaDeQuiz,
    PerguntaNaPartida,
    RespostaDeQuiz,
    SituacaoDaPartida,
)

# Documento 11 §4, eixo Natureza: "Competição ao vivo (Quiz)", já
# normalizada por `trilhas.regra._normalizar_natureza`. É a natureza que
# liga a partida à atividade da trilha, e daí à trilha do ponto regular
# (`RF-01-21`, `RN-01-42`, documento 05 §5).
NATUREZA_DE_COMPETICAO_AO_VIVO = "competição ao vivo"


def _exigir_operacao(operador: Persona, operacao: Operacao, acesso: Acesso = "escreve") -> None:
    """Confere a matriz do PRD-01 §4 aqui, e não numa rota: esta fatia é
    entidade e regra, e as rotas do quiz são do PRD-02, do PRD-04 e do
    PRD-09. Nega por padrão, como `permissoes.exigir_permissao`
    (`RF-01-16`)."""
    if not conferir_permissao(operador.papel, acesso, operacao):
        raise PermissaoNegada()


def _conferir_conducao(partida: PartidaDeQuiz, operador: Persona) -> None:
    """Conduz a partida quem a abriu, e o Admin em qualquer uma
    (`RF-01-17`, `RF-01-16`, PRD-01 §4)."""
    if operador.papel == Papel.admin:
        return
    if partida.autor_id != operador.id:
        raise PermissaoNegada(mensagem="Só quem conduz a partida escreve nela.")


def _trilha_da_atividade(sessao: Session, atividade: Atividade) -> Trilha:
    """A trilha da partida é derivada de `atividade → missao → trilha`, e
    nunca copiada para a partida (design — decisão 3)."""
    missao = sessao.get(Missao, atividade.missao_id)
    return sessao.get(Trilha, missao.trilha_id)


def cadastrar_pergunta(
    sessao: Session,
    *,
    operador: Persona,
    enunciado: str | None,
    alternativas: list[str] | None,
    alternativa_correta: int | None,
    missao: Missao | None,
) -> PerguntaDeQuiz:
    """Pergunta do banco do Mestre curador, restrita a Mestre e Admin pela
    matriz de permissões — é conteúdo dele, na mesma célula das trilhas e
    conteúdos (`RF-01-36`, `RF-01-03`, `RF-01-16`, PRD-01 §4). Exige
    exatamente quatro alternativas, a correta declarada e a missão a que a
    pergunta se refere; **nenhum tempo-limite**, porque o ritmo é de quem
    conduz (documento 05 §5). A trilha é derivada da missão e gravada junto
    — o cliente declara só a missão (`RF-09-39`, design — decisão 1).
    """
    _exigir_operacao(operador, Operacao.suas_trilhas_e_conteudos)

    if not enunciado or not enunciado.strip():
        raise ErroDeValidacao(mensagem="Pergunta de quiz exige o enunciado.", campo="enunciado")

    if missao is None:
        raise ErroDeValidacao(
            mensagem="Pergunta de quiz exige a missão a que ela se refere.",
            campo="missao_id",
        )

    if alternativas is None or len(alternativas) != TOTAL_DE_ALTERNATIVAS:
        raise ErroDeValidacao(
            mensagem="Pergunta de quiz exige exatamente quatro alternativas.",
            campo="alternativas",
        )
    if any(not alternativa or not alternativa.strip() for alternativa in alternativas):
        raise ErroDeValidacao(
            mensagem="Toda alternativa da pergunta de quiz precisa de texto.",
            campo="alternativas",
        )

    if alternativa_correta is None:
        raise ErroDeValidacao(
            mensagem="Pergunta de quiz exige a alternativa correta declarada.",
            campo="alternativa_correta",
        )
    if not PRIMEIRA_ALTERNATIVA <= alternativa_correta <= TOTAL_DE_ALTERNATIVAS:
        raise ErroDeValidacao(
            mensagem="A alternativa correta precisa ser uma das quatro.",
            campo="alternativa_correta",
        )

    pergunta = PerguntaDeQuiz(
        enunciado=enunciado,
        alternativa_1=alternativas[0],
        alternativa_2=alternativas[1],
        alternativa_3=alternativas[2],
        alternativa_4=alternativas[3],
        alternativa_correta=alternativa_correta,
        missao_id=missao.id,
        trilha_id=missao.trilha_id,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(pergunta)
    sessao.flush()
    return pergunta


class PerguntaDeQuizSaida(BaseModel):
    id: uuid.UUID
    enunciado: str
    alternativas: list[str]
    alternativa_correta: int
    missao_id: uuid.UUID
    trilha_id: uuid.UUID
    registrado_em: datetime


def saida_da_pergunta(pergunta: PerguntaDeQuiz) -> PerguntaDeQuizSaida:
    return PerguntaDeQuizSaida(
        id=pergunta.id,
        enunciado=pergunta.enunciado,
        alternativas=[
            pergunta.alternativa_1,
            pergunta.alternativa_2,
            pergunta.alternativa_3,
            pergunta.alternativa_4,
        ],
        alternativa_correta=pergunta.alternativa_correta,
        missao_id=pergunta.missao_id,
        trilha_id=pergunta.trilha_id,
        registrado_em=pergunta.registrado_em,
    )


def perguntas_do_mestre(
    sessao: Session,
    *,
    operador: Persona,
    trilha_id: uuid.UUID | None,
    missao_id: uuid.UUID | None,
    cursor: str | None,
    tamanho: int,
) -> PaginaDeResultado[PerguntaDeQuizSaida]:
    """Banco do Mestre em sessão, por autoria — o de um Mestre nunca aparece
    para outro —, filtrável por trilha e por missão para montar o banco de
    uma aula (`RF-09-40`, `RF-01-16`). Mesma permissão do cadastro: a
    entidade é conteúdo do Mestre, não outra célula da matriz (design —
    decisão 5). Sem filtro padrão de situação: a pergunta não tem situação
    e o banco devolve tudo o que o Mestre cadastrou (design — decisão 3).
    """
    _exigir_operacao(operador, Operacao.suas_trilhas_e_conteudos)

    consulta = sessao.query(PerguntaDeQuiz).filter(PerguntaDeQuiz.autor_id == operador.id)
    if missao_id is not None:
        consulta = consulta.filter(PerguntaDeQuiz.missao_id == missao_id)
    if trilha_id is not None:
        consulta = consulta.filter(PerguntaDeQuiz.trilha_id == trilha_id)

    if cursor:
        posicao = decodificar_cursor(cursor)
        try:
            registrado_em_cursor = datetime.fromisoformat(posicao["registrado_em"])
            id_cursor = uuid.UUID(posicao["id"])
        except (KeyError, ValueError) as exc:
            raise ErroDeValidacao(mensagem="Cursor de paginação inválido.", campo="cursor") from exc
        consulta = consulta.filter(
            tuple_(PerguntaDeQuiz.registrado_em, PerguntaDeQuiz.id)
            > (registrado_em_cursor, id_cursor)
        )

    consulta = consulta.order_by(PerguntaDeQuiz.registrado_em, PerguntaDeQuiz.id).limit(tamanho + 1)
    perguntas = consulta.all()

    proximo_cursor = None
    if len(perguntas) > tamanho:
        perguntas = perguntas[:tamanho]
        ultima = perguntas[-1]
        proximo_cursor = codificar_cursor(
            {"registrado_em": ultima.registrado_em.isoformat(), "id": str(ultima.id)}
        )

    return PaginaDeResultado(
        itens=[saida_da_pergunta(pergunta) for pergunta in perguntas],
        proximo_cursor=proximo_cursor,
    )


def _materializar_equipes_disputantes(
    sessao: Session, *, partida: PartidaDeQuiz, aula: Aula, equipes: list[Equipe]
) -> None:
    """Fixa a lista de equipes na abertura e verifica ali, uma vez só, que
    nenhum Guerreiro(a) dispute por duas delas — reavaliar a cada resposta
    leria uma composição que já pode ter mudado (`RF-01-39`, design —
    decisão 4). Só equipe da aula, e da aula da partida: a equipe da trilha
    tem outro tempo de vida (`RF-01-37`, `RF-01-18`).
    """
    ja_disputam: set[uuid.UUID] = set()
    for equipe in equipes:
        if equipe.aula_id is None:
            raise ErroDeValidacao(
                mensagem="Só equipe da aula disputa partida de quiz.", campo="equipes"
            )
        if equipe.aula_id != aula.id:
            raise ErroDeValidacao(
                mensagem="A equipe disputante precisa ser da aula da partida.", campo="equipes"
            )

        integrantes = {
            integrante.persona_id
            for integrante in sessao.query(IntegranteDaEquipe).filter_by(equipe_id=equipe.id).all()
        }
        if integrantes & ja_disputam:
            raise ErroDeValidacao(
                mensagem="Na partida de quiz cada Guerreiro(a) joga por uma única equipe.",
                campo="equipes",
            )
        ja_disputam |= integrantes

        sessao.add(EquipeNaPartida(partida_id=partida.id, equipe_id=equipe.id))


def abrir_partida(
    sessao: Session,
    *,
    operador: Persona,
    aula: Aula | None,
    atividade: Atividade | None,
    equipes: list[Equipe],
) -> PartidaDeQuiz:
    """Abertura restrita ao Mestre autor da trilha sobre a qual a partida
    corre e ao Admin, pela mesma conferência de posse que a atividade já
    usa — a aula não guarda quem a ministra, e a condução do Quiz ao Vivo é
    "das suas aulas" justamente porque a partida corre sobre atividade sua
    (`RF-01-17`, `RF-01-16`, `RF-01-03`).

    A partida se vincula a uma atividade de natureza competição ao vivo e
    daí herda missão e trilha; a aula **não** ganha trilha, e por isso duas
    partidas de trilhas diferentes convivem no mesmo encontro (`RF-01-21`,
    documento 05 §§4, 5).
    """
    _exigir_operacao(operador, Operacao.conducao_do_quiz_ao_vivo_das_suas_aulas)

    if aula is None:
        raise ErroDeValidacao(mensagem="Partida de quiz exige uma aula.", campo="aula_id")
    if atividade is None:
        raise ErroDeValidacao(
            mensagem="Partida de quiz exige a atividade sobre a qual ela corre.",
            campo="atividade_id",
        )

    conferir_posse_da_trilha(_trilha_da_atividade(sessao, atividade), operador)

    if atividade.natureza != NATUREZA_DE_COMPETICAO_AO_VIVO:
        raise ErroDeValidacao(
            mensagem="A partida de quiz corre sobre atividade de natureza competição ao vivo.",
            campo="atividade_id",
        )

    partida = PartidaDeQuiz(
        aula_id=aula.id,
        atividade_id=atividade.id,
        situacao=SituacaoDaPartida.aberta,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(partida)
    sessao.flush()

    _materializar_equipes_disputantes(sessao, partida=partida, aula=aula, equipes=equipes)
    sessao.flush()
    return partida


def _pergunta_no_ar(sessao: Session, partida: PartidaDeQuiz) -> PerguntaNaPartida | None:
    """A pergunta no ar é a de maior `ordem` da partida (design —
    decisão 1)."""
    return (
        sessao.query(PerguntaNaPartida)
        .filter_by(partida_id=partida.id)
        .order_by(PerguntaNaPartida.ordem.desc())
        .first()
    )


def por_pergunta_no_ar(
    sessao: Session,
    *,
    operador: Persona,
    partida: PartidaDeQuiz,
    pergunta: PerguntaDeQuiz | None,
) -> PerguntaNaPartida:
    """_Start_ da pergunta corrente, aceito apenas de quem conduz a partida
    (`RF-02-60`, documento 05 §5). Substitui a pergunta no ar sem apagar a
    anterior, que segue registrada com a ordem e o momento em que caiu
    (design — decisão 1). A pergunta precisa ser do banco da **missão da
    atividade** sobre a qual a partida corre (`RF-09-41`); de outra missão,
    ou a partida já encerrada, é recusa 422.
    """
    _exigir_operacao(operador, Operacao.conducao_do_quiz_ao_vivo_das_suas_aulas)
    _conferir_conducao(partida, operador)

    if partida.situacao != SituacaoDaPartida.aberta:
        raise ErroDeValidacao(
            mensagem="Esta partida já encerrou; não recebe mais pergunta no ar.",
            campo="partida_id",
        )

    if pergunta is None:
        raise ErroDeValidacao(
            mensagem="Start de pergunta exige a pergunta do banco.", campo="pergunta_id"
        )

    atividade = sessao.get(Atividade, partida.atividade_id)
    if pergunta.missao_id != atividade.missao_id:
        raise ErroDeValidacao(
            mensagem="A pergunta precisa ser do banco da missão desta atividade.",
            campo="pergunta_id",
        )

    ultima_ordem = (
        sessao.query(func.max(PerguntaNaPartida.ordem)).filter_by(partida_id=partida.id).scalar()
    )
    pergunta_no_ar = PerguntaNaPartida(
        partida_id=partida.id,
        pergunta_id=pergunta.id,
        ordem=(ultima_ordem or 0) + 1,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(pergunta_no_ar)
    sessao.flush()
    return pergunta_no_ar


def liberar_resultado(
    sessao: Session, *, operador: Persona, partida: PartidaDeQuiz
) -> PerguntaNaPartida:
    """Libera o resultado da pergunta no ar, aceito apenas de quem conduz
    (`RF-04-44`, `RF-02-62`). Idempotente — liberar de novo devolve o
    mesmo registro, sem mover o momento —, e **nunca credita**: o crédito
    segue sendo do encerramento (design — decisão 1, Risks).
    """
    _exigir_operacao(operador, Operacao.conducao_do_quiz_ao_vivo_das_suas_aulas)
    _conferir_conducao(partida, operador)

    pergunta_no_ar = _pergunta_no_ar(sessao, partida)
    if pergunta_no_ar is None:
        raise ErroDeValidacao(
            mensagem="Nenhuma pergunta está no ar nesta partida.", campo="partida_id"
        )

    if pergunta_no_ar.liberada_em is None:
        pergunta_no_ar.liberada_em = agora()
        sessao.flush()
    return pergunta_no_ar


def registrar_resposta(
    sessao: Session,
    *,
    operador: Persona,
    partida: PartidaDeQuiz | None,
    pergunta: PerguntaDeQuiz | None,
    equipe: Equipe | None,
    alternativa_escolhida: int | None,
    momento_declarado: datetime | None = None,
) -> RespostaDeQuiz:
    """Resposta da **equipe**, com o momento de chegada carimbado pelo
    núcleo (`RF-01-36`, `RF-01-03`, documento 05 §5). `momento_declarado`
    existe só para ser ignorado: a ordem de chegada é do servidor, e
    cliente não arbitra a própria ordem (design — decisão 2).

    Idempotente por (partida, pergunta, equipe): o reenvio com a rede
    instável devolve o registro já gravado, sem duplicar e sem mover o
    momento; alternativa diferente da já gravada é recusada com 422
    (PRD-01 §10). Não se confere se quem envia integra a equipe — a trava
    contra responder por outra equipe é a equipe única por partida,
    verificada na abertura (`RF-01-39`).
    """
    _exigir_operacao(operador, Operacao.resposta_de_quiz_da_equipe)

    if partida is None:
        raise ErroDeValidacao(mensagem="Resposta de quiz exige a partida.", campo="partida_id")
    if pergunta is None:
        raise ErroDeValidacao(mensagem="Resposta de quiz exige a pergunta.", campo="pergunta_id")
    if equipe is None:
        raise ErroDeValidacao(mensagem="Resposta de quiz exige a equipe.", campo="equipe_id")

    if partida.situacao != SituacaoDaPartida.aberta:
        raise ErroDeValidacao(
            mensagem="Esta partida já encerrou; não recebe mais resposta.", campo="partida_id"
        )

    disputa = (
        sessao.query(EquipeNaPartida).filter_by(partida_id=partida.id, equipe_id=equipe.id).first()
    )
    if disputa is None:
        raise ErroDeValidacao(mensagem="Esta equipe não disputa esta partida.", campo="equipe_id")

    if alternativa_escolhida is None:
        raise ErroDeValidacao(
            mensagem="Resposta de quiz exige a alternativa escolhida.",
            campo="alternativa_escolhida",
        )
    if not PRIMEIRA_ALTERNATIVA <= alternativa_escolhida <= TOTAL_DE_ALTERNATIVAS:
        raise ErroDeValidacao(
            mensagem="A alternativa escolhida precisa ser uma das quatro.",
            campo="alternativa_escolhida",
        )

    existente = (
        sessao.query(RespostaDeQuiz)
        .filter_by(partida_id=partida.id, pergunta_id=pergunta.id, equipe_id=equipe.id)
        .first()
    )
    if existente is not None:
        if existente.alternativa_escolhida != alternativa_escolhida:
            raise ErroDeValidacao(
                mensagem="Esta equipe já respondeu a esta pergunta.",
                campo="alternativa_escolhida",
            )
        return existente

    # A pergunta já anulada segue recebendo resposta enquanto a partida
    # está aberta; a resposta nasce marcada e fica fora da apuração, para
    # que a anulação valha também para quem chegou depois dela (design —
    # decisão 6).
    anulacao = (
        sessao.query(PerguntaAnuladaNaPartida)
        .filter_by(partida_id=partida.id, pergunta_id=pergunta.id)
        .first()
    )

    resposta = RespostaDeQuiz(
        partida_id=partida.id,
        pergunta_id=pergunta.id,
        equipe_id=equipe.id,
        alternativa_escolhida=alternativa_escolhida,
        momento_de_chegada=agora(),
        anulada_em=anulacao.registrado_em if anulacao is not None else None,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(resposta)
    sessao.flush()
    return resposta


def anular_pergunta(
    sessao: Session,
    *,
    operador: Persona,
    partida: PartidaDeQuiz,
    pergunta: PerguntaDeQuiz,
) -> PerguntaAnuladaNaPartida:
    """Anulação havendo contestação, pelo Mestre que conduz a partida ou por
    um Admin, com autoria, data e hora (`RF-01-03`, `RF-01-16`, documento
    05 §5). Exige a partida **ainda aberta**: depois do encerramento a
    apuração já creditou, e estornar é proibido (`RN-01-38`, design —
    decisão 1). As respostas já gravadas ficam marcadas e seguem
    consultáveis; a anulação nunca reduz saldo de ninguém. Repetir a
    anulação devolve o registro existente, sem duplicar.
    """
    _exigir_operacao(operador, Operacao.conducao_do_quiz_ao_vivo_das_suas_aulas)
    _conferir_conducao(partida, operador)

    if partida.situacao != SituacaoDaPartida.aberta:
        raise ErroDeValidacao(
            mensagem="Esta partida já encerrou; a pergunta não é mais anulável.",
            campo="partida_id",
        )

    existente = (
        sessao.query(PerguntaAnuladaNaPartida)
        .filter_by(partida_id=partida.id, pergunta_id=pergunta.id)
        .first()
    )
    if existente is not None:
        return existente

    anulacao = PerguntaAnuladaNaPartida(
        partida_id=partida.id,
        pergunta_id=pergunta.id,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(anulacao)
    sessao.flush()

    respostas = (
        sessao.query(RespostaDeQuiz).filter_by(partida_id=partida.id, pergunta_id=pergunta.id).all()
    )
    for resposta in respostas:
        resposta.anulada_em = anulacao.registrado_em
    sessao.flush()
    return anulacao


def encerrar_partida(
    sessao: Session, *, operador: Persona, partida: PartidaDeQuiz
) -> PartidaDeQuiz:
    """Aceito apenas na transição `aberta → encerrada`; a segunda chamada
    recebe 422 sem tocar em `PontoRegular`, e é o que impede crédito duplo
    (design — decisão 7). O crédito acontece na mesma transação da
    transição, de modo que não há janela em que a partida esteja encerrada
    e o crédito ainda não tenha ocorrido (`RF-01-21`, `RN-01-38`).
    """
    _exigir_operacao(operador, Operacao.conducao_do_quiz_ao_vivo_das_suas_aulas)
    _conferir_conducao(partida, operador)

    if partida.situacao != SituacaoDaPartida.aberta:
        raise ErroDeValidacao(mensagem="Esta partida já foi encerrada.", campo="situacao")

    partida.situacao = SituacaoDaPartida.encerrada
    partida.encerrada_por_id = operador.id
    partida.encerrada_em = agora()
    sessao.flush()

    atividade = sessao.get(Atividade, partida.atividade_id)
    creditar_pontuacao_da_partida_de_quiz(
        sessao, partida=partida, trilha=_trilha_da_atividade(sessao, atividade)
    )
    return partida


class PartidaDeQuizSaida(BaseModel):
    id: uuid.UUID
    aula_id: uuid.UUID
    atividade_id: uuid.UUID
    situacao: SituacaoDaPartida
    equipes_disputantes: list[uuid.UUID]
    encerrada_em: datetime | None
    registrado_em: datetime


def saida_da_partida(sessao: Session, partida: PartidaDeQuiz) -> PartidaDeQuizSaida:
    equipes_disputantes = [
        linha.equipe_id
        for linha in sessao.query(EquipeNaPartida).filter_by(partida_id=partida.id).all()
    ]
    return PartidaDeQuizSaida(
        id=partida.id,
        aula_id=partida.aula_id,
        atividade_id=partida.atividade_id,
        situacao=partida.situacao,
        equipes_disputantes=equipes_disputantes,
        encerrada_em=partida.encerrada_em,
        registrado_em=partida.registrado_em,
    )


class PerguntaAnuladaSaida(BaseModel):
    id: uuid.UUID
    pergunta_id: uuid.UUID
    registrado_em: datetime


def saida_da_anulacao(anulacao: PerguntaAnuladaNaPartida) -> PerguntaAnuladaSaida:
    return PerguntaAnuladaSaida(
        id=anulacao.id, pergunta_id=anulacao.pergunta_id, registrado_em=anulacao.registrado_em
    )


class RespostaDeQuizSaida(BaseModel):
    id: uuid.UUID
    equipe_id: uuid.UUID
    pergunta_id: uuid.UUID
    alternativa_escolhida: int
    momento_de_chegada: datetime


def saida_da_resposta(resposta: RespostaDeQuiz) -> RespostaDeQuizSaida:
    return RespostaDeQuizSaida(
        id=resposta.id,
        equipe_id=resposta.equipe_id,
        pergunta_id=resposta.pergunta_id,
        alternativa_escolhida=resposta.alternativa_escolhida,
        momento_de_chegada=resposta.momento_de_chegada,
    )


def _apurar_pergunta_no_ar(
    sessao: Session,
    *,
    partida: PartidaDeQuiz,
    pergunta_no_ar: PerguntaNaPartida,
    pergunta: PerguntaDeQuiz,
) -> tuple[list[uuid.UUID], uuid.UUID | None]:
    """Equipes que acertaram a pergunta no ar, por ordem de chegada no
    servidor, e a primeira delas (`RF-02-62`, `RF-04-44`)."""
    respostas = (
        sessao.query(RespostaDeQuiz)
        .filter_by(partida_id=partida.id, pergunta_id=pergunta_no_ar.pergunta_id)
        .order_by(RespostaDeQuiz.momento_de_chegada, RespostaDeQuiz.id)
        .all()
    )
    acertaram = [
        resposta.equipe_id
        for resposta in respostas
        if resposta.alternativa_escolhida == pergunta.alternativa_correta
    ]
    primeira = acertaram[0] if acertaram else None
    return acertaram, primeira


class PerguntaNoArSaida(BaseModel):
    id: uuid.UUID
    pergunta_id: uuid.UUID
    enunciado: str
    alternativas: list[str]
    ordem: int
    entrou_em: datetime
    resultado_liberado: bool
    alternativa_correta: int | None = None
    equipes_que_acertaram: list[uuid.UUID] | None = None
    primeira_equipe_a_acertar: uuid.UUID | None = None


class EstadoDaPartidaSaida(BaseModel):
    id: uuid.UUID
    aula_id: uuid.UUID
    atividade_id: uuid.UUID
    situacao: SituacaoDaPartida
    equipes_disputantes: list[uuid.UUID]
    pergunta_no_ar: PerguntaNoArSaida | None
    equipes_que_responderam: list[uuid.UUID]


def estado_da_partida(
    sessao: Session, *, operador: Persona, partida: PartidaDeQuiz
) -> EstadoDaPartidaSaida:
    """Leitura sondada a cada 2 segundos por quem conduz — situação,
    pergunta no ar, liberação, equipes disputantes e contagem de respostas
    —, restrita a quem conduz a partida, como a escrita (`RF-02-60`,
    `RF-02-62`, PRD-02 §12, design — decisão 3). Nunca devolve a
    alternativa correta nem quem acertou antes da liberação.
    """
    _exigir_operacao(operador, Operacao.conducao_do_quiz_ao_vivo_das_suas_aulas, "le")
    _conferir_conducao(partida, operador)

    equipes_disputantes = [
        linha.equipe_id
        for linha in sessao.query(EquipeNaPartida).filter_by(partida_id=partida.id).all()
    ]

    pergunta_atual = _pergunta_no_ar(sessao, partida)
    pergunta_saida: PerguntaNoArSaida | None = None
    equipes_que_responderam: list[uuid.UUID] = []

    if pergunta_atual is not None:
        pergunta = sessao.get(PerguntaDeQuiz, pergunta_atual.pergunta_id)
        equipes_que_responderam = [
            linha.equipe_id
            for linha in sessao.query(RespostaDeQuiz)
            .filter_by(partida_id=partida.id, pergunta_id=pergunta_atual.pergunta_id)
            .all()
        ]

        liberado = pergunta_atual.liberada_em is not None
        acertaram: list[uuid.UUID] | None = None
        primeira: uuid.UUID | None = None
        if liberado:
            acertaram, primeira = _apurar_pergunta_no_ar(
                sessao, partida=partida, pergunta_no_ar=pergunta_atual, pergunta=pergunta
            )

        pergunta_saida = PerguntaNoArSaida(
            id=pergunta_atual.id,
            pergunta_id=pergunta.id,
            enunciado=pergunta.enunciado,
            alternativas=[
                pergunta.alternativa_1,
                pergunta.alternativa_2,
                pergunta.alternativa_3,
                pergunta.alternativa_4,
            ],
            ordem=pergunta_atual.ordem,
            entrou_em=pergunta_atual.registrado_em,
            resultado_liberado=liberado,
            alternativa_correta=pergunta.alternativa_correta if liberado else None,
            equipes_que_acertaram=acertaram,
            primeira_equipe_a_acertar=primeira,
        )

    return EstadoDaPartidaSaida(
        id=partida.id,
        aula_id=partida.aula_id,
        atividade_id=partida.atividade_id,
        situacao=partida.situacao,
        equipes_disputantes=equipes_disputantes,
        pergunta_no_ar=pergunta_saida,
        equipes_que_responderam=equipes_que_responderam,
    )


class PerguntaParaEquipeSaida(BaseModel):
    id: uuid.UUID | None
    enunciado: str | None
    alternativas: list[str] | None


def pergunta_para_equipe(
    sessao: Session, *, operador: Persona, partida: PartidaDeQuiz
) -> PerguntaParaEquipeSaida:
    """A pergunta no ar para o aparelho da equipe — sem situação, sem
    liberação e sem a correta: essa informação é só de quem conduz
    (`RF-04-41`, design — decisão 3). Sem pergunta no ar ainda, devolve
    tudo nulo, sem erro — é o que faz o aparelho que caiu voltar na
    pergunta corrente assim que ela existir (`RF-04-41`).
    """
    _exigir_operacao(operador, Operacao.resposta_de_quiz_da_equipe, "le")

    pergunta_atual = _pergunta_no_ar(sessao, partida)
    if pergunta_atual is None:
        return PerguntaParaEquipeSaida(id=None, enunciado=None, alternativas=None)

    pergunta = sessao.get(PerguntaDeQuiz, pergunta_atual.pergunta_id)
    return PerguntaParaEquipeSaida(
        id=pergunta.id,
        enunciado=pergunta.enunciado,
        alternativas=[
            pergunta.alternativa_1,
            pergunta.alternativa_2,
            pergunta.alternativa_3,
            pergunta.alternativa_4,
        ],
    )
