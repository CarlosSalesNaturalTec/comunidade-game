from .banco import obter_fabrica_de_sessao
from .chaves.semeadura import semear_ambiente
from .configuracao import obter_configuracao


def semear() -> None:
    """Comando de implantação: `python -m nucleo.cli`. Roda uma vez por ambiente."""
    configuracao = obter_configuracao()
    fabrica = obter_fabrica_de_sessao()
    with fabrica() as sessao:
        segredos = semear_ambiente(sessao, configuracao.ambiente)

    if not segredos:
        print(f"Nenhuma chave nova: o ambiente '{configuracao.ambiente}' já está semeado.")
        return

    print(
        f"Chaves emitidas para o ambiente '{configuracao.ambiente}' — "
        "anote agora, o segredo não aparece de novo:"
    )
    for aplicacao, segredo in segredos.items():
        print(f"  {aplicacao}: {segredo}")


if __name__ == "__main__":
    semear()
