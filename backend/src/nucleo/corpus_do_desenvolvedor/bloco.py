from dataclasses import dataclass


@dataclass(frozen=True)
class BlocoDoCorpus:
    """Unidade do corpus fechado da Área do Apoiador Desenvolvedor: a origem
    de onde saiu, o título da seção e o texto (design — decisão 1). O corpus
    inteiro tem ~1,8 milhão de caracteres; é em bloco que ele cabe no recorte
    por pergunta (decisão do fundador, 2026-09-29)."""

    origem: str
    titulo: str
    texto: str

    def como_dicionario(self) -> dict[str, str]:
        return {"origem": self.origem, "titulo": self.titulo, "texto": self.texto}
