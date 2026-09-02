import uuid
from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from sqlalchemy.orm import Session

from ..aportes.modelo import Aporte, AporteDeclarado, OrigemDaEscolhaDoAporte
from ..comunidades.modelo import ComunidadeVirtual
from ..comunidades.regra import resolver_vinculo_na_data
from ..consentimentos.regra import condicao_de_autorizacao_vigente
from ..desafios_extras.modelo import (
    ConclusaoDeDesafioExtra,
    DesafioExtra,
    Modalidade,
    SituacaoDoDesafioExtra,
)
from ..desafios_extras.regra import listar_desafios_do_proponente
from ..missoes_do_apoiador.modelo import MissaoDoApoiador
from ..ods.regra import cobertura_por_trilha, resolver_etiquetas_da_missao
from ..personas.modelo import Nick, Persona
from ..recursos.modelo import TipoDeRecurso
from ..trilhas.modelo import Missao, Trilha


@dataclass(frozen=True)
class ConcluinteExibivel:
    """Avatar e nick — nunca mais que isso — de quem concluiu e tem
    divulgação autorizada vigente (`RF-14-45`, `RN-14-22`)."""

    avatar: str | None
    nick: str


@dataclass(frozen=True)
class DesafioDeEfetividade:
    """Um desafio do proponente na leitura do painel. Os campos de
    conclusão são de um dos dois grupos, nunca os dois: `aberto` preenche
    a contagem, o período e os concluintes; `direcionado` preenche só
    `houve_conclusao`, e nem chega a consultar concluinte, trilha do
    destinatário ou qualquer outro dado dele (`RF-14-42`, `RF-14-47`,
    design — decisão 6)."""

    id: uuid.UUID
    trilha_id: uuid.UUID
    trilha_nome: str
    modalidade: str
    situacao: str
    etiquetas_ods: list[int]
    quantidade_de_conclusoes: int | None
    primeira_conclusao_em: date | None
    ultima_conclusao_em: date | None
    concluintes_exibiveis: list[ConcluinteExibivel] | None
    concluintes_nao_identificados: int | None
    houve_conclusao: bool | None


@dataclass(frozen=True)
class PainelDeDesafios:
    """Os desafios do proponente por situação (`RF-14-41`). Um desafio
    **recusado** nunca chegou a produzir efeito algum — não entra em
    nenhum dos três grupos do painel de efetividade."""

    propostos: list[DesafioDeEfetividade]
    publicados: list[DesafioDeEfetividade]
    concluidos: list[DesafioDeEfetividade]


@dataclass(frozen=True)
class AporteDeEfetividade:
    """Um aporte homologado com o que ele custeou (`RF-14-43`)."""

    id: uuid.UUID
    valor_em_moedas: Decimal
    data_do_aporte: date
    custeio_tipo: str
    custeio_descricao: str | None


@dataclass(frozen=True)
class MoedasDeEfetividade:
    total_em_moedas: Decimal
    aportes: list[AporteDeEfetividade]


@dataclass(frozen=True)
class CoberturaPorComunidade:
    comunidade_virtual_id: uuid.UUID
    comunidade_virtual_nome: str
    ciclo_rotulo: str
    objetivos: list[int]


@dataclass(frozen=True)
class CoberturaDeOds:
    por_comunidade: list[CoberturaPorComunidade]


@dataclass(frozen=True)
class PainelDeEfetividade:
    desafios: PainelDeDesafios
    moedas: MoedasDeEfetividade
    cobertura_de_ods: CoberturaDeOds


def _etiquetas_herdadas(sessao: Session, desafio: DesafioExtra) -> set[int]:
    """A da missão quando declarada, senão a da trilha — disponível mesmo
    sem conclusão (`RF-14-44`, design — decisão 8)."""
    if desafio.missao_id is not None:
        missao = sessao.get(Missao, desafio.missao_id)
        if missao is not None:
            return {etiqueta.objetivo for etiqueta in resolver_etiquetas_da_missao(sessao, missao)}
    return cobertura_por_trilha(sessao, desafio.trilha_id)


def _concluintes_exibiveis(
    sessao: Session, guerreiro_ids: list[uuid.UUID]
) -> tuple[list[ConcluinteExibivel], int]:
    """O portão da divulgação entra na consulta, não em pós-filtro
    (`RF-14-45`, `RF-14-46`, design — decisão 7)."""
    if not guerreiro_ids:
        return [], 0
    autorizados = (
        sessao.query(Persona.id, Persona.avatar, Nick.valor)
        .join(Nick, Nick.persona_id == Persona.id)
        .filter(Persona.id.in_(guerreiro_ids), condicao_de_autorizacao_vigente(sessao, Persona.id))
        .all()
    )
    exibiveis = [ConcluinteExibivel(avatar=avatar, nick=nick) for _, avatar, nick in autorizados]
    return exibiveis, len(guerreiro_ids) - len(exibiveis)


def _montar_desafio(sessao: Session, desafio: DesafioExtra, trilha: Trilha) -> DesafioDeEfetividade:
    etiquetas = sorted(_etiquetas_herdadas(sessao, desafio))

    if desafio.modalidade == Modalidade.direcionado:
        # Podado antes de qualquer consulta de concluinte: nem avatar, nem
        # nick, nem `VinculoJogador` do destinatário chegam a ser lidos
        # (`RF-14-47`, `RN-14-22`, design — decisão 6).
        houve_conclusao = (
            sessao.query(ConclusaoDeDesafioExtra).filter_by(desafio_id=desafio.id).first()
            is not None
        )
        return DesafioDeEfetividade(
            id=desafio.id,
            trilha_id=trilha.id,
            trilha_nome=trilha.nome,
            modalidade=desafio.modalidade.value,
            situacao=desafio.situacao.value,
            etiquetas_ods=etiquetas,
            quantidade_de_conclusoes=None,
            primeira_conclusao_em=None,
            ultima_conclusao_em=None,
            concluintes_exibiveis=None,
            concluintes_nao_identificados=None,
            houve_conclusao=houve_conclusao,
        )

    conclusoes = (
        sessao.query(ConclusaoDeDesafioExtra)
        .filter_by(desafio_id=desafio.id)
        .order_by(ConclusaoDeDesafioExtra.momento_do_fato)
        .all()
    )
    exibiveis, nao_identificados = _concluintes_exibiveis(
        sessao, [conclusao.guerreiro_id for conclusao in conclusoes]
    )
    return DesafioDeEfetividade(
        id=desafio.id,
        trilha_id=trilha.id,
        trilha_nome=trilha.nome,
        modalidade=desafio.modalidade.value,
        situacao=desafio.situacao.value,
        etiquetas_ods=etiquetas,
        quantidade_de_conclusoes=len(conclusoes),
        primeira_conclusao_em=conclusoes[0].momento_do_fato.date() if conclusoes else None,
        ultima_conclusao_em=conclusoes[-1].momento_do_fato.date() if conclusoes else None,
        concluintes_exibiveis=exibiveis,
        concluintes_nao_identificados=nao_identificados,
        houve_conclusao=None,
    )


def _montar_painel_de_desafios(
    sessao: Session, desafios: list[DesafioExtra], trilhas: dict[uuid.UUID, Trilha]
) -> tuple[PainelDeDesafios, list[DesafioExtra]]:
    propostos: list[DesafioDeEfetividade] = []
    publicados: list[DesafioDeEfetividade] = []
    concluidos: list[DesafioDeEfetividade] = []
    desafios_publicados: list[DesafioExtra] = []

    for desafio in desafios:
        if desafio.situacao == SituacaoDoDesafioExtra.recusado:
            continue
        trilha = trilhas[desafio.trilha_id]
        if desafio.situacao != SituacaoDoDesafioExtra.publicado:
            propostos.append(_montar_desafio(sessao, desafio, trilha))
            continue

        desafios_publicados.append(desafio)
        item = _montar_desafio(sessao, desafio, trilha)
        concluido = (
            bool(item.houve_conclusao)
            if desafio.modalidade == Modalidade.direcionado
            else bool(item.quantidade_de_conclusoes)
        )
        (concluidos if concluido else publicados).append(item)

    return (
        PainelDeDesafios(propostos=propostos, publicados=publicados, concluidos=concluidos),
        desafios_publicados,
    )


def _custeio_do_aporte(sessao: Session, aporte: Aporte) -> tuple[str, str | None]:
    """O que o aporte custeou: a necessidade ou a missão que a declaração
    de origem apontou, ou o desafio extra a que serve de lastro; sem
    nenhum dos dois, é aporte livre (`RF-14-43`, design — decisão 9)."""
    if aporte.aporte_declarado_id is not None:
        declaracao = sessao.get(AporteDeclarado, aporte.aporte_declarado_id)
        if declaracao is not None:
            if (
                declaracao.origem_da_escolha == OrigemDaEscolhaDoAporte.missao
                and declaracao.missao_do_apoiador_id is not None
            ):
                missao = sessao.get(MissaoDoApoiador, declaracao.missao_do_apoiador_id)
                if missao is not None:
                    return "missao", missao.titulo
            if (
                declaracao.origem_da_escolha == OrigemDaEscolhaDoAporte.necessidade
                and declaracao.tipo_de_recurso_id is not None
            ):
                tipo = sessao.get(TipoDeRecurso, declaracao.tipo_de_recurso_id)
                if tipo is not None:
                    return "necessidade", tipo.nome

    desafio_lastreado = sessao.query(DesafioExtra).filter_by(aporte_id=aporte.id).first()
    if desafio_lastreado is not None:
        trilha = sessao.get(Trilha, desafio_lastreado.trilha_id)
        return "desafio_extra", trilha.nome if trilha is not None else None

    return "livre", None


def _moedas_do_proponente(sessao: Session, proponente_id: uuid.UUID) -> MoedasDeEfetividade:
    """Só o homologado, nunca o pendente, e sempre em moedas (`RF-14-43`,
    `RN-14-07`, `RN-14-09`)."""
    aportes = (
        sessao.query(Aporte)
        .filter(Aporte.provedor_id == proponente_id, Aporte.admin_homologador_id.isnot(None))
        .order_by(Aporte.data_do_aporte.desc())
        .all()
    )
    itens: list[AporteDeEfetividade] = []
    total = Decimal("0")
    for aporte in aportes:
        custeio_tipo, custeio_descricao = _custeio_do_aporte(sessao, aporte)
        itens.append(
            AporteDeEfetividade(
                id=aporte.id,
                valor_em_moedas=aporte.valor_em_moedas,
                data_do_aporte=aporte.data_do_aporte,
                custeio_tipo=custeio_tipo,
                custeio_descricao=custeio_descricao,
            )
        )
        total += aporte.valor_em_moedas
    return MoedasDeEfetividade(total_em_moedas=total, aportes=itens)


def _cobertura_por_comunidade(
    sessao: Session, desafios_publicados: list[DesafioExtra], *, ciclo_rotulo: str
) -> list[CoberturaPorComunidade]:
    """Agregada por Comunidade Virtual de quem concluiu, na data do fato —
    a única leitura possível dado que a trilha não tem comunidade
    (`RF-14-44`, `RN-14-28`, design — decisão 8). O direcionado nunca entra
    aqui: agregar por comunidade exigiria o `VinculoJogador` do
    destinatário, que a decisão 6 proíbe consultar."""
    objetivos_por_comunidade: dict[uuid.UUID, set[int]] = {}

    for desafio in desafios_publicados:
        if desafio.modalidade == Modalidade.direcionado:
            continue
        etiquetas = _etiquetas_herdadas(sessao, desafio)
        if not etiquetas:
            continue
        conclusoes = sessao.query(ConclusaoDeDesafioExtra).filter_by(desafio_id=desafio.id).all()
        for conclusao in conclusoes:
            vinculo = resolver_vinculo_na_data(
                sessao, guerreiro_id=conclusao.guerreiro_id, data=conclusao.momento_do_fato
            )
            if vinculo is None:
                continue
            objetivos_por_comunidade.setdefault(vinculo.comunidade_virtual_id, set()).update(
                etiquetas
            )

    resultado: list[CoberturaPorComunidade] = []
    for comunidade_id, objetivos in objetivos_por_comunidade.items():
        comunidade = sessao.get(ComunidadeVirtual, comunidade_id)
        resultado.append(
            CoberturaPorComunidade(
                comunidade_virtual_id=comunidade_id,
                comunidade_virtual_nome=comunidade.nome if comunidade is not None else "",
                ciclo_rotulo=ciclo_rotulo,
                objetivos=sorted(objetivos),
            )
        )
    return resultado


def montar_painel_de_efetividade(
    sessao: Session, *, proponente: Persona, ciclo_rotulo: str
) -> PainelDeEfetividade:
    """A leitura vivo do painel: consulta sob demanda, nada materializado
    (`RF-14-40`, `RN-14-21`, design — decisão 5). `ciclo_rotulo` vem de
    `configuracao.ciclo_rotulo`, injetada na rota — a regra não lê
    configuração global, no mesmo padrão de `trilhas.rotas`."""
    desafios = listar_desafios_do_proponente(sessao, proponente_id=proponente.id)
    trilhas = {
        trilha.id: trilha
        for trilha in sessao.query(Trilha).filter(
            Trilha.id.in_({desafio.trilha_id for desafio in desafios})
        )
    }

    painel_de_desafios, desafios_publicados = _montar_painel_de_desafios(sessao, desafios, trilhas)

    return PainelDeEfetividade(
        desafios=painel_de_desafios,
        moedas=_moedas_do_proponente(sessao, proponente.id),
        cobertura_de_ods=CoberturaDeOds(
            por_comunidade=_cobertura_por_comunidade(
                sessao, desafios_publicados, ciclo_rotulo=ciclo_rotulo
            )
        ),
    )
