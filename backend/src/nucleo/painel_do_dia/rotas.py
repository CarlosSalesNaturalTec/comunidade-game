from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..autenticacao import ContextoDaSessao
from ..banco import obter_sessao
from ..permissoes import Operacao, exigir_permissao
from ..personas.modelo import Persona
from .regra import PainelDoDiaSaida, montar_painel_do_dia

roteador = APIRouter()


@roteador.get("/painel-do-dia")
def painel_do_dia_rota(
    contexto: Annotated[
        ContextoDaSessao, Depends(exigir_permissao(Operacao.painel_do_dia_na_app_03, "le"))
    ],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> PainelDoDiaSaida:
    """`RF-02-41` a `RF-02-47`, `RF-02-69`: o estado do encontro em
    andamento numa leitura só — a resolução da aula, o recorte do Mestre
    às comunidades dele e a composição de cada bloco já são de
    `montar_painel_do_dia`."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    return montar_painel_do_dia(sessao_bd, operador=operador)
