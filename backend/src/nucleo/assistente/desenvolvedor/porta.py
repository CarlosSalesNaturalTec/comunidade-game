from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class MensagemDaConversa:
    """Um turno da conversa que a App 06 mantém no estado da página. Viaja com
    a pergunta para que o assistente aprofunde o tópico escolhido (PRD-03 §5.8)
    e **não é guardado em lugar nenhum** (PRD-03 §8, design — decisão 5)."""

    de: str
    texto: str


@dataclass(frozen=True)
class RespostaDoDesenvolvedor:
    """`desfecho` é do próprio modelo; a regra é quem decide o texto final da
    recusa fora do corpus (`RF-03-70`). `opcoes` são as escolhas do próximo
    passo — vazias, a regra completa com o conjunto fixo, e nenhuma mensagem
    sai sem pergunta (`RF-03-69`, design — decisão 6)."""

    desfecho: str
    resposta: str | None
    opcoes: tuple[str, ...]


class PortaDoAssistenteDoDesenvolvedor(ABC):
    """Porta própria, e não a do assistente de trilhas (design — decisão 3): lá
    a pergunta chega transcrita do aparelho e existe o desfecho
    `tarefa_escolar`, que aqui não faz sentido. `None` é a indisponibilidade —
    erro, demora ou resposta fora do formato esperado —, e quem chama a declara
    como o que é, nunca como recusa do domínio (`RF-03-72`, documento 99 §6
    invariante 25)."""

    @abstractmethod
    def responder(
        self,
        *,
        texto: str,
        corpus: str,
        historico: tuple[MensagemDaConversa, ...],
    ) -> RespostaDoDesenvolvedor | None: ...
