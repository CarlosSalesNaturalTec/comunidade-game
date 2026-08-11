import hashlib
import secrets

PREFIXO = "cg"


class ChaveMalFormada(Exception):
    pass


def gerar_segredo() -> str:
    """256 bits de entropia aleatória, codificados para caber num cabeçalho HTTP."""
    return secrets.token_urlsafe(32)


def montar_chave_completa(ambiente: str, id_da_chave: str, segredo: str) -> str:
    return f"{PREFIXO}_{ambiente}_{id_da_chave}.{segredo}"


def calcular_resumo(segredo: str) -> str:
    return hashlib.sha256(segredo.encode("utf-8")).hexdigest()


def decompor_chave(chave_completa: str) -> tuple[str, str, str]:
    """Devolve (ambiente, id_da_chave, segredo) a partir de `cg_<ambiente>_<id>.<segredo>`.

    O prefixo público leva o núcleo direto ao registro por índice, sem varredura.
    Formato inválido levanta `ChaveMalFormada` — o chamador trata isso como chave
    inexistente, sem abrir um ramo curto de recusa.
    """
    try:
        prefixo_e_id, segredo = chave_completa.split(".", 1)
        prefixo, ambiente, id_da_chave = prefixo_e_id.split("_", 2)
        if prefixo != PREFIXO or not segredo or not id_da_chave:
            raise ValueError
        return ambiente, id_da_chave, segredo
    except ValueError as exc:
        raise ChaveMalFormada from exc
