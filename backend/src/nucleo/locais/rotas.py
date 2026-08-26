import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from ..autenticacao import ContextoDaSessao, exigir_persona
from ..banco import obter_sessao
from ..coletas.modelo import DesafioDeColeta
from ..erros import ErroDeValidacao
from ..paginacao import PaginaDeResultado, ParametrosDeListagem, contrato_de_listagem
from ..permissoes import Operacao, exigir_permissao
from ..personas.modelo import Persona
from .modelo import SituacaoDaSolicitacaoDeLocal, SolicitacaoDeLocal
from .regra import (
    LocalSaida,
    SolicitacaoDeLocalSaida,
    avaliar_solicitacao_de_local,
    cadastrar_local,
    consultar_solicitacoes_do_guerreiro,
    listar_solicitacoes_de_local_abertas,
    paginar_locais,
    solicitar_local,
)

roteador = APIRouter()


def _saida_da_solicitacao(solicitacao: SolicitacaoDeLocal) -> SolicitacaoDeLocalSaida:
    return SolicitacaoDeLocalSaida(
        id=solicitacao.id,
        solicitante_id=solicitacao.solicitante_id,
        comunidade_virtual_id=solicitacao.comunidade_virtual_id,
        desafio_de_coleta_id=solicitacao.desafio_de_coleta_id,
        nivel_pretendido=solicitacao.nivel_pretendido.value,
        rotulo=solicitacao.rotulo,
        justificativa=solicitacao.justificativa,
        situacao=solicitacao.situacao.value,
        avaliador_id=solicitacao.avaliador_id,
        motivo_da_recusa=solicitacao.motivo_da_recusa,
        local_criado_id=solicitacao.local_criado_id,
        avaliado_em=solicitacao.avaliado_em,
        registrado_em=solicitacao.registrado_em,
    )


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


class SolicitarLocalEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    comunidade_id: uuid.UUID
    desafio_de_coleta_id: uuid.UUID
    nivel: str = Field(min_length=1)
    rotulo: str = Field(min_length=1)
    justificativa: str = Field(min_length=1)


@roteador.post("/solicitacoes-de-local", status_code=201)
def solicitar_local_rota(
    entrada: SolicitarLocalEntrada,
    contexto: Annotated[
        ContextoDaSessao, Depends(exigir_permissao(Operacao.solicitacao_de_local, "escreve"))
    ],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> SolicitacaoDeLocalSaida:
    """Restrita ao Guerreiro(a), pela matriz de permissões — a recusa de
    qualquer outro papel é 403 (`RF-08-22`). O pedido em si NEVER cria
    local (`RN-08-18`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    desafio = sessao_bd.get(DesafioDeColeta, entrada.desafio_de_coleta_id)
    solicitacao = solicitar_local(
        sessao_bd,
        operador=operador,
        desafio=desafio,
        comunidade_id=entrada.comunidade_id,
        nivel=entrada.nivel,
        rotulo=entrada.rotulo,
        justificativa=entrada.justificativa,
    )
    sessao_bd.commit()
    return _saida_da_solicitacao(solicitacao)


@roteador.get(
    "/solicitacoes-de-local/minhas", response_model=PaginaDeResultado[SolicitacaoDeLocalSaida]
)
def consultar_solicitacoes_do_guerreiro_rota(
    parametros: Annotated[ParametrosDeListagem, Depends(contrato_de_listagem())],
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> PaginaDeResultado[SolicitacaoDeLocalSaida]:
    """Restrita ao Guerreiro(a) — a recusa de qualquer outro papel é 403,
    devolvida por `consultar_solicitacoes_do_guerreiro` (`RF-05-32`,
    `RN-05-11`, `RN-05-21`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    pagina = consultar_solicitacoes_do_guerreiro(
        sessao_bd, operador=operador, cursor=parametros.cursor, tamanho=parametros.tamanho
    )
    sessao_bd.commit()
    return pagina


class AvaliarSolicitacaoDeLocalEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    situacao: str = Field(min_length=1)
    local_pai_id: uuid.UUID | None = None
    motivo: str | None = None


@roteador.post("/solicitacoes-de-local/{id_da_solicitacao}/avaliacao")
def avaliar_solicitacao_de_local_rota(
    id_da_solicitacao: uuid.UUID,
    entrada: AvaliarSolicitacaoDeLocalEntrada,
    contexto: Annotated[
        ContextoDaSessao, Depends(exigir_permissao(Operacao.aprovacao_de_local, "escreve"))
    ],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> SolicitacaoDeLocalSaida:
    """Restrita a Admin e ao Mestre autor da trilha do desafio de origem —
    quem não tem essa posse, inclusive o Guerreiro(a) solicitante, recebe
    403 de `avaliar_solicitacao_de_local` (`RF-08-23`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    solicitacao = sessao_bd.get(SolicitacaoDeLocal, id_da_solicitacao)
    try:
        situacao_valida = SituacaoDaSolicitacaoDeLocal(entrada.situacao)
    except ValueError as exc:
        raise ErroDeValidacao(
            mensagem="Desfecho precisa ser aprovada ou recusada.", campo="situacao"
        ) from exc
    solicitacao = avaliar_solicitacao_de_local(
        sessao_bd,
        solicitacao,
        operador=operador,
        situacao=situacao_valida,
        local_pai_id=entrada.local_pai_id,
        motivo=entrada.motivo,
    )
    sessao_bd.commit()
    return _saida_da_solicitacao(solicitacao)


@roteador.get(
    "/solicitacoes-de-local/abertas", response_model=PaginaDeResultado[SolicitacaoDeLocalSaida]
)
def listar_solicitacoes_de_local_abertas_rota(
    parametros: Annotated[
        ParametrosDeListagem, Depends(contrato_de_listagem(filtro_comunidade_obrigatorio=True))
    ],
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> PaginaDeResultado[SolicitacaoDeLocalSaida]:
    """O filtro de comunidade é obrigatório (`RF-01-18`, `RF-01-28`); o
    recorte por papel — Admin vê todas, Mestre só as das suas trilhas — é
    de `listar_solicitacoes_de_local_abertas`, que também recusa com 403
    qualquer outro papel (`RF-08-24`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    comunidade_id = _analisar_comunidade(parametros.filtros.get("comunidade"))
    return listar_solicitacoes_de_local_abertas(
        sessao_bd,
        operador=operador,
        comunidade_id=comunidade_id,
        cursor=parametros.cursor,
        tamanho=parametros.tamanho,
    )
