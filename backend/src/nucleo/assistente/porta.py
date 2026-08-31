from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class RespostaDoAssistente:
    transcricao_da_pergunta: str
    desfecho: str
    resposta: str | None


class PortaDoAssistente(ABC):
    """Interface da consulta ao assistente — local, sem rede, fora de
    produção; Gemini em produção (design — decisão 1). `None` é a
    indisponibilidade: erro, demora ou resposta fora do formato esperado, e
    quem chama trata o desfecho como resposta indisponível, nunca como
    falha da operação (design — decisão 5). O desfecho vem do próprio
    modelo — a regra é quem decide o texto final de `fora_do_corpus` e de
    `tarefa_escolar` (design — decisão 3).
    """

    @abstractmethod
    def responder(
        self, *, texto: str | None, arquivo: bytes | None, corpus: str
    ) -> RespostaDoAssistente | None: ...
