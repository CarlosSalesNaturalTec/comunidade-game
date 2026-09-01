import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from ..autenticacao import ContextoDaSessao
from ..banco import obter_sessao
from ..configuracao import Configuracao, obter_configuracao
from ..consentimentos.modelo import DecisaoDeConsentimento
from ..consentimentos.regra import recusar_biometria
from ..erros import NaoEncontrado
from ..permissoes import Operacao, exigir_permissao
from ..personas.modelo import Papel, Persona
from ..responsaveis.regra import exigir_vinculo_do_responsavel
from .modelo import GatilhoDeApagamento
from .regra import consultar_estado_da_biometria, gravar_ou_recadastrar_template

roteador = APIRouter()


class GravarDescritorEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    descritor: list[float] = Field(min_length=1)


class GravarDescritorSaida(BaseModel):
    guerreiro_id: uuid.UUID
    gravado_em: datetime


@roteador.post("/guerreiros/{id}/descritor", status_code=201)
def gravar_descritor(
    id: uuid.UUID,
    entrada: GravarDescritorEntrada,
    contexto: Annotated[
        ContextoDaSessao,
        Depends(exigir_permissao(Operacao.cadastro_biometrico_do_guerreiro, "escreve")),
    ],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    configuracao: Annotated[Configuracao, Depends(obter_configuracao)],
) -> GravarDescritorSaida:
    """Restrita a Mestre e Admin pela matriz (`RF-01-05`, `RF-01-07`,
    `RF-01-08`, `RF-01-16`). A mesma rota grava e recadastra; nenhuma das
    duas respostas devolve o descritor ou o _template_ (`RN-01-14`).
    """
    guerreiro = sessao_bd.get(Persona, id)
    if guerreiro is None or guerreiro.papel != Papel.guerreiro:
        raise NaoEncontrado(mensagem="Guerreiro(a) não encontrado.", campo="id")

    operado_por = sessao_bd.get(Persona, contexto.persona_id)
    credencial = gravar_ou_recadastrar_template(
        sessao_bd,
        configuracao,
        guerreiro=guerreiro,
        descritor=entrada.descritor,
        operado_por=operado_por,
    )
    sessao_bd.commit()
    return GravarDescritorSaida(guerreiro_id=guerreiro.id, gravado_em=credencial.criada_em)


class RecusarBiometriaSaida(BaseModel):
    guerreiro_id: uuid.UUID
    apagar_em: datetime | None


@roteador.post("/eu/guerreiros/{id}/biometria/recusa", status_code=201)
def recusar_biometria_rota(
    id: uuid.UUID,
    contexto: Annotated[
        ContextoDaSessao, Depends(exigir_permissao(Operacao.consentimentos, "escreve"))
    ],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    configuracao: Annotated[Configuracao, Depends(obter_configuracao)],
) -> RecusarBiometriaSaida:
    """Restrita ao responsável em sessão, com o vínculo vigente exigido na
    própria regra — sem vínculo, 403 sem revelar dado algum (`RF-13-27`,
    `RN-13-04`). A rota nunca aceita concessão: só a recusa.
    """
    responsavel = sessao_bd.get(Persona, contexto.persona_id)
    _consentimento, apagar_em = recusar_biometria(
        sessao_bd,
        responsavel=responsavel,
        guerreiro_id=id,
        versao_do_termo=configuracao.consentimento_versao_vigente_do_termo,
    )
    sessao_bd.commit()
    return RecusarBiometriaSaida(guerreiro_id=id, apagar_em=apagar_em)


class EstadoDaBiometriaSaida(BaseModel):
    tem_template: bool
    decisao_do_termo: DecisaoDeConsentimento | None
    apagar_em: datetime | None
    gatilho_do_apagamento: GatilhoDeApagamento | None


@roteador.get("/eu/guerreiros/{id}/biometria")
def ler_estado_da_biometria_rota(
    id: uuid.UUID,
    contexto: Annotated[
        ContextoDaSessao,
        Depends(exigir_permissao(Operacao.guerreiros_sob_sua_responsabilidade, "le")),
    ],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> EstadoDaBiometriaSaida:
    """Restrita ao responsável, e ao vínculo vigente com o Guerreiro(a)
    pedido (`RF-13-27`, `RF-13-44`, `RN-13-04`). A resposta nunca contém o
    descritor nem o _template_.
    """
    exigir_vinculo_do_responsavel(
        sessao_bd, papel=contexto.papel, responsavel_id=contexto.persona_id, guerreiro_id=id
    )
    estado = consultar_estado_da_biometria(sessao_bd, guerreiro_id=id)
    return EstadoDaBiometriaSaida(
        tem_template=estado.tem_template,
        decisao_do_termo=estado.decisao_do_termo,
        apagar_em=estado.apagar_em,
        gatilho_do_apagamento=estado.gatilho_do_apagamento,
    )
