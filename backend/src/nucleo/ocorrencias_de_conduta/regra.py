import uuid
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from ..aulas.modelo import Aula
from ..erros import ErroDeValidacao
from ..personas.modelo import Persona
from ..pontuacao.modelo import PontoRegular
from ..pontuacao.regra import debitar_ponto_regular
from ..trilhas.modelo import Atividade, FormatoDeAtividade, Missao, Trilha
from ..trilhas.regra import conferir_posse_da_trilha
from .modelo import OcorrenciaDeConduta

# Documento 11 §5, única fonte do valor: 5 pontos por ocorrência, com teto de
# 10 por Guerreiro(a) e por aula presencial. Quem lança não arbitra o valor —
# a rota nem aceita o campo na entrada (design — Decisions 3).
VALOR_DA_OCORRENCIA_DE_CONDUTA = 5
TETO_POR_GUERREIRO_E_AULA = 10


def lancar_ocorrencia_de_conduta(
    sessao: Session,
    *,
    operador: Persona,
    aula: Aula | None,
    atividade: Atividade | None,
    guerreiro_id: uuid.UUID | None,
    motivo: str | None,
    momento_do_fato: datetime | None,
) -> OcorrenciaDeConduta:
    """Grava a ocorrência e debita, na mesma operação, o ponto regular da
    trilha derivada de atividade → missão → trilha — só o Mestre autor da
    trilha ou o Admin lançam, pela mesma conferência de posse do Resultado
    (`RF-09-46`, `RF-01-57`, `RN-09-08`, `RN-09-09`, 11 §5).
    """
    if atividade is None:
        raise ErroDeValidacao(
            mensagem="Ocorrência de conduta exige uma atividade.", campo="atividade_id"
        )

    missao = sessao.get(Missao, atividade.missao_id)
    trilha = sessao.get(Trilha, missao.trilha_id)
    conferir_posse_da_trilha(trilha, operador)

    if aula is None:
        raise ErroDeValidacao(
            mensagem="Ocorrência de conduta exige a aula em que aconteceu.", campo="aula_id"
        )
    # Aula é sempre o encontro presencial; a atividade on-line acontece entre
    # encontros e nunca pertence a uma aula (`RN-09-08`, "presencial do
    # encontro e on-line entre encontros").
    if atividade.formato != FormatoDeAtividade.presencial:
        raise ErroDeValidacao(
            mensagem="Esta atividade é on-line e não pertence a nenhuma aula.",
            campo="atividade_id",
        )
    if guerreiro_id is None:
        raise ErroDeValidacao(
            mensagem="Ocorrência de conduta exige o Guerreiro(a).", campo="guerreiro_id"
        )
    if not motivo or not motivo.strip():
        raise ErroDeValidacao(mensagem="Ocorrência de conduta exige o motivo.", campo="motivo")
    if momento_do_fato is None:
        raise ErroDeValidacao(
            mensagem="Ocorrência de conduta exige a data do fato.", campo="momento_do_fato"
        )

    soma_existente = (
        sessao.query(func.coalesce(func.sum(OcorrenciaDeConduta.valor), 0))
        .filter(
            OcorrenciaDeConduta.aula_id == aula.id,
            OcorrenciaDeConduta.guerreiro_id == guerreiro_id,
        )
        .scalar()
    )
    if soma_existente + VALOR_DA_OCORRENCIA_DE_CONDUTA > TETO_POR_GUERREIRO_E_AULA:
        raise ErroDeValidacao(
            mensagem="O teto de pontuação negativa desta aula para este Guerreiro(a) já foi "
            "alcançado.",
            campo="guerreiro_id",
        )

    # O que o débito vai tirar de fato, depois do aparo em zero de
    # `debitar_ponto_regular` (`RN-01-55`) — gravado na inserção porque o
    # saldo muda depois, e o ranking do fim de ciclo precisa devolver
    # exatamente isso, não o nominal (design — decisões 3 e 4, `RF-02-100`).
    saldo_antes = (
        sessao.query(PontoRegular.total)
        .filter_by(guerreiro_id=guerreiro_id, trilha_id=trilha.id, poder_id=None)
        .scalar()
    ) or 0
    valor_debitado = min(VALOR_DA_OCORRENCIA_DE_CONDUTA, saldo_antes)

    ocorrencia = OcorrenciaDeConduta(
        guerreiro_id=guerreiro_id,
        aula_id=aula.id,
        atividade_id=atividade.id,
        valor=VALOR_DA_OCORRENCIA_DE_CONDUTA,
        valor_debitado=valor_debitado,
        motivo=motivo,
        momento_do_fato=momento_do_fato,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(ocorrencia)
    sessao.flush()

    debitar_ponto_regular(
        sessao,
        guerreiro_id=guerreiro_id,
        valor=VALOR_DA_OCORRENCIA_DE_CONDUTA,
        trilha_id=trilha.id,
    )

    return ocorrencia
