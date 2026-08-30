from typing import Annotated

from fastapi import Depends

from ..configuracao import Configuracao, obter_configuracao
from .local import TemplateDeMissaoLocal
from .nuvem import TemplateDeMissaoNaNuvem
from .porta import PortaDoTemplateDeMissao


def obter_porta_do_template_de_missao(configuracao: Configuracao) -> PortaDoTemplateDeMissao:
    """Escolhe o adaptador pelo ambiente, no mesmo padrão de
    `armazenamento.fabrica`: local fora de produção, sem exigir credencial;
    Gemini em produção (documento 03 §1.12, design — decisão 2)."""
    if configuracao.ambiente == "producao":
        return TemplateDeMissaoNaNuvem(
            chave_de_api=configuracao.template_de_missao_gemini_chave_de_api,
            modelo=configuracao.template_de_missao_gemini_modelo,
        )
    return TemplateDeMissaoLocal()


def dependencia_do_template_de_missao(
    configuracao: Annotated[Configuracao, Depends(obter_configuracao)],
) -> PortaDoTemplateDeMissao:
    return obter_porta_do_template_de_missao(configuracao)
