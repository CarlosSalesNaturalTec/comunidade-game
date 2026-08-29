import uuid
from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from ..autenticacao import ContextoDaSessao, exigir_persona
from ..banco import obter_sessao
from ..erros import PermissaoNegada
from ..personas.modelo import Papel, Persona
from ..pontos_de_apoio.modelo import PontoDeApoio
from ..recursos.modelo import TipoDeRecurso
from ..tempo import DataHoraComFuso
from ..trilhas.modelo import Missao, Trilha
from .modelo import EntregaDeRecompensa, RecompensaDeMarco
from .regra import (
    declarar_recompensa_de_marco,
    listar_entregas,
    listar_recompensas_conquistadas,
    listar_recompensas_de_marco,
    registrar_entrega,
)

roteador = APIRouter()


class RecompensaDeMarcoSaida(BaseModel):
    id: uuid.UUID
    trilha_id: uuid.UUID
    missao_id: uuid.UUID
    tipo_de_recurso_id: uuid.UUID
    quantidade: Decimal
    autor_id: uuid.UUID
    registrado_em: DataHoraComFuso


def _saida(recompensa: RecompensaDeMarco) -> RecompensaDeMarcoSaida:
    return RecompensaDeMarcoSaida(
        id=recompensa.id,
        trilha_id=recompensa.trilha_id,
        missao_id=recompensa.missao_id,
        tipo_de_recurso_id=recompensa.tipo_de_recurso_id,
        quantidade=recompensa.quantidade,
        autor_id=recompensa.autor_id,
        registrado_em=recompensa.registrado_em,
    )


class DeclararRecompensaDeMarcoEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    missao_id: uuid.UUID
    tipo_de_recurso_id: uuid.UUID
    quantidade: Decimal


@roteador.post("/trilhas/{id_da_trilha}/recompensas-de-marco", status_code=201)
def declarar_recompensa_de_marco_rota(
    id_da_trilha: uuid.UUID,
    entrada: DeclararRecompensaDeMarcoEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> RecompensaDeMarcoSaida:
    """Restrita ao Mestre autor da trilha — o marco precisa ser uma missão
    dela, e a declaração não aceita preço nem contrapartida (`RF-09-71`,
    `RN-09-26`, `RN-09-39`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    trilha = sessao_bd.get(Trilha, id_da_trilha)
    missao = sessao_bd.get(Missao, entrada.missao_id)
    tipo = sessao_bd.get(TipoDeRecurso, entrada.tipo_de_recurso_id)
    recompensa = declarar_recompensa_de_marco(
        sessao_bd,
        operador=operador,
        trilha=trilha,
        missao=missao,
        tipo=tipo,
        quantidade=entrada.quantidade,
    )
    sessao_bd.commit()
    return _saida(recompensa)


@roteador.get("/trilhas/{id_da_trilha}/recompensas-de-marco")
def listar_recompensas_de_marco_rota(
    id_da_trilha: uuid.UUID,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> list[RecompensaDeMarcoSaida]:
    """As recompensas de marco declaradas na trilha, para a gestão
    (`RF-09-71`)."""
    recompensas = listar_recompensas_de_marco(sessao_bd, trilha_id=id_da_trilha)
    return [_saida(recompensa) for recompensa in recompensas]


class EntregaDeRecompensaSaida(BaseModel):
    id: uuid.UUID
    recompensa_de_marco_id: uuid.UUID
    missao_id: uuid.UUID
    trilha_id: uuid.UUID
    tipo_de_recurso_id: uuid.UUID
    quantidade: Decimal
    guerreiro_id: uuid.UUID
    ponto_de_apoio_id: uuid.UUID
    lancamento_id: uuid.UUID
    autor_id: uuid.UUID
    registrado_em: DataHoraComFuso


def _saida_da_entrega(sessao: Session, entrega: EntregaDeRecompensa) -> EntregaDeRecompensaSaida:
    """`RF-02-50`, `RF-02-51`, `RN-02-17`: o tipo de recurso, a quantidade e
    o lançamento da baixa entram na saída para a gestão distinguir o
    exemplar da linha Alpha da camisa e alcançar a baixa definitiva — nunca
    o valor em moedas nem em reais, que ficam só no lançamento."""
    recompensa = sessao.get(RecompensaDeMarco, entrega.recompensa_de_marco_id)
    return EntregaDeRecompensaSaida(
        id=entrega.id,
        recompensa_de_marco_id=entrega.recompensa_de_marco_id,
        missao_id=recompensa.missao_id,
        trilha_id=recompensa.trilha_id,
        tipo_de_recurso_id=recompensa.tipo_de_recurso_id,
        quantidade=recompensa.quantidade,
        guerreiro_id=entrega.guerreiro_id,
        ponto_de_apoio_id=entrega.ponto_de_apoio_id,
        lancamento_id=entrega.lancamento_id,
        autor_id=entrega.autor_id,
        registrado_em=entrega.registrado_em,
    )


class RegistrarEntregaEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    guerreiro_id: uuid.UUID
    ponto_de_apoio_id: uuid.UUID


@roteador.post("/recompensas-de-marco/{id_da_recompensa}/entregas", status_code=201)
def registrar_entrega_rota(
    id_da_recompensa: uuid.UUID,
    entrada: RegistrarEntregaEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> EntregaDeRecompensaSaida:
    """Restrita ao Mestre vinculado à comunidade do Guerreiro(a) — o Admin
    nunca confirma a entrega (`RF-07-13`, `RF-02-50`, `RF-02-51`,
    `RN-02-17`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    recompensa = sessao_bd.get(RecompensaDeMarco, id_da_recompensa)
    guerreiro = sessao_bd.get(Persona, entrada.guerreiro_id)
    ponto_de_apoio = sessao_bd.get(PontoDeApoio, entrada.ponto_de_apoio_id)
    entrega = registrar_entrega(
        sessao_bd,
        operador=operador,
        recompensa=recompensa,
        guerreiro=guerreiro,
        ponto_de_apoio=ponto_de_apoio,
    )
    sessao_bd.commit()
    return _saida_da_entrega(sessao_bd, entrega)


class RecompensaConquistadaSaida(BaseModel):
    recompensa_de_marco_id: uuid.UUID
    trilha_id: uuid.UUID
    missao_id: uuid.UUID
    tipo_de_recurso_id: uuid.UUID
    quantidade: Decimal
    entregue: bool
    entregue_em: DataHoraComFuso | None


@roteador.get("/eu/recompensas")
def minhas_recompensas_conquistadas_rota(
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> list[RecompensaConquistadaSaida]:
    """As recompensas de marco que o Guerreiro(a) em sessão já conquistou,
    entregues ou aguardando o Mestre — nenhum valor em moedas nem em reais,
    e nenhum caminho de compra (`RF-05-45`, `RF-05-46`, `RN-05-07`,
    `RN-05-21`, `RN-05-41`)."""
    if contexto.papel != Papel.guerreiro:
        raise PermissaoNegada(mensagem="Só o Guerreiro(a) lê as próprias recompensas conquistadas.")

    guerreiro = sessao_bd.get(Persona, contexto.persona_id)
    conquistadas = listar_recompensas_conquistadas(sessao_bd, guerreiro=guerreiro)
    return [
        RecompensaConquistadaSaida(
            recompensa_de_marco_id=recompensa.id,
            trilha_id=recompensa.trilha_id,
            missao_id=recompensa.missao_id,
            tipo_de_recurso_id=recompensa.tipo_de_recurso_id,
            quantidade=recompensa.quantidade,
            entregue=entrega is not None,
            entregue_em=entrega.registrado_em if entrega is not None else None,
        )
        for recompensa, entrega in conquistadas
    ]


@roteador.get("/entregas")
def listar_entregas_rota(
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> list[EntregaDeRecompensaSaida]:
    """O histórico de entregas, filtrado por persona: Guerreiro(a) só as
    próprias, Mestre e Admin as da comunidade a que estão vinculados
    (`RF-07-13`, `RN-07-05`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    entregas = listar_entregas(sessao_bd, operador=operador)
    return [_saida_da_entrega(sessao_bd, entrega) for entrega in entregas]
