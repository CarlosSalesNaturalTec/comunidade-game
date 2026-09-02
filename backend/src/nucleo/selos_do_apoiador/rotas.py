import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..autenticacao import ContextoDaSessao, exigir_persona
from ..banco import obter_sessao
from ..erros import PermissaoNegada
from ..personas.modelo import Papel
from .modelo import FamiliaDeSelo, SeloDoApoiador
from .regra import derivar_sustento, listar_selos

roteador = APIRouter()


class SeloDoApoiadorSaida(BaseModel):
    selo_nome: str
    missao_do_apoiador_id: uuid.UUID
    creditado_em: datetime


def _saida_do_selo(selo: SeloDoApoiador) -> SeloDoApoiadorSaida:
    return SeloDoApoiadorSaida(
        selo_nome=selo.selo_nome,
        missao_do_apoiador_id=selo.missao_do_apoiador_id,
        creditado_em=selo.creditado_em,
    )


class SustentoDoApoiadorSaida(BaseModel):
    nivel: int
    nome_do_nivel: str
    frente_que_falta: str
    selos: dict[str, list[SeloDoApoiadorSaida]]


_GRUPOS_DE_SELO_VAZIOS: dict[str, list[SeloDoApoiadorSaida]] = {
    familia.value: [] for familia in FamiliaDeSelo
}


@roteador.get("/eu/apoiador/sustento")
def consultar_meu_sustento_rota(
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> SustentoDoApoiadorSaida:
    """Restrita ao Apoiador em sessão: o próprio nível de sustento, os
    próprios selos agrupados por família e a frente que falta — nunca o de
    outro (`RF-14-67`, `RF-14-68`, `RN-14-09`, `RN-14-38`)."""
    if contexto.papel != Papel.apoiador:
        raise PermissaoNegada(mensagem="Só o Apoiador consulta o próprio sustento.")

    sustento = derivar_sustento(sessao_bd, apoiador_id=contexto.persona_id)
    selos_por_familia = listar_selos(sessao_bd, apoiador_id=contexto.persona_id)

    selos_agrupados = {familia: list(grupo) for familia, grupo in _GRUPOS_DE_SELO_VAZIOS.items()}
    for familia, selos in selos_por_familia.items():
        selos_agrupados[familia.value] = [_saida_do_selo(selo) for selo in selos]

    return SustentoDoApoiadorSaida(
        nivel=sustento.nivel,
        nome_do_nivel=sustento.nome_do_nivel,
        frente_que_falta=sustento.frente_que_falta,
        selos=selos_agrupados,
    )
