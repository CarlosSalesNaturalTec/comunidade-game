from datetime import timedelta
from typing import Annotated

from fastapi import Depends, Request

from ..chaves.conferencia import ContextoDaChave, exigir_chave_de_aplicacao
from ..chaves.modelo import NaturezaDaChave
from ..configuracao import Configuracao, obter_configuracao
from ..erros import CotaDeLeituraExcedida
from ..tempo import agora
from .estado import obter_ou_criar
from .janela import JanelaDeslizante

_METODOS_DE_LEITURA = frozenset({"GET", "HEAD"})
_JANELA_DA_COTA = timedelta(hours=1)


def exigir_cota_de_leitura(
    request: Request,
    contexto: Annotated[ContextoDaChave, Depends(exigir_chave_de_aplicacao)],
    configuracao: Annotated[Configuracao, Depends(obter_configuracao)],
) -> None:
    """Cota de leitura por faixa da chave (`RF-01-55`). Declarada depois de
    `exigir_chave_de_aplicacao` em `incluir_roteador_de_dados`, para que
    chave inválida receba 401 antes de a cota contar qualquer coisa
    (design — Decisions, delta de `chave-de-aplicacao`).
    """
    if request.method not in _METODOS_DE_LEITURA:
        return

    cota = (
        configuracao.protecao_cota_do_projeto_por_hora
        if contexto.natureza == NaturezaDaChave.do_projeto
        else configuracao.protecao_cota_de_terceiro_por_hora
    )
    janela = obter_ou_criar(request, "protecao_janela_da_cota", JanelaDeslizante)
    total = janela.registrar_e_contar(contexto.id, agora(), _JANELA_DA_COTA)
    if total > cota:
        raise CotaDeLeituraExcedida()
