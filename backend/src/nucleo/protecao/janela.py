import threading
from collections import defaultdict, deque
from datetime import datetime, timedelta


class JanelaDeslizante:
    """Mapa em memória de chave de contagem para fila de instantes —
    descarta na leitura o que já saiu da janela. A cota por chave e o freio
    por origem compartilham esta implementação (design — Decisions:
    "N por janela" em vez de _token bucket_).
    """

    def __init__(self) -> None:
        self._filas: dict[str, deque[datetime]] = defaultdict(deque)
        self._trava = threading.Lock()

    def _descartar_expirados(self, fila: deque[datetime], limite: datetime) -> None:
        while fila and fila[0] <= limite:
            fila.popleft()

    def registrar_e_contar(
        self, chave_de_contagem: str, agora: datetime, duracao_da_janela: timedelta
    ) -> int:
        """Registra um instante novo e devolve quantos, incluindo este,
        ainda estão dentro da janela."""
        with self._trava:
            fila = self._filas[chave_de_contagem]
            self._descartar_expirados(fila, agora - duracao_da_janela)
            fila.append(agora)
            return len(fila)

    def contar(self, chave_de_contagem: str, agora: datetime, duracao_da_janela: timedelta) -> int:
        """Só lê a contagem corrente, sem registrar instante novo — usada
        para somar o que resta da fila do sal anterior na virada (design —
        Decisions)."""
        with self._trava:
            fila = self._filas.get(chave_de_contagem)
            if fila is None:
                return 0
            self._descartar_expirados(fila, agora - duracao_da_janela)
            return len(fila)
