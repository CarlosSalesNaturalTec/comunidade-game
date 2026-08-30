from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class LeituraDaProducao:
    transcricao: str
    devolutiva: str | None


class PortaDaProducaoDaMissao(ABC):
    """Interface da leitura e da devolutiva da produção — local, sem rede,
    fora de produção; Gemini em produção (design — decisão 4). `None` é a
    indisponibilidade: erro, demora ou resposta fora do formato esperado, e
    quem chama trata o desfecho conforme a forma da entrega (design —
    decisão 5), nunca como falha da operação.
    """

    @abstractmethod
    def ler(
        self, *, forma: str, texto: str | None, arquivo: bytes | None, producao_esperada: str
    ) -> LeituraDaProducao | None: ...
