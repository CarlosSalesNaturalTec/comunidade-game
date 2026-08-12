from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from ..configuracao import Configuracao


def _hasher(configuracao: Configuracao) -> PasswordHasher:
    """Argon2id, não o SHA-256 das chaves: senha de pessoa não tem 256 bits de
    entropia aleatória (design — decisões)."""
    return PasswordHasher(
        time_cost=configuracao.argon2_iteracoes,
        memory_cost=configuracao.argon2_memoria_kib,
        parallelism=configuracao.argon2_paralelismo,
    )


def calcular_hash(senha: str, configuracao: Configuracao) -> str:
    return _hasher(configuracao).hash(senha)


def conferir_senha(hash_guardado: str, senha: str, configuracao: Configuracao) -> bool:
    try:
        return _hasher(configuracao).verify(hash_guardado, senha)
    except VerifyMismatchError:
        return False
