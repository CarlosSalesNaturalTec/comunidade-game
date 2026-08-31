from typing import Annotated

from fastapi import Depends

from ..configuracao import Configuracao, obter_configuracao
from .local import AssistenteDeTrilhasLocal
from .nuvem import AssistenteDeTrilhasNaNuvem
from .porta import PortaDoAssistente


def obter_porta_do_assistente(configuracao: Configuracao) -> PortaDoAssistente:
    """Escolhe o adaptador pelo ambiente, no mesmo padrão de
    `producoes.fabrica`: local fora de produção, sem exigir credencial;
    Gemini em produção, com a mesma chave e o mesmo modelo do
    `template_de_missao` (documento 03 §1.12, design — decisão 1)."""
    if configuracao.ambiente == "producao":
        return AssistenteDeTrilhasNaNuvem(
            chave_de_api=configuracao.template_de_missao_gemini_chave_de_api,
            modelo=configuracao.template_de_missao_gemini_modelo,
        )
    return AssistenteDeTrilhasLocal()


def dependencia_do_assistente(
    configuracao: Annotated[Configuracao, Depends(obter_configuracao)],
) -> PortaDoAssistente:
    return obter_porta_do_assistente(configuracao)
