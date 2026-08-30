import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from ..autenticacao import ContextoDaSessao, exigir_persona
from ..banco import obter_sessao
from ..personas.modelo import Persona
from ..trilhas.modelo import Missao
from .fabrica import dependencia_do_template_de_missao
from .modelo import SituacaoDaSugestaoDeEstrutura, SugestaoDeEstrutura
from .porta import PortaDoTemplateDeMissao
from .regra import pedir_estrutura_da_missao, registrar_desfecho_da_sugestao

roteador = APIRouter()

AVISO_DE_INDISPONIBILIDADE = (
    "A sugestão de estrutura não veio agora. Você pode seguir escrevendo a missão à mão."
)


class AtividadeSugeridaSaida(BaseModel):
    titulo: str
    descricao: str | None
    modalidade: str
    formato: str
    natureza: str
    producao_esperada: str
    desplugada: bool


class EstruturaSugeridaSaida(BaseModel):
    sugestao_id: uuid.UUID
    disponivel: bool
    aviso: str | None
    atividades: list[AtividadeSugeridaSaida]
    objetivo_ods: int | None
    meta_ods: str | None
    cadencia_de_retomada: list[int]
    lacunas: list[str]


class PedirEstruturaEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    topico: str | None = None


@roteador.post("/missoes/{id_da_missao}/estrutura", status_code=201)
def pedir_estrutura_rota(
    id_da_missao: uuid.UUID,
    entrada: PedirEstruturaEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    porta: Annotated[PortaDoTemplateDeMissao, Depends(dependencia_do_template_de_missao)],
) -> EstruturaSugeridaSaida:
    """`RF-09-85`, `RF-09-86`, `RF-09-91`, PRD-09 §9: o Mestre autor envia o
    tópico e recebe a estrutura sugerida e as lacunas — indisponibilidade do
    modelo responde 200 com aviso em linguagem simples, nunca 5xx (design —
    decisão 3)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    missao = sessao_bd.get(Missao, id_da_missao)
    resultado = pedir_estrutura_da_missao(
        sessao_bd, operador=operador, missao=missao, topico=entrada.topico, porta=porta
    )
    sessao_bd.commit()
    return EstruturaSugeridaSaida(
        sugestao_id=resultado.sugestao.id,
        disponivel=resultado.disponivel,
        aviso=None if resultado.disponivel else AVISO_DE_INDISPONIBILIDADE,
        atividades=[
            AtividadeSugeridaSaida(
                titulo=atividade.titulo,
                descricao=atividade.descricao,
                modalidade=atividade.modalidade,
                formato=atividade.formato,
                natureza=atividade.natureza,
                producao_esperada=atividade.producao_esperada,
                desplugada=atividade.desplugada,
            )
            for atividade in resultado.atividades
        ],
        objetivo_ods=resultado.objetivo_ods,
        meta_ods=resultado.meta_ods,
        cadencia_de_retomada=resultado.cadencia_de_retomada,
        lacunas=resultado.lacunas,
    )


class SugestaoDeEstruturaSaida(BaseModel):
    id: uuid.UUID
    missao_id: uuid.UUID
    topico: str
    situacao: SituacaoDaSugestaoDeEstrutura


class RegistrarDesfechoEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    situacao: SituacaoDaSugestaoDeEstrutura


@roteador.post("/sugestoes-de-estrutura/{id_da_sugestao}/desfecho")
def registrar_desfecho_rota(
    id_da_sugestao: uuid.UUID,
    entrada: RegistrarDesfechoEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> SugestaoDeEstruturaSaida:
    """`RF-09-89`, `RN-09-33`: o desfecho que o Mestre autor deu à sugestão
    — aceita, recusada ou alterada. O que ele aceita ou altera é gravado à
    parte, pelas rotas de autoria já existentes (atividade, retomada,
    etiqueta ODS); este registro nunca toca a missão."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    sugestao = sessao_bd.get(SugestaoDeEstrutura, id_da_sugestao)
    sugestao = registrar_desfecho_da_sugestao(
        sessao_bd, operador=operador, sugestao=sugestao, situacao=entrada.situacao
    )
    sessao_bd.commit()
    return SugestaoDeEstruturaSaida(
        id=sugestao.id,
        missao_id=sugestao.missao_id,
        topico=sugestao.topico,
        situacao=sugestao.situacao,
    )
