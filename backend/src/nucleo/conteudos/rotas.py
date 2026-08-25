import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from ..armazenamento.fabrica import dependencia_de_armazenamento
from ..armazenamento.porta import PortaDeArmazenamento
from ..autenticacao import ContextoDaSessao, exigir_persona
from ..banco import obter_sessao
from ..erros import NaoEncontrado
from ..personas.modelo import Persona
from ..trilhas.modelo import Missao
from .modelo import AutoriaDoConteudo, ConteudoDaMissao, TipoDeConteudo
from .regra import abrir_envio, confirmar_envio, criar_conteudo

roteador = APIRouter()


class ConteudoSaida(BaseModel):
    id: uuid.UUID
    missao_id: uuid.UUID
    ordem: int
    tipo: TipoDeConteudo
    corpo: str | None
    endereco: str | None
    referencia: str | None
    tamanho: int | None
    autoria: AutoriaDoConteudo
    fonte: str | None


def saida_do_conteudo(conteudo: ConteudoDaMissao) -> ConteudoSaida:
    return ConteudoSaida(
        id=conteudo.id,
        missao_id=conteudo.missao_id,
        ordem=conteudo.ordem,
        tipo=conteudo.tipo,
        corpo=conteudo.corpo,
        endereco=conteudo.endereco,
        referencia=conteudo.referencia,
        tamanho=conteudo.tamanho,
        autoria=conteudo.autoria,
        fonte=conteudo.fonte,
    )


def _obter_missao(sessao_bd: Session, id_da_missao: uuid.UUID) -> Missao:
    missao = sessao_bd.get(Missao, id_da_missao)
    if missao is None:
        raise NaoEncontrado(mensagem="Missão não encontrada.")
    return missao


def _obter_conteudo(sessao_bd: Session, id_do_conteudo: uuid.UUID) -> ConteudoDaMissao:
    conteudo = sessao_bd.get(ConteudoDaMissao, id_do_conteudo)
    if conteudo is None:
        raise NaoEncontrado(mensagem="Conteúdo não encontrado.")
    return conteudo


class CriarConteudoEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tipo: str
    ordem: int
    corpo: str | None = None
    endereco: str | None = None
    autoria: str
    fonte: str | None = None


@roteador.post("/missoes/{id_da_missao}/conteudos", status_code=201)
def criar_conteudo_rota(
    id_da_missao: uuid.UUID,
    entrada: CriarConteudoEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> ConteudoSaida:
    """`RF-09-14`, `RF-09-15`: a autoria estrita e a coerência de cada tipo
    já são de `criar_conteudo` (design — decisão 4)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    missao = _obter_missao(sessao_bd, id_da_missao)
    conteudo = criar_conteudo(
        sessao_bd,
        operador=operador,
        missao=missao,
        tipo=entrada.tipo,
        ordem=entrada.ordem,
        corpo=entrada.corpo,
        endereco=entrada.endereco,
        autoria=entrada.autoria,
        fonte=entrada.fonte,
    )
    sessao_bd.commit()
    return saida_do_conteudo(conteudo)


class AbrirEnvioEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tipo_mime: str
    tamanho_declarado: int


class AbrirEnvioSaida(BaseModel):
    endereco_da_sessao: str


@roteador.post("/conteudos/{id_do_conteudo}/arquivo", status_code=201)
def abrir_envio_rota(
    id_do_conteudo: uuid.UUID,
    entrada: AbrirEnvioEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    armazenamento: Annotated[PortaDeArmazenamento, Depends(dependencia_de_armazenamento)],
) -> AbrirEnvioSaida:
    """`RF-09-16` a `RF-09-19`, `RF-09-115`: abre a sessão retomável — a
    autoria, o formato e o teto já são de `abrir_envio` (design — decisões
    1, 2)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    conteudo = _obter_conteudo(sessao_bd, id_do_conteudo)
    endereco = abrir_envio(
        sessao_bd,
        conteudo,
        operador=operador,
        tipo_mime=entrada.tipo_mime,
        tamanho_declarado=entrada.tamanho_declarado,
        armazenamento=armazenamento,
    )
    sessao_bd.commit()
    return AbrirEnvioSaida(endereco_da_sessao=endereco)


@roteador.patch("/conteudos/{id_do_conteudo}/arquivo")
def confirmar_envio_rota(
    id_do_conteudo: uuid.UUID,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    armazenamento: Annotated[PortaDeArmazenamento, Depends(dependencia_de_armazenamento)],
) -> ConteudoSaida:
    """Confirma o envio encerrado pelo cliente — só agora o conteúdo passa
    a servir bytes, depois de o armazenamento confirmar o tamanho real
    (`RF-09-16`, `RF-09-17`, design — decisão 1)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    conteudo = _obter_conteudo(sessao_bd, id_do_conteudo)
    conteudo = confirmar_envio(sessao_bd, conteudo, operador=operador, armazenamento=armazenamento)
    sessao_bd.commit()
    return saida_do_conteudo(conteudo)
