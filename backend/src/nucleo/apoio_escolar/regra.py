from datetime import UTC, datetime

from sqlalchemy.orm import Session

from ..erros import ErroDeValidacao, PermissaoNegada
from ..personas.modelo import Papel, Persona
from .modelo import Conteudo, Disciplina


def _exigir_mestre_ou_admin(operador: Persona) -> None:
    if operador.papel not in (Papel.mestre, Papel.admin):
        raise PermissaoNegada(mensagem="Só Mestre ou Admin cadastram o corpus do apoio escolar.")


def conferir_posse_do_conteudo(conteudo: Conteudo, persona: Persona) -> None:
    """Aceita o Mestre autor e o Admin; recusa qualquer outro Mestre com
    403, no mesmo padrão de `trilhas.regra.conferir_posse_da_trilha`
    (`RF-01-16`, design — decisões).
    """
    if persona.papel == Papel.admin:
        return
    if conteudo.autor_id != persona.id:
        raise PermissaoNegada(mensagem="Só o Mestre autor escreve no próprio conteúdo.")


def _normalizar_nome(nome: str) -> str:
    return nome.strip().lower()


def cadastrar_disciplina(sessao: Session, *, operador: Persona, nome: str | None) -> Disciplina:
    """Catálogo aberto: qualquer Mestre cadastra, sem posse (`RF-01-35`,
    design — decisões)."""
    _exigir_mestre_ou_admin(operador)
    if not nome or not nome.strip():
        raise ErroDeValidacao(mensagem="Disciplina exige nome.", campo="nome")

    nome_normalizado = _normalizar_nome(nome)
    existente = sessao.query(Disciplina).filter_by(nome_normalizado=nome_normalizado).first()
    if existente is not None:
        raise ErroDeValidacao(mensagem="Já existe disciplina com este nome.", campo="nome")

    disciplina = Disciplina(
        nome=nome,
        nome_normalizado=nome_normalizado,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(disciplina)
    sessao.flush()
    return disciplina


def cadastrar_conteudo(
    sessao: Session,
    *,
    operador: Persona,
    disciplina: Disciplina | None,
    material: str | None,
) -> Conteudo:
    """Pertence a exatamente uma disciplina; a posse do próprio conteúdo é
    conferida em alteração futura, não no cadastro (`RF-01-35`,
    `RF-01-16`)."""
    _exigir_mestre_ou_admin(operador)
    if disciplina is None:
        raise ErroDeValidacao(mensagem="Conteúdo exige uma disciplina.", campo="disciplina_id")
    if not material or not material.strip():
        raise ErroDeValidacao(mensagem="Conteúdo exige material.", campo="material")

    conteudo = Conteudo(
        disciplina_id=disciplina.id,
        material=material,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(conteudo)
    sessao.flush()
    return conteudo


def alterar_conteudo(
    sessao: Session, conteudo: Conteudo, *, operador: Persona, material: str
) -> Conteudo:
    conferir_posse_do_conteudo(conteudo, operador)
    if not material or not material.strip():
        raise ErroDeValidacao(mensagem="Conteúdo exige material.", campo="material")
    conteudo.material = material
    sessao.flush()
    return conteudo


def despublicar_conteudo(
    sessao: Session,
    conteudo: Conteudo,
    *,
    operador: Persona,
    motivo: str | None,
) -> Conteudo:
    """Restrito a Admin, sem exigir posse — a mesma auditoria por
    amostragem que já vale para a trilha (`RF-01-35`, `RF-01-16`, 03 §7)."""
    if operador.papel != Papel.admin:
        raise PermissaoNegada(mensagem="Só Admin despublica conteúdo do corpus.")
    if not motivo or not motivo.strip():
        raise ErroDeValidacao(mensagem="Despublicação exige motivo.", campo="motivo")

    conteudo.despublicado_em = datetime.now(UTC)
    conteudo.despublicado_por_id = operador.id
    conteudo.motivo_da_despublicacao = motivo
    sessao.flush()
    return conteudo
