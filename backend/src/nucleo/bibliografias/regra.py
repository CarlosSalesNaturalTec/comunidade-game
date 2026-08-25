import uuid

from sqlalchemy.orm import Session

from ..aportes.modelo import Aporte
from ..erros import ErroDeValidacao
from ..patrimonio.modelo import ItemPatrimonial
from ..personas.modelo import Persona
from ..trilhas.modelo import Missao, Trilha
from ..trilhas.regra import conferir_autoria_estrita_da_trilha
from .modelo import BibliografiaDaMissao


def _trilha_da_missao(sessao: Session, missao: Missao) -> Trilha:
    return sessao.get(Trilha, missao.trilha_id)


def criar_bibliografia(
    sessao: Session,
    *,
    operador: Persona,
    missao: Missao | None,
    titulo: str | None,
    capitulo: str | None,
    item_patrimonial_id: uuid.UUID | None,
) -> BibliografiaDaMissao:
    """Autoria estrita do Mestre autor (`RF-09-21`). O vínculo com o
    exemplar tombado é opcional — decisão do fundador de 2026-08-25 —, e o
    Apoiador **nunca** é aceito do cliente: o crédito só existe na leitura,
    derivado do exemplar (`RF-09-23`)."""
    if missao is None:
        raise ErroDeValidacao(mensagem="Bibliografia exige uma missão.", campo="missao_id")
    conferir_autoria_estrita_da_trilha(_trilha_da_missao(sessao, missao), operador)

    if not titulo or not titulo.strip():
        raise ErroDeValidacao(mensagem="Bibliografia exige o título.", campo="titulo")
    if not capitulo or not capitulo.strip():
        raise ErroDeValidacao(
            mensagem="Bibliografia exige o capítulo recomendado.", campo="capitulo"
        )

    if item_patrimonial_id is not None:
        item = sessao.get(ItemPatrimonial, item_patrimonial_id)
        if item is None:
            raise ErroDeValidacao(
                mensagem="Exemplar do acervo não encontrado.", campo="item_patrimonial_id"
            )

    bibliografia = BibliografiaDaMissao(
        missao_id=missao.id,
        titulo=titulo,
        capitulo=capitulo,
        item_patrimonial_id=item_patrimonial_id,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(bibliografia)
    sessao.flush()
    return bibliografia


def consultar_bibliografia_da_missao(
    sessao: Session, missao_id: uuid.UUID
) -> list[BibliografiaDaMissao]:
    return sessao.query(BibliografiaDaMissao).filter_by(missao_id=missao_id).all()


def ler_disponibilidade_e_credito(
    sessao: Session,
    bibliografia: BibliografiaDaMissao,
    *,
    ponto_de_apoio_id: uuid.UUID | None,
) -> tuple[bool | None, Persona | None]:
    """Deriva disponibilidade e crédito do exemplar tombado e do aporte de
    origem dele — nunca gravados (`RF-09-22`, `RF-09-23`, design — decisão
    3). Sem vínculo, nenhum dos dois é afirmado. Com vínculo, a
    disponibilidade compara o ponto de apoio do exemplar ao ponto de apoio
    de quem lê — quando este não é informado, permanece indeterminada. O
    crédito só existe quando o exemplar tem aporte de origem.
    """
    if bibliografia.item_patrimonial_id is None:
        return None, None

    item = sessao.get(ItemPatrimonial, bibliografia.item_patrimonial_id)
    if item is None:
        return None, None

    disponivel = (
        item.ponto_de_apoio_id == ponto_de_apoio_id if ponto_de_apoio_id is not None else None
    )

    apoiador = None
    if item.aporte_de_origem_id is not None:
        aporte = sessao.get(Aporte, item.aporte_de_origem_id)
        if aporte is not None:
            apoiador = sessao.get(Persona, aporte.provedor_id)

    return disponivel, apoiador
