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

    # Cota de leitura por faixa da chave, janela fixa de uma hora (`RF-01-55`,
    # 03 §8). Só os tetos por faixa são parâmetro; a janela é estrutural.
    protecao_cota_do_projeto_por_hora: int = 6_000
    protecao_cota_de_terceiro_por_hora: int = 600

    # Prazo de apresentação da URL da chave de terceiro, contado da emissão
    # (`RN-01-36`, design — o prazo é configuração).
    prazo_de_apresentacao_dias: int = 30

    # Freio por origem, com limite e janela próprios por superfície, e o
    # atraso progressivo comum às duas (`RF-01-65`, `RN-01-27`, 03 §8).
    protecao_freio_nick_limite: int = 30
    protecao_freio_nick_janela: timedelta = timedelta(minutes=10)
    protecao_freio_formulario_limite: int = 3
    protecao_freio_formulario_janela: timedelta = timedelta(hours=1)
    protecao_freio_atraso_inicial: timedelta = timedelta(seconds=2)
    protecao_freio_atraso_fator_de_crescimento: float = 2.0
    protecao_freio_atraso_teto: timedelta = timedelta(minutes=15)

    # Porta de armazenamento do comprovante (design — Decisions): disco fora
    # de produção, sem exigir credencial de nuvem; Cloud Storage em produção
    # (documento 03 §1).
    armazenamento_diretorio_local: str = "./armazenamento"
    armazenamento_bucket_cloud_storage: str = ""

    # Diretório das sessões de envio retomável, fora de produção — separado
    # do diretório final, para que o arquivo em costura nunca seja servido
    # antes de o envio ser confirmado (`RF-09-19`, design — Migration Plan).
    armazenamento_diretorio_sessoes_locais: str = "./armazenamento-sessoes"

    # Rótulo do ciclo corrente, declarado na implantação — não é entidade,
    # não tem calendário (`RF-01-42`, `RF-01-43`, design — Decisions).
    ciclo_rotulo: str = "Ciclo 01"

    # Versão vigente do termo de consentimento, carimbada pelo núcleo em todo
    # registro — a porta HTTP não a recebe do cliente (`RF-04-12`, `RN-01-12`,
    # documento 09 — decisão do fundador, 2026-08-24). Trocar o termo é
    # trocar esta configuração; o registro já gravado continua afirmando a
    # versão que valia quando foi feito.
    consentimento_versao_vigente_do_termo: str = "2026-08"

    # Piso de coletores distintos do recorte publicado do território — abaixo
    # dele, o recorte sobe ao nível acima (`RF-08-28`, `RN-08-24`, documento
    # 02 §1).
    territorio_piso_de_coletores_distintos: int = 3

    # Licença do conjunto exportado do território e o texto da declaração da
    # contribuição à meta 17.18 — nunca embutidos no código (`RF-08-27`,
    # documento 03 §12.3, documento 04 §4).
    territorio_licenca: str = "CC BY-SA"
    territorio_declaracao_meta_17_18: str = (
        "Este conjunto é a contribuição do Comunidade Game à meta 17.18 da Agenda 2030: "
        "dado local, desagregado, datado e de guarda permanente sobre um território periférico."
    )


@lru_cache
def obter_configuracao() -> Configuracao:
    return Configuracao()
