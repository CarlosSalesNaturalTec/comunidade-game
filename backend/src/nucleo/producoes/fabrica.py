from typing import Annotated

from fastapi import Depends

from ..configuracao import Configuracao, obter_configuracao
from .local import ProducaoDaMissaoLocal
from .nuvem import ProducaoDaMissaoNaNuvem
from .porta import PortaDaProducaoDaMissao


def obter_porta_da_producao_da_missao(configuracao: Configuracao) -> PortaDaProducaoDaMissao:
    """Escolhe o adaptador pelo ambiente, no mesmo padrão de
    `template_de_missao.fabrica`: local fora de produção, sem exigir
    credencial; Gemini em produção, com a mesma chave e o mesmo modelo do
    template da missão (documento 03 §1.12, design — decisão 4)."""
    if configuracao.ambiente == "producao":
        return ProducaoDaMissaoNaNuvem(
            chave_de_api=configuracao.template_de_missao_gemini_chave_de_api,
            modelo=configuracao.template_de_missao_gemini_modelo,
        )
    return ProducaoDaMissaoLocal()


def dependencia_da_producao_da_missao(
    configuracao: Annotated[Configuracao, Depends(obter_configuracao)],
) -> PortaDaProducaoDaMissao:
    return obter_porta_da_producao_da_missao(configuracao)
