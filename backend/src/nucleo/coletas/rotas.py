import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from ..autenticacao import ContextoDaSessao
from ..banco import obter_sessao
from ..permissoes import Operacao, exigir_permissao
from ..personas.modelo import Persona
from ..tempo import DataHoraComFuso
from ..trilhas.modelo import Missao
from .regra import cadastrar_tipo_de_coleta, criar_desafio_de_coleta

roteador = APIRouter()


class CriarTipoDeColetaEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nome: str = Field(min_length=1)
    forma_de_registro: str = Field(min_length=1)
    unidade: str | None = None
    faixa_minima: float | None = None
    faixa_maxima: float | None = None


class TipoDeColetaSaida(BaseModel):
    id: uuid.UUID
    nome: str
    forma_de_registro: str
    unidade: str | None
    faixa_minima: float | None
    faixa_maxima: float | None
    ativo: bool


@roteador.post("/tipos-de-coleta", status_code=201)
def cadastrar_tipo_de_coleta_rota(
    entrada: CriarTipoDeColetaEntrada,
    contexto: Annotated[
        ContextoDaSessao,
        Depends(exigir_permissao(Operacao.catalogo_de_tipos_de_coleta, "escreve")),
    ],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> TipoDeColetaSaida:
    """Restrita ao Admin — a recusa de qualquer outro papel, inclusive o
    Mestre, é 403 pela matriz de permissões (`RF-08-05`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    tipo = cadastrar_tipo_de_coleta(
        sessao_bd,
        operador=operador,
        nome=entrada.nome,
        forma_de_registro=entrada.forma_de_registro,
        unidade=entrada.unidade,
        faixa_minima=entrada.faixa_minima,
        faixa_maxima=entrada.faixa_maxima,
    )
    sessao_bd.commit()
    return TipoDeColetaSaida(
        id=tipo.id,
        nome=tipo.nome,
        forma_de_registro=tipo.forma_de_registro.value,
        unidade=tipo.unidade,
        faixa_minima=tipo.faixa_minima,
        faixa_maxima=tipo.faixa_maxima,
        ativo=tipo.ativo,
    )


class CriarDesafioDeColetaEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    missao_id: uuid.UUID
    tipo_de_coleta_id: uuid.UUID
    cadencia: str = Field(min_length=1)
    vigencia_inicio: DataHoraComFuso
    vigencia_fim: DataHoraComFuso
    granularidade_exigida: str = Field(min_length=1)
    registros_que_pontuam_por_periodo: int


class DesafioDeColetaSaida(BaseModel):
    id: uuid.UUID
    missao_id: uuid.UUID
    tipo_de_coleta_id: uuid.UUID
    cadencia: str
    vigencia_inicio: datetime
    vigencia_fim: datetime
    granularidade_exigida: str
    registros_que_pontuam_por_periodo: int


@roteador.post("/desafios-de-coleta", status_code=201)
def criar_desafio_de_coleta_rota(
    entrada: CriarDesafioDeColetaEntrada,
    contexto: Annotated[
        ContextoDaSessao, Depends(exigir_permissao(Operacao.suas_trilhas_e_conteudos, "escreve"))
    ],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> DesafioDeColetaSaida:
    """Restrita ao Mestre autor da trilha da missão e ao Admin — a posse é
    conferida em `criar_desafio_de_coleta`, pela trilha alcançada a partir
    da missão (`RF-08-06`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    missao = sessao_bd.get(Missao, entrada.missao_id)
    desafio = criar_desafio_de_coleta(
        sessao_bd,
        operador=operador,
        missao=missao,
        tipo_de_coleta_id=entrada.tipo_de_coleta_id,
        cadencia=entrada.cadencia,
        vigencia_inicio=entrada.vigencia_inicio,
        vigencia_fim=entrada.vigencia_fim,
        granularidade_exigida=entrada.granularidade_exigida,
        registros_que_pontuam_por_periodo=entrada.registros_que_pontuam_por_periodo,
    )
    sessao_bd.commit()
    return DesafioDeColetaSaida(
        id=desafio.id,
        missao_id=desafio.missao_id,
        tipo_de_coleta_id=desafio.tipo_de_coleta_id,
        cadencia=desafio.cadencia.value,
        vigencia_inicio=desafio.vigencia_inicio,
        vigencia_fim=desafio.vigencia_fim,
        granularidade_exigida=desafio.granularidade_exigida.value,
        registros_que_pontuam_por_periodo=desafio.registros_que_pontuam_por_periodo,
    )
