"""Corpus do assistente do Desenvolvedor: montagem pela esteira e recorte por
pergunta (`RF-03-70`, `RN-03-30`, change
`2026-09-29-area-do-apoiador-desenvolvedor`)."""

import json
from pathlib import Path

from nucleo.corpus_do_desenvolvedor.bloco import BlocoDoCorpus
from nucleo.corpus_do_desenvolvedor.leitura import carregar, recortar
from nucleo.corpus_do_desenvolvedor.montagem import (
    blocos_da_documentacao,
    blocos_do_contrato,
    blocos_do_markdown,
    escrever,
)

RAIZ_DO_REPOSITORIO = Path(__file__).resolve().parents[2]


def test_markdown_vira_um_bloco_por_secao_com_a_abertura_a_parte():
    texto = "# Documento\n\nAbertura.\n\n## Primeira\n\nCorpo um.\n\n## Segunda\n\nCorpo dois.\n"

    blocos = blocos_do_markdown(texto, "docs/exemplo.md")

    assert [bloco.titulo for bloco in blocos] == [
        "Documento",
        "Documento — Primeira",
        "Documento — Segunda",
    ]
    assert blocos[1].texto == "Corpo um."
    assert all(bloco.origem == "docs/exemplo.md" for bloco in blocos)


def test_montagem_cobre_as_origens_decididas_e_nenhuma_outra():
    """`docs/`, o README da raiz e o contrato OpenAPI — e nada de `backend/`
    nem de `openspec/` (documento 03 §8, design — Risks)."""
    documentacao = blocos_da_documentacao(RAIZ_DO_REPOSITORIO)
    contrato = blocos_do_contrato(
        {"paths": {"/v1/exemplo": {"get": {"summary": "Exemplo", "description": "Descrição."}}}}
    )

    origens = {bloco.origem for bloco in documentacao}
    assert any(origem.startswith("docs/") for origem in origens)
    assert not any(origem.startswith(("backend/", "openspec/")) for origem in origens)
    if (RAIZ_DO_REPOSITORIO / "README.md").exists():
        assert "README.md" in origens
    assert contrato[0].titulo == "GET /v1/exemplo"
    assert "Descrição." in contrato[0].texto


def test_readme_da_raiz_entra_quando_existe(tmp_path):
    """O README da raiz é uma das três origens decididas (documento 03 §8), e
    ainda não existe neste repositório: a montagem o inclui quando ele nascer e
    não quebra enquanto não nasce."""
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "um.md").write_text("# Um\n\nCorpo.\n", encoding="utf-8")

    sem_readme = blocos_da_documentacao(tmp_path)
    (tmp_path / "README.md").write_text("# Projeto\n\nApresentação.\n", encoding="utf-8")
    com_readme = blocos_da_documentacao(tmp_path)

    assert "README.md" not in {bloco.origem for bloco in sem_readme}
    assert "README.md" in {bloco.origem for bloco in com_readme}


def test_recorte_para_no_teto_e_nao_inventa_texto_de_fora(tmp_path):
    blocos = [
        BlocoDoCorpus(origem="docs/a.md", titulo=f"Chave de aplicação {indice}", texto="x" * 400)
        for indice in range(20)
    ]

    recorte = recortar(blocos, pergunta="Como funciona a chave de aplicação?", teto=1_000)

    assert len(recorte) <= 1_000
    assert recorte
    assert set(recorte.split()) <= set(
        " ".join(f"[{b.origem}] {b.titulo}\n{b.texto}" for b in blocos).split()
    )


def test_bloco_sem_sobreposicao_fica_de_fora():
    blocos = [
        BlocoDoCorpus(origem="docs/a.md", titulo="Chave de aplicação", texto="Sobre a chave."),
        BlocoDoCorpus(origem="docs/b.md", titulo="Trilhas e missões", texto="Sobre trilhas."),
    ]

    recorte = recortar(blocos, pergunta="Como peço a chave?", teto=10_000)

    assert "Sobre a chave." in recorte
    assert "Sobre trilhas." not in recorte


def test_sem_artefato_o_corpus_e_vazio(tmp_path):
    """Comportamento declarado, não exceção silenciosa: sem artefato toda
    pergunta sai como fora do corpus (design — decisão 1)."""
    assert carregar(tmp_path / "nao-existe.json") == []


def test_artefato_escrito_volta_igual(tmp_path):
    blocos = [BlocoDoCorpus(origem="README.md", titulo="Título", texto="Corpo.")]
    saida = tmp_path / "corpus.json"

    escrever(blocos, saida)

    assert json.loads(saida.read_text(encoding="utf-8")) == [
        {"origem": "README.md", "titulo": "Título", "texto": "Corpo."}
    ]
    assert carregar(saida) == blocos
