from sqlalchemy.orm import Session

from ..erros import ErroDeValidacao, PapelDoPoderTerritorioJaDeclarado, PermissaoNegada
from ..personas.modelo import Papel, Persona
from .modelo import NaturezaDoPoder, PapelDoPoder, Poder, VigenciaDoPoder


def _exigir_admin(operador: Persona) -> None:
    if operador.papel != Papel.admin:
        raise PermissaoNegada(mensagem="Só Admin cadastra, altera ou desativa poder do catálogo.")


def _conferir_papel_territorio_livre(sessao: Session) -> None:
    """Pré-conferência de aplicação para a resposta 409 rápida; o índice
    único parcial do modelo é quem garante a unicidade sob concorrência
    (`RN-01-54`, design — decisões)."""
    ja_existe = sessao.query(Poder).filter(Poder.papel == PapelDoPoder.territorio).first()
    if ja_existe is not None:
        raise PapelDoPoderTerritorioJaDeclarado()


def cadastrar_poder(
    sessao: Session,
    *,
    operador: Persona,
    nome: str | None,
    descricao: str,
    natureza: NaturezaDoPoder,
    vigencia: VigenciaDoPoder = VigenciaDoPoder.vigente,
    papel: PapelDoPoder | None = None,
    tecnico: bool = False,
) -> Poder:
    """Restrito a Admin (`RF-01-62`, `RN-01-43`); o Mestre escolhe entre os
    poderes cadastrados e nunca cria poder novo ao escrever a trilha. O
    papel e a marca de técnico são opcionais e nunca deduzidos do nome
    (`RN-01-54`).
    """
    _exigir_admin(operador)
    if not nome or not nome.strip():
        raise ErroDeValidacao(mensagem="Poder exige nome.", campo="nome")
    if papel is not None:
        _conferir_papel_territorio_livre(sessao)

    poder = Poder(
        nome=nome,
        descricao=descricao,
        natureza=natureza,
        vigencia=vigencia,
        papel=papel,
        ativo=True,
        tecnico=tecnico,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(poder)
    sessao.flush()
    return poder


def buscar_poder_do_territorio(sessao: Session) -> Poder | None:
    """Usado pelo crédito da coleta (`RN-08-15`) — nunca por aproximação de
    nome, sempre pelo papel declarado no catálogo (`RN-01-54`)."""
    return sessao.query(Poder).filter(Poder.papel == PapelDoPoder.territorio).first()


def alterar_poder(
    sessao: Session,
    poder: Poder,
    *,
    operador: Persona,
    nome: str | None = None,
    descricao: str | None = None,
    vigencia: VigenciaDoPoder | None = None,
    tecnico: bool | None = None,
) -> Poder:
    """A natureza e o papel não entram aqui: mudar de que tipo um poder é
    reescreveria o vínculo já concedido às trilhas existentes. A marca de
    técnico é alterável — dela não deriva vínculo nem crédito, só a próxima
    sugestão do template (`RN-01-54`, `RN-09-34`)."""
    _exigir_admin(operador)
    if nome is not None:
        if not nome.strip():
            raise ErroDeValidacao(mensagem="Poder exige nome.", campo="nome")
        poder.nome = nome
    if descricao is not None:
        poder.descricao = descricao
    if vigencia is not None:
        poder.vigencia = vigencia
    if tecnico is not None:
        poder.tecnico = tecnico
    sessao.flush()
    return poder


def desativar_poder(sessao: Session, poder: Poder, *, operador: Persona) -> Poder:
    _exigir_admin(operador)
    poder.ativo = False
    sessao.flush()
    return poder
