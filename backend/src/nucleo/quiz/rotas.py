import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from ..aulas.modelo import Aula
from ..autenticacao import ContextoDaSessao, exigir_persona
from ..banco import obter_sessao
from ..equipes.modelo import Equipe
from ..erros import ErroDeValidacao, NaoEncontrado
from ..paginacao import PaginaDeResultado, ParametrosDeListagem, contrato_de_listagem
from ..personas.modelo import Persona
from ..trilhas.modelo import Atividade, Missao
from .modelo import PartidaDeQuiz, PerguntaDeQuiz
from .regra import (
    EstadoDaPartidaSaida,
    PartidaDaAulaSaida,
    PartidaDeQuizSaida,
    PerguntaAnuladaSaida,
    PerguntaDeQuizSaida,
    PerguntaParaEquipeSaida,
    RespostaDeQuizSaida,
    abrir_partida,
    anular_pergunta,
    cadastrar_pergunta,
    encerrar_partida,
    estado_da_partida,
    liberar_resultado,
    partidas_da_aula,
    pergunta_para_equipe,
    perguntas_do_mestre,
    por_pergunta_no_ar,
    registrar_resposta,
    saida_da_anulacao,
    saida_da_partida,
    saida_da_pergunta,
    saida_da_resposta,
)

roteador = APIRouter()

# Filtros de domínio do banco de perguntas; período e persona já vêm dos
# universais de `contrato_de_listagem` (`RF-09-40`).
_FILTROS_DE_DOMINIO = frozenset({"trilha", "missao"})


def _obter_missao(sessao_bd: Session, id_da_missao: uuid.UUID) -> Missao:
    missao = sessao_bd.get(Missao, id_da_missao)
    if missao is None:
        raise NaoEncontrado(mensagem="Missão não encontrada.")
    return missao


def _obter_partida(sessao_bd: Session, id_da_partida: uuid.UUID) -> PartidaDeQuiz:
    partida = sessao_bd.get(PartidaDeQuiz, id_da_partida)
    if partida is None:
        raise NaoEncontrado(mensagem="Partida de quiz não encontrada.")
    return partida


def _analisar_uuid(bruto: str | None, campo: str) -> uuid.UUID | None:
    if not bruto:
        return None
    try:
        return uuid.UUID(bruto)
    except ValueError as exc:
        raise ErroDeValidacao(
            mensagem=f"Filtro '{campo}' precisa ser um identificador válido.", campo=campo
        ) from exc


class CriarPerguntaEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    enunciado: str | None = None
    alternativas: list[str] | None = None
    alternativa_correta: int | None = None
    missao_id: uuid.UUID | None = None


@roteador.post("/perguntas", status_code=201)
def cadastrar_pergunta_rota(
    entrada: CriarPerguntaEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> PerguntaDeQuizSaida:
    """`RF-09-36` a `RF-09-39`: a permissão, as quatro alternativas, a
    correta e a missão obrigatórias já são de `cadastrar_pergunta` — a rota
    não acrescenta conferência própria (design — decisão 5)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    missao = _obter_missao(sessao_bd, entrada.missao_id) if entrada.missao_id else None
    pergunta = cadastrar_pergunta(
        sessao_bd,
        operador=operador,
        enunciado=entrada.enunciado,
        alternativas=entrada.alternativas,
        alternativa_correta=entrada.alternativa_correta,
        missao=missao,
    )
    sessao_bd.commit()
    return saida_da_pergunta(pergunta)


@roteador.get("/perguntas/minhas")
def listar_minhas_perguntas_rota(
    parametros: Annotated[ParametrosDeListagem, Depends(contrato_de_listagem(_FILTROS_DE_DOMINIO))],
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> PaginaDeResultado[PerguntaDeQuizSaida]:
    """`RF-09-40`: o banco do Mestre em sessão, filtrável por trilha e por
    missão — a permissão e o recorte por autoria já são de
    `perguntas_do_mestre` (design — decisões 4, 5)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    trilha_id = _analisar_uuid(parametros.filtros.get("trilha"), "trilha")
    missao_id = _analisar_uuid(parametros.filtros.get("missao"), "missao")
    return perguntas_do_mestre(
        sessao_bd,
        operador=operador,
        trilha_id=trilha_id,
        missao_id=missao_id,
        cursor=parametros.cursor,
        tamanho=parametros.tamanho,
    )


@roteador.get("/aulas/{id_da_aula}/partidas")
def listar_partidas_da_aula_rota(
    id_da_aula: uuid.UUID,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> list[PartidaDaAulaSaida]:
    """`RF-04-41`, `RF-04-42`: a descoberta da partida pelo Guerreiro(a) em
    sessão, com a equipe dele já derivada — a permissão e a derivação já
    são de `partidas_da_aula` (design — decisão 1)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    aula = sessao_bd.get(Aula, id_da_aula)
    if aula is None:
        raise NaoEncontrado(mensagem="Aula não encontrada.")
    return partidas_da_aula(sessao_bd, operador=operador, aula=aula)


class AbrirPartidaEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    aula_id: uuid.UUID | None = None
    atividade_id: uuid.UUID | None = None
    equipes: list[uuid.UUID] = []


@roteador.post("/partidas-de-quiz", status_code=201)
def abrir_partida_rota(
    entrada: AbrirPartidaEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> PartidaDeQuizSaida:
    """`RF-02-59`: abertura sobre a atividade e as equipes da aula, com a
    posse da trilha e o 403 de quem não conduz já de `abrir_partida`
    (design — decisão 5)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    aula = sessao_bd.get(Aula, entrada.aula_id) if entrada.aula_id else None
    atividade = sessao_bd.get(Atividade, entrada.atividade_id) if entrada.atividade_id else None
    equipes = sessao_bd.query(Equipe).filter(Equipe.id.in_(entrada.equipes)).all()
    partida = abrir_partida(
        sessao_bd, operador=operador, aula=aula, atividade=atividade, equipes=equipes
    )
    sessao_bd.commit()
    return saida_da_partida(sessao_bd, partida)


class PorPerguntaNoArEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    pergunta_id: uuid.UUID | None = None


@roteador.post("/partidas-de-quiz/{id_da_partida}/perguntas", status_code=201)
def por_pergunta_no_ar_rota(
    id_da_partida: uuid.UUID,
    entrada: PorPerguntaNoArEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> EstadoDaPartidaSaida:
    """`RF-02-60`, `RF-09-41`: o _start_ da pergunta corrente, com a
    substituição, a missão da atividade e o 403 de quem não conduz já de
    `por_pergunta_no_ar` (design — decisão 5)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    partida = _obter_partida(sessao_bd, id_da_partida)
    pergunta = sessao_bd.get(PerguntaDeQuiz, entrada.pergunta_id) if entrada.pergunta_id else None
    por_pergunta_no_ar(sessao_bd, operador=operador, partida=partida, pergunta=pergunta)
    sessao_bd.commit()
    return estado_da_partida(sessao_bd, operador=operador, partida=partida)


@roteador.post("/partidas-de-quiz/{id_da_partida}/resultado")
def liberar_resultado_rota(
    id_da_partida: uuid.UUID,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> EstadoDaPartidaSaida:
    """`RF-04-44`, `RF-02-62`: liberação do resultado da pergunta no ar,
    idempotente e sem crédito, já de `liberar_resultado`."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    partida = _obter_partida(sessao_bd, id_da_partida)
    liberar_resultado(sessao_bd, operador=operador, partida=partida)
    sessao_bd.commit()
    return estado_da_partida(sessao_bd, operador=operador, partida=partida)


class AnularPerguntaEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    pergunta_id: uuid.UUID | None = None


@roteador.post("/partidas-de-quiz/{id_da_partida}/anulacoes", status_code=201)
def anular_pergunta_rota(
    id_da_partida: uuid.UUID,
    entrada: AnularPerguntaEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> PerguntaAnuladaSaida:
    """`RF-02-72`: anulação da pergunta contestada, sem crédito para
    ninguém, já de `anular_pergunta`."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    partida = _obter_partida(sessao_bd, id_da_partida)
    if entrada.pergunta_id is None:
        raise ErroDeValidacao(mensagem="Anulação exige a pergunta.", campo="pergunta_id")
    pergunta = sessao_bd.get(PerguntaDeQuiz, entrada.pergunta_id)
    if pergunta is None:
        raise NaoEncontrado(mensagem="Pergunta de quiz não encontrada.")
    anulacao = anular_pergunta(sessao_bd, operador=operador, partida=partida, pergunta=pergunta)
    sessao_bd.commit()
    return saida_da_anulacao(anulacao)


@roteador.post("/partidas-de-quiz/{id_da_partida}/encerramento")
def encerrar_partida_rota(
    id_da_partida: uuid.UUID,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> PartidaDeQuizSaida:
    """`RF-02-73`: encerramento com o crédito automático já de
    `encerrar_partida`."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    partida = _obter_partida(sessao_bd, id_da_partida)
    encerrar_partida(sessao_bd, operador=operador, partida=partida)
    sessao_bd.commit()
    return saida_da_partida(sessao_bd, partida)


@roteador.get("/partidas-de-quiz/{id_da_partida}")
def ler_estado_da_partida_rota(
    id_da_partida: uuid.UUID,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> EstadoDaPartidaSaida:
    """`RF-02-60`: leitura sondada por quem conduz — a restrição a quem
    conduz aquela aula já é de `estado_da_partida` (design — decisão 3)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    partida = _obter_partida(sessao_bd, id_da_partida)
    return estado_da_partida(sessao_bd, operador=operador, partida=partida)


@roteador.get("/partidas-de-quiz/{id_da_partida}/pergunta", response_model_exclude_none=True)
def ler_pergunta_da_partida_rota(
    id_da_partida: uuid.UUID,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> PerguntaParaEquipeSaida:
    """`RF-04-41`, `RF-04-44`: a pergunta no ar para o aparelho da equipe,
    sondada a cada 2 segundos, sem a correta antes da liberação; liberado o
    resultado, a mesma leitura passa a trazê-lo (PRD-04 §9, design —
    decisões 2, 3). `exclude_none` mantém os três campos do resultado fora
    do corpo enquanto não liberados, no padrão que a fatia da condução já
    fixou."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    partida = _obter_partida(sessao_bd, id_da_partida)
    return pergunta_para_equipe(sessao_bd, operador=operador, partida=partida)


class ResponderEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    pergunta_id: uuid.UUID | None = None
    equipe_id: uuid.UUID | None = None
    alternativa_escolhida: int | None = None


@roteador.post("/partidas-de-quiz/{id_da_partida}/respostas", status_code=201)
def registrar_resposta_rota(
    id_da_partida: uuid.UUID,
    entrada: ResponderEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> RespostaDeQuizSaida:
    """`RF-04-43`, `RF-04-41`: a resposta da equipe, idempotente por
    (partida, pergunta, equipe), já de `registrar_resposta`."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    partida = _obter_partida(sessao_bd, id_da_partida)
    pergunta = sessao_bd.get(PerguntaDeQuiz, entrada.pergunta_id) if entrada.pergunta_id else None
    equipe = sessao_bd.get(Equipe, entrada.equipe_id) if entrada.equipe_id else None
    resposta = registrar_resposta(
        sessao_bd,
        operador=operador,
        partida=partida,
        pergunta=pergunta,
        equipe=equipe,
        alternativa_escolhida=entrada.alternativa_escolhida,
    )
    sessao_bd.commit()
    return saida_da_resposta(resposta)
