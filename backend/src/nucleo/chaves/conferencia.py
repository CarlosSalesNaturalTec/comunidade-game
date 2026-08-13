import hashlib
import hmac
import uuid
from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.orm import Session

from ..banco import obter_sessao
from ..configuracao import Configuracao, obter_configuracao
from ..erros import ChaveInvalida
from .modelo import ChaveDeAplicacao, SituacaoDaChave
from .segredo import ChaveMalFormada, calcular_resumo, decompor_chave

NOME_DO_CABECALHO = "X-Chave-Aplicacao"

# Usados quando o cabeçalho está ausente ou mal formado, para que o mesmo caminho
# de código — uma busca por índice, um SHA-256, uma comparação — rode sempre,
# sem o ramo curto que denunciaria por que a chave foi recusada.
_ID_FANTASMA = uuid.UUID("00000000-0000-0000-0000-000000000000")
_SEGREDO_FANTASMA = ""
_RESUMO_FANTASMA = hashlib.sha256(b"comunidade-game-resumo-fantasma").hexdigest()


@dataclass(frozen=True)
class ContextoDaChave:
    id: str
    aplicacao: str
    ambiente: str
    natureza: str


def _buscar_por_id(sessao: Session, id_da_chave: uuid.UUID) -> ChaveDeAplicacao | None:
    return sessao.get(ChaveDeAplicacao, id_da_chave)


def exigir_chave_de_aplicacao(
    request: Request,
    sessao: Annotated[Session, Depends(obter_sessao)],
    configuracao: Annotated[Configuracao, Depends(obter_configuracao)],
) -> ContextoDaChave:
    cabecalho = request.headers.get(NOME_DO_CABECALHO)

    id_da_chave = _ID_FANTASMA
    segredo = _SEGREDO_FANTASMA
    if cabecalho:
        try:
            _, id_bruto, segredo = decompor_chave(cabecalho)
            id_da_chave = uuid.UUID(id_bruto)
        except (ChaveMalFormada, ValueError):
            id_da_chave, segredo = _ID_FANTASMA, _SEGREDO_FANTASMA

    registro = _buscar_por_id(sessao, id_da_chave)

    resumo_esperado = registro.resumo_do_segredo if registro is not None else _RESUMO_FANTASMA
    resumo_calculado = calcular_resumo(segredo)
    resumo_confere = hmac.compare_digest(resumo_calculado, resumo_esperado)

    ambiente_confere = registro is not None and registro.ambiente == configuracao.ambiente
    situacao_confere = registro is not None and registro.situacao == SituacaoDaChave.vigente

    tudo_certo = registro is not None and resumo_confere and ambiente_confere and situacao_confere

    if not tudo_certo:
        raise ChaveInvalida()

    contexto = ContextoDaChave(
        id=str(registro.id),
        aplicacao=registro.aplicacao,
        ambiente=registro.ambiente,
        natureza=registro.natureza.value,
    )
    # A trilha de auditoria (RF-01-29) lê este contexto de `request.state`
    # depois de `call_next`, sem recalcular a chave — nenhuma rota muda.
    request.state.contexto_da_chave = contexto
    return contexto
