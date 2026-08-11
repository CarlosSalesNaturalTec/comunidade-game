from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

Ambiente = Literal["desenvolvimento", "producao"]


class Configuracao(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="CG_")

    ambiente: Ambiente = "desenvolvimento"
    dsn_banco: str = "postgresql+psycopg://comunidade:comunidade@localhost:5432/comunidade_game"

    paginacao_tamanho_padrao: int = 25
    paginacao_tamanho_teto: int = 100


@lru_cache
def obter_configuracao() -> Configuracao:
    return Configuracao()
