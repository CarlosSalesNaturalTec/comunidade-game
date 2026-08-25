import re
from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response

from ..erros import ErroDeValidacao, NaoEncontrado
from .disco import ArmazenamentoEmDisco
from .fabrica import dependencia_de_armazenamento
from .porta import PortaDeArmazenamento

roteador = APIRouter()

_PADRAO_CONTENT_RANGE = re.compile(r"bytes (?:(\d+)-(\d+)|\*)/(\d+)")

# A chave só existe pelo que `ArmazenamentoEmDisco.chave_da_sessao` produz —
# letras, dígitos e os separadores da referência. Barra, ponto duplo ou
# qualquer outro caractere indicam manipulação da URL, não uma sessão
# legítima; a recusa aqui é o que impede a chave de escapar do diretório de
# sessões ao virar caminho de arquivo (design — Risks).
_PADRAO_CHAVE_VALIDA = re.compile(r"^[A-Za-z0-9_.-]+$")


@roteador.put("/armazenamento/sessoes/{chave}")
async def receber_parte_da_sessao_rota(
    chave: str,
    requisicao: Request,
    armazenamento: Annotated[PortaDeArmazenamento, Depends(dependencia_de_armazenamento)],
) -> Response:
    """Rota local do protocolo `Content-Range` que o Cloud Storage já fala
    em produção — só o adaptador de disco a usa; fora dele a chamada nunca
    conclui a sessão (`RF-09-19`, design — decisão 2). Recebe cada parte na
    posição declarada e costura o arquivo temporário; uma chamada de
    consulta (`bytes */{total}`, sem corpo) devolve o que já foi recebido,
    o que sustenta a retomada depois da queda de rede."""
    if not isinstance(armazenamento, ArmazenamentoEmDisco):
        raise NaoEncontrado(mensagem="Rota disponível apenas fora de produção.")
    if _PADRAO_CHAVE_VALIDA.fullmatch(chave) is None or ".." in chave:
        raise NaoEncontrado(mensagem="Sessão de envio não encontrada.")

    cabecalho = requisicao.headers.get("Content-Range", "")
    casamento = _PADRAO_CONTENT_RANGE.fullmatch(cabecalho)
    if casamento is None:
        raise ErroDeValidacao(
            mensagem="Cabeçalho Content-Range ausente ou fora do formato esperado.",
            campo="content_range",
        )

    total_declarado = armazenamento.tamanho_declarado(chave=chave)
    if total_declarado is None:
        raise NaoEncontrado(mensagem="Sessão de envio não encontrada.")

    inicio = casamento.group(1)
    if inicio is not None:
        corpo = await requisicao.body()
        recebidos = armazenamento.receber_parte(chave=chave, inicio=int(inicio), conteudo=corpo)
    else:
        recebidos = armazenamento.bytes_recebidos(chave=chave)

    if recebidos >= total_declarado:
        referencia = _referencia_da_chave(chave)
        armazenamento.concluir_sessao(chave=chave, referencia=referencia)
        return Response(status_code=200)

    cabecalhos = {"Range": f"bytes=0-{recebidos - 1}"} if recebidos > 0 else {}
    return Response(status_code=308, headers=cabecalhos)


def _referencia_da_chave(chave: str) -> str:
    return chave.replace("__", "/")
