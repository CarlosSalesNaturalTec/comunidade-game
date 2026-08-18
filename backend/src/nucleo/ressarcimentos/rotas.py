import uuid
from datetime import date
from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, UploadFile
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..aportes.modelo import Aporte
from ..armazenamento.fabrica import dependencia_de_armazenamento
from ..armazenamento.porta import PortaDeArmazenamento
from ..autenticacao import ContextoDaSessao, exigir_persona
from ..banco import obter_sessao
from ..personas.modelo import Persona
from .regra import (
    listar_absorcoes_do_provedor,
    listar_ressarciveis,
    registrar_ressarcimento,
    total_de_receita_destinada_em_aberto,
)

roteador = APIRouter()


class AporteRessarcivelSaida(BaseModel):
    id: uuid.UUID
    provedor_id: uuid.UUID
    tipo_de_recurso_id: uuid.UUID
    quantidade: Decimal
    ponto_de_apoio_id: uuid.UUID
    valor_em_moedas: Decimal
    valor_em_reais: Decimal | None
    data_do_aporte: date


class FilaDeRessarciveisSaida(BaseModel):
    receita_destinada_em_aberto_em_reais: Decimal
    aportes: list[AporteRessarcivelSaida]


def _saida_ressarcivel(aporte: Aporte) -> AporteRessarcivelSaida:
    return AporteRessarcivelSaida(
        id=aporte.id,
        provedor_id=aporte.provedor_id,
        tipo_de_recurso_id=aporte.tipo_de_recurso_id,
        quantidade=aporte.quantidade,
        ponto_de_apoio_id=aporte.ponto_de_apoio_id,
        valor_em_moedas=aporte.valor_em_moedas,
        valor_em_reais=aporte.valor_de_origem,
        data_do_aporte=aporte.data_do_aporte,
    )


@roteador.get("/aportes/ressarciveis")
def listar_ressarciveis_rota(
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> FilaDeRessarciveisSaida:
    """Restrita ao Admin: os aportes ressarcíveis em aberto, do mais antigo
    ao mais novo, com o que a receita destinada ainda cobre (`RF-07-24`,
    `RN-07-17`, PRD-07 §9)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    aportes = listar_ressarciveis(sessao_bd, operador=operador)
    return FilaDeRessarciveisSaida(
        receita_destinada_em_aberto_em_reais=total_de_receita_destinada_em_aberto(sessao_bd),
        aportes=[_saida_ressarcivel(aporte) for aporte in aportes],
    )


class RessarcimentoSaida(BaseModel):
    id: uuid.UUID
    aporte_id: uuid.UUID
    receita_destinada_id: uuid.UUID
    valor_em_reais: Decimal
    admin_pagador_id: uuid.UUID
    data: date


@roteador.post("/aportes/{aporte_id}/ressarcimento", status_code=201)
def registrar_ressarcimento_rota(
    aporte_id: uuid.UUID,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    armazenamento: Annotated[PortaDeArmazenamento, Depends(dependencia_de_armazenamento)],
    receita_destinada_id: Annotated[uuid.UUID, Form()],
    data: Annotated[date, Form()],
    comprovante: Annotated[UploadFile, File()],
) -> RessarcimentoSaida:
    """Restrita ao Admin: reverte, no mesmo ato, as moedas do aporte
    absorvido, contra o que a receita destinada declarada ainda cobre
    (`RF-07-22`, `RF-07-25`, `RN-07-17`, PRD-07 §9)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    aporte = sessao_bd.get(Aporte, aporte_id)
    receita_destinada = sessao_bd.get(Aporte, receita_destinada_id)
    conteudo = comprovante.file.read()

    ressarcimento = registrar_ressarcimento(
        sessao_bd,
        operador=operador,
        aporte=aporte,
        receita_destinada=receita_destinada,
        data=data,
        comprovante_conteudo=conteudo,
        comprovante_nome_original=comprovante.filename,
        comprovante_tipo=comprovante.content_type,
        armazenamento=armazenamento,
    )
    sessao_bd.commit()
    return RessarcimentoSaida(
        id=ressarcimento.id,
        aporte_id=ressarcimento.aporte_id,
        receita_destinada_id=ressarcimento.receita_destinada_id,
        valor_em_reais=ressarcimento.valor_em_reais,
        admin_pagador_id=ressarcimento.admin_pagador_id,
        data=ressarcimento.data,
    )


class AbsorcaoDoProvedorSaida(BaseModel):
    id: uuid.UUID
    tipo_de_recurso_id: uuid.UUID
    quantidade: Decimal
    ponto_de_apoio_id: uuid.UUID
    valor_em_moedas: Decimal
    situacao_de_ressarcimento: str
    data_do_aporte: date


@roteador.get("/meus-aportes/ressarciveis")
def listar_minhas_absorcoes_rota(
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> list[AbsorcaoDoProvedorSaida]:
    """Restrita a Mestre ou Admin: a situação de ressarcimento das
    absorções do próprio operador em sessão, somente leitura (`RF-07-24`,
    `RN-07-17`, PRD-07 §§4, 9)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    aportes = listar_absorcoes_do_provedor(sessao_bd, operador=operador)
    return [
        AbsorcaoDoProvedorSaida(
            id=aporte.id,
            tipo_de_recurso_id=aporte.tipo_de_recurso_id,
            quantidade=aporte.quantidade,
            ponto_de_apoio_id=aporte.ponto_de_apoio_id,
            valor_em_moedas=aporte.valor_em_moedas,
            situacao_de_ressarcimento=aporte.situacao_de_ressarcimento.value,
            data_do_aporte=aporte.data_do_aporte,
        )
        for aporte in aportes
    ]
