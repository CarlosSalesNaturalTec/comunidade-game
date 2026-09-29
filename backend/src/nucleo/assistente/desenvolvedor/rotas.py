from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field

from ...configuracao import Configuracao, obter_configuracao
from ...protecao.freio import exigir_freio_por_origem
from .fabrica import dependencia_do_assistente_do_desenvolvedor
from .porta import MensagemDaConversa, PortaDoAssistenteDoDesenvolvedor
from .regra import TETO_DO_HISTORICO, consultar_assistente_do_desenvolvedor

roteador = APIRouter()


class MensagemDaConversaEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    de: str = Field(pattern="^(visitante|assistente)$")
    texto: str = Field(min_length=1)


class ConsultaDoDesenvolvedorEntrada(BaseModel):
    """`extra="forbid"` é o que cumpre o `RF-03-71`: campo de nome, contato ou
    identificador do visitante não passa — a recusa é 422, e nada é
    respondido. O corpo tem só a pergunta e os últimos turnos da conversa."""

    model_config = ConfigDict(extra="forbid")

    texto: str = Field(min_length=1)
    historico: list[MensagemDaConversaEntrada] = Field(
        default_factory=list, max_length=TETO_DO_HISTORICO
    )


class ConsultaDoDesenvolvedorSaida(BaseModel):
    """Sem identificador e sem momento: não há linha nenhuma para apontar. A
    conversa vive no aparelho do visitante enquanto a página está aberta
    (PRD-03 §8)."""

    desfecho: str
    resposta: str
    opcoes: list[str]


@roteador.post("/assistente-do-desenvolvedor")
def consultar_assistente_do_desenvolvedor_rota(
    entrada: ConsultaDoDesenvolvedorEntrada,
    configuracao: Annotated[Configuracao, Depends(obter_configuracao)],
    porta: Annotated[
        PortaDoAssistenteDoDesenvolvedor,
        Depends(dependencia_do_assistente_do_desenvolvedor),
    ],
    _freio: Annotated[None, Depends(exigir_freio_por_origem("assistente_do_desenvolvedor"))],
) -> ConsultaDoDesenvolvedorSaida:
    """`RF-03-67` a `RF-03-72`, PRD-03 §9. Pública, sem credencial de persona
    (`RN-03-29`, `RN-03-33`), e **sem sessão de banco**: nada desta rota é
    gravado. Superfície própria do freio por origem, porque cada pergunta
    consome modelo pago numa rota aberta a qualquer visitante (`RN-03-08`,
    decisão do fundador de 2026-09-29)."""
    resposta = consultar_assistente_do_desenvolvedor(
        texto=entrada.texto,
        historico=tuple(
            MensagemDaConversa(de=mensagem.de, texto=mensagem.texto)
            for mensagem in entrada.historico
        ),
        porta=porta,
        configuracao=configuracao,
    )
    return ConsultaDoDesenvolvedorSaida(
        desfecho=resposta.desfecho,
        resposta=resposta.resposta or "",
        opcoes=list(resposta.opcoes),
    )
