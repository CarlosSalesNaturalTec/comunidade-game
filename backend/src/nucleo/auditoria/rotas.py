import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import tuple_
from sqlalchemy.orm import Session

from ..autenticacao import ContextoDaSessao
from ..banco import obter_sessao
from ..erros import ErroDeValidacao
from ..paginacao import (
    PaginaDeResultado,
    ParametrosDeListagem,
    codificar_cursor,
    contrato_de_listagem,
    decodificar_cursor,
)
from ..permissoes import Operacao, exigir_permissao
from .modelo import Auditoria

roteador = APIRouter()

# Filtros de domínio da trilha; período e persona já vêm dos universais de
# `contrato_de_listagem` (`RF-01-28`).
_FILTROS_DE_DOMINIO = frozenset({"acao", "entidade_afetada"})


class RegistroDeAuditoriaSaida(BaseModel):
    id: uuid.UUID
    autor_id: uuid.UUID
    papel_do_autor: str
    acao: str
    entidade_afetada: str
    momento: datetime
    origem: str


def _analisar_momento(bruto: str, campo: str) -> datetime:
    """Toda data e hora de filtro exige fuso explícito, como em qualquer
    entrada do núcleo (PRD-01 §9)."""
    try:
        valor = datetime.fromisoformat(bruto)
    except ValueError as exc:
        raise ErroDeValidacao(
            mensagem=f"Filtro '{campo}' precisa ser uma data e hora ISO 8601.", campo=campo
        ) from exc
    if valor.tzinfo is None:
        raise ErroDeValidacao(mensagem=f"Filtro '{campo}' exige fuso explícito.", campo=campo)
    return valor


@roteador.get("/auditoria", response_model=PaginaDeResultado[RegistroDeAuditoriaSaida])
def consultar_auditoria(
    parametros: Annotated[ParametrosDeListagem, Depends(contrato_de_listagem(_FILTROS_DE_DOMINIO))],
    contexto: Annotated[ContextoDaSessao, Depends(exigir_permissao(Operacao.tudo, "le"))],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> PaginaDeResultado[RegistroDeAuditoriaSaida]:
    """Restrita a Admin pela matriz — só ele alcança `Operacao.tudo` em
    leitura, sem entrada nova na matriz (`RF-01-29`, PRD-01 §9). Paginada
    por cursor opaco sobre `(momento, id)`, no mesmo contrato das demais
    listagens (`RF-01-28`).
    """
    consulta = sessao_bd.query(Auditoria)

    persona_filtro = parametros.filtros.get("persona")
    if persona_filtro:
        try:
            id_da_persona = uuid.UUID(persona_filtro)
        except ValueError as exc:
            raise ErroDeValidacao(
                mensagem="Filtro 'persona' precisa ser um identificador válido.", campo="persona"
            ) from exc
        consulta = consulta.filter(Auditoria.autor_id == id_da_persona)

    periodo_inicio = parametros.filtros.get("periodo_inicio")
    if periodo_inicio:
        consulta = consulta.filter(
            Auditoria.momento >= _analisar_momento(periodo_inicio, "periodo_inicio")
        )

    periodo_fim = parametros.filtros.get("periodo_fim")
    if periodo_fim:
        consulta = consulta.filter(
            Auditoria.momento <= _analisar_momento(periodo_fim, "periodo_fim")
        )

    acao_filtro = parametros.filtros.get("acao")
    if acao_filtro:
        consulta = consulta.filter(Auditoria.acao == acao_filtro)

    entidade_filtro = parametros.filtros.get("entidade_afetada")
    if entidade_filtro:
        consulta = consulta.filter(Auditoria.entidade_afetada == entidade_filtro)

    if parametros.cursor:
        posicao = decodificar_cursor(parametros.cursor)
        try:
            momento_cursor = datetime.fromisoformat(posicao["momento"])
            id_cursor = uuid.UUID(posicao["id"])
        except (KeyError, ValueError) as exc:
            raise ErroDeValidacao(mensagem="Cursor de paginação inválido.", campo="cursor") from exc
        consulta = consulta.filter(
            tuple_(Auditoria.momento, Auditoria.id) > (momento_cursor, id_cursor)
        )

    consulta = consulta.order_by(Auditoria.momento, Auditoria.id).limit(parametros.tamanho + 1)
    registros = consulta.all()

    proximo_cursor = None
    if len(registros) > parametros.tamanho:
        registros = registros[: parametros.tamanho]
        ultimo = registros[-1]
        proximo_cursor = codificar_cursor(
            {"momento": ultimo.momento.isoformat(), "id": str(ultimo.id)}
        )

    return PaginaDeResultado(
        itens=[
            RegistroDeAuditoriaSaida(
                id=registro.id,
                autor_id=registro.autor_id,
                papel_do_autor=registro.papel_do_autor,
                acao=registro.acao,
                entidade_afetada=registro.entidade_afetada,
                momento=registro.momento,
                origem=registro.origem,
            )
            for registro in registros
        ],
        proximo_cursor=proximo_cursor,
    )
