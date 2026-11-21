import enum
import uuid
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from sqlalchemy import func
from sqlalchemy.orm import Session

from ..aulas.modelo import Aula, RecursoDeclaradoDaAula, SituacaoDaAula
from ..aulas.regra import aula_de_referencia_da_comunidade
from ..comunidades.modelo import ComunidadeVirtual, VinculoJogador
from ..comunidades.regra import comunidades_do_mestre
from ..erros import PermissaoNegada
from ..personas.modelo import Papel, Persona
from ..pontos_de_apoio.modelo import PontoDeApoio
from ..recompensas_de_marco.modelo import EntregaDeRecompensa, RecompensaDeMarco
from ..recursos.modelo import TipoDeRecurso
from ..recursos.regra import consultar_valor_de_referencia
from ..reservas.regra import disponivel_de
from ..tempo import agora
from ..trilhas.modelo import Atividade, Missao, Trilha


class EspecieDaNecessidade(enum.StrEnum):
    """As duas espécies de necessidade: a da aula pendente de lastro e a da
    recompensa de marco (`RF-07-28`, `RF-07-54`, documento 04 §1)."""

    aula = "aula"
    recompensa_de_marco = "recompensa_de_marco"


@dataclass(frozen=True)
class NecessidadeDeRecurso:
    """A falta de recurso — nunca gravada, sempre recalculada da leitura,
    como o saldo (`RF-07-18`, `RF-07-27`, design — Decisions 1). O nome ao
    lado do identificador poupa a App 08 de uma rota de cadastro da gestão
    (`RF-14-24`, design — Decisions 6).

    A da aula identifica-se por aula + tipo e traz o horário; a da
    recompensa de marco, por comunidade + trilha + tipo, sem aula nem
    horário (`RF-07-54`, change `necessidade-da-recompensa-de-marco`,
    design — decisões 1, 3)."""

    especie: EspecieDaNecessidade
    tipo_de_recurso_id: uuid.UUID
    tipo_de_recurso_nome: str
    quantidade_faltante: Decimal
    valor_em_moedas: Decimal | None
    comunidade_virtual_id: uuid.UUID
    comunidade_virtual_nome: str
    ponto_de_apoio_id: uuid.UUID
    ponto_de_apoio_nome: str
    aula_id: uuid.UUID | None = None
    inicio_em: datetime | None = None
    fim_em: datetime | None = None
    trilha_id: uuid.UUID | None = None
    trilha_nome: str | None = None

    @property
    def chave(self) -> tuple:
        """A identidade da necessidade, que missão e declaração apontam:
        `(aula, tipo)` ou `(comunidade, trilha, tipo)` (design — decisão 7)."""
        if self.especie == EspecieDaNecessidade.aula:
            return (self.aula_id, self.tipo_de_recurso_id)
        return (self.comunidade_virtual_id, self.trilha_id, self.tipo_de_recurso_id)


def chave_da_necessidade(
    *,
    tipo_de_recurso_id: uuid.UUID | None,
    aula_id: uuid.UUID | None = None,
    comunidade_virtual_id: uuid.UUID | None = None,
    trilha_id: uuid.UUID | None = None,
) -> tuple:
    """A chave de quem aponta a necessidade, no mesmo formato de
    `NecessidadeDeRecurso.chave`."""
    if aula_id is not None:
        return (aula_id, tipo_de_recurso_id)
    return (comunidade_virtual_id, trilha_id, tipo_de_recurso_id)


class _Cache:
    """Os nomes e as vigências lidos uma vez por derivação."""

    def __init__(self, sessao: Session) -> None:
        self.sessao = sessao
        self.hoje = agora().date()
        self._por_classe: dict[tuple[type, uuid.UUID], object] = {}

    def obter(self, classe: type, id_: uuid.UUID):
        chave = (classe, id_)
        if chave not in self._por_classe:
            self._por_classe[chave] = self.sessao.get(classe, id_)
        return self._por_classe[chave]

    def valorar(self, tipo: TipoDeRecurso, falta: Decimal) -> Decimal | None:
        referencia = consultar_valor_de_referencia(self.sessao, tipo=tipo, data=self.hoje)
        if referencia is None:
            return None
        return (falta * referencia.valor_em_moedas).quantize(Decimal("0.01"))


def derivar_necessidades(
    sessao: Session, *, comunidade_ids: set[uuid.UUID] | None = None
) -> list[NecessidadeDeRecurso]:
    """As necessidades das duas espécies: as da aula primeiro, pela data, e
    as da recompensa depois, por comunidade, trilha e tipo (design — decisão
    4). As duas não disputam saldo: a aula só declara consumo do encontro, e
    a recompensa só recompensa (`RN-07-41`). `comunidade_ids` filtra para a
    leitura do Mestre; `None` deriva de todas, para a rota pública."""
    cache = _Cache(sessao)
    da_recompensa = _derivar_necessidades_da_recompensa(
        sessao, cache=cache, comunidade_ids=comunidade_ids
    )
    da_recompensa.sort(
        key=lambda n: (n.comunidade_virtual_nome, n.trilha_nome, n.tipo_de_recurso_nome)
    )
    return _derivar_necessidades_da_aula(sessao, comunidade_ids=comunidade_ids) + da_recompensa


def _derivar_necessidades_da_aula(
    sessao: Session, *, comunidade_ids: set[uuid.UUID] | None = None
) -> list[NecessidadeDeRecurso]:
    """Deriva a necessidade de cada par aula + tipo de recurso das aulas em
    **pendente de lastro**, por atribuição gulosa do disponível de cada par
    tipo/ponto de apoio às aulas candidatas, em `inicio_em asc` — a mesma
    ordem de `confirmar_aulas_pendentes()` (`RF-07-18`, `RN-07-37`, design —
    Decisions 2, 3). `comunidade_ids` filtra a derivação para a leitura do
    Mestre; `None` deriva de todas, para a rota pública.
    """
    consulta = sessao.query(Aula).filter(Aula.situacao == SituacaoDaAula.pendente_de_lastro)
    if comunidade_ids is not None:
        consulta = consulta.filter(Aula.comunidade_virtual_id.in_(comunidade_ids))
    aulas = consulta.all()
    if not aulas:
        return []

    aulas_por_id = {aula.id: aula for aula in aulas}
    declarados = (
        sessao.query(RecursoDeclaradoDaAula)
        .filter(RecursoDeclaradoDaAula.aula_id.in_(aulas_por_id.keys()))
        .all()
    )

    por_par: dict[tuple[uuid.UUID, uuid.UUID], list[tuple[Aula, RecursoDeclaradoDaAula]]] = {}
    for declarado in declarados:
        aula = aulas_por_id[declarado.aula_id]
        chave = (declarado.tipo_de_recurso_id, aula.ponto_de_apoio_id)
        por_par.setdefault(chave, []).append((aula, declarado))

    hoje = agora().date()
    tipos: dict[uuid.UUID, TipoDeRecurso] = {}
    comunidades: dict[uuid.UUID, ComunidadeVirtual] = {}
    pontos_de_apoio: dict[uuid.UUID, PontoDeApoio] = {}
    necessidades: list[NecessidadeDeRecurso] = []
    for (tipo_id, ponto_de_apoio_id), pares in por_par.items():
        restante = disponivel_de(
            sessao, tipo_de_recurso_id=tipo_id, ponto_de_apoio_id=ponto_de_apoio_id
        )
        for aula, declarado in sorted(pares, key=lambda par: par[0].inicio_em):
            atribuido = min(declarado.quantidade, max(restante, Decimal("0")))
            restante -= atribuido
            falta = declarado.quantidade - atribuido
            if falta <= 0:
                continue

            if tipo_id not in tipos:
                tipos[tipo_id] = sessao.get(TipoDeRecurso, tipo_id)
            referencia = consultar_valor_de_referencia(sessao, tipo=tipos[tipo_id], data=hoje)
            valor_em_moedas = (
                (falta * referencia.valor_em_moedas).quantize(Decimal("0.01"))
                if referencia is not None
                else None
            )

            if aula.comunidade_virtual_id not in comunidades:
                comunidades[aula.comunidade_virtual_id] = sessao.get(
                    ComunidadeVirtual, aula.comunidade_virtual_id
                )
            if ponto_de_apoio_id not in pontos_de_apoio:
                pontos_de_apoio[ponto_de_apoio_id] = sessao.get(PontoDeApoio, ponto_de_apoio_id)

            necessidades.append(
                NecessidadeDeRecurso(
                    especie=EspecieDaNecessidade.aula,
                    aula_id=aula.id,
                    tipo_de_recurso_id=tipo_id,
                    tipo_de_recurso_nome=tipos[tipo_id].nome,
                    quantidade_faltante=falta,
                    valor_em_moedas=valor_em_moedas,
                    comunidade_virtual_id=aula.comunidade_virtual_id,
                    comunidade_virtual_nome=comunidades[aula.comunidade_virtual_id].nome,
                    ponto_de_apoio_id=ponto_de_apoio_id,
                    ponto_de_apoio_nome=pontos_de_apoio[ponto_de_apoio_id].nome,
                    inicio_em=aula.inicio_em,
                    fim_em=aula.fim_em,
                )
            )

    necessidades.sort(key=lambda necessidade: (necessidade.inicio_em, str(necessidade.aula_id)))
    return necessidades


def _trilhas_da_comunidade(
    sessao: Session, *, comunidade_id: uuid.UUID
) -> list[tuple[uuid.UUID, datetime]]:
    """As trilhas com atividade não removida em aula não cancelada da
    comunidade — passada, em andamento ou futura —, cada uma com a data da
    atividade mais antiga, que é a ordem de contagem (`RF-07-54`, decisão
    do fundador de 2026-11-21, design — decisão 2)."""
    return (
        sessao.query(Missao.trilha_id, func.min(Aula.inicio_em))
        .join(Atividade, Atividade.missao_id == Missao.id)
        .join(Aula, Aula.id == Atividade.aula_id)
        .filter(
            Aula.comunidade_virtual_id == comunidade_id,
            Aula.situacao != SituacaoDaAula.cancelada,
            Atividade.removida_em.is_(None),
        )
        .group_by(Missao.trilha_id)
        .all()
    )


def _derivar_necessidades_da_recompensa(
    sessao: Session, *, cache: _Cache, comunidade_ids: set[uuid.UUID] | None
) -> list[NecessidadeDeRecurso]:
    """A necessidade da recompensa de marco, por comunidade, ponto de apoio,
    tipo e trilha: Guerreiros(as) com vínculo vigente que ainda não
    receberam cada recompensa da trilha, vezes a quantidade dela, menos o
    disponível no ponto de apoio da aula imediatamente anterior. Comunidade
    sem aula anterior não gera necessidade. Disputando o mesmo par tipo e
    ponto de apoio, conta primeiro a trilha de atividade em aula mais antiga
    (`RF-07-54`, `RF-07-18`, `RN-07-42`, design — decisão 2)."""
    consulta = sessao.query(Aula.comunidade_virtual_id).filter(
        Aula.situacao != SituacaoDaAula.cancelada
    )
    if comunidade_ids is not None:
        consulta = consulta.filter(Aula.comunidade_virtual_id.in_(comunidade_ids))
    comunidades = sorted({linha[0] for linha in consulta.distinct().all()}, key=str)

    # (tipo, ponto) -> [(data de ordem, trilha_id, comunidade_id, pedido)]
    candidatas: dict[
        tuple[uuid.UUID, uuid.UUID], list[tuple[datetime, uuid.UUID, uuid.UUID, Decimal]]
    ] = {}
    for comunidade_id in comunidades:
        referencia = aula_de_referencia_da_comunidade(sessao, comunidade_id=comunidade_id)
        if referencia is None:
            continue
        trilhas = dict(_trilhas_da_comunidade(sessao, comunidade_id=comunidade_id))
        if not trilhas:
            continue
        guerreiros = {
            linha[0]
            for linha in sessao.query(VinculoJogador.guerreiro_id)
            .filter(
                VinculoJogador.comunidade_virtual_id == comunidade_id,
                VinculoJogador.data_fim.is_(None),
            )
            .all()
        }
        if not guerreiros:
            continue
        recompensas = (
            sessao.query(RecompensaDeMarco)
            .filter(RecompensaDeMarco.trilha_id.in_(trilhas.keys()))
            .all()
        )
        if not recompensas:
            continue
        entregues = dict(
            sessao.query(
                EntregaDeRecompensa.recompensa_de_marco_id,
                func.count(func.distinct(EntregaDeRecompensa.guerreiro_id)),
            )
            .filter(
                EntregaDeRecompensa.recompensa_de_marco_id.in_([r.id for r in recompensas]),
                EntregaDeRecompensa.guerreiro_id.in_(guerreiros),
            )
            .group_by(EntregaDeRecompensa.recompensa_de_marco_id)
            .all()
        )
        pedidos: dict[tuple[uuid.UUID, uuid.UUID], Decimal] = {}
        for recompensa in recompensas:
            faltam_receber = len(guerreiros) - entregues.get(recompensa.id, 0)
            if faltam_receber <= 0:
                continue
            chave = (recompensa.trilha_id, recompensa.tipo_de_recurso_id)
            pedidos[chave] = (
                pedidos.get(chave, Decimal("0")) + faltam_receber * recompensa.quantidade
            )
        for (trilha_id, tipo_id), pedido in pedidos.items():
            candidatas.setdefault((tipo_id, referencia.ponto_de_apoio_id), []).append(
                (trilhas[trilha_id], trilha_id, comunidade_id, pedido)
            )

    necessidades: list[NecessidadeDeRecurso] = []
    for (tipo_id, ponto_de_apoio_id), itens in candidatas.items():
        restante = disponivel_de(
            sessao, tipo_de_recurso_id=tipo_id, ponto_de_apoio_id=ponto_de_apoio_id
        )
        for _, trilha_id, comunidade_id, pedido in sorted(
            itens, key=lambda item: (item[0], str(item[1]))
        ):
            atribuido = min(pedido, max(restante, Decimal("0")))
            restante -= atribuido
            falta = pedido - atribuido
            if falta <= 0:
                continue
            tipo = cache.obter(TipoDeRecurso, tipo_id)
            necessidades.append(
                NecessidadeDeRecurso(
                    especie=EspecieDaNecessidade.recompensa_de_marco,
                    tipo_de_recurso_id=tipo_id,
                    tipo_de_recurso_nome=tipo.nome,
                    quantidade_faltante=falta,
                    valor_em_moedas=cache.valorar(tipo, falta),
                    comunidade_virtual_id=comunidade_id,
                    comunidade_virtual_nome=cache.obter(ComunidadeVirtual, comunidade_id).nome,
                    ponto_de_apoio_id=ponto_de_apoio_id,
                    ponto_de_apoio_nome=cache.obter(PontoDeApoio, ponto_de_apoio_id).nome,
                    trilha_id=trilha_id,
                    trilha_nome=cache.obter(Trilha, trilha_id).nome,
                )
            )
    return necessidades


def consultar_necessidades_publicas(sessao: Session) -> list[NecessidadeDeRecurso]:
    """A vitrine enxerga a falta de todas as comunidades, das aulas e das
    recompensas de marco, sem credencial de persona (`RF-07-27`, `RF-03-47`,
    `RF-07-54`)."""
    return derivar_necessidades(sessao)


def consultar_necessidades_do_mestre(
    sessao: Session, *, operador: Persona
) -> list[NecessidadeDeRecurso]:
    """Restrita ao Mestre — a lista alcança só as aulas e as recompensas
    das comunidades a que ele está vinculado, pelo mesmo vínculo que `cancelar_aula` já
    confere; sem vínculo algum, a lista sai vazia (`RF-07-27`, `RF-01-72`,
    design — Decisions 6)."""
    if operador.papel != Papel.mestre:
        raise PermissaoNegada(mensagem="Só o Mestre consulta as necessidades das suas comunidades.")

    alvos = comunidades_do_mestre(sessao, mestre=operador)
    if not alvos:
        return []
    return derivar_necessidades(sessao, comunidade_ids=alvos)
