import uuid
from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from ..autenticacao import ContextoDaSessao, exigir_persona
from ..banco import obter_sessao
from ..comunidades.modelo import ComunidadeVirtual
from ..personas.modelo import Persona
from ..pontos_de_apoio.modelo import PontoDeApoio
from ..recursos.modelo import TipoDeRecurso
from ..recursos.regra import consultar_preco_de_referencia
from ..tempo import agora
from .modelo import ItemDeCatalogoAvulso
from .regra import (
    SITUACOES_QUE_NUNCA_ATIVAM,
    alterar_estoque,
    ativar_item,
    cadastrar_item,
    contar_trocas_por_item,
    falta_de_lastro,
    homologar_item,
    listar_catalogo,
    listar_ofertas_do_apoiador,
    retirar_item,
)

roteador = APIRouter()


class ItemDeCatalogoAvulsoSaida(BaseModel):
    id: uuid.UUID
    nome: str
    tipo_de_recurso_id: uuid.UUID
    estoque: Decimal
    comunidade_virtual_id: uuid.UUID
    ponto_de_apoio_id: uuid.UUID
    origem_do_cadastro: str
    situacao_de_homologacao: str
    homologacao_motivo: str | None
    ativo: bool
    preco_em_pontos_extras: int | None
    preco_de_referencia_ausente: bool
    quantidade_faltante: Decimal | None


def _saida(sessao: Session, item: ItemDeCatalogoAvulso) -> ItemDeCatalogoAvulsoSaida:
    tipo = sessao.get(TipoDeRecurso, item.tipo_de_recurso_id)
    preco = consultar_preco_de_referencia(sessao, tipo=tipo, data=agora().date())

    quantidade_faltante = None
    if (
        not item.ativo
        and preco is not None
        and item.situacao_de_homologacao not in SITUACOES_QUE_NUNCA_ATIVAM
    ):
        falta = falta_de_lastro(sessao, item=item)
        if falta > 0:
            quantidade_faltante = falta

    return ItemDeCatalogoAvulsoSaida(
        id=item.id,
        nome=item.nome,
        tipo_de_recurso_id=item.tipo_de_recurso_id,
        estoque=item.estoque,
        comunidade_virtual_id=item.comunidade_virtual_id,
        ponto_de_apoio_id=item.ponto_de_apoio_id,
        origem_do_cadastro=item.origem_do_cadastro.value,
        situacao_de_homologacao=item.situacao_de_homologacao.value,
        homologacao_motivo=item.homologacao_motivo,
        ativo=item.ativo,
        preco_em_pontos_extras=preco.preco_em_pontos_extras if preco is not None else None,
        preco_de_referencia_ausente=preco is None,
        quantidade_faltante=quantidade_faltante,
    )


class MinhaOfertaDeCatalogoAvulsoSaida(ItemDeCatalogoAvulsoSaida):
    quantidade_de_trocas: int


def _saida_da_oferta(
    sessao: Session, item: ItemDeCatalogoAvulso
) -> MinhaOfertaDeCatalogoAvulsoSaida:
    return MinhaOfertaDeCatalogoAvulsoSaida(
        **_saida(sessao, item).model_dump(),
        quantidade_de_trocas=contar_trocas_por_item(sessao, item=item),
    )


class CadastrarItemDeCatalogoAvulsoEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nome: str = Field(min_length=1)
    tipo_de_recurso_id: uuid.UUID
    estoque: Decimal
    comunidade_virtual_id: uuid.UUID
    ponto_de_apoio_id: uuid.UUID
    preco_em_pontos_extras: int | None = None


@roteador.post("/catalogo-avulso", status_code=201)
def cadastrar_item_rota(
    entrada: CadastrarItemDeCatalogoAvulsoEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> ItemDeCatalogoAvulsoSaida:
    """Restrita a Mestre ou Apoiador — o item nasce sem preço próprio, com
    homologação dispensada para Mestre e pendente para Apoiador (`RF-07-33`,
    `RF-07-45`, `RF-09-99`, `RF-09-100`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    tipo = sessao_bd.get(TipoDeRecurso, entrada.tipo_de_recurso_id)
    comunidade = sessao_bd.get(ComunidadeVirtual, entrada.comunidade_virtual_id)
    ponto_de_apoio = sessao_bd.get(PontoDeApoio, entrada.ponto_de_apoio_id)
    item = cadastrar_item(
        sessao_bd,
        operador=operador,
        nome=entrada.nome,
        tipo=tipo,
        estoque=entrada.estoque,
        comunidade=comunidade,
        ponto_de_apoio=ponto_de_apoio,
        preco_em_pontos_extras=entrada.preco_em_pontos_extras,
    )
    sessao_bd.commit()
    return _saida(sessao_bd, item)


@roteador.get("/catalogo-avulso")
def listar_catalogo_avulso_rota(
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    comunidade_virtual_id: uuid.UUID | None = None,
    incluir_inativos: bool = False,
) -> list[ItemDeCatalogoAvulsoSaida]:
    """O catálogo por comunidade: Guerreiro(a) só ativos da sua comunidade;
    Admin e Mestre vinculado podem pedir também os inativos (`RF-07-33`,
    `RF-04-50`, `RF-05-83`, `RF-09-103`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    comunidade = (
        sessao_bd.get(ComunidadeVirtual, comunidade_virtual_id)
        if comunidade_virtual_id is not None
        else None
    )
    itens = listar_catalogo(
        sessao_bd, operador=operador, comunidade=comunidade, incluir_inativos=incluir_inativos
    )
    return [_saida(sessao_bd, item) for item in itens]


@roteador.get("/eu/catalogo-avulso")
def minhas_ofertas_de_catalogo_avulso_rota(
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> list[MinhaOfertaDeCatalogoAvulsoSaida]:
    """Restrita ao Apoiador — os itens que ele ofertou, em qualquer situação,
    com a contagem agregada de trocas, sem identificar quem trocou
    (`RF-14-80`, `RF-14-81`, `RN-14-42`, `RN-14-43`, `RN-14-44`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    itens = listar_ofertas_do_apoiador(sessao_bd, operador=operador)
    return [_saida_da_oferta(sessao_bd, item) for item in itens]


class HomologarItemEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    decisao: str
    motivo: str | None = None


@roteador.post("/catalogo-avulso/{id_do_item}/homologacao")
def homologar_item_rota(
    id_do_item: uuid.UUID,
    entrada: HomologarItemEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> ItemDeCatalogoAvulsoSaida:
    """Restrita ao Admin — homologa ou recusa item pendente de Apoiador
    (`RF-09-100`, `RN-14-42`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    item = sessao_bd.get(ItemDeCatalogoAvulso, id_do_item)
    item = homologar_item(
        sessao_bd, operador=operador, item=item, decisao=entrada.decisao, motivo=entrada.motivo
    )
    sessao_bd.commit()
    return _saida(sessao_bd, item)


@roteador.post("/catalogo-avulso/{id_do_item}/ativacao")
def ativar_item_rota(
    id_do_item: uuid.UUID,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> ItemDeCatalogoAvulsoSaida:
    """Restrita a Admin ou Mestre vinculado — reverifica o lastro no ato
    (`RF-07-34`, `RN-09-37`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    item = sessao_bd.get(ItemDeCatalogoAvulso, id_do_item)
    item = ativar_item(sessao_bd, operador=operador, item=item)
    sessao_bd.commit()
    return _saida(sessao_bd, item)


class AlterarEstoqueEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    estoque: Decimal


@roteador.put("/catalogo-avulso/{id_do_item}/estoque")
def alterar_estoque_rota(
    id_do_item: uuid.UUID,
    entrada: AlterarEstoqueEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> ItemDeCatalogoAvulsoSaida:
    """Restrita a Admin ou Mestre vinculado — estoque acima do lastro
    disponível desativa o item (`RF-07-33`, `RF-07-34`, `RF-09-102`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    item = sessao_bd.get(ItemDeCatalogoAvulso, id_do_item)
    item = alterar_estoque(sessao_bd, operador=operador, item=item, estoque=entrada.estoque)
    sessao_bd.commit()
    return _saida(sessao_bd, item)


@roteador.delete("/catalogo-avulso/{id_do_item}")
def retirar_item_rota(
    id_do_item: uuid.UUID,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> ItemDeCatalogoAvulsoSaida:
    """Restrita a Admin ou Mestre vinculado — a retirada do `RF-09-102`
    deixa o item inativo e preserva o registro."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    item = sessao_bd.get(ItemDeCatalogoAvulso, id_do_item)
    item = retirar_item(sessao_bd, operador=operador, item=item)
    sessao_bd.commit()
    return _saida(sessao_bd, item)
