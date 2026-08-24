import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from ..autenticacao import ContextoDaSessao
from ..banco import obter_sessao
from ..configuracao import Configuracao, obter_configuracao
from ..erros import NaoEncontrado
from ..permissoes import Operacao, exigir_permissao
from ..personas.modelo import Papel, Persona
from .modelo import DecisaoDeConsentimento, OrigemDoConsentimento
from .regra import registrar_consentimento

roteador = APIRouter()


class RegistrarConsentimentoEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    responsavel_id: uuid.UUID
    guerreiro_id: uuid.UUID
    # `tipo` fica como texto: `registrar_consentimento` já converte para o
    # conjunto fechado e devolve a mensagem e o campo que a spec exige
    # (`RN-13-05`, `RN-13-06`). `decisao` e `origem` validam aqui mesmo, pelo
    # próprio tipo do Pydantic.
    tipo: str
    decisao: DecisaoDeConsentimento
    origem: OrigemDoConsentimento
    testemunha_id: uuid.UUID | None = None


class ConsentimentoSaida(BaseModel):
    id: uuid.UUID
    registrado_em: datetime


@roteador.post("/consentimentos", status_code=201)
def registrar_consentimento_rota(
    entrada: RegistrarConsentimentoEntrada,
    contexto: Annotated[
        ContextoDaSessao,
        Depends(exigir_permissao(Operacao.testemunho_do_termo_impresso, "escreve")),
    ],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    configuracao: Annotated[Configuracao, Depends(obter_configuracao)],
) -> ConsentimentoSaida:
    """Restrita a Admin e Mestre pela matriz — o testemunho do termo impresso
    assinado por um terceiro, distinto do consentimento que o próprio
    responsável dá na App 07 (`RF-01-19`, `RF-04-12`, `RN-01-12`, design —
    decisão 3). A versão do termo é carimbada pela configuração vigente; a
    rota nunca a recebe do cliente (design — decisão 2).
    """
    responsavel = sessao_bd.get(Persona, entrada.responsavel_id)
    if responsavel is None or responsavel.papel != Papel.responsavel:
        raise NaoEncontrado(mensagem="Responsável não encontrado.", campo="responsavel_id")

    operado_por = sessao_bd.get(Persona, contexto.persona_id)
    consentimento = registrar_consentimento(
        sessao_bd,
        responsavel=responsavel,
        guerreiro_id=entrada.guerreiro_id,
        tipo=entrada.tipo,
        versao_do_termo=configuracao.consentimento_versao_vigente_do_termo,
        decisao=entrada.decisao,
        origem=entrada.origem,
        operado_por=operado_por,
        testemunha_id=entrada.testemunha_id,
    )
    sessao_bd.commit()
    return ConsentimentoSaida(id=consentimento.id, registrado_em=consentimento.registrado_em)
