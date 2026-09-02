import hashlib
import hmac
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.orm import Session

from .banco import obter_sessao
from .chaves.segredo import calcular_resumo as calcular_resumo_do_segredo
from .erros import (
    CredencialDeDispositivoInvalida,
    SessaoAusente,
    SessaoInvalida,
    TrocaDeSenhaPendente,
)
from .personas.modelo import Credencial, Papel, Persona, TipoDeCredencial
from .sessoes.modelo import Sessao
from .sessoes.token import calcular_resumo

NOME_DO_CABECALHO_DE_SESSAO = "Authorization"
PREFIXO_DO_TOKEN = "Bearer "
NOME_DO_CABECALHO_DE_DISPOSITIVO = "X-Credencial-Dispositivo"

# Mesmo padrão de `chaves.conferencia`: um identificador e um segredo
# fantasmas para que credencial inexistente e segredo errado custem o mesmo
# tempo (`RF-01-67`, design — decisões).
_IDENTIFICADOR_DE_DISPOSITIVO_FANTASMA = ""
_SEGREDO_DE_DISPOSITIVO_FANTASMA = ""
_RESUMO_DE_DISPOSITIVO_FANTASMA = hashlib.sha256(
    b"comunidade-game-resumo-fantasma-dispositivo"
).hexdigest()

# Única rota que uma sessão com troca de senha pendente pode chamar (RF-01-12).
ROTA_DE_TROCA_DE_SENHA = "/v1/credenciais/senha"


@dataclass(frozen=True)
class ContextoDaSessao:
    persona_id: uuid.UUID
    papel: Papel
    sessao_id: uuid.UUID


@dataclass(frozen=True)
class ContextoDoDispositivo:
    """Nunca `ContextoDaSessao`: sem papel, sem `sessao_id` — o que impede,
    por construção, a credencial de dispositivo escorregar para uma rota
    que espera persona (`RN-08-23`, `RN-01-34`, design — decisões)."""

    credencial_id: uuid.UUID
    coletor_id: uuid.UUID
    serie_de_coleta_id: uuid.UUID


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

    contexto = ContextoDaSessao(persona_id=persona.id, papel=persona.papel, sessao_id=registro.id)
    # A trilha de auditoria (RF-01-29) lê este contexto de `request.state`
    # depois de `call_next`, sem recalcular sessão — nenhuma rota muda.
    request.state.contexto_da_sessao = contexto
    return contexto


def persona_opcional(
    request: Request,
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> ContextoDaSessao | None:
    """A mesma resolução de `exigir_persona`, mas devolve `None` sem token —
    para a rota que responde às duas personas pelo mesmo caminho: sem
    sessão como leitura pública, com sessão de Admin com o alcance da
    gestão (`RF-14-60`, `RF-02-104`, design — Decisions 9). Token presente
    e inválido continua recusado, como em `exigir_persona`."""
    if _extrair_token(request) is None:
        return None
    return exigir_persona(request, sessao_bd)


def _extrair_credencial_de_dispositivo(request: Request) -> tuple[str, str]:
    cabecalho = request.headers.get(NOME_DO_CABECALHO_DE_DISPOSITIVO)
    if not cabecalho or "." not in cabecalho:
        return _IDENTIFICADOR_DE_DISPOSITIVO_FANTASMA, _SEGREDO_DE_DISPOSITIVO_FANTASMA
    identificador, segredo = cabecalho.split(".", 1)
    if not identificador or not segredo:
        return _IDENTIFICADOR_DE_DISPOSITIVO_FANTASMA, _SEGREDO_DE_DISPOSITIVO_FANTASMA
    return identificador, segredo


def exigir_credencial_de_dispositivo(
    request: Request,
    sessao_bd: Session,
    serie_de_coleta_id: uuid.UUID,
) -> ContextoDoDispositivo:
    """Confere a credencial de dispositivo pelo par identificador e série
    (`RN-01-53`), a cada chamada e sem sessão (`RN-08-23`). Vive ao lado de
    `exigir_persona`, mas nunca chama nem devolve `ContextoDaSessao` — é o
    que impede a credencial de alcançar rota que espera persona. Chamada
    manualmente pelo resolvedor de autenticação do registro de coleta
    (design — decisões), nunca via `Depends()` direto: o terceiro parâmetro
    vem do corpo do formulário daquela rota, não é injetável sozinho.
    """
    identificador, segredo = _extrair_credencial_de_dispositivo(request)

    registro = (
        sessao_bd.query(Credencial)
        .filter_by(
            tipo=TipoDeCredencial.dispositivo,
            identificador=identificador,
            serie_de_coleta_id=serie_de_coleta_id,
            ativa=True,
        )
        .first()
    )

    resumo_esperado = registro.segredo if registro is not None else _RESUMO_DE_DISPOSITIVO_FANTASMA
    resumo_calculado = calcular_resumo_do_segredo(segredo)
    resumo_confere = hmac.compare_digest(resumo_calculado, resumo_esperado)

    if registro is None or not resumo_confere:
        raise CredencialDeDispositivoInvalida()

    return ContextoDoDispositivo(
        credencial_id=registro.id,
        coletor_id=registro.persona_id,
        serie_de_coleta_id=registro.serie_de_coleta_id,
    )
