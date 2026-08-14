import uuid
from datetime import datetime

from sqlalchemy import and_, func, select
from sqlalchemy.orm import Session
from sqlalchemy.sql.elements import ColumnElement

from ..erros import ErroDeValidacao, PermissaoNegada
from ..personas.modelo import Persona
from ..responsaveis.modelo import VinculoResponsavel
from ..tempo import agora
from .modelo import (
    Consentimento,
    DecisaoDeConsentimento,
    OrigemDoConsentimento,
    TipoDeConsentimento,
)


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
