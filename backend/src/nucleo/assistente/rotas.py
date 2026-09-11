import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from ..autenticacao import ContextoDaSessao
from ..banco import obter_sessao
from ..equipes.modelo import Equipe
from ..erros import NaoEncontrado
from ..permissoes import Operacao, exigir_permissao
from ..personas.modelo import Persona
from .fabrica import dependencia_do_assistente
from .modelo import ConsultaAoAssistente, DesfechoDaConsulta, TipoDeAssistente
from .porta import PortaDoAssistente
from .regra import consultar_assistente_de_trilhas

roteador = APIRouter()


class ConsultaAoAssistenteSaida(BaseModel):
    id: uuid.UUID
    equipe_id: uuid.UUID | None
    guerreiro_id: uuid.UUID | None
    assistente: TipoDeAssistente
    desfecho: DesfechoDaConsulta
    pergunta: str
    resposta: str
    registrado_em: datetime


def _saida_da_consulta(consulta: ConsultaAoAssistente) -> ConsultaAoAssistenteSaida:
    return ConsultaAoAssistenteSaida(
        id=consulta.id,
        equipe_id=consulta.equipe_id,
        guerreiro_id=consulta.guerreiro_id,
        assistente=consulta.assistente,
        desfecho=consulta.desfecho,
        pergunta=consulta.pergunta,
        resposta=consulta.resposta,
        registrado_em=consulta.registrado_em,
    )


class ConsultaAoAssistenteEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    equipe_id: uuid.UUID
    texto: str


@roteador.post("/assistente/trilhas/consultas")
def consultar_assistente_de_trilhas_rota(
    entrada: ConsultaAoAssistenteEntrada,
    contexto: Annotated[
        ContextoDaSessao, Depends(exigir_permissao(Operacao.consulta_ao_assistente, "escreve"))
    ],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    porta: Annotated[PortaDoAssistente, Depends(dependencia_do_assistente)],
) -> ConsultaAoAssistenteSaida:
    """`RF-04-36` a `RF-04-40`, PRD-04 §9: a pergunta da equipe ao
    assistente de trilhas, sempre em texto — a fala é transcrita no
    aparelho, e o áudio nunca chega aqui (`RF-04-40`, `RN-04-21`,
    documento 03 §1.12). A integrância, a atividade corrente e o desfecho
    da indisponibilidade já são de `consultar_assistente_de_trilhas`."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    equipe = sessao_bd.get(Equipe, entrada.equipe_id)
    if equipe is None:
        raise NaoEncontrado(mensagem="Equipe não encontrada.")

    consulta = consultar_assistente_de_trilhas(
        sessao_bd,
        operador=operador,
        equipe=equipe,
        texto=entrada.texto,
        porta=porta,
    )
    sessao_bd.commit()
    return _saida_da_consulta(consulta)
