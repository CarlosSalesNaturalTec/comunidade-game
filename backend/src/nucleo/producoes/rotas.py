import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, Response, UploadFile
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..armazenamento.fabrica import dependencia_de_armazenamento
from ..armazenamento.porta import PortaDeArmazenamento
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
from .regra import (
    ler_arquivo_da_producao,
    registrar_producao,
    registrar_producao_individual,
)

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
    armazenamento: Annotated[PortaDeArmazenamento, Depends(dependencia_de_armazenamento)],
    forma: Annotated[FormaDeEntregaDaProducao, Form()],
    texto: Annotated[str | None, Form()] = None,
    arquivo: Annotated[UploadFile | None, File()] = None,
) -> ProducaoDaMissaoSaida:
    """`RF-04-45` a `RF-04-47`, PRD-04 §9: a entrega da produção pela
    equipe — a integrância, a atividade corrente, a aula encerrada e o
    desfecho da indisponibilidade já são de `registrar_producao`. `arquivo`
    vem na **foto** e, desde 2026-11-03, também no **áudio**, ao lado da
    transcrição em `texto` (`RF-01-79`, `RN-01-61`). Os bytes passam a ser
    **guardados** — antes a foto era lida e descartada —, e a leitura de
    volta é de `GET /v1/producoes/{id}/arquivo`."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    equipe = sessao_bd.get(Equipe, id_da_equipe)
    if equipe is None:
        raise NaoEncontrado(mensagem="Equipe não encontrada.")

    conteudo = arquivo.file.read() if arquivo is not None else None
    tipo_mime = arquivo.content_type if arquivo is not None else None

    producao = registrar_producao(
        sessao_bd,
        operador=operador,
        equipe=equipe,
        forma=forma,
        texto=texto,
        arquivo=conteudo,
        tipo_mime=tipo_mime,
        porta=porta,
        armazenamento=armazenamento,
    )
    sessao_bd.commit()
    return _saida_da_producao(producao)


@roteador.post("/eu/missoes/{id_da_missao}/producao", status_code=201)
def registrar_producao_individual_rota(
    id_da_missao: uuid.UUID,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    porta: Annotated[PortaDaProducaoDaMissao, Depends(dependencia_da_producao_da_missao)],
    armazenamento: Annotated[PortaDeArmazenamento, Depends(dependencia_de_armazenamento)],
    forma: Annotated[FormaDeEntregaDaProducao, Form()],
    atividade_id: Annotated[uuid.UUID, Form()],
    texto: Annotated[str | None, Form()] = None,
    arquivo: Annotated[UploadFile | None, File()] = None,
) -> ProducaoDaMissaoSaida:
    """`RF-05-74` a `RF-05-77`, PRD-05 §9: a entrega individual do
    Guerreiro(a) em sessão, sobre uma missão do próprio percurso — a mesma
    superfície `multipart/form-data` da porta de equipe, que a foto mantém,
    com a atividade declarada no corpo (design — decisão 1). A posse do
    percurso, a forma única — `arquivo` na foto e no áudio, a transcrição em
    `texto` — e o desfecho da indisponibilidade já são de
    `registrar_producao_individual`."""
    if contexto.papel != Papel.guerreiro:
        raise PermissaoNegada(mensagem="Só o Guerreiro(a) entrega a produção da missão.")
    operador = sessao_bd.get(Persona, contexto.persona_id)
    missao = sessao_bd.get(Missao, id_da_missao)
    if missao is None:
        raise NaoEncontrado(mensagem="Missão não encontrada.")

    conteudo = arquivo.file.read() if arquivo is not None else None
    tipo_mime = arquivo.content_type if arquivo is not None else None

    producao = registrar_producao_individual(
        sessao_bd,
        operador=operador,
        missao=missao,
        atividade_id=atividade_id,
        forma=forma,
        texto=texto,
        arquivo=conteudo,
        tipo_mime=tipo_mime,
        porta=porta,
        armazenamento=armazenamento,
    )
    sessao_bd.commit()
    return _saida_da_producao(producao)


@roteador.get("/producoes/{id_da_producao}/arquivo")
def ler_arquivo_da_producao_rota(
    id_da_producao: uuid.UUID,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    armazenamento: Annotated[PortaDeArmazenamento, Depends(dependencia_de_armazenamento)],
) -> Response:
    """`RF-01-80`, `RN-01-62`: os bytes da mídia guardada, a quem já pode ver
    a produção. **Não há rota pública equivalente**, e não é esquecimento: a
    produção da missão não é item de acervo, porque não passa por aprovação
    de ninguém — só a comprovação do desafio e a criação da culminância vão à
    vitrine."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    producao = sessao_bd.get(ProducaoDaMissao, id_da_producao)
    arquivo = ler_arquivo_da_producao(
        sessao_bd, producao, operador=operador, armazenamento=armazenamento
    )
    return Response(content=arquivo.bytes_do_arquivo, media_type=arquivo.tipo_mime)
