import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from ..autenticacao import ContextoDaSessao, exigir_persona
from ..banco import obter_sessao
from ..configuracao import Configuracao, obter_configuracao
from ..erros import NaoEncontrado, PermissaoNegada
from ..protecao.freio import exigir_freio_por_origem
from .credenciais import criar_credencial_provisoria
from .modelo import Credencial, Papel, Persona, TipoDeCredencial
from .regra import (
    conferir_disponibilidade_de_nick,
    definir_ou_trocar_nick,
    sugerir_variacoes_de_nick,
)
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


class DisponibilidadeDeNickSaida(BaseModel):
    disponivel: bool
    sugestoes: list[str]


@roteador.get(
    "/nicks/disponibilidade",
    dependencies=[Depends(exigir_freio_por_origem("consulta_por_nick"))],
)
def conferir_disponibilidade_de_nick_rota(
    nick: str,
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> DisponibilidadeDeNickSaida:
    """Pública, sem credencial de persona — serve o pré-cadastro e a tela do
    adulto autenticado com a mesma resposta, porque o alcance é o mesmo:
    só nicks de adulto (`RF-14-13`, `RN-01-22`, `RN-14-23`). Entra no freio
    por origem já vigente para consulta de nick, sem superfície nova
    (`RF-01-65`)."""
    disponivel = conferir_disponibilidade_de_nick(sessao_bd, nick)
    sugestoes = [] if disponivel else sugerir_variacoes_de_nick(sessao_bd, nick)
    return DisponibilidadeDeNickSaida(disponivel=disponivel, sugestoes=sugestoes)


class DefinirNickEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nick: str = Field(min_length=1)


class MinhaIdentidadeSaida(BaseModel):
    nick: str


@roteador.put("/eu/apoiador/identidade")
def definir_identidade_do_apoiador(
    entrada: DefinirNickEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> MinhaIdentidadeSaida:
    """Define ou troca o próprio nick do Apoiador em sessão; outro papel
    recebe 403 (`RF-14-12`, `RN-14-10`, `RN-01-30`, PRD-01 §9)."""
    if contexto.papel != Papel.apoiador:
        raise PermissaoNegada(mensagem="Só o Apoiador define o próprio nick por aqui.")

    persona = sessao_bd.get(Persona, contexto.persona_id)
    definir_ou_trocar_nick(sessao_bd, persona, entrada.nick)
    sessao_bd.commit()
    return MinhaIdentidadeSaida(nick=entrada.nick)


@roteador.put("/eu/mestre/identidade")
def definir_identidade_do_mestre(
    entrada: DefinirNickEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> MinhaIdentidadeSaida:
    """Rota simétrica à do Apoiador, para o Mestre definir ou trocar o
    próprio nick no primeiro acesso; outro papel recebe 403 (`RF-14-12`,
    `RN-14-10`, `RN-01-30`, PRD-01 §9, design — Decisions)."""
    if contexto.papel != Papel.mestre:
        raise PermissaoNegada(mensagem="Só o Mestre define o próprio nick por aqui.")

    persona = sessao_bd.get(Persona, contexto.persona_id)
    definir_ou_trocar_nick(sessao_bd, persona, entrada.nick)
    sessao_bd.commit()
    return MinhaIdentidadeSaida(nick=entrada.nick)
