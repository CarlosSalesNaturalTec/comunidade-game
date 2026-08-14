from sqlalchemy.orm import Session

from ..aulas.modelo import Aula
from ..comunidades.regra import abrir_vinculo
from ..erros import ErroDeValidacao, PermissaoNegada
from .modelo import Nick, Papel, Persona

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
    aula: Aula | None = None,
    nick: str | None = None,
    permitir_semeadura_de_admin: bool = False,
) -> Persona:
    """Cria a persona aplicando RN-01-01, RN-01-02 e RN-01-05. Login nunca
    chama esta função (`RN-01-04`) — quem chama é quem cadastra: Admin,
    Mestre ou, no caso do Guerreiro(a), o próprio autocadastro.

    O nick é exigido só do Guerreiro(a) (`RF-01-19`); a unicidade é conferida
    antes de qualquer gravação, para que a recusa nunca deixe persona
    nem nick a meio caminho (`RN-01-30`). A comunidade do Guerreiro(a) nunca
    é parâmetro desta função: ela vem só da `aula` agendada em que ele se
    cadastra, nunca de quem cadastra (`RF-08-02`, `RN-08-02`, PRD-08).
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

    if papel == Papel.guerreiro and aula is None:
        raise ErroDeValidacao(
            mensagem="Guerreiro(a) precisa de uma aula agendada que origine o vínculo de "
            "comunidade.",
            campo="aula_id",
        )

    if papel == Papel.guerreiro:
        if not nick or not nick.strip():
            raise ErroDeValidacao(mensagem="Guerreiro(a) precisa de nick.", campo="nick")
        if sessao.query(Nick).filter_by(valor=nick).first() is not None:
            raise ErroDeValidacao(mensagem="Este nick já está em uso.", campo="nick")

    persona = Persona(
        papel=papel,
        criada_por=criada_por.id if criada_por is not None else None,
    )
    sessao.add(persona)
    sessao.flush()

    if nick is not None:
        sessao.add(Nick(persona_id=persona.id, valor=nick))
        sessao.flush()

    if papel == Papel.guerreiro:
        abrir_vinculo(sessao, guerreiro=persona, comunidade_id=aula.comunidade_virtual_id)

    return persona
