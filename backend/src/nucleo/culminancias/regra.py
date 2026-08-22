from sqlalchemy.orm import Session

from ..erros import ErroDeValidacao, NaoEncontrado
from ..personas.modelo import Persona
from ..trilhas.modelo import Trilha
from ..trilhas.regra import conferir_autoria_estrita_da_trilha
from .modelo import Culminancia, ModalidadeDaCulminancia


def declarar_culminancia(
    sessao: Session,
    *,
    trilha: Trilha | None,
    operador: Persona,
    descricao: str | None,
    modalidade: str | None,
    criterio_de_validacao: str | None,
) -> Culminancia:
    """Privativa do Mestre autor — outro Mestre e o Admin são recusados com
    403 (`RF-09-29`, `RF-09-30`). A segunda declaração substitui a
    anterior em vez de criar uma segunda linha, pela unicidade de
    `trilha_id` (design — decisões 1).
    """
    if trilha is None:
        raise NaoEncontrado(mensagem="Trilha não encontrada.")
    conferir_autoria_estrita_da_trilha(trilha, operador)

    if not descricao or not descricao.strip():
        raise ErroDeValidacao(
            mensagem="Culminância exige a descrição da criação original esperada.",
            campo="descricao",
        )
    if not modalidade:
        raise ErroDeValidacao(mensagem="Culminância exige modalidade.", campo="modalidade")
    try:
        modalidade_valida = ModalidadeDaCulminancia(modalidade)
    except ValueError as exc:
        raise ErroDeValidacao(
            mensagem="Modalidade fora dos valores previstos.", campo="modalidade"
        ) from exc
    if not criterio_de_validacao or not criterio_de_validacao.strip():
        raise ErroDeValidacao(
            mensagem="Culminância exige o critério de validação.",
            campo="criterio_de_validacao",
        )

    culminancia = sessao.query(Culminancia).filter_by(trilha_id=trilha.id).first()
    if culminancia is None:
        culminancia = Culminancia(
            trilha_id=trilha.id,
            descricao=descricao,
            modalidade=modalidade_valida,
            criterio_de_validacao=criterio_de_validacao,
            autor_id=operador.id,
            papel_do_autor=operador.papel.value,
        )
        sessao.add(culminancia)
    else:
        culminancia.descricao = descricao
        culminancia.modalidade = modalidade_valida
        culminancia.criterio_de_validacao = criterio_de_validacao

    sessao.flush()
    return culminancia
