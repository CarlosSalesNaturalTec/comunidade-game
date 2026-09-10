from typing import Annotated

from fastapi import Depends

from ..configuracao import (
    Configuracao,
    ConfiguracaoDeProducaoIncompleta,
    obter_configuracao,
)
from .disco import ArmazenamentoEmDisco
from .nuvem import ArmazenamentoNoCloudStorage
from .porta import PortaDeArmazenamento


def obter_porta_de_armazenamento(configuracao: Configuracao) -> PortaDeArmazenamento:
    """Escolhe o adaptador pelo ambiente (documento 03 §1): disco fora de
    produção, sem exigir credencial de nuvem; Cloud Storage em produção.

    Em produção **não há queda para disco**: o disco do Cloud Run é efêmero e
    não sobrevive ao deploy seguinte, então aceitar o envio e perdê-lo depois
    seria pior que recusar. Bucket não declarado é erro de implantação e
    interrompe o arranque com o nome da variável que falta — antes, a falta
    virava `IndexError` na validação do nome do bucket, numa requisição
    qualquer e para um usuário (change `bucket-de-armazenamento-em-producao`,
    design — decisão 2)."""
    if configuracao.ambiente == "producao":
        if not configuracao.armazenamento_bucket_cloud_storage:
            raise ConfiguracaoDeProducaoIncompleta(
                "CG_ARMAZENAMENTO_BUCKET_CLOUD_STORAGE não foi declarada, e em produção o "
                "armazenamento não cai para disco: declare o bucket do Cloud Storage."
            )
        return ArmazenamentoNoCloudStorage(configuracao.armazenamento_bucket_cloud_storage)
    return ArmazenamentoEmDisco(
        configuracao.armazenamento_diretorio_local,
        configuracao.armazenamento_diretorio_sessoes_locais,
    )


def dependencia_de_armazenamento(
    configuracao: Annotated[Configuracao, Depends(obter_configuracao)],
) -> PortaDeArmazenamento:
    return obter_porta_de_armazenamento(configuracao)
