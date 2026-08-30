from .porta import AtividadeSugerida, EstruturaSugerida, PortaDoTemplateDeMissao

# Palavra do tópico → Objetivo de Desenvolvimento Sustentável (1 a 18), a
# mesma faixa de `ods.modelo`. Cobertura deliberadamente pobre — este
# adaptador serve a esteira e o desenvolvimento, nunca a comunidade (design
# — Risks); a redação do modelo real é tarefa do adaptador de produção.
_PALAVRA_PARA_OBJETIVO_ODS: dict[str, int] = {
    "pobreza": 1,
    "fome": 2,
    "alimentação": 2,
    "saúde": 3,
    "educação": 4,
    "gênero": 5,
    "água": 6,
    "energia": 7,
    "trabalho": 8,
    "robô": 9,
    "robótica": 9,
    "tecnologia": 9,
    "programação": 9,
    "desigualdade": 10,
    "cidade": 11,
    "consumo": 12,
    "clima": 13,
    "oceano": 14,
    "floresta": 15,
    "paz": 16,
    "justiça": 16,
    "parceria": 17,
}


def _derivar_ods(topico: str) -> int | None:
    topico_normalizado = topico.strip().lower()
    for palavra, objetivo in _PALAVRA_PARA_OBJETIVO_ODS.items():
        if palavra in topico_normalizado:
            return objetivo
    return None


class TemplateDeMissaoLocal(PortaDoTemplateDeMissao):
    """Adaptador padrão fora de produção (design — Migration Plan): monta
    uma estrutura fixa a partir do tópico, sem chamar rede nem exigir
    credencial — o mesmo precedente de `armazenamento.disco`."""

    def sugerir_estrutura(
        self, *, topico: str, exigir_atividade_desplugada: bool
    ) -> EstruturaSugerida | None:
        atividades = []
        if exigir_atividade_desplugada:
            atividades.append(
                AtividadeSugerida(
                    titulo=f"Atividade desplugada sobre {topico}",
                    modalidade="individual",
                    formato="presencial",
                    natureza="desplugada",
                    producao_esperada="Registro em papel do que o Guerreiro(a) descobriu.",
                    desplugada=True,
                )
            )
        atividades.append(
            AtividadeSugerida(
                titulo=f"Atividade sobre {topico}",
                modalidade="individual",
                formato="presencial",
                natureza="construcao",
                producao_esperada=f"Uma produção própria sobre {topico}.",
                desplugada=False,
            )
        )
        return EstruturaSugerida(atividades=atividades, objetivo_ods=_derivar_ods(topico))
