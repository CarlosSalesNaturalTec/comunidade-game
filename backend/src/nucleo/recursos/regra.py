from datetime import date
from decimal import Decimal

from sqlalchemy.orm import Session

from ..erros import ErroDeValidacao, PermissaoNegada, TipoEmUso
from ..personas.modelo import Papel, Persona
from ..referencias import esta_em_uso
from .modelo import NaturezaDoRecurso, PrecoDeReferencia, TipoDeRecurso, ValorDeReferencia

PISO_DE_PONTOS_EXTRAS = 25


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


def listar_tipos_de_recurso(sessao: Session, *, operador: Persona) -> list[TipoDeRecurso]:
    """Admin e Mestre leem o catálogo — o Admin porque cadastra, o Mestre
    porque escolhe entre os tipos ao assumir uma necessidade como absorção
    e precisa saber a natureza e se exige comprovante (`RF-07-01`,
    `RF-09-56`, `RF-09-57`). A escrita segue privativa do Admin. Ordenado
    por nome: catálogo pequeno, sem paginação por cursor, e a listagem
    serve o seletor de tipo de recurso da gestão (PRD-02 §6.2)."""
    if operador.papel not in (Papel.admin, Papel.mestre):
        raise PermissaoNegada(mensagem="Só Admin ou Mestre leem o catálogo de tipos de recurso.")
    return sessao.query(TipoDeRecurso).order_by(TipoDeRecurso.nome).all()


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


def registrar_preco_de_referencia(
    sessao: Session,
    *,
    operador: Persona,
    tipo: TipoDeRecurso,
    preco_em_pontos_extras: int | Decimal | None,
    vigencia_inicio: date | None,
) -> PrecoDeReferencia:
    """A segunda régua do tipo de recurso, irmã de `registrar_valor_de_
    referencia` — mesma mecânica de vigência, nunca deriva nem altera o
    valor em moedas (`RF-07-42`, `RF-07-43`, `RN-07-24`, `RN-07-25`,
    design — Decisions 1). Preço fracionário ou abaixo do piso de 25 é
    recusado aqui, antes do banco (`RF-07-44`, `RN-07-30`)."""
    if operador.papel != Papel.admin:
        raise PermissaoNegada(mensagem="Só o Admin registra preço de referência.")
    if preco_em_pontos_extras is None:
        raise ErroDeValidacao(
            mensagem="Preço de referência exige o preço em pontos extras.",
            campo="preco_em_pontos_extras",
        )
    if vigencia_inicio is None:
        raise ErroDeValidacao(
            mensagem="Preço de referência exige o início de vigência.", campo="vigencia_inicio"
        )
    if preco_em_pontos_extras != int(preco_em_pontos_extras):
        raise ErroDeValidacao(
            mensagem="Preço de referência é número inteiro de pontos extras, sem casas decimais.",
            campo="preco_em_pontos_extras",
        )
    preco_em_pontos_extras = int(preco_em_pontos_extras)
    if preco_em_pontos_extras < PISO_DE_PONTOS_EXTRAS:
        raise ErroDeValidacao(
            mensagem=f"Preço de referência não pode ser menor que {PISO_DE_PONTOS_EXTRAS} "
            "pontos extras.",
            campo="preco_em_pontos_extras",
        )

    vigencia_aberta = (
        sessao.query(PrecoDeReferencia)
        .filter_by(tipo_de_recurso_id=tipo.id, vigencia_fim=None)
        .first()
    )
    if vigencia_aberta is not None:
        vigencia_aberta.vigencia_fim = vigencia_inicio

    novo_preco = PrecoDeReferencia(
        tipo_de_recurso_id=tipo.id,
        preco_em_pontos_extras=preco_em_pontos_extras,
        vigencia_inicio=vigencia_inicio,
        vigencia_fim=None,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(novo_preco)
    sessao.flush()
    return novo_preco


def consultar_preco_de_referencia(
    sessao: Session, *, tipo: TipoDeRecurso, data: date
) -> PrecoDeReferencia | None:
    """Consulta pela data no intervalo semiaberto `inicio <= data < fim`,
    mesmo desempate de `consultar_valor_de_referencia` — a vigência
    registrada por último vence entre duas abertas no mesmo dia
    (`RF-07-43`)."""
    return (
        sessao.query(PrecoDeReferencia)
        .filter(
            PrecoDeReferencia.tipo_de_recurso_id == tipo.id,
            PrecoDeReferencia.vigencia_inicio <= data,
            (PrecoDeReferencia.vigencia_fim.is_(None)) | (PrecoDeReferencia.vigencia_fim > data),
        )
        .order_by(PrecoDeReferencia.vigencia_inicio.desc(), PrecoDeReferencia.registrado_em.desc())
        .first()
    )


def consultar_precos_de_referencia(
    sessao: Session, *, operador: Persona, tipo: TipoDeRecurso
) -> list[PrecoDeReferencia]:
    """Restrita ao Admin — todas as vigências do tipo, da mais recente para
    a mais antiga: histórico consultável, nunca reescrito (`RF-07-43`,
    `RF-01-16`)."""
    if operador.papel != Papel.admin:
        raise PermissaoNegada(mensagem="Só o Admin lê o histórico de preço de referência.")
    return (
        sessao.query(PrecoDeReferencia)
        .filter_by(tipo_de_recurso_id=tipo.id)
        .order_by(PrecoDeReferencia.vigencia_inicio.desc(), PrecoDeReferencia.registrado_em.desc())
        .all()
    )


def _exigir_admin(operador: Persona, mensagem: str) -> None:
    if operador.papel != Papel.admin:
        raise PermissaoNegada(mensagem=mensagem)


def alterar_tipo_de_recurso(
    sessao: Session,
    tipo: TipoDeRecurso,
    *,
    operador: Persona,
    nome: str | None = None,
    unidade: str | None = None,
    exige_comprovante: bool | None = None,
    natureza: str | None = None,
) -> TipoDeRecurso:
    """Só Admin altera nome, unidade e a marca de exige comprovante. A
    natureza nunca se altera — decide se há valor de origem em reais a
    declarar —, e as vigências de valor e de preço não são tocadas
    (`RF-07-51`, design — decisão 2)."""
    _exigir_admin(operador, "Só o Admin altera tipo de recurso.")
    if natureza is not None:
        raise ErroDeValidacao(
            mensagem="A natureza do tipo de recurso não se altera.", campo="natureza"
        )
    if nome is not None and not nome.strip():
        raise ErroDeValidacao(mensagem="Tipo de recurso exige nome.", campo="nome")
    if unidade is not None and not unidade.strip():
        raise ErroDeValidacao(mensagem="Tipo de recurso exige unidade.", campo="unidade")
    if nome is not None:
        tipo.nome = nome
    if unidade is not None:
        tipo.unidade = unidade
    if exige_comprovante is not None:
        tipo.exige_comprovante = exige_comprovante
    sessao.flush()
    return tipo


def desativar_tipo_de_recurso(
    sessao: Session, tipo: TipoDeRecurso, *, operador: Persona
) -> TipoDeRecurso:
    """Desativado sai só da escolha nova; o que já existe segue inalterado
    (`RF-07-52`). Desativar o já desativado não tem efeito."""
    _exigir_admin(operador, "Só o Admin desativa tipo de recurso.")
    tipo.ativo = False
    sessao.flush()
    return tipo


def reativar_tipo_de_recurso(
    sessao: Session, tipo: TipoDeRecurso, *, operador: Persona
) -> TipoDeRecurso:
    """Volta a aceitar escolha nova (`RF-07-52`)."""
    _exigir_admin(operador, "Só o Admin reativa tipo de recurso.")
    tipo.ativo = True
    sessao.flush()
    return tipo


def exigir_tipo_de_recurso_ativo(
    tipo: TipoDeRecurso | None, *, campo: str = "tipo_de_recurso_id"
) -> None:
    """Guarda dos atos de **escolha nova** de tipo de recurso; o ato que só
    segue fato já existente não a chama (`RF-07-52`, design — decisão 6).
    Tipo ausente fica para a validação própria de cada ato."""
    if tipo is not None and not tipo.ativo:
        raise ErroDeValidacao(
            mensagem="O tipo de recurso está desativado e não pode ser escolhido.",
            campo=campo,
        )


_VIGENCIAS_DO_TIPO = frozenset({ValorDeReferencia.__tablename__, PrecoDeReferencia.__tablename__})


def excluir_tipo_de_recurso(sessao: Session, tipo: TipoDeRecurso, *, operador: Persona) -> None:
    """Só o tipo nunca usado sai, com as suas vigências; o usado é recusado
    e o caminho é desativá-lo (`RN-07-40`, design — decisão 4)."""
    _exigir_admin(operador, "Só o Admin exclui tipo de recurso.")
    if esta_em_uso(
        sessao,
        tabela=TipoDeRecurso.__table__,
        identificador=tipo.id,
        tabelas_ignoradas=_VIGENCIAS_DO_TIPO,
    ):
        raise TipoEmUso(campo="tipo_de_recurso_id")
    sessao.query(ValorDeReferencia).filter_by(tipo_de_recurso_id=tipo.id).delete()
    sessao.query(PrecoDeReferencia).filter_by(tipo_de_recurso_id=tipo.id).delete()
    sessao.delete(tipo)
    sessao.flush()
