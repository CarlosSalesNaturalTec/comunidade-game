from typing import Annotated

from fastapi import Depends

from ...configuracao import Configuracao, obter_configuracao
from .local import AssistenteDoDesenvolvedorLocal
from .nuvem import AssistenteDoDesenvolvedorNaNuvem
from .porta import PortaDoAssistenteDoDesenvolvedor


def obter_porta(configuracao: Configuracao) -> PortaDoAssistenteDoDesenvolvedor:
    """Mesmo padrão de `assistente.fabrica`: local fora de produção, sem exigir
    credencial; Gemini em produção, pela chave única do projeto (documento 03
    §1.12, `RN-03-31`)."""
    if configuracao.ambiente == "producao":
        return AssistenteDoDesenvolvedorNaNuvem(
            chave_de_api=configuracao.gemini_chave_de_api,
            modelo=configuracao.gemini_modelo,
        )
    return AssistenteDoDesenvolvedorLocal()


def dependencia_do_assistente_do_desenvolvedor(
    configuracao: Annotated[Configuracao, Depends(obter_configuracao)],
) -> PortaDoAssistenteDoDesenvolvedor:
    return obter_porta(configuracao)
