import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, UploadFile
from pydantic import BaseModel
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


@roteador.post("/assistente/trilhas/consultas")
def consultar_assistente_de_trilhas_rota(
    contexto: Annotated[
        ContextoDaSessao, Depends(exigir_permissao(Operacao.consulta_ao_assistente, "escreve"))
    ],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    porta: Annotated[PortaDoAssistente, Depends(dependencia_do_assistente)],
    equipe_id: Annotated[uuid.UUID, Form()],
    texto: Annotated[str | None, Form()] = None,
    arquivo: Annotated[UploadFile | None, File()] = None,
) -> ConsultaAoAssistenteSaida:
    """`RF-04-36` a `RF-04-40`, PRD-04 §9: a pergunta da equipe ao
    assistente de trilhas, em texto ou áudio — a integrância, a atividade
    corrente e o desfecho da indisponibilidade já são de
    `consultar_assistente_de_trilhas`. O byte do áudio é lido em memória e
    sai de escopo ao fim da chamada, sem tocar `armazenamento`, disco ou
    log (`RF-04-40`, `RN-04-21`, design — decisão 4)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    equipe = sessao_bd.get(Equipe, equipe_id)
    if equipe is None:
        raise NaoEncontrado(mensagem="Equipe não encontrada.")

    conteudo = arquivo.file.read() if arquivo is not None else None

    consulta = consultar_assistente_de_trilhas(
        sessao_bd,
        operador=operador,
        equipe=equipe,
        texto=texto,
        arquivo=conteudo,
        porta=porta,
    )
    sessao_bd.commit()
    return _saida_da_consulta(consulta)
