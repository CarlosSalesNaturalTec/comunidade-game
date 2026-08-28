import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from ..autenticacao import ContextoDaSessao, exigir_persona
from ..banco import obter_sessao
from ..erros import PermissaoNegada
from ..personas.modelo import Papel, Persona
from ..trilhas.modelo import Atividade, FormatoDeAtividade, ModalidadeDeAtividade
from .regra import cadastrar_atividade_avulsa, listar_atividades_avulsas

roteador = APIRouter()


class AtividadeAvulsaSaida(BaseModel):
    id: uuid.UUID
    titulo: str
    descricao: str | None
    modalidade: ModalidadeDeAtividade
    formato: FormatoDeAtividade
    natureza: str
    producao_esperada: str
    poder_id: uuid.UUID


def _saida(atividade: Atividade) -> AtividadeAvulsaSaida:
    return AtividadeAvulsaSaida(
        id=atividade.id,
        titulo=atividade.titulo,
        descricao=atividade.descricao,
        modalidade=atividade.modalidade,
        formato=atividade.formato,
        natureza=atividade.natureza,
        producao_esperada=atividade.producao_esperada,
        poder_id=atividade.poder_id,
    )


class CadastrarAtividadeAvulsaEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    titulo: str | None = None
    descricao: str | None = None
    modalidade: str | None = None
    formato: str | None = None
    natureza: str | None = None
    producao_esperada: str | None = None
    poder_id: uuid.UUID | None = None


@roteador.post("/atividades", status_code=201)
def cadastrar_atividade_avulsa_rota(
    entrada: CadastrarAtividadeAvulsaEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> AtividadeAvulsaSaida:
    """`RF-02-29`, PRD-02 §9: cadastra a atividade fora de trilha, com o
    poder que ela desenvolve — a exigência de Admin e as recusas de campo
    já são de `cadastrar_atividade_avulsa`."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    atividade = cadastrar_atividade_avulsa(
        sessao_bd,
        operador=operador,
        titulo=entrada.titulo,
        descricao=entrada.descricao,
        modalidade=entrada.modalidade,
        formato=entrada.formato,
        natureza=entrada.natureza,
        producao_esperada=entrada.producao_esperada,
        poder_id=entrada.poder_id,
    )
    sessao_bd.commit()
    return _saida(atividade)


@roteador.get("/atividades", response_model=list[AtividadeAvulsaSaida])
def listar_atividades_avulsas_rota(
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> list[AtividadeAvulsaSaida]:
    """Adição não prevista na proposal desta change, mesmo precedente de
    `recursos.rotas.listar_tipos_de_recurso_rota`: sem ela a `TelaDeAtividades`
    da App 03 não tem o que listar (`RF-02-29`). Restrita à mesma exigência
    de Admin do cadastro — a recusa é de `cadastrar_atividade_avulsa`, que
    esta leitura não invoca; a matriz de permissões desta fatia é só a do
    cadastro, então a leitura confere o papel diretamente."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    if operador.papel != Papel.admin:
        raise PermissaoNegada(mensagem="Só o Admin lê o cadastro de atividades avulsas.")
    atividades = listar_atividades_avulsas(sessao_bd)
    return [_saida(atividade) for atividade in atividades]
