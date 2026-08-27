import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from ..aulas.modelo import Aula
from ..autenticacao import ContextoDaSessao, exigir_persona
from ..banco import obter_sessao
from ..bibliografias.regra import consultar_bibliografia_da_missao
from ..conteudos.regra import consultar_conteudos_da_missao
from ..conteudos.rotas import ConteudoSaida, saida_do_conteudo
from ..erros import NaoEncontrado
from ..paginacao import PaginaDeResultado, ParametrosDeListagem, contrato_de_listagem
from ..permissoes import Operacao, exigir_permissao
from ..personas.modelo import Persona
from ..trilhas.modelo import Atividade, Missao
from ..trilhas.rotas import (
    AtividadeSaida,
    BibliografiaPublicaSaida,
    saida_da_atividade,
    saida_da_bibliografia_publica,
)
from ..vitrine.publico import AvatarENickSaida, buscar_avatares_e_nicks
from .modelo import Equipe, IntegranteDaEquipe
from .regra import criar_equipe as _criar_equipe
from .regra import declarar_escolha_da_equipe as _declarar_escolha_da_equipe
from .regra import entrar_na_equipe as _entrar_na_equipe
from .regra import equipes_da_aula as _equipes_da_aula
from .regra import programacao_do_encontro as _programacao_do_encontro
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


def saida_da_equipe(sessao: Session, equipe: Equipe) -> EquipeSaida:
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
        itens=[saida_da_equipe(sessao_bd, equipe) for equipe in equipes], proximo_cursor=None
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
    return saida_da_equipe(sessao_bd, equipe)


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
    return saida_da_equipe(sessao_bd, equipe)


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


class ItemDaProgramacaoSaida(BaseModel):
    atividade: AtividadeSaida
    missao_id: uuid.UUID
    missao_titulo: str
    conteudos: list[ConteudoSaida] = Field(default_factory=list)
    bibliografia: list[BibliografiaPublicaSaida] = Field(default_factory=list)
    corrente: bool


def _saida_do_item_da_programacao(
    sessao_bd: Session,
    atividade: Atividade,
    *,
    ponto_de_apoio_id: uuid.UUID | None,
    atividade_corrente_id: uuid.UUID | None,
) -> ItemDaProgramacaoSaida:
    missao = sessao_bd.get(Missao, atividade.missao_id)
    return ItemDaProgramacaoSaida(
        atividade=saida_da_atividade(atividade),
        missao_id=missao.id,
        missao_titulo=missao.titulo,
        conteudos=[
            saida_do_conteudo(conteudo)
            for conteudo in consultar_conteudos_da_missao(sessao_bd, missao.id)
        ],
        bibliografia=[
            saida_da_bibliografia_publica(
                sessao_bd, bibliografia, ponto_de_apoio_id=ponto_de_apoio_id
            )
            for bibliografia in consultar_bibliografia_da_missao(sessao_bd, missao.id)
        ],
        corrente=atividade.id == atividade_corrente_id,
    )


@roteador.get("/equipes/{id_da_equipe}/missao")
def obter_programacao_do_encontro_rota(
    id_da_equipe: uuid.UUID,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> list[ItemDaProgramacaoSaida]:
    """`RF-04-35`: a programação do encontro da aula da equipe — cada
    atividade presencial declarada nela, com a missão, o conteúdo e a
    bibliografia. A integrância na equipe, a trava de trilha publicada e a
    lista vazia sem programação já são de `programacao_do_encontro`."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    equipe = sessao_bd.get(Equipe, id_da_equipe)
    if equipe is None:
        raise NaoEncontrado(mensagem="Equipe não encontrada.")
    atividades = _programacao_do_encontro(sessao_bd, operador=operador, equipe=equipe)

    ponto_de_apoio_id = None
    if equipe.aula_id is not None:
        aula = sessao_bd.get(Aula, equipe.aula_id)
        ponto_de_apoio_id = aula.ponto_de_apoio_id if aula is not None else None

    return [
        _saida_do_item_da_programacao(
            sessao_bd,
            atividade,
            ponto_de_apoio_id=ponto_de_apoio_id,
            atividade_corrente_id=equipe.atividade_corrente_id,
        )
        for atividade in atividades
    ]


class DeclararEscolhaEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    atividade_id: uuid.UUID


class EscolhaDaEquipeSaida(BaseModel):
    equipe_id: uuid.UUID
    atividade_corrente_id: uuid.UUID


@roteador.post("/equipes/{id_da_equipe}/atividade-corrente")
def declarar_escolha_da_equipe_rota(
    id_da_equipe: uuid.UUID,
    entrada: DeclararEscolhaEntrada,
    contexto: Annotated[
        ContextoDaSessao, Depends(exigir_permissao(Operacao.equipe_que_forma_na_aula, "escreve"))
    ],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> EscolhaDaEquipeSaida:
    """`RF-02-42`, `RF-04-35`: a equipe declara, pelo aparelho, a atividade
    da programação em que está trabalhando — a integrância e o pertencimento
    à programação daquela aula já são de `declarar_escolha_da_equipe`."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    equipe = sessao_bd.get(Equipe, id_da_equipe)
    if equipe is None:
        raise NaoEncontrado(mensagem="Equipe não encontrada.")
    atividade = sessao_bd.get(Atividade, entrada.atividade_id)
    _declarar_escolha_da_equipe(sessao_bd, operador=operador, equipe=equipe, atividade=atividade)
    sessao_bd.commit()
    return EscolhaDaEquipeSaida(
        equipe_id=equipe.id, atividade_corrente_id=equipe.atividade_corrente_id
    )


@roteador.get("/eu/trilhas/{id_da_trilha}/equipe")
def obter_minha_equipe_da_trilha_rota(
    id_da_trilha: uuid.UUID,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> EquipeSaida:
    """A equipe da trilha de que o Guerreiro(a) em sessão integra — só
    consulta, nunca forma nem edita (`RN-05-12`, `RF-05-40`, `RF-05-41`):
    a entrega da criação original em equipe precisa saber qual equipe
    entrega e quem são os integrantes, sem que a App 05 ofereça formá-la."""
    equipe = (
        sessao_bd.query(Equipe)
        .join(IntegranteDaEquipe, IntegranteDaEquipe.equipe_id == Equipe.id)
        .filter(
            Equipe.trilha_id == id_da_trilha,
            IntegranteDaEquipe.persona_id == contexto.persona_id,
        )
        .first()
    )
    if equipe is None:
        raise NaoEncontrado(mensagem="Você não integra nenhuma equipe desta trilha.")
    return saida_da_equipe(sessao_bd, equipe)
