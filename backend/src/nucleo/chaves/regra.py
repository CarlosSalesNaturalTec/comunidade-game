import uuid
from datetime import timedelta

from sqlalchemy.orm import Session

from ..configuracao import Configuracao
from ..erros import (
    ErroDeValidacao,
    NaoEncontrado,
    PrazoDeApresentacaoVencido,
    SolicitacaoDeChaveNaoDisponivelParaEmissao,
    UrlJaApresentada,
)
from ..fila.modelo import SituacaoDaSolicitacao, SolicitacaoDeChave
from ..tempo import agora
from .modelo import ChaveDeAplicacao, NaturezaDaChave, SituacaoDaChave
from .segredo import calcular_resumo, gerar_segredo, montar_chave_completa

# A chave de terceiro nasce sempre neste ambiente, qualquer que seja o
# ambiente em que o Admin opera (`RN-01-51`).
AMBIENTE_DA_CHAVE_DE_TERCEIRO = "producao"

# Motivo gravado na revogação automática — sem autoria de pessoa, o que a
# distingue da revogação de Admin (`RF-01-52`, design — Decisions).
MOTIVO_DO_DECURSO = "Prazo de apresentação da URL vencido sem apresentação."


def aplicar_decurso_se_vencido(chave: ChaveDeAplicacao) -> bool:
    """Prazo vencido sem URL implica revogada (`RF-01-52`), num único ponto
    reaproveitado pela conferência da chave e pela leitura de gestão.
    Devolve se a transição aconteceu, para que o chamador saiba se precisa
    persistir."""
    venceu = (
        chave.natureza == NaturezaDaChave.de_terceiro
        and chave.situacao == SituacaoDaChave.vigente
        and chave.prazo_de_apresentacao is not None
        and chave.url_apresentada is None
        and agora() > chave.prazo_de_apresentacao
    )
    if not venceu:
        return False

    chave.situacao = SituacaoDaChave.revogada
    chave.motivo_da_revogacao = MOTIVO_DO_DECURSO
    chave.revogada_em = agora()
    return True


def emitir_chave_de_terceiro(
    sessao: Session,
    solicitacao: SolicitacaoDeChave,
    *,
    emitida_por: str,
    configuracao: Configuracao,
) -> tuple[ChaveDeAplicacao, str]:
    """`RF-01-50`: só sobre solicitação aprovada, e cada solicitação rende
    uma única chave (`RN-01-51`). Devolve o segredo em claro — a chave
    completa, pronta para o cabeçalho `X-Chave-Aplicacao` —, uma única vez
    (`RN-01-35`)."""
    if solicitacao.situacao != SituacaoDaSolicitacao.aceita or solicitacao.chave_id is not None:
        raise SolicitacaoDeChaveNaoDisponivelParaEmissao()

    chave = ChaveDeAplicacao(
        aplicacao=solicitacao.solicitante,
        ambiente=AMBIENTE_DA_CHAVE_DE_TERCEIRO,
        natureza=NaturezaDaChave.de_terceiro,
        resumo_do_segredo="",
        emitida_por=emitida_por,
        solicitacao_de_chave_id=solicitacao.id,
        prazo_de_apresentacao=agora() + timedelta(days=configuracao.prazo_de_apresentacao_dias),
    )
    sessao.add(chave)
    sessao.flush()

    segredo = gerar_segredo()
    chave.resumo_do_segredo = calcular_resumo(segredo)
    solicitacao.chave_id = chave.id
    sessao.flush()

    chave_completa = montar_chave_completa(AMBIENTE_DA_CHAVE_DE_TERCEIRO, str(chave.id), segredo)
    return chave, chave_completa


def apresentar_url(sessao: Session, id_da_chave: uuid.UUID, url: str) -> ChaveDeAplicacao:
    """`RF-01-51`: identifica a chave só pelo identificador, entregue na
    emissão e nunca devolvido por rota pública. Desconhecido ou de natureza
    do projeto recebem a mesma recusa, sem revelar existência (`RN-01-33`)."""
    chave = sessao.get(ChaveDeAplicacao, id_da_chave)
    if chave is None or chave.natureza != NaturezaDaChave.de_terceiro:
        raise NaoEncontrado()

    if aplicar_decurso_se_vencido(chave):
        sessao.flush()

    if chave.situacao != SituacaoDaChave.vigente:
        raise PrazoDeApresentacaoVencido()

    if chave.url_apresentada is not None:
        raise UrlJaApresentada()

    chave.url_apresentada = url
    sessao.flush()
    return chave


def revogar(
    sessao: Session, chave: ChaveDeAplicacao, *, motivo: str, revogada_por: str
) -> ChaveDeAplicacao:
    """`RF-01-53`: Admin revoga a qualquer tempo, com motivo e autoria. Não
    desfaz registro algum — a chave só lê (`RN-01-36`)."""
    if not motivo.strip():
        raise ErroDeValidacao(mensagem="O motivo da revogação é obrigatório.", campo="motivo")

    chave.situacao = SituacaoDaChave.revogada
    chave.motivo_da_revogacao = motivo
    chave.revogada_por = revogada_por
    chave.revogada_em = agora()
    sessao.flush()
    return chave
