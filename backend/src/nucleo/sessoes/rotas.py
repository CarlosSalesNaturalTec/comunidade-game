import uuid
from collections.abc import Callable
from datetime import UTC, datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from ..aulas.modelo import Aula
from ..autenticacao import ContextoDaSessao, exigir_persona
from ..banco import obter_sessao
from ..biometria.regra import autenticar_por_nick_e_descritor
from ..chaves.conferencia import ContextoDaChave, exigir_chave_de_aplicacao
from ..configuracao import Configuracao, obter_configuracao
from ..consentimentos.regra import autorizacao_de_divulgacao_vigente
from ..erros import (
    AutenticacaoBiometricaInvalida,
    ConfirmacaoDeGuerreiroRecusada,
    CredencialInvalida,
    ErroDeValidacao,
    LoginSemCadastro,
)
from ..permissoes import (
    MATRIZ_DE_PERMISSOES,
    Operacao,
    exigir_qualquer_permissao,
)
from ..personas.modelo import Credencial, Papel, Persona, TipoDeCredencial
from ..personas.regra import buscar_guerreiro_confirmavel_por
from ..personas.senha import conferir_senha
from ..pin_de_confirmacao.regra import conferir_pin_da_sessao
from ..pin_de_confirmacao.rotas import APLICACAO_DO_ENCONTRO
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
    # **Opcional**, e é a presença dela que escolhe de onde vem o limiar: com
    # aula, o ponto de apoio dela; sem aula — a entrada fora do encontro, da
    # App 05 —, a comunidade do vínculo vigente do Guerreiro(a) (`RF-01-73`,
    # `RN-01-57`).
    aula_id: uuid.UUID | None = None


@roteador.post("/sessoes/guerreiro", status_code=201)
def abrir_sessao_de_guerreiro(
    entrada: AbrirSessaoDeGuerreiroEntrada,
    contexto_da_chave: Annotated[ContextoDaChave, Depends(exigir_chave_de_aplicacao)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    configuracao: Annotated[Configuracao, Depends(obter_configuracao)],
) -> AberturaDeSessaoSaida:
    """Pública quanto à persona — dispensa credencial, nunca a chave de
    aplicação (`RF-01-04`, `RF-01-05`).

    **Com aula**, ela determina o ponto de apoio, e com ele o limiar
    (`RF-01-73`); aula de outra comunidade ou não vigente não alcança limiar
    algum, pelo mesmo laço que o registro de presença já aplica. **Sem aula** —
    a entrada de fora do encontro —, o limiar vem da comunidade do vínculo
    vigente do Guerreiro(a), e não há como o pedido alcançar comunidade alheia,
    porque a busca parte do vínculo dele (`RN-01-57`).

    A recusa não diferencia nick inexistente, Guerreiro(a) sem _template_,
    descritor que não confere, ponto de apoio sem limiar medido, aula que não
    vale para aquele Guerreiro(a), Guerreiro(a) sem vínculo vigente e
    comunidade sem nenhum limiar medido — nem no corpo nem, dentro de cada
    caminho, no tempo (`RN-01-22`, `RN-01-56`, `RN-01-57`).
    """
    guerreiro = autenticar_por_nick_e_descritor(
        sessao_bd,
        configuracao,
        nick=entrada.nick,
        descritor=entrada.descritor,
        aula=sessao_bd.get(Aula, entrada.aula_id) if entrada.aula_id is not None else None,
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
    # Exigido só no encontro — chave do App 01, Mestre ou Admin —; a App 05
    # segue sem PIN (`RF-01-06`, `RN-01-59`, design — decisão 4).
    pin: str | None = Field(default=None, pattern=r"^[0-9]{4}$")


@roteador.post("/sessoes/guerreiro/confirmacao", status_code=201)
def confirmar_sessao_de_guerreiro(
    entrada: ConfirmarSessaoDeGuerreiroEntrada,
    contexto: Annotated[
        ContextoDaSessao,
        Depends(
            exigir_qualquer_permissao(
                frozenset(
                    {
                        Operacao.confirmacao_de_identidade_do_guerreiro,
                        Operacao.confirmacao_de_identidade_dos_seus_guerreiros,
                    }
                ),
                "escreve",
            )
        ),
    ],
    contexto_da_chave: Annotated[ContextoDaChave, Depends(exigir_chave_de_aplicacao)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    configuracao: Annotated[Configuracao, Depends(obter_configuracao)],
) -> AberturaDeSessaoSaida:
    """Aberta a Mestre, Admin e **responsável** pela matriz (`RF-01-06`,
    `RF-01-74`, `RF-01-16`) — a alternativa equivalente para quem não tem
    _template_, para a falha de reconhecimento e para quem recusou a
    biometria (`RN-01-16`). Recebe o **nick**, nunca um identificador:
    resolvê-lo por uma rota de busca abriria o oráculo que `RN-01-22` veda
    para qualquer persona, adulto autenticado incluído.

    Mestre e Admin confirmam qualquer Guerreiro(a); o responsável, só os que
    estão sob a responsabilidade dele. As três recusas — nick inexistente,
    nick de outro papel e nick fora do alcance de quem confirma — são
    indistinguíveis no corpo e no tempo (`RN-01-22`, `RN-01-58`).
    """
    quem_confirma = sessao_bd.get(Persona, contexto.persona_id)
    # No encontro, confirma só quem abriu a sessão de trabalho, e só com o
    # próprio PIN — conferido antes do nick, para que a recusa de PIN nunca
    # revele se o nick existe (`RN-04-37`, `RN-01-59`, `RN-01-22`).
    if contexto_da_chave.aplicacao == APLICACAO_DO_ENCONTRO and quem_confirma.papel in (
        Papel.mestre,
        Papel.admin,
    ):
        if entrada.pin is None:
            raise ErroDeValidacao("O PIN de quem confirma é obrigatório.", campo="pin")
        conferir_pin_da_sessao(
            sessao_bd,
            persona=quem_confirma,
            sessao=sessao_bd.get(Sessao, contexto.sessao_id),
            pin=entrada.pin,
        )
    guerreiro = buscar_guerreiro_confirmavel_por(
        sessao_bd, nick=entrada.nick, quem_confirma=quem_confirma
    )
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
    divulgacao_autorizada: bool | None = None
    tem_pin_de_confirmacao: bool | None = None


@roteador.get("/eu", response_model_exclude_none=True)
def eu(
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> EuSaida:
    """`divulgacao_autorizada` só aparece para o Guerreiro(a) — derivado do
    mesmo histórico de consentimento que já vale para toda a plataforma, sem
    estado à parte e sem revelar quem decidiu (`RF-05-50`, `RN-05-14`,
    `RN-05-21`)."""
    matriz_do_papel = MATRIZ_DE_PERMISSOES[contexto.papel]
    divulgacao_autorizada = None
    if contexto.papel == Papel.guerreiro:
        divulgacao_autorizada = autorizacao_de_divulgacao_vigente(sessao_bd, contexto.persona_id)
    # Só para quem confirma no encontro: as telas das Apps 09 e 03 dizem se já
    # há PIN, sem nunca mostrá-lo (`RF-09-121`, `RF-02-110`, design — decisão 8).
    tem_pin_de_confirmacao = None
    if contexto.papel in (Papel.mestre, Papel.admin):
        persona = sessao_bd.get(Persona, contexto.persona_id)
        tem_pin_de_confirmacao = persona.pin_verificador is not None
    return EuSaida(
        persona_id=contexto.persona_id,
        papel=contexto.papel,
        permissoes={acesso: sorted(operacoes) for acesso, operacoes in matriz_do_papel.items()},
        divulgacao_autorizada=divulgacao_autorizada,
        tem_pin_de_confirmacao=tem_pin_de_confirmacao,
    )
