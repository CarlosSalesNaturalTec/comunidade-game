from datetime import UTC, datetime

from sqlalchemy.orm import Session

from ..equipes.modelo import Equipe, IntegranteDaEquipe
from ..erros import ErroDeValidacao, PermissaoNegada
from ..personas.modelo import Persona
from ..pontuacao.regra import creditar_pontuacao_da_criacao_original
from ..trilhas.modelo import Trilha
from ..trilhas.regra import conferir_posse_da_trilha
from .modelo import CriacaoOriginal, SituacaoDaCriacaoOriginal


def entregar_criacao_original(
    sessao: Session,
    *,
    guerreiro: Persona | None,
    equipe: Equipe | None,
    producao: str | None,
) -> CriacaoOriginal:
    """Entrega feita por um integrante da equipe da trilha, e vale pela
    equipe inteira; a trilha é a da própria equipe (`RF-01-26`, `RF-01-64`).
    Nasce sempre com situação "entregue". Como cada Guerreiro(a) tem uma só
    equipe por trilha (`RN-01-44`), a equipe aceita no máximo uma entrega.
    """
    if equipe is None or equipe.trilha_id is None:
        raise ErroDeValidacao(
            mensagem="Criação original exige a equipe da trilha.", campo="equipe_id"
        )
    if guerreiro is None:
        raise ErroDeValidacao(
            mensagem="Criação original exige o Guerreiro(a) autor.", campo="guerreiro_id"
        )
    if not producao or not producao.strip():
        raise ErroDeValidacao(
            mensagem="Criação original exige a produção declarada.", campo="producao"
        )

    e_integrante = (
        sessao.query(IntegranteDaEquipe)
        .filter_by(equipe_id=equipe.id, persona_id=guerreiro.id)
        .first()
    )
    if e_integrante is None:
        raise PermissaoNegada(
            mensagem="Só um integrante da equipe entrega a criação original dela."
        )

    ja_entregou = sessao.query(CriacaoOriginal).filter_by(equipe_id=equipe.id).first()
    if ja_entregou is not None:
        raise ErroDeValidacao(
            mensagem="Esta equipe já entregou a criação original desta trilha.",
            campo="equipe_id",
        )

    criacao = CriacaoOriginal(
        trilha_id=equipe.trilha_id,
        equipe_id=equipe.id,
        producao=producao,
        situacao=SituacaoDaCriacaoOriginal.entregue,
        autor_id=guerreiro.id,
        papel_do_autor=guerreiro.papel.value,
    )
    sessao.add(criacao)
    sessao.flush()
    return criacao


def _conferir_transicao(criacao: CriacaoOriginal, trilha: Trilha, operador: Persona) -> None:
    """Comum a validar e devolver: só o Mestre autor da trilha ou o Admin
    decidem (`RF-01-16`), e só uma entrega "entregue" aceita transição —
    o que também impede crédito duplo por chamada repetida (design —
    decisões).
    """
    conferir_posse_da_trilha(trilha, operador)
    if criacao.situacao != SituacaoDaCriacaoOriginal.entregue:
        raise ErroDeValidacao(
            mensagem="Só uma criação original entregue pode ser validada ou devolvida.",
            campo="situacao",
        )


def validar_criacao_original(
    sessao: Session, *, operador: Persona, criacao: CriacaoOriginal
) -> CriacaoOriginal:
    """Credita, na mesma transação da mudança de situação, os 50 pontos
    regulares, o nível 5 e o badge de autoria (`RF-01-26`, `RF-01-21`,
    11 §§5-7).
    """
    trilha = sessao.get(Trilha, criacao.trilha_id)
    _conferir_transicao(criacao, trilha, operador)

    criacao.situacao = SituacaoDaCriacaoOriginal.validada
    criacao.validado_por_id = operador.id
    criacao.validado_em = datetime.now(UTC)
    sessao.flush()

    creditar_pontuacao_da_criacao_original(sessao, criacao_original=criacao, trilha=trilha)
    return criacao


def devolver_criacao_original(
    sessao: Session, *, operador: Persona, criacao: CriacaoOriginal
) -> CriacaoOriginal:
    """Devolve para ajuste sem creditar nada; a autoria original permanece
    (`RN-01-13`) — o reenvio é fluxo do PRD-09.
    """
    trilha = sessao.get(Trilha, criacao.trilha_id)
    _conferir_transicao(criacao, trilha, operador)

    criacao.situacao = SituacaoDaCriacaoOriginal.devolvida
    criacao.validado_por_id = operador.id
    criacao.validado_em = datetime.now(UTC)
    sessao.flush()
    return criacao
