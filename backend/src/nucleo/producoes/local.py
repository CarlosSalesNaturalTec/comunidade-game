from .porta import LeituraDaProducao, PortaDaProducaoDaMissao

_DEVOLUTIVA_FIXA = (
    "Bom trabalho! Releia o que você produziu e pense: o que você acrescentaria se "
    "fosse explicar isso para um colega que não estava na aula?"
)


class ProducaoDaMissaoLocal(PortaDaProducaoDaMissao):
    """Adaptador padrão fora de produção (design — Migration Plan): devolve
    o eco do texto e uma devolutiva fixa, sem chamar rede nem exigir
    credencial — o mesmo precedente de `template_de_missao.local`."""

    def ler(
        self, *, forma: str, texto: str | None, arquivo: bytes | None, producao_esperada: str
    ) -> LeituraDaProducao | None:
        # Só a foto é mídia: a fala chega transcrita do aparelho e passa pelo
        # mesmo caminho do texto digitado (`RF-05-76`, design — decisão 3).
        if forma == "foto":
            transcricao = (
                f"Transcrição simulada da foto do manuscrito ({len(arquivo or b'')} bytes)."
            )
        else:
            transcricao = texto or ""
        return LeituraDaProducao(transcricao=transcricao, devolutiva=_DEVOLUTIVA_FIXA)
