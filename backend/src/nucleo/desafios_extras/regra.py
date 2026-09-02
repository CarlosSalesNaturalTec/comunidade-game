import uuid
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy.orm import Session

from ..aportes.modelo import Aporte
from ..erros import (
    EdicaoDeDesafioExtraPublicadoRecusada,
    ErroDeValidacao,
    PermissaoNegada,
    SituacaoDoDesafioExtraIncompativel,
)
from ..livro_razao.regra import saldo_de
from ..personas.modelo import Papel, Persona
from ..pontos_de_apoio.modelo import PontoDeApoio
from ..recursos.modelo import NaturezaDoRecurso, TipoDeRecurso
from ..reservas.regra import liberar_reservas_do_desafio, reservar_recompensa_do_desafio
from ..tempo import agora
from ..trilhas.modelo import Missao, SituacaoDaTrilha, Trilha
from .modelo import (
    ConclusaoDeDesafioExtra,
    CusteioDoDesafioExtra,
    DesafioExtra,
    FormatoDoDesafioExtra,
    Modalidade,
    SituacaoDoDesafioExtra,
)

TETO_DE_PONTOS_EXTRAS = 10


def propor_desafio_extra(
    sessao: Session,
    *,
    operador: Persona,
    trilha: Trilha | None,
    missao: Missao | None,
    modalidade: Modalidade | None,
    nick_do_destinatario: str | None,
    justificativa_do_vinculo: str | None,
    tipo_de_recurso: TipoDeRecurso | None,
    ponto_de_apoio: PontoDeApoio | None,
    quantidade_disponivel: int | None,
    criterio_de_atribuicao: str | None,
    pontos_extras: int | None,
    formato: FormatoDoDesafioExtra | None,
    custeio: CusteioDoDesafioExtra | None,
    aporte: Aporte | None,
    vigencia_inicio: date | None,
    vigencia_fim: date | None,
) -> DesafioExtra:
    """O Apoiador propõe o desafio sobre uma trilha em andamento — trilha
    **publicada**, o mesmo estado que `trilhas.regra.inscrever_na_trilha`
    exige do Guerreiro(a) (`RF-14-29`, `RF-14-30`). Não há teto de propostas
    simultâneas (`RN-14-15`). Nasce sempre em `em_validacao_do_mestre`,
    isolada da pontuação regular (`RF-14-35`, `RN-14-13`, `RN-14-19`)."""
    if operador.papel != Papel.apoiador:
        raise PermissaoNegada(mensagem="Só o Apoiador propõe desafio extra.")
    if trilha is None:
        raise ErroDeValidacao(mensagem="Desafio extra exige uma trilha.", campo="trilha_id")
    if trilha.situacao != SituacaoDaTrilha.publicada:
        raise ErroDeValidacao(
            mensagem="A trilha precisa estar em andamento (publicada).", campo="trilha_id"
        )
    if missao is not None and missao.trilha_id != trilha.id:
        raise ErroDeValidacao(
            mensagem="A missão declarada não pertence à trilha declarada.", campo="missao_id"
        )
    if modalidade is None:
        raise ErroDeValidacao(mensagem="Desafio extra exige a modalidade.", campo="modalidade")
    if modalidade == Modalidade.direcionado:
        if not nick_do_destinatario or not nick_do_destinatario.strip():
            raise ErroDeValidacao(
                mensagem="O direcionado exige o nick do destinatário.",
                campo="nick_do_destinatario",
            )
        if not justificativa_do_vinculo or not justificativa_do_vinculo.strip():
            raise ErroDeValidacao(
                mensagem="O direcionado exige a justificativa do vínculo.",
                campo="justificativa_do_vinculo",
            )
    else:
        nick_do_destinatario = None
        justificativa_do_vinculo = None
    if not criterio_de_atribuicao or not criterio_de_atribuicao.strip():
        raise ErroDeValidacao(
            mensagem="Desafio extra exige o critério de atribuição.",
            campo="criterio_de_atribuicao",
        )
    if pontos_extras is None or pontos_extras < 1:
        raise ErroDeValidacao(
            mensagem="Desafio extra exige os pontos extras.", campo="pontos_extras"
        )
    if pontos_extras > TETO_DE_PONTOS_EXTRAS:
        raise ErroDeValidacao(
            mensagem=f"Pontos extras acima do teto de {TETO_DE_PONTOS_EXTRAS}.",
            campo="pontos_extras",
        )
    if formato is None:
        raise ErroDeValidacao(mensagem="Desafio extra exige o formato.", campo="formato")
    if tipo_de_recurso is None:
        raise ErroDeValidacao(
            mensagem="Desafio extra exige o tipo de recurso da recompensa.",
            campo="tipo_de_recurso_id",
        )
    if ponto_de_apoio is None:
        raise ErroDeValidacao(
            mensagem="Desafio extra exige o ponto de apoio da recompensa.",
            campo="ponto_de_apoio_id",
        )
    if quantidade_disponivel is None or quantidade_disponivel < 1:
        raise ErroDeValidacao(
            mensagem="Desafio extra exige a quantidade disponível.",
            campo="quantidade_disponivel",
        )
    if vigencia_inicio is None or vigencia_fim is None:
        raise ErroDeValidacao(
            mensagem="Desafio extra exige o período de vigência.", campo="vigencia_inicio"
        )
    if vigencia_fim < vigencia_inicio:
        raise ErroDeValidacao(
            mensagem="A vigência não pode terminar antes de começar.", campo="vigencia_fim"
        )
    if custeio is None:
        raise ErroDeValidacao(mensagem="Desafio extra exige o custeio.", campo="custeio")
    if custeio == CusteioDoDesafioExtra.aporte_do_proponente:
        if aporte is None:
            raise ErroDeValidacao(
                mensagem="Custeio por aporte exige um aporte existente.", campo="aporte_id"
            )
        if aporte.provedor_id != operador.id:
            raise ErroDeValidacao(
                mensagem="O aporte declarado não é deste proponente.", campo="aporte_id"
            )
        if aporte.tipo_de_recurso_id != tipo_de_recurso.id:
            raise ErroDeValidacao(
                mensagem="O aporte declarado não é do tipo de recurso da recompensa.",
                campo="aporte_id",
            )
    else:
        aporte = None

    desafio = DesafioExtra(
        trilha_id=trilha.id,
        missao_id=missao.id if missao is not None else None,
        modalidade=modalidade,
        nick_do_destinatario=nick_do_destinatario,
        justificativa_do_vinculo=justificativa_do_vinculo,
        tipo_de_recurso_id=tipo_de_recurso.id,
        ponto_de_apoio_id=ponto_de_apoio.id,
        quantidade_disponivel=quantidade_disponivel,
        criterio_de_atribuicao=criterio_de_atribuicao,
        pontos_extras=pontos_extras,
        formato=formato,
        custeio=custeio,
        aporte_id=aporte.id if aporte is not None else None,
        vigencia_inicio=vigencia_inicio,
        vigencia_fim=vigencia_fim,
        situacao=SituacaoDoDesafioExtra.em_validacao_do_mestre,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(desafio)
    sessao.flush()
    return desafio


def lastro_provido(sessao: Session, *, desafio: DesafioExtra) -> bool:
    """Lido na hora a partir do custeio declarado — aporte homologado do
    proponente ou saldo de recurso suficiente no ponto de apoio, nunca um
    espelho gravado (`RF-14-34`, `RF-07-15`, `RN-14-14`, design —
    Decisions)."""
    if desafio.custeio == CusteioDoDesafioExtra.aporte_do_proponente:
        if desafio.aporte_id is None:
            return False
        aporte = sessao.get(Aporte, desafio.aporte_id)
        return aporte is not None and aporte.admin_homologador_id is not None

    disponivel = saldo_de(
        sessao,
        tipo_de_recurso_id=desafio.tipo_de_recurso_id,
        ponto_de_apoio_id=desafio.ponto_de_apoio_id,
    )
    return disponivel >= Decimal(desafio.quantidade_disponivel)


def motivo_de_lastro_faltante(sessao: Session, *, desafio: DesafioExtra) -> str | None:
    """A leitura do proponente informa o que falta prover — nunca só que
    falta (`RF-14-34`, PRD-14 §12)."""
    if lastro_provido(sessao, desafio=desafio):
        return None
    if desafio.custeio == CusteioDoDesafioExtra.aporte_do_proponente:
        return "Falta um aporte homologado deste proponente para o tipo de recurso declarado."
    return "Falta saldo suficiente do tipo de recurso declarado no ponto de apoio."


def conferir_publicacao_com_lastro(sessao: Session, *, desafio: DesafioExtra) -> None:
    """A guarda que a publicação (fatia 15 do PRD-02) chama antes de gravar
    `publicado`: sem lastro provido, a publicação é recusada (`RF-14-34`,
    `RF-07-15`, `RN-14-14`)."""
    if not lastro_provido(sessao, desafio=desafio):
        raise ErroDeValidacao(
            mensagem=motivo_de_lastro_faltante(sessao, desafio=desafio), campo="custeio"
        )


def conferir_editavel(desafio: DesafioExtra) -> None:
    """Desafio publicado não se edita: a correção é proposta nova, e esta
    fica registrada com o desfecho que teve (`RF-14-38`)."""
    if desafio.situacao == SituacaoDoDesafioExtra.publicado:
        raise EdicaoDeDesafioExtraPublicadoRecusada()


def listar_desafios_do_proponente(
    sessao: Session, *, proponente_id: uuid.UUID
) -> list[DesafioExtra]:
    """Só os do próprio proponente, da mais recente para a mais antiga
    (`RF-14-35` a `RF-14-39`)."""
    return (
        sessao.query(DesafioExtra)
        .filter_by(autor_id=proponente_id)
        .order_by(DesafioExtra.registrado_em.desc())
        .all()
    )


def registrar_conclusao_de_desafio_extra(
    sessao: Session,
    *,
    desafio: DesafioExtra | None,
    guerreiro_id: uuid.UUID,
    momento_do_fato: datetime,
    recompensa_entregue: bool,
    pontos_extras_creditados: int,
) -> ConclusaoDeDesafioExtra:
    """A entidade nasce sem rota nesta fatia — o ato de chamar esta função é
    do PRD-09, ainda sem fatia; aqui só as guardas (design — decisão 2).
    Recusa desafio não publicado, desafio encerrado — a reserva já voltou
    à disponível e não há o que entregar (`RF-07-40`, design — decisão 8)
    — e segunda conclusão do mesmo Guerreiro(a) para o mesmo desafio; a
    `UniqueConstraint` do modelo sustenta a segunda guarda também fora
    desta função (`RF-14-42`)."""
    if (
        desafio is None
        or desafio.situacao != SituacaoDoDesafioExtra.publicado
        or desafio.encerrado_em is not None
    ):
        raise ErroDeValidacao(
            mensagem="Só desafio extra publicado e não encerrado recebe conclusão.",
            campo="desafio_id",
        )
    ja_concluiu = (
        sessao.query(ConclusaoDeDesafioExtra)
        .filter_by(desafio_id=desafio.id, guerreiro_id=guerreiro_id)
        .first()
    )
    if ja_concluiu is not None:
        raise ErroDeValidacao(
            mensagem="Este Guerreiro(a) já concluiu este desafio.", campo="guerreiro_id"
        )

    conclusao = ConclusaoDeDesafioExtra(
        desafio_id=desafio.id,
        guerreiro_id=guerreiro_id,
        momento_do_fato=momento_do_fato,
        recompensa_entregue=recompensa_entregue,
        pontos_extras_creditados=pontos_extras_creditados,
    )
    sessao.add(conclusao)
    sessao.flush()
    return conclusao


def quantidade_restante(sessao: Session, *, desafio: DesafioExtra) -> int:
    """A disponível menos as conclusões com recompensa entregue, nunca
    negativa — derivada na leitura, sem coluna de contador (`RF-14-37`,
    `RF-14-42`, design — decisão 3)."""
    entregues = (
        sessao.query(ConclusaoDeDesafioExtra)
        .filter_by(desafio_id=desafio.id, recompensa_entregue=True)
        .count()
    )
    return max(desafio.quantidade_disponivel - entregues, 0)


def listar_desafios_em_aprovacao_do_admin(sessao: Session) -> list[DesafioExtra]:
    """A fila do Admin: só os já validados pelo Mestre da trilha, nunca os
    em validação, publicados ou recusados — da mais antiga para a mais
    recente (`RF-02-27`, `RN-02-10`)."""
    return (
        sessao.query(DesafioExtra)
        .filter_by(situacao=SituacaoDoDesafioExtra.em_aprovacao_do_admin)
        .order_by(DesafioExtra.registrado_em.asc())
        .all()
    )


def listar_desafios_publicados(sessao: Session) -> list[DesafioExtra]:
    """Os desafios publicados, para a tela do encerramento — a quantidade
    restante e a vigência são lidas de cada um pela própria saída
    (`RF-02-106`)."""
    return (
        sessao.query(DesafioExtra)
        .filter_by(situacao=SituacaoDoDesafioExtra.publicado)
        .order_by(DesafioExtra.registrado_em.asc())
        .all()
    )


def aprovar_desafio_extra(
    sessao: Session, desafio: DesafioExtra, *, admin: Persona
) -> DesafioExtra:
    """A ordem das guardas é situação → natureza → lastro → disponível,
    para que o erro devolvido seja o que o Admin precisa resolver primeiro
    (`RF-02-28`, `RN-02-10`, `RN-02-11`, `RF-07-15`, design — decisão 4).
    A reserva da recompensa acontece no mesmo ato que publica, sob o
    bloqueio que o agendamento concorrente já usa (`RF-07-39`, design —
    decisão 3)."""
    if desafio.situacao != SituacaoDoDesafioExtra.em_aprovacao_do_admin:
        raise SituacaoDoDesafioExtraIncompativel(
            mensagem="Só desafio já validado pelo Mestre, ainda sem desfecho, é aprovável."
        )
    tipo = sessao.get(TipoDeRecurso, desafio.tipo_de_recurso_id)
    if tipo.natureza == NaturezaDoRecurso.duravel:
        raise ErroDeValidacao(
            mensagem=(
                "Tipo de recurso de natureza durável não é reservável: o saldo é "
                "patrimônio, não insumo de atividade."
            ),
            campo="tipo_de_recurso_id",
        )
    conferir_publicacao_com_lastro(sessao, desafio=desafio)
    reservar_recompensa_do_desafio(sessao, desafio=desafio, operador=admin)

    desafio.situacao = SituacaoDoDesafioExtra.publicado
    desafio.admin_aprovador_id = admin.id
    sessao.flush()
    return desafio


def recusar_desafio_extra(
    sessao: Session, desafio: DesafioExtra, *, admin: Persona, motivo: str | None
) -> DesafioExtra:
    """Exige o motivo, que a leitura do proponente já devolve, e não grava
    reserva alguma (`RF-02-28`, `RF-14-36`, `RN-14-13`)."""
    if desafio.situacao != SituacaoDoDesafioExtra.em_aprovacao_do_admin:
        raise SituacaoDoDesafioExtraIncompativel(
            mensagem="Só desafio já validado pelo Mestre, ainda sem desfecho, é recusável."
        )
    if not motivo or not motivo.strip():
        raise ErroDeValidacao(mensagem="A recusa exige o motivo.", campo="motivo")

    desafio.situacao = SituacaoDoDesafioExtra.recusado
    desafio.motivo_da_recusa = motivo
    sessao.flush()
    return desafio


def encerrar_desafio_extra(
    sessao: Session, desafio: DesafioExtra, *, admin: Persona
) -> DesafioExtra:
    """Só o desafio **publicado** encerra, uma única vez: leva a
    **liberada** toda reserva ainda **reservada** daquele desafio,
    devolvendo a quantidade à disponível, e grava quem encerrou e quando —
    nunca por decurso da vigência (`RF-02-106`, `RF-07-40`, design —
    decisão 1)."""
    if desafio.situacao != SituacaoDoDesafioExtra.publicado:
        raise SituacaoDoDesafioExtraIncompativel(mensagem="Só desafio publicado é encerrável.")
    if desafio.encerrado_em is not None:
        raise SituacaoDoDesafioExtraIncompativel(mensagem="Este desafio já foi encerrado.")

    liberar_reservas_do_desafio(sessao, desafio=desafio)
    desafio.admin_encerrador_id = admin.id
    desafio.encerrado_em = agora()
    sessao.flush()
    return desafio
