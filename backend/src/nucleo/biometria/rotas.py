import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from ..aulas.modelo import Aula
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
from .regra import (
    consultar_estado_da_biometria,
    consultar_limiares_por_ponto_de_apoio,
    gravar_medicao_do_limiar,
    gravar_ou_recadastrar_template,
)

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


class GravarMedicaoDoLimiarEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    aula_id: uuid.UUID
    distancias_do_piso: list[float] = Field(min_length=1)
    distancias_do_teto: list[float] = Field(min_length=1)
    pessoas_no_teto: int = Field(ge=1)


class MedicaoDoLimiarSaida(BaseModel):
    id: uuid.UUID
    ponto_de_apoio_id: uuid.UUID
    limiar: float
    distancias_do_piso: list[float]
    distancias_do_teto: list[float]
    pessoas_no_teto: int
    medido_por: uuid.UUID
    registrado_em: datetime


@roteador.post("/medicoes-do-limiar", status_code=201)
def gravar_medicao_do_limiar_rota(
    entrada: GravarMedicaoDoLimiarEntrada,
    contexto: Annotated[
        ContextoDaSessao,
        Depends(exigir_permissao(Operacao.medicao_do_limiar_do_ponto_de_apoio, "escreve")),
    ],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> MedicaoDoLimiarSaida:
    """Restrita a Mestre e Admin pela matriz (`RF-01-16`). Recebe a **aula em
    curso** — é ela que determina o ponto de apoio — e as duas séries de
    **distâncias**; `extra="forbid"` recusa descritor no corpo (`RF-01-73`,
    `RF-04-66`, `RN-01-15`, design — decisão 3).

    O **limiar não vem do aparelho**: o núcleo o calcula das séries, pela
    mesma fórmula que a bancada mostra a quem confirma (`RN-04-35`).
    """
    aula = sessao_bd.get(Aula, entrada.aula_id)
    if aula is None:
        raise NaoEncontrado(mensagem="Aula não encontrada.", campo="aula_id")

    operado_por = sessao_bd.get(Persona, contexto.persona_id)
    medicao = gravar_medicao_do_limiar(
        sessao_bd,
        ponto_de_apoio_id=aula.ponto_de_apoio_id,
        distancias_do_piso=entrada.distancias_do_piso,
        distancias_do_teto=entrada.distancias_do_teto,
        pessoas_no_teto=entrada.pessoas_no_teto,
        operado_por=operado_por,
    )
    sessao_bd.commit()
    return MedicaoDoLimiarSaida(
        id=medicao.id,
        ponto_de_apoio_id=medicao.ponto_de_apoio_id,
        limiar=medicao.limiar,
        distancias_do_piso=medicao.distancias_do_piso,
        distancias_do_teto=medicao.distancias_do_teto,
        pessoas_no_teto=medicao.pessoas_no_teto,
        medido_por=medicao.autor_id,
        registrado_em=medicao.registrado_em,
    )


class LimiarDoPontoDeApoioSaida(BaseModel):
    """O `medicao` é nulo no ponto de apoio que ainda não foi medido — e é
    exatamente esse caso que a App 03 destaca, porque ali o reconhecimento
    não confere ninguém (`RF-02-109`, `RN-01-56`)."""

    ponto_de_apoio_id: uuid.UUID
    nome: str
    medicao: MedicaoDoLimiarSaida | None


@roteador.get("/pontos-de-apoio/limiares")
def listar_limiares_dos_pontos_de_apoio(
    contexto: Annotated[
        ContextoDaSessao,
        Depends(exigir_permissao(Operacao.medicao_do_limiar_do_ponto_de_apoio, "le")),
    ],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> list[LimiarDoPontoDeApoioSaida]:
    """A consulta da App 03: o limiar vigente de cada ponto de apoio, com a
    origem da medição, e quem ainda não tem (`RF-02-109`). Não existe rota de
    edição — corrigir é medir de novo na App 01 (`RF-04-66`).
    """
    return [
        LimiarDoPontoDeApoioSaida(
            ponto_de_apoio_id=ponto.id,
            nome=ponto.nome,
            medicao=(
                MedicaoDoLimiarSaida(
                    id=medicao.id,
                    ponto_de_apoio_id=medicao.ponto_de_apoio_id,
                    limiar=medicao.limiar,
                    distancias_do_piso=medicao.distancias_do_piso,
                    distancias_do_teto=medicao.distancias_do_teto,
                    pessoas_no_teto=medicao.pessoas_no_teto,
                    medido_por=medicao.autor_id,
                    registrado_em=medicao.registrado_em,
                )
                if medicao is not None
                else None
            ),
        )
        for ponto, medicao in consultar_limiares_por_ponto_de_apoio(sessao_bd)
    ]
