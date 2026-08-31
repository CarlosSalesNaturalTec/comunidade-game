import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, UploadFile
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..autenticacao import ContextoDaSessao, exigir_persona
from ..banco import obter_sessao
from ..equipes.modelo import Equipe
from ..erros import NaoEncontrado, PermissaoNegada
from ..permissoes import Operacao, exigir_permissao
from ..personas.modelo import Papel, Persona
from ..trilhas.modelo import Missao
from .fabrica import dependencia_da_producao_da_missao
from .modelo import FormaDeEntregaDaProducao, ProducaoDaMissao
from .porta import PortaDaProducaoDaMissao
from .regra import registrar_producao, registrar_producao_individual

roteador = APIRouter()


class ProducaoDaMissaoSaida(BaseModel):
    id: uuid.UUID
    equipe_id: uuid.UUID | None
    guerreiro_id: uuid.UUID | None
    missao_id: uuid.UUID
    atividade_id: uuid.UUID
    forma: FormaDeEntregaDaProducao
    transcricao: str
    devolutiva: str | None
    registrado_em: datetime


def _saida_da_producao(producao: ProducaoDaMissao) -> ProducaoDaMissaoSaida:
    return ProducaoDaMissaoSaida(
        id=producao.id,
        equipe_id=producao.equipe_id,
        guerreiro_id=producao.guerreiro_id,
        missao_id=producao.missao_id,
        atividade_id=producao.atividade_id,
        forma=producao.forma,
        transcricao=producao.transcricao,
        devolutiva=producao.devolutiva,
        registrado_em=producao.registrado_em,
    )


@roteador.post("/equipes/{id_da_equipe}/producao", status_code=201)
def registrar_producao_rota(
    id_da_equipe: uuid.UUID,
    contexto: Annotated[
        ContextoDaSessao, Depends(exigir_permissao(Operacao.producao_da_equipe, "escreve"))
    ],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    porta: Annotated[PortaDaProducaoDaMissao, Depends(dependencia_da_producao_da_missao)],
    forma: Annotated[FormaDeEntregaDaProducao, Form()],
    texto: Annotated[str | None, Form()] = None,
    arquivo: Annotated[UploadFile | None, File()] = None,
) -> ProducaoDaMissaoSaida:
    """`RF-04-45` a `RF-04-47`, PRD-04 §9: a entrega da produção pela
    equipe, em texto, áudio ou foto — a integrância, a atividade corrente,
    a aula encerrada e o desfecho da indisponibilidade já são de
    `registrar_producao`. O byte do arquivo é lido em memória e sai de
    escopo ao fim da chamada, sem tocar `armazenamento`, disco ou log
    (`RF-04-46`, design — decisão 3)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    equipe = sessao_bd.get(Equipe, id_da_equipe)
    if equipe is None:
        raise NaoEncontrado(mensagem="Equipe não encontrada.")

    conteudo = arquivo.file.read() if arquivo is not None else None

    producao = registrar_producao(
        sessao_bd,
        operador=operador,
        equipe=equipe,
        forma=forma,
        texto=texto,
        arquivo=conteudo,
        porta=porta,
    )
    sessao_bd.commit()
    return _saida_da_producao(producao)


@roteador.post("/eu/missoes/{id_da_missao}/producao", status_code=201)
def registrar_producao_individual_rota(
    id_da_missao: uuid.UUID,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    porta: Annotated[PortaDaProducaoDaMissao, Depends(dependencia_da_producao_da_missao)],
    forma: Annotated[FormaDeEntregaDaProducao, Form()],
    atividade_id: Annotated[uuid.UUID, Form()],
    texto: Annotated[str | None, Form()] = None,
    arquivo: Annotated[UploadFile | None, File()] = None,
) -> ProducaoDaMissaoSaida:
    """`RF-05-74` a `RF-05-77`, PRD-05 §9: a entrega individual do
    Guerreiro(a) em sessão, sobre uma missão do próprio percurso — a mesma
    superfície `multipart/form-data` da porta de equipe, com a atividade
    declarada no corpo (design — decisões 2, 6). A posse do percurso, a
    forma única e o desfecho da indisponibilidade já são de
    `registrar_producao_individual`."""
    if contexto.papel != Papel.guerreiro:
        raise PermissaoNegada(mensagem="Só o Guerreiro(a) entrega a produção da missão.")
    operador = sessao_bd.get(Persona, contexto.persona_id)
    missao = sessao_bd.get(Missao, id_da_missao)
    if missao is None:
        raise NaoEncontrado(mensagem="Missão não encontrada.")

    conteudo = arquivo.file.read() if arquivo is not None else None

    producao = registrar_producao_individual(
        sessao_bd,
        operador=operador,
        missao=missao,
        atividade_id=atividade_id,
        forma=forma,
        texto=texto,
        arquivo=conteudo,
        porta=porta,
    )
    sessao_bd.commit()
    return _saida_da_producao(producao)
