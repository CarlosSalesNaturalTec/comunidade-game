"""O registro único de modelos (`nucleo.modelos`) precisa alcançar todo módulo
que define tabela.

Um teste de comportamento não pega essa falha: no processo da suíte, os demais
módulos de teste já importaram todos os modelos, e `Base.metadata` fica completa
por tabela. A falha só aparece num processo que importa **apenas** o ponto de
entrada — o `cli.py` da implantação —, onde uma chave estrangeira aponta para
tabela que ninguém registrou. Por isso a verificação aqui é estrutural.
"""

from pathlib import Path

import nucleo
from nucleo import modelos


def _modulos_com_tabela() -> set[str]:
    raiz = Path(nucleo.__file__).parent
    return {caminho.parent.name for caminho in raiz.glob("*/modelo.py")}


def test_registro_alcanca_todo_modulo_que_define_tabela():
    fonte = Path(modelos.__file__).read_text(encoding="utf-8")
    faltando = sorted(m for m in _modulos_com_tabela() if f"from .{m} import modelo" not in fonte)

    assert not faltando, (
        "módulos com tabela fora de `nucleo.modelos`: "
        f"{faltando}. Acrescente o import, senão a chave estrangeira que aponta "
        "para essas tabelas quebra no `cli.py` da implantação."
    )


def test_toda_chave_estrangeira_resolve_a_tabela_de_destino():
    from nucleo.banco import Base

    nao_resolvem = []
    for tabela in Base.metadata.tables.values():
        for chave in tabela.foreign_keys:
            try:
                # Acessar `.column` é o que dispara a resolução da tabela de
                # destino — é aqui que o erro de produção apareceu.
                _ = chave.column
            except Exception as erro:  # noqa: BLE001 — o teste reporta qualquer falha
                nao_resolvem.append(f"{tabela.name}.{chave.parent.name}: {erro}")

    assert not nao_resolvem, "chaves estrangeiras sem tabela de destino: " + "; ".join(nao_resolvem)
