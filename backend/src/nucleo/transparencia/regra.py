import uuid
from collections.abc import Callable
from dataclasses import dataclass

from sqlalchemy import exists
from sqlalchemy.orm import Session

from ..assistente.modelo import ConsultaAoAssistente, TipoDeAssistente
from ..consentimentos.modelo import Consentimento
from ..equipes.modelo import IntegranteDaEquipe
from ..ocorrencias_de_conduta.modelo import OcorrenciaDeConduta
from ..personas.modelo import Credencial, Nick, Persona, TipoDeCredencial
from ..producoes.modelo import ProducaoDaMissao
from ..responsaveis.modelo import VinculoResponsavel


@dataclass(frozen=True)
class ItemDoCatalogo:
    dado: str
    finalidade: str
    prazo: str
    restrito_a_gestao: bool
    guardado: bool


def _existe(sessao: Session, *criterios) -> bool:
    return bool(sessao.query(exists().where(*criterios)).scalar())


def _guardado_template_biometrico(sessao: Session, guerreiro_id: uuid.UUID) -> bool:
    return _existe(
        sessao,
        Credencial.persona_id == guerreiro_id,
        Credencial.tipo == TipoDeCredencial.biometria,
        Credencial.ativa.is_(True),
    )


def _guardado_consulta_ao_assistente(
    tipo: TipoDeAssistente,
) -> Callable[[Session, uuid.UUID], bool]:
    def _verificar(sessao: Session, guerreiro_id: uuid.UUID) -> bool:
        direta = _existe(
            sessao,
            ConsultaAoAssistente.guerreiro_id == guerreiro_id,
            ConsultaAoAssistente.assistente == tipo,
        )
        if direta:
            return True
        return bool(
            sessao.query(ConsultaAoAssistente)
            .join(
                IntegranteDaEquipe, IntegranteDaEquipe.equipe_id == ConsultaAoAssistente.equipe_id
            )
            .filter(
                IntegranteDaEquipe.persona_id == guerreiro_id,
                ConsultaAoAssistente.assistente == tipo,
            )
            .first()
            is not None
        )

    return _verificar


# O catálogo é conteúdo declarado — as tabelas do PRD-01 §11 e do documento
# 03 §12.2 —, nunca inventário de linha da base: cada item responde se o
# núcleo guarda AQUELE dado daquele Guerreiro(a) hoje (`RF-13-29`, `RN-13-20`,
# design — decisão 4). `consulta ao assistente` e `transcrição de apoio
# escolar` entram restritas à gestão: o que a criança faz sozinha não é
# vigilância da família.
_CATALOGO: list[tuple[str, str, str, bool, Callable[[Session, uuid.UUID], bool]]] = [
    (
        "Nick",
        "Identificação pública do Guerreiro(a) na plataforma",
        "Enquanto durar o vínculo com o projeto",
        False,
        lambda sessao, guerreiro_id: _existe(sessao, Nick.persona_id == guerreiro_id),
    ),
    (
        "Nome e data de nascimento",
        "Identificação e conferência da faixa etária",
        "Enquanto durar o vínculo com o projeto",
        False,
        lambda sessao, guerreiro_id: _existe(
            sessao,
            Persona.id == guerreiro_id,
            (Persona.nome.is_not(None)) | (Persona.nascimento.is_not(None)),
        ),
    ),
    (
        "Template biométrico",
        "Presença e autenticação nas aplicações",
        (
            "Enquanto durar o vínculo com o projeto; 30 dias após o fim, ou 5 dias se você "
            "pedir a exclusão ou recusar a biometria"
        ),
        False,
        _guardado_template_biometrico,
    ),
    (
        "Vínculo com o(s) responsável(is) e grau de parentesco",
        "Provar quem responde pela criança",
        "Enquanto durar o vínculo com o projeto",
        False,
        lambda sessao, guerreiro_id: _existe(
            sessao,
            VinculoResponsavel.guerreiro_id == guerreiro_id,
            VinculoResponsavel.fim.is_(None),
        ),
    ),
    (
        "Consentimentos e autorizações versionados",
        "Prova do que foi autorizado, e quando",
        "Permanente",
        False,
        lambda sessao, guerreiro_id: _existe(sessao, Consentimento.guerreiro_id == guerreiro_id),
    ),
    (
        "Motivo da ocorrência de conduta",
        "Aplicar o Código de Conduta",
        "Até o fim do ciclo em que ocorreu; o lançamento de pontos permanece depois, sem o motivo",
        False,
        lambda sessao, guerreiro_id: _existe(
            sessao,
            OcorrenciaDeConduta.guerreiro_id == guerreiro_id,
            OcorrenciaDeConduta.motivo.is_not(None),
        ),
    ),
    (
        "Histórico de quem acessou os dados dele",
        "Rastreabilidade das ações sobre os dados dele",
        "Permanente",
        False,
        lambda sessao, guerreiro_id: True,
    ),
    (
        "Produção das missões (texto da transcrição)",
        "Avaliar o trabalho da missão e dar a devolutiva",
        "Permanente, junto da devolutiva; a foto e o áudio são descartados assim que lidos",
        False,
        lambda sessao, guerreiro_id: _existe(sessao, ProducaoDaMissao.autor_id == guerreiro_id),
    ),
    (
        "Consulta ao assistente de trilhas",
        "Apoio à jornada da missão, revisado pela gestão por amostragem",
        (
            "7 dias vinculada ao Guerreiro(a) quando respondida; até o fim do ciclo se "
            "recusada pelos filtros de segurança"
        ),
        True,
        _guardado_consulta_ao_assistente(TipoDeAssistente.trilhas),
    ),
    (
        "Transcrição de apoio escolar",
        "Apoio escolar individual, revisado pela gestão por amostragem",
        (
            "7 dias vinculada ao Guerreiro(a) quando respondida; até o fim do ciclo se "
            "recusada pelos filtros de segurança"
        ),
        True,
        _guardado_consulta_ao_assistente(TipoDeAssistente.apoio_escolar),
    ),
]


def consultar_catalogo_de_dados(
    sessao: Session, *, guerreiro_id: uuid.UUID
) -> list[ItemDoCatalogo]:
    """`RF-13-29`, `RN-13-20`: a lista declarada, cada linha com a marca do
    que está guardado hoje daquele Guerreiro(a) — nunca o conteúdo."""
    return [
        ItemDoCatalogo(
            dado=dado,
            finalidade=finalidade,
            prazo=prazo,
            restrito_a_gestao=restrito_a_gestao,
            guardado=verificar(sessao, guerreiro_id),
        )
        for dado, finalidade, prazo, restrito_a_gestao, verificar in _CATALOGO
    ]
