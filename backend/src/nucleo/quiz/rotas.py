import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from ..autenticacao import ContextoDaSessao, exigir_persona
from ..banco import obter_sessao
from ..erros import ErroDeValidacao, NaoEncontrado
from ..paginacao import PaginaDeResultado, ParametrosDeListagem, contrato_de_listagem
from ..personas.modelo import Persona
from ..trilhas.modelo import Missao
from .regra import PerguntaDeQuizSaida, cadastrar_pergunta, perguntas_do_mestre, saida_da_pergunta

roteador = APIRouter()

# Filtros de domínio do banco de perguntas; período e persona já vêm dos
# universais de `contrato_de_listagem` (`RF-09-40`).
_FILTROS_DE_DOMINIO = frozenset({"trilha", "missao"})


def _obter_missao(sessao_bd: Session, id_da_missao: uuid.UUID) -> Missao:
    missao = sessao_bd.get(Missao, id_da_missao)
    if missao is None:
        raise NaoEncontrado(mensagem="Missão não encontrada.")
    return missao


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
