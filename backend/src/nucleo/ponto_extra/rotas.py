from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..autenticacao import ContextoDaSessao, exigir_persona
from ..banco import obter_sessao
from ..erros import PermissaoNegada
from ..personas.modelo import Papel
from .modelo import PontoExtra

roteador = APIRouter()


class PontosExtrasSaida(BaseModel):
    acumulado: int
    saldo_disponivel: int


@roteador.get("/eu/pontos-extras")
def meus_pontos_extras(
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> PontosExtrasSaida:
    """As duas contas do próprio Guerreiro(a) em sessão; nenhum outro papel
    lê o saldo de uma criança por aqui, e sem identificador de persona no
    caminho não há como apontá-la para outra (`RF-04-51`, `RF-05-82`,
    `RN-01-41`, design — decisão 1)."""
    if contexto.papel != Papel.guerreiro:
        raise PermissaoNegada(mensagem="Só o Guerreiro(a) lê os próprios pontos extras.")

    conta = sessao_bd.query(PontoExtra).filter_by(guerreiro_id=contexto.persona_id).first()
    if conta is None:
        return PontosExtrasSaida(acumulado=0, saldo_disponivel=0)
    return PontosExtrasSaida(acumulado=conta.acumulado, saldo_disponivel=conta.saldo_disponivel)
