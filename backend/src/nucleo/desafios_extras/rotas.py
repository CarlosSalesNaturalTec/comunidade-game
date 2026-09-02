import uuid
from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from ..aportes.modelo import Aporte
from ..autenticacao import ContextoDaSessao, exigir_persona
from ..banco import obter_sessao
from ..erros import PermissaoNegada
from ..permissoes import Operacao, exigir_permissao
from ..personas.modelo import Papel, Persona
from ..pontos_de_apoio.modelo import PontoDeApoio
from ..recursos.modelo import TipoDeRecurso
from ..trilhas.modelo import Missao, Trilha
from .modelo import CusteioDoDesafioExtra, DesafioExtra, FormatoDoDesafioExtra, Modalidade
from .regra import (
    lastro_provido as calcular_lastro_provido,
)
from .regra import (
    listar_desafios_do_proponente,
    motivo_de_lastro_faltante,
    propor_desafio_extra,
)
from .regra import (
    quantidade_restante as calcular_quantidade_restante,
)

roteador = APIRouter()


class DesafioExtraSaida(BaseModel):
    id: uuid.UUID
    trilha_id: uuid.UUID
    missao_id: uuid.UUID | None
    modalidade: str
    nick_do_destinatario: str | None
    justificativa_do_vinculo: str | None
    tipo_de_recurso_id: uuid.UUID
    ponto_de_apoio_id: uuid.UUID
    quantidade_disponivel: int
    quantidade_restante: int
    criterio_de_atribuicao: str
    pontos_extras: int
    formato: str
    custeio: str
    aporte_id: uuid.UUID | None
    vigencia_inicio: date
    vigencia_fim: date
    situacao: str
    motivo_da_recusa: str | None
    lastro_provido: bool
    lastro_faltante: str | None


def _saida(sessao: Session, desafio: DesafioExtra) -> DesafioExtraSaida:
    return DesafioExtraSaida(
        id=desafio.id,
        trilha_id=desafio.trilha_id,
        missao_id=desafio.missao_id,
        modalidade=desafio.modalidade.value,
        nick_do_destinatario=desafio.nick_do_destinatario,
        justificativa_do_vinculo=desafio.justificativa_do_vinculo,
        tipo_de_recurso_id=desafio.tipo_de_recurso_id,
        ponto_de_apoio_id=desafio.ponto_de_apoio_id,
        quantidade_disponivel=desafio.quantidade_disponivel,
        # A disponível menos as conclusões com recompensa entregue, nunca
        # negativa (`RF-14-37`, `RF-14-42`).
        quantidade_restante=calcular_quantidade_restante(sessao, desafio=desafio),
        criterio_de_atribuicao=desafio.criterio_de_atribuicao,
        pontos_extras=desafio.pontos_extras,
        formato=desafio.formato.value,
        custeio=desafio.custeio.value,
        aporte_id=desafio.aporte_id,
        vigencia_inicio=desafio.vigencia_inicio,
        vigencia_fim=desafio.vigencia_fim,
        situacao=desafio.situacao.value,
        motivo_da_recusa=desafio.motivo_da_recusa,
        lastro_provido=calcular_lastro_provido(sessao, desafio=desafio),
        lastro_faltante=motivo_de_lastro_faltante(sessao, desafio=desafio),
    )


class ProporDesafioExtraEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    trilha_id: uuid.UUID
    missao_id: uuid.UUID | None = None
    modalidade: Modalidade
    nick_do_destinatario: str | None = None
    justificativa_do_vinculo: str | None = None
    tipo_de_recurso_id: uuid.UUID
    ponto_de_apoio_id: uuid.UUID
    quantidade_disponivel: int
    criterio_de_atribuicao: str
    pontos_extras: int
    formato: FormatoDoDesafioExtra
    custeio: CusteioDoDesafioExtra
    aporte_id: uuid.UUID | None = None
    vigencia_inicio: date
    vigencia_fim: date


@roteador.post("/desafios-extras", status_code=201)
def propor_desafio_extra_rota(
    entrada: ProporDesafioExtraEntrada,
    contexto: Annotated[
        ContextoDaSessao, Depends(exigir_permissao(Operacao.propostas_de_desafio_extra, "escreve"))
    ],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> DesafioExtraSaida:
    """Restrita ao Apoiador em sessão — nasce sempre em validação do Mestre
    (`RF-14-29` a `RF-14-34`, `RF-14-74` a `RF-14-76`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    trilha = sessao_bd.get(Trilha, entrada.trilha_id)
    missao = sessao_bd.get(Missao, entrada.missao_id) if entrada.missao_id is not None else None
    tipo_de_recurso = sessao_bd.get(TipoDeRecurso, entrada.tipo_de_recurso_id)
    ponto_de_apoio = sessao_bd.get(PontoDeApoio, entrada.ponto_de_apoio_id)
    aporte = sessao_bd.get(Aporte, entrada.aporte_id) if entrada.aporte_id is not None else None
    desafio = propor_desafio_extra(
        sessao_bd,
        operador=operador,
        trilha=trilha,
        missao=missao,
        modalidade=entrada.modalidade,
        nick_do_destinatario=entrada.nick_do_destinatario,
        justificativa_do_vinculo=entrada.justificativa_do_vinculo,
        tipo_de_recurso=tipo_de_recurso,
        ponto_de_apoio=ponto_de_apoio,
        quantidade_disponivel=entrada.quantidade_disponivel,
        criterio_de_atribuicao=entrada.criterio_de_atribuicao,
        pontos_extras=entrada.pontos_extras,
        formato=entrada.formato,
        custeio=entrada.custeio,
        aporte=aporte,
        vigencia_inicio=entrada.vigencia_inicio,
        vigencia_fim=entrada.vigencia_fim,
    )
    sessao_bd.commit()
    return _saida(sessao_bd, desafio)


@roteador.get("/eu/desafios-extras")
def meus_desafios_extras_rota(
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> list[DesafioExtraSaida]:
    """Restrita ao Apoiador — só os próprios, no mesmo molde de
    `/eu/solicitacoes` (`RF-14-35` a `RF-14-39`)."""
    if contexto.papel != Papel.apoiador:
        raise PermissaoNegada(mensagem="Só o Apoiador lê os próprios desafios extras.")

    desafios = listar_desafios_do_proponente(sessao_bd, proponente_id=contexto.persona_id)
    return [_saida(sessao_bd, desafio) for desafio in desafios]
