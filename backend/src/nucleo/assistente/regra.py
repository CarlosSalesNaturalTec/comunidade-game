import logging

from sqlalchemy.orm import Session

from ..conteudos.modelo import ConteudoDaMissao, TipoDeConteudo
from ..equipes.modelo import Equipe, IntegranteDaEquipe
from ..erros import ErroDeAplicacao, ErroDeValidacao, PermissaoNegada
from ..personas.modelo import Papel, Persona
from ..trilhas.modelo import Atividade, Missao
from .modelo import ConsultaAoAssistente, DesfechoDaConsulta, TipoDeAssistente
from .porta import PortaDoAssistente

logger = logging.getLogger("nucleo.assistente")

# Teto do corpus no prompt (design — Risks): a montagem trunca pela posição
# mais recente para trás, mantendo sempre a missão corrente inteira.
_TETO_DO_CORPUS_EM_CARACTERES = 20_000

_RECUSA_FIXA = (
    "Esse assunto ainda não está no material desta trilha. Procure um Mestre no encontro "
    "para aprender mais sobre isso."
)
_ENCAMINHAMENTO_FIXO = (
    "Essa pergunta é de tarefa escolar — esse apoio é da App 05, não deste assistente."
)


class ConsultaAoAssistenteIndisponivel(ErroDeAplicacao):
    """Sem resposta não há consulta: gravar a pergunta sozinha guardaria
    uma conversa que não aconteceu (design — decisão 5)."""

    status_code = 503
    codigo = "consulta_ao_assistente_indisponivel"
    mensagem = "O assistente não respondeu agora. Tente perguntar de novo."


def _bloco_da_missao(missao: Missao, conteudos: list[ConteudoDaMissao]) -> str:
    """Texto entra pelo corpo; link, imagem, vídeo e arquivo entram só pelo
    título da missão a que pertencem (design — decisão 2)."""
    linhas = [f"Missão: {missao.titulo}"]
    for conteudo in conteudos:
        if conteudo.tipo == TipoDeConteudo.texto and conteudo.corpo:
            linhas.append(conteudo.corpo)
    return "\n".join(linhas)


def _montar_corpus(sessao: Session, equipe: Equipe) -> str:
    """Equipe → atividade corrente → missão → trilha, com os conteúdos das
    missões de posição ≤ à da corrente, na ordem da posição e da `ordem`,
    truncando pela mais recente para trás e mantendo a missão corrente
    inteira (design — decisão 2, `RN-04-19`)."""
    atividade = sessao.get(Atividade, equipe.atividade_corrente_id)
    missao_corrente = sessao.get(Missao, atividade.missao_id)

    missoes = (
        sessao.query(Missao)
        .filter(
            Missao.trilha_id == missao_corrente.trilha_id,
            Missao.posicao <= missao_corrente.posicao,
        )
        .order_by(Missao.posicao.desc())
        .all()
    )

    blocos_em_ordem_reversa: list[str] = []
    caracteres = 0
    for missao in missoes:
        conteudos = (
            sessao.query(ConteudoDaMissao)
            .filter_by(missao_id=missao.id)
            .order_by(ConteudoDaMissao.ordem)
            .all()
        )
        bloco = _bloco_da_missao(missao, conteudos)
        if missao.id != missao_corrente.id and caracteres + len(bloco) > _TETO_DO_CORPUS_EM_CARACTERES:
            break
        blocos_em_ordem_reversa.append(bloco)
        caracteres += len(bloco)

    return "\n\n".join(reversed(blocos_em_ordem_reversa))


def consultar_assistente_de_trilhas(
    sessao: Session,
    *,
    operador: Persona,
    equipe: Equipe,
    texto: str | None,
    arquivo: bytes | None,
    porta: PortaDoAssistente,
) -> ConsultaAoAssistente:
    """Restrita ao Guerreiro(a) integrante da equipe (`RF-04-36`, design —
    decisão 6): a operação da matriz já recusa quem não é Guerreiro(a), mas
    o Admin, que tem `Operacao.tudo`, só é barrado aqui — o mesmo
    precedente de `producoes.regra.registrar_producao`."""
    if operador.papel != Papel.guerreiro:
        raise PermissaoNegada(mensagem="Só o Guerreiro(a) consulta o assistente pela equipe.")

    integrante = (
        sessao.query(IntegranteDaEquipe)
        .filter_by(equipe_id=equipe.id, persona_id=operador.id)
        .first()
    )
    if integrante is None:
        raise PermissaoNegada(
            mensagem="Só integrante da equipe consulta o assistente pela equipe."
        )

    if equipe.atividade_corrente_id is None:
        raise ErroDeValidacao(
            mensagem="A equipe ainda não declarou a atividade que está trabalhando.",
            campo="equipe_id",
        )

    if (texto is None) == (arquivo is None):
        raise ErroDeValidacao(
            mensagem="Envie a pergunta em uma única forma: texto ou áudio.", campo="texto"
        )

    corpus = _montar_corpus(sessao, equipe)

    resposta = porta.responder(texto=texto, arquivo=arquivo, corpus=corpus)
    if resposta is None:
        logger.warning("Consulta ao assistente de trilhas indisponível.")
        raise ConsultaAoAssistenteIndisponivel()

    if resposta.desfecho == DesfechoDaConsulta.fora_do_corpus.value:
        texto_da_resposta = _RECUSA_FIXA
    elif resposta.desfecho == DesfechoDaConsulta.tarefa_escolar.value:
        texto_da_resposta = _ENCAMINHAMENTO_FIXO
    else:
        texto_da_resposta = resposta.resposta or ""

    consulta = ConsultaAoAssistente(
        equipe_id=equipe.id,
        guerreiro_id=None,
        assistente=TipoDeAssistente.trilhas,
        desfecho=DesfechoDaConsulta(resposta.desfecho),
        pergunta=resposta.transcricao_da_pergunta,
        resposta=texto_da_resposta,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(consulta)
    sessao.flush()
    return consulta
