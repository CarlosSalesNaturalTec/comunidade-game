import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from ..aulas.modelo import Aula
from ..autenticacao import ContextoDaSessao
from ..banco import obter_sessao
from ..permissoes import Operacao, exigir_permissao
from ..personas.modelo import Persona
from ..tempo import DataHoraComFuso
from ..trilhas.modelo import Atividade
from .modelo import Resultado
from .regra import ResultadoDaEquipe, ResultadoDeclarado, lancar_resultados_da_atividade

roteador = APIRouter()


class ParticipanteDoLancamentoCorpo(BaseModel):
    model_config = ConfigDict(extra="forbid")

    guerreiro_id: uuid.UUID
    momento_do_fato: DataHoraComFuso
    producao: str = Field(min_length=1)
    desfecho: str


class EquipeDoLancamentoCorpo(BaseModel):
    """O lançamento **da equipe da aula**: um desfecho e uma produção só,
    que valem igualmente a cada integrante presente (`RF-02-112`,
    `RN-02-32`)."""

    model_config = ConfigDict(extra="forbid")

    equipe_id: uuid.UUID
    momento_do_fato: DataHoraComFuso
    producao: str = Field(min_length=1)
    desfecho: str


class LancarResultadosDaAtividadeEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    aula_id: uuid.UUID
    participantes: list[ParticipanteDoLancamentoCorpo] = Field(default_factory=list)
    equipe: EquipeDoLancamentoCorpo | None = None
    """A equipe é alternativa à lista de participantes, nunca companhia
    dela — a recusa das duas e a de nenhuma são da regra (`RN-02-33`)."""


class ResultadoSaida(BaseModel):
    id: uuid.UUID
    guerreiro_id: uuid.UUID
    atividade_id: uuid.UUID
    aula_id: uuid.UUID
    momento_do_fato: DataHoraComFuso
    producao: str
    desfecho: str


class LancamentoDaAtividadeSaida(BaseModel):
    """Os Resultados gravados e quem ficou de fora por não ter presença na
    aula — é por essa lista que a tela diz quem não recebeu (`RF-02-112`,
    `RN-02-32`)."""

    resultados: list[ResultadoSaida]
    fora_por_falta_de_presenca: list[uuid.UUID]


def _saida(resultado: Resultado) -> ResultadoSaida:
    return ResultadoSaida(
        id=resultado.id,
        guerreiro_id=resultado.guerreiro_id,
        atividade_id=resultado.atividade_id,
        aula_id=resultado.aula_id,
        momento_do_fato=resultado.momento_do_fato,
        producao=resultado.producao,
        desfecho=resultado.desfecho.value,
    )


@roteador.post("/atividades/{id_da_atividade}/lancamentos", status_code=201)
def lancar_resultados_da_atividade_rota(
    id_da_atividade: uuid.UUID,
    entrada: LancarResultadosDaAtividadeEntrada,
    contexto: Annotated[
        ContextoDaSessao,
        Depends(
            exigir_permissao(
                Operacao.lancamentos_e_pontuacao_negativa_das_suas_atividades, "escreve"
            )
        ),
    ],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> LancamentoDaAtividadeSaida:
    """Mestre autor da trilha da atividade, ou Admin: lança o Resultado de
    todos os participantes numa operação só, sem consumir reserva nem
    alterar a situação da aula — distinto do lançamento por aula, do Admin
    (`RF-09-43`, `RF-09-44`, `RF-09-49`, `RF-09-74`).

    É também o caminho da **atividade avulsa**, do Admin, por participante
    ou pela equipe da aula (`RF-02-112`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    aula = sessao_bd.get(Aula, entrada.aula_id)
    atividade = sessao_bd.get(Atividade, id_da_atividade)

    resultados_declarados = [
        ResultadoDeclarado(
            guerreiro_id=item.guerreiro_id,
            atividade=atividade,
            momento_do_fato=item.momento_do_fato,
            producao=item.producao,
            desfecho=item.desfecho,
        )
        for item in entrada.participantes
    ]

    equipe = (
        ResultadoDaEquipe(
            equipe_id=entrada.equipe.equipe_id,
            momento_do_fato=entrada.equipe.momento_do_fato,
            producao=entrada.equipe.producao,
            desfecho=entrada.equipe.desfecho,
        )
        if entrada.equipe is not None
        else None
    )

    gravados, fora = lancar_resultados_da_atividade(
        sessao_bd,
        operador=operador,
        aula=aula,
        atividade=atividade,
        resultados=resultados_declarados,
        equipe=equipe,
    )
    sessao_bd.commit()
    return LancamentoDaAtividadeSaida(
        resultados=[_saida(resultado) for resultado in gravados],
        fora_por_falta_de_presenca=fora,
    )
