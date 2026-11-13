"""Conferência de uso de uma linha por qualquer chave estrangeira do esquema.

Serve a exclusão dos tipos de catálogo, que só apaga o tipo nunca usado
(`RN-07-40`, `RN-08-30`). A lista de tabelas sai de `Base.metadata`, não de
uma lista à mão: tabela nova que referencie o tipo entra na conferência sem
tocar aqui (design — decisão 4).
"""

import uuid

from sqlalchemy import Table, exists, select
from sqlalchemy.orm import Session

from . import modelos as _modelos  # noqa: F401 — popula Base.metadata
from .banco import Base


def esta_em_uso(
    sessao: Session,
    *,
    tabela: Table,
    identificador: uuid.UUID,
    tabelas_ignoradas: frozenset[str] = frozenset(),
) -> bool:
    """Verdadeiro se alguma linha, de qualquer tabela fora de
    `tabelas_ignoradas`, aponta para `identificador` em `tabela`."""
    for outra in Base.metadata.tables.values():
        if outra.name in tabelas_ignoradas:
            continue
        for chave in outra.foreign_keys:
            if chave.column.table is not tabela:
                continue
            consulta = select(exists().where(chave.parent == identificador))
            if sessao.execute(consulta).scalar():
                return True
    return False
