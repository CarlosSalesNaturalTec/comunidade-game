import uuid
from datetime import date
from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..aportes.modelo import Aporte
from ..autenticacao import ContextoDaSessao, exigir_persona
from ..banco import obter_sessao
from ..erros import NaoEncontrado, PermissaoNegada
from ..personas.modelo import Papel, Persona
from ..pontos_de_apoio.modelo import PontoDeApoio
from ..recursos.modelo import TipoDeRecurso
from .regra import contagem_de_absorcoes_de, poder_sustentador_de

roteador = APIRouter()

# Provedor é sempre adulto (`RN-07-06`): Guerreiro(a) e responsável recebem o
# mesmo 404 do identificador inexistente, sem confirmar a existência de
# ninguém (`RN-01-32`, `RN-01-33`, design — Decisions 8).
_PAPEIS_QUE_NAO_SAO_PROVEDOR = frozenset({Papel.guerreiro, Papel.responsavel})


class PoderSustentadorDoProvedorSaida(BaseModel):
    provedor_id: uuid.UUID
    poder_sustentador_em_moedas: Decimal
    absorcoes: int


@roteador.get("/provedores/{provedor_id}/poder-sustentador")
def poder_sustentador_do_provedor(
    provedor_id: uuid.UUID,
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> PoderSustentadorDoProvedorSaida:
    """Pública, sem `exigir_persona`: 404 indistinto para identificador
    inexistente e para persona de Guerreiro(a) ou responsável; adulto sem
    aporte responde 200 com zero (`RF-07-10`, `RF-07-26`, `RN-07-05`,
    `RN-07-06`, PRD-07 §9, design — Decisions 8)."""
    provedor = sessao_bd.get(Persona, provedor_id)
    if provedor is None or provedor.papel in _PAPEIS_QUE_NAO_SAO_PROVEDOR:
        raise NaoEncontrado(mensagem="Provedor não encontrado.")

    return PoderSustentadorDoProvedorSaida(
        provedor_id=provedor.id,
        poder_sustentador_em_moedas=poder_sustentador_de(sessao_bd, provedor_id=provedor.id),
        absorcoes=contagem_de_absorcoes_de(sessao_bd, provedor_id=provedor.id),
    )


class AporteDoApoiadorSaida(BaseModel):
    id: uuid.UUID
    tipo_de_recurso_id: uuid.UUID
    tipo_de_recurso_nome: str
    quantidade: Decimal
    ponto_de_apoio_id: uuid.UUID
    ponto_de_apoio_nome: str
    valor_em_moedas: Decimal
    forma: str
    situacao_de_ressarcimento: str
    data_do_aporte: date


class MeusAportesSaida(BaseModel):
    poder_sustentador_em_moedas: Decimal
    aportes: list[AporteDoApoiadorSaida]


@roteador.get("/meus-aportes")
def meus_aportes(
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> MeusAportesSaida:
    """Restrita ao Apoiador em sessão: os aportes dele e o Poder Sustentador
    dele, sem o valor de origem em reais e sem rota de escrita (`RF-07-17`,
    `RN-07-05`, PRD-07 §§9, 11). O nome do tipo de recurso e o destino —
    ponto de apoio — acompanham o identificador, para que "Meus aportes" se
    apresente sem rota de Admin (`RF-14-21`, design — Decisions 6). A
    declaração pendente não aparece aqui: só vira `Aporte` na homologação
    (`RN-14-07`)."""
    if contexto.papel != Papel.apoiador:
        raise PermissaoNegada(mensagem="Só o Apoiador lê os próprios aportes.")

    aportes = (
        sessao_bd.query(Aporte)
        .filter(Aporte.provedor_id == contexto.persona_id)
        .order_by(Aporte.data_do_aporte.desc())
        .all()
    )
    tipos: dict[uuid.UUID, TipoDeRecurso] = {}
    pontos_de_apoio: dict[uuid.UUID, PontoDeApoio] = {}
    saida: list[AporteDoApoiadorSaida] = []
    for aporte in aportes:
        if aporte.tipo_de_recurso_id not in tipos:
            tipos[aporte.tipo_de_recurso_id] = sessao_bd.get(
                TipoDeRecurso, aporte.tipo_de_recurso_id
            )
        if aporte.ponto_de_apoio_id not in pontos_de_apoio:
            pontos_de_apoio[aporte.ponto_de_apoio_id] = sessao_bd.get(
                PontoDeApoio, aporte.ponto_de_apoio_id
            )
        saida.append(
            AporteDoApoiadorSaida(
                id=aporte.id,
                tipo_de_recurso_id=aporte.tipo_de_recurso_id,
                tipo_de_recurso_nome=tipos[aporte.tipo_de_recurso_id].nome,
                quantidade=aporte.quantidade,
                ponto_de_apoio_id=aporte.ponto_de_apoio_id,
                ponto_de_apoio_nome=pontos_de_apoio[aporte.ponto_de_apoio_id].nome,
                valor_em_moedas=aporte.valor_em_moedas,
                forma=aporte.forma.value,
                situacao_de_ressarcimento=aporte.situacao_de_ressarcimento.value,
                data_do_aporte=aporte.data_do_aporte,
            )
        )
    return MeusAportesSaida(
        poder_sustentador_em_moedas=poder_sustentador_de(
            sessao_bd, provedor_id=contexto.persona_id
        ),
        aportes=saida,
    )
