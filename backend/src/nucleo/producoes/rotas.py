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
from .fabrica import dependencia_da_producao_da_missao
from .modelo import FormaDeEntregaDaProducao, ProducaoDaMissao
from .porta import PortaDaProducaoDaMissao
from .regra import registrar_producao

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
