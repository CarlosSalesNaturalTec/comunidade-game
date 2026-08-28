import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import case, func, tuple_
from sqlalchemy.orm import Session

from ..erros import ErroDeValidacao, PermissaoNegada
from ..paginacao import codificar_cursor, decodificar_cursor
from ..personas.modelo import Papel, Persona
from ..pontos_de_apoio.modelo import PontoDeApoio
from ..recursos.modelo import TipoDeRecurso
from ..recursos.regra import consultar_valor_de_referencia
from ..tempo import agora
from .modelo import DestinacaoDoAporte, Lancamento, NaturezaDoLancamento


def lancar_credito(
    sessao: Session,
    *,
    tipo_de_recurso_id,
    ponto_de_apoio_id,
    quantidade: Decimal,
    valor_em_moedas: Decimal,
    operador: Persona,
    destinacao: DestinacaoDoAporte = DestinacaoDoAporte.lastro,
) -> Lancamento:
    """O lançamento de crédito que todo aporte homologado gera, um por
    aporte, no ponto de apoio declarado (`RF-07-04`, `RF-07-07`, `RN-07-36`,
    design — Decisions 9). `destinacao` herda a do aporte que o gerou; o
    crédito de destinação ressarcimento fica fora do saldo derivado
    (`RF-07-23`, `RN-07-38`, design — Decisions 2)."""
    lancamento = Lancamento(
        natureza=NaturezaDoLancamento.credito,
        tipo_de_recurso_id=tipo_de_recurso_id,
        ponto_de_apoio_id=ponto_de_apoio_id,
        quantidade=quantidade,
        valor_em_moedas=valor_em_moedas,
        destinacao=destinacao,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(lancamento)
    sessao.flush()
    return lancamento


def lancar_debito(
    sessao: Session,
    *,
    tipo_de_recurso_id,
    ponto_de_apoio_id,
    quantidade: Decimal,
    valor_em_moedas: Decimal,
    operador: Persona,
    aula_id=None,
) -> Lancamento:
    """O lançamento de débito que a baixa de uma reserva gera, um por
    reserva consumida, no ponto de apoio da aula que a consumiu (`RF-07-09`,
    `RN-07-36`, design — Decisions 7). `aula_id` é anulável porque fatias
    futuras trarão débito sem aula — a baixa da troca do catálogo avulso e
    a de recompensa entregue (`RF-07-16`, design — Decisions 3)."""
    lancamento = Lancamento(
        natureza=NaturezaDoLancamento.debito,
        tipo_de_recurso_id=tipo_de_recurso_id,
        ponto_de_apoio_id=ponto_de_apoio_id,
        quantidade=quantidade,
        valor_em_moedas=valor_em_moedas,
        aula_id=aula_id,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(lancamento)
    sessao.flush()
    return lancamento


def lancar_ajuste(
    sessao: Session,
    *,
    operador: Persona,
    lancamento_original: Lancamento | None,
    quantidade: Decimal | None,
    valor_em_moedas: Decimal | None,
    motivo: str | None,
) -> Lancamento:
    """Só Admin corrige lançamento, e só por lançamento novo que referencia
    o original sem alterá-lo (`RF-07-19`, `RN-07-15`). Herda tipo de
    recurso, ponto de apoio e **destinação** do original, para que a
    correção entre na mesma conta de saldo (design — Decisions 9). O
    ajuste que reverte um ressarcimento grava **quantidade zero**: reverte
    moedas sem desfazer um consumo que já aconteceu (`RF-07-25`, design —
    Decisions 1)."""
    if operador.papel != Papel.admin:
        raise PermissaoNegada(mensagem="Só o Admin lança ajuste.")
    if lancamento_original is None:
        raise ErroDeValidacao(
            mensagem="Lançamento original não encontrado.", campo="lancamento_original_id"
        )
    if not motivo or not motivo.strip():
        raise ErroDeValidacao(mensagem="Ajuste exige motivo.", campo="motivo")
    if quantidade is None:
        raise ErroDeValidacao(mensagem="Ajuste exige quantidade.", campo="quantidade")
    if valor_em_moedas is None:
        raise ErroDeValidacao(mensagem="Ajuste exige valor em moedas.", campo="valor_em_moedas")

    ajuste = Lancamento(
        natureza=NaturezaDoLancamento.ajuste,
        tipo_de_recurso_id=lancamento_original.tipo_de_recurso_id,
        ponto_de_apoio_id=lancamento_original.ponto_de_apoio_id,
        quantidade=quantidade,
        valor_em_moedas=valor_em_moedas,
        destinacao=lancamento_original.destinacao,
        lancamento_original_id=lancamento_original.id,
        motivo_do_ajuste=motivo,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(ajuste)
    sessao.flush()
    return ajuste


def transferir_saldo(
    sessao: Session,
    *,
    operador: Persona,
    tipo_de_recurso: TipoDeRecurso | None,
    ponto_de_apoio_origem: PontoDeApoio | None,
    ponto_de_apoio_destino: PontoDeApoio | None,
    quantidade: Decimal | None,
    motivo: str | None,
) -> tuple[Lancamento, Lancamento]:
    """Só Admin transfere, e move recurso que existe e está certo — por isso
    não é `ajuste`, que corrige erro (`RF-07-19`, `RN-07-15`, design —
    Decisions 1). Grava um débito na origem e um crédito no destino, na
    mesma operação, com o mesmo tipo de recurso, quantidade, moedas, motivo,
    autoria e momento; os dois `id` são gerados antes da inserção para que
    cada lançamento já nasça referenciando o outro (`lancamento_relacionado_id`
    é `DEFERRABLE`, design — Decisions 1). `valor_em_moedas` é derivado da
    vigência de hoje do valor de referência do tipo, pela mesma régua de
    `aportes/regra.py`: a tela de transferência não pede o valor à mão."""
    if operador.papel != Papel.admin:
        raise PermissaoNegada(mensagem="Só o Admin transfere saldo entre pontos de apoio.")
    if ponto_de_apoio_origem is None:
        raise ErroDeValidacao(
            mensagem="Transferência exige o ponto de apoio de origem.",
            campo="ponto_de_apoio_origem_id",
        )
    if ponto_de_apoio_destino is None:
        raise ErroDeValidacao(
            mensagem="Transferência exige o ponto de apoio de destino.",
            campo="ponto_de_apoio_destino_id",
        )
    if ponto_de_apoio_origem.id == ponto_de_apoio_destino.id:
        raise ErroDeValidacao(
            mensagem="Origem e destino da transferência não podem ser o mesmo ponto de apoio.",
            campo="ponto_de_apoio_destino_id",
        )
    if tipo_de_recurso is None:
        raise ErroDeValidacao(
            mensagem="Transferência exige o tipo de recurso.", campo="tipo_de_recurso_id"
        )
    if quantidade is None or quantidade <= 0:
        raise ErroDeValidacao(
            mensagem="Transferência exige quantidade maior que zero.", campo="quantidade"
        )
    if not motivo or not motivo.strip():
        raise ErroDeValidacao(mensagem="Transferência exige motivo.", campo="motivo")
    if not ponto_de_apoio_destino.ativo:
        raise ErroDeValidacao(
            mensagem="O ponto de apoio de destino está inativo.",
            campo="ponto_de_apoio_destino_id",
        )

    saldo_na_origem = saldo_de(
        sessao, tipo_de_recurso_id=tipo_de_recurso.id, ponto_de_apoio_id=ponto_de_apoio_origem.id
    )
    if quantidade > saldo_na_origem:
        raise ErroDeValidacao(
            mensagem=f"Saldo insuficiente na origem: disponível {saldo_na_origem}.",
            campo="quantidade",
        )

    momento = agora()
    referencia = consultar_valor_de_referencia(sessao, tipo=tipo_de_recurso, data=momento.date())
    if referencia is None:
        raise ErroDeValidacao(
            mensagem="Nenhuma vigência do valor de referência cobre a data de hoje.",
            campo="tipo_de_recurso_id",
        )
    valor_em_moedas = (quantidade * referencia.valor_em_moedas).quantize(Decimal("0.01"))

    id_do_debito = uuid.uuid4()
    id_do_credito = uuid.uuid4()

    debito = Lancamento(
        id=id_do_debito,
        natureza=NaturezaDoLancamento.debito,
        tipo_de_recurso_id=tipo_de_recurso.id,
        ponto_de_apoio_id=ponto_de_apoio_origem.id,
        quantidade=quantidade,
        valor_em_moedas=valor_em_moedas,
        lancamento_relacionado_id=id_do_credito,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
        registrado_em=momento,
    )
    credito = Lancamento(
        id=id_do_credito,
        natureza=NaturezaDoLancamento.credito,
        tipo_de_recurso_id=tipo_de_recurso.id,
        ponto_de_apoio_id=ponto_de_apoio_destino.id,
        quantidade=quantidade,
        valor_em_moedas=valor_em_moedas,
        lancamento_relacionado_id=id_do_debito,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
        registrado_em=momento,
    )
    sessao.add(debito)
    sessao.add(credito)
    sessao.flush()
    return debito, credito


def saldos_por_ponto_de_apoio(
    sessao: Session, *, ponto_de_apoio_id
) -> list[tuple[uuid.UUID, Decimal]]:
    """Todo tipo de recurso com saldo não nulo neste ponto de apoio, cada um
    recontado por `saldo_de` — usado pela desativação, que bloqueia enquanto
    restar saldo, e pela tela de transferência, que mostra o disponível
    antes de confirmar (`RF-07-47`, `RF-07-19`)."""
    tipos_ids = (
        sessao.query(Lancamento.tipo_de_recurso_id)
        .filter(Lancamento.ponto_de_apoio_id == ponto_de_apoio_id)
        .distinct()
        .all()
    )
    resultado = []
    for (tipo_de_recurso_id,) in tipos_ids:
        saldo = saldo_de(
            sessao, tipo_de_recurso_id=tipo_de_recurso_id, ponto_de_apoio_id=ponto_de_apoio_id
        )
        if saldo != 0:
            resultado.append((tipo_de_recurso_id, saldo))
    return resultado


def listar_lancamentos(
    sessao: Session,
    *,
    operador: Persona,
    ponto_de_apoio_id: uuid.UUID | None,
    tipo_de_recurso_id: uuid.UUID | None,
    periodo_inicio: datetime | None,
    periodo_fim: datetime | None,
    cursor: str | None,
    tamanho: int,
) -> tuple[list[Lancamento], str | None]:
    """Leitura de Admin do extrato de um ponto de apoio, com o filtro
    obrigatório que evita misturar o livro-razão de espaços diferentes; é o
    que dá ao ajuste do `RF-02-40` como alcançar o lançamento a corrigir
    (`RF-07-19`, `RF-01-18`, `RF-01-28`)."""
    if operador.papel != Papel.admin:
        raise PermissaoNegada(mensagem="Só o Admin lê os lançamentos de um ponto de apoio.")
    if ponto_de_apoio_id is None:
        raise ErroDeValidacao(
            mensagem="Esta consulta exige o filtro de ponto de apoio.",
            campo="ponto_de_apoio",
        )

    consulta = sessao.query(Lancamento).filter(Lancamento.ponto_de_apoio_id == ponto_de_apoio_id)
    if tipo_de_recurso_id is not None:
        consulta = consulta.filter(Lancamento.tipo_de_recurso_id == tipo_de_recurso_id)
    if periodo_inicio is not None:
        consulta = consulta.filter(Lancamento.registrado_em >= periodo_inicio)
    if periodo_fim is not None:
        consulta = consulta.filter(Lancamento.registrado_em <= periodo_fim)

    if cursor:
        posicao = decodificar_cursor(cursor)
        try:
            registrado_em_cursor = datetime.fromisoformat(posicao["registrado_em"])
            id_cursor = uuid.UUID(posicao["id"])
        except (KeyError, ValueError) as exc:
            raise ErroDeValidacao(mensagem="Cursor de paginação inválido.", campo="cursor") from exc
        consulta = consulta.filter(
            tuple_(Lancamento.registrado_em, Lancamento.id) > (registrado_em_cursor, id_cursor)
        )

    consulta = consulta.order_by(Lancamento.registrado_em, Lancamento.id).limit(tamanho + 1)
    lancamentos = consulta.all()

    proximo_cursor = None
    if len(lancamentos) > tamanho:
        lancamentos = lancamentos[:tamanho]
        ultimo = lancamentos[-1]
        proximo_cursor = codificar_cursor(
            {"registrado_em": ultimo.registrado_em.isoformat(), "id": str(ultimo.id)}
        )

    return lancamentos, proximo_cursor


def saldo_de(sessao: Session, *, tipo_de_recurso_id, ponto_de_apoio_id) -> Decimal:
    """O saldo é sempre agregado sobre `lancamento`, nunca um número
    editável: recontar devolve o mesmo número (`RF-07-07`, `RN-07-36`,
    design — Decisions 1). Crédito soma, débito subtrai, ajuste entra pelo
    sinal que a própria quantidade já carrega. Exclui o lançamento de
    destinação **ressarcimento**: a receita destinada a ressarcir credita
    reconhecimento, não estoque (`RN-07-38`, design — Decisions 2)."""
    contribuicao = case(
        (Lancamento.natureza == NaturezaDoLancamento.debito, -Lancamento.quantidade),
        else_=Lancamento.quantidade,
    )
    total = (
        sessao.query(func.coalesce(func.sum(contribuicao), 0))
        .filter(
            Lancamento.tipo_de_recurso_id == tipo_de_recurso_id,
            Lancamento.ponto_de_apoio_id == ponto_de_apoio_id,
            Lancamento.destinacao == DestinacaoDoAporte.lastro,
        )
        .scalar()
    )
    return Decimal(total)
