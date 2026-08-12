import base64
import json
import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from ..configuracao import Configuracao

# Versão fixa no Ciclo 01 — a chave não rotaciona (design — riscos), mas a
# versão já viaja com o dado para que a rotação futura não exija migração de
# estrutura, só recifragem.
VERSAO_DA_CHAVE = "1"
TAMANHO_DO_NONCE_EM_BYTES = 12


def _chave(configuracao: Configuracao) -> bytes:
    return base64.urlsafe_b64decode(configuracao.biometria_chave_de_cifragem)


def cifrar_descritor(descritor: list[float], configuracao: Configuracao) -> str:
    """AES-GCM: confidencialidade e detecção de adulteração no mesmo passo
    (design — decisões). O resultado guarda a versão da chave e o nonce
    junto ao texto cifrado, tudo codificado para caber em `Credencial.segredo`.
    """
    aesgcm = AESGCM(_chave(configuracao))
    nonce = os.urandom(TAMANHO_DO_NONCE_EM_BYTES)
    texto_cifrado = aesgcm.encrypt(nonce, json.dumps(descritor).encode("utf-8"), None)
    payload = base64.urlsafe_b64encode(nonce + texto_cifrado).decode("ascii")
    return f"{VERSAO_DA_CHAVE}:{payload}"


def decifrar_descritor(segredo: str, configuracao: Configuracao) -> list[float]:
    _versao, payload = segredo.split(":", 1)
    bruto = base64.urlsafe_b64decode(payload)
    nonce, texto_cifrado = bruto[:TAMANHO_DO_NONCE_EM_BYTES], bruto[TAMANHO_DO_NONCE_EM_BYTES:]
    aesgcm = AESGCM(_chave(configuracao))
    dados = aesgcm.decrypt(nonce, texto_cifrado, None)
    return json.loads(dados)
