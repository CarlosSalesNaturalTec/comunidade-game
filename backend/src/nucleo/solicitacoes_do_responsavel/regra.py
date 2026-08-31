import uuid

from sqlalchemy.orm import Session

from ..erros import ErroDeValidacao, SolicitacaoDoResponsavelDuplicada, SolicitacaoJaAvaliada
from ..fila.modelo import SituacaoDaSolicitacao
from ..fila.regra import PRAZO_DE_AVALIACAO
from ..personas.modelo import Persona
from ..responsaveis.regra import exigir_vinculo_do_responsavel
from ..tempo import agora
from .modelo import SolicitacaoDoResponsavel, TipoDeSolicitacaoDoResponsavel


def abrir_solicitacao(
    sessao: Session,
    *,
    responsavel: Persona,
    guerreiro_id: uuid.UUID,
    tipo: TipoDeSolicitacaoDoResponsavel,
    texto: str,
) -> SolicitacaoDoResponsavel:
    """`RF-13-22`, `RF-13-24`: guarda de vínculo do responsável com o
    Guerreiro(a) (403, `RN-13-13`) e guarda de duplicata em aberto — mesmo
    responsável, mesmo Guerreiro(a), mesmo tipo, sem desfecho (409,
    `RN-13-14`) —, sempre antes de gravar. A guarda não alcança a
    solicitação que o próprio núcleo abriu pela suspensão por divergência
    (`aberta_pela_suspensao`): ela é ato do sistema, e nunca impede que
    aquele mesmo responsável abra o próprio pedido (`RF-13-19`, design —
    decisão 4)."""
    exigir_vinculo_do_responsavel(
        sessao,
        papel=responsavel.papel,
        responsavel_id=responsavel.id,
        guerreiro_id=guerreiro_id,
    )

    duplicata = (
        sessao.query(SolicitacaoDoResponsavel)
        .filter_by(
            responsavel_id=responsavel.id,
            guerreiro_id=guerreiro_id,
            tipo=tipo,
            tratado_em=None,
            aberta_pela_suspensao=False,
        )
        .first()
    )
    if duplicata is not None:
        raise SolicitacaoDoResponsavelDuplicada()

    solicitacao = SolicitacaoDoResponsavel(
        responsavel_id=responsavel.id,
        guerreiro_id=guerreiro_id,
        tipo=tipo,
        texto=texto,
        situacao=SituacaoDaSolicitacao.recebida,
        prazo=agora() + PRAZO_DE_AVALIACAO,
    )
    sessao.add(solicitacao)
    sessao.flush()
    return solicitacao


_TEXTO_DA_SOLICITACAO_DE_DIVERGENCIA = (
    "A autorização única deste Guerreiro(a) ficou suspensa por divergência entre os "
    "responsáveis: um recusou depois de outro ter concedido. A gestão precisa tratar o caso "
    "com a família."
)


def abrir_solicitacao_da_divergencia(
    sessao: Session, *, guerreiro_id: uuid.UUID, responsavel_que_recusou: Persona
) -> SolicitacaoDoResponsavel | None:
    """`RF-13-19`: abre, em nome de quem recusou, quando a suspensão por
    divergência nasce — do tipo `esclarecimento`, com texto escrito pelo
    núcleo. Uma só enquanto estiver sem desfecho para aquele Guerreiro(a)
    (decisão do fundador, 2026-08-31, documento 09 §1): havendo uma em
    aberto, não abre outra e devolve `None` sem levantar erro — a recusa
    que a chama nunca é recusada por isso. Não reusa `abrir_solicitacao`:
    aquela guarda de vínculo e de duplicata é do pedido do próprio
    responsável (`RF-13-22`), e esta é ato do núcleo, por Guerreiro(a)."""
    ja_aberta = (
        sessao.query(SolicitacaoDoResponsavel)
        .filter_by(guerreiro_id=guerreiro_id, aberta_pela_suspensao=True, tratado_em=None)
        .first()
    )
    if ja_aberta is not None:
        return None

    solicitacao = SolicitacaoDoResponsavel(
        responsavel_id=responsavel_que_recusou.id,
        guerreiro_id=guerreiro_id,
        tipo=TipoDeSolicitacaoDoResponsavel.esclarecimento,
        texto=_TEXTO_DA_SOLICITACAO_DE_DIVERGENCIA,
        situacao=SituacaoDaSolicitacao.recebida,
        prazo=agora() + PRAZO_DE_AVALIACAO,
        aberta_pela_suspensao=True,
    )
    sessao.add(solicitacao)
    sessao.flush()
    return solicitacao


def listar_minhas_solicitacoes(
    sessao: Session, *, responsavel_id: uuid.UUID
) -> list[SolicitacaoDoResponsavel]:
    """`RF-13-25`, `RF-13-26`: só as próprias, da mais antiga para a mais
    recente — o mesmo recorte de leitura de `RN-13-13`."""
    return (
        sessao.query(SolicitacaoDoResponsavel)
        .filter_by(responsavel_id=responsavel_id)
        .order_by(SolicitacaoDoResponsavel.registrado_em)
        .all()
    )


def listar_fila_do_admin(sessao: Session) -> list[SolicitacaoDoResponsavel]:
    """`RF-02-23`: da mais antiga para a mais recente, como as demais
    naturezas da fila."""
    return (
        sessao.query(SolicitacaoDoResponsavel)
        .order_by(SolicitacaoDoResponsavel.registrado_em)
        .all()
    )


def registrar_tratamento(
    sessao: Session,
    solicitacao: SolicitacaoDoResponsavel,
    *,
    situacao: SituacaoDaSolicitacao,
    tratado_por: Persona,
    desfecho: str | None = None,
) -> SolicitacaoDoResponsavel:
    """`RF-02-24`: grava quem tratou e quando; recusa segundo desfecho sobre
    a mesma solicitação (`RN-13-14`). O desfecho é só o registro do
    tratamento — nenhum dado do Guerreiro(a) é apagado, despersonalizado ou
    alterado por este ato, mesmo no tipo exclusão: a execução do pedido é do
    PRD-13 (`RN-13-12`, `RN-13-22`)."""
    if situacao not in (SituacaoDaSolicitacao.aceita, SituacaoDaSolicitacao.recusada):
        raise ErroDeValidacao(mensagem="Desfecho precisa ser aceita ou recusada.", campo="situacao")
    if solicitacao.tratado_em is not None:
        raise SolicitacaoJaAvaliada()

    solicitacao.situacao = situacao
    solicitacao.desfecho = desfecho
    solicitacao.tratado_por_id = tratado_por.id
    solicitacao.tratado_em = agora()
    sessao.flush()
    return solicitacao


def esta_em_atraso(solicitacao: SolicitacaoDoResponsavel) -> bool:
    """`RN-13-14`: derivado de `prazo < agora` sem desfecho, nunca um
    estado gravado — o mesmo precedente de `fila.regra.esta_em_atraso`."""
    return solicitacao.tratado_em is None and solicitacao.prazo < agora()
