from sqlalchemy.orm import Session

from .modelo import Credencial, Papel, Persona, TipoDeCredencial
from .regra import criar_persona


def semear_admin_fundador(sessao: Session, identidade_fundador: str) -> Persona | None:
    """Converge a persona Admin do fundador a partir da identidade social
    declarada no ambiente (`RF-01-61`). Não insere de novo se já existe, e
    não cria persona de nenhum outro papel.
    """
    credencial_existente = (
        sessao.query(Credencial)
        .filter_by(tipo=TipoDeCredencial.login_social, identificador=identidade_fundador)
        .first()
    )
    if credencial_existente is not None:
        return None

    persona = criar_persona(
        sessao, papel=Papel.admin, criada_por=None, permitir_semeadura_de_admin=True
    )

    credencial = Credencial(
        persona_id=persona.id,
        tipo=TipoDeCredencial.login_social,
        identificador=identidade_fundador,
        criada_por=None,
        troca_pendente=False,
        ativa=True,
    )
    sessao.add(credencial)
    sessao.commit()
    return persona
