import uuid
from dataclasses import dataclass

from sqlalchemy.orm import Session

from ..coletas.modelo import DesafioDeColeta, SerieDeColeta
from ..comunidades.modelo import VinculoJogador
from ..comunidades.regra import filtrar_personas_por_comunidade, unir_vinculo_vigente
from ..erros import ErroDeValidacao
from ..personas.modelo import Persona
from ..resultados.modelo import Resultado
from ..trilhas.modelo import Atividade, Missao, Trilha
from ..trilhas.regra import conferir_autoria_estrita_da_trilha
from .modelo import OBJETIVO_ODS_MAXIMO, OBJETIVO_ODS_MINIMO, EtiquetaOds


@dataclass(frozen=True)
class EtiquetaDeclarada:
    """Uma linha da lista completa que a substituição recebe — objetivo
    obrigatório e meta opcional (`RF-09-92`, `RF-09-98`)."""

    objetivo: int | None
    meta: str | None = None


def _conferir_objetivo(objetivo: int | None) -> None:
    if objetivo is None or not (OBJETIVO_ODS_MINIMO <= objetivo <= OBJETIVO_ODS_MAXIMO):
        raise ErroDeValidacao(
            mensagem=f"Objetivo ODS deve estar entre {OBJETIVO_ODS_MINIMO} e "
            f"{OBJETIVO_ODS_MAXIMO}.",
            campo="objetivo",
        )


def criar_etiqueta_ods(
    sessao: Session,
    *,
    operador: Persona,
    objetivo: int | None,
    meta: str | None = None,
    trilha: Trilha | None = None,
    missao: Missao | None = None,
) -> EtiquetaOds:
    """Presa a exatamente uma trilha ou a exatamente uma missão, declarada
    pelo **Mestre autor** da trilha — autoria estrita, a mesma da
    publicação: nem outro Mestre nem o Admin declaram, porque o Admin não
    edita a trilha de um Mestre (`RF-01-40`, `RF-01-45`, `RF-01-16`,
    `RF-09-92`, `RF-09-98`, design — decisão 2)."""
    if (trilha is None) == (missao is None):
        raise ErroDeValidacao(
            mensagem="Etiqueta ODS exige exatamente uma trilha ou uma missão.",
            campo="trilha_id",
        )

    trilha_da_autoria = trilha
    if missao is not None:
        trilha_da_autoria = sessao.get(Trilha, missao.trilha_id)
    conferir_autoria_estrita_da_trilha(trilha_da_autoria, operador)

    _conferir_objetivo(objetivo)

    etiqueta = EtiquetaOds(
        objetivo=objetivo,
        meta=meta,
        trilha_id=trilha.id if trilha is not None else None,
        missao_id=missao.id if missao is not None else None,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(etiqueta)
    sessao.flush()
    return etiqueta


def _substituir_etiquetas(
    sessao: Session,
    *,
    operador: Persona,
    trilha_da_autoria: Trilha | None,
    etiquetas: list[EtiquetaDeclarada],
    trilha: Trilha | None = None,
    missao: Missao | None = None,
) -> list[EtiquetaOds]:
    """Todas as recusas antes de qualquer escrita: confere a autoria e
    valida **todos** os objetivos recebidos antes de apagar o que havia, de
    modo que uma etiqueta inválida recuse a operação inteira e deixe o
    conjunto anterior intacto (design — decisão 4)."""
    conferir_autoria_estrita_da_trilha(trilha_da_autoria, operador)
    for declarada in etiquetas:
        _conferir_objetivo(declarada.objetivo)

    consulta = sessao.query(EtiquetaOds)
    consulta = (
        consulta.filter_by(trilha_id=trilha.id)
        if trilha is not None
        else consulta.filter_by(missao_id=missao.id)
    )
    for anterior in consulta.all():
        sessao.delete(anterior)
    sessao.flush()

    return [
        criar_etiqueta_ods(
            sessao,
            operador=operador,
            objetivo=declarada.objetivo,
            meta=declarada.meta,
            trilha=trilha,
            missao=missao,
        )
        for declarada in etiquetas
    ]


def substituir_etiquetas_da_trilha(
    sessao: Session,
    *,
    operador: Persona,
    trilha: Trilha,
    etiquetas: list[EtiquetaDeclarada],
) -> list[EtiquetaOds]:
    """A lista recebida substitui o conjunto que a trilha tinha: o anterior
    é apagado e o recebido gravado, na mesma transação. Lista vazia deixa a
    trilha sem etiqueta — legal no Ciclo 01 (`RF-09-93`). A substituição é
    **escopada à trilha** e nunca alcança as etiquetas das missões dela, o
    que preserva a precedência da etiqueta própria da missão (`RF-09-92`,
    `RF-01-45`, design — decisões 1 e 4)."""
    return _substituir_etiquetas(
        sessao,
        operador=operador,
        trilha_da_autoria=trilha,
        etiquetas=etiquetas,
        trilha=trilha,
    )


def substituir_etiquetas_da_missao(
    sessao: Session,
    *,
    operador: Persona,
    missao: Missao,
    etiquetas: list[EtiquetaDeclarada],
) -> list[EtiquetaOds]:
    """O mesmo da trilha, **escopado à missão**: nunca alcança as etiquetas
    da trilha a que ela pertence (`RF-09-98`, `RF-01-45`, design —
    decisões 1 e 4)."""
    return _substituir_etiquetas(
        sessao,
        operador=operador,
        trilha_da_autoria=sessao.get(Trilha, missao.trilha_id),
        etiquetas=etiquetas,
        missao=missao,
    )


def resolver_etiquetas_da_missao(sessao: Session, missao: Missao) -> list[EtiquetaOds]:
    """A etiqueta própria da missão prevalece sobre a da trilha; na falta
    dela, cai para a trilha (`RF-01-45`, 11 §2.1)."""
    proprias = sessao.query(EtiquetaOds).filter_by(missao_id=missao.id).all()
    if proprias:
        return proprias
    return sessao.query(EtiquetaOds).filter_by(trilha_id=missao.trilha_id).all()


def cobertura_por_trilha(sessao: Session, trilha_id: uuid.UUID) -> set[int]:
    """União dos objetivos da trilha e das missões dela (`RF-01-42`,
    `RN-01-24`)."""
    objetivos = {
        objetivo
        for (objetivo,) in sessao.query(EtiquetaOds.objetivo).filter_by(trilha_id=trilha_id)
    }
    ids_das_missoes = [
        missao_id for (missao_id,) in sessao.query(Missao.id).filter_by(trilha_id=trilha_id)
    ]
    if ids_das_missoes:
        objetivos |= {
            objetivo
            for (objetivo,) in sessao.query(EtiquetaOds.objetivo).filter(
                EtiquetaOds.missao_id.in_(ids_das_missoes)
            )
        }
    return objetivos


def cobertura_por_poder(sessao: Session, poder_id: uuid.UUID) -> set[int]:
    """União das coberturas das trilhas vinculadas ao poder (`RF-01-42`,
    `RN-01-24`)."""
    objetivos: set[int] = set()
    ids_das_trilhas = [
        trilha_id for (trilha_id,) in sessao.query(Trilha.id).filter_by(poder_id=poder_id)
    ]
    for trilha_id in ids_das_trilhas:
        objetivos |= cobertura_por_trilha(sessao, trilha_id)
    return objetivos


def _cobertura_de_coleta_por_comunidade(sessao: Session, comunidade_id: uuid.UUID) -> set[int]:
    """A segunda fonte: união das etiquetas herdadas pelos desafios de
    coleta com série aberta por Guerreiro(a) daquela comunidade, sem
    recuar por estado da série — ativa, interrompida e encerrada contam
    igual, porque a cobertura mede alcance declarado, não continuidade
    (`RF-08-26`, `RF-08-25`, design — Decisions)."""
    consulta = (
        sessao.query(Missao.id)
        .join(DesafioDeColeta, DesafioDeColeta.missao_id == Missao.id)
        .join(SerieDeColeta, SerieDeColeta.desafio_de_coleta_id == DesafioDeColeta.id)
        .join(Persona, Persona.id == SerieDeColeta.coletor_id)
    )
    ids_das_missoes = {
        missao_id for (missao_id,) in filtrar_personas_por_comunidade(consulta, comunidade_id)
    }
    objetivos: set[int] = set()
    for missao_id in ids_das_missoes:
        missao = sessao.get(Missao, missao_id)
        objetivos |= {
            etiqueta.objetivo for etiqueta in resolver_etiquetas_da_missao(sessao, missao)
        }
    return objetivos


def cobertura_por_comunidade(sessao: Session, comunidade_id: uuid.UUID) -> set[int]:
    """União de duas fontes, nunca por Guerreiro(a) individual: as trilhas
    em que há Guerreiro(a) daquela comunidade com Resultado registrado, e
    os desafios de coleta com série aberta por Guerreiro(a) dela — a
    segunda fonte vale ainda que a primeira esteja vazia (`RF-01-42`,
    `RN-01-24`, `RF-08-26`, `RF-08-25`)."""
    consulta = (
        sessao.query(Trilha.id)
        .join(Missao, Missao.trilha_id == Trilha.id)
        .join(Atividade, Atividade.missao_id == Missao.id)
        .join(Resultado, Resultado.atividade_id == Atividade.id)
        .join(Persona, Persona.id == Resultado.guerreiro_id)
    )
    ids_das_trilhas = {
        trilha_id for (trilha_id,) in filtrar_personas_por_comunidade(consulta, comunidade_id)
    }
    objetivos: set[int] = set()
    for trilha_id in ids_das_trilhas:
        objetivos |= cobertura_por_trilha(sessao, trilha_id)
    objetivos |= _cobertura_de_coleta_por_comunidade(sessao, comunidade_id)
    return objetivos


def comunidades_com_cobertura(sessao: Session) -> list[uuid.UUID]:
    """Comunidades com ao menos um Resultado registrado ou uma série de
    coleta aberta sobre desafio etiquetado — a população sobre a qual a
    cobertura pública por comunidade é apurada, para que a comunidade que
    só coletou seja calculada e também perguntada (`RF-01-42`, `RF-01-43`,
    `RN-01-24`, `RF-08-26`, design — Decisions)."""
    consulta_de_resultado = sessao.query(Persona.id).join(
        Resultado, Resultado.guerreiro_id == Persona.id
    )
    consulta_de_resultado = unir_vinculo_vigente(consulta_de_resultado).with_entities(
        VinculoJogador.comunidade_virtual_id
    )
    comunidades = {comunidade_id for (comunidade_id,) in consulta_de_resultado.distinct()}

    consulta_de_coleta = sessao.query(Persona.id).join(
        SerieDeColeta, SerieDeColeta.coletor_id == Persona.id
    )
    consulta_de_coleta = unir_vinculo_vigente(consulta_de_coleta).with_entities(
        VinculoJogador.comunidade_virtual_id
    )
    comunidades |= {comunidade_id for (comunidade_id,) in consulta_de_coleta.distinct()}

    return list(comunidades)
