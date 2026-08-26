from sqlalchemy import update
from sqlalchemy.orm import Session

from ..ocorrencias_de_conduta.modelo import OcorrenciaDeConduta
from ..tempo import agora


def encerrar_ciclo(sessao: Session) -> int:
    """Expurga o motivo de toda ocorrência de conduta que ainda o guarda e
    carimba `encerrada_em`, num só `UPDATE` de Core — não passa pelo ORM, e
    por isso não colide com a recusa de `UPDATE` que os `event.listen` de
    mapper mantêm para todo o resto (`RF-02-99`, `RF-02-100`, design —
    decisões 2 e 5). Não cria nada, não declara o ciclo seguinte e não grava
    indicador (`RN-02-30`). O filtro por `motivo IS NOT NULL` torna o ato
    idempotente: executá-lo de novo sem ocorrência nova não altera nada.
    Devolve quantas ocorrências foram expurgadas.
    """
    resultado = sessao.execute(
        update(OcorrenciaDeConduta.__table__)
        .where(OcorrenciaDeConduta.__table__.c.motivo.is_not(None))
        .values(motivo=None, encerrada_em=agora())
    )
    sessao.commit()
    return resultado.rowcount
