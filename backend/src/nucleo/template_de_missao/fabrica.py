from typing import Annotated

from fastapi import Depends

from ..configuracao import Configuracao, obter_configuracao
from .local import TemplateDeMissaoLocal
from .nuvem import TemplateDeMissaoNaNuvem
from .porta import PortaDoTemplateDeMissao


def obter_porta_do_template_de_missao(configuracao: Configuracao) -> PortaDoTemplateDeMissao:
    """Escolhe o adaptador pelo ambiente, no mesmo padrão de
    `armazenamento.fabrica`: local fora de produção, sem exigir credencial;
    **DeepSeek** em produção. Esta porta manda só texto, e é a que o
    documento 03 §1.12 destina ao provedor de menor custo — deixa, por isso,
    de compartilhar credencial com `producoes` e `assistente`, que leem
    imagem e áudio e seguem no Gemini."""
    if configuracao.ambiente == "producao":
        return TemplateDeMissaoNaNuvem(
            chave_de_api=configuracao.deepseek_chave_de_api,
            modelo=configuracao.deepseek_modelo,
        )
    return TemplateDeMissaoLocal()


def dependencia_do_template_de_missao(
    configuracao: Annotated[Configuracao, Depends(obter_configuracao)],
) -> PortaDoTemplateDeMissao:
    return obter_porta_do_template_de_missao(configuracao)
