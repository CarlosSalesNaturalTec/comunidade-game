import uuid
from datetime import datetime

from sqlalchemy.orm import Session

from ..erros import ErroDeValidacao
from ..personas.modelo import Persona
from ..ponto_extra.regra import creditar_ponto_extra_do_resultado
from ..pontuacao.regra import creditar_pontuacao_do_resultado
from ..trilhas.modelo import Atividade, Missao, Trilha
from ..trilhas.regra import conferir_posse_da_trilha
from .modelo import DesfechoDoResultado, Resultado


def registrar_resultado(
    sessao: Session,
    *,
    operador: Persona,
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
    `RF-01-03`, 11 §4).
    """
    if atividade is None:
        raise ErroDeValidacao(mensagem="Resultado exige uma atividade.", campo="atividade_id")

    missao = sessao.get(Missao, atividade.missao_id)
    trilha = sessao.get(Trilha, missao.trilha_id)
    conferir_posse_da_trilha(trilha, operador)

    if guerreiro_id is None:
        raise ErroDeValidacao(mensagem="Resultado exige um Guerreiro(a).", campo="guerreiro_id")
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
