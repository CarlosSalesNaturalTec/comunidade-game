from decimal import Decimal

from sqlalchemy import func
from sqlalchemy.orm import Session

from ..comunidades.modelo import VinculoJogador
from ..erros import ErroDeValidacao, PermissaoNegada
from ..livro_razao.regra import lancar_debito, saldo_de
from ..personas.modelo import Papel, Persona
from ..pontos_de_apoio.modelo import PontoDeApoio
from ..pontuacao.regra import missoes_concluidas_pelo_guerreiro
from ..recursos.modelo import NaturezaDoRecurso, TipoDeRecurso
from ..recursos.regra import consultar_valor_de_referencia
from ..tempo import agora
from ..trilhas.modelo import Missao, Trilha
from ..trilhas.regra import conferir_posse_da_trilha
from .modelo import EntregaDeRecompensa, RecompensaDeMarco


def declarar_recompensa_de_marco(
    sessao: Session,
    *,
    operador: Persona,
    trilha: Trilha | None,
    missao: Missao | None,
    tipo: TipoDeRecurso | None,
    quantidade: Decimal | None,
) -> RecompensaDeMarco:
    """Só o Mestre autor da trilha declara, pela mesma conferência de posse
    do restante dela (`RF-09-71`, design — Decisions). O marco precisa ser
    uma missão **desta** trilha: as demais espécies do documento 02 §8.1
    ainda não são verificáveis pelo núcleo (`RN-09-26`, `RN-09-39`). A
    declaração não recebe preço nem contrapartida — não há campo para isso
    aqui; quem tenta declará-los é recusado pela própria rota."""
    if trilha is None:
        raise ErroDeValidacao(mensagem="Recompensa de marco exige uma trilha.", campo="trilha_id")
    conferir_posse_da_trilha(trilha, operador)

    if missao is None or missao.trilha_id != trilha.id:
        raise ErroDeValidacao(
            mensagem="O marco precisa ser uma missão desta trilha; só a missão é aceita "
            "como marco.",
            campo="missao_id",
        )
    if tipo is None:
        raise ErroDeValidacao(
            mensagem="Recompensa de marco exige um tipo de recurso existente.",
            campo="tipo_de_recurso_id",
        )
    if quantidade is None or quantidade <= 0:
        raise ErroDeValidacao(
            mensagem="Recompensa de marco exige quantidade positiva.", campo="quantidade"
        )

    recompensa = RecompensaDeMarco(
        trilha_id=trilha.id,
        missao_id=missao.id,
        tipo_de_recurso_id=tipo.id,
        quantidade=quantidade,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(recompensa)
    sessao.flush()
    return recompensa


def listar_recompensas_de_marco(sessao: Session, *, trilha_id) -> list[RecompensaDeMarco]:
    """As recompensas de marco declaradas numa trilha, para a gestão
    (`RF-09-71`)."""
    return (
        sessao.query(RecompensaDeMarco)
        .filter_by(trilha_id=trilha_id)
        .order_by(RecompensaDeMarco.registrado_em.desc())
        .all()
    )


def _bloquear_recompensa(sessao: Session, *, recompensa: RecompensaDeMarco) -> None:
    """`SELECT ... FOR UPDATE` da linha da recompensa, para que duas
    entregas concorrentes da última vaga não passem as duas pela
    verificação de quantidade (mesmo padrão de
    `catalogo_avulso.regra._bloquear_item`)."""
    sessao.query(RecompensaDeMarco.id).filter_by(id=recompensa.id).with_for_update().all()
    sessao.refresh(recompensa)


def _valorar_debito(sessao: Session, *, tipo: TipoDeRecurso, quantidade: Decimal) -> Decimal:
    """A baixa da entrega é valorada pela vigência do valor de referência no
    dia da entrega, no mesmo mecanismo de `trocas.regra._valorar_debito`
    (design — Decisions)."""
    referencia = consultar_valor_de_referencia(sessao, tipo=tipo, data=agora().date())
    if referencia is None:
        raise ErroDeValidacao(
            mensagem="Nenhuma vigência do valor de referência cobre a data da entrega.",
            campo="ponto_de_apoio_id",
        )
    return (quantidade * referencia.valor_em_moedas).quantize(Decimal("0.01"))


def _validar_entrega(
    sessao: Session,
    *,
    recompensa: RecompensaDeMarco,
    tipo: TipoDeRecurso,
    operador: Persona,
    guerreiro: Persona,
    ponto_de_apoio: PontoDeApoio,
) -> None:
    """As cinco recusas do delta, na ordem dele — durável, lastro, quantidade
    esgotada, comunidade, marco alcançado —, todas antes de qualquer escrita
    (`RF-07-13`, `RN-07-07`, `RN-09-26`, invariante 9)."""
    if tipo.natureza == NaturezaDoRecurso.duravel:
        raise ErroDeValidacao(
            mensagem="Recurso de natureza durável é patrimônio e nunca lastreia recompensa.",
            campo="recompensa_de_marco_id",
        )

    saldo_disponivel = saldo_de(
        sessao, tipo_de_recurso_id=tipo.id, ponto_de_apoio_id=ponto_de_apoio.id
    )
    if saldo_disponivel < recompensa.quantidade:
        raise ErroDeValidacao(
            mensagem="Lastro insuficiente no ponto de apoio informado para esta entrega.",
            campo="ponto_de_apoio_id",
        )

    ja_entregues = (
        sessao.query(func.count(EntregaDeRecompensa.id))
        .filter_by(recompensa_de_marco_id=recompensa.id)
        .scalar()
    )
    if Decimal(ja_entregues) >= recompensa.quantidade:
        raise ErroDeValidacao(
            mensagem="A quantidade declarada nesta recompensa já foi esgotada pelas "
            "entregas anteriores.",
            campo="recompensa_de_marco_id",
        )

    vinculo_mestre: VinculoJogador | None = operador.vinculo_vigente
    vinculo_guerreiro: VinculoJogador | None = guerreiro.vinculo_vigente
    if (
        vinculo_mestre is None
        or vinculo_guerreiro is None
        or vinculo_mestre.comunidade_virtual_id != vinculo_guerreiro.comunidade_virtual_id
    ):
        raise ErroDeValidacao(
            mensagem="Só o Mestre vinculado à comunidade do Guerreiro(a) confirma a entrega.",
            campo="guerreiro_id",
        )

    concluidas = missoes_concluidas_pelo_guerreiro(
        sessao, guerreiro_id=guerreiro.id, trilha_id=recompensa.trilha_id
    )
    if recompensa.missao_id not in concluidas:
        raise ErroDeValidacao(
            mensagem="Este Guerreiro(a) ainda não alcançou o marco declarado.",
            campo="guerreiro_id",
        )


def registrar_entrega(
    sessao: Session,
    *,
    operador: Persona,
    recompensa: RecompensaDeMarco | None,
    guerreiro: Persona | None,
    ponto_de_apoio: PontoDeApoio | None,
) -> EntregaDeRecompensa:
    """Restrita ao Mestre — o Admin nunca confirma a entrega (`RF-02-50`,
    `RF-02-51`, `RN-02-17`). Grava a entrega e emite o débito numa operação
    só, sem aula e sem tocar ponto regular nem extra do Guerreiro(a)
    (`RF-07-13`, `RN-07-08`, `RN-07-36`, `RN-07-15`)."""
    if operador.papel != Papel.mestre:
        raise PermissaoNegada(mensagem="Só o Mestre confirma a entrega da recompensa de marco.")
    if recompensa is None:
        raise ErroDeValidacao(
            mensagem="Entrega exige uma recompensa de marco existente.",
            campo="recompensa_de_marco_id",
        )
    if guerreiro is None:
        raise ErroDeValidacao(mensagem="Entrega exige o Guerreiro(a).", campo="guerreiro_id")
    if ponto_de_apoio is None:
        raise ErroDeValidacao(
            mensagem="Entrega exige o ponto de apoio de onde o recurso sai.",
            campo="ponto_de_apoio_id",
        )

    tipo = sessao.get(TipoDeRecurso, recompensa.tipo_de_recurso_id)

    _bloquear_recompensa(sessao, recompensa=recompensa)
    _validar_entrega(
        sessao,
        recompensa=recompensa,
        tipo=tipo,
        operador=operador,
        guerreiro=guerreiro,
        ponto_de_apoio=ponto_de_apoio,
    )

    valor_em_moedas = _valorar_debito(sessao, tipo=tipo, quantidade=recompensa.quantidade)
    lancamento = lancar_debito(
        sessao,
        tipo_de_recurso_id=tipo.id,
        ponto_de_apoio_id=ponto_de_apoio.id,
        quantidade=recompensa.quantidade,
        valor_em_moedas=valor_em_moedas,
        operador=operador,
        aula_id=None,
    )

    entrega = EntregaDeRecompensa(
        recompensa_de_marco_id=recompensa.id,
        guerreiro_id=guerreiro.id,
        ponto_de_apoio_id=ponto_de_apoio.id,
        lancamento_id=lancamento.id,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(entrega)
    sessao.flush()
    return entrega


def listar_entregas(sessao: Session, *, operador: Persona) -> list[EntregaDeRecompensa]:
    """Guerreiro(a) lê só as próprias; Mestre e Admin, as da comunidade a
    que estão vinculados — sem moedas nem reais na saída, o custo real fica
    no livro-razão (`RF-07-13`, `RN-07-05`)."""
    if operador.papel == Papel.guerreiro:
        return (
            sessao.query(EntregaDeRecompensa)
            .filter_by(guerreiro_id=operador.id)
            .order_by(EntregaDeRecompensa.registrado_em.desc())
            .all()
        )
    if operador.papel in (Papel.mestre, Papel.admin):
        vinculo: VinculoJogador | None = operador.vinculo_vigente
        if vinculo is None:
            return []
        return (
            sessao.query(EntregaDeRecompensa)
            .join(
                VinculoJogador,
                (VinculoJogador.guerreiro_id == EntregaDeRecompensa.guerreiro_id)
                & (VinculoJogador.data_fim.is_(None)),
            )
            .filter(VinculoJogador.comunidade_virtual_id == vinculo.comunidade_virtual_id)
            .order_by(EntregaDeRecompensa.registrado_em.desc())
            .all()
        )
    raise PermissaoNegada(mensagem="Persona sem histórico de entregas a consultar.")
