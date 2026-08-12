import uuid
from datetime import datetime

from sqlalchemy.orm import Session

from ..erros import ErroDeValidacao, PermissaoNegada
from ..personas.modelo import Persona
from ..responsaveis.modelo import VinculoResponsavel
from .modelo import Consentimento, DecisaoDeConsentimento, OrigemDoConsentimento


def registrar_consentimento(
    sessao: Session,
    *,
    responsavel: Persona,
    guerreiro_id: uuid.UUID,
    tipo: str,
    versao_do_termo: str,
    decisao: DecisaoDeConsentimento,
    origem: OrigemDoConsentimento,
    operado_por: Persona,
    testemunha_id: uuid.UUID | None = None,
    anexo: str | None = None,
) -> Consentimento:
    """Concentra as invariantes do consentimento — versão do termo
    obrigatória, vínculo vigente exigido e inserção sempre nova (`RF-01-19`,
    `RN-01-12`, design — decisões). Revogar é chamar de novo com a decisão
    contrária: o registro anterior nunca é tocado.
    """
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
        tipo=tipo,
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
    sessao: Session, *, guerreiro_id: uuid.UUID, tipo: str, em: datetime
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
