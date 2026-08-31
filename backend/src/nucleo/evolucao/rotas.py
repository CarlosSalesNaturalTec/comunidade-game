import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..autenticacao import ContextoDaSessao
from ..banco import obter_sessao
from ..permissoes import Operacao, exigir_permissao
from ..responsaveis.regra import exigir_vinculo_do_responsavel
from ..resultados.modelo import DesfechoDoResultado
from ..trilhas.rotas import ProgressoDaTrilhaSaida
from .regra import listar_ocorrencias_do_guerreiro, montar_evolucao

roteador = APIRouter()


class ItemDePresencaSaida(BaseModel):
    aula_id: uuid.UUID
    momento_do_fato: datetime


class ItemDeAtividadeRealizadaSaida(BaseModel):
    atividade_id: uuid.UUID
    atividade_titulo: str
    desfecho: DesfechoDoResultado
    momento_do_fato: datetime


class ItemDePontosPorPoderSaida(BaseModel):
    poder_id: uuid.UUID
    poder_nome: str
    total: int


class ItemDeCriacaoValidadaSaida(BaseModel):
    trilha_id: uuid.UUID
    trilha_titulo: str
    validado_em: datetime


class EvolucaoDoGuerreiroSaida(BaseModel):
    presencas: list[ItemDePresencaSaida]
    atividades: list[ItemDeAtividadeRealizadaSaida]
    trilhas: list[ProgressoDaTrilhaSaida]
    pontos_por_poder: list[ItemDePontosPorPoderSaida]
    criacoes_validadas: list[ItemDeCriacaoValidadaSaida]


class OcorrenciaDaEvolucaoSaida(BaseModel):
    id: uuid.UUID
    motivo: str | None
    momento_do_fato: datetime


@roteador.get("/eu/guerreiros/{id}/evolucao")
def obter_evolucao_rota(
    id: uuid.UUID,
    contexto: Annotated[
        ContextoDaSessao,
        Depends(exigir_permissao(Operacao.guerreiros_sob_sua_responsabilidade, "le")),
    ],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> EvolucaoDoGuerreiroSaida:
    """Restrita ao responsável pela matriz, e ao vínculo vigente com o
    Guerreiro(a) pedido — sem vínculo, 403 sem revelar dado algum (`RF-13-07`
    a `RF-13-12`, `RN-13-04`, design — decisão 3). Payload consolidado numa
    só chamada (PRD-13 §9)."""
    exigir_vinculo_do_responsavel(
        sessao_bd, papel=contexto.papel, responsavel_id=contexto.persona_id, guerreiro_id=id
    )
    evolucao = montar_evolucao(sessao_bd, guerreiro_id=id)
    return EvolucaoDoGuerreiroSaida(
        presencas=[
            ItemDePresencaSaida(aula_id=item.aula_id, momento_do_fato=item.momento_do_fato)
            for item in evolucao.presencas
        ],
        atividades=[
            ItemDeAtividadeRealizadaSaida(
                atividade_id=item.atividade_id,
                atividade_titulo=item.atividade_titulo,
                desfecho=item.desfecho,
                momento_do_fato=item.momento_do_fato,
            )
            for item in evolucao.atividades
        ],
        trilhas=[
            ProgressoDaTrilhaSaida(
                trilha_id=item.trilha.id,
                trilha_nome=item.trilha.nome,
                nivel_atual=item.nivel_atual,
                obrigatorias_desbloqueadas=item.obrigatorias_desbloqueadas,
                obrigatorias_totais=item.obrigatorias_totais,
                pontos_regulares=item.pontos_regulares,
                badges=item.badges,
            )
            for item in evolucao.progresso_das_trilhas
        ],
        pontos_por_poder=[
            ItemDePontosPorPoderSaida(
                poder_id=item.poder_id, poder_nome=item.poder_nome, total=item.total
            )
            for item in evolucao.pontos_por_poder
        ],
        criacoes_validadas=[
            ItemDeCriacaoValidadaSaida(
                trilha_id=item.trilha_id,
                trilha_titulo=item.trilha_titulo,
                validado_em=item.validado_em,
            )
            for item in evolucao.criacoes_validadas
        ],
    )


@roteador.get("/eu/guerreiros/{id}/ocorrencias")
def listar_ocorrencias_rota(
    id: uuid.UUID,
    contexto: Annotated[
        ContextoDaSessao,
        Depends(exigir_permissao(Operacao.guerreiros_sob_sua_responsabilidade, "le")),
    ],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> list[OcorrenciaDaEvolucaoSaida]:
    """Mesma guarda de papel e vínculo da evolução; o motivo já vem `None`
    do modelo quando o expurgo do ciclo o apagou, e esta rota só reproduz o
    que lá está (`RF-13-09`, `RN-13-21`, `RN-01-52`)."""
    exigir_vinculo_do_responsavel(
        sessao_bd, papel=contexto.papel, responsavel_id=contexto.persona_id, guerreiro_id=id
    )
    ocorrencias = listar_ocorrencias_do_guerreiro(sessao_bd, guerreiro_id=id)
    return [
        OcorrenciaDaEvolucaoSaida(
            id=ocorrencia.id, motivo=ocorrencia.motivo, momento_do_fato=ocorrencia.momento_do_fato
        )
        for ocorrencia in ocorrencias
    ]
