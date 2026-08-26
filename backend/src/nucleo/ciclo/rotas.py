from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..autenticacao import ContextoDaSessao
from ..banco import obter_sessao
from ..permissoes import Operacao, exigir_permissao
from .regra import encerrar_ciclo

roteador = APIRouter()


class EncerramentoDeCicloSaida(BaseModel):
    ocorrencias_expurgadas: int


@roteador.post("/ciclo/encerramento", status_code=201)
def encerrar_ciclo_rota(
    contexto: Annotated[
        ContextoDaSessao, Depends(exigir_permissao(Operacao.encerramento_de_ciclo, "escreve"))
    ],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> EncerramentoDeCicloSaida:
    """Restrita a Admin — nenhuma outra persona tem `encerramento_de_ciclo`
    na matriz, e o Admin passa só pelo curinga `Operacao.tudo` (`RF-02-99`,
    permissoes.py). A auditoria vem de graça, do `MiddlewareDeAuditoria`
    para toda escrita bem-sucedida sob `/v1` (design — decisão 5)."""
    quantidade = encerrar_ciclo(sessao_bd)
    return EncerramentoDeCicloSaida(ocorrencias_expurgadas=quantidade)
