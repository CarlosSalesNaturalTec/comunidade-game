import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.orm import Session

from .banco import obter_sessao
from .erros import SessaoAusente, SessaoInvalida, TrocaDeSenhaPendente
from .personas.modelo import Credencial, Papel, Persona, TipoDeCredencial
from .sessoes.modelo import Sessao
from .sessoes.token import calcular_resumo

NOME_DO_CABECALHO_DE_SESSAO = "Authorization"
PREFIXO_DO_TOKEN = "Bearer "

# Única rota que uma sessão com troca de senha pendente pode chamar (RF-01-12).
ROTA_DE_TROCA_DE_SENHA = "/v1/credenciais/senha"


@dataclass(frozen=True)
class ContextoDaSessao:
    persona_id: uuid.UUID
    papel: Papel
    sessao_id: uuid.UUID


def _extrair_token(request: Request) -> str | None:
    cabecalho = request.headers.get(NOME_DO_CABECALHO_DE_SESSAO)
    if not cabecalho or not cabecalho.startswith(PREFIXO_DO_TOKEN):
        return None
    token = cabecalho[len(PREFIXO_DO_TOKEN) :]
    return token or None


def exigir_persona(
    request: Request,
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> ContextoDaSessao:
    """Resolve o token opaco de sessão contra o banco (design — token
    opaco). A recusa aqui nunca se confunde com a da chave ausente
    (`RN-01-34`): são credenciais independentes.
    """
    token = _extrair_token(request)
    if token is None:
        raise SessaoAusente()

    resumo = calcular_resumo(token)
    registro = sessao_bd.query(Sessao).filter_by(resumo_do_token=resumo).first()

    agora = datetime.now(UTC)
    if registro is None or registro.encerrada_em is not None or registro.expira_em <= agora:
        raise SessaoInvalida()

    persona = sessao_bd.get(Persona, registro.persona_id)

    tem_troca_pendente = (
        sessao_bd.query(Credencial)
        .filter_by(
            persona_id=persona.id,
            tipo=TipoDeCredencial.usuario_e_senha,
            troca_pendente=True,
            ativa=True,
        )
        .first()
        is not None
    )
    if tem_troca_pendente and request.url.path != ROTA_DE_TROCA_DE_SENHA:
        raise TrocaDeSenhaPendente()

    return ContextoDaSessao(persona_id=persona.id, papel=persona.papel, sessao_id=registro.id)
