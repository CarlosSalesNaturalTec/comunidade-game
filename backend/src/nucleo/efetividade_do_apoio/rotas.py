import uuid
from datetime import date
from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..autenticacao import ContextoDaSessao, exigir_persona
from ..banco import obter_sessao
from ..configuracao import Configuracao, obter_configuracao
from ..erros import PermissaoNegada
from ..personas.modelo import Papel, Persona
from .regra import (
    CoberturaDeOds,
    DesafioDeEfetividade,
    MoedasDeEfetividade,
    PainelDeDesafios,
    PainelDeEfetividade,
    montar_painel_de_efetividade,
)

roteador = APIRouter()


class ConcluinteExibivelSaida(BaseModel):
    avatar: str | None
    nick: str


class DesafioDeEfetividadeSaida(BaseModel):
    id: uuid.UUID
    trilha_id: uuid.UUID
    trilha_nome: str
    modalidade: str
    situacao: str
    etiquetas_ods: list[int]
    quantidade_de_conclusoes: int | None
    primeira_conclusao_em: date | None
    ultima_conclusao_em: date | None
    concluintes_exibiveis: list[ConcluinteExibivelSaida] | None
    concluintes_nao_identificados: int | None
    houve_conclusao: bool | None


class PainelDeDesafiosSaida(BaseModel):
    propostos: list[DesafioDeEfetividadeSaida]
    publicados: list[DesafioDeEfetividadeSaida]
    concluidos: list[DesafioDeEfetividadeSaida]


class AporteDeEfetividadeSaida(BaseModel):
    id: uuid.UUID
    valor_em_moedas: Decimal
    data_do_aporte: date
    custeio_tipo: str
    custeio_descricao: str | None


class MoedasDeEfetividadeSaida(BaseModel):
    total_em_moedas: Decimal
    aportes: list[AporteDeEfetividadeSaida]


class CoberturaPorComunidadeSaida(BaseModel):
    comunidade_virtual_id: uuid.UUID
    comunidade_virtual_nome: str
    ciclo_rotulo: str
    objetivos: list[int]


class CoberturaDeOdsSaida(BaseModel):
    por_comunidade: list[CoberturaPorComunidadeSaida]


class PainelDeEfetividadeSaida(BaseModel):
    desafios: PainelDeDesafiosSaida
    moedas: MoedasDeEfetividadeSaida
    cobertura_de_ods: CoberturaDeOdsSaida


def _saida_do_desafio(desafio: DesafioDeEfetividade) -> DesafioDeEfetividadeSaida:
    return DesafioDeEfetividadeSaida(
        id=desafio.id,
        trilha_id=desafio.trilha_id,
        trilha_nome=desafio.trilha_nome,
        modalidade=desafio.modalidade,
        situacao=desafio.situacao,
        etiquetas_ods=desafio.etiquetas_ods,
        quantidade_de_conclusoes=desafio.quantidade_de_conclusoes,
        primeira_conclusao_em=desafio.primeira_conclusao_em,
        ultima_conclusao_em=desafio.ultima_conclusao_em,
        concluintes_exibiveis=(
            [
                ConcluinteExibivelSaida(avatar=concluinte.avatar, nick=concluinte.nick)
                for concluinte in desafio.concluintes_exibiveis
            ]
            if desafio.concluintes_exibiveis is not None
            else None
        ),
        concluintes_nao_identificados=desafio.concluintes_nao_identificados,
        houve_conclusao=desafio.houve_conclusao,
    )


def _saida_dos_desafios(desafios: PainelDeDesafios) -> PainelDeDesafiosSaida:
    return PainelDeDesafiosSaida(
        propostos=[_saida_do_desafio(desafio) for desafio in desafios.propostos],
        publicados=[_saida_do_desafio(desafio) for desafio in desafios.publicados],
        concluidos=[_saida_do_desafio(desafio) for desafio in desafios.concluidos],
    )


def _saida_das_moedas(moedas: MoedasDeEfetividade) -> MoedasDeEfetividadeSaida:
    return MoedasDeEfetividadeSaida(
        total_em_moedas=moedas.total_em_moedas,
        aportes=[
            AporteDeEfetividadeSaida(
                id=aporte.id,
                valor_em_moedas=aporte.valor_em_moedas,
                data_do_aporte=aporte.data_do_aporte,
                custeio_tipo=aporte.custeio_tipo,
                custeio_descricao=aporte.custeio_descricao,
            )
            for aporte in moedas.aportes
        ],
    )


def _saida_da_cobertura(cobertura: CoberturaDeOds) -> CoberturaDeOdsSaida:
    return CoberturaDeOdsSaida(
        por_comunidade=[
            CoberturaPorComunidadeSaida(
                comunidade_virtual_id=item.comunidade_virtual_id,
                comunidade_virtual_nome=item.comunidade_virtual_nome,
                ciclo_rotulo=item.ciclo_rotulo,
                objetivos=item.objetivos,
            )
            for item in cobertura.por_comunidade
        ]
    )


def _saida(painel: PainelDeEfetividade) -> PainelDeEfetividadeSaida:
    return PainelDeEfetividadeSaida(
        desafios=_saida_dos_desafios(painel.desafios),
        moedas=_saida_das_moedas(painel.moedas),
        cobertura_de_ods=_saida_da_cobertura(painel.cobertura_de_ods),
    )


@roteador.get("/eu/desafios-extras/efetividade")
def painel_de_efetividade_rota(
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    configuracao: Annotated[Configuracao, Depends(obter_configuracao)],
) -> PainelDeEfetividadeSaida:
    """Restrita ao Apoiador em sessão, sempre com os dados de quem está em
    sessão — sem identificador de outro Apoiador no caminho ou em
    parâmetro (`RF-14-40`, `RN-14-20`, PRD-14 §9)."""
    if contexto.papel != Papel.apoiador:
        raise PermissaoNegada(mensagem="Só o Apoiador lê o próprio painel de efetividade.")

    proponente = sessao_bd.get(Persona, contexto.persona_id)
    painel = montar_painel_de_efetividade(
        sessao_bd, proponente=proponente, ciclo_rotulo=configuracao.ciclo_rotulo
    )
    return _saida(painel)
