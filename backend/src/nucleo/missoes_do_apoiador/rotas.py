import uuid
from datetime import date
from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from ..aulas.modelo import Aula
from ..autenticacao import ContextoDaSessao, exigir_persona, persona_opcional
from ..banco import obter_sessao
from ..erros import NaoEncontrado
from ..personas.modelo import Papel, Persona
from ..recursos.modelo import TipoDeRecurso
from ..selos_do_apoiador.modelo import FamiliaDeSelo
from .modelo import MissaoDoApoiador, NivelDeNecessidade, SituacaoDaMissao
from .regra import (
    MissaoDerivada,
    derivar_missoes,
    despublicar_missao,
    missoes_abertas_e_visiveis,
    publicar_missao,
)

roteador = APIRouter()


class MissaoDoApoiadorSaidaPublica(BaseModel):
    id: uuid.UUID
    nivel_de_necessidade: str
    titulo: str
    o_que_se_pede: str
    quantidade: Decimal
    falta: Decimal
    coberto: Decimal
    prazo: date
    selo_nome: str
    selo_familia: str


class MissaoDoApoiadorSaidaAdmin(MissaoDoApoiadorSaidaPublica):
    situacao: str
    vencida: bool


def _saida_publica(derivada: MissaoDerivada) -> MissaoDoApoiadorSaidaPublica:
    missao = derivada.missao
    return MissaoDoApoiadorSaidaPublica(
        id=missao.id,
        nivel_de_necessidade=missao.nivel_de_necessidade.value,
        titulo=missao.titulo,
        o_que_se_pede=missao.o_que_se_pede,
        quantidade=missao.quantidade,
        falta=derivada.falta,
        coberto=derivada.coberto,
        prazo=missao.prazo,
        selo_nome=missao.selo_nome,
        selo_familia=missao.selo_familia.value,
    )


def _saida_admin(derivada: MissaoDerivada) -> MissaoDoApoiadorSaidaAdmin:
    missao = derivada.missao
    return MissaoDoApoiadorSaidaAdmin(
        id=missao.id,
        nivel_de_necessidade=missao.nivel_de_necessidade.value,
        titulo=missao.titulo,
        o_que_se_pede=missao.o_que_se_pede,
        quantidade=missao.quantidade,
        falta=derivada.falta,
        coberto=derivada.coberto,
        prazo=missao.prazo,
        selo_nome=missao.selo_nome,
        selo_familia=missao.selo_familia.value,
        situacao=missao.situacao.value,
        vencida=derivada.vencida,
    )


class PublicarMissaoDoApoiadorEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    aula_id: uuid.UUID
    tipo_de_recurso_id: uuid.UUID
    nivel_de_necessidade: NivelDeNecessidade
    titulo: str = Field(min_length=1)
    o_que_se_pede: str = Field(min_length=1)
    quantidade: Decimal = Field(gt=0)
    prazo: date
    selo_nome: str = Field(min_length=1)
    selo_familia: FamiliaDeSelo


@roteador.post("/missoes-do-apoiador", status_code=201)
def publicar_missao_do_apoiador_rota(
    entrada: PublicarMissaoDoApoiadorEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> MissaoDoApoiadorSaidaAdmin:
    """Restrita ao Admin, a partir de uma necessidade de recurso em aberto
    (`RF-02-102`, `RF-02-103`, `RN-02-31`, `RN-14-31`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    aula = sessao_bd.get(Aula, entrada.aula_id)
    tipo = sessao_bd.get(TipoDeRecurso, entrada.tipo_de_recurso_id)

    missao = publicar_missao(
        sessao_bd,
        operador=operador,
        aula=aula,
        tipo=tipo,
        nivel_de_necessidade=entrada.nivel_de_necessidade,
        titulo=entrada.titulo,
        o_que_se_pede=entrada.o_que_se_pede,
        quantidade=entrada.quantidade,
        prazo=entrada.prazo,
        selo_nome=entrada.selo_nome,
        selo_familia=entrada.selo_familia,
    )
    sessao_bd.commit()
    return _saida_admin(
        MissaoDerivada(
            missao=missao,
            coberto=Decimal("0"),
            falta=missao.quantidade,
            vencida=False,
            tem_necessidade_por_tras=True,
        )
    )


_GRUPOS_VAZIOS: dict[str, list[MissaoDoApoiadorSaidaPublica]] = {
    nivel.value: [] for nivel in NivelDeNecessidade
}


@roteador.get("/missoes-do-apoiador", response_model=None)
def listar_missoes_do_apoiador_rota(
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    contexto: Annotated[ContextoDaSessao | None, Depends(persona_opcional)],
    situacao: SituacaoDaMissao | None = None,
) -> dict[str, list[MissaoDoApoiadorSaidaPublica]] | list[MissaoDoApoiadorSaidaAdmin]:
    """Responde às duas personas pelo mesmo caminho: sem sessão ou com
    sessão que não é de Admin, só as abertas, agrupadas por nível de
    necessidade, sem identificar quem cobriu (`RF-14-60` a `RF-14-62`,
    `RF-14-71`, `RF-14-72`). Com sessão de Admin, qualquer situação — com o
    filtro opcional de `situacao` —, com o coberto e o que falta
    (`RF-02-104`)."""
    if contexto is not None and contexto.papel == Papel.admin:
        derivadas = derivar_missoes(sessao_bd)
        if situacao is not None:
            derivadas = [d for d in derivadas if d.missao.situacao == situacao]
        return [_saida_admin(derivada) for derivada in derivadas]

    agrupadas = {nivel: list(grupo) for nivel, grupo in _GRUPOS_VAZIOS.items()}
    for derivada in missoes_abertas_e_visiveis(sessao_bd):
        agrupadas[derivada.missao.nivel_de_necessidade.value].append(_saida_publica(derivada))
    return agrupadas


@roteador.post("/missoes-do-apoiador/{missao_id}/despublicacao")
def despublicar_missao_do_apoiador_rota(
    missao_id: uuid.UUID,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> MissaoDoApoiadorSaidaAdmin:
    """Restrita ao Admin; não estorna aporte já homologado, e a missão já
    concluída não se despublica (`RF-02-105`, `RN-02-31`, `RN-14-32`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    missao = sessao_bd.get(MissaoDoApoiador, missao_id)
    if missao is None:
        raise NaoEncontrado(mensagem="Missão do Apoiador não encontrada.")

    missao = despublicar_missao(sessao_bd, missao, operador=operador)
    sessao_bd.commit()

    derivadas = derivar_missoes(sessao_bd)
    derivada = next(d for d in derivadas if d.missao.id == missao.id)
    return _saida_admin(derivada)
