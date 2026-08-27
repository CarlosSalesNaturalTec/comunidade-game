import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from ..autenticacao import ContextoDaSessao, exigir_persona
from ..banco import obter_sessao
from ..bibliografias.modelo import BibliografiaDaMissao
from ..bibliografias.regra import consultar_bibliografia_da_missao, ler_disponibilidade_e_credito
from ..configuracao import Configuracao, obter_configuracao
from ..conteudos.modelo import ConteudoDaMissao
from ..conteudos.regra import consultar_conteudos_da_missao
from ..conteudos.rotas import ConteudoSaida, saida_do_conteudo
from ..culminancias.modelo import Culminancia
from ..culminancias.rotas import CulminanciaSaida, saida_da_culminancia
from ..erros import NaoEncontrado, PermissaoNegada
from ..ods.modelo import EtiquetaOds
from ..ods.regra import cobertura_por_trilha
from ..ods.rotas import EtiquetaOdsSaida, saida_da_etiqueta
from ..personas.modelo import Papel, Persona
from .modelo import (
    Atividade,
    DesbloqueioDaMissao,
    EtapaDoCiclo,
    FormatoDeAtividade,
    Missao,
    ModalidadeDeAtividade,
    SituacaoDaTrilha,
    TipoDeDesafioDeDesbloqueio,
    Trilha,
)
from .regra import (
    consultar_inscricoes_do_guerreiro,
    consultar_progresso,
    criar_atividade,
    criar_missao,
    criar_trilha,
    declarar_cadencia_de_retomada,
    declarar_desafio_de_desbloqueio,
    derivar_percurso,
    despublicar_trilha,
    inscrever_na_trilha,
    julgar_desafio_pratico,
    listar_desbloqueios_praticos_pendentes,
    obter_proxima_missao,
    publicar_trilha,
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
    enunciado: str
    alternativas: list[str] | None = None


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


def _saida_do_desafio_de_desbloqueio(missao: Missao) -> DesafioDeDesbloqueioSaida | None:
    if missao.tipo_do_desafio_de_desbloqueio is None:
        return None
    alternativas = None
    if missao.tipo_do_desafio_de_desbloqueio == TipoDeDesafioDeDesbloqueio.quiz:
        alternativas = [
            missao.desafio_de_desbloqueio_alternativa_1,
            missao.desafio_de_desbloqueio_alternativa_2,
            missao.desafio_de_desbloqueio_alternativa_3,
            missao.desafio_de_desbloqueio_alternativa_4,
        ]
    return DesafioDeDesbloqueioSaida(
        tipo=missao.tipo_do_desafio_de_desbloqueio,
        enunciado=missao.desafio_de_desbloqueio_enunciado,
        alternativas=alternativas,
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
        desafio_de_desbloqueio=_saida_do_desafio_de_desbloqueio(item.missao),
    )


class DeclararDesafioDeDesbloqueioEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tipo: str
    enunciado: str = Field(min_length=1)
    alternativas: list[str] | None = None
    alternativa_correta: int | None = None


class MissaoComDesafioDeDesbloqueioSaida(MissaoSaida):
    """Só a resposta desta rota traz o desafio inteiro, alternativa correta
    inclusa — nunca `MissaoSaida` das rotas públicas ou de leitura geral,
    para que a resposta certa não vaze ao Guerreiro(a) (design — decisão 4).
    """

    tipo_do_desafio_de_desbloqueio: TipoDeDesafioDeDesbloqueio
    desafio_de_desbloqueio_enunciado: str
    desafio_de_desbloqueio_alternativas: list[str] | None
    desafio_de_desbloqueio_alternativa_correta: int | None


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
        alternativas=entrada.alternativas,
        alternativa_correta=entrada.alternativa_correta,
    )
    sessao_bd.commit()
    alternativas = None
    if missao.tipo_do_desafio_de_desbloqueio == TipoDeDesafioDeDesbloqueio.quiz:
        alternativas = [
            missao.desafio_de_desbloqueio_alternativa_1,
            missao.desafio_de_desbloqueio_alternativa_2,
            missao.desafio_de_desbloqueio_alternativa_3,
            missao.desafio_de_desbloqueio_alternativa_4,
        ]
    return MissaoComDesafioDeDesbloqueioSaida(
        **_saida_da_missao(missao, etiquetas=_etiquetas_da_missao(sessao_bd, missao)).model_dump(),
        tipo_do_desafio_de_desbloqueio=missao.tipo_do_desafio_de_desbloqueio,
        desafio_de_desbloqueio_enunciado=missao.desafio_de_desbloqueio_enunciado,
        desafio_de_desbloqueio_alternativas=alternativas,
        desafio_de_desbloqueio_alternativa_correta=missao.desafio_de_desbloqueio_alternativa_correta,
    )


class SubmeterDesafioDeDesbloqueioEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    alternativa_escolhida: int | None = None


class SubmeterDesafioDeDesbloqueioSaida(BaseModel):
    aprovado: bool | None
    aguardando_mestre: bool


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
        alternativa_escolhida=entrada.alternativa_escolhida,
    )
    sessao_bd.commit()
    return SubmeterDesafioDeDesbloqueioSaida(
        aprovado=resultado.aprovado, aguardando_mestre=resultado.aprovado is None
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
