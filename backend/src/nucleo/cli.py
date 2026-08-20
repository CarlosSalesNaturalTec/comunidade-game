from . import modelos as _modelos  # noqa: F401 — popula Base.metadata com todas as tabelas
from .banco import obter_fabrica_de_sessao
from .chaves.semeadura import semear_ambiente
from .configuracao import obter_configuracao
from .personas.semeadura import semear_admin_fundador


def semear() -> None:
    """Comando de implantação: `python -m nucleo.cli`. Roda uma vez por
    ambiente — converge as chaves e a persona Admin do fundador (`RF-01-61`).
    Sem `CG_IDENTIDADE_FUNDADOR` declarada, `obter_configuracao` já falha de
    forma visível antes de qualquer semeadura.
    """
    configuracao = obter_configuracao()
    fabrica = obter_fabrica_de_sessao()
    with fabrica() as sessao:
        segredos = semear_ambiente(sessao, configuracao.ambiente)
        persona_admin = semear_admin_fundador(sessao, configuracao.identidade_fundador)

    if not segredos:
        print(f"Nenhuma chave nova: o ambiente '{configuracao.ambiente}' já está semeado.")
    else:
        print(
            f"Chaves emitidas para o ambiente '{configuracao.ambiente}' — "
            "anote agora, o segredo não aparece de novo:"
        )
        for aplicacao, segredo in segredos.items():
            print(f"  {aplicacao}: {segredo}")

    if persona_admin is not None:
        print(f"Persona Admin do fundador semeada: {configuracao.identidade_fundador}")
    else:
        print("Persona Admin do fundador já existia: nada semeado.")


if __name__ == "__main__":
    semear()
