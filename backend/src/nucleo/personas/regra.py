import uuid

from sqlalchemy.orm import Session

from ..erros import ErroDeValidacao, PermissaoNegada
from .modelo import Papel, Persona

# Quem cadastra quem (RN-01-01, RN-01-02). Guerreiro(a) tem autocadastro:
# frozenset vazio significa "nenhum autor exigido".
_PAPEIS_QUE_CADASTRAM: dict[Papel, frozenset[Papel]] = {
    Papel.guerreiro: frozenset(),
    Papel.mestre: frozenset({Papel.admin}),
    Papel.apoiador: frozenset({Papel.admin}),
    Papel.responsavel: frozenset({Papel.admin, Papel.mestre}),
    Papel.admin: frozenset({Papel.admin}),
}


def criar_persona(
    sessao: Session,
    *,
    papel: Papel | None,
    criada_por: Persona | None,
    comunidade_virtual_id: uuid.UUID | None = None,
    permitir_semeadura_de_admin: bool = False,
) -> Persona:
    """Cria a persona aplicando RN-01-01, RN-01-02 e RN-01-05. Login nunca
    chama esta função (`RN-01-04`) — quem chama é quem cadastra: Admin,
    Mestre ou, no caso do Guerreiro(a), o próprio autocadastro.
    """
    if papel is None:
        raise ErroDeValidacao(mensagem="Toda persona precisa declarar o papel.", campo="papel")

    autores_exigidos = _PAPEIS_QUE_CADASTRAM[papel]
    eh_semeadura_de_admin = permitir_semeadura_de_admin and papel == Papel.admin
    if autores_exigidos and not eh_semeadura_de_admin:
        if criada_por is None or criada_por.papel not in autores_exigidos:
            raise PermissaoNegada(
                mensagem=f"Persona de {papel.value} só é cadastrada por quem tem autoridade "
                "para isso."
            )

    if papel == Papel.guerreiro and comunidade_virtual_id is None:
        raise ErroDeValidacao(
            mensagem="Guerreiro(a) precisa de vínculo com uma comunidade.",
            campo="comunidade_virtual_id",
        )

    persona = Persona(
        papel=papel,
        comunidade_virtual_id=comunidade_virtual_id if papel == Papel.guerreiro else None,
        criada_por=criada_por.id if criada_por is not None else None,
    )
    sessao.add(persona)
    sessao.flush()
    return persona


def vincular_guerreiro_a_comunidade(persona: Persona, comunidade_virtual_id: uuid.UUID) -> None:
    """Vínculo obrigatório a exatamente uma comunidade (`RN-01-05`). Um
    segundo vínculo vigente é recusado; o existente permanece.
    """
    if persona.papel != Papel.guerreiro:
        raise ErroDeValidacao(mensagem="Só o Guerreiro(a) tem vínculo de comunidade.")
    if persona.comunidade_virtual_id is not None:
        raise ErroDeValidacao(
            mensagem="Este Guerreiro(a) já tem um vínculo de comunidade vigente.",
            campo="comunidade_virtual_id",
        )
    persona.comunidade_virtual_id = comunidade_virtual_id
