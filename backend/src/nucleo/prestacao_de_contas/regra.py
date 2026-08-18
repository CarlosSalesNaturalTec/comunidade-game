import uuid
from dataclasses import dataclass
from decimal import Decimal

from sqlalchemy import func
from sqlalchemy.orm import Session

from ..aulas.modelo import Aula
from ..livro_razao.modelo import Lancamento, NaturezaDoLancamento
from ..poder_sustentador.regra import poder_sustentador_por_provedor


@dataclass(frozen=True)
class MovimentadoPorProvedor:
    provedor_id: uuid.UUID
    movimentado_em_moedas: Decimal


def movimentado_total_e_por_provedor(
    sessao: Session,
) -> tuple[Decimal, list[MovimentadoPorProvedor]]:
    """O movimentado total e por provedor, lido no momento da chamada, sem
    fechamento periódico nem número guardado à parte — reaproveita a mesma
    derivação da capacidade `poder-sustentador` para as duas leituras não
    divergirem (`RF-07-16`, `RN-07-31`, `RN-07-15`, design — Decisions 1, 5)."""
    por_provedor = poder_sustentador_por_provedor(sessao)
    total = sum(por_provedor.values(), Decimal("0"))
    linhas = [
        MovimentadoPorProvedor(provedor_id=provedor_id, movimentado_em_moedas=valor)
        for provedor_id, valor in por_provedor.items()
    ]
    return total, linhas


@dataclass(frozen=True)
class ConsumoDaAula:
    aula_id: uuid.UUID
    comunidade_virtual_id: uuid.UUID
    consumo_em_moedas: Decimal


@dataclass(frozen=True)
class ConsumoDaComunidade:
    comunidade_virtual_id: uuid.UUID
    consumo_em_moedas: Decimal


def consumo_por_aula_e_comunidade(
    sessao: Session,
) -> tuple[list[ConsumoDaAula], list[ConsumoDaComunidade]]:
    """O consumo por aula e por comunidade, somado dos débitos pelo valor
    que cada um gravou no ato — nunca revalorado pela tabela de referência
    corrente. A comunidade é a do ponto de apoio em que a aula acontece,
    que já é a mesma `comunidade_virtual_id` gravada na própria aula
    (`RN-07-33`). Aula sem baixa não aparece (`RF-07-16`, `RN-07-33`,
    `RN-07-36`, design — Decisions 5)."""
    por_aula = (
        sessao.query(
            Lancamento.aula_id,
            Aula.comunidade_virtual_id,
            func.sum(Lancamento.valor_em_moedas),
        )
        .join(Aula, Aula.id == Lancamento.aula_id)
        .filter(Lancamento.natureza == NaturezaDoLancamento.debito)
        .group_by(Lancamento.aula_id, Aula.comunidade_virtual_id)
        .all()
    )
    aulas = [
        ConsumoDaAula(
            aula_id=aula_id,
            comunidade_virtual_id=comunidade_id,
            consumo_em_moedas=Decimal(total),
        )
        for aula_id, comunidade_id, total in por_aula
    ]

    por_comunidade = (
        sessao.query(Aula.comunidade_virtual_id, func.sum(Lancamento.valor_em_moedas))
        .join(Aula, Aula.id == Lancamento.aula_id)
        .filter(Lancamento.natureza == NaturezaDoLancamento.debito)
        .group_by(Aula.comunidade_virtual_id)
        .all()
    )
    comunidades = [
        ConsumoDaComunidade(comunidade_virtual_id=comunidade_id, consumo_em_moedas=Decimal(total))
        for comunidade_id, total in por_comunidade
    ]

    return aulas, comunidades
