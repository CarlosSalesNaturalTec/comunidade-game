import uuid
from collections.abc import Callable
from datetime import UTC, datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from ..autenticacao import ContextoDaSessao, exigir_persona
from ..banco import obter_sessao
from ..biometria.regra import autenticar_por_nick_e_descritor
from ..chaves.conferencia import ContextoDaChave, exigir_chave_de_aplicacao
from ..configuracao import Configuracao, obter_configuracao
from ..erros import (
    AutenticacaoBiometricaInvalida,
    ConfirmacaoDeGuerreiroRecusada,
    CredencialInvalida,
    LoginSemCadastro,
)
from ..permissoes import MATRIZ_DE_PERMISSOES, Operacao, exigir_permissao
from ..personas.modelo import Credencial, Papel, Persona, TipoDeCredencial
from ..personas.regra import buscar_guerreiro_por_nick
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
    *,
    persona_id: uuid.UUID,
    papel: Papel,
    origem: str,
    como_autenticou: ComoAutenticou,
    duracao: timedelta,
    quem_confirmou: uuid.UUID | None = None,
) -> AberturaDeSessaoSaida:
    token = gerar_token()
    expira_em = datetime.now(UTC) + duracao
    registro = Sessao(
        persona_id=persona_id,
        resumo_do_token=calcular_resumo(token),
        expira_em=expira_em,
        origem=origem,
        como_autenticou=como_autenticou,
        quem_confirmou=quem_confirmou,
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
        persona_id=persona.id,
        papel=persona.papel,
        origem=contexto_da_chave.aplicacao,
        como_autenticou=ComoAutenticou.social,
        duracao=configuracao.sessao_adulto_duracao,
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
        persona_id=persona.id,
        papel=persona.papel,
        origem=contexto_da_chave.aplicacao,
        como_autenticou=ComoAutenticou.credencial,
        duracao=configuracao.sessao_adulto_duracao,
    )


class AbrirSessaoDeGuerreiroEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nick: str
    descritor: list[float] = Field(min_length=1)


@roteador.post("/sessoes/guerreiro", status_code=201)
def abrir_sessao_de_guerreiro(
    entrada: AbrirSessaoDeGuerreiroEntrada,
    contexto_da_chave: Annotated[ContextoDaChave, Depends(exigir_chave_de_aplicacao)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    configuracao: Annotated[Configuracao, Depends(obter_configuracao)],
) -> AberturaDeSessaoSaida:
    """Pública quanto à persona — dispensa credencial, nunca a chave de
    aplicação (`RF-01-04`, `RF-01-05`). A recusa não diferencia nick
    inexistente, Guerreiro(a) sem _template_ e descritor que não confere,
    nem no corpo nem no tempo (`RN-01-22`).
    """
    guerreiro = autenticar_por_nick_e_descritor(
        sessao_bd, configuracao, nick=entrada.nick, descritor=entrada.descritor
    )
    if guerreiro is None:
        # O registro de acesso da comparação (RN-01-14) precisa persistir mesmo
        # na recusa — sem este commit, `sessao_bd.close()` o descartaria.
        sessao_bd.commit()
        raise AutenticacaoBiometricaInvalida()

    return _abrir_sessao(
        sessao_bd,
        persona_id=guerreiro.id,
        papel=guerreiro.papel,
        origem=contexto_da_chave.aplicacao,
        como_autenticou=ComoAutenticou.biometria,
        duracao=configuracao.sessao_guerreiro_duracao,
    )


class ConfirmarSessaoDeGuerreiroEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nick: str = Field(min_length=1)


@roteador.post("/sessoes/guerreiro/confirmacao", status_code=201)
def confirmar_sessao_de_guerreiro(
    entrada: ConfirmarSessaoDeGuerreiroEntrada,
    contexto: Annotated[
        ContextoDaSessao,
        Depends(exigir_permissao(Operacao.confirmacao_de_identidade_do_guerreiro, "escreve")),
    ],
    contexto_da_chave: Annotated[ContextoDaChave, Depends(exigir_chave_de_aplicacao)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    configuracao: Annotated[Configuracao, Depends(obter_configuracao)],
) -> AberturaDeSessaoSaida:
    """Restrita a Mestre e Admin pela matriz (`RF-01-06`, `RF-01-16`) — a
    alternativa equivalente para quem não tem _template_, para a falha de
    reconhecimento e para quem recusou a biometria (`RN-01-16`). Recebe o
    **nick**, nunca um identificador: resolvê-lo por uma rota de busca
    abriria o oráculo que `RN-01-22` veda para qualquer persona, adulto
    autenticado incluído — a recusa por nick inexistente é indistinguível
    da recusa por nick de outro papel (openspec —
    esqueleto-da-aula-presencial-e-equipe-da-aula, design — decisão 1.1).
    """
    guerreiro = buscar_guerreiro_por_nick(sessao_bd, entrada.nick)
    if guerreiro is None:
        raise ConfirmacaoDeGuerreiroRecusada()

    return _abrir_sessao(
        sessao_bd,
        persona_id=guerreiro.id,
        papel=guerreiro.papel,
        origem=contexto_da_chave.aplicacao,
        como_autenticou=ComoAutenticou.confirmacao_humana,
        duracao=configuracao.sessao_guerreiro_duracao,
        quem_confirmou=contexto.persona_id,
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
