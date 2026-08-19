import uuid

from sqlalchemy import func
from sqlalchemy.orm import Session

from ..aportes.modelo import Aporte
from ..comunidades.modelo import VinculoJogador
from ..erros import ErroDeValidacao, PermissaoNegada
from ..personas.modelo import Papel, Persona
from ..pontos_de_apoio.modelo import PontoDeApoio
from ..recursos.modelo import NaturezaDoRecurso, TipoDeRecurso
from .modelo import AnotacaoDaFichaDeVida, ItemPatrimonial, TeorDaAnotacao


def _contar_itens_do_aporte(sessao: Session, *, aporte: Aporte) -> int:
    """`SELECT ... FOR UPDATE` sobre o aporte, à imagem de `_bloquear_par`
    de `reservas/regra.py`, para que dois tombamentos concorrentes não
    passem o teto juntos (design — Decisions 6)."""
    sessao.query(Aporte.id).filter(Aporte.id == aporte.id).with_for_update().all()
    return (
        sessao.query(func.count(ItemPatrimonial.id))
        .filter(ItemPatrimonial.aporte_de_origem_id == aporte.id)
        .scalar()
    )


def tombar_item(
    sessao: Session,
    *,
    operador: Persona,
    titulo: str | None,
    numero_de_tombo: str | None,
    ponto_de_apoio: PontoDeApoio | None,
    estado_de_conservacao: str | None,
    aporte_de_origem: Aporte | None = None,
) -> ItemPatrimonial:
    """Só Admin tomba. O aporte de origem é opcional; quando declarado,
    precisa ser de tipo de natureza durável e o tombamento não pode exceder
    a quantidade aportada (`RF-07-11`, `RN-07-07`, design — Decisions 6).
    O número de tombo é digitado por quem tomba e único por ponto de apoio
    (design — Decisions 5).
    """
    if operador.papel != Papel.admin:
        raise PermissaoNegada(mensagem="Só o Admin tomba item patrimonial.")
    if not titulo or not titulo.strip():
        raise ErroDeValidacao(mensagem="Tombamento exige título.", campo="titulo")
    if not numero_de_tombo or not numero_de_tombo.strip():
        raise ErroDeValidacao(mensagem="Tombamento exige número de tombo.", campo="numero_de_tombo")
    if ponto_de_apoio is None:
        raise ErroDeValidacao(
            mensagem="Tombamento exige um ponto de apoio.", campo="ponto_de_apoio_id"
        )
    if not estado_de_conservacao or not estado_de_conservacao.strip():
        raise ErroDeValidacao(
            mensagem="Tombamento exige o estado de conservação.",
            campo="estado_de_conservacao",
        )

    if aporte_de_origem is not None:
        tipo = sessao.get(TipoDeRecurso, aporte_de_origem.tipo_de_recurso_id)
        if tipo.natureza != NaturezaDoRecurso.duravel:
            raise ErroDeValidacao(
                mensagem="O aporte de origem precisa ser de tipo de natureza durável.",
                campo="aporte_de_origem_id",
            )
        tombados = _contar_itens_do_aporte(sessao, aporte=aporte_de_origem)
        if tombados >= aporte_de_origem.quantidade:
            raise ErroDeValidacao(
                mensagem="O tombamento excederia a quantidade aportada.",
                campo="aporte_de_origem_id",
            )

    repetido = (
        sessao.query(ItemPatrimonial.id)
        .filter_by(ponto_de_apoio_id=ponto_de_apoio.id, numero_de_tombo=numero_de_tombo)
        .first()
    )
    if repetido is not None:
        raise ErroDeValidacao(
            mensagem="Já existe um exemplar com este número de tombo neste ponto de apoio.",
            campo="numero_de_tombo",
        )

    item = ItemPatrimonial(
        aporte_de_origem_id=aporte_de_origem.id if aporte_de_origem is not None else None,
        titulo=titulo,
        numero_de_tombo=numero_de_tombo,
        ponto_de_apoio_id=ponto_de_apoio.id,
        estado_de_conservacao=estado_de_conservacao,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(item)
    sessao.flush()
    return item


def anotar_ficha_de_vida(
    sessao: Session,
    *,
    operador: Persona,
    item: ItemPatrimonial | None,
    teor: str | None,
    estado_de_conservacao: str | None,
) -> AnotacaoDaFichaDeVida:
    """Admin ou Mestre anotam. A anotação não recebe Guerreiro(a) como
    parâmetro e não chama `livro_razao` nem `ponto_extra`: não há caminho
    de código para perda ou dano virar débito (`RF-07-48`, `RN-07-09`,
    design — Decisions 7). Reescreve o estado de conservação corrente do
    item (design — Decisions 3).
    """
    if operador.papel not in (Papel.admin, Papel.mestre):
        raise PermissaoNegada(mensagem="Só Admin ou Mestre anotam a ficha de vida.")
    if item is None:
        raise ErroDeValidacao(
            mensagem="Anotação exige um item patrimonial existente.",
            campo="item_patrimonial_id",
        )
    try:
        teor_valido = TeorDaAnotacao(teor)
    except (ValueError, TypeError) as exc:
        raise ErroDeValidacao(
            mensagem="Teor precisa ser cuidado, perda ou dano.", campo="teor"
        ) from exc
    if not estado_de_conservacao or not estado_de_conservacao.strip():
        raise ErroDeValidacao(
            mensagem="Anotação exige o estado de conservação apurado.",
            campo="estado_de_conservacao",
        )

    anotacao = AnotacaoDaFichaDeVida(
        item_patrimonial_id=item.id,
        teor=teor_valido,
        estado_de_conservacao=estado_de_conservacao,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(anotacao)
    item.estado_de_conservacao = estado_de_conservacao
    sessao.flush()
    return anotacao


def listar_ficha_de_vida(
    sessao: Session, *, item_patrimonial_id: uuid.UUID
) -> list[AnotacaoDaFichaDeVida]:
    """Da anotação mais antiga à mais recente (`RF-07-11`)."""
    return (
        sessao.query(AnotacaoDaFichaDeVida)
        .filter_by(item_patrimonial_id=item_patrimonial_id)
        .order_by(AnotacaoDaFichaDeVida.registrado_em.asc())
        .all()
    )


def listar_acervo(
    sessao: Session, *, operador: Persona, comunidade_virtual_id: uuid.UUID | None
) -> list[ItemPatrimonial]:
    """Admin lê qualquer comunidade, sempre declarada; Mestre lê só a do
    seu vínculo vigente. Apoiador, Guerreiro(a) e responsável recebem 403
    (`RF-07-11`, `RN-07-10`, `RF-01-16`)."""
    if operador.papel == Papel.admin:
        if comunidade_virtual_id is None:
            raise ErroDeValidacao(
                mensagem="Leitura do acervo exige o filtro de comunidade.",
                campo="comunidade_virtual_id",
            )
        alvo_id = comunidade_virtual_id
    elif operador.papel == Papel.mestre:
        vinculo: VinculoJogador | None = operador.vinculo_vigente
        if vinculo is None:
            return []
        alvo_id = vinculo.comunidade_virtual_id
    else:
        raise PermissaoNegada(mensagem="Persona sem acervo patrimonial a consultar.")

    return (
        sessao.query(ItemPatrimonial)
        .join(PontoDeApoio, PontoDeApoio.id == ItemPatrimonial.ponto_de_apoio_id)
        .filter(PontoDeApoio.comunidade_virtual_id == alvo_id)
        .order_by(ItemPatrimonial.registrado_em.desc())
        .all()
    )
