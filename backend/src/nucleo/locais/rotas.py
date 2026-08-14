import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from ..autenticacao import ContextoDaSessao, exigir_persona
from ..banco import obter_sessao
from ..erros import ErroDeValidacao
from ..paginacao import PaginaDeResultado, ParametrosDeListagem, contrato_de_listagem
from ..personas.modelo import Persona
from .regra import LocalSaida, cadastrar_local, paginar_locais

roteador = APIRouter()


class CriarLocalEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    comunidade_id: uuid.UUID
    nivel: str = Field(min_length=1)
    rotulo: str = Field(min_length=1)
    local_pai_id: uuid.UUID | None = None


@roteador.post("/locais", status_code=201)
def cadastrar_local_rota(
    entrada: CriarLocalEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> LocalSaida:
    """Restrita ao Admin — a recusa de qualquer outro papel é 403,
    devolvida por `cadastrar_local` (`RF-08-04`, `RN-08-18`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    local = cadastrar_local(
        sessao_bd,
        operador=operador,
        comunidade_id=entrada.comunidade_id,
        nivel=entrada.nivel,
        rotulo=entrada.rotulo,
        local_pai_id=entrada.local_pai_id,
    )
    sessao_bd.commit()
    return LocalSaida(
        id=local.id,
        comunidade_virtual_id=local.comunidade_virtual_id,
        nivel=local.nivel.value,
        rotulo=local.rotulo,
        local_pai_id=local.local_pai_id,
    )


def _analisar_comunidade(valor: str | None) -> uuid.UUID | None:
    if not valor:
        return None
    try:
        return uuid.UUID(valor)
    except ValueError as exc:
        raise ErroDeValidacao(
            mensagem="Filtro 'comunidade' precisa ser um identificador válido.",
            campo="comunidade",
        ) from exc


@roteador.get("/locais", response_model=PaginaDeResultado[LocalSaida])
def listar_locais(
    parametros: Annotated[
        ParametrosDeListagem, Depends(contrato_de_listagem(filtro_comunidade_obrigatorio=True))
    ],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> PaginaDeResultado[LocalSaida]:
    """O filtro de comunidade é obrigatório: sem ele o núcleo recusa com
    422, em vez de misturar locais de comunidades diferentes (`RF-01-18`,
    `RF-01-28`)."""
    comunidade_id = _analisar_comunidade(parametros.filtros.get("comunidade"))
    return paginar_locais(
        sessao_bd,
        comunidade_id=comunidade_id,
        cursor=parametros.cursor,
        tamanho=parametros.tamanho,
    )
