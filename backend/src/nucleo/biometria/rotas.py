import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from ..autenticacao import ContextoDaSessao
from ..banco import obter_sessao
from ..configuracao import Configuracao, obter_configuracao
from ..erros import NaoEncontrado
from ..permissoes import Operacao, exigir_permissao
from ..personas.modelo import Papel, Persona
from .regra import gravar_ou_recadastrar_template

roteador = APIRouter()


class GravarDescritorEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    descritor: list[float] = Field(min_length=1)


class GravarDescritorSaida(BaseModel):
    guerreiro_id: uuid.UUID
    gravado_em: datetime


@roteador.post("/guerreiros/{id}/descritor", status_code=201)
def gravar_descritor(
    id: uuid.UUID,
    entrada: GravarDescritorEntrada,
    contexto: Annotated[
        ContextoDaSessao,
        Depends(exigir_permissao(Operacao.cadastro_biometrico_do_guerreiro, "escreve")),
    ],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    configuracao: Annotated[Configuracao, Depends(obter_configuracao)],
) -> GravarDescritorSaida:
    """Restrita a Mestre e Admin pela matriz (`RF-01-05`, `RF-01-07`,
    `RF-01-08`, `RF-01-16`). A mesma rota grava e recadastra; nenhuma das
    duas respostas devolve o descritor ou o _template_ (`RN-01-14`).
    """
    guerreiro = sessao_bd.get(Persona, id)
    if guerreiro is None or guerreiro.papel != Papel.guerreiro:
        raise NaoEncontrado(mensagem="Guerreiro(a) não encontrado.", campo="id")

    operado_por = sessao_bd.get(Persona, contexto.persona_id)
    credencial = gravar_ou_recadastrar_template(
        sessao_bd,
        configuracao,
        guerreiro=guerreiro,
        descritor=entrada.descritor,
        operado_por=operado_por,
    )
    sessao_bd.commit()
    return GravarDescritorSaida(guerreiro_id=guerreiro.id, gravado_em=credencial.criada_em)
