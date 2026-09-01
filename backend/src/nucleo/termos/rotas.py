import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..autenticacao import ContextoDaSessao, exigir_persona
from ..banco import obter_sessao
from ..consentimentos.modelo import TipoDeConsentimento
from ..permissoes import Operacao, exigir_permissao
from ..personas.modelo import Persona
from .regra import consultar_catalogo_de_termos, registrar_leitura_de_termo

roteador = APIRouter()


class VersaoDeTermoSaida(BaseModel):
    versao: str
    texto: str
    vigente_desde: datetime


class TermoSaida(BaseModel):
    tipo: TipoDeConsentimento
    vigente: VersaoDeTermoSaida
    historico: list[VersaoDeTermoSaida]


@roteador.get("/termos")
def consultar_termos_rota(
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> list[TermoSaida]:
    """Sob `exigir_persona`, de qualquer papel — o texto do termo não é
    dado de criança (`RF-13-32`, design — decisão 6)."""
    catalogo = consultar_catalogo_de_termos(sessao_bd)
    return [
        TermoSaida(
            tipo=item.tipo,
            vigente=VersaoDeTermoSaida(
                versao=item.vigente.versao,
                texto=item.vigente.texto,
                vigente_desde=item.vigente.vigente_desde,
            ),
            historico=[
                VersaoDeTermoSaida(versao=v.versao, texto=v.texto, vigente_desde=v.vigente_desde)
                for v in item.historico
            ],
        )
        for item in catalogo
    ]


class LeituraDeTermoSaida(BaseModel):
    id: uuid.UUID
    versao: str
    lida_em: datetime


@roteador.post("/termos/{versao}/leitura", status_code=201)
def registrar_leitura_de_termo_rota(
    versao: str,
    contexto: Annotated[
        ContextoDaSessao, Depends(exigir_permissao(Operacao.consentimentos, "escreve"))
    ],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> LeituraDeTermoSaida:
    """Restrita ao responsável pela matriz (403 para outro papel,
    `RF-13-32`). Nunca vale como consentimento: nenhuma autorização é lida
    nem gravada aqui."""
    responsavel = sessao_bd.get(Persona, contexto.persona_id)
    leitura = registrar_leitura_de_termo(sessao_bd, responsavel=responsavel, versao=versao)
    sessao_bd.commit()
    return LeituraDeTermoSaida(id=leitura.id, versao=leitura.versao, lida_em=leitura.lida_em)
