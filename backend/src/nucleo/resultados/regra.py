import uuid
from dataclasses import dataclass
from datetime import datetime

from sqlalchemy.orm import Session

from ..aulas.modelo import Aula, SituacaoDaAula
from ..erros import ErroDeValidacao, PermissaoNegada
from ..personas.modelo import Papel, Persona
from ..ponto_extra.regra import creditar_ponto_extra_do_resultado
from ..pontuacao.regra import creditar_pontuacao_do_resultado
from ..reservas.regra import consumir_reservas_da_aula
from ..trilhas.modelo import Atividade, Missao, Trilha
from ..trilhas.regra import conferir_posse_da_trilha
from .modelo import DesfechoDoResultado, Resultado

_SITUACOES_COM_DESFECHO = (SituacaoDaAula.realizada, SituacaoDaAula.cancelada)


def registrar_resultado(
    sessao: Session,
    *,
    operador: Persona,
    aula: Aula | None,
    guerreiro_id: uuid.UUID | None,
    atividade: Atividade | None,
    momento_do_fato: datetime | None,
    producao: str | None,
    desfecho: str | None,
) -> Resultado:
    """Grava o Resultado e credita, na mesma operação, o ponto regular e o
    ponto extra, além de reavaliar nível e badge — só o Mestre autor da
    trilha da atividade ou o Admin lançam o desfecho, pela mesma
    conferência de posse da quinta fatia (`RF-01-20`, `RF-01-16`,
    `RF-01-03`, 11 §4). A aula é quem liga o resultado às reservas que a
    baixa consome (`RF-07-09`, `RF-02-35`, documento 04 §1).
    """
    if atividade is None:
        raise ErroDeValidacao(mensagem="Resultado exige uma atividade.", campo="atividade_id")

    missao = sessao.get(Missao, atividade.missao_id)
    trilha = sessao.get(Trilha, missao.trilha_id)
    conferir_posse_da_trilha(trilha, operador)

    if guerreiro_id is None:
        raise ErroDeValidacao(mensagem="Resultado exige um Guerreiro(a).", campo="guerreiro_id")
    if aula is None:
        raise ErroDeValidacao(
            mensagem="Resultado exige a aula em que foi lançado.", campo="aula_id"
        )
    if momento_do_fato is None:
        raise ErroDeValidacao(mensagem="Resultado exige a data do fato.", campo="momento_do_fato")
    if not producao or not producao.strip():
        raise ErroDeValidacao(
            mensagem="Resultado exige a produção do Guerreiro(a).", campo="producao"
        )
    if not desfecho:
        raise ErroDeValidacao(mensagem="Resultado exige um desfecho.", campo="desfecho")
    try:
        desfecho_valido = DesfechoDoResultado(desfecho)
    except ValueError as exc:
        raise ErroDeValidacao(
            mensagem="Desfecho fora dos valores previstos.", campo="desfecho"
        ) from exc

    resultado = Resultado(
        guerreiro_id=guerreiro_id,
        atividade_id=atividade.id,
        aula_id=aula.id,
        momento_do_fato=momento_do_fato,
        producao=producao,
        desfecho=desfecho_valido,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(resultado)
    sessao.flush()

    creditar_pontuacao_do_resultado(sessao, resultado=resultado, atividade=atividade, trilha=trilha)
    creditar_ponto_extra_do_resultado(sessao, resultado=resultado)

    return resultado


@dataclass
class ResultadoDeclarado:
    """Um participante do lançamento da atividade realizada — os mesmos
    campos de `registrar_resultado`, sem `aula`, que o ato já fixa uma vez
    para todos (`RF-07-09`, `RF-02-35`)."""

    guerreiro_id: uuid.UUID | None
    atividade: Atividade | None
    momento_do_fato: datetime | None
    producao: str | None
    desfecho: str | None


def _registrar_resultados(
    sessao: Session, *, operador: Persona, aula: Aula, resultados: list[ResultadoDeclarado]
) -> list[Resultado]:
    """Montagem comum aos dois atos de lançamento — por aula, do Admin, e
    por atividade, do Mestre autor: grava um `Resultado` por participante,
    na mesma transação, sem decidir nada sobre reserva nem situação da aula
    — isso é exclusivo de quem chama (design — Decisions 1, riscos)."""
    return [
        registrar_resultado(
            sessao,
            operador=operador,
            aula=aula,
            guerreiro_id=entrada.guerreiro_id,
            atividade=entrada.atividade,
            momento_do_fato=entrada.momento_do_fato,
            producao=entrada.producao,
            desfecho=entrada.desfecho,
        )
        for entrada in resultados
    ]


def lancar_atividade_realizada(
    sessao: Session,
    *,
    operador: Persona,
    aula: Aula | None,
    resultados: list[ResultadoDeclarado],
) -> tuple[Aula, list[Resultado]]:
    """Ato **por aula**, restrito ao Admin: registra em uma operação os
    Resultados de todos os participantes, converte cada reserva da aula em
    baixa e leva a aula a **realizada** — não há operação de baixa separada
    deste ato (`RF-07-09`, `RF-02-35`, `RN-07-36`, `RF-01-16`, documento
    04 §1, design — Decisions 7).
    """
    if operador.papel != Papel.admin:
        raise PermissaoNegada(mensagem="Só o Admin lança a atividade realizada da aula.")
    if aula is None:
        raise ErroDeValidacao(mensagem="Lançamento exige uma aula.", campo="aula_id")
    if aula.situacao in _SITUACOES_COM_DESFECHO:
        raise ErroDeValidacao(
            mensagem="Esta aula já teve desfecho; o lançamento não se repete.",
            campo="situacao",
        )

    gravados = _registrar_resultados(sessao, operador=operador, aula=aula, resultados=resultados)

    consumir_reservas_da_aula(sessao, aula=aula, operador=operador)
    aula.situacao = SituacaoDaAula.realizada
    sessao.flush()

    return aula, gravados


def lancar_resultados_da_atividade(
    sessao: Session,
    *,
    operador: Persona,
    aula: Aula | None,
    atividade: Atividade | None,
    resultados: list[ResultadoDeclarado],
) -> list[Resultado]:
    """Ato **por atividade**, aberto ao Mestre autor da trilha dela ou ao
    Admin: registra em uma operação os Resultados de todos os participantes
    — a mesma `registrar_resultado` do ato por aula —, sem consumir reserva
    nem alterar a situação da aula, que permanecem exclusivas do lançamento
    por aula (`RF-09-43`, `RF-09-44`, `RF-09-49`, `RF-09-74`, design —
    Decisions 1). A posse é conferida aqui, antes de iterar os participantes,
    para que a lista vazia também recuse o Mestre que não é o autor
    (`RN-09-08`)."""
    if atividade is None:
        raise ErroDeValidacao(mensagem="Lançamento exige uma atividade.", campo="atividade_id")

    missao = sessao.get(Missao, atividade.missao_id)
    trilha = sessao.get(Trilha, missao.trilha_id)
    conferir_posse_da_trilha(trilha, operador)

    if aula is None:
        raise ErroDeValidacao(mensagem="Lançamento exige a aula em que aconteceu.", campo="aula_id")
    return _registrar_resultados(sessao, operador=operador, aula=aula, resultados=resultados)
