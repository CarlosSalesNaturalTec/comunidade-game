import uuid
from decimal import Decimal

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from ..aulas.modelo import Aula, Presenca, SituacaoDaAula
from ..aulas.regra import aulas_vigentes
from ..comunidades.modelo import VinculoJogador
from ..consentimentos.modelo import (
    AnexoDoTermo,
    DecisaoDeConsentimento,
    OrigemDoConsentimento,
    TipoDeConsentimento,
)
from ..consentimentos.regra import consultar_consentimento_vigente_em
from ..equipes.modelo import Equipe, IntegranteDaEquipe
from ..equipes.regra import equipes_da_aula
from ..erros import PermissaoNegada
from ..livro_razao.regra import saldos_por_ponto_de_apoio
from ..personas.modelo import Papel, Persona
from ..reservas.modelo import Reserva
from ..tempo import agora
from ..trilhas.modelo import Atividade, Missao, SituacaoDaTrilha, Trilha
from ..vitrine.publico import AvatarENickSaida, buscar_avatares_e_nicks

_SITUACOES_COM_DESFECHO = (SituacaoDaAula.realizada, SituacaoDaAula.cancelada)


class PresencaDoPainelSaida(BaseModel):
    guerreiro_id: uuid.UUID
    avatar: str | None
    nick: str
    modo: str
    confirmador_id: uuid.UUID | None


class GuerreiroDoPainelSaida(BaseModel):
    guerreiro_id: uuid.UUID
    avatar: str | None
    nick: str


class EquipeDoPainelSaida(BaseModel):
    id: uuid.UUID
    integrantes: list[AvatarENickSaida]
    missao_id: uuid.UUID | None
    missao_titulo: str | None


class AtividadePrevistaSaida(BaseModel):
    id: uuid.UUID
    titulo: str
    missao_id: uuid.UUID
    missao_titulo: str


class RecursoProvidoSaida(BaseModel):
    tipo_de_recurso_id: uuid.UUID
    quantidade: Decimal


class SaldoDoTipoSaida(BaseModel):
    tipo_de_recurso_id: uuid.UUID
    saldo: Decimal


class PendenciaDoPainelSaida(BaseModel):
    tipo: str
    guerreiro_id: uuid.UUID | None = None
    nick: str | None = None
    consentimento_id: uuid.UUID | None = None


class PainelDoDiaSaida(BaseModel):
    aula_id: uuid.UUID | None
    comunidade_virtual_id: uuid.UUID | None
    ponto_de_apoio_id: uuid.UUID | None
    presencas: list[PresencaDoPainelSaida] = Field(default_factory=list)
    aguardando_aparelho: list[GuerreiroDoPainelSaida] = Field(default_factory=list)
    equipes: list[EquipeDoPainelSaida] = Field(default_factory=list)
    atividades_previstas: list[AtividadePrevistaSaida] = Field(default_factory=list)
    recursos_providos: list[RecursoProvidoSaida] = Field(default_factory=list)
    saldo_do_ponto_de_apoio: list[SaldoDoTipoSaida] = Field(default_factory=list)
    pendencias: list[PendenciaDoPainelSaida] = Field(default_factory=list)


def _resolver_aula(sessao: Session, *, operador: Persona) -> Aula | None:
    """A aula em andamento pela janela de data e horários — para o Mestre,
    restrita à comunidade a que está vinculado; sem vínculo, nada a
    mostrar. Havendo mais de uma aula vigente para o Admin, a escolha
    segue o mesmo precedente de `aulas_vigentes` (`RF-01-32`, `RF-01-18`):
    não é do núcleo escolher entre comunidades, mas o painel serve uma
    aula por vez (design — Goals), então a primeira responde.
    """
    candidatas = aulas_vigentes(sessao)
    if operador.papel == Papel.mestre:
        vinculo: VinculoJogador | None = operador.vinculo_vigente
        if vinculo is None:
            return None
        candidatas = [
            aula
            for aula in candidatas
            if aula.comunidade_virtual_id == vinculo.comunidade_virtual_id
        ]
    if not candidatas:
        return None
    return sorted(candidatas, key=lambda aula: aula.inicio_em)[0]


def _presencas(sessao: Session, aula_id: uuid.UUID) -> list[PresencaDoPainelSaida]:
    presencas = sessao.query(Presenca).filter_by(aula_id=aula_id).all()
    avatares_e_nicks = buscar_avatares_e_nicks(sessao, [p.guerreiro_id for p in presencas])
    return [
        PresencaDoPainelSaida(
            guerreiro_id=presenca.guerreiro_id,
            avatar=avatares_e_nicks[presenca.guerreiro_id].avatar,
            nick=avatares_e_nicks[presenca.guerreiro_id].nick,
            modo=presenca.modo.value,
            confirmador_id=presenca.confirmador_id,
        )
        for presenca in presencas
        if presenca.guerreiro_id in avatares_e_nicks
    ]


def _aguardando_aparelho(sessao: Session, aula_id: uuid.UUID) -> list[GuerreiroDoPainelSaida]:
    """Presente na aula e ainda sem equipe formada nela — lista derivada,
    sem entidade nem fila explícita (`RF-02-43`)."""
    ja_em_equipe = (
        sessao.query(IntegranteDaEquipe.persona_id)
        .join(Equipe, Equipe.id == IntegranteDaEquipe.equipe_id)
        .filter(Equipe.aula_id == aula_id)
    )
    presentes_sem_equipe = (
        sessao.query(Presenca.guerreiro_id)
        .filter(Presenca.aula_id == aula_id, ~Presenca.guerreiro_id.in_(ja_em_equipe))
        .all()
    )
    ids = [guerreiro_id for (guerreiro_id,) in presentes_sem_equipe]
    avatares_e_nicks = buscar_avatares_e_nicks(sessao, ids)
    return [
        GuerreiroDoPainelSaida(
            guerreiro_id=guerreiro_id,
            avatar=avatares_e_nicks[guerreiro_id].avatar,
            nick=avatares_e_nicks[guerreiro_id].nick,
        )
        for guerreiro_id in ids
        if guerreiro_id in avatares_e_nicks
    ]


def _equipes(sessao: Session, aula_id: uuid.UUID) -> list[EquipeDoPainelSaida]:
    resultado = []
    for equipe in equipes_da_aula(sessao, aula_id):
        integrantes = sessao.query(IntegranteDaEquipe).filter_by(equipe_id=equipe.id).all()
        avatares_e_nicks = buscar_avatares_e_nicks(sessao, [i.persona_id for i in integrantes])

        missao_id = None
        missao_titulo = None
        if equipe.atividade_corrente_id is not None:
            atividade = sessao.get(Atividade, equipe.atividade_corrente_id)
            if atividade is not None:
                missao = sessao.get(Missao, atividade.missao_id)
                missao_id = missao.id
                missao_titulo = missao.titulo

        resultado.append(
            EquipeDoPainelSaida(
                id=equipe.id,
                integrantes=[
                    avatares_e_nicks[i.persona_id]
                    for i in integrantes
                    if i.persona_id in avatares_e_nicks
                ],
                missao_id=missao_id,
                missao_titulo=missao_titulo,
            )
        )
    return resultado


def _atividades_previstas(sessao: Session, aula_id: uuid.UUID) -> list[AtividadePrevistaSaida]:
    """A programação declarada na aula, de trilha publicada — a mesma que a
    equipe lê em `equipes.regra.programacao_do_encontro` (`RF-02-44`)."""
    atividades = (
        sessao.query(Atividade)
        .join(Missao, Missao.id == Atividade.missao_id)
        .join(Trilha, Trilha.id == Missao.trilha_id)
        .filter(Atividade.aula_id == aula_id, Trilha.situacao == SituacaoDaTrilha.publicada)
        .all()
    )
    resultado = []
    for atividade in atividades:
        missao = sessao.get(Missao, atividade.missao_id)
        resultado.append(
            AtividadePrevistaSaida(
                id=atividade.id,
                titulo=atividade.titulo,
                missao_id=missao.id,
                missao_titulo=missao.titulo,
            )
        )
    return resultado


def _recursos_providos(sessao: Session, aula_id: uuid.UUID) -> list[RecursoProvidoSaida]:
    """As reservas que o agendamento constituiu, independente do estado —
    aula sem recurso declarado devolve lista vazia, sem erro (`RF-02-44`)."""
    reservas = sessao.query(Reserva).filter_by(aula_id=aula_id).all()
    return [
        RecursoProvidoSaida(
            tipo_de_recurso_id=reserva.tipo_de_recurso_id, quantidade=reserva.quantidade
        )
        for reserva in reservas
    ]


def _saldo_do_ponto_de_apoio(
    sessao: Session, ponto_de_apoio_id: uuid.UUID
) -> list[SaldoDoTipoSaida]:
    """O saldo dos tipos do catálogo configurável, sem tipo algum fixado em
    código (`RF-02-45`, `RN-07-36`)."""
    pares = saldos_por_ponto_de_apoio(sessao, ponto_de_apoio_id=ponto_de_apoio_id)
    return [
        SaldoDoTipoSaida(tipo_de_recurso_id=tipo_de_recurso_id, saldo=saldo)
        for tipo_de_recurso_id, saldo in pares
    ]


def _pendencias(sessao: Session, aula: Aula) -> list[PendenciaDoPainelSaida]:
    """O que falta lançar antes de a aula terminar: a atividade realizada
    ainda não lançada e os termos de biometria assinados no encontro e
    ainda sem digitalização anexada (`RF-02-46`, `RF-02-47`, `RF-02-69`)."""
    pendencias: list[PendenciaDoPainelSaida] = []
    if aula.situacao not in _SITUACOES_COM_DESFECHO:
        pendencias.append(PendenciaDoPainelSaida(tipo="lancamento_da_atividade_realizada"))

    guerreiro_ids = [
        guerreiro_id
        for (guerreiro_id,) in sessao.query(Presenca.guerreiro_id).filter_by(aula_id=aula.id).all()
    ]
    if not guerreiro_ids:
        return pendencias

    avatares_e_nicks = buscar_avatares_e_nicks(sessao, guerreiro_ids)
    momento = agora()
    for guerreiro_id in guerreiro_ids:
        consentimento = consultar_consentimento_vigente_em(
            sessao, guerreiro_id=guerreiro_id, tipo=TipoDeConsentimento.biometria, em=momento
        )
        if consentimento is None or consentimento.origem != OrigemDoConsentimento.impressa:
            continue
        if consentimento.decisao != DecisaoDeConsentimento.concede:
            continue
        tem_anexo = (
            sessao.query(AnexoDoTermo).filter_by(consentimento_id=consentimento.id).first()
            is not None
        )
        if tem_anexo:
            continue
        pendencias.append(
            PendenciaDoPainelSaida(
                tipo="digitalizacao_do_termo",
                guerreiro_id=guerreiro_id,
                nick=avatares_e_nicks[guerreiro_id].nick
                if guerreiro_id in avatares_e_nicks
                else None,
                consentimento_id=consentimento.id,
            )
        )
    return pendencias


def montar_painel_do_dia(sessao: Session, *, operador: Persona) -> PainelDoDiaSaida:
    """A leitura agregada do encontro em andamento, numa única chamada —
    fora a escolha corrente da equipe, tudo aqui é recomputado a cada
    consulta (`RF-02-41` a `RF-02-47`, `RF-02-69`, `RN-02-20`)."""
    if operador.papel not in (Papel.admin, Papel.mestre):
        raise PermissaoNegada(mensagem="Só Admin ou Mestre leem o painel do dia.")

    aula = _resolver_aula(sessao, operador=operador)
    if aula is None:
        return PainelDoDiaSaida(aula_id=None, comunidade_virtual_id=None, ponto_de_apoio_id=None)

    return PainelDoDiaSaida(
        aula_id=aula.id,
        comunidade_virtual_id=aula.comunidade_virtual_id,
        ponto_de_apoio_id=aula.ponto_de_apoio_id,
        presencas=_presencas(sessao, aula.id),
        aguardando_aparelho=_aguardando_aparelho(sessao, aula.id),
        equipes=_equipes(sessao, aula.id),
        atividades_previstas=_atividades_previstas(sessao, aula.id),
        recursos_providos=_recursos_providos(sessao, aula.id),
        saldo_do_ponto_de_apoio=_saldo_do_ponto_de_apoio(sessao, aula.ponto_de_apoio_id),
        pendencias=_pendencias(sessao, aula),
    )
