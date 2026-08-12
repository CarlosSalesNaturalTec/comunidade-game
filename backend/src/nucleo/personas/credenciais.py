import secrets

from sqlalchemy.orm import Session

from ..configuracao import Configuracao
from ..erros import PermissaoNegada
from .modelo import Credencial, Papel, Persona, TipoDeCredencial
from .senha import calcular_hash

# Só Admin ou Mestre cria credencial de usuário e senha (`RF-01-11`, `RF-01-16`).
PAPEIS_QUE_CRIAM_CREDENCIAL = frozenset({Papel.admin, Papel.mestre})


def gerar_senha_provisoria() -> str:
    return secrets.token_urlsafe(9)


def criar_credencial_provisoria(
    sessao: Session,
    configuracao: Configuracao,
    *,
    persona: Persona,
    usuario: str,
    criada_por: Persona,
) -> tuple[Credencial, str]:
    """Credencial de usuário e senha provisória, com o mesmo vínculo e as
    mesmas permissões que a persona já tem — não amplia nada (`RN-01-18`).
    A senha em claro só existe neste retorno; a base guarda apenas o hash.
    """
    if criada_por.papel not in PAPEIS_QUE_CRIAM_CREDENCIAL:
        raise PermissaoNegada(mensagem="Só Admin ou Mestre cria credencial de usuário e senha.")

    senha_provisoria = gerar_senha_provisoria()
    credencial = Credencial(
        persona_id=persona.id,
        tipo=TipoDeCredencial.usuario_e_senha,
        identificador=usuario,
        segredo=calcular_hash(senha_provisoria, configuracao),
        criada_por=criada_por.id,
        troca_pendente=True,
        ativa=True,
    )
    sessao.add(credencial)
    sessao.flush()
    return credencial, senha_provisoria
