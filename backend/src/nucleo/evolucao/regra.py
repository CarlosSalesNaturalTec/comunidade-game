import uuid
from dataclasses import dataclass
from datetime import datetime

from sqlalchemy.orm import Session

from ..aulas.modelo import Presenca
from ..criacoes_originais.modelo import CriacaoOriginal, SituacaoDaCriacaoOriginal
from ..equipes.modelo import IntegranteDaEquipe
from ..ocorrencias_de_conduta.modelo import OcorrenciaDeConduta
from ..poderes.modelo import Poder
from ..pontuacao.modelo import PontoRegular
from ..resultados.modelo import DesfechoDoResultado, Resultado
from ..trilhas.modelo import Atividade, Trilha
from ..trilhas.regra import ProgressoDaTrilha, consultar_progresso


@dataclass
class ItemDePresenca:
    aula_id: uuid.UUID
    momento_do_fato: datetime


@dataclass
class ItemDeAtividadeRealizada:
    atividade_id: uuid.UUID
    atividade_titulo: str
    desfecho: DesfechoDoResultado
    momento_do_fato: datetime


@dataclass
class ItemDePontosPorPoder:
    poder_id: uuid.UUID
    poder_nome: str
    total: int


@dataclass
class ItemDeCriacaoValidada:
    trilha_id: uuid.UUID
    trilha_titulo: str
    validado_em: datetime


@dataclass
class EvolucaoDoGuerreiro:
    presencas: list[ItemDePresenca]
    atividades: list[ItemDeAtividadeRealizada]
    progresso_das_trilhas: list[ProgressoDaTrilha]
    pontos_por_poder: list[ItemDePontosPorPoder]
    criacoes_validadas: list[ItemDeCriacaoValidada]


def _presencas_do_guerreiro(sessao: Session, guerreiro_id: uuid.UUID) -> list[ItemDePresenca]:
    linhas = (
        sessao.query(Presenca)
        .filter_by(guerreiro_id=guerreiro_id, anulada_em=None)
        .order_by(Presenca.momento_do_fato)
        .all()
    )
    return [
        ItemDePresenca(aula_id=linha.aula_id, momento_do_fato=linha.momento_do_fato)
        for linha in linhas
    ]


def _atividades_do_guerreiro(
    sessao: Session, guerreiro_id: uuid.UUID
) -> list[ItemDeAtividadeRealizada]:
    linhas = (
        sessao.query(Resultado, Atividade)
        .join(Atividade, Atividade.id == Resultado.atividade_id)
        .filter(Resultado.guerreiro_id == guerreiro_id)
        .order_by(Resultado.momento_do_fato)
        .all()
    )
    return [
        ItemDeAtividadeRealizada(
            atividade_id=atividade.id,
            atividade_titulo=atividade.titulo,
            desfecho=resultado.desfecho,
            momento_do_fato=resultado.momento_do_fato,
        )
        for resultado, atividade in linhas
    ]


def _pontos_por_poder_do_guerreiro(
    sessao: Session, guerreiro_id: uuid.UUID
) -> list[ItemDePontosPorPoder]:
    linhas = (
        sessao.query(PontoRegular, Poder)
        .join(Poder, Poder.id == PontoRegular.poder_id)
        .filter(PontoRegular.guerreiro_id == guerreiro_id, PontoRegular.poder_id.is_not(None))
        .all()
    )
    return [
        ItemDePontosPorPoder(poder_id=poder.id, poder_nome=poder.nome, total=ponto.total)
        for ponto, poder in linhas
    ]


def _criacoes_validadas_do_guerreiro(
    sessao: Session, guerreiro_id: uuid.UUID
) -> list[ItemDeCriacaoValidada]:
    """A validada do Guerreiro(a), individual ou da equipe de que participa
    — nunca a de outro integrante isolada, e nunca o nome dos demais
    integrantes: a evolução do responsável não credita coautoria
    (`RF-13-10`, `RF-13-12`).
    """
    equipes_do_guerreiro = (
        sessao.query(IntegranteDaEquipe.equipe_id)
        .filter_by(persona_id=guerreiro_id)
        .scalar_subquery()
    )
    linhas = (
        sessao.query(CriacaoOriginal, Trilha)
        .join(Trilha, Trilha.id == CriacaoOriginal.trilha_id)
        .filter(
            CriacaoOriginal.situacao == SituacaoDaCriacaoOriginal.validada,
            (CriacaoOriginal.guerreiro_id == guerreiro_id)
            | (CriacaoOriginal.equipe_id.in_(equipes_do_guerreiro)),
        )
        .order_by(CriacaoOriginal.validado_em)
        .all()
    )
    return [
        ItemDeCriacaoValidada(
            trilha_id=trilha.id, trilha_titulo=trilha.nome, validado_em=criacao.validado_em
        )
        for criacao, trilha in linhas
    ]


def montar_evolucao(sessao: Session, *, guerreiro_id: uuid.UUID) -> EvolucaoDoGuerreiro:
    """Monta o payload consolidado numa só chamada, por reaproveitamento:
    nada aqui reapura nível, ponto ou percurso — só lê o que cada capability
    já grava (`RF-13-07`, `RF-13-08`, `RF-13-10`, design — decisão 2). Nem
    `assistente/` nem `apoio_escolar/` são tocados em nenhuma linha deste
    módulo — a vedação de `RF-13-11` é estrutural, não filtro (design —
    decisão 4).
    """
    return EvolucaoDoGuerreiro(
        presencas=_presencas_do_guerreiro(sessao, guerreiro_id),
        atividades=_atividades_do_guerreiro(sessao, guerreiro_id),
        progresso_das_trilhas=consultar_progresso(sessao, guerreiro_id=guerreiro_id),
        pontos_por_poder=_pontos_por_poder_do_guerreiro(sessao, guerreiro_id),
        criacoes_validadas=_criacoes_validadas_do_guerreiro(sessao, guerreiro_id),
    )


def listar_ocorrencias_do_guerreiro(
    sessao: Session, *, guerreiro_id: uuid.UUID
) -> list[OcorrenciaDeConduta]:
    """As ocorrências do vinculado, na guarda que `ocorrencias_de_conduta`
    já impõe ao motivo apagado pelo expurgo (`RF-13-09`, `RN-13-21`,
    `RN-01-52`)."""
    return (
        sessao.query(OcorrenciaDeConduta)
        .filter_by(guerreiro_id=guerreiro_id)
        .order_by(OcorrenciaDeConduta.momento_do_fato)
        .all()
    )
