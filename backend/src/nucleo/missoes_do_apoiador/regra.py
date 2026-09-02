import uuid
from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from sqlalchemy import func
from sqlalchemy.orm import Session

from ..aportes.modelo import Aporte, AporteDeclarado
from ..aulas.modelo import Aula
from ..erros import DespublicacaoDeMissaoConcluidaRecusada, ErroDeValidacao, PermissaoNegada
from ..necessidades.regra import derivar_necessidades
from ..personas.modelo import Papel, Persona
from ..recursos.modelo import TipoDeRecurso
from ..selos_do_apoiador.modelo import FamiliaDeSelo, SeloDoApoiador
from ..tempo import agora
from .modelo import MissaoDoApoiador, NivelDeNecessidade, SituacaoDaMissao

_SELO_DE_MUTIRAO = "Mutirão"


def publicar_missao(
    sessao: Session,
    *,
    operador: Persona,
    aula: Aula | None,
    tipo: TipoDeRecurso | None,
    nivel_de_necessidade: NivelDeNecessidade | None,
    titulo: str | None,
    o_que_se_pede: str | None,
    quantidade: Decimal | None,
    prazo: date | None,
    selo_nome: str | None,
    selo_familia: FamiliaDeSelo | None,
) -> MissaoDoApoiador:
    """Só Admin publica, a partir de uma necessidade de recurso em aberto —
    o par aula + tipo de recurso precisa estar entre as necessidades
    derivadas no momento do ato (`RF-02-102`, `RF-02-103`, `RN-02-31`,
    `RN-14-31`, design — Decisions 1)."""
    if operador.papel != Papel.admin:
        raise PermissaoNegada(mensagem="Só o Admin publica missão do Apoiador.")
    if aula is None or tipo is None:
        raise ErroDeValidacao(
            mensagem="Missão exige a aula e o tipo de recurso da necessidade de origem.",
            campo="aula_id",
        )
    if nivel_de_necessidade is None:
        raise ErroDeValidacao(
            mensagem="Missão exige o nível de necessidade.", campo="nivel_de_necessidade"
        )
    if not titulo:
        raise ErroDeValidacao(mensagem="Missão exige o título.", campo="titulo")
    if not o_que_se_pede:
        raise ErroDeValidacao(mensagem="Missão exige o que se pede.", campo="o_que_se_pede")
    if quantidade is None or quantidade <= 0:
        raise ErroDeValidacao(
            mensagem="Missão exige quantidade maior que zero.", campo="quantidade"
        )
    if prazo is None:
        raise ErroDeValidacao(mensagem="Missão exige o prazo.", campo="prazo")
    if not selo_nome:
        raise ErroDeValidacao(mensagem="Missão exige o selo que rende.", campo="selo_nome")
    if selo_familia is None:
        raise ErroDeValidacao(mensagem="Missão exige a família do selo.", campo="selo_familia")

    pares_com_necessidade = {
        (necessidade.aula_id, necessidade.tipo_de_recurso_id)
        for necessidade in derivar_necessidades(sessao)
    }
    if (aula.id, tipo.id) not in pares_com_necessidade:
        raise ErroDeValidacao(
            mensagem="Não há necessidade de recurso publicada para esta aula e tipo de recurso.",
            campo="aula_id",
        )

    missao = MissaoDoApoiador(
        aula_id=aula.id,
        tipo_de_recurso_id=tipo.id,
        nivel_de_necessidade=nivel_de_necessidade,
        titulo=titulo,
        o_que_se_pede=o_que_se_pede,
        quantidade=quantidade,
        prazo=prazo,
        selo_nome=selo_nome,
        selo_familia=selo_familia,
        situacao=SituacaoDaMissao.aberta,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(missao)
    sessao.flush()
    return missao


def despublicar_missao(
    sessao: Session, missao: MissaoDoApoiador, *, operador: Persona
) -> MissaoDoApoiador:
    """Só Admin despublica; a missão sai das listas sem estornar aporte já
    homologado, e a já concluída não se despublica (`RF-02-105`, `RN-02-31`,
    `RN-14-32`)."""
    if operador.papel != Papel.admin:
        raise PermissaoNegada(mensagem="Só o Admin despublica missão do Apoiador.")
    if missao.situacao == SituacaoDaMissao.concluida:
        raise DespublicacaoDeMissaoConcluidaRecusada()

    missao.situacao = SituacaoDaMissao.despublicada
    sessao.flush()
    return missao


@dataclass(frozen=True)
class MissaoDerivada:
    """A missão com o coberto, o que falta e a vencida derivados dos
    aportes homologados — nunca gravados (`RF-14-61`, `RF-14-62`, `RF-14-64`,
    `RF-14-71`, `RF-14-72`, `RF-02-104`, design — Decisions 2, 3, 4)."""

    missao: MissaoDoApoiador
    coberto: Decimal
    falta: Decimal
    vencida: bool
    tem_necessidade_por_tras: bool


def _coberto_por_missao(
    sessao: Session, *, missao_ids: list[uuid.UUID]
) -> dict[uuid.UUID, Decimal]:
    if not missao_ids:
        return {}
    linhas = (
        sessao.query(AporteDeclarado.missao_do_apoiador_id, func.sum(Aporte.valor_em_moedas))
        .join(Aporte, Aporte.aporte_declarado_id == AporteDeclarado.id)
        .filter(AporteDeclarado.missao_do_apoiador_id.in_(missao_ids))
        .group_by(AporteDeclarado.missao_do_apoiador_id)
        .all()
    )
    return {missao_id: Decimal(total).quantize(Decimal("0.01")) for missao_id, total in linhas}


def derivar_missoes(sessao: Session) -> list[MissaoDerivada]:
    """Deriva o coberto, o que falta e a vencida de toda missão publicada, a
    partir dos aportes homologados que a apontam (design — Decisions 2, 3,
    4). Quem lê filtra o que precisa: a leitura pública só mostra a aberta,
    não vencida e ainda com necessidade por trás; a do Admin alcança
    qualquer situação."""
    missoes = sessao.query(MissaoDoApoiador).all()
    if not missoes:
        return []

    coberto_por_missao = _coberto_por_missao(sessao, missao_ids=[missao.id for missao in missoes])
    pares_com_necessidade = {
        (necessidade.aula_id, necessidade.tipo_de_recurso_id)
        for necessidade in derivar_necessidades(sessao)
    }
    hoje = agora().date()

    derivadas = []
    for missao in missoes:
        coberto = coberto_por_missao.get(missao.id, Decimal("0.00"))
        falta = max(missao.quantidade - coberto, Decimal("0.00"))
        vencida = missao.situacao == SituacaoDaMissao.aberta and missao.prazo < hoje
        derivadas.append(
            MissaoDerivada(
                missao=missao,
                coberto=coberto,
                falta=falta,
                vencida=vencida,
                tem_necessidade_por_tras=(missao.aula_id, missao.tipo_de_recurso_id)
                in pares_com_necessidade,
            )
        )
    return derivadas


def missoes_abertas_e_visiveis(sessao: Session) -> list[MissaoDerivada]:
    """A leitura pública e a do Apoiador: só a aberta, não vencida e ainda
    com necessidade de recurso publicada por trás (`RF-14-71`, `RF-14-72`)."""
    return [
        derivada
        for derivada in derivar_missoes(sessao)
        if derivada.missao.situacao == SituacaoDaMissao.aberta
        and not derivada.vencida
        and derivada.tem_necessidade_por_tras
    ]


def _participantes_de(sessao: Session, *, missao_id: uuid.UUID) -> list[uuid.UUID]:
    linhas = (
        sessao.query(Aporte.provedor_id)
        .join(AporteDeclarado, AporteDeclarado.id == Aporte.aporte_declarado_id)
        .filter(AporteDeclarado.missao_do_apoiador_id == missao_id)
        .distinct()
        .all()
    )
    return [linha[0] for linha in linhas]


def _creditar_selo(
    sessao: Session,
    *,
    apoiador_id: uuid.UUID,
    missao_id: uuid.UUID,
    selo_nome: str,
    familia: FamiliaDeSelo,
) -> None:
    ja_creditado = (
        sessao.query(SeloDoApoiador.id)
        .filter_by(apoiador_id=apoiador_id, missao_do_apoiador_id=missao_id, selo_nome=selo_nome)
        .first()
    )
    if ja_creditado is not None:
        return
    sessao.add(
        SeloDoApoiador(
            apoiador_id=apoiador_id,
            familia=familia,
            selo_nome=selo_nome,
            missao_do_apoiador_id=missao_id,
        )
    )


def concluir_se_fechou(sessao: Session, *, missao: MissaoDoApoiador) -> None:
    """Chamada por `registrar_aporte()` na homologação de uma declaração de
    origem `missao`: recalcula o coberto e, fechando o saldo, grava
    `concluida` e credita o selo da missão a cada participante — mais o de
    mutirão, com mais de um — na mesma transação (`RF-14-65`, `RF-14-66`,
    `RN-14-32` a `RN-14-34`, design — Decisions 5, 8)."""
    coberto = _coberto_por_missao(sessao, missao_ids=[missao.id]).get(missao.id, Decimal("0.00"))
    if coberto < missao.quantidade:
        return

    missao.situacao = SituacaoDaMissao.concluida
    participantes = _participantes_de(sessao, missao_id=missao.id)
    for apoiador_id in participantes:
        _creditar_selo(
            sessao,
            apoiador_id=apoiador_id,
            missao_id=missao.id,
            selo_nome=missao.selo_nome,
            familia=missao.selo_familia,
        )
        if len(participantes) > 1:
            _creditar_selo(
                sessao,
                apoiador_id=apoiador_id,
                missao_id=missao.id,
                selo_nome=_SELO_DE_MUTIRAO,
                familia=FamiliaDeSelo.ato,
            )
    sessao.flush()
