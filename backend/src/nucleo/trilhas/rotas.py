import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from ..autenticacao import ContextoDaSessao, exigir_persona
from ..banco import obter_sessao
from ..configuracao import Configuracao, obter_configuracao
from ..erros import NaoEncontrado
from ..ods.modelo import EtiquetaOds
from ..ods.regra import cobertura_por_trilha
from ..ods.rotas import EtiquetaOdsSaida, saida_da_etiqueta
from ..personas.modelo import Persona
from .modelo import (
    Atividade,
    EtapaDoCiclo,
    FormatoDeAtividade,
    Missao,
    ModalidadeDeAtividade,
    SituacaoDaTrilha,
    Trilha,
)
from .regra import (
    criar_atividade,
    criar_missao,
    criar_trilha,
    declarar_cadencia_de_retomada,
    despublicar_trilha,
    publicar_trilha,
)

roteador = APIRouter()

# Conteúdo educacional aberto sob licença fixa, decidida no documento 03
# (Estado atual — código aberto e CC BY-SA): não é parâmetro de operação,
# então não entra em `Configuracao`.
LICENCA_DO_CONTEUDO = "CC BY-SA"


class AtividadeSaida(BaseModel):
    id: uuid.UUID
    missao_id: uuid.UUID
    titulo: str
    descricao: str | None
    modalidade: ModalidadeDeAtividade
    formato: FormatoDeAtividade
    natureza: str
    producao_esperada: str


def _saida_da_atividade(atividade: Atividade) -> AtividadeSaida:
    return AtividadeSaida(
        id=atividade.id,
        missao_id=atividade.missao_id,
        titulo=atividade.titulo,
        descricao=atividade.descricao,
        modalidade=atividade.modalidade,
        formato=atividade.formato,
        natureza=atividade.natureza,
        producao_esperada=atividade.producao_esperada,
    )


class MissaoSaida(BaseModel):
    id: uuid.UUID
    trilha_id: uuid.UUID
    titulo: str
    posicao: int
    nivel_de_dificuldade: int
    obrigatoria: bool
    e_sondagem: bool
    etapa_do_ciclo: EtapaDoCiclo
    cadencia_de_retomada: list[int] | None
    atividades: list[AtividadeSaida] = Field(default_factory=list)
    etiquetas_ods: list[EtiquetaOdsSaida] = Field(default_factory=list)


def _etiquetas_da_missao(sessao_bd: Session, missao: Missao) -> list[EtiquetaOds]:
    """As etiquetas **próprias** da missão: a leitura não cai para a da
    trilha: a precedência do `RF-01-45` resolve o vínculo, não a leitura da
    autoria (`RF-09-98`)."""
    return sessao_bd.query(EtiquetaOds).filter_by(missao_id=missao.id).all()


def _saida_da_missao(
    missao: Missao,
    *,
    atividades: list[Atividade] | None = None,
    etiquetas: list[EtiquetaOds] | None = None,
) -> MissaoSaida:
    return MissaoSaida(
        id=missao.id,
        trilha_id=missao.trilha_id,
        titulo=missao.titulo,
        posicao=missao.posicao,
        nivel_de_dificuldade=missao.nivel_de_dificuldade,
        obrigatoria=missao.obrigatoria,
        e_sondagem=missao.e_sondagem,
        etapa_do_ciclo=missao.etapa_do_ciclo,
        cadencia_de_retomada=missao.cadencia_de_retomada,
        atividades=[_saida_da_atividade(atividade) for atividade in (atividades or [])],
        etiquetas_ods=[saida_da_etiqueta(etiqueta) for etiqueta in (etiquetas or [])],
    )


class CoberturaOdsDaTrilhaSaida(BaseModel):
    objetivos: list[int]
    ciclo: str


class TrilhaSaida(BaseModel):
    id: uuid.UUID
    nome: str
    objetivo: str
    area_do_conhecimento: str
    poder_id: uuid.UUID
    situacao: SituacaoDaTrilha
    motivo_da_situacao: str | None
    etiquetas_ods: list[EtiquetaOdsSaida] = Field(default_factory=list)
    cobertura_ods: CoberturaOdsDaTrilhaSaida


def _saida_da_trilha(sessao_bd: Session, trilha: Trilha, *, ciclo: str) -> TrilhaSaida:
    """A trilha sai com as etiquetas declaradas nela e com a cobertura
    resultante — a união dos objetivos dela e das missões dela, agregada por
    trilha e nunca por Guerreiro(a) —, acompanhada do rótulo do ciclo
    (`RF-09-92`, `RF-09-94`, `RF-01-42`, `RN-01-24`, design — decisão 5)."""
    etiquetas = sessao_bd.query(EtiquetaOds).filter_by(trilha_id=trilha.id).all()
    return TrilhaSaida(
        id=trilha.id,
        nome=trilha.nome,
        objetivo=trilha.objetivo,
        area_do_conhecimento=trilha.area_do_conhecimento,
        poder_id=trilha.poder_id,
        situacao=trilha.situacao,
        motivo_da_situacao=trilha.motivo_da_situacao,
        etiquetas_ods=[saida_da_etiqueta(etiqueta) for etiqueta in etiquetas],
        cobertura_ods=CoberturaOdsDaTrilhaSaida(
            objetivos=sorted(cobertura_por_trilha(sessao_bd, trilha.id)),
            ciclo=ciclo,
        ),
    )


class TrilhaComMissoesSaida(TrilhaSaida):
    missoes: list[MissaoSaida] = Field(default_factory=list)


def _saida_da_trilha_com_missoes(
    sessao_bd: Session, trilha: Trilha, *, missoes: list[MissaoSaida], ciclo: str
) -> TrilhaComMissoesSaida:
    return TrilhaComMissoesSaida(
        **_saida_da_trilha(sessao_bd, trilha, ciclo=ciclo).model_dump(), missoes=missoes
    )


def _obter_trilha(sessao_bd: Session, id_da_trilha: uuid.UUID) -> Trilha:
    trilha = sessao_bd.get(Trilha, id_da_trilha)
    if trilha is None:
        raise NaoEncontrado(mensagem="Trilha não encontrada.")
    return trilha


def _obter_missao(sessao_bd: Session, id_da_missao: uuid.UUID) -> Missao:
    missao = sessao_bd.get(Missao, id_da_missao)
    if missao is None:
        raise NaoEncontrado(mensagem="Missão não encontrada.")
    return missao


class CriarTrilhaEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nome: str
    objetivo: str
    area_do_conhecimento: str
    poder_id: uuid.UUID | None = None


@roteador.post("/trilhas", status_code=201)
def criar_trilha_rota(
    entrada: CriarTrilhaEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    configuracao: Annotated[Configuracao, Depends(obter_configuracao)],
) -> TrilhaSaida:
    """`RF-09-01`: nasce em rascunho, com o Mestre em sessão como autor — a
    recusa a poder fora da natureza de Guerreiro(a) já é de `criar_trilha`,
    que a porta apenas reexpõe (design — decisão 1)."""
    autor = sessao_bd.get(Persona, contexto.persona_id)
    trilha = criar_trilha(
        sessao_bd,
        autor=autor,
        nome=entrada.nome,
        objetivo=entrada.objetivo,
        area_do_conhecimento=entrada.area_do_conhecimento,
        poder_id=entrada.poder_id,
    )
    sessao_bd.commit()
    return _saida_da_trilha(sessao_bd, trilha, ciclo=configuracao.ciclo_rotulo)


@roteador.get("/trilhas/minhas")
def listar_minhas_trilhas_rota(
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    configuracao: Annotated[Configuracao, Depends(obter_configuracao)],
) -> list[TrilhaComMissoesSaida]:
    """`RF-09-04`: as trilhas de que a persona em sessão é autora, rascunho
    incluso, com as missões na ordem da posição e as atividades de cada
    missão aninhadas na mesma resposta — o PRD-09 §9 não declara rota
    própria para nenhuma das duas (design — decisão 2). Bem comum da
    plataforma: sem filtro de comunidade (`RN-01-42`)."""
    persona = sessao_bd.get(Persona, contexto.persona_id)
    trilhas = sessao_bd.query(Trilha).filter_by(autor_id=persona.id).all()

    saida = []
    for trilha in trilhas:
        missoes = (
            sessao_bd.query(Missao).filter_by(trilha_id=trilha.id).order_by(Missao.posicao).all()
        )
        missoes_saida = []
        for missao in missoes:
            atividades = sessao_bd.query(Atividade).filter_by(missao_id=missao.id).all()
            missoes_saida.append(
                _saida_da_missao(
                    missao,
                    atividades=atividades,
                    etiquetas=_etiquetas_da_missao(sessao_bd, missao),
                )
            )
        saida.append(
            _saida_da_trilha_com_missoes(
                sessao_bd, trilha, missoes=missoes_saida, ciclo=configuracao.ciclo_rotulo
            )
        )
    return saida


class CriarMissaoEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    titulo: str | None = None
    posicao: int
    nivel_de_dificuldade: int
    obrigatoria: bool | None = None
    etapa_do_ciclo: str | None = None
    e_sondagem: bool = False


@roteador.post("/trilhas/{id_da_trilha}/missoes", status_code=201)
def criar_missao_rota(
    id_da_trilha: uuid.UUID,
    entrada: CriarMissaoEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> MissaoSaida:
    """`RF-09-02`, `RF-09-03`, `RF-09-80`, `RF-09-81`: a posse do Mestre
    autor e as recusas de título, obrigatoriedade, etapa e sondagem já são
    de `criar_missao` (design — decisão 1)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    trilha = _obter_trilha(sessao_bd, id_da_trilha)
    missao = criar_missao(
        sessao_bd,
        operador=operador,
        trilha=trilha,
        titulo=entrada.titulo,
        posicao=entrada.posicao,
        nivel_de_dificuldade=entrada.nivel_de_dificuldade,
        obrigatoria=entrada.obrigatoria,
        etapa_do_ciclo=entrada.etapa_do_ciclo,
        e_sondagem=entrada.e_sondagem,
    )
    sessao_bd.commit()
    return _saida_da_missao(missao, etiquetas=_etiquetas_da_missao(sessao_bd, missao))


class CriarAtividadeEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    titulo: str | None = None
    descricao: str | None = None
    modalidade: str | None = None
    formato: str | None = None
    natureza: str | None = None
    producao_esperada: str | None = None


@roteador.post("/missoes/{id_da_missao}/atividades", status_code=201)
def criar_atividade_rota(
    id_da_missao: uuid.UUID,
    entrada: CriarAtividadeEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> AtividadeSaida:
    """`RF-09-69`, `RF-09-70`: a posse do Mestre autor da trilha e as
    recusas de título, modalidade e formato já são de `criar_atividade`
    (design — decisão 1)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    missao = _obter_missao(sessao_bd, id_da_missao)
    atividade = criar_atividade(
        sessao_bd,
        operador=operador,
        missao=missao,
        titulo=entrada.titulo,
        descricao=entrada.descricao,
        modalidade=entrada.modalidade,
        formato=entrada.formato,
        natureza=entrada.natureza,
        producao_esperada=entrada.producao_esperada,
    )
    sessao_bd.commit()
    return _saida_da_atividade(atividade)


class DeclararCadenciaDeRetomadaEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    cadencia_de_retomada: list[int] | None = None


@roteador.post("/missoes/{id_da_missao}/retomada")
def declarar_cadencia_de_retomada_rota(
    id_da_missao: uuid.UUID,
    entrada: DeclararCadenciaDeRetomadaEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> MissaoSaida:
    """`RF-09-83`, `RF-09-101`: a cadência é sempre a que o Mestre autor
    declara; declarar de novo substitui a anterior, e `null` deixa a missão
    sem retomada (design — decisão 4)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    missao = _obter_missao(sessao_bd, id_da_missao)
    missao = declarar_cadencia_de_retomada(
        sessao_bd,
        operador=operador,
        missao=missao,
        cadencia_de_retomada=entrada.cadencia_de_retomada,
    )
    sessao_bd.commit()
    return _saida_da_missao(missao, etiquetas=_etiquetas_da_missao(sessao_bd, missao))


@roteador.post("/trilhas/{id_da_trilha}/publicacao")
def publicar_trilha_rota(
    id_da_trilha: uuid.UUID,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    configuracao: Annotated[Configuracao, Depends(obter_configuracao)],
) -> TrilhaSaida:
    """`RF-09-05` a `RF-09-09`, `RF-09-82`: publica ou republica a pedido do
    Mestre autor, sem aprovação — a posse estrita, as três travas e a
    recusa nomeando todas as pendentes já são de `publicar_trilha` (design —
    decisões 4, 5, 6, 7)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    trilha = sessao_bd.get(Trilha, id_da_trilha)
    trilha = publicar_trilha(sessao_bd, trilha, operador=operador)
    sessao_bd.commit()
    return _saida_da_trilha(sessao_bd, trilha, ciclo=configuracao.ciclo_rotulo)


class DespublicarTrilhaEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    motivo: str = Field(min_length=1)


@roteador.post("/trilhas/{id_da_trilha}/despublicacao")
def despublicar_trilha_rota(
    id_da_trilha: uuid.UUID,
    entrada: DespublicarTrilhaEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    configuracao: Annotated[Configuracao, Depends(obter_configuracao)],
) -> TrilhaSaida:
    """`RF-09-10`, `RF-09-11`: só Admin, sempre com motivo — a recusa de
    Mestre e a exigência do motivo já são de `despublicar_trilha`."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    trilha = sessao_bd.get(Trilha, id_da_trilha)
    trilha = despublicar_trilha(sessao_bd, trilha, operador=operador, motivo=entrada.motivo)
    sessao_bd.commit()
    return _saida_da_trilha(sessao_bd, trilha, ciclo=configuracao.ciclo_rotulo)


class TrilhaPublicaSaida(TrilhaComMissoesSaida):
    licenca: str
    autor_nome: str | None


@roteador.get("/trilhas/{id_da_trilha}")
def obter_trilha_publica_rota(
    id_da_trilha: uuid.UUID,
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    configuracao: Annotated[Configuracao, Depends(obter_configuracao)],
) -> TrilhaPublicaSaida:
    """`RF-09-09`, `RN-09-05`: pública, sem persona em sessão — só serve
    trilha publicada; rascunho e despublicada respondem como não
    encontrada, para não vazar a existência de rascunho alheio (`RF-09-04`,
    design — decisões 8). Destrava o consumo pela App 05 e pela App 01."""
    trilha = sessao_bd.get(Trilha, id_da_trilha)
    if trilha is None or trilha.situacao != SituacaoDaTrilha.publicada:
        raise NaoEncontrado(mensagem="Trilha não encontrada.")

    autor = sessao_bd.get(Persona, trilha.autor_id)
    missoes = sessao_bd.query(Missao).filter_by(trilha_id=trilha.id).order_by(Missao.posicao).all()
    missoes_saida = []
    for missao in missoes:
        atividades = sessao_bd.query(Atividade).filter_by(missao_id=missao.id).all()
        missoes_saida.append(
            _saida_da_missao(
                missao, atividades=atividades, etiquetas=_etiquetas_da_missao(sessao_bd, missao)
            )
        )

    return TrilhaPublicaSaida(
        **_saida_da_trilha_com_missoes(
            sessao_bd, trilha, missoes=missoes_saida, ciclo=configuracao.ciclo_rotulo
        ).model_dump(),
        licenca=LICENCA_DO_CONTEUDO,
        autor_nome=autor.nome if autor is not None else None,
    )
