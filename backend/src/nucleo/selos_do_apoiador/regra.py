import uuid
from dataclasses import dataclass

from sqlalchemy.orm import Session

from ..aportes.modelo import Aporte, AporteDeclarado
from ..missoes_do_apoiador.modelo import MissaoDoApoiador, NivelDeNecessidade, SituacaoDaMissao
from .modelo import FamiliaDeSelo, SeloDoApoiador

_NOME_DO_NIVEL = {
    0: "Sem aporte",
    1: "Apoiador",
    2: "Sustenta o encontro",
    3: "Sustenta o ciclo",
    4: "Sustenta a permanência",
}


@dataclass(frozen=True)
class SustentoDoApoiador:
    """Derivado dos níveis de necessidade das missões concluídas em que o
    Apoiador é participante, mais o primeiro aporte homologado — nunca
    gravado, e por isso nunca regride (`RF-14-67`, `RF-14-69`, `RN-14-35`,
    `RN-14-36`, design — Decisions 7). A escada para no nível 4: as duas
    vias do nível 5 não são verificáveis no núcleo (documento 09)."""

    nivel: int
    nome_do_nivel: str
    frente_que_falta: str


def _niveis_concluidos_por(sessao: Session, *, apoiador_id: uuid.UUID) -> set[NivelDeNecessidade]:
    linhas = (
        sessao.query(MissaoDoApoiador.nivel_de_necessidade)
        .join(AporteDeclarado, AporteDeclarado.missao_do_apoiador_id == MissaoDoApoiador.id)
        .join(Aporte, Aporte.aporte_declarado_id == AporteDeclarado.id)
        .filter(
            Aporte.provedor_id == apoiador_id,
            MissaoDoApoiador.situacao == SituacaoDaMissao.concluida,
        )
        .distinct()
        .all()
    )
    return {linha[0] for linha in linhas}


def _frente_que_falta(nivel: int, niveis_concluidos: set[NivelDeNecessidade]) -> str:
    if nivel == 0:
        return "Faça o primeiro aporte."
    if nivel == 1:
        return "Cubra uma missão do nível Acontecer."
    if nivel == 2:
        return "Cubra uma missão de outro nível de necessidade."
    if nivel == 3:
        if NivelDeNecessidade.permanecer not in niveis_concluidos:
            return "Cubra uma missão do nível Permanecer."
        return "Cubra uma missão de um terceiro nível de necessidade."
    return "Vire Mestre."


def derivar_sustento(sessao: Session, *, apoiador_id: uuid.UUID) -> SustentoDoApoiador:
    """A escada do documento 14 §7: nível 1 pelo primeiro aporte homologado,
    2 a 4 pelos níveis de necessidade das missões concluídas em que o
    Apoiador participou — sobe por frente diferente coberta, nunca por
    volume (`RF-14-67`, `RN-14-35`)."""
    tem_aporte_homologado = (
        sessao.query(Aporte.id).filter(Aporte.provedor_id == apoiador_id).first() is not None
    )
    niveis_concluidos = _niveis_concluidos_por(sessao, apoiador_id=apoiador_id)

    nivel = 1 if tem_aporte_homologado else 0
    if NivelDeNecessidade.acontecer in niveis_concluidos:
        nivel = max(nivel, 2)
    if len(niveis_concluidos) >= 2:
        nivel = max(nivel, 3)
    if len(niveis_concluidos) >= 3 and NivelDeNecessidade.permanecer in niveis_concluidos:
        nivel = max(nivel, 4)

    return SustentoDoApoiador(
        nivel=nivel,
        nome_do_nivel=_NOME_DO_NIVEL[nivel],
        frente_que_falta=_frente_que_falta(nivel, niveis_concluidos),
    )


def listar_selos(
    sessao: Session, *, apoiador_id: uuid.UUID
) -> dict[FamiliaDeSelo, list[SeloDoApoiador]]:
    """Os selos do próprio Apoiador, agrupados por família — somente
    leitura, e a permissão é conferida por quem chama, como em
    `meus_aportes` (`RF-14-68`, `RN-14-38`)."""
    selos = (
        sessao.query(SeloDoApoiador)
        .filter(SeloDoApoiador.apoiador_id == apoiador_id)
        .order_by(SeloDoApoiador.creditado_em)
        .all()
    )
    agrupado: dict[FamiliaDeSelo, list[SeloDoApoiador]] = {}
    for selo in selos:
        agrupado.setdefault(selo.familia, []).append(selo)
    return agrupado
