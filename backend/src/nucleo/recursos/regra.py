from datetime import date
from decimal import Decimal

from sqlalchemy.orm import Session

from ..erros import ErroDeValidacao, PermissaoNegada
from ..personas.modelo import Papel, Persona
from .modelo import NaturezaDoRecurso, TipoDeRecurso, ValorDeReferencia


def cadastrar_tipo_de_recurso(
    sessao: Session,
    *,
    operador: Persona,
    nome: str | None,
    natureza: str | None,
    unidade: str | None,
    exige_comprovante: bool = False,
) -> TipoDeRecurso:
    """Só Admin cadastra tipo de recurso, operação avulsa que não depende de
    nenhum outro fluxo (`RF-07-01`, `RF-07-03`). `exige_comprovante` é
    opcional e nasce falsa quando não declarada (`RN-07-22`)."""
    if operador.papel != Papel.admin:
        raise PermissaoNegada(mensagem="Só o Admin cadastra tipo de recurso.")
    if not nome or not nome.strip():
        raise ErroDeValidacao(mensagem="Tipo de recurso exige nome.", campo="nome")
    if not unidade or not unidade.strip():
        raise ErroDeValidacao(mensagem="Tipo de recurso exige unidade.", campo="unidade")
    try:
        natureza_valida = NaturezaDoRecurso(natureza)
    except (ValueError, TypeError) as exc:
        raise ErroDeValidacao(
            mensagem="Natureza fora dos valores previstos.", campo="natureza"
        ) from exc

    tipo = TipoDeRecurso(
        nome=nome,
        natureza=natureza_valida,
        unidade=unidade,
        exige_comprovante=exige_comprovante,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(tipo)
    sessao.flush()
    return tipo


def registrar_valor_de_referencia(
    sessao: Session,
    *,
    operador: Persona,
    tipo: TipoDeRecurso,
    valor_em_moedas: Decimal | None,
    vigencia_inicio: date | None,
) -> ValorDeReferencia:
    """Abre vigência nova e encerra a vigente no dia de início da nova, sem
    nunca reescrever nem apagar a anterior (`RF-07-02`, `RN-07-03`, design —
    Decisions 2). Valor negativo ou com mais de duas casas decimais é
    recusado aqui, antes do banco, sem arredondar em silêncio (`RN-07-04`).
    """
    if operador.papel != Papel.admin:
        raise PermissaoNegada(mensagem="Só o Admin registra valor de referência.")
    if valor_em_moedas is None:
        raise ErroDeValidacao(
            mensagem="Valor de referência exige o valor em moedas.", campo="valor_em_moedas"
        )
    if vigencia_inicio is None:
        raise ErroDeValidacao(
            mensagem="Valor de referência exige o início de vigência.", campo="vigencia_inicio"
        )
    if valor_em_moedas < 0:
        raise ErroDeValidacao(
            mensagem="Valor de referência não pode ser negativo.", campo="valor_em_moedas"
        )
    if -valor_em_moedas.as_tuple().exponent > 2:
        raise ErroDeValidacao(
            mensagem="Valor de referência aceita no máximo duas casas decimais.",
            campo="valor_em_moedas",
        )

    vigencia_aberta = (
        sessao.query(ValorDeReferencia)
        .filter_by(tipo_de_recurso_id=tipo.id, vigencia_fim=None)
        .first()
    )
    if vigencia_aberta is not None:
        vigencia_aberta.vigencia_fim = vigencia_inicio

    novo_valor = ValorDeReferencia(
        tipo_de_recurso_id=tipo.id,
        valor_em_moedas=valor_em_moedas,
        vigencia_inicio=vigencia_inicio,
        vigencia_fim=None,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(novo_valor)
    sessao.flush()
    return novo_valor


def consultar_valor_de_referencia(
    sessao: Session, *, tipo: TipoDeRecurso, data: date
) -> ValorDeReferencia | None:
    """Consulta pela data no intervalo semiaberto `inicio <= data < fim`,
    ordenada por `vigencia_inicio DESC, registrado_em DESC` — o desempate
    entre vigências abertas no mesmo dia é a ordem de registro (`RF-07-02`,
    design — Decisions 2)."""
    return (
        sessao.query(ValorDeReferencia)
        .filter(
            ValorDeReferencia.tipo_de_recurso_id == tipo.id,
            ValorDeReferencia.vigencia_inicio <= data,
            (ValorDeReferencia.vigencia_fim.is_(None)) | (ValorDeReferencia.vigencia_fim > data),
        )
        .order_by(ValorDeReferencia.vigencia_inicio.desc(), ValorDeReferencia.registrado_em.desc())
        .first()
    )
