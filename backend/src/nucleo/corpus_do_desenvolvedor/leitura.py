"""Leitura do artefato de corpus e o recorte por pergunta.

Em tempo de resposta o núcleo **só lê** o que a esteira montou: nenhuma
requisição a terceiro (documento 03 §8). Sem artefato — desenvolvimento e
teste — o corpus é vazio, e toda pergunta sai como fora do corpus, que é
comportamento declarado e não exceção silenciosa (design — decisão 1).
"""

import json
import logging
import re
from functools import lru_cache
from pathlib import Path

from .bloco import BlocoDoCorpus

logger = logging.getLogger("nucleo.corpus_do_desenvolvedor")

# Palavra com menos de quatro letras não distingue bloco nenhum — o mesmo
# corte do adaptador local do assistente de trilhas.
_PALAVRA = re.compile(r"\w{4,}")


def carregar(caminho: Path) -> list[BlocoDoCorpus]:
    if not caminho.exists():
        logger.warning(
            "Artefato de corpus do Desenvolvedor ausente em %s: o corpus está vazio e "
            "toda pergunta sairá como fora do corpus.",
            caminho,
        )
        return []
    dados = json.loads(caminho.read_text(encoding="utf-8"))
    return [
        BlocoDoCorpus(origem=item["origem"], titulo=item["titulo"], texto=item["texto"])
        for item in dados
    ]


@lru_cache(maxsize=4)
def carregar_uma_vez(caminho: Path) -> tuple[BlocoDoCorpus, ...]:
    """O artefato não muda enquanto o contêiner vive — ele nasce com a imagem.
    Ler a cada pergunta custaria o arquivo inteiro por chamada."""
    return tuple(carregar(caminho))


def _palavras(texto: str) -> set[str]:
    return set(_PALAVRA.findall(texto.lower()))


def _pontuar(bloco: BlocoDoCorpus, palavras_da_pergunta: set[str]) -> int:
    """O título pesa o dobro: é onde está o assunto do bloco, e é o que
    distingue a seção certa de uma menção de passagem no corpo."""
    do_titulo = _palavras(bloco.titulo) & palavras_da_pergunta
    do_texto = _palavras(bloco.texto) & palavras_da_pergunta
    return 2 * len(do_titulo) + len(do_texto)


def recortar(
    blocos: tuple[BlocoDoCorpus, ...] | list[BlocoDoCorpus], *, pergunta: str, teto: int
) -> str:
    """Recorte por pergunta, com teto (decisão do fundador, 2026-09-29): pontua
    cada bloco pela sobreposição de palavras, ordena e acumula até o teto de
    caracteres. Bloco sem sobreposição nenhuma não entra — servir texto que
    não responde só encarece a pergunta."""
    palavras_da_pergunta = _palavras(pergunta)
    if not palavras_da_pergunta:
        return ""

    pontuados = [
        (pontuacao, bloco)
        for bloco in blocos
        if (pontuacao := _pontuar(bloco, palavras_da_pergunta)) > 0
    ]
    pontuados.sort(key=lambda par: (-par[0], par[1].origem, par[1].titulo))

    escolhidos: list[str] = []
    caracteres = 0
    for _, bloco in pontuados:
        trecho = f"[{bloco.origem}] {bloco.titulo}\n{bloco.texto}"
        if caracteres + len(trecho) > teto:
            continue
        escolhidos.append(trecho)
        caracteres += len(trecho)

    return "\n\n".join(escolhidos)
