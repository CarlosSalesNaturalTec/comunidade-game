import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, UploadFile
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import tuple_
from sqlalchemy.orm import Session

from ..armazenamento.fabrica import dependencia_de_armazenamento
from ..armazenamento.porta import PortaDeArmazenamento
from ..autenticacao import ContextoDaSessao
from ..banco import obter_sessao
from ..erros import ErroDeValidacao, NaoEncontrado, SolicitacaoJaAvaliada
from ..paginacao import (
    PaginaDeResultado,
    ParametrosDeListagem,
    codificar_cursor,
    contrato_de_listagem,
    decodificar_cursor,
)
from ..permissoes import Operacao, exigir_permissao, exigir_qualquer_permissao
from ..personas.modelo import Persona
from ..protecao.freio import exigir_freio_por_origem
from .modelo import (
    PretensaoDeParticipacao,
    SituacaoDaSolicitacao,
    SolicitacaoDeParticipacao,
    TipoDeAlvo,
)
from .regra import (
    avaliar_solicitacao_de_participacao,
    esta_em_atraso,
    registrar_solicitacao_de_chave,
    registrar_solicitacao_de_dados,
    registrar_solicitacao_de_participacao,
    registrar_sugestao,
)

roteador = APIRouter()

# `RF-01-25`: as três operações de proposta das personas — todas levam à
# mesma rota de sugestão e proposta.
_OPERACOES_DE_SUGESTAO = frozenset(
    {
        Operacao.suas_sugestoes,
        Operacao.solicitacoes_e_propostas,
        Operacao.propostas_de_evolucao,
    }
)


class SolicitacaoSaida(BaseModel):
    """As três rotas de envio devolvem só o registro e o prazo — nunca
    dado, arquivo, chave ou acesso (`RN-01-03`, `RN-01-25`, `RN-01-37`)."""

    id: uuid.UUID
    prazo: datetime


@roteador.post("/solicitacoes-de-participacao", status_code=201)
def registrar_solicitacao_de_participacao_rota(
    nome_ou_razao_social: Annotated[str, Form()],
    email: Annotated[str, Form()],
    whatsapp: Annotated[str, Form()],
    pretensao: Annotated[PretensaoDeParticipacao, Form()],
    apresentacao: Annotated[str, Form()],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    armazenamento: Annotated[PortaDeArmazenamento, Depends(dependencia_de_armazenamento)],
    _freio: Annotated[None, Depends(exigir_freio_por_origem("formulario_participacao"))],
    instituicao: Annotated[str | None, Form()] = None,
    links: Annotated[str | None, Form()] = None,
    nick: Annotated[str | None, Form()] = None,
    aporte_declarado: Annotated[str | None, Form()] = None,
    comprovante: Annotated[UploadFile | None, File()] = None,
) -> SolicitacaoSaida:
    """Pública, sem credencial de persona (`RF-01-25`, design — Decisions).
    O pré-cadastro do Apoiador entra aqui, com aporte declarado, comprovante
    e o nick pretendido; nenhum caminho cria cadastro (`RN-01-03`,
    `RN-01-28`, `RF-14-13`)."""
    conteudo = comprovante.file.read() if comprovante is not None else None
    solicitacao = registrar_solicitacao_de_participacao(
        sessao_bd,
        nome_ou_razao_social=nome_ou_razao_social,
        email=email,
        whatsapp=whatsapp,
        pretensao=pretensao,
        apresentacao=apresentacao,
        instituicao=instituicao,
        links=links,
        nick=nick,
        aporte_declarado=aporte_declarado,
        comprovante_conteudo=conteudo,
        comprovante_nome_original=comprovante.filename if comprovante is not None else None,
        comprovante_tipo=comprovante.content_type if comprovante is not None else None,
        armazenamento=armazenamento,
    )
    sessao_bd.commit()
    return SolicitacaoSaida(id=solicitacao.id, prazo=solicitacao.prazo)


class SolicitacaoDeParticipacaoSaida(BaseModel):
    """Leitura e desfecho compartilham a mesma forma de saída. O aporte
    declarado, o nick pretendido e a indicação de comprovante só se aplicam
    à pretensão de Apoiador; o conteúdo do arquivo nunca sai daqui
    (`RN-01-28`)."""

    id: uuid.UUID
    nome_ou_razao_social: str
    email: str
    whatsapp: str
    pretensao: PretensaoDeParticipacao
    apresentacao: str
    instituicao: str | None
    links: str | None
    situacao: SituacaoDaSolicitacao
    prazo: datetime
    em_atraso: bool
    avaliado_por_id: uuid.UUID | None
    parecer: str | None
    decidido_em: datetime | None
    nick: str | None = None
    aporte_declarado: str | None = None
    comprovante_anexado: bool = False


def _saida_da_solicitacao_de_participacao(
    solicitacao: SolicitacaoDeParticipacao,
) -> SolicitacaoDeParticipacaoSaida:
    eh_apoiador = solicitacao.pretensao == PretensaoDeParticipacao.apoiador
    return SolicitacaoDeParticipacaoSaida(
        id=solicitacao.id,
        nome_ou_razao_social=solicitacao.nome_ou_razao_social,
        email=solicitacao.email,
        whatsapp=solicitacao.whatsapp,
        pretensao=solicitacao.pretensao,
        apresentacao=solicitacao.apresentacao,
        instituicao=solicitacao.instituicao,
        links=solicitacao.links,
        situacao=solicitacao.situacao,
        prazo=solicitacao.prazo,
        em_atraso=esta_em_atraso(solicitacao),
        avaliado_por_id=solicitacao.avaliado_por_id,
        parecer=solicitacao.parecer,
        decidido_em=solicitacao.decidido_em,
        nick=solicitacao.nick if eh_apoiador else None,
        aporte_declarado=solicitacao.aporte_declarado if eh_apoiador else None,
        comprovante_anexado=eh_apoiador and solicitacao.comprovante_referencia is not None,
    )


@roteador.get(
    "/solicitacoes-de-participacao",
    response_model=PaginaDeResultado[SolicitacaoDeParticipacaoSaida],
)
def listar_solicitacoes_de_participacao_rota(
    parametros: Annotated[ParametrosDeListagem, Depends(contrato_de_listagem())],
    contexto: Annotated[ContextoDaSessao, Depends(exigir_permissao(Operacao.tudo, "le"))],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> PaginaDeResultado[SolicitacaoDeParticipacaoSaida]:
    """Restrita a Admin (`RF-01-16`). Sem filtro de comunidade — a
    solicitação chega antes de qualquer vínculo (design — decisão 1).
    Ordenada da mais antiga para a mais recente, para que o atraso apareça
    no topo (design — decisão 2)."""
    consulta = sessao_bd.query(SolicitacaoDeParticipacao)

    if parametros.cursor:
        posicao = decodificar_cursor(parametros.cursor)
        try:
            registrada_em_cursor = datetime.fromisoformat(posicao["registrado_em"])
            id_cursor = uuid.UUID(posicao["id"])
        except (KeyError, ValueError) as exc:
            raise ErroDeValidacao(mensagem="Cursor de paginação inválido.", campo="cursor") from exc
        consulta = consulta.filter(
            tuple_(SolicitacaoDeParticipacao.registrado_em, SolicitacaoDeParticipacao.id)
            > (registrada_em_cursor, id_cursor)
        )

    consulta = consulta.order_by(
        SolicitacaoDeParticipacao.registrado_em, SolicitacaoDeParticipacao.id
    )
    registros = consulta.limit(parametros.tamanho + 1).all()

    proximo_cursor = None
    if len(registros) > parametros.tamanho:
        registros = registros[: parametros.tamanho]
        ultimo = registros[-1]
        proximo_cursor = codificar_cursor(
            {"registrado_em": ultimo.registrado_em.isoformat(), "id": str(ultimo.id)}
        )

    return PaginaDeResultado(
        itens=[_saida_da_solicitacao_de_participacao(registro) for registro in registros],
        proximo_cursor=proximo_cursor,
    )


class AvaliarSolicitacaoDeParticipacaoEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    situacao: str = Field(min_length=1)
    parecer: str | None = None


@roteador.post("/solicitacoes-de-participacao/{id_da_solicitacao}/avaliacao")
def avaliar_solicitacao_de_participacao_rota(
    id_da_solicitacao: uuid.UUID,
    entrada: AvaliarSolicitacaoDeParticipacaoEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_permissao(Operacao.tudo, "escreve"))],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> SolicitacaoDeParticipacaoSaida:
    """Restrita a Admin (`RF-02-19`, `RF-01-16`). Nenhum cadastro, persona
    ou acesso nasce daqui (`RN-01-03`, `RN-01-28`); a guarda de reavaliação
    fica aqui, e não na regra, para não alcançar as outras três naturezas
    da fila (design — decisão 3)."""
    solicitacao = sessao_bd.get(SolicitacaoDeParticipacao, id_da_solicitacao)
    if solicitacao is None:
        raise NaoEncontrado(mensagem="Solicitação de participação não encontrada.")
    if solicitacao.decidido_em is not None:
        raise SolicitacaoJaAvaliada()

    try:
        situacao_valida = SituacaoDaSolicitacao(entrada.situacao)
    except ValueError as exc:
        raise ErroDeValidacao(
            mensagem="Desfecho precisa ser aceita ou recusada.", campo="situacao"
        ) from exc

    avaliador = sessao_bd.get(Persona, contexto.persona_id)
    solicitacao = avaliar_solicitacao_de_participacao(
        sessao_bd,
        solicitacao,
        situacao=situacao_valida,
        avaliado_por=avaliador,
        parecer=entrada.parecer,
    )
    sessao_bd.commit()
    return _saida_da_solicitacao_de_participacao(solicitacao)


class SolicitacaoDeDadosEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    solicitante: str = Field(min_length=1)
    instituicao: str = Field(min_length=1)
    email: str = Field(min_length=1)
    finalidade_declarada: str = Field(min_length=1)
    recorte_pedido: str = Field(min_length=1)


@roteador.post("/solicitacoes-de-dados", status_code=201)
def registrar_solicitacao_de_dados_rota(
    entrada: SolicitacaoDeDadosEntrada,
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    _freio: Annotated[None, Depends(exigir_freio_por_origem("formulario_dados"))],
) -> SolicitacaoSaida:
    """Pública, sem credencial de persona (`RF-01-46`). Sem finalidade
    declarada, o núcleo recusa o registro."""
    solicitacao = registrar_solicitacao_de_dados(
        sessao_bd,
        solicitante=entrada.solicitante,
        instituicao=entrada.instituicao,
        email=entrada.email,
        finalidade_declarada=entrada.finalidade_declarada,
        recorte_pedido=entrada.recorte_pedido,
    )
    sessao_bd.commit()
    return SolicitacaoSaida(id=solicitacao.id, prazo=solicitacao.prazo)


class SolicitacaoDeChaveEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    solicitante: str = Field(min_length=1)
    contato: str = Field(min_length=1)
    o_que_pretende_construir: str = Field(min_length=1)
    instituicao: str | None = None


@roteador.post("/solicitacoes-de-chave", status_code=201)
def registrar_solicitacao_de_chave_rota(
    entrada: SolicitacaoDeChaveEntrada,
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> SolicitacaoSaida:
    """Pública, sem credencial de persona (`RF-01-49`). Sem freio por
    origem — nova solicitação é sempre possível (`RN-01-46`) —, protegida
    só pela cota da chave da aplicação que chama."""
    solicitacao = registrar_solicitacao_de_chave(
        sessao_bd,
        solicitante=entrada.solicitante,
        contato=entrada.contato,
        o_que_pretende_construir=entrada.o_que_pretende_construir,
        instituicao=entrada.instituicao,
    )
    sessao_bd.commit()
    return SolicitacaoSaida(id=solicitacao.id, prazo=solicitacao.prazo)


class SugestaoEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    alvo_tipo: TipoDeAlvo
    texto: str = Field(min_length=1)
    alvo_id: uuid.UUID | None = None


@roteador.post("/sugestoes", status_code=201)
def registrar_sugestao_rota(
    entrada: SugestaoEntrada,
    contexto: Annotated[
        ContextoDaSessao, Depends(exigir_qualquer_permissao(_OPERACOES_DE_SUGESTAO, "escreve"))
    ],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> SolicitacaoSaida:
    """Autenticada — recusa com 401 quem não tem credencial de persona
    (`RF-01-03`). Só texto: não há campo de áudio (03 §12.2)."""
    autor = sessao_bd.get(Persona, contexto.persona_id)
    sugestao = registrar_sugestao(
        sessao_bd,
        autor=autor,
        alvo_tipo=entrada.alvo_tipo,
        texto=entrada.texto,
        alvo_id=entrada.alvo_id,
    )
    sessao_bd.commit()
    return SolicitacaoSaida(id=sugestao.id, prazo=sugestao.prazo)
