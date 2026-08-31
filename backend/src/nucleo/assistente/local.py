import re

from .porta import PortaDoAssistente, RespostaDoAssistente

_TERMOS_DE_TAREFA_ESCOLAR = (
    "dever de casa",
    "tarefa de casa",
    "tarefa escolar",
    "trabalho da escola",
    "trabalho de casa",
    "prova da escola",
)


class AssistenteDeTrilhasLocal(PortaDoAssistente):
    """Adaptador padrão fora de produção (design — Migration Plan): classifica
    por sobreposição simples de palavras com o corpus, sem chamar rede nem
    exigir credencial — o mesmo precedente de `producoes.local`."""

    def responder(
        self, *, texto: str | None, arquivo: bytes | None, corpus: str
    ) -> RespostaDoAssistente | None:
        if texto is not None:
            transcricao_da_pergunta = texto
        else:
            transcricao_da_pergunta = (
                f"Transcrição simulada da pergunta em áudio ({len(arquivo or b'')} bytes)."
            )

        pergunta_normalizada = transcricao_da_pergunta.strip().lower()
        if any(termo in pergunta_normalizada for termo in _TERMOS_DE_TAREFA_ESCOLAR):
            return RespostaDoAssistente(
                transcricao_da_pergunta=transcricao_da_pergunta,
                desfecho="tarefa_escolar",
                resposta=None,
            )

        palavras = re.findall(r"\w{4,}", pergunta_normalizada)
        corpus_normalizado = corpus.lower()
        if palavras and any(palavra in corpus_normalizado for palavra in palavras):
            return RespostaDoAssistente(
                transcricao_da_pergunta=transcricao_da_pergunta,
                desfecho="respondida",
                resposta=f"Resposta simulada com base no material da trilha: {corpus[:280]}",
            )

        return RespostaDoAssistente(
            transcricao_da_pergunta=transcricao_da_pergunta,
            desfecho="fora_do_corpus",
            resposta=None,
        )
