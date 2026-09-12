import uuid
from datetime import date, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Response
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from ..armazenamento.fabrica import dependencia_de_armazenamento
from ..armazenamento.porta import PortaDeArmazenamento
from ..autenticacao import ContextoDaSessao, exigir_persona
from ..banco import obter_sessao
from ..bibliografias.modelo import BibliografiaDaMissao
from ..bibliografias.regra import consultar_bibliografia_da_missao, ler_disponibilidade_e_credito
from ..coletas.modelo import DesafioDeColeta
from ..configuracao import Configuracao, obter_configuracao
from ..conteudos.modelo import ConteudoDaMissao
from ..conteudos.regra import consultar_conteudos_da_missao
from ..conteudos.rotas import ConteudoSaida, saida_do_conteudo
from ..culminancias.modelo import Culminancia
from ..culminancias.rotas import CulminanciaSaida, saida_da_culminancia
from ..desafios_extras.modelo import DesafioExtra
from ..desafios_extras.regra import desafios_extras_elegiveis_do_guerreiro
from ..desafios_extras.regra import quantidade_restante as calcular_quantidade_restante_do_extra
from ..erros import NaoEncontrado, PermissaoNegada
from ..ods.modelo import EtiquetaOds
from ..ods.regra import cobertura_por_trilha
from ..ods.rotas import EtiquetaOdsSaida, saida_da_etiqueta
from ..personas.modelo import Papel, Persona
from ..pontos_de_apoio.modelo import PontoDeApoio
from ..recursos.modelo import TipoDeRecurso
from ..tempo import agora
from .modelo import (
    Atividade,
    DesbloqueioDaMissao,
    EtapaDoCiclo,
    FormatoDeAtividade,
    Missao,
    ModalidadeDeAtividade,
    PerguntaDoDesbloqueio,
    SituacaoDaTrilha,
    TipoDeDesafioDeDesbloqueio,
    Trilha,
)
from .regra import (
    abrir_envio_da_imagem_da_pergunta,
    confirmar_envio_da_imagem_da_pergunta,
    consultar_inscricoes_do_guerreiro,
    consultar_progresso,
    criar_atividade,
    criar_missao,
    criar_trilha,
    declarar_cadencia_de_retomada,
    declarar_desafio_de_desbloqueio,
    derivar_percurso,
    desafios_em_aberto_do_guerreiro,
    despublicar_trilha,
    duplicar_trilha,
    inscrever_na_trilha,
    julgar_desafio_pratico,
    ler_imagem_da_pergunta,
    listar_desbloqueios_praticos_pendentes,
    obter_proxima_missao,
    perguntas_do_desbloqueio,
    perguntas_do_desbloqueio_por_missao,
    publicar_trilha,
    retomadas_em_aberto_do_guerreiro,
    submeter_desafio_de_desbloqueio,
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
    aula_id: uuid.UUID | None


def saida_da_atividade(atividade: Atividade) -> AtividadeSaida:
    return AtividadeSaida(
        id=atividade.id,
        missao_id=atividade.missao_id,
        titulo=atividade.titulo,
        descricao=atividade.descricao,
        modalidade=atividade.modalidade,
        formato=atividade.formato,
        natureza=atividade.natureza,
        producao_esperada=atividade.producao_esperada,
        aula_id=atividade.aula_id,
    )


class BibliografiaPublicaSaida(BaseModel):
    id: uuid.UUID
    missao_id: uuid.UUID
    titulo: str
    capitulo: str
    disponivel: bool | None
    apoiador_nome: str | None


def saida_da_bibliografia_publica(
    sessao_bd: Session, bibliografia: BibliografiaDaMissao, *, ponto_de_apoio_id: uuid.UUID | None
) -> BibliografiaPublicaSaida:
    disponivel, apoiador = ler_disponibilidade_e_credito(
        sessao_bd, bibliografia, ponto_de_apoio_id=ponto_de_apoio_id
    )
    return BibliografiaPublicaSaida(
        id=bibliografia.id,
        missao_id=bibliografia.missao_id,
        titulo=bibliografia.titulo,
        capitulo=bibliografia.capitulo,
        disponivel=disponivel,
        apoiador_nome=apoiador.nome if apoiador is not None else None,
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
    conteudos: list[ConteudoSaida] = Field(default_factory=list)
    bibliografia: list[BibliografiaPublicaSaida] = Field(default_factory=list)


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
    conteudos: list[ConteudoDaMissao] | None = None,
    bibliografia: list[BibliografiaPublicaSaida] | None = None,
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
        atividades=[saida_da_atividade(atividade) for atividade in (atividades or [])],
        etiquetas_ods=[saida_da_etiqueta(etiqueta) for etiqueta in (etiquetas or [])],
        conteudos=[saida_do_conteudo(conteudo) for conteudo in (conteudos or [])],
        bibliografia=bibliografia or [],
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


class DesafioDeColetaDaMissaoSaida(BaseModel):
    id: uuid.UUID
    tipo_de_coleta_id: uuid.UUID
    cadencia: str
    vigencia_inicio: datetime
    vigencia_fim: datetime
    granularidade_exigida: str
    registros_que_pontuam_por_periodo: int


def _desafios_de_coleta_da_missao(
    sessao_bd: Session, missao: Missao
) -> list[DesafioDeColetaDaMissaoSaida]:
    """Só para `GET /v1/trilhas/minhas`: a leitura do Mestre autor, inclusive
    em rascunho — a mesma trilha própria em que atividades e etiquetas ODS já
    vêm aninhadas (`RF-09-27`, `RF-09-28`, `RF-09-04`, design — decisão 1)."""
    desafios = sessao_bd.query(DesafioDeColeta).filter_by(missao_id=missao.id).all()
    return [
        DesafioDeColetaDaMissaoSaida(
            id=desafio.id,
            tipo_de_coleta_id=desafio.tipo_de_coleta_id,
            cadencia=desafio.cadencia.value,
            vigencia_inicio=desafio.vigencia_inicio,
            vigencia_fim=desafio.vigencia_fim,
            granularidade_exigida=desafio.granularidade_exigida.value,
            registros_que_pontuam_por_periodo=desafio.registros_que_pontuam_por_periodo,
        )
        for desafio in desafios
    ]


class PerguntaDoDesbloqueioSaida(BaseModel):
    """A pergunta como o Guerreiro(a) a vê: **sem** a alternativa correta,
    que nunca sai do núcleo para ele (`RF-09-118`, design — decisão 6).
    `imagem_referencia` diz apenas **se** a pergunta tem imagem — os bytes
    vêm da rota própria, que confere quem pede (`RF-09-119`)."""

    id: uuid.UUID
    ordem: int
    enunciado: str
    alternativas: list[str]
    imagem_referencia: str | None = None


class PerguntaDoDesbloqueioAoAutorSaida(PerguntaDoDesbloqueioSaida):
    """Só ao Mestre autor, e só nesta rota: a pergunta com a alternativa
    correta."""

    alternativa_correta: int


def _saida_das_perguntas(
    perguntas: list[PerguntaDoDesbloqueio],
) -> list[PerguntaDoDesbloqueioSaida]:
    return [
        PerguntaDoDesbloqueioSaida(
            id=pergunta.id,
            ordem=pergunta.ordem,
            enunciado=pergunta.enunciado,
            alternativas=[
                pergunta.alternativa_1,
                pergunta.alternativa_2,
                pergunta.alternativa_3,
                pergunta.alternativa_4,
            ],
            imagem_referencia=pergunta.imagem_referencia,
        )
        for pergunta in perguntas
    ]


def _saida_das_perguntas_ao_autor(
    perguntas: list[PerguntaDoDesbloqueio],
) -> list[PerguntaDoDesbloqueioAoAutorSaida]:
    """A mesma pergunta, com a alternativa correta: só ao Mestre autor. A
    declaração e a leitura das trilhas próprias usam esta forma única, para
    que a App 09 alimente o mesmo formulário com as duas (design —
    decisão 2)."""
    return [
        PerguntaDoDesbloqueioAoAutorSaida(
            **saida.model_dump(), alternativa_correta=pergunta.alternativa_correta
        )
        for saida, pergunta in zip(_saida_das_perguntas(perguntas), perguntas, strict=True)
    ]


class MissaoDoMestreSaida(MissaoSaida):
    """Só a saída de `GET /v1/trilhas/minhas` traz o desafio de coleta e o
    desafio de desbloqueio aninhados — a trilha pública e as demais rotas de
    missão continuam em `MissaoSaida` (design — decisão 1).

    O desafio de desbloqueio vem aqui com a **alternativa correta** e a
    referência da imagem de cada pergunta porque esta rota é exclusiva do
    Mestre autor: é ela que lhe permite reabrir e corrigir o que declarou,
    sem reenviar arquivo nem reescrever o quiz (`RF-09-26`, `RF-09-118`,
    `RF-09-119`). `tipo_do_desafio_de_desbloqueio` nulo é missão **sem**
    desafio declarado."""

    desafios_de_coleta: list[DesafioDeColetaDaMissaoSaida] = Field(default_factory=list)
    tipo_do_desafio_de_desbloqueio: TipoDeDesafioDeDesbloqueio | None = None
    desafio_de_desbloqueio_enunciado: str | None = None
    perguntas_do_desbloqueio: list[PerguntaDoDesbloqueioAoAutorSaida] = Field(default_factory=list)


class TrilhaDoMestreSaida(TrilhaSaida):
    missoes: list[MissaoDoMestreSaida] = Field(default_factory=list)


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


@roteador.post("/trilhas/{id_da_trilha}/duplicacao", status_code=201)
def duplicar_trilha_rota(
    id_da_trilha: uuid.UUID,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    configuracao: Annotated[Configuracao, Depends(obter_configuracao)],
) -> TrilhaSaida:
    """`RF-09-13`: o Mestre duplica uma trilha do catálogo como ponto de
    partida de outra, em rascunho e sob a própria autoria — a recusa de
    rascunho alheio e de quem não é Mestre já são de `duplicar_trilha`."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    trilha_de_origem = sessao_bd.get(Trilha, id_da_trilha)
    copia = duplicar_trilha(sessao_bd, trilha_de_origem, operador=operador)
    sessao_bd.commit()
    return _saida_da_trilha(sessao_bd, copia, ciclo=configuracao.ciclo_rotulo)


@roteador.get("/trilhas/minhas")
def listar_minhas_trilhas_rota(
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    configuracao: Annotated[Configuracao, Depends(obter_configuracao)],
) -> list[TrilhaDoMestreSaida]:
    """`RF-09-04`: as trilhas de que a persona em sessão é autora, rascunho
    incluso, com as missões na ordem da posição e as atividades de cada
    missão aninhadas na mesma resposta — o PRD-09 §9 não declara rota
    própria para nenhuma das duas (design — decisão 2). Bem comum da
    plataforma: sem filtro de comunidade (`RN-01-42`). Cada missão traz
    também os desafios de coleta já declarados nela (`RF-09-27`, `RF-09-28`,
    design — decisão 1) e o **desafio de desbloqueio**, com a alternativa
    correta e a referência da imagem de cada pergunta: é por esta leitura
    que o Mestre autor reabre e corrige o que declarou (`RF-09-26`,
    `RF-09-118`, `RF-09-119`)."""
    persona = sessao_bd.get(Persona, contexto.persona_id)
    trilhas = sessao_bd.query(Trilha).filter_by(autor_id=persona.id).all()

    saida = []
    for trilha in trilhas:
        missoes = (
            sessao_bd.query(Missao).filter_by(trilha_id=trilha.id).order_by(Missao.posicao).all()
        )
        perguntas_por_missao = perguntas_do_desbloqueio_por_missao(
            sessao_bd, missao_ids=[missao.id for missao in missoes]
        )
        missoes_saida = []
        for missao in missoes:
            atividades = sessao_bd.query(Atividade).filter_by(missao_id=missao.id).all()
            missoes_saida.append(
                MissaoDoMestreSaida(
                    **_saida_da_missao(
                        missao,
                        atividades=atividades,
                        etiquetas=_etiquetas_da_missao(sessao_bd, missao),
                    ).model_dump(),
                    desafios_de_coleta=_desafios_de_coleta_da_missao(sessao_bd, missao),
                    tipo_do_desafio_de_desbloqueio=missao.tipo_do_desafio_de_desbloqueio,
                    desafio_de_desbloqueio_enunciado=missao.desafio_de_desbloqueio_enunciado,
                    perguntas_do_desbloqueio=_saida_das_perguntas_ao_autor(
                        perguntas_por_missao.get(missao.id, [])
                    ),
                )
            )
        saida.append(
            TrilhaDoMestreSaida(
                **_saida_da_trilha(sessao_bd, trilha, ciclo=configuracao.ciclo_rotulo).model_dump(),
                missoes=missoes_saida,
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
    aula_id: uuid.UUID | None = None


@roteador.post("/missoes/{id_da_missao}/atividades", status_code=201)
def criar_atividade_rota(
    id_da_missao: uuid.UUID,
    entrada: CriarAtividadeEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> AtividadeSaida:
    """`RF-09-69`, `RF-09-70`, `RF-09-73`: a posse do Mestre autor da
    trilha, as recusas de título, modalidade e formato, e as do vínculo com
    a aula do encontro já são de `criar_atividade` (design — decisão 1)."""
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
        aula_id=entrada.aula_id,
    )
    sessao_bd.commit()
    return saida_da_atividade(atividade)


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
    # `None` é "esta trilha ainda não declarou culminância" — a App 05
    # exibe isso em linguagem simples e não oferece a entrega da criação
    # original enquanto durar (`RF-05-39`).
    culminancia: CulminanciaSaida | None


@roteador.get("/trilhas/{id_da_trilha}")
def obter_trilha_publica_rota(
    id_da_trilha: uuid.UUID,
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    configuracao: Annotated[Configuracao, Depends(obter_configuracao)],
    ponto_de_apoio_id: uuid.UUID | None = None,
) -> TrilhaPublicaSaida:
    """`RF-09-09`, `RN-09-05`: pública, sem persona em sessão — só serve
    trilha publicada; rascunho e despublicada respondem como não
    encontrada, para não vazar a existência de rascunho alheio (`RF-09-04`,
    design — decisões 8). Destrava o consumo pela App 05 e pela App 01.

    `ponto_de_apoio_id` é opcional e só orienta a disponibilidade da
    bibliografia vinculada (`RF-09-22`): sem ele, a disponibilidade
    permanece indeterminada — nunca afirmada nem negada por suposição."""
    trilha = sessao_bd.get(Trilha, id_da_trilha)
    if trilha is None or trilha.situacao != SituacaoDaTrilha.publicada:
        raise NaoEncontrado(mensagem="Trilha não encontrada.")

    autor = sessao_bd.get(Persona, trilha.autor_id)
    missoes = sessao_bd.query(Missao).filter_by(trilha_id=trilha.id).order_by(Missao.posicao).all()
    missoes_saida = []
    for missao in missoes:
        atividades = sessao_bd.query(Atividade).filter_by(missao_id=missao.id).all()
        bibliografias = consultar_bibliografia_da_missao(sessao_bd, missao.id)
        missoes_saida.append(
            _saida_da_missao(
                missao,
                atividades=atividades,
                etiquetas=_etiquetas_da_missao(sessao_bd, missao),
                conteudos=consultar_conteudos_da_missao(sessao_bd, missao.id),
                bibliografia=[
                    saida_da_bibliografia_publica(
                        sessao_bd, bibliografia, ponto_de_apoio_id=ponto_de_apoio_id
                    )
                    for bibliografia in bibliografias
                ],
            )
        )

    culminancia = sessao_bd.query(Culminancia).filter_by(trilha_id=trilha.id).first()

    return TrilhaPublicaSaida(
        **_saida_da_trilha_com_missoes(
            sessao_bd, trilha, missoes=missoes_saida, ciclo=configuracao.ciclo_rotulo
        ).model_dump(),
        licenca=LICENCA_DO_CONTEUDO,
        autor_nome=autor.nome if autor is not None else None,
        culminancia=saida_da_culminancia(culminancia) if culminancia is not None else None,
    )


def _exigir_guerreiro(contexto: ContextoDaSessao) -> None:
    if contexto.papel != Papel.guerreiro:
        raise PermissaoNegada(mensagem="Só o Guerreiro(a) executa esta operação.")


class InscricaoSaida(BaseModel):
    id: uuid.UUID
    trilha_id: uuid.UUID
    momento: str


@roteador.post("/eu/trilhas/{id_da_trilha}/inscricao", status_code=201)
def inscrever_na_trilha_rota(
    id_da_trilha: uuid.UUID,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> InscricaoSaida:
    """`RF-05-09`: ato do próprio Guerreiro(a) em sessão — a exigência de
    trilha publicada e a devolução da inscrição já existente são de
    `inscrever_na_trilha` (design — decisão 1)."""
    _exigir_guerreiro(contexto)
    guerreiro = sessao_bd.get(Persona, contexto.persona_id)
    trilha = sessao_bd.get(Trilha, id_da_trilha)
    inscricao = inscrever_na_trilha(sessao_bd, guerreiro=guerreiro, trilha=trilha)
    sessao_bd.commit()
    return InscricaoSaida(
        id=inscricao.id, trilha_id=inscricao.trilha_id, momento=inscricao.momento.isoformat()
    )


class TrilhaComProximaMissaoSaida(BaseModel):
    id: uuid.UUID
    nome: str
    poder_id: uuid.UUID
    proxima_missao_id: uuid.UUID | None
    proxima_missao_titulo: str | None
    proxima_missao_posicao: int | None


@roteador.get("/eu/trilhas")
def listar_minhas_trilhas_do_guerreiro_rota(
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> list[TrilhaComProximaMissaoSaida]:
    """`RF-05-08`, `RF-05-17`, `RN-05-21`: as trilhas em que o Guerreiro(a)
    em sessão está inscrito, cada uma com a próxima missão do percurso dele
    — nunca inscrição de terceiro, porque não há outro identificador senão
    o da própria sessão."""
    _exigir_guerreiro(contexto)
    saida = []
    for inscricao in consultar_inscricoes_do_guerreiro(sessao_bd, guerreiro_id=contexto.persona_id):
        trilha = sessao_bd.get(Trilha, inscricao.trilha_id)
        proxima = obter_proxima_missao(
            sessao_bd, guerreiro_id=contexto.persona_id, trilha_id=trilha.id
        )
        saida.append(
            TrilhaComProximaMissaoSaida(
                id=trilha.id,
                nome=trilha.nome,
                poder_id=trilha.poder_id,
                proxima_missao_id=proxima.id if proxima is not None else None,
                proxima_missao_titulo=proxima.titulo if proxima is not None else None,
                proxima_missao_posicao=proxima.posicao if proxima is not None else None,
            )
        )
    return saida


class DesafioDeDesbloqueioSaida(BaseModel):
    tipo: TipoDeDesafioDeDesbloqueio
    enunciado: str | None = None
    perguntas: list[PerguntaDoDesbloqueioSaida] | None = None


class MissaoNoPercursoSaida(BaseModel):
    id: uuid.UUID
    titulo: str
    posicao: int
    obrigatoria: bool
    e_sondagem: bool
    desbloqueada: bool
    e_proxima: bool
    aguardando_mestre: bool
    motivo_do_bloqueio: str | None
    desafio_de_desbloqueio: DesafioDeDesbloqueioSaida | None


def _saida_do_desafio_de_desbloqueio(
    sessao: Session, missao: Missao
) -> DesafioDeDesbloqueioSaida | None:
    if missao.tipo_do_desafio_de_desbloqueio is None:
        return None
    perguntas = None
    if missao.tipo_do_desafio_de_desbloqueio == TipoDeDesafioDeDesbloqueio.quiz:
        perguntas = _saida_das_perguntas(perguntas_do_desbloqueio(sessao, missao_id=missao.id))
    return DesafioDeDesbloqueioSaida(
        tipo=missao.tipo_do_desafio_de_desbloqueio,
        enunciado=missao.desafio_de_desbloqueio_enunciado,
        perguntas=perguntas,
    )


@roteador.get("/eu/trilhas/{id_da_trilha}/missoes/{ordem}")
def obter_missao_no_percurso_rota(
    id_da_trilha: uuid.UUID,
    ordem: int,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> MissaoNoPercursoSaida:
    """`RF-05-08`, `RF-05-10`, `RN-05-21`: o estado da missão no percurso do
    Guerreiro(a) em sessão — desbloqueada, próxima, bloqueada com motivo ou
    aguardando o Mestre. O conteúdo e a bibliografia continuam vindo de
    `GET /v1/trilhas/{id}` (design — decisão 6); `ordem` é a posição da
    missão na trilha."""
    _exigir_guerreiro(contexto)
    percurso = derivar_percurso(sessao_bd, guerreiro_id=contexto.persona_id, trilha_id=id_da_trilha)
    item = next((item for item in percurso if item.missao.posicao == ordem), None)
    if item is None:
        raise NaoEncontrado(mensagem="Missão não encontrada nesta posição da trilha.")
    return MissaoNoPercursoSaida(
        id=item.missao.id,
        titulo=item.missao.titulo,
        posicao=item.missao.posicao,
        obrigatoria=item.missao.obrigatoria,
        e_sondagem=item.missao.e_sondagem,
        desbloqueada=item.desbloqueada,
        e_proxima=item.e_proxima,
        aguardando_mestre=item.aguardando_mestre,
        motivo_do_bloqueio=item.motivo_do_bloqueio,
        desafio_de_desbloqueio=_saida_do_desafio_de_desbloqueio(sessao_bd, item.missao),
    )


class PerguntaDoDesbloqueioEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    enunciado: str
    alternativas: list[str]
    alternativa_correta: int
    # A referência que volta conserva a imagem; omiti-la a remove. A
    # conferência contra as imagens daquela missão é da regra
    # (`RF-09-119`, design — decisão 3).
    imagem_referencia: str | None = None


class DeclararDesafioDeDesbloqueioEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tipo: str
    # O quiz traz `perguntas`, uma ou mais; o prático traz `enunciado`
    # (`RF-09-118`, design — decisões 2 e 6). A recusa de cada caso é da
    # regra, não do schema, para que a mensagem chegue ao Mestre por campo.
    enunciado: str | None = None
    perguntas: list[PerguntaDoDesbloqueioEntrada] | None = None


class MissaoComDesafioDeDesbloqueioSaida(MissaoSaida):
    """Só a resposta desta rota traz o desafio inteiro, alternativa correta
    inclusa — nunca `MissaoSaida` das rotas públicas ou de leitura geral,
    para que a resposta certa não vaze ao Guerreiro(a) (design — decisão 4).
    """

    tipo_do_desafio_de_desbloqueio: TipoDeDesafioDeDesbloqueio
    desafio_de_desbloqueio_enunciado: str | None
    perguntas_do_desbloqueio: list[PerguntaDoDesbloqueioAoAutorSaida]


@roteador.post("/missoes/{id_da_missao}/desbloqueio")
def declarar_desafio_de_desbloqueio_rota(
    id_da_missao: uuid.UUID,
    entrada: DeclararDesafioDeDesbloqueioEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> MissaoComDesafioDeDesbloqueioSaida:
    """`RF-09-26`, `RF-09-117`: o Mestre autor declara o desafio de
    desbloqueio, na forma de quiz ou de desafio prático — a posse e as
    recusas de enunciado, alternativas e alternativa correta já são de
    `declarar_desafio_de_desbloqueio` (design — decisão 4). Só esta
    resposta, ao próprio Mestre autor, traz a alternativa correta."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    missao = _obter_missao(sessao_bd, id_da_missao)
    missao = declarar_desafio_de_desbloqueio(
        sessao_bd,
        operador=operador,
        missao=missao,
        tipo=entrada.tipo,
        enunciado=entrada.enunciado,
        perguntas=[pergunta.model_dump() for pergunta in entrada.perguntas]
        if entrada.perguntas is not None
        else None,
    )
    sessao_bd.commit()
    perguntas = perguntas_do_desbloqueio(sessao_bd, missao_id=missao.id)
    return MissaoComDesafioDeDesbloqueioSaida(
        **_saida_da_missao(missao, etiquetas=_etiquetas_da_missao(sessao_bd, missao)).model_dump(),
        tipo_do_desafio_de_desbloqueio=missao.tipo_do_desafio_de_desbloqueio,
        desafio_de_desbloqueio_enunciado=missao.desafio_de_desbloqueio_enunciado,
        perguntas_do_desbloqueio=_saida_das_perguntas_ao_autor(perguntas),
    )


def _obter_pergunta_do_desbloqueio(
    sessao_bd: Session, id_da_pergunta: uuid.UUID
) -> PerguntaDoDesbloqueio:
    pergunta = sessao_bd.get(PerguntaDoDesbloqueio, id_da_pergunta)
    if pergunta is None:
        raise NaoEncontrado(mensagem="Pergunta não encontrada.")
    return pergunta


class AbrirEnvioDaImagemEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tipo_mime: str
    tamanho_declarado: int


class AbrirEnvioDaImagemSaida(BaseModel):
    endereco_da_sessao: str


@roteador.post("/perguntas-do-desbloqueio/{id_da_pergunta}/imagem", status_code=201)
def abrir_envio_da_imagem_da_pergunta_rota(
    id_da_pergunta: uuid.UUID,
    entrada: AbrirEnvioDaImagemEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    armazenamento: Annotated[PortaDeArmazenamento, Depends(dependencia_de_armazenamento)],
) -> AbrirEnvioDaImagemSaida:
    """`RF-09-119`, `RF-09-115`: abre a sessão retomável da imagem da
    pergunta — a autoria, os formatos e o teto de 1 MB já são de
    `abrir_envio_da_imagem_da_pergunta`. Os bytes nunca passam por aqui."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    pergunta = _obter_pergunta_do_desbloqueio(sessao_bd, id_da_pergunta)
    endereco = abrir_envio_da_imagem_da_pergunta(
        sessao_bd,
        pergunta,
        operador=operador,
        tipo_mime=entrada.tipo_mime,
        tamanho_declarado=entrada.tamanho_declarado,
        armazenamento=armazenamento,
    )
    sessao_bd.commit()
    return AbrirEnvioDaImagemSaida(endereco_da_sessao=endereco)


@roteador.patch("/perguntas-do-desbloqueio/{id_da_pergunta}/imagem")
def confirmar_envio_da_imagem_da_pergunta_rota(
    id_da_pergunta: uuid.UUID,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    armazenamento: Annotated[PortaDeArmazenamento, Depends(dependencia_de_armazenamento)],
) -> PerguntaDoDesbloqueioSaida:
    """Confirma o envio encerrado pelo cliente — só agora a pergunta passa
    a ter imagem, depois de o armazenamento apurar o tamanho real
    (`RF-09-119`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    pergunta = _obter_pergunta_do_desbloqueio(sessao_bd, id_da_pergunta)
    pergunta = confirmar_envio_da_imagem_da_pergunta(
        sessao_bd, pergunta, operador=operador, armazenamento=armazenamento
    )
    sessao_bd.commit()
    return _saida_das_perguntas([pergunta])[0]


@roteador.get("/perguntas-do-desbloqueio/{id_da_pergunta}/imagem")
def ler_imagem_da_pergunta_rota(
    id_da_pergunta: uuid.UUID,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    armazenamento: Annotated[PortaDeArmazenamento, Depends(dependencia_de_armazenamento)],
) -> Response:
    """`RF-09-119`, `RF-05-89`: os bytes da imagem, ao Mestre autor da
    trilha e ao Guerreiro(a) inscrito nela — a autorização e o 404 da
    pergunta sem imagem são de `ler_imagem_da_pergunta` (design — decisão
    5)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    pergunta = _obter_pergunta_do_desbloqueio(sessao_bd, id_da_pergunta)
    imagem = ler_imagem_da_pergunta(
        sessao_bd, pergunta, operador=operador, armazenamento=armazenamento
    )
    return Response(content=imagem.bytes_da_imagem, media_type=imagem.tipo_mime)


class RespostaDoDesbloqueioEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    pergunta_id: uuid.UUID
    alternativa_escolhida: int


class SubmeterDesafioDeDesbloqueioEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    # O quiz vai de uma vez, com a resposta de todas as perguntas
    # (`RF-05-89`); o prático não tem o que responder.
    respostas: list[RespostaDoDesbloqueioEntrada] | None = None


class SubmeterDesafioDeDesbloqueioSaida(BaseModel):
    aprovado: bool | None
    aguardando_mestre: bool
    acertos: int
    total: int


@roteador.post("/eu/missoes/{id_da_missao}/desbloqueio", status_code=201)
def submeter_desafio_de_desbloqueio_rota(
    id_da_missao: uuid.UUID,
    entrada: SubmeterDesafioDeDesbloqueioEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> SubmeterDesafioDeDesbloqueioSaida:
    """`RF-05-13`, `RF-05-14`, `RN-05-06`, `RN-05-20`: o Guerreiro(a)
    inscrito submete o desafio — a aferição do quiz, a declaração do
    prático e a exigência de inscrição já são de
    `submeter_desafio_de_desbloqueio`."""
    _exigir_guerreiro(contexto)
    guerreiro = sessao_bd.get(Persona, contexto.persona_id)
    missao = _obter_missao(sessao_bd, id_da_missao)
    resultado = submeter_desafio_de_desbloqueio(
        sessao_bd,
        guerreiro=guerreiro,
        missao=missao,
        respostas=[resposta.model_dump() for resposta in entrada.respostas]
        if entrada.respostas is not None
        else None,
    )
    sessao_bd.commit()
    return SubmeterDesafioDeDesbloqueioSaida(
        aprovado=resultado.aprovado,
        aguardando_mestre=resultado.aprovado is None,
        acertos=resultado.acertos,
        total=resultado.total,
    )


class DesbloqueioPendenteSaida(BaseModel):
    id: uuid.UUID
    guerreiro_id: uuid.UUID
    guerreiro_nome: str | None
    missao_id: uuid.UUID
    missao_titulo: str
    momento: str


@roteador.get("/missoes/desbloqueios-pendentes")
def listar_desbloqueios_pendentes_rota(
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> list[DesbloqueioPendenteSaida]:
    """`RF-09-117`: as declarações de desafio prático ainda não julgadas,
    só das trilhas do Mestre autor em sessão."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    pendentes = listar_desbloqueios_praticos_pendentes(sessao_bd, operador=operador)
    saida = []
    for pendente in pendentes:
        guerreiro = sessao_bd.get(Persona, pendente.guerreiro_id)
        missao = sessao_bd.get(Missao, pendente.missao_id)
        saida.append(
            DesbloqueioPendenteSaida(
                id=pendente.id,
                guerreiro_id=pendente.guerreiro_id,
                guerreiro_nome=guerreiro.nome if guerreiro is not None else None,
                missao_id=pendente.missao_id,
                missao_titulo=missao.titulo,
                momento=pendente.momento.isoformat(),
            )
        )
    return saida


class JulgarDesafioPraticoEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    aprovado: bool


@roteador.post("/missoes/{id_da_missao}/desbloqueios/{id_do_guerreiro}/julgamento")
def julgar_desafio_pratico_rota(
    id_da_missao: uuid.UUID,
    id_do_guerreiro: uuid.UUID,
    entrada: JulgarDesafioPraticoEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> dict[str, bool]:
    """`RF-09-117`: o Mestre autor julga a declaração — aprovada, ela vira
    o desbloqueio de fato e abre a missão seguinte; reprovada, ela é
    apagada e o Guerreiro(a) declara de novo, sem limite (`RN-05-20`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    desbloqueio = (
        sessao_bd.query(DesbloqueioDaMissao)
        .filter_by(missao_id=id_da_missao, guerreiro_id=id_do_guerreiro)
        .first()
    )
    julgar_desafio_pratico(
        sessao_bd, operador=operador, desbloqueio=desbloqueio, aprovado=entrada.aprovado
    )
    sessao_bd.commit()
    return {"aprovado": entrada.aprovado}


class ProgressoDaTrilhaSaida(BaseModel):
    trilha_id: uuid.UUID
    trilha_nome: str
    nivel_atual: int | None
    obrigatorias_desbloqueadas: int
    obrigatorias_totais: int
    pontos_regulares: int
    badges: list[str]


@roteador.get("/eu/progresso")
def obter_progresso_rota(
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> list[ProgressoDaTrilhaSaida]:
    """`RF-05-15`, `RF-05-16`, `RN-05-03`, `RN-05-04`: nível e quanto falta
    para o próximo, pontos e badges, por trilha inscrita — nível é
    percurso, nunca saldo de pontos. As recompensas conquistadas continuam
    servidas por `GET /v1/eu/recompensas`."""
    _exigir_guerreiro(contexto)
    progresso = consultar_progresso(sessao_bd, guerreiro_id=contexto.persona_id)
    return [
        ProgressoDaTrilhaSaida(
            trilha_id=item.trilha.id,
            trilha_nome=item.trilha.nome,
            nivel_atual=item.nivel_atual,
            obrigatorias_desbloqueadas=item.obrigatorias_desbloqueadas,
            obrigatorias_totais=item.obrigatorias_totais,
            pontos_regulares=item.pontos_regulares,
            badges=item.badges,
        )
        for item in progresso
    ]


class DesafioSaida(BaseModel):
    atividade: AtividadeSaida
    missao_id: uuid.UUID
    missao_titulo: str
    trilha_id: uuid.UUID
    trilha_titulo: str


class RecompensaDoDesafioExtraSaida(BaseModel):
    tipo_de_recurso_nome: str
    ponto_de_apoio_nome: str


class DesafioExtraDoGuerreiroSaida(BaseModel):
    id: uuid.UUID
    trilha_id: uuid.UUID
    trilha_nome: str
    missao_id: uuid.UUID | None
    missao_titulo: str | None
    modalidade: str
    formato: str
    criterio_de_atribuicao: str
    pontos_extras: int
    recompensa: RecompensaDoDesafioExtraSaida
    quantidade_disponivel: int
    quantidade_restante: int
    vigencia_inicio: date
    vigencia_fim: date


def _saida_do_desafio_extra_do_guerreiro(
    sessao_bd: Session, desafio: DesafioExtra
) -> DesafioExtraDoGuerreiroSaida:
    """A saída própria e enxuta do Guerreiro(a): nunca o nick do
    destinatário, a justificativa, o parecer, o motivo de recusa, o custeio,
    o aporte nem o lastro que a `DesafioExtraSaida` do proponente carrega
    (`RF-05-21`, `RN-05-21`, `RN-14-20`, design — decisão 5)."""
    trilha = sessao_bd.get(Trilha, desafio.trilha_id)
    missao = sessao_bd.get(Missao, desafio.missao_id) if desafio.missao_id is not None else None
    tipo_de_recurso = sessao_bd.get(TipoDeRecurso, desafio.tipo_de_recurso_id)
    ponto_de_apoio = sessao_bd.get(PontoDeApoio, desafio.ponto_de_apoio_id)
    return DesafioExtraDoGuerreiroSaida(
        id=desafio.id,
        trilha_id=trilha.id,
        trilha_nome=trilha.nome,
        missao_id=missao.id if missao is not None else None,
        missao_titulo=missao.titulo if missao is not None else None,
        modalidade=desafio.modalidade.value,
        formato=desafio.formato.value,
        criterio_de_atribuicao=desafio.criterio_de_atribuicao,
        pontos_extras=desafio.pontos_extras,
        recompensa=RecompensaDoDesafioExtraSaida(
            tipo_de_recurso_nome=tipo_de_recurso.nome,
            ponto_de_apoio_nome=ponto_de_apoio.nome,
        ),
        quantidade_disponivel=desafio.quantidade_disponivel,
        quantidade_restante=calcular_quantidade_restante_do_extra(sessao_bd, desafio=desafio),
        vigencia_inicio=desafio.vigencia_inicio,
        vigencia_fim=desafio.vigencia_fim,
    )


class MeusDesafiosSaida(BaseModel):
    semanais: list[DesafioSaida] = Field(default_factory=list)
    extras: list[DesafioExtraDoGuerreiroSaida] = Field(default_factory=list)


@roteador.get("/eu/desafios")
def listar_meus_desafios_rota(
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> MeusDesafiosSaida:
    """`RF-05-19`, `RF-05-20`, `RN-05-21`, `RN-05-06`: os dois conjuntos em
    aberto do Guerreiro(a) em sessão — os **semanais**, as atividades
    desbloqueadas de trilha inscrita sem Resultado lançado para ele
    (proposal — decisão de recorte, `desafios_em_aberto_do_guerreiro`), e os
    **extras**, os desafios extras publicados, vigentes e elegíveis a ele
    (`desafios_extras_elegiveis_do_guerreiro`). Sem nada em aberto, os dois
    conjuntos vazios, nunca erro (design — decisão 1). **BREAKING**: no
    lugar da lista de atividades que a rota devolvia até a fatia 6."""
    _exigir_guerreiro(contexto)
    atividades = desafios_em_aberto_do_guerreiro(sessao_bd, guerreiro_id=contexto.persona_id)
    semanais = []
    for atividade in atividades:
        missao = sessao_bd.get(Missao, atividade.missao_id)
        trilha = sessao_bd.get(Trilha, missao.trilha_id)
        semanais.append(
            DesafioSaida(
                atividade=saida_da_atividade(atividade),
                missao_id=missao.id,
                missao_titulo=missao.titulo,
                trilha_id=trilha.id,
                trilha_titulo=trilha.nome,
            )
        )

    desafios_extras = desafios_extras_elegiveis_do_guerreiro(
        sessao_bd, guerreiro_id=contexto.persona_id, hoje=agora().date()
    )
    extras = [
        _saida_do_desafio_extra_do_guerreiro(sessao_bd, desafio) for desafio in desafios_extras
    ]

    return MeusDesafiosSaida(semanais=semanais, extras=extras)


class RetomadaSaida(BaseModel):
    missao_id: uuid.UUID
    missao_titulo: str
    trilha_id: uuid.UUID
    trilha_titulo: str
    prazo: datetime


@roteador.get("/eu/retomadas")
def listar_minhas_retomadas_rota(
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> list[RetomadaSaida]:
    """`RF-05-79`, `RF-05-80`, `RN-05-38`, `RN-05-21`: as retomadas em
    aberto do Guerreiro(a) em sessão — missão, trilha e prazo de cada
    agendamento vencido sem produção. Sem nada em aberto, lista vazia, sem
    erro; a derivação já é de `retomadas_em_aberto_do_guerreiro`."""
    _exigir_guerreiro(contexto)
    retomadas = retomadas_em_aberto_do_guerreiro(sessao_bd, guerreiro_id=contexto.persona_id)
    return [
        RetomadaSaida(
            missao_id=item.missao.id,
            missao_titulo=item.missao.titulo,
            trilha_id=item.trilha.id,
            trilha_titulo=item.trilha.nome,
            prazo=item.prazo,
        )
        for item in retomadas
    ]
