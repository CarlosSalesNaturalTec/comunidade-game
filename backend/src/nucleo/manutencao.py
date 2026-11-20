from . import modelos as _modelos  # noqa: F401 — popula Base.metadata com todas as tabelas
from .banco import obter_fabrica_de_sessao
from .biometria.regra import apagar_templates_vencidos
from .reservas.regra import encerrar_aulas_vencidas
from .vinculo_do_guerreiro.regra import varrer_vinculos_vencidos


def executar_manutencao() -> None:
    """Comando periódico: `python -m nucleo.manutencao`. Primeiro encerra as
    aulas cujo horário terminou — a aula não tem fechamento, e a baixa da
    reserva é do sistema (`RF-01-91`, `RN-07-43`). Depois cumpre os prazos de
    guarda em duas etapas, nessa ordem — encerra os vínculos vencidos pelos
    12 meses e só então apaga os _templates_ vencidos —, para que um vínculo
    encerrado nesta mesma execução já nasça com a marca de 30 dias. Repetível
    sem efeito duplicado; a implantação agenda a execução periódica
    (decisão do fundador, 2026-09-01, documento 03 §12.2).
    """
    fabrica = obter_fabrica_de_sessao()

    with fabrica() as sessao:
        aulas_encerradas = encerrar_aulas_vencidas(sessao)
        sessao.commit()

        vinculos_encerrados = varrer_vinculos_vencidos(sessao)
        sessao.commit()

        templates_apagados = apagar_templates_vencidos(sessao)
        sessao.commit()

    print(
        f"Manutenção concluída: {aulas_encerradas} aula(s) encerrada(s) pelo horário, "
        f"{vinculos_encerrados} vínculo(s) encerrado(s) pela "
        f"varredura, {templates_apagados} template(s) biométrico(s) apagado(s)."
    )


if __name__ == "__main__":
    executar_manutencao()
