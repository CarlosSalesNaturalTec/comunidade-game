from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass(frozen=True)
class AtividadeSugerida:
    titulo: str
    modalidade: str
    formato: str
    natureza: str
    producao_esperada: str
    desplugada: bool = False
    descricao: str | None = None


@dataclass(frozen=True)
class EstruturaSugerida:
    """O que o modelo propõe — nunca as lacunas nem a cadência de retomada,
    que o núcleo calcula sozinho (design — decisão 1). `objetivo_ods` vem
    `None` quando o tópico não permite derivar objetivo algum, e a sugestão
    segue sem etiqueta em vez de trazer um objetivo arbitrado (`RN-09-35`).
    """

    atividades: list[AtividadeSugerida] = field(default_factory=list)
    objetivo_ods: int | None = None
    meta_ods: str | None = None


class PortaDoTemplateDeMissao(ABC):
    """Interface do pedido de estrutura ao modelo — local, sem rede, fora de
    produção; Gemini em produção (design — decisão 2). `None` é a
    indisponibilidade: erro, demora ou resposta fora do formato esperado, e
    quem chama a trata como "a sugestão não veio", nunca como falha da
    operação (`RF-09-91`, design — decisão 3)."""

    @abstractmethod
    def sugerir_estrutura(
        self, *, topico: str, exigir_atividade_desplugada: bool
    ) -> EstruturaSugerida | None: ...
