import enum
import uuid
from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import and_, func, select
from sqlalchemy.orm import Session
from sqlalchemy.sql.elements import ColumnElement

from ..armazenamento.porta import PortaDeArmazenamento
from ..erros import (
    AutorizacaoSuspensaPorOutroResponsavel,
    DigitalizacaoDoTermoJaAnexada,
    ErroDeValidacao,
    PermissaoNegada,
    RevogacaoSemAutorizacaoVigente,
)
from ..personas.modelo import Papel, Persona
from ..responsaveis.modelo import VinculoResponsavel
from ..tempo import agora
from .modelo import (
    AnexoDoTermo,
    Consentimento,
    DecisaoDeConsentimento,
    OrigemDoConsentimento,
    TipoDeConsentimento,
)

_FORMATOS_DE_DIGITALIZACAO_ACEITOS = frozenset({"application/pdf", "image/jpeg", "image/png"})


def registrar_consentimento(
    sessao: Session,
    *,
    responsavel: Persona,
    guerreiro_id: uuid.UUID,
    tipo: TipoDeConsentimento | str,
    versao_do_termo: str,
    decisao: DecisaoDeConsentimento,
    origem: OrigemDoConsentimento,
    operado_por: Persona,
    testemunha_id: uuid.UUID | None = None,
    anexo: str | None = None,
) -> Consentimento:
    """Concentra as invariantes do consentimento — tipo do conjunto fechado,
    versão do termo obrigatória, vínculo vigente exigido e inserção sempre
    nova (`RF-01-19`, `RN-01-12`, design — decisões). Revogar é chamar de
    novo com a decisão contrária: o registro anterior nunca é tocado.
    """
    try:
        tipo_valido = TipoDeConsentimento(tipo)
    except ValueError as exc:
        raise ErroDeValidacao(
            mensagem="Tipo de consentimento fora do conjunto aceito.", campo="tipo"
        ) from exc

    if not versao_do_termo or not versao_do_termo.strip():
        raise ErroDeValidacao(
            mensagem="Consentimento exige a versão do termo.", campo="versao_do_termo"
        )

    vinculo_vigente = (
        sessao.query(VinculoResponsavel)
        .filter_by(responsavel_id=responsavel.id, guerreiro_id=guerreiro_id, fim=None)
        .first()
    )
    if vinculo_vigente is None:
        raise PermissaoNegada(
            mensagem="Responsável só consente sobre Guerreiro(a) vinculado a ele."
        )

    consentimento = Consentimento(
        responsavel_id=responsavel.id,
        guerreiro_id=guerreiro_id,
        tipo=tipo_valido,
        versao_do_termo=versao_do_termo,
        decisao=decisao,
        origem=origem,
        testemunha_id=testemunha_id,
        anexo=anexo,
        autor_id=operado_por.id,
        papel_do_autor=operado_por.papel.value,
    )
    sessao.add(consentimento)
    sessao.flush()
    return consentimento


def consultar_consentimento_vigente_em(
    sessao: Session, *, guerreiro_id: uuid.UUID, tipo: TipoDeConsentimento | str, em: datetime
) -> Consentimento | None:
    """Responde pelo registro vigente naquela data — o mais recente até
    `em`, nunca a decisão mais recente de todas (`RN-01-12`)."""
    return (
        sessao.query(Consentimento)
        .filter(
            Consentimento.guerreiro_id == guerreiro_id,
            Consentimento.tipo == tipo,
            Consentimento.registrado_em <= em,
        )
        .order_by(Consentimento.registrado_em.desc())
        .first()
    )


def _subquery_ultimas_decisoes_por_responsavel(
    sessao: Session, *, tipo: TipoDeConsentimento, em: datetime
):
    """A decisão mais recente de cada responsável, até `em` — um registro
    por (responsável, Guerreiro(a)), sem coluna de estado à parte (design —
    Decisions: a vigência é consulta derivada do histórico somente
    inserção)."""
    ultimo_momento = (
        sessao.query(
            Consentimento.responsavel_id,
            Consentimento.guerreiro_id,
            func.max(Consentimento.registrado_em).label("ultimo_momento"),
        )
        .filter(Consentimento.tipo == tipo, Consentimento.registrado_em <= em)
        .group_by(Consentimento.responsavel_id, Consentimento.guerreiro_id)
        .subquery()
    )
    return (
        sessao.query(ultimo_momento.c.guerreiro_id, Consentimento.decisao)
        .join(
            Consentimento,
            and_(
                Consentimento.responsavel_id == ultimo_momento.c.responsavel_id,
                Consentimento.guerreiro_id == ultimo_momento.c.guerreiro_id,
                Consentimento.registrado_em == ultimo_momento.c.ultimo_momento,
                Consentimento.tipo == tipo,
            ),
        )
        .subquery()
    )


def condicao_de_autorizacao_vigente(
    sessao: Session,
    coluna_guerreiro_id: ColumnElement[uuid.UUID] | uuid.UUID,
    *,
    tipo: TipoDeConsentimento = TipoDeConsentimento.autorizacao_de_divulgacao,
    em: datetime | None = None,
) -> ColumnElement[bool]:
    """Expressão SQL reutilizável de vigência (`RF-01-19`, `RN-01-12`,
    `RN-01-10`, `RN-13-07`, design — Decisions): vigente quando existe ao
    menos uma decisão e nenhuma delas — a mais recente de cada responsável —
    é recusa. Correlaciona com `coluna_guerreiro_id`, usável tanto no
    `WHERE` de uma listagem quanto na consulta pontual do perfil por nick.
    """
    ultimas = _subquery_ultimas_decisoes_por_responsavel(sessao, tipo=tipo, em=em or agora())
    tem_decisao = (
        select(ultimas.c.guerreiro_id).where(ultimas.c.guerreiro_id == coluna_guerreiro_id).exists()
    )
    tem_recusa = (
        select(ultimas.c.guerreiro_id)
        .where(
            ultimas.c.guerreiro_id == coluna_guerreiro_id,
            ultimas.c.decisao == DecisaoDeConsentimento.nega,
        )
        .exists()
    )
    return and_(tem_decisao, ~tem_recusa)


def autorizacao_de_divulgacao_vigente(
    sessao: Session, guerreiro_id: uuid.UUID, *, em: datetime | None = None
) -> bool:
    """Resposta booleana direta, para quem precisa da pergunta isolada em
    vez de compor a expressão numa consulta maior (`RN-01-10`)."""
    condicao = condicao_de_autorizacao_vigente(sessao, guerreiro_id, em=em)
    return bool(sessao.execute(select(condicao)).scalar())


class EstadoDaAutorizacao(enum.StrEnum):
    """Os três estados que o histórico deriva, sem coluna à parte
    (`RF-13-17`, design — decisão 1): `vigente` quando há concessão e
    nenhuma recusa; `suspensa` quando concessão e recusa convivem — a
    divergência; `nao_autorizada` quando não há decisão alguma, ou há só
    recusa. `condicao_de_autorizacao_vigente` continua a única fonte da
    vigência booleana que as superfícies públicas usam; este enum é
    equivalente a ela — `vigente` aqui é exatamente o `True` de lá — só
    que distinguindo os dois jeitos de não estar vigente."""

    vigente = "vigente"
    suspensa = "suspensa"
    nao_autorizada = "nao_autorizada"


def _ultimas_decisoes_dos_responsaveis(
    sessao: Session, *, guerreiro_id: uuid.UUID, tipo: TipoDeConsentimento, em: datetime
) -> list[Consentimento]:
    """A decisão mais recente de **cada** responsável vinculado sobre um
    Guerreiro(a), até `em` — a base de que o estado, os dois 409 e a
    idempotência derivam. Um só `Consentimento` por responsável."""
    ultimo_momento = (
        sessao.query(
            Consentimento.responsavel_id,
            func.max(Consentimento.registrado_em).label("ultimo_momento"),
        )
        .filter(
            Consentimento.guerreiro_id == guerreiro_id,
            Consentimento.tipo == tipo,
            Consentimento.registrado_em <= em,
        )
        .group_by(Consentimento.responsavel_id)
        .subquery()
    )
    return (
        sessao.query(Consentimento)
        .join(
            ultimo_momento,
            and_(
                Consentimento.responsavel_id == ultimo_momento.c.responsavel_id,
                Consentimento.registrado_em == ultimo_momento.c.ultimo_momento,
            ),
        )
        .filter(Consentimento.guerreiro_id == guerreiro_id, Consentimento.tipo == tipo)
        .all()
    )


def _estado_a_partir_das_decisoes(decisoes: list[Consentimento]) -> EstadoDaAutorizacao:
    tem_concessao = any(d.decisao == DecisaoDeConsentimento.concede for d in decisoes)
    tem_recusa = any(d.decisao == DecisaoDeConsentimento.nega for d in decisoes)
    if tem_concessao and tem_recusa:
        return EstadoDaAutorizacao.suspensa
    if tem_concessao:
        return EstadoDaAutorizacao.vigente
    return EstadoDaAutorizacao.nao_autorizada


@dataclass(frozen=True)
class QuemMotivouASuspensao:
    responsavel_id: uuid.UUID
    decidido_em: datetime


@dataclass(frozen=True)
class ItemDoHistoricoDaAutorizacao:
    id: uuid.UUID
    responsavel_id: uuid.UUID
    decisao: DecisaoDeConsentimento
    versao_do_termo: str
    origem: OrigemDoConsentimento
    registrado_em: datetime


@dataclass(frozen=True)
class LeituraDaAutorizacao:
    estado: EstadoDaAutorizacao
    suspensa_por: QuemMotivouASuspensao | None
    historico: list[ItemDoHistoricoDaAutorizacao]


def ler_autorizacao(sessao: Session, *, guerreiro_id: uuid.UUID) -> LeituraDaAutorizacao:
    """`RF-13-18`, `RF-13-21`: o estado derivado, quem motivou a suspensão
    — a recusa mais recente entre as que a compõem — com data e hora, e o
    histórico completo daquele Guerreiro(a), do mais recente ao mais
    antigo. Não alcança `biometria` (`RN-13-06`)."""
    momento = agora()
    decisoes = _ultimas_decisoes_dos_responsaveis(
        sessao,
        guerreiro_id=guerreiro_id,
        tipo=TipoDeConsentimento.autorizacao_de_divulgacao,
        em=momento,
    )
    estado = _estado_a_partir_das_decisoes(decisoes)

    suspensa_por = None
    if estado == EstadoDaAutorizacao.suspensa:
        recusa_mais_recente = max(
            (d for d in decisoes if d.decisao == DecisaoDeConsentimento.nega),
            key=lambda d: d.registrado_em,
        )
        suspensa_por = QuemMotivouASuspensao(
            responsavel_id=recusa_mais_recente.responsavel_id,
            decidido_em=recusa_mais_recente.registrado_em,
        )

    historico = (
        sessao.query(Consentimento)
        .filter_by(guerreiro_id=guerreiro_id, tipo=TipoDeConsentimento.autorizacao_de_divulgacao)
        .order_by(Consentimento.registrado_em.desc())
        .all()
    )
    return LeituraDaAutorizacao(
        estado=estado,
        suspensa_por=suspensa_por,
        historico=[
            ItemDoHistoricoDaAutorizacao(
                id=item.id,
                responsavel_id=item.responsavel_id,
                decisao=item.decisao,
                versao_do_termo=item.versao_do_termo,
                origem=item.origem,
                registrado_em=item.registrado_em,
            )
            for item in historico
        ],
    )


def decidir_autorizacao(
    sessao: Session,
    *,
    responsavel: Persona,
    guerreiro_id: uuid.UUID,
    decisao: DecisaoDeConsentimento,
    versao_do_termo: str,
) -> tuple[Consentimento, EstadoDaAutorizacao]:
    """`RF-13-14`, `RF-13-15`: o responsável concede ou revoga em nome
    próprio, com origem `propria`. Guarda de vínculo (403, `RN-13-04`),
    idempotência do reenvio da mesma decisão (PRD-13 §10), e os dois 409
    da PRD-13 §9 — concessão sobre recusa vigente de **outro** responsável,
    revogação sem nenhuma concessão vigente de ninguém. O responsável que
    nunca decidiu revoga do mesmo jeito que quem já concedeu: é assim que
    a divergência nasce (`RF-13-17`, `RN-13-07`) — a guarda é sobre o
    estado geral, não sobre a história pessoal de quem decide. Quando a
    decisão faz o estado passar a `suspensa`, abre a solicitação da
    divergência no mesmo commit (`RF-13-19`, design — decisão 4)."""
    vinculo_vigente = (
        sessao.query(VinculoResponsavel)
        .filter_by(responsavel_id=responsavel.id, guerreiro_id=guerreiro_id, fim=None)
        .first()
    )
    if vinculo_vigente is None:
        raise PermissaoNegada(mensagem="Responsável só decide sobre Guerreiro(a) vinculado a ele.")

    momento = agora()
    decisoes_atuais = _ultimas_decisoes_dos_responsaveis(
        sessao,
        guerreiro_id=guerreiro_id,
        tipo=TipoDeConsentimento.autorizacao_de_divulgacao,
        em=momento,
    )
    minha_decisao_atual = next(
        (d for d in decisoes_atuais if d.responsavel_id == responsavel.id), None
    )

    if minha_decisao_atual is not None and minha_decisao_atual.decisao == decisao:
        return minha_decisao_atual, _estado_a_partir_das_decisoes(decisoes_atuais)

    if decisao == DecisaoDeConsentimento.concede:
        recusa_de_outro = next(
            (
                d
                for d in decisoes_atuais
                if d.responsavel_id != responsavel.id and d.decisao == DecisaoDeConsentimento.nega
            ),
            None,
        )
        if recusa_de_outro is not None:
            raise AutorizacaoSuspensaPorOutroResponsavel()
    else:
        estado_atual = _estado_a_partir_das_decisoes(decisoes_atuais)
        if estado_atual == EstadoDaAutorizacao.nao_autorizada:
            raise RevogacaoSemAutorizacaoVigente()

    novo_registro = registrar_consentimento(
        sessao,
        responsavel=responsavel,
        guerreiro_id=guerreiro_id,
        tipo=TipoDeConsentimento.autorizacao_de_divulgacao,
        versao_do_termo=versao_do_termo,
        decisao=decisao,
        origem=OrigemDoConsentimento.propria,
        operado_por=responsavel,
    )

    decisoes_apos = [d for d in decisoes_atuais if d.responsavel_id != responsavel.id] + [
        novo_registro
    ]
    estado_apos = _estado_a_partir_das_decisoes(decisoes_apos)
    if estado_apos == EstadoDaAutorizacao.suspensa:
        # Import adiado: `solicitacoes_do_responsavel.regra` alcança
        # `pontuacao.regra`, que importa este módulo — o ciclo só existe no
        # topo do arquivo, nunca em tempo de chamada (`RF-13-19`).
        from ..solicitacoes_do_responsavel.regra import abrir_solicitacao_da_divergencia

        abrir_solicitacao_da_divergencia(
            sessao, guerreiro_id=guerreiro_id, responsavel_que_recusou=responsavel
        )

    return novo_registro, estado_apos


def anexar_digitalizacao_do_termo(
    sessao: Session,
    *,
    operador: Persona,
    consentimento: Consentimento | None,
    conteudo: bytes | None,
    nome_original: str | None,
    tipo_mime: str | None,
    armazenamento: PortaDeArmazenamento | None,
) -> AnexoDoTermo:
    """Anexa a digitalização do termo impresso de biometria assinado no
    encontro, como registro próprio que aponta para o consentimento — este
    permanece de somente inserção (`RF-02-68`, `RN-01-12`, design —
    Decisions). Só o Admin anexa; só o consentimento de tipo `biometria`
    recebe anexo, e só um por consentimento.
    """
    if operador.papel != Papel.admin:
        raise PermissaoNegada(mensagem="Só o Admin anexa a digitalização do termo.")
    if consentimento is None:
        raise ErroDeValidacao(mensagem="Consentimento não encontrado.", campo="consentimento_id")
    if consentimento.tipo != TipoDeConsentimento.biometria:
        raise ErroDeValidacao(
            mensagem="Só o consentimento de biometria recebe a digitalização do termo.",
            campo="consentimento_id",
        )

    ja_anexado = sessao.query(AnexoDoTermo).filter_by(consentimento_id=consentimento.id).first()
    if ja_anexado is not None:
        raise DigitalizacaoDoTermoJaAnexada()

    if conteudo is None or tipo_mime not in _FORMATOS_DE_DIGITALIZACAO_ACEITOS:
        raise ErroDeValidacao(
            mensagem="Digitalização aceita apenas em PDF, JPG ou PNG.",
            campo="digitalizacao",
        )
    if armazenamento is None:
        raise ErroDeValidacao(mensagem="Porta de armazenamento não disponível.")

    referencia = f"anexos-do-termo/{uuid.uuid4()}"
    armazenamento.gravar(referencia=referencia, conteudo=conteudo)

    anexo = AnexoDoTermo(
        consentimento_id=consentimento.id,
        digitalizacao_referencia=referencia,
        digitalizacao_nome_original=nome_original,
        digitalizacao_tipo=tipo_mime,
        digitalizacao_tamanho=len(conteudo),
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(anexo)
    sessao.flush()
    return anexo
