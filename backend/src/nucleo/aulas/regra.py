from datetime import datetime

from sqlalchemy.orm import Session

from ..erros import ErroDeValidacao, PermissaoNegada
from ..personas.modelo import ComunidadeVirtual, Papel, Persona
from ..tempo import agora
from .modelo import Aula, ModoDeComprovacao, Presenca


def agendar_aula(
    sessao: Session,
    *,
    operador: Persona,
    comunidade: ComunidadeVirtual | None,
    inicio_em: datetime | None,
    fim_em: datetime | None,
) -> Aula:
    """Restrita ao Admin — o Mestre lê o painel do dia, mas não escreve em
    gestão (`RF-01-20`, `RF-01-16`, `RF-01-03`, PRD-01 §4).
    """
    if operador.papel != Papel.admin:
        raise PermissaoNegada(mensagem="Só o Admin agenda aula.")
    if comunidade is None:
        raise ErroDeValidacao(mensagem="Aula exige uma comunidade.", campo="comunidade_virtual_id")
    if inicio_em is None:
        raise ErroDeValidacao(mensagem="Aula exige o horário inicial.", campo="inicio_em")
    if fim_em is None:
        raise ErroDeValidacao(mensagem="Aula exige o horário final.", campo="fim_em")
    if fim_em <= inicio_em:
        raise ErroDeValidacao(
            mensagem="O horário final da aula precisa ser posterior ao inicial.",
            campo="fim_em",
        )

    aula = Aula(
        comunidade_virtual_id=comunidade.id,
        inicio_em=inicio_em,
        fim_em=fim_em,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(aula)
    sessao.flush()
    return aula


def aulas_vigentes(sessao: Session) -> list[Aula]:
    """Todas as aulas cujo intervalo contém o momento corrente — havendo
    mais de uma comunidade vigente ao mesmo tempo, a escolha é de quem abre,
    nunca do núcleo (`RF-01-32`, `RF-01-18`).
    """
    momento = agora()
    return sessao.query(Aula).filter(Aula.inicio_em <= momento, Aula.fim_em >= momento).all()


def registrar_presenca(
    sessao: Session,
    *,
    operador: Persona,
    aula: Aula | None,
    guerreiro: Persona | None,
    modo: str | None,
    confirmador: Persona | None,
    momento_do_fato: datetime | None,
) -> Presenca:
    """Idempotente por (aula, guerreiro): o reenvio do App 01 depois da rede
    voltar devolve o registro já gravado, sem duplicar e sem erro
    (`RF-01-20`, PRD-01 §10, design — decisões).
    """
    if aula is None:
        raise ErroDeValidacao(mensagem="Presença exige uma aula.", campo="aula_id")
    if guerreiro is None:
        raise ErroDeValidacao(mensagem="Presença exige o Guerreiro(a).", campo="guerreiro_id")

    existente = sessao.query(Presenca).filter_by(aula_id=aula.id, guerreiro_id=guerreiro.id).first()
    if existente is not None:
        return existente

    if guerreiro.comunidade_virtual_id != aula.comunidade_virtual_id:
        raise ErroDeValidacao(
            mensagem="Presença só é registrada na comunidade do próprio Guerreiro(a).",
            campo="aula_id",
        )
    if not modo:
        raise ErroDeValidacao(mensagem="Presença exige o modo de comprovação.", campo="modo")
    try:
        modo_valido = ModoDeComprovacao(modo)
    except ValueError as exc:
        raise ErroDeValidacao(
            mensagem="Modo de comprovação fora dos valores previstos.", campo="modo"
        ) from exc
    if modo_valido == ModoDeComprovacao.confirmacao and confirmador is None:
        raise ErroDeValidacao(
            mensagem="Presença por confirmação exige quem confirmou.", campo="confirmador_id"
        )
    if momento_do_fato is None:
        raise ErroDeValidacao(
            mensagem="Presença exige o momento em que aconteceu.", campo="momento_do_fato"
        )

    presenca = Presenca(
        aula_id=aula.id,
        guerreiro_id=guerreiro.id,
        modo=modo_valido,
        confirmador_id=confirmador.id if confirmador is not None else None,
        momento_do_fato=momento_do_fato,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(presenca)
    sessao.flush()
    return presenca
