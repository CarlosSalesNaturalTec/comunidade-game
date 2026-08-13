from typing import Annotated

from fastapi import Depends

from ..configuracao import Configuracao, obter_configuracao
from .disco import ArmazenamentoEmDisco
from .nuvem import ArmazenamentoNoCloudStorage
from .porta import PortaDeArmazenamento


def obter_porta_de_armazenamento(configuracao: Configuracao) -> PortaDeArmazenamento:
    """Escolhe o adaptador pelo ambiente (documento 03 §1): disco fora de
    produção, sem exigir credencial de nuvem; Cloud Storage em produção."""
    if configuracao.ambiente == "producao":
        return ArmazenamentoNoCloudStorage(configuracao.armazenamento_bucket_cloud_storage)
    return ArmazenamentoEmDisco(configuracao.armazenamento_diretorio_local)


def dependencia_de_armazenamento(
    configuracao: Annotated[Configuracao, Depends(obter_configuracao)],
) -> PortaDeArmazenamento:
    return obter_porta_de_armazenamento(configuracao)
