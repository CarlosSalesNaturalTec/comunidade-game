import re

from .porta import (
    MensagemDaConversa,
    PortaDoAssistenteDoDesenvolvedor,
    RespostaDoDesenvolvedor,
)

_PALAVRA = re.compile(r"\w{4,}")


class AssistenteDoDesenvolvedorLocal(PortaDoAssistenteDoDesenvolvedor):
    """Adaptador padrão fora de produção: classifica por sobreposição simples
    de palavras com o recorte do corpus, sem chamar rede nem exigir credencial
    — o mesmo precedente de `assistente.local` (design — decisão 3)."""

    def responder(
        self,
        *,
        texto: str,
        corpus: str,
        historico: tuple[MensagemDaConversa, ...],
    ) -> RespostaDoDesenvolvedor | None:
        palavras = set(_PALAVRA.findall(texto.lower()))
        corpus_normalizado = corpus.lower()
        if not corpus.strip() or not any(palavra in corpus_normalizado for palavra in palavras):
            return RespostaDoDesenvolvedor(desfecho="fora_do_corpus", resposta=None, opcoes=())

        return RespostaDoDesenvolvedor(
            desfecho="respondida",
            resposta=f"Resposta simulada com base na documentação do projeto: {corpus[:280]}",
            opcoes=("Como a API se autentica", "Quais são as oito aplicações"),
        )
