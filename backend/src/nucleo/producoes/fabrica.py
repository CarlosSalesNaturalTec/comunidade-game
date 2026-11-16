from typing import Annotated

from fastapi import Depends

from ..configuracao import Configuracao, obter_configuracao
from .local import ProducaoDaMissaoLocal
from .nuvem import ProducaoDaMissaoNaNuvem
from .porta import PortaDaProducaoDaMissao


def obter_porta_da_producao_da_missao(configuracao: Configuracao) -> PortaDaProducaoDaMissao:
    """Escolhe o adaptador pelo ambiente: local fora de produção, sem
    exigir credencial; Gemini em produção, pela chave única do projeto — a
    mesma que `assistente` lê (documento 03 §1.12, design — decisão 4)."""
    if configuracao.ambiente == "producao":
        return ProducaoDaMissaoNaNuvem(
            chave_de_api=configuracao.gemini_chave_de_api,
            modelo=configuracao.gemini_modelo,
        )
    return ProducaoDaMissaoLocal()


def dependencia_da_producao_da_missao(
    configuracao: Annotated[Configuracao, Depends(obter_configuracao)],
) -> PortaDaProducaoDaMissao:
    return obter_porta_da_producao_da_missao(configuracao)
