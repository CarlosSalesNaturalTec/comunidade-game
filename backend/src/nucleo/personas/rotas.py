import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..autenticacao import ContextoDaSessao, exigir_persona
from ..banco import obter_sessao
from ..configuracao import Configuracao, obter_configuracao
from ..erros import NaoEncontrado
from .credenciais import criar_credencial_provisoria
from .modelo import Credencial, Persona, TipoDeCredencial
from .senha import calcular_hash

roteador = APIRouter()


class CriarCredencialEntrada(BaseModel):
    persona_id: uuid.UUID
    usuario: str


class CredencialSaida(BaseModel):
    id: uuid.UUID
    usuario: str
    senha_provisoria: str


@roteador.post("/credenciais", status_code=201)
def criar_credencial(
    entrada: CriarCredencialEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    configuracao: Annotated[Configuracao, Depends(obter_configuracao)],
) -> CredencialSaida:
    """Restrita a Admin e Mestre — `criar_credencial_provisoria` recusa com
    403 quem não é (`RF-01-11`, `RF-01-16`)."""
    persona_alvo = sessao_bd.get(Persona, entrada.persona_id)
    if persona_alvo is None:
        raise NaoEncontrado(mensagem="Persona não encontrada.", campo="persona_id")

    criada_por = sessao_bd.get(Persona, contexto.persona_id)
    credencial, senha_provisoria = criar_credencial_provisoria(
        sessao_bd,
        configuracao,
        persona=persona_alvo,
        usuario=entrada.usuario,
        criada_por=criada_por,
    )
    sessao_bd.commit()
    return CredencialSaida(
        id=credencial.id, usuario=credencial.identificador, senha_provisoria=senha_provisoria
    )


class TrocarSenhaEntrada(BaseModel):
    senha_nova: str


@roteador.post("/credenciais/senha", status_code=204)
def trocar_senha(
    entrada: TrocarSenhaEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    configuracao: Annotated[Configuracao, Depends(obter_configuracao)],
) -> None:
    """Conclui a troca e derruba a pendência (`RF-01-12`). A senha antiga
    deixa de valer porque o hash é substituído — não há segundo caminho
    de acesso com a senha provisória (`RN-01-18`)."""
    credencial = (
        sessao_bd.query(Credencial)
        .filter_by(
            persona_id=contexto.persona_id,
            tipo=TipoDeCredencial.usuario_e_senha,
            ativa=True,
        )
        .first()
    )
    if credencial is None:
        raise NaoEncontrado(mensagem="Esta persona não tem credencial de usuário e senha.")

    credencial.segredo = calcular_hash(entrada.senha_nova, configuracao)
    credencial.troca_pendente = False
    sessao_bd.commit()
