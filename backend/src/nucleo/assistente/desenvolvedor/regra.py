import logging

from ...configuracao import Configuracao
from ...corpus_do_desenvolvedor.leitura import carregar_uma_vez, recortar
from ...erros import ErroDeValidacao, ServicoIndisponivel
from .porta import (
    MensagemDaConversa,
    PortaDoAssistenteDoDesenvolvedor,
    RespostaDoDesenvolvedor,
)

logger = logging.getLogger("nucleo.assistente")

# Quantos turnos da conversa acompanham a pergunta. Nada disso é guardado: a
# conversa vive no estado da página e some ao fechá-la (PRD-03 §8, design —
# decisão 5).
TETO_DO_HISTORICO = 6

_RECUSA_FIXA = (
    "Esse assunto não está na documentação, no README nem no contrato da API, e eu só "
    "respondo a partir deles. A documentação completa está publicada no site do projeto."
)

# Conjunto de reserva: resposta do modelo sem opções, e a recusa fora do
# corpus, saem com estas escolhas — nenhuma mensagem sai sem pergunta
# (`RF-03-69`, design — decisão 6).
OPCOES_FIXAS: tuple[str, ...] = (
    "Como a plataforma está montada",
    "Como a API se autentica por chave",
    "Como pedir a chave de aplicação",
)


class ConsultaAoAssistenteDoDesenvolvedorIndisponivel(ServicoIndisponivel):
    """Falha do assistente dita como o que é, nunca disfarçada de recusa do
    domínio (`RF-03-72`, documento 99 §6 invariante 25). A área segue de pé: a
    documentação, o repositório e o formulário não dependem dela."""

    codigo = "assistente_do_desenvolvedor_indisponivel"
    mensagem = (
        "O assistente não respondeu agora e voltará. A documentação, o repositório e o "
        "formulário de chave continuam disponíveis."
    )


def consultar_assistente_do_desenvolvedor(
    *,
    texto: str,
    historico: tuple[MensagemDaConversa, ...],
    porta: PortaDoAssistenteDoDesenvolvedor,
    configuracao: Configuracao,
) -> RespostaDoDesenvolvedor:
    """Recorta o corpus pela pergunta, consulta a porta e devolve a resposta
    com a pergunta de múltipla escolha. **Nada é gravado** — nem a pergunta,
    nem a resposta, nem a origem (PRD-03 §8, `RN-03-15`): esta função não
    recebe sessão de banco, e é assim que a regra fica impossível de violar."""
    if not texto.strip():
        raise ErroDeValidacao(mensagem="Envie a pergunta.", campo="texto")

    corpus = recortar(
        carregar_uma_vez(configuracao.corpus_do_desenvolvedor_caminho),
        pergunta=texto,
        teto=configuracao.corpus_do_desenvolvedor_teto,
    )

    resposta = porta.responder(texto=texto, corpus=corpus, historico=historico)
    if resposta is None:
        logger.warning("Consulta ao assistente do Desenvolvedor indisponível.")
        raise ConsultaAoAssistenteDoDesenvolvedorIndisponivel()

    if resposta.desfecho == "fora_do_corpus":
        return RespostaDoDesenvolvedor(
            desfecho="fora_do_corpus", resposta=_RECUSA_FIXA, opcoes=OPCOES_FIXAS
        )

    return RespostaDoDesenvolvedor(
        desfecho="respondida",
        resposta=resposta.resposta or "",
        opcoes=resposta.opcoes or OPCOES_FIXAS,
    )
