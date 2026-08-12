from datetime import timedelta
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

    # Sem valor padrão: o ambiente que não declarar não sobe (design — a
    # duração da sessão não tem valor padrão no código).
    identidade_fundador: str
    sessao_adulto_duracao: timedelta

    # Parâmetros da entrada do Guerreiro(a), também sem valor padrão: duração
    # da sessão curta, limiar de comparação do descritor, dimensão esperada
    # dele e a chave que cifra o _template_ (`RN-01-14`, design — decisões).
    sessao_guerreiro_duracao: timedelta
    biometria_dimensao_do_descritor: int
    biometria_limiar_de_comparacao: float
    biometria_chave_de_cifragem: str

    google_client_id: str = ""

    # Custo do Argon2id, ajustável por ambiente (design — decisão da senha).
    argon2_memoria_kib: int = 19_456
    argon2_iteracoes: int = 2
    argon2_paralelismo: int = 1


@lru_cache
def obter_configuracao() -> Configuracao:
    return Configuracao()
