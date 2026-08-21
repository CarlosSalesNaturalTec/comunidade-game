import uuid

from sqlalchemy.orm import Session

from ..comunidades.modelo import ComunidadeVirtual, VinculoJogador
from ..erros import ErroDeValidacao, NaoEncontrado, PermissaoNegada
from ..personas.modelo import Papel, Persona
from .modelo import PontoDeApoio

PAPEIS_QUE_PODEM_SER_RESPONSAVEL = frozenset({Papel.admin, Papel.mestre, Papel.apoiador})


def cadastrar_ponto_de_apoio(
    sessao: Session,
    *,
    operador: Persona,
    nome: str | None,
    comunidade_id: uuid.UUID | None,
) -> PontoDeApoio:
    """Só Admin cadastra ponto de apoio, sem responsável — quem responde
    pelo acervo é designado depois, em operação própria (`RF-07-47`,
    `RN-07-33`, `RF-07-49`)."""
    if operador.papel != Papel.admin:
        raise PermissaoNegada(mensagem="Só o Admin cadastra ponto de apoio.")
    if not nome or not nome.strip():
        raise ErroDeValidacao(mensagem="Ponto de apoio exige nome.", campo="nome")
    if comunidade_id is None:
        raise ErroDeValidacao(
            mensagem="Ponto de apoio exige uma comunidade.", campo="comunidade_id"
        )

    comunidade = sessao.get(ComunidadeVirtual, comunidade_id)
    if comunidade is None:
        raise ErroDeValidacao(mensagem="Comunidade não encontrada.", campo="comunidade_id")

    ponto_de_apoio = PontoDeApoio(
        nome=nome,
        comunidade_virtual_id=comunidade.id,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(ponto_de_apoio)
    sessao.flush()
    return ponto_de_apoio


def designar_responsavel(
    sessao: Session,
    ponto_de_apoio: PontoDeApoio | None,
    *,
    operador: Persona,
    responsavel: Persona | None,
) -> PontoDeApoio:
    """Designa ou troca o responsável pelo acervo, a qualquer tempo — só
    Admin, e só para persona de papel Admin, Mestre ou Apoiador; Guerreiro(a)
    e responsável familiar são recusados (`RF-07-49`, `RN-07-34`). A troca
    substitui o designado anterior, cuja designação permanece auditável pela
    trilha de auditoria (`RF-01-29`, design — Decisions 6).
    """
    if ponto_de_apoio is None:
        raise NaoEncontrado(mensagem="Ponto de apoio não encontrado.")
    if operador.papel != Papel.admin:
        raise PermissaoNegada(mensagem="Só o Admin designa o responsável pelo acervo.")
    if responsavel is None:
        raise ErroDeValidacao(
            mensagem="Designação exige o responsável pelo acervo.", campo="responsavel_id"
        )
    if responsavel.papel not in PAPEIS_QUE_PODEM_SER_RESPONSAVEL:
        raise ErroDeValidacao(
            mensagem="O responsável pelo acervo precisa ser Admin, Mestre ou Apoiador.",
            campo="responsavel_id",
        )

    ponto_de_apoio.responsavel_id = responsavel.id
    sessao.flush()
    return ponto_de_apoio


def escopo_de_comunidade_da_leitura(
    *, operador: Persona, comunidade_virtual_id: uuid.UUID | None
) -> uuid.UUID | None:
    """Resolve a comunidade a que a leitura dos pontos de apoio se
    restringe, no molde de `listar_acervo` (`patrimonio/regra.py`): Admin
    declara a comunidade, sempre obrigatória; Mestre herda do vínculo
    vigente, e sem vínculo não tem o que listar — `None` aqui sinaliza
    lista vazia, nunca erro. Demais papéis são recusados (`RF-07-47`,
    `RF-01-28`, `RF-01-18`, `RF-01-16`).
    """
    if operador.papel == Papel.admin:
        if comunidade_virtual_id is None:
            raise ErroDeValidacao(
                mensagem="Esta consulta exige o filtro de comunidade.", campo="comunidade"
            )
        return comunidade_virtual_id
    if operador.papel == Papel.mestre:
        vinculo: VinculoJogador | None = operador.vinculo_vigente
        return vinculo.comunidade_virtual_id if vinculo is not None else None
    raise PermissaoNegada(mensagem="Persona sem pontos de apoio a consultar.")
