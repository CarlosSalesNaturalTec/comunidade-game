import uuid

from sqlalchemy.orm import Session

from ..erros import ErroDeValidacao, PermissaoNegada
from ..personas.modelo import Papel, Persona
from ..poderes.modelo import Poder
from ..trilhas.modelo import Atividade, FormatoDeAtividade, ModalidadeDeAtividade


def cadastrar_atividade_avulsa(
    sessao: Session,
    *,
    operador: Persona,
    titulo: str | None,
    descricao: str | None = None,
    modalidade: str | None,
    formato: str | None,
    natureza: str | None,
    producao_esperada: str | None,
    poder_id: uuid.UUID | None,
) -> Atividade:
    """A única atividade que a gestão cadastra, fora de trilha e sem
    missão: o poder é onde o ponto regular dela pousa, no lugar da missão
    que a atividade de trilha sempre exige (`RF-02-29`, design — decisões
    1, 2, 3). Restrita ao Admin — nem o Mestre, cuja bancada de autoria é
    a App 09, cadastra aqui.
    """
    if operador.papel != Papel.admin:
        raise PermissaoNegada(mensagem="Só o Admin cadastra a atividade avulsa.")

    if not titulo or not titulo.strip():
        raise ErroDeValidacao(mensagem="Atividade avulsa exige um título.", campo="titulo")

    if not modalidade:
        raise ErroDeValidacao(mensagem="Atividade avulsa exige modalidade.", campo="modalidade")
    try:
        modalidade_valida = ModalidadeDeAtividade(modalidade)
    except ValueError as exc:
        raise ErroDeValidacao(
            mensagem="Modalidade fora dos valores previstos.", campo="modalidade"
        ) from exc

    if not formato:
        raise ErroDeValidacao(mensagem="Atividade avulsa exige formato.", campo="formato")
    try:
        formato_valido = FormatoDeAtividade(formato)
    except ValueError as exc:
        raise ErroDeValidacao(
            mensagem="Formato fora dos valores previstos.", campo="formato"
        ) from exc

    if not natureza or not natureza.strip():
        raise ErroDeValidacao(mensagem="Atividade avulsa exige natureza.", campo="natureza")

    if not producao_esperada or not producao_esperada.strip():
        raise ErroDeValidacao(
            mensagem="Atividade avulsa exige a declaração do que o Guerreiro(a) produz.",
            campo="producao_esperada",
        )

    if poder_id is None:
        raise ErroDeValidacao(
            mensagem="Atividade avulsa exige o poder que ela desenvolve.", campo="poder_id"
        )
    poder = sessao.get(Poder, poder_id)
    if poder is None:
        raise ErroDeValidacao(mensagem="Poder não encontrado no catálogo.", campo="poder_id")

    atividade = Atividade(
        missao_id=None,
        poder_id=poder.id,
        titulo=titulo,
        descricao=descricao,
        modalidade=modalidade_valida,
        formato=formato_valido,
        natureza=natureza.strip().lower(),
        producao_esperada=producao_esperada,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(atividade)
    sessao.flush()
    return atividade


def listar_atividades_avulsas(sessao: Session) -> list[Atividade]:
    """A lista do que a gestão já cadastrou, para a tela de Atividades da
    App 03 (`RF-02-29`)."""
    return sessao.query(Atividade).filter(Atividade.missao_id.is_(None)).all()
