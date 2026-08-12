import uuid

from sqlalchemy.orm import Session

from ..aulas.modelo import Aula
from ..erros import ErroDeValidacao, NaoEncontrado, PermissaoNegada
from ..personas.modelo import Papel, Persona
from ..tempo import agora
from ..trilhas.modelo import Trilha
from .modelo import Equipe, IntegranteDaEquipe

# `RF-01-38`, documento 02 §5: até cinco integrantes, no máximo um deles
# de 17 anos ou mais — o núcleo não guarda idade, e lê isso do papel da
# persona não ser Guerreiro(a) (design — decisões).
TETO_DE_INTEGRANTES = 5
TETO_DE_INTEGRANTES_NAO_GUERREIROS = 1

# A gestão nunca forma nem altera composição de equipe (`RF-01-16`,
# documento 99 §6 invariante 15) — só quem não é Admin nem Mestre entra
# ou sai por conta própria.
_PAPEIS_QUE_NAO_ALTERAM_COMPOSICAO = frozenset({Papel.admin, Papel.mestre})


def _confirmar_equipe_aberta(sessao: Session, equipe: Equipe) -> None:
    """A equipe da trilha fecha na homologação (`RN-01-44`); a da aula
    fecha com o fim da aula (`RF-01-37`) — sem conferir onde a homologação
    aconteceu (`RF-01-63`)."""
    if equipe.trilha_id is not None and equipe.homologado_em is not None:
        raise ErroDeValidacao(
            mensagem="Esta equipe da trilha já foi homologada; a composição está fixa.",
            campo="equipe_id",
        )
    if equipe.aula_id is not None:
        aula = sessao.get(Aula, equipe.aula_id)
        if aula.fim_em <= agora():
            raise ErroDeValidacao(
                mensagem="Esta aula já encerrou; a equipe não recebe nem perde integrante.",
                campo="equipe_id",
            )


def _confirmar_uma_equipe_por_trilha(sessao: Session, *, persona_id: uuid.UUID, trilha_id) -> None:
    """`RN-01-44`: no máximo uma equipe da trilha por Guerreiro(a) e
    trilha."""
    ja_tem = (
        sessao.query(IntegranteDaEquipe)
        .join(Equipe, Equipe.id == IntegranteDaEquipe.equipe_id)
        .filter(Equipe.trilha_id == trilha_id, IntegranteDaEquipe.persona_id == persona_id)
        .first()
    )
    if ja_tem is not None:
        raise ErroDeValidacao(
            mensagem="Este Guerreiro(a) já integra uma equipe desta trilha.",
            campo="trilha_id",
        )


def _confirmar_composicao(sessao: Session, *, equipe: Equipe, persona: Persona) -> None:
    total = sessao.query(IntegranteDaEquipe).filter_by(equipe_id=equipe.id).count()
    if total >= TETO_DE_INTEGRANTES:
        raise ErroDeValidacao(
            mensagem="Esta equipe já tem os cinco integrantes permitidos.", campo="equipe_id"
        )

    if persona.papel == Papel.guerreiro:
        return
    nao_guerreiros = (
        sessao.query(IntegranteDaEquipe)
        .join(Persona, Persona.id == IntegranteDaEquipe.persona_id)
        .filter(IntegranteDaEquipe.equipe_id == equipe.id, Persona.papel != Papel.guerreiro)
        .count()
    )
    if nao_guerreiros >= TETO_DE_INTEGRANTES_NAO_GUERREIROS:
        raise ErroDeValidacao(
            mensagem="Esta equipe já tem o integrante de 17 anos ou mais permitido.",
            campo="persona_id",
        )


def criar_equipe(
    sessao: Session,
    *,
    operador: Persona,
    aula: Aula | None,
    trilha: Trilha | None,
    papel_do_integrante: str | None = None,
) -> Equipe:
    """Restrita ao Guerreiro(a), que entra como primeiro integrante
    (`RF-01-37`, `RF-01-16`, documento 99 §6 invariante 15)."""
    if operador.papel != Papel.guerreiro:
        raise PermissaoNegada(mensagem="Só o Guerreiro(a) cria equipe.")
    if aula is None and trilha is None:
        raise ErroDeValidacao(mensagem="Equipe exige uma aula ou uma trilha.", campo="aula_id")
    if aula is not None and trilha is not None:
        raise ErroDeValidacao(
            mensagem="Equipe se vincula a uma aula ou a uma trilha, nunca as duas.",
            campo="trilha_id",
        )

    if trilha is not None:
        _confirmar_uma_equipe_por_trilha(sessao, persona_id=operador.id, trilha_id=trilha.id)

    equipe = Equipe(
        aula_id=aula.id if aula is not None else None,
        trilha_id=trilha.id if trilha is not None else None,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(equipe)
    sessao.flush()

    sessao.add(
        IntegranteDaEquipe(equipe_id=equipe.id, persona_id=operador.id, papel=papel_do_integrante)
    )
    sessao.flush()
    return equipe


def entrar_na_equipe(
    sessao: Session, *, operador: Persona, equipe: Equipe, papel: str | None = None
) -> IntegranteDaEquipe:
    """Entrada por conta própria — a gestão nunca forma nem altera
    composição (`RF-01-16`, invariante 15)."""
    if operador.papel in _PAPEIS_QUE_NAO_ALTERAM_COMPOSICAO:
        raise PermissaoNegada(
            mensagem="Admin e Mestre não formam nem alteram a composição da equipe."
        )
    _confirmar_equipe_aberta(sessao, equipe)
    if equipe.trilha_id is not None:
        _confirmar_uma_equipe_por_trilha(sessao, persona_id=operador.id, trilha_id=equipe.trilha_id)
    _confirmar_composicao(sessao, equipe=equipe, persona=operador)

    integrante = IntegranteDaEquipe(equipe_id=equipe.id, persona_id=operador.id, papel=papel)
    sessao.add(integrante)
    sessao.flush()
    return integrante


def sair_da_equipe(
    sessao: Session, *, operador: Persona, equipe: Equipe, persona_id: uuid.UUID
) -> None:
    """Saída — trava pelas mesmas regras de fixidez da entrada (`RF-01-37`,
    `RN-01-44`, `RF-01-16`)."""
    if operador.papel in _PAPEIS_QUE_NAO_ALTERAM_COMPOSICAO:
        raise PermissaoNegada(mensagem="Admin e Mestre não alteram a composição da equipe.")
    _confirmar_equipe_aberta(sessao, equipe)

    integrante = (
        sessao.query(IntegranteDaEquipe)
        .filter_by(equipe_id=equipe.id, persona_id=persona_id)
        .first()
    )
    if integrante is None:
        raise NaoEncontrado(mensagem="Este integrante não pertence a esta equipe.")
    sessao.delete(integrante)
    sessao.flush()


def homologar_equipe_da_trilha(sessao: Session, *, operador: Persona, equipe: Equipe) -> Equipe:
    """Restrita a Mestre ou Admin; sem conferir onde aconteceu — "em
    encontro presencial" é regra de operação, não do núcleo (`RF-01-63`,
    `RF-01-16`)."""
    if operador.papel not in (Papel.mestre, Papel.admin):
        raise PermissaoNegada(mensagem="Só Mestre ou Admin homologam a equipe da trilha.")
    if equipe.trilha_id is None:
        raise ErroDeValidacao(mensagem="Só a equipe da trilha é homologada.", campo="equipe_id")

    equipe.homologado_por_id = operador.id
    equipe.homologado_em = agora()
    sessao.flush()
    return equipe


def equipes_da_aula(sessao: Session, aula_id: uuid.UUID) -> list[Equipe]:
    """Leitura das equipes da aula em andamento — a equipe de uma aula
    nunca aparece em outra (`RF-01-37`)."""
    return sessao.query(Equipe).filter_by(aula_id=aula_id).all()
