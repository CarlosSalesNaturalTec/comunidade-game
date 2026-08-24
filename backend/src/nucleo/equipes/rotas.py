import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from ..aulas.modelo import Aula
from ..autenticacao import ContextoDaSessao
from ..banco import obter_sessao
from ..erros import NaoEncontrado
from ..paginacao import PaginaDeResultado, ParametrosDeListagem, contrato_de_listagem
from ..permissoes import Operacao, exigir_permissao
from ..personas.modelo import Persona
from ..vitrine.publico import AvatarENickSaida, buscar_avatares_e_nicks
from .modelo import Equipe, IntegranteDaEquipe
from .regra import criar_equipe as _criar_equipe
from .regra import entrar_na_equipe as _entrar_na_equipe
from .regra import equipes_da_aula as _equipes_da_aula
from .regra import sair_da_equipe as _sair_da_equipe

roteador = APIRouter()


class IntegranteSaida(AvatarENickSaida):
    """Avatar e nick, e nada além disso — a restrição é do contrato de
    saída da rota, não do modelo (`RF-04-34`, `RN-04-14`, invariante 11)."""

    papel: str | None


class EquipeSaida(BaseModel):
    id: uuid.UUID
    aula_id: uuid.UUID | None
    integrantes: list[IntegranteSaida]


def _saida_da_equipe(sessao: Session, equipe: Equipe) -> EquipeSaida:
    integrantes = sessao.query(IntegranteDaEquipe).filter_by(equipe_id=equipe.id).all()
    avatares_e_nicks = buscar_avatares_e_nicks(sessao, [i.persona_id for i in integrantes])
    return EquipeSaida(
        id=equipe.id,
        aula_id=equipe.aula_id,
        integrantes=[
            IntegranteSaida(
                avatar=avatares_e_nicks[i.persona_id].avatar,
                nick=avatares_e_nicks[i.persona_id].nick,
                papel=i.papel,
            )
            for i in integrantes
        ],
    )


@roteador.get("/aulas/{id_da_aula}/equipes", response_model=PaginaDeResultado[EquipeSaida])
def listar_equipes_da_aula_rota(
    id_da_aula: uuid.UUID,
    parametros: Annotated[ParametrosDeListagem, Depends(contrato_de_listagem())],
    contexto: Annotated[
        ContextoDaSessao, Depends(exigir_permissao(Operacao.equipes_da_aula_em_andamento, "le"))
    ],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> PaginaDeResultado[EquipeSaida]:
    """`RF-04-33`, `RF-04-34`: as equipes vinculadas àquela aula, cada
    integrante identificado apenas por avatar e nick (`RN-04-14`); aula sem
    equipe devolve conjunto vazio, nunca erro."""
    aula = sessao_bd.get(Aula, id_da_aula)
    if aula is None:
        raise NaoEncontrado(mensagem="Aula não encontrada.")
    equipes = _equipes_da_aula(sessao_bd, aula.id)
    return PaginaDeResultado(
        itens=[_saida_da_equipe(sessao_bd, equipe) for equipe in equipes], proximo_cursor=None
    )


class CriarEquipeEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    papel: str | None = None


@roteador.post("/aulas/{id_da_aula}/equipes", status_code=201)
def criar_equipe_rota(
    id_da_aula: uuid.UUID,
    entrada: CriarEquipeEntrada,
    contexto: Annotated[
        ContextoDaSessao, Depends(exigir_permissao(Operacao.equipe_que_forma_na_aula, "escreve"))
    ],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> EquipeSaida:
    """`RF-04-30`, `RF-04-59`: cria a equipe da aula com o autor como
    primeiro integrante — a restrição ao Guerreiro(a) é de `criar_equipe`,
    sem alteração aqui."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    aula = sessao_bd.get(Aula, id_da_aula)
    if aula is None:
        raise NaoEncontrado(mensagem="Aula não encontrada.")
    equipe = _criar_equipe(
        sessao_bd, operador=operador, aula=aula, trilha=None, papel_do_integrante=entrada.papel
    )
    sessao_bd.commit()
    return _saida_da_equipe(sessao_bd, equipe)


class EntrarNaEquipeEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    papel: str | None = None


@roteador.post("/equipes/{id_da_equipe}/integrantes", status_code=201)
def entrar_na_equipe_rota(
    id_da_equipe: uuid.UUID,
    entrada: EntrarNaEquipeEntrada,
    contexto: Annotated[
        ContextoDaSessao, Depends(exigir_permissao(Operacao.equipe_que_forma_na_aula, "escreve"))
    ],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> EquipeSaida:
    """`RF-04-30`, `RF-04-31`, `RF-04-59`: as recusas de teto, aula
    encerrada e composição já são de `entrar_na_equipe`, reexpostas sem
    alteração."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    equipe = sessao_bd.get(Equipe, id_da_equipe)
    if equipe is None:
        raise NaoEncontrado(mensagem="Equipe não encontrada.")
    _entrar_na_equipe(sessao_bd, operador=operador, equipe=equipe, papel=entrada.papel)
    sessao_bd.commit()
    return _saida_da_equipe(sessao_bd, equipe)


@roteador.delete("/equipes/{id_da_equipe}/integrantes/eu", status_code=204)
def sair_da_equipe_rota(
    id_da_equipe: uuid.UUID,
    contexto: Annotated[
        ContextoDaSessao, Depends(exigir_permissao(Operacao.equipe_que_forma_na_aula, "escreve"))
    ],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> None:
    """`RF-04-30`: quem sai é sempre a persona em sessão — `persona_id` vem
    do contexto, nunca de um identificador do cliente (invariante 15)."""
    equipe = sessao_bd.get(Equipe, id_da_equipe)
    if equipe is None:
        raise NaoEncontrado(mensagem="Equipe não encontrada.")
    operador = sessao_bd.get(Persona, contexto.persona_id)
    _sair_da_equipe(sessao_bd, operador=operador, equipe=equipe, persona_id=contexto.persona_id)
    sessao_bd.commit()
