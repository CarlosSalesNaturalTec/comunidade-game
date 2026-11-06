from collections.abc import Callable
from datetime import timedelta
from typing import Annotated

from fastapi import Depends, Request

from ..configuracao import Configuracao, obter_configuracao
from ..erros import FreioPorOrigemAcionado
from ..tempo import agora
from .estado import obter_ou_criar
from .janela import JanelaDeslizante
from .origem import SalRotativo, obter_endereco_de_rede

# Limite dos passos de crescimento considerados no cálculo do atraso — generoso
# o bastante para qualquer teto plausível, e o que evita estourar a potência
# quando a mesma origem insiste um número enorme de vezes.
_PASSOS_MAXIMOS_DE_CRESCIMENTO = 50

_CONFIGURACAO_POR_SUPERFICIE: dict[str, Callable[[Configuracao], tuple[int, timedelta]]] = {
    "consulta_por_nick": lambda c: (c.protecao_freio_nick_limite, c.protecao_freio_nick_janela),
    "formulario_participacao": lambda c: (
        c.protecao_freio_formulario_limite,
        c.protecao_freio_formulario_janela,
    ),
    "formulario_dados": lambda c: (
        c.protecao_freio_formulario_limite,
        c.protecao_freio_formulario_janela,
    ),
}


def _formatar_tempo_em_linguagem_simples(segundos: int) -> str:
    if segundos < 60:
        return f"{segundos} segundo{'s' if segundos != 1 else ''}"
    minutos = round(segundos / 60)
    return f"{minutos} minuto{'s' if minutos != 1 else ''}"


def _calcular_atraso(excesso: int, configuracao: Configuracao) -> timedelta:
    passos = min(excesso - 1, _PASSOS_MAXIMOS_DE_CRESCIMENTO)
    fator = configuracao.protecao_freio_atraso_fator_de_crescimento**passos
    atraso = configuracao.protecao_freio_atraso_inicial * fator
    return min(atraso, configuracao.protecao_freio_atraso_teto)


def exigir_freio_por_origem(superficie: str):
    """Fábrica de dependency do freio por origem (`RF-01-65`, `RN-01-27`).
    Cada rota que precisa do freio declara a superfície que a protege — ao
    contrário da cota, o freio não é transversal (design — Decisions).
    """
    if superficie not in _CONFIGURACAO_POR_SUPERFICIE:
        raise ValueError(f"Superfície de freio desconhecida: {superficie!r}")

    def dependencia(
        request: Request,
        configuracao: Annotated[Configuracao, Depends(obter_configuracao)],
    ) -> None:
        limite, duracao_da_janela = _CONFIGURACAO_POR_SUPERFICIE[superficie](configuracao)
        endereco = obter_endereco_de_rede(request)

        sal = obter_ou_criar(request, "protecao_sal_de_origem", SalRotativo)
        instante = agora()
        resumo_atual, resumo_anterior = sal.resumos(endereco, instante)

        janela = obter_ou_criar(request, "protecao_janela_do_freio", JanelaDeslizante)
        total = janela.registrar_e_contar(
            f"{superficie}:{resumo_atual}", instante, duracao_da_janela
        )
        if resumo_anterior is not None:
            total += janela.contar(f"{superficie}:{resumo_anterior}", instante, duracao_da_janela)

        if total <= limite:
            return

        atraso = _calcular_atraso(total - limite, configuracao)
        segundos = max(1, round(atraso.total_seconds()))
        raise FreioPorOrigemAcionado(
            mensagem=(
                "Muitas tentativas em pouco tempo. Tente novamente em "
                f"{_formatar_tempo_em_linguagem_simples(segundos)}."
            ),
            tempo_de_espera_em_segundos=segundos,
        )

    return dependencia
