import base64
import hashlib
import hmac
import re
import secrets

from sqlalchemy.orm import Session

from ..configuracao import Configuracao
from ..erros import PinBloqueado, PinNaoCadastrado, PinRecusado
from ..personas.modelo import Persona
from ..sessoes.modelo import Sessao

ALGORITMO = "PBKDF2-SHA256"
TAMANHO_DO_SAL = 16
FORMATO_DO_PIN = re.compile(r"^[0-9]{4}$")

# Cinco erros seguidos bloqueiam o PIN na sessão de trabalho (`RN-01-59`,
# `RN-04-38`, documento 03 §1.1).
ERROS_ATE_O_BLOQUEIO = 5


def _b64(dado: bytes) -> str:
    return base64.b64encode(dado).decode("ascii")


def _derivar(pin: str, sal: bytes, iteracoes: int) -> bytes:
    """PBKDF2-HMAC-SHA256: a única derivação lenta que o núcleo e o
    `SubtleCrypto` do App 01 fazem igual, sem dependência nova (design —
    decisão 1)."""
    return hashlib.pbkdf2_hmac("sha256", pin.encode("ascii"), sal, iteracoes)


def gerar_verificador(pin: str, configuracao: Configuracao) -> dict:
    sal = secrets.token_bytes(TAMANHO_DO_SAL)
    iteracoes = configuracao.pin_iteracoes
    return {
        "algoritmo": ALGORITMO,
        "iteracoes": iteracoes,
        "sal": _b64(sal),
        "resumo": _b64(_derivar(pin, sal, iteracoes)),
    }


def pin_confere(verificador: dict, pin: str) -> bool:
    sal = base64.b64decode(verificador["sal"])
    calculado = _derivar(pin, sal, int(verificador["iteracoes"]))
    return hmac.compare_digest(calculado, base64.b64decode(verificador["resumo"]))


def cadastrar_pin(persona: Persona, pin: str, configuracao: Configuracao) -> None:
    """A troca não pede o PIN antigo: quem autentica o adulto é o login da
    sessão (`RF-01-75`)."""
    persona.pin_verificador = gerar_verificador(pin, configuracao)


def conferir_pin_da_sessao(
    sessao_bd: Session, *, persona: Persona, sessao: Sessao, pin: str
) -> None:
    """Na ordem bloqueio → cadastro → resumo (design — decisão 2): o PIN
    certo não desbloqueia, e nada aqui depende do nick. O erro conta na
    sessão e o acerto zera, porque o bloqueio é de erros **seguidos**
    (`RN-01-59`). Grava a contagem antes de recusar, para que a recusa não
    desfaça o próprio registro."""
    if sessao.erros_de_pin_seguidos >= ERROS_ATE_O_BLOQUEIO:
        raise PinBloqueado()
    if persona.pin_verificador is None:
        raise PinNaoCadastrado()
    if not pin_confere(persona.pin_verificador, pin):
        sessao.erros_de_pin_seguidos += 1
        sessao_bd.commit()
        if sessao.erros_de_pin_seguidos >= ERROS_ATE_O_BLOQUEIO:
            raise PinBloqueado()
        raise PinRecusado()
    if sessao.erros_de_pin_seguidos:
        sessao.erros_de_pin_seguidos = 0
        sessao_bd.commit()
