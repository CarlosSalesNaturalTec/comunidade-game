import logging

from sqlalchemy.orm import Session

from ..aulas.modelo import Aula
from ..equipes.modelo import Equipe, IntegranteDaEquipe
from ..erros import ErroDeAplicacao, ErroDeValidacao, PermissaoNegada
from ..personas.modelo import Papel, Persona
from ..tempo import agora
from ..trilhas.modelo import Atividade, Missao
from .modelo import FormaDeEntregaDaProducao, ProducaoDaMissao
from .porta import PortaDaProducaoDaMissao

logger = logging.getLogger("nucleo.producoes")


class LeituraDaProducaoIndisponivel(ErroDeAplicacao):
    """`RF-04-46`: sem leitura não há transcrição do áudio ou da foto, e
    gravar o registro vazio guardaria uma entrega que não diz nada (design
    — decisão 5)."""

    status_code = 503
    codigo = "leitura_da_producao_indisponivel"
    mensagem = "A leitura da produção não veio agora. Tente enviar de novo."


def registrar_producao(
    sessao: Session,
    *,
    operador: Persona,
    equipe: Equipe,
    forma: FormaDeEntregaDaProducao,
    texto: str | None,
    arquivo: bytes | None,
    porta: PortaDaProducaoDaMissao,
) -> ProducaoDaMissao:
    """Restrita ao Guerreiro(a) integrante da equipe (`RF-04-45`, design —
    decisão 6): a operação da matriz já recusa quem não é Guerreiro(a), mas
    o Admin, que tem `Operacao.tudo`, só é barrado aqui — o mesmo precedente
    de `equipes.regra.criar_equipe`."""
    if operador.papel != Papel.guerreiro:
        raise PermissaoNegada(mensagem="Só o Guerreiro(a) entrega a produção da missão.")

    integrante = (
        sessao.query(IntegranteDaEquipe)
        .filter_by(equipe_id=equipe.id, persona_id=operador.id)
        .first()
    )
    if integrante is None:
        raise PermissaoNegada(mensagem="Só integrante da equipe entrega a produção pela equipe.")

    if equipe.atividade_corrente_id is None:
        raise ErroDeValidacao(
            mensagem="A equipe ainda não declarou a atividade que está trabalhando.",
            campo="equipe_id",
        )

    if equipe.aula_id is not None:
        aula = sessao.get(Aula, equipe.aula_id)
        if aula.fim_em <= agora():
            raise ErroDeValidacao(mensagem="Esta aula já encerrou.", campo="equipe_id")

    if forma == FormaDeEntregaDaProducao.texto:
        if not texto or arquivo is not None:
            raise ErroDeValidacao(
                mensagem="Envie a produção em uma única forma: texto, áudio ou foto.",
                campo="forma",
            )
    else:
        if arquivo is None or texto is not None:
            raise ErroDeValidacao(
                mensagem="Envie a produção em uma única forma: texto, áudio ou foto.",
                campo="forma",
            )

    atividade = sessao.get(Atividade, equipe.atividade_corrente_id)
    missao = sessao.get(Missao, atividade.missao_id)

    leitura = porta.ler(
        forma=forma.value,
        texto=texto,
        arquivo=arquivo,
        producao_esperada=atividade.producao_esperada,
    )

    if leitura is not None:
        transcricao = leitura.transcricao
        devolutiva = leitura.devolutiva
    elif forma == FormaDeEntregaDaProducao.texto:
        transcricao = texto
        devolutiva = None
    else:
        logger.warning(
            "Leitura da produção indisponível (forma=%s, tamanho=%d bytes).",
            forma.value,
            len(arquivo or b""),
        )
        raise LeituraDaProducaoIndisponivel()

    producao = ProducaoDaMissao(
        equipe_id=equipe.id,
        guerreiro_id=None,
        missao_id=missao.id,
        atividade_id=atividade.id,
        forma=forma,
        transcricao=transcricao,
        devolutiva=devolutiva,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(producao)
    sessao.flush()
    return producao
