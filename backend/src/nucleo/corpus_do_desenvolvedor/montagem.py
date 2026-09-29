"""Montagem do corpus do assistente do Desenvolvedor.

Roda **na esteira**, antes do `docker build`, e nunca em tempo de resposta: o
corpus é a documentação de `docs/`, o `README.md` da raiz e o contrato OpenAPI
que o próprio núcleo gera (documento 03 §8, decisão do fundador de 2026-09-26).
A imagem é construída com contexto em `backend/`, onde `docs/` não está — por
isso o artefato é escrito aqui e copiado pelo `Dockerfile` (design — decisão 1).
"""

import argparse
import json
import re
from pathlib import Path

from .bloco import BlocoDoCorpus

_TITULO_DE_SECAO = re.compile(r"^##\s+(.*)$", re.MULTILINE)
_TITULO_DO_ARQUIVO = re.compile(r"^#\s+(.*)$", re.MULTILINE)


def _titulo_do_arquivo(texto: str, caminho_relativo: str) -> str:
    achado = _TITULO_DO_ARQUIVO.search(texto)
    return achado.group(1).strip() if achado else caminho_relativo


def blocos_do_markdown(texto: str, caminho_relativo: str) -> list[BlocoDoCorpus]:
    """Uma seção `##` por bloco. O que vem antes da primeira seção — a abertura
    do documento — vira um bloco com o título do arquivo, para que documento
    curto sem seção nenhuma não se perca."""
    titulo_do_documento = _titulo_do_arquivo(texto, caminho_relativo)
    cortes = list(_TITULO_DE_SECAO.finditer(texto))

    blocos: list[BlocoDoCorpus] = []
    abertura = texto[: cortes[0].start()] if cortes else texto
    if abertura.strip():
        blocos.append(
            BlocoDoCorpus(
                origem=caminho_relativo,
                titulo=titulo_do_documento,
                texto=abertura.strip(),
            )
        )

    for indice, corte in enumerate(cortes):
        fim = cortes[indice + 1].start() if indice + 1 < len(cortes) else len(texto)
        corpo = texto[corte.end() : fim].strip()
        if not corpo:
            continue
        blocos.append(
            BlocoDoCorpus(
                origem=caminho_relativo,
                titulo=f"{titulo_do_documento} — {corte.group(1).strip()}",
                texto=corpo,
            )
        )
    return blocos


def blocos_da_documentacao(raiz: Path) -> list[BlocoDoCorpus]:
    """`docs/` e o `README.md` da raiz — os dois já públicos. Nada de
    `backend/`, de `openspec/` nem de qualquer arquivo fora dessas origens
    (design — Risks)."""
    blocos: list[BlocoDoCorpus] = []
    for arquivo in sorted((raiz / "docs").rglob("*.md")):
        relativo = arquivo.relative_to(raiz).as_posix()
        blocos.extend(blocos_do_markdown(arquivo.read_text(encoding="utf-8"), relativo))

    readme = raiz / "README.md"
    if readme.exists():
        blocos.extend(blocos_do_markdown(readme.read_text(encoding="utf-8"), "README.md"))
    return blocos


def blocos_do_contrato(contrato: dict) -> list[BlocoDoCorpus]:
    """Uma rota do contrato OpenAPI por bloco, com método, caminho, resumo e
    descrição — é o que um desenvolvedor de terceiro precisa ler para decidir
    pedir a chave (documento 09, "Documentação da API em OpenAPI")."""
    blocos: list[BlocoDoCorpus] = []
    for caminho, operacoes in sorted(contrato.get("paths", {}).items()):
        for metodo, operacao in sorted(operacoes.items()):
            if not isinstance(operacao, dict):
                continue
            linhas = [f"{metodo.upper()} {caminho}"]
            for campo in ("summary", "description"):
                valor = operacao.get(campo)
                if valor:
                    linhas.append(str(valor).strip())
            blocos.append(
                BlocoDoCorpus(
                    origem="contrato OpenAPI",
                    titulo=f"{metodo.upper()} {caminho}",
                    texto="\n\n".join(linhas),
                )
            )
    return blocos


def _contrato_do_nucleo() -> dict:
    """Importar `nucleo.principal` **não** exige ambiente completo: a
    conferência da implantação mora no `lifespan` (change
    `bucket-de-armazenamento-em-producao`, design — decisão 2). Por isso o
    contrato sai aqui, na esteira, sem serviço de pé."""
    from ..principal import app

    return app.openapi()


def montar(raiz: Path) -> list[BlocoDoCorpus]:
    return blocos_da_documentacao(raiz) + blocos_do_contrato(_contrato_do_nucleo())


def escrever(blocos: list[BlocoDoCorpus], saida: Path) -> None:
    saida.parent.mkdir(parents=True, exist_ok=True)
    saida.write_text(
        json.dumps([bloco.como_dicionario() for bloco in blocos], ensure_ascii=False),
        encoding="utf-8",
    )


def principal(argumentos: list[str] | None = None) -> int:
    analisador = argparse.ArgumentParser(description=__doc__)
    analisador.add_argument("--raiz", type=Path, required=True, help="Raiz do repositório.")
    analisador.add_argument("--saida", type=Path, required=True, help="Artefato JSON de saída.")
    opcoes = analisador.parse_args(argumentos)

    blocos = montar(opcoes.raiz)
    escrever(blocos, opcoes.saida)
    print(f"Corpus do Desenvolvedor: {len(blocos)} blocos em {opcoes.saida}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(principal())
