import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from ..autenticacao import ContextoDaSessao, exigir_persona
from ..banco import obter_sessao
from ..coletas.regra import PontoDaSeriePublicaSaida, paginar_serie_publica
from ..configuracao import Configuracao, obter_configuracao
from ..erros import ErroDeValidacao, NaoEncontrado
from ..paginacao import PaginaDeResultado, ParametrosDeListagem, contrato_de_listagem
from ..personas.modelo import Persona
from .modelo import ComunidadeVirtual
from .regra import ComunidadePublicaSaida, consultar_comunidade_publica, criar_comunidade

roteador = APIRouter()


class CriarComunidadeEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nome: str = Field(min_length=1)
    localizacao: str = Field(min_length=1)
    granularidade_maxima: str = Field(min_length=1)


class ComunidadeSaida(BaseModel):
    id: uuid.UUID
    nome: str
    localizacao: str
    granularidade_maxima: str
    admin_criador_id: uuid.UUID | None
    criada_em: datetime


@roteador.post("/comunidades", status_code=201)
def criar_comunidade_rota(
    entrada: CriarComunidadeEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> ComunidadeSaida:
    """Restrita ao Admin — a recusa de qualquer outro papel é 403,
    devolvida por `criar_comunidade` (`RF-08-01`, `RN-08-01`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    comunidade = criar_comunidade(
        sessao_bd,
        operador=operador,
        nome=entrada.nome,
        localizacao=entrada.localizacao,
        granularidade_maxima=entrada.granularidade_maxima,
    )
    sessao_bd.commit()
    return ComunidadeSaida(
        id=comunidade.id,
        nome=comunidade.nome,
        localizacao=comunidade.localizacao,
        granularidade_maxima=comunidade.granularidade_maxima,
        admin_criador_id=comunidade.admin_criador_id,
        criada_em=comunidade.criada_em,
    )


def _obter_comunidade(sessao_bd: Session, id_da_comunidade: uuid.UUID) -> ComunidadeVirtual:
    comunidade = sessao_bd.get(ComunidadeVirtual, id_da_comunidade)
    if comunidade is None:
        raise NaoEncontrado(mensagem="Comunidade não encontrada.")
    return comunidade


@roteador.get("/comunidades/{id_da_comunidade}", response_model=ComunidadePublicaSaida)
def comunidade_publica(
    id_da_comunidade: uuid.UUID,
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> ComunidadePublicaSaida:
    """Leitura pública, sem credencial de persona: a comunidade, os locais
    até o bairro e os tipos de coleta ativos nela (`RF-08-16`, `RN-08-13`,
    `RF-01-02`, `RN-01-32`, PRD-08 §9)."""
    comunidade = _obter_comunidade(sessao_bd, id_da_comunidade)
    return consultar_comunidade_publica(sessao_bd, comunidade=comunidade)


def _analisar_momento(bruto: str, campo: str) -> datetime:
    """Mesma régua de `auditoria/rotas.py`: toda data e hora de filtro exige
    fuso explícito (PRD-01 §9)."""
    try:
        valor = datetime.fromisoformat(bruto)
    except ValueError as exc:
        raise ErroDeValidacao(
            mensagem=f"Filtro '{campo}' precisa ser uma data e hora ISO 8601.", campo=campo
        ) from exc
    if valor.tzinfo is None:
        raise ErroDeValidacao(mensagem=f"Filtro '{campo}' exige fuso explícito.", campo=campo)
    return valor


@roteador.get(
    "/comunidades/{id_da_comunidade}/series",
    response_model=PaginaDeResultado[PontoDaSeriePublicaSaida],
)
def serie_publica_da_comunidade(
    id_da_comunidade: uuid.UUID,
    parametros: Annotated[ParametrosDeListagem, Depends(contrato_de_listagem())],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    configuracao: Annotated[Configuracao, Depends(obter_configuracao)],
) -> PaginaDeResultado[PontoDaSeriePublicaSaida]:
    """Série histórica pública da comunidade, agregada por tipo de coleta e
    local, parando no bairro e sem coletor (`RF-08-16`, `RN-08-13`,
    `RN-08-12`, `RF-08-28`, `RN-08-24`, `RF-01-28`, `RF-01-02`,
    `RN-01-32`). O período recorta pela data da medição, e o piso de
    coletores é apurado sobre o resultado inteiro antes de qualquer corte
    de página (design — Decisions)."""
    comunidade = _obter_comunidade(sessao_bd, id_da_comunidade)

    periodo_inicio_bruto = parametros.filtros.get("periodo_inicio")
    periodo_inicio = (
        _analisar_momento(periodo_inicio_bruto, "periodo_inicio") if periodo_inicio_bruto else None
    )
    periodo_fim_bruto = parametros.filtros.get("periodo_fim")
    periodo_fim = _analisar_momento(periodo_fim_bruto, "periodo_fim") if periodo_fim_bruto else None

    return paginar_serie_publica(
        sessao_bd,
        comunidade=comunidade,
        piso_de_coletores=configuracao.territorio_piso_de_coletores_distintos,
        cursor=parametros.cursor,
        tamanho=parametros.tamanho,
        periodo_inicio=periodo_inicio,
        periodo_fim=periodo_fim,
    )
