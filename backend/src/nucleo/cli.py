from . import modelos as _modelos  # noqa: F401 — popula Base.metadata com todas as tabelas
from .banco import obter_fabrica_de_sessao
from .chaves.semeadura import semear_ambiente
from .configuracao import obter_configuracao
from .personas.semeadura import semear_admin_fundador
from .termos.semeadura import semear_termo_vigente


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

        # Imprime ANTES de qualquer outra escrita: `semear_ambiente` já fez
        # commit, e o segredo em claro só existe nesta variável — o banco
        # guarda apenas o resumo (`RN-01-35`). Falha posterior deixaria chave
        # vigente cujo segredo ninguém conhece, sem caminho de recuperação
        # além de revogar e reemitir.
        _relatar_chaves(configuracao.ambiente, segredos)

        persona_admin = semear_admin_fundador(sessao, configuracao.identidade_fundador)
        termo = semear_termo_vigente(sessao, configuracao)

    if persona_admin is not None:
        print(f"Persona Admin do fundador semeada: {configuracao.identidade_fundador}")
    else:
        print("Persona Admin do fundador já existia: nada semeado.")

    if termo is not None:
        print(
            f"Termo semeado na versão vigente: {configuracao.consentimento_versao_vigente_do_termo}"
        )
    else:
        print("Termo da versão vigente já existia: nada semeado.")


def _relatar_chaves(ambiente: str, segredos: dict[str, str]) -> None:
    if not segredos:
        print(f"Nenhuma chave nova: o ambiente '{ambiente}' já está semeado.")
        return

    print(
        f"Chaves emitidas para o ambiente '{ambiente}' — "
        "anote agora, o segredo não aparece de novo:"
    )
    for aplicacao, segredo in segredos.items():
        print(f"  {aplicacao}: {segredo}")


if __name__ == "__main__":
    semear()
