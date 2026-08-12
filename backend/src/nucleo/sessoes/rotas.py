import uuid
from collections.abc import Callable
from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..autenticacao import ContextoDaSessao, exigir_persona
from ..banco import obter_sessao
from ..chaves.conferencia import ContextoDaChave, exigir_chave_de_aplicacao
from ..configuracao import Configuracao, obter_configuracao
from ..erros import CredencialInvalida, LoginSemCadastro
from ..permissoes import MATRIZ_DE_PERMISSOES
from ..personas.modelo import Credencial, Papel, Persona, TipoDeCredencial
from ..personas.senha import conferir_senha
from .modelo import ComoAutenticou, Sessao
from .social import TokenSocialInvalido, obter_verificador_social
from .token import calcular_resumo, gerar_token

roteador = APIRouter()


class AberturaDeSessaoSaida(BaseModel):
    token: str
    expira_em: datetime
    papel: Papel


def _abrir_sessao(
    sessao_bd: Session,
    configuracao: Configuracao,
    *,
    persona_id: uuid.UUID,
    papel: Papel,
    origem: str,
    como_autenticou: ComoAutenticou,
) -> AberturaDeSessaoSaida:
    token = gerar_token()
    expira_em = datetime.now(UTC) + configuracao.sessao_adulto_duracao
    registro = Sessao(
        persona_id=persona_id,
        resumo_do_token=calcular_resumo(token),
        expira_em=expira_em,
        origem=origem,
        como_autenticou=como_autenticou,
    )
    sessao_bd.add(registro)
    sessao_bd.commit()
    return AberturaDeSessaoSaida(token=token, expira_em=expira_em, papel=papel)


class LoginSocialEntrada(BaseModel):
    id_token: str


@roteador.post("/sessoes/social", status_code=201)
def login_social(
    entrada: LoginSocialEntrada,
    contexto_da_chave: Annotated[ContextoDaChave, Depends(exigir_chave_de_aplicacao)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    configuracao: Annotated[Configuracao, Depends(obter_configuracao)],
    verificar: Annotated[Callable[[str], str], Depends(obter_verificador_social)],
) -> AberturaDeSessaoSaida:
    try:
        email = verificar(entrada.id_token)
    except TokenSocialInvalido as exc:
        raise LoginSemCadastro() from exc

    credencial = (
        sessao_bd.query(Credencial)
        .filter_by(tipo=TipoDeCredencial.login_social, identificador=email, ativa=True)
        .first()
    )
    if credencial is None:
        raise LoginSemCadastro()

    persona = sessao_bd.get(Persona, credencial.persona_id)
    return _abrir_sessao(
        sessao_bd,
        configuracao,
        persona_id=persona.id,
        papel=persona.papel,
        origem=contexto_da_chave.aplicacao,
        como_autenticou=ComoAutenticou.social,
    )


class LoginPorCredencialEntrada(BaseModel):
    usuario: str
    senha: str


@roteador.post("/sessoes/credencial", status_code=201)
def login_por_credencial(
    entrada: LoginPorCredencialEntrada,
    contexto_da_chave: Annotated[ContextoDaChave, Depends(exigir_chave_de_aplicacao)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    configuracao: Annotated[Configuracao, Depends(obter_configuracao)],
) -> AberturaDeSessaoSaida:
    credencial = (
        sessao_bd.query(Credencial)
        .filter_by(tipo=TipoDeCredencial.usuario_e_senha, identificador=entrada.usuario, ativa=True)
        .first()
    )
    if credencial is None:
        raise LoginSemCadastro()
    if not conferir_senha(credencial.segredo, entrada.senha, configuracao):
        raise CredencialInvalida()

    persona = sessao_bd.get(Persona, credencial.persona_id)
    return _abrir_sessao(
        sessao_bd,
        configuracao,
        persona_id=persona.id,
        papel=persona.papel,
        origem=contexto_da_chave.aplicacao,
        como_autenticou=ComoAutenticou.credencial,
    )


@roteador.delete("/sessoes/atual", status_code=204)
def encerrar_sessao(
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> None:
    registro = sessao_bd.get(Sessao, contexto.sessao_id)
    registro.encerrada_em = datetime.now(UTC)
    sessao_bd.commit()


class EuSaida(BaseModel):
    persona_id: uuid.UUID
    papel: Papel
    permissoes: dict[str, list[str]]


@roteador.get("/eu")
def eu(contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)]) -> EuSaida:
    matriz_do_papel = MATRIZ_DE_PERMISSOES[contexto.papel]
    return EuSaida(
        persona_id=contexto.persona_id,
        papel=contexto.papel,
        permissoes={acesso: sorted(operacoes) for acesso, operacoes in matriz_do_papel.items()},
    )
