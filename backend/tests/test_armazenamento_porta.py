"""A escolha do adaptador de armazenamento e a guarda da implantação.

O adaptador de nuvem não tinha teste nenhum, e foi por aí que a implantação
subiu sem `CG_ARMAZENAMENTO_BUCKET_CLOUD_STORAGE`: em produção a fábrica
devolve **sempre** o adaptador de nuvem — não há queda para disco, ao
contrário do que o README afirmava —, e o nome vazio estourava `IndexError`
na validação do bucket, numa requisição qualquer. Oito módulos responderam
500 por isso (change `bucket-de-armazenamento-em-producao`, decisão 2).
"""

from datetime import timedelta

import pytest

from nucleo.armazenamento.disco import ArmazenamentoEmDisco
from nucleo.armazenamento.fabrica import obter_porta_de_armazenamento
from nucleo.armazenamento.nuvem import ArmazenamentoNoCloudStorage
from nucleo.configuracao import (
    Configuracao,
    ConfiguracaoDeProducaoIncompleta,
    conferir_configuracao_de_producao,
)

CHAVE_DE_CIFRAGEM = "a" * 32


def _configuracao(**extras) -> Configuracao:
    return Configuracao(
        _env_file=None,
        identidade_fundador="fundador-de-teste@example.org",
        sessao_adulto_duracao=timedelta(hours=8),
        sessao_guerreiro_duracao=timedelta(hours=4),
        biometria_dimensao_do_descritor=4,
        biometria_limiar_de_comparacao=0.5,
        biometria_chave_de_cifragem=CHAVE_DE_CIFRAGEM,
        **extras,
    )


def test_fora_de_producao_a_porta_e_disco_sem_exigir_credencial(tmp_path):
    """`RF-09-19` e o desenho de sempre: desenvolvimento e a esteira não
    precisam de bucket nem de credencial de nuvem."""
    porta = obter_porta_de_armazenamento(
        _configuracao(
            ambiente="desenvolvimento",
            armazenamento_diretorio_local=str(tmp_path / "arquivos"),
            armazenamento_diretorio_sessoes_locais=str(tmp_path / "sessoes"),
        )
    )

    assert isinstance(porta, ArmazenamentoEmDisco)


def test_fora_de_producao_o_bucket_vazio_nao_atrapalha(tmp_path):
    porta = obter_porta_de_armazenamento(
        _configuracao(
            ambiente="desenvolvimento",
            armazenamento_bucket_cloud_storage="",
            armazenamento_diretorio_local=str(tmp_path / "arquivos"),
            armazenamento_diretorio_sessoes_locais=str(tmp_path / "sessoes"),
        )
    )

    assert isinstance(porta, ArmazenamentoEmDisco)


def test_em_producao_sem_bucket_a_fabrica_recusa_nomeando_a_variavel():
    """Nunca `IndexError`, e nunca queda silenciosa para disco: o disco do
    Cloud Run é efêmero e perderia o envio no deploy seguinte."""
    with pytest.raises(ConfiguracaoDeProducaoIncompleta) as excinfo:
        obter_porta_de_armazenamento(_configuracao(ambiente="producao"))

    assert "CG_ARMAZENAMENTO_BUCKET_CLOUD_STORAGE" in str(excinfo.value)


def test_o_arranque_recusa_producao_sem_bucket():
    """A mesma falta derruba o arranque, e não uma requisição de usuário: o
    Cloud Run mantém a revisão anterior servindo quando a nova não sobe."""
    with pytest.raises(ConfiguracaoDeProducaoIncompleta) as excinfo:
        conferir_configuracao_de_producao(_configuracao(ambiente="producao"))

    assert "CG_ARMAZENAMENTO_BUCKET_CLOUD_STORAGE" in str(excinfo.value)


def test_o_arranque_passa_em_producao_com_bucket_declarado():
    conferir_configuracao_de_producao(
        _configuracao(ambiente="producao", armazenamento_bucket_cloud_storage="um-bucket")
    )


def test_o_arranque_nao_exige_bucket_fora_de_producao():
    conferir_configuracao_de_producao(_configuracao(ambiente="desenvolvimento"))


def test_o_arranque_nao_exige_chave_de_ia():
    """As portas de IA ficam de fora da guarda de propósito: ali a
    indisponibilidade é comportamento previsto e a tela avisa em linguagem
    simples (`RF-09-91`, `RN-04-21`, `RN-05-35`)."""
    conferir_configuracao_de_producao(
        _configuracao(
            ambiente="producao",
            armazenamento_bucket_cloud_storage="um-bucket",
            gemini_chave_de_api="",
        )
    )


def test_o_lifespan_recusa_o_servico_em_producao_sem_bucket(monkeypatch):
    """A guarda é do `lifespan`, não do corpo de `criar_app`: importar o
    módulo continua não exigindo ambiente completo, e é o serviço que deixa
    de ficar pronto — o Cloud Run mantém a revisão anterior no ar."""
    from fastapi.testclient import TestClient

    from nucleo.configuracao import obter_configuracao
    from nucleo.principal import criar_app

    for variavel, valor in {
        "CG_AMBIENTE": "producao",
        "CG_IDENTIDADE_FUNDADOR": "fundador-de-teste@example.org",
        "CG_SESSAO_ADULTO_DURACAO": "PT8H",
        "CG_SESSAO_GUERREIRO_DURACAO": "PT4H",
        "CG_BIOMETRIA_DIMENSAO_DO_DESCRITOR": "4",
        "CG_BIOMETRIA_LIMIAR_DE_COMPARACAO": "0.5",
        "CG_BIOMETRIA_CHAVE_DE_CIFRAGEM": CHAVE_DE_CIFRAGEM,
    }.items():
        monkeypatch.setenv(variavel, valor)
    monkeypatch.delenv("CG_ARMAZENAMENTO_BUCKET_CLOUD_STORAGE", raising=False)
    obter_configuracao.cache_clear()

    try:
        with pytest.raises(ConfiguracaoDeProducaoIncompleta):
            with TestClient(criar_app()):
                pass
    finally:
        obter_configuracao.cache_clear()


# --- A origem de quem envia, declarada na abertura da sessão --------------


class _BlobDeMentira:
    """O que o cliente do Cloud Storage expõe à abertura da sessão, e nada
    mais: guardar a chamada basta para conferir o que o adaptador manda."""

    def __init__(self) -> None:
        self.chamada: dict | None = None

    def create_resumable_upload_session(self, **argumentos) -> str:
        self.chamada = argumentos
        return "https://armazenamento-de-mentira/sessao"


class _BucketDeMentira:
    def __init__(self, blob: _BlobDeMentira) -> None:
        self._blob = blob
        self.referencia: str | None = None

    def blob(self, referencia: str) -> _BlobDeMentira:
        self.referencia = referencia
        return self._blob


def _adaptador_de_nuvem(blob: _BlobDeMentira) -> ArmazenamentoNoCloudStorage:
    """Sem passar pelo `__init__`, que instancia o cliente do Cloud Storage:
    a esteira não tem credencial de nuvem nem precisa ter."""
    adaptador = ArmazenamentoNoCloudStorage.__new__(ArmazenamentoNoCloudStorage)
    adaptador._bucket = _BucketDeMentira(blob)
    return adaptador


def test_a_nuvem_abre_a_sessao_declarando_a_origem_recebida():
    """`RF-09-19`: o envio parte do navegador, e o bucket é outra origem —
    a sessão nasce sabendo de onde o envio virá, senão o navegador o barra
    antes de qualquer byte (change `cors-do-bucket-de-armazenamento`)."""
    blob = _BlobDeMentira()

    endereco = _adaptador_de_nuvem(blob).abrir_sessao(
        referencia="perguntas-do-desbloqueio/uma-pergunta/imagem",
        tipo_mime="image/png",
        tamanho_declarado=1024,
        origem="https://mestre.comunidadegame.org",
    )

    assert endereco == "https://armazenamento-de-mentira/sessao"
    assert blob.chamada["origin"] == "https://mestre.comunidadegame.org"
    assert blob.chamada["content_type"] == "image/png"
    assert blob.chamada["size"] == 1024


def test_a_nuvem_abre_a_sessao_mesmo_sem_origem():
    """Quem admite ou recusa a origem é o bucket, não o núcleo: sem o
    cabeçalho a sessão abre assim mesmo, e o bucket decide (`RF-09-19`)."""
    blob = _BlobDeMentira()

    _adaptador_de_nuvem(blob).abrir_sessao(
        referencia="conteudos/um-conteudo/arquivo",
        tipo_mime="video/mp4",
        tamanho_declarado=2048,
    )

    assert blob.chamada["origin"] is None


def test_o_disco_ignora_a_origem_e_segue_devolvendo_endereco_relativo(tmp_path):
    """No adaptador de disco o envio volta ao próprio núcleo, cujo CORS já
    o atende: a origem não tem uso, e o endereço continua relativo."""
    disco = ArmazenamentoEmDisco(str(tmp_path / "arquivos"), str(tmp_path / "sessoes"))

    endereco = disco.abrir_sessao(
        referencia="conteudos/um-conteudo/arquivo",
        tipo_mime="image/png",
        tamanho_declarado=16,
        origem="https://mestre.comunidadegame.org",
    )

    assert endereco.startswith("/v1/armazenamento/sessoes/")
