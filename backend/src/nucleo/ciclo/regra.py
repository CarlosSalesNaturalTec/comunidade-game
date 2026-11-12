from dataclasses import dataclass

from sqlalchemy import update
from sqlalchemy.orm import Session

from ..cuidado_do_bem.regra import expirar_customizacoes_pendentes
from ..ocorrencias_de_conduta.modelo import OcorrenciaDeConduta
from ..tempo import agora


@dataclass
class ResultadoDoEncerramento:
    ocorrencias_expurgadas: int
    customizacoes_expiradas: int


def encerrar_ciclo(sessao: Session) -> ResultadoDoEncerramento:
    """Expurga o motivo de toda ocorrência de conduta que ainda o guarda e
    carimba `encerrada_em`, num só `UPDATE` de Core — não passa pelo ORM, e
    por isso não colide com a recusa de `UPDATE` que os `event.listen` de
    mapper mantêm para todo o resto (`RF-02-99`, `RF-02-100`, design —
    decisões 2 e 5). Não cria nada, não declara o ciclo seguinte e não grava
    indicador (`RN-02-30`). O filtro por `motivo IS NOT NULL` torna o ato
    idempotente: executá-lo de novo sem ocorrência nova não altera nada.

    Desde 2026-11-12, expira também todo registro de customização do kit
    ainda pendente — o mesmo `UPDATE` de Core, idempotente pelo filtro da
    situação (`RF-01-86`). Devolve quantos de cada um.
    """
    resultado = sessao.execute(
        update(OcorrenciaDeConduta.__table__)
        .where(OcorrenciaDeConduta.__table__.c.motivo.is_not(None))
        .values(motivo=None, encerrada_em=agora())
    )
    expiradas = expirar_customizacoes_pendentes(sessao)
    sessao.commit()
    return ResultadoDoEncerramento(
        ocorrencias_expurgadas=resultado.rowcount, customizacoes_expiradas=expiradas
    )
