import uuid
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from sqlalchemy.orm import Session

from ..aulas.modelo import Aula, RecursoDeclaradoDaAula, SituacaoDaAula
from ..comunidades.modelo import ComunidadeVirtual
from ..erros import PermissaoNegada
from ..personas.modelo import Papel, Persona
from ..pontos_de_apoio.modelo import PontoDeApoio
from ..recursos.modelo import TipoDeRecurso
from ..recursos.regra import consultar_valor_de_referencia
from ..reservas.regra import disponivel_de
from ..tempo import agora


@dataclass(frozen=True)
class NecessidadeDeRecurso:
    """A falta de uma aula pendente de lastro, por tipo de recurso — nunca
    gravada, sempre recalculada da leitura, como o saldo (`RF-07-18`,
    `RF-07-27`, design — Decisions 1). O nome ao lado do identificador
    poupa a App 08 de uma rota de cadastro da gestão (`RF-14-24`, design —
    Decisions 6)."""

    aula_id: uuid.UUID
    tipo_de_recurso_id: uuid.UUID
    tipo_de_recurso_nome: str
    quantidade_faltante: Decimal
    valor_em_moedas: Decimal | None
    comunidade_virtual_id: uuid.UUID
    comunidade_virtual_nome: str
    ponto_de_apoio_id: uuid.UUID
    ponto_de_apoio_nome: str
    inicio_em: datetime
    fim_em: datetime


def derivar_necessidades(
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


def consultar_necessidades_publicas(sessao: Session) -> list[NecessidadeDeRecurso]:
    """A vitrine enxerga a falta de todas as comunidades, sem credencial de
    persona (`RF-07-27`, `RF-03-47`)."""
    return derivar_necessidades(sessao)


def consultar_necessidades_do_mestre(
    sessao: Session, *, operador: Persona
) -> list[NecessidadeDeRecurso]:
    """Restrita ao Mestre — a lista alcança só as aulas das comunidades a
    que ele está vinculado, pelo mesmo vínculo que `cancelar_aula` já
    confere; sem vínculo vigente, a lista sai vazia (`RF-07-27`, `RF-01-72`,
    design — Decisions 6)."""
    if operador.papel != Papel.mestre:
        raise PermissaoNegada(mensagem="Só o Mestre consulta as necessidades das suas comunidades.")

    vinculo = operador.vinculo_vigente
    if vinculo is None:
        return []
    return derivar_necessidades(sessao, comunidade_ids={vinculo.comunidade_virtual_id})
