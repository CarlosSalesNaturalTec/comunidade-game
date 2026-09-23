from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from ..autenticacao import ContextoDaSessao
from ..banco import obter_sessao
from ..chaves.conferencia import ContextoDaChave, exigir_chave_de_aplicacao
from ..configuracao import Configuracao, obter_configuracao
from ..erros import PermissaoNegada, PinNaoCadastrado
from ..permissoes import Operacao, exigir_permissao
from ..personas.modelo import Persona
from .regra import cadastrar_pin

roteador = APIRouter()

APLICACAO_DO_ENCONTRO = "app-01-aula-presencial"

# O PIN serve a um ato só — confirmar a identidade do Guerreiro(a) no
# encontro —, e quem o tem é quem a matriz deixa confirmar: Mestre e Admin.
# O responsável confirma por outra operação, com escopo, e sem PIN (`RF-01-74`).
_exigir_quem_confirma = exigir_permissao(Operacao.confirmacao_de_identidade_do_guerreiro, "escreve")


class CadastroDoPinEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    pin: str = Field(pattern=r"^[0-9]{4}$")


@roteador.put("/eu/pin-de-confirmacao", status_code=204)
def cadastrar_pin_rota(
    entrada: CadastroDoPinEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(_exigir_quem_confirma)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    configuracao: Annotated[Configuracao, Depends(obter_configuracao)],
) -> None:
    """Cadastra ou troca o próprio PIN; o núcleo guarda só o verificador, e
    a resposta não devolve nada (`RF-01-75`, `RF-09-121`, `RF-02-110`)."""
    persona = sessao_bd.get(Persona, contexto.persona_id)
    cadastrar_pin(persona, entrada.pin, configuracao)
    sessao_bd.commit()


class VerificadorDoPinSaida(BaseModel):
    algoritmo: str
    iteracoes: int
    sal: str
    resumo: str


@roteador.get("/eu/pin-de-confirmacao/verificador")
def ler_verificador_rota(
    contexto_da_chave: Annotated[ContextoDaChave, Depends(exigir_chave_de_aplicacao)],
    contexto: Annotated[ContextoDaSessao, Depends(_exigir_quem_confirma)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> VerificadorDoPinSaida:
    """Só a chave do App 01 recebe o verificador — é lá que a confirmação
    sem rede acontece —, e só o da própria persona da sessão de trabalho
    (`RN-04-38`, design — decisão 7)."""
    if contexto_da_chave.aplicacao != APLICACAO_DO_ENCONTRO:
        raise PermissaoNegada(mensagem="O verificador do PIN só é entregue à App 01.")
    persona = sessao_bd.get(Persona, contexto.persona_id)
    if persona.pin_verificador is None:
        raise PinNaoCadastrado()
    return VerificadorDoPinSaida(**persona.pin_verificador)
