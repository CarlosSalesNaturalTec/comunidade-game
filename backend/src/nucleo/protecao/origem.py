import hashlib
import secrets
import threading
from datetime import datetime, timedelta

from starlette.requests import Request

# O sal roda por período maior que a maior janela de origem (a do
# formulário, 1 hora) — sem isso a rotação sempre cairia dentro de alguma
# janela em andamento (design — Decisions).
PERIODO_DE_ROTACAO_DO_SAL = timedelta(hours=2)
RETENCAO_DO_SAL_ANTERIOR = timedelta(hours=1)


class SalRotativo:
    """Sal do resumo de origem (`RN-01-45`). Roda por período e retém o sal
    anterior por uma janela, para que a virada não zere quem já estava
    sendo freado — os baldes contados com o sal anterior seguem válidos até
    expirarem, e as chamadas novas já usam o sal novo (design — Decisions).
    """

    def __init__(
        self,
        periodo_de_rotacao: timedelta = PERIODO_DE_ROTACAO_DO_SAL,
        retencao_do_sal_anterior: timedelta = RETENCAO_DO_SAL_ANTERIOR,
    ) -> None:
        self._periodo_de_rotacao = periodo_de_rotacao
        self._retencao_do_sal_anterior = retencao_do_sal_anterior
        self._trava = threading.Lock()
        self._sal_atual = secrets.token_bytes(32)
        self._sal_anterior: bytes | None = None
        self._trocado_em: datetime | None = None

    def resumos(self, endereco_de_rede: str, agora: datetime) -> tuple[str, str | None]:
        """Devolve o resumo com o sal atual e, enquanto durar a retenção, o
        resumo com o sal anterior."""
        with self._trava:
            if self._trocado_em is None:
                self._trocado_em = agora
            elif agora - self._trocado_em >= self._periodo_de_rotacao:
                self._sal_anterior = self._sal_atual
                self._sal_atual = secrets.token_bytes(32)
                self._trocado_em = agora
            elif (
                self._sal_anterior is not None
                and agora - self._trocado_em >= self._retencao_do_sal_anterior
            ):
                self._sal_anterior = None

            resumo_atual = _resumir(endereco_de_rede, self._sal_atual)
            resumo_anterior = (
                _resumir(endereco_de_rede, self._sal_anterior)
                if self._sal_anterior is not None
                else None
            )
            return resumo_atual, resumo_anterior


def _resumir(endereco_de_rede: str, sal: bytes) -> str:
    return hashlib.sha256(sal + endereco_de_rede.encode("utf-8")).hexdigest()


def obter_endereco_de_rede(request: Request) -> str:
    """O endereço de quem chamou, sem cair em cookie ou identificador
    persistente (`RN-01-45`)."""
    return request.client.host if request.client is not None else ""
