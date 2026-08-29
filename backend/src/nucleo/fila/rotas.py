import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, UploadFile
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import tuple_
from sqlalchemy.orm import Session

from ..armazenamento.fabrica import dependencia_de_armazenamento
from ..armazenamento.porta import PortaDeArmazenamento
from ..autenticacao import ContextoDaSessao, exigir_persona
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
    SituacaoDaSugestao,
    SolicitacaoDeChave,
    SolicitacaoDeDados,
    SolicitacaoDeParticipacao,
    SugestaoOuProposta,
    TipoDeAlvo,
)
from .regra import (
    avaliar_solicitacao_de_chave,
    avaliar_solicitacao_de_dados,
    avaliar_solicitacao_de_participacao,
    avaliar_sugestao,
    esta_em_atraso,
    liberar_conjunto_de_dados,
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


class SolicitacaoDeDadosSaida(BaseModel):
    """`RF-02-77`; `entregue` só existe depois da aprovação, pela guarda
    `liberar_conjunto_de_dados` (`RF-02-79`)."""

    id: uuid.UUID
    solicitante: str
    instituicao: str
    finalidade_declarada: str
    recorte_pedido: str
    situacao: SituacaoDaSolicitacao
    prazo: datetime
    em_atraso: bool
    avaliado_por_id: uuid.UUID | None
    parecer: str | None
    decidido_em: datetime | None
    entregue: str | None = None


def _saida_da_solicitacao_de_dados(solicitacao: SolicitacaoDeDados) -> SolicitacaoDeDadosSaida:
    return SolicitacaoDeDadosSaida(
        id=solicitacao.id,
        solicitante=solicitacao.solicitante,
        instituicao=solicitacao.instituicao,
        finalidade_declarada=solicitacao.finalidade_declarada,
        recorte_pedido=solicitacao.recorte_pedido,
        situacao=solicitacao.situacao,
        prazo=solicitacao.prazo,
        em_atraso=esta_em_atraso(solicitacao),
        avaliado_por_id=solicitacao.avaliado_por_id,
        parecer=solicitacao.parecer,
        decidido_em=solicitacao.decidido_em,
        entregue=solicitacao.entregue,
    )


@roteador.get("/solicitacoes-de-dados", response_model=PaginaDeResultado[SolicitacaoDeDadosSaida])
def listar_solicitacoes_de_dados_rota(
    parametros: Annotated[ParametrosDeListagem, Depends(contrato_de_listagem())],
    contexto: Annotated[ContextoDaSessao, Depends(exigir_permissao(Operacao.tudo, "le"))],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> PaginaDeResultado[SolicitacaoDeDadosSaida]:
    """Restrita a Admin (`RF-01-16`), no mesmo molde de paginação e atraso da
    fila de participação (`RF-02-77`, `RN-01-49`)."""
    consulta = sessao_bd.query(SolicitacaoDeDados)

    if parametros.cursor:
        posicao = decodificar_cursor(parametros.cursor)
        try:
            registrada_em_cursor = datetime.fromisoformat(posicao["registrado_em"])
            id_cursor = uuid.UUID(posicao["id"])
        except (KeyError, ValueError) as exc:
            raise ErroDeValidacao(mensagem="Cursor de paginação inválido.", campo="cursor") from exc
        consulta = consulta.filter(
            tuple_(SolicitacaoDeDados.registrado_em, SolicitacaoDeDados.id)
            > (registrada_em_cursor, id_cursor)
        )

    consulta = consulta.order_by(SolicitacaoDeDados.registrado_em, SolicitacaoDeDados.id)
    registros = consulta.limit(parametros.tamanho + 1).all()

    proximo_cursor = None
    if len(registros) > parametros.tamanho:
        registros = registros[: parametros.tamanho]
        ultimo = registros[-1]
        proximo_cursor = codificar_cursor(
            {"registrado_em": ultimo.registrado_em.isoformat(), "id": str(ultimo.id)}
        )

    return PaginaDeResultado(
        itens=[_saida_da_solicitacao_de_dados(registro) for registro in registros],
        proximo_cursor=proximo_cursor,
    )


class AvaliarSolicitacaoDeDadosEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    situacao: str = Field(min_length=1)
    parecer: str
    compromisso_de_nao_reidentificar: bool = False
    entregue: str | None = None


@roteador.post("/solicitacoes-de-dados/{id_da_solicitacao}/avaliacao")
def avaliar_solicitacao_de_dados_rota(
    id_da_solicitacao: uuid.UUID,
    entrada: AvaliarSolicitacaoDeDadosEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_permissao(Operacao.tudo, "escreve"))],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> SolicitacaoDeDadosSaida:
    """Restrita a Admin (`RF-02-78`, `RF-01-16`). O compromisso de não
    reidentificação é só transportado — quem exige é a regra (design —
    decisão 2). `entregue` só se aplica à aprovação, e passa pela guarda
    `liberar_conjunto_de_dados` antes de gravar (`RF-02-79`)."""
    solicitacao = sessao_bd.get(SolicitacaoDeDados, id_da_solicitacao)
    if solicitacao is None:
        raise NaoEncontrado(mensagem="Solicitação de dados não encontrada.")
    if solicitacao.decidido_em is not None:
        raise SolicitacaoJaAvaliada()

    try:
        situacao_valida = SituacaoDaSolicitacao(entrada.situacao)
    except ValueError as exc:
        raise ErroDeValidacao(
            mensagem="Desfecho precisa ser aceita ou recusada.", campo="situacao"
        ) from exc

    if entrada.entregue is not None and situacao_valida != SituacaoDaSolicitacao.aceita:
        raise ErroDeValidacao(
            mensagem="Só a solicitação aprovada registra o que foi entregue.", campo="entregue"
        )

    avaliador = sessao_bd.get(Persona, contexto.persona_id)
    solicitacao = avaliar_solicitacao_de_dados(
        sessao_bd,
        solicitacao,
        situacao=situacao_valida,
        avaliado_por=avaliador,
        parecer=entrada.parecer,
        compromisso_de_nao_reidentificar=entrada.compromisso_de_nao_reidentificar,
    )

    if entrada.entregue is not None:
        liberar_conjunto_de_dados(solicitacao)
        solicitacao.entregue = entrada.entregue
        sessao_bd.flush()

    sessao_bd.commit()
    return _saida_da_solicitacao_de_dados(solicitacao)


class SolicitacaoDeChaveSaida(BaseModel):
    """A leitura nunca traz o segredo (`RN-02-28`) — só se a chave já foi
    emitida a partir desta solicitação."""

    id: uuid.UUID
    solicitante: str
    contato: str
    instituicao: str | None
    o_que_pretende_construir: str
    situacao: SituacaoDaSolicitacao
    prazo: datetime
    em_atraso: bool
    avaliado_por_id: uuid.UUID | None
    parecer: str | None
    decidido_em: datetime | None
    chave_emitida: bool


def _saida_da_solicitacao_de_chave(solicitacao: SolicitacaoDeChave) -> SolicitacaoDeChaveSaida:
    return SolicitacaoDeChaveSaida(
        id=solicitacao.id,
        solicitante=solicitacao.solicitante,
        contato=solicitacao.contato,
        instituicao=solicitacao.instituicao,
        o_que_pretende_construir=solicitacao.o_que_pretende_construir,
        situacao=solicitacao.situacao,
        prazo=solicitacao.prazo,
        em_atraso=esta_em_atraso(solicitacao),
        avaliado_por_id=solicitacao.avaliado_por_id,
        parecer=solicitacao.parecer,
        decidido_em=solicitacao.decidido_em,
        chave_emitida=solicitacao.chave_id is not None,
    )


@roteador.get("/solicitacoes-de-chave", response_model=PaginaDeResultado[SolicitacaoDeChaveSaida])
def listar_solicitacoes_de_chave_rota(
    parametros: Annotated[ParametrosDeListagem, Depends(contrato_de_listagem())],
    contexto: Annotated[ContextoDaSessao, Depends(exigir_permissao(Operacao.tudo, "le"))],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> PaginaDeResultado[SolicitacaoDeChaveSaida]:
    """Restrita a Admin (`RF-01-16`, `RF-02-87`)."""
    consulta = sessao_bd.query(SolicitacaoDeChave)

    if parametros.cursor:
        posicao = decodificar_cursor(parametros.cursor)
        try:
            registrada_em_cursor = datetime.fromisoformat(posicao["registrado_em"])
            id_cursor = uuid.UUID(posicao["id"])
        except (KeyError, ValueError) as exc:
            raise ErroDeValidacao(mensagem="Cursor de paginação inválido.", campo="cursor") from exc
        consulta = consulta.filter(
            tuple_(SolicitacaoDeChave.registrado_em, SolicitacaoDeChave.id)
            > (registrada_em_cursor, id_cursor)
        )

    consulta = consulta.order_by(SolicitacaoDeChave.registrado_em, SolicitacaoDeChave.id)
    registros = consulta.limit(parametros.tamanho + 1).all()

    proximo_cursor = None
    if len(registros) > parametros.tamanho:
        registros = registros[: parametros.tamanho]
        ultimo = registros[-1]
        proximo_cursor = codificar_cursor(
            {"registrado_em": ultimo.registrado_em.isoformat(), "id": str(ultimo.id)}
        )

    return PaginaDeResultado(
        itens=[_saida_da_solicitacao_de_chave(registro) for registro in registros],
        proximo_cursor=proximo_cursor,
    )


class AvaliarSolicitacaoDeChaveEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    situacao: str = Field(min_length=1)
    parecer: str | None = None


@roteador.post("/solicitacoes-de-chave/{id_da_solicitacao}/avaliacao")
def avaliar_solicitacao_de_chave_rota(
    id_da_solicitacao: uuid.UUID,
    entrada: AvaliarSolicitacaoDeChaveEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_permissao(Operacao.tudo, "escreve"))],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> SolicitacaoDeChaveSaida:
    """Restrita a Admin (`RF-02-88`, `RF-01-16`). Só o desfecho — a emissão
    é ato separado, sobre solicitação aceita (`POST /chaves`), decisão do
    fundador em 2026-08-22 (design — decisão 1)."""
    solicitacao = sessao_bd.get(SolicitacaoDeChave, id_da_solicitacao)
    if solicitacao is None:
        raise NaoEncontrado(mensagem="Solicitação de chave não encontrada.")
    if solicitacao.decidido_em is not None:
        raise SolicitacaoJaAvaliada()

    try:
        situacao_valida = SituacaoDaSolicitacao(entrada.situacao)
    except ValueError as exc:
        raise ErroDeValidacao(
            mensagem="Desfecho precisa ser aceita ou recusada.", campo="situacao"
        ) from exc

    avaliador = sessao_bd.get(Persona, contexto.persona_id)
    solicitacao = avaliar_solicitacao_de_chave(
        sessao_bd,
        solicitacao,
        situacao=situacao_valida,
        avaliado_por=avaliador,
        parecer=entrada.parecer,
    )
    sessao_bd.commit()
    return _saida_da_solicitacao_de_chave(solicitacao)


class SugestaoSaida(BaseModel):
    """`RF-02-25`; `motivo_do_retorno` só existe na não adotada
    (`RF-02-26`)."""

    id: uuid.UUID
    autor_id: uuid.UUID
    papel_do_autor: str
    alvo_tipo: TipoDeAlvo
    alvo_id: uuid.UUID | None
    texto: str
    situacao: SituacaoDaSugestao
    prazo: datetime
    em_atraso: bool
    avaliado_por_id: uuid.UUID | None
    parecer: str | None
    motivo_do_retorno: str | None
    decidido_em: datetime | None


def _saida_da_sugestao(sugestao: SugestaoOuProposta) -> SugestaoSaida:
    return SugestaoSaida(
        id=sugestao.id,
        autor_id=sugestao.autor_id,
        papel_do_autor=sugestao.papel_do_autor,
        alvo_tipo=sugestao.alvo_tipo,
        alvo_id=sugestao.alvo_id,
        texto=sugestao.texto,
        situacao=sugestao.situacao,
        prazo=sugestao.prazo,
        em_atraso=esta_em_atraso(sugestao),
        avaliado_por_id=sugestao.avaliado_por_id,
        parecer=sugestao.parecer,
        motivo_do_retorno=sugestao.motivo_do_retorno,
        decidido_em=sugestao.decidido_em,
    )


@roteador.get("/sugestoes", response_model=PaginaDeResultado[SugestaoSaida])
def listar_sugestoes_rota(
    parametros: Annotated[ParametrosDeListagem, Depends(contrato_de_listagem())],
    contexto: Annotated[ContextoDaSessao, Depends(exigir_permissao(Operacao.tudo, "le"))],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> PaginaDeResultado[SugestaoSaida]:
    """Restrita a Admin (`RF-01-16`). Fila única das Apps 05, 07, 08 e 09 —
    todas gravam na mesma tabela (`RF-02-25`)."""
    consulta = sessao_bd.query(SugestaoOuProposta)

    if parametros.cursor:
        posicao = decodificar_cursor(parametros.cursor)
        try:
            registrada_em_cursor = datetime.fromisoformat(posicao["registrado_em"])
            id_cursor = uuid.UUID(posicao["id"])
        except (KeyError, ValueError) as exc:
            raise ErroDeValidacao(mensagem="Cursor de paginação inválido.", campo="cursor") from exc
        consulta = consulta.filter(
            tuple_(SugestaoOuProposta.registrado_em, SugestaoOuProposta.id)
            > (registrada_em_cursor, id_cursor)
        )

    consulta = consulta.order_by(SugestaoOuProposta.registrado_em, SugestaoOuProposta.id)
    registros = consulta.limit(parametros.tamanho + 1).all()

    proximo_cursor = None
    if len(registros) > parametros.tamanho:
        registros = registros[: parametros.tamanho]
        ultimo = registros[-1]
        proximo_cursor = codificar_cursor(
            {"registrado_em": ultimo.registrado_em.isoformat(), "id": str(ultimo.id)}
        )

    return PaginaDeResultado(
        itens=[_saida_da_sugestao(registro) for registro in registros],
        proximo_cursor=proximo_cursor,
    )


class AvaliarSugestaoEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    situacao: str = Field(min_length=1)
    parecer: str | None = None
    motivo_do_retorno: str | None = None


@roteador.post("/sugestoes/{id_da_sugestao}/avaliacao")
def avaliar_sugestao_rota(
    id_da_sugestao: uuid.UUID,
    entrada: AvaliarSugestaoEntrada,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_permissao(Operacao.tudo, "escreve"))],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> SugestaoSaida:
    """Restrita a Admin (`RF-02-26`, `RF-01-16`). O crédito dos 20 extras, o
    badge de protagonismo e a data de descarte da transcrição vêm da regra,
    não da rota (`RF-01-56`, `RN-01-50`)."""
    sugestao = sessao_bd.get(SugestaoOuProposta, id_da_sugestao)
    if sugestao is None:
        raise NaoEncontrado(mensagem="Sugestão ou proposta não encontrada.")
    if sugestao.decidido_em is not None:
        raise SolicitacaoJaAvaliada()

    try:
        situacao_valida = SituacaoDaSugestao(entrada.situacao)
    except ValueError as exc:
        raise ErroDeValidacao(
            mensagem="Desfecho precisa ser adotada ou não adotada.", campo="situacao"
        ) from exc

    avaliador = sessao_bd.get(Persona, contexto.persona_id)
    sugestao = avaliar_sugestao(
        sessao_bd,
        sugestao,
        situacao=situacao_valida,
        avaliado_por=avaliador,
        parecer=entrada.parecer,
        motivo_do_retorno=entrada.motivo_do_retorno,
    )
    sessao_bd.commit()
    return _saida_da_sugestao(sugestao)


class SugestaoDoAutorSaida(BaseModel):
    """Leitura de quem propôs, na própria plataforma — nunca o `parecer`
    interno da avaliação, que é só da leitura de Admin; o retorno chega pelo
    `motivo_do_retorno` (`RF-09-55`, `RN-02-25`, design — decisão 3)."""

    id: uuid.UUID
    alvo_tipo: TipoDeAlvo
    alvo_id: uuid.UUID | None
    texto: str
    situacao: SituacaoDaSugestao
    prazo: datetime
    em_atraso: bool
    motivo_do_retorno: str | None
    decidido_em: datetime | None


def _saida_da_sugestao_do_autor(sugestao: SugestaoOuProposta) -> SugestaoDoAutorSaida:
    return SugestaoDoAutorSaida(
        id=sugestao.id,
        alvo_tipo=sugestao.alvo_tipo,
        alvo_id=sugestao.alvo_id,
        texto=sugestao.texto,
        situacao=sugestao.situacao,
        prazo=sugestao.prazo,
        em_atraso=esta_em_atraso(sugestao),
        motivo_do_retorno=sugestao.motivo_do_retorno,
        decidido_em=sugestao.decidido_em,
    )


@roteador.get("/sugestoes/minhas", response_model=PaginaDeResultado[SugestaoDoAutorSaida])
def listar_minhas_sugestoes_rota(
    parametros: Annotated[ParametrosDeListagem, Depends(contrato_de_listagem())],
    contexto: Annotated[ContextoDaSessao, Depends(exigir_persona)],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> PaginaDeResultado[SugestaoDoAutorSaida]:
    """`RF-09-55`, `RF-01-25`: a persona em sessão acompanha as próprias
    sugestões e propostas na fila única, sem depender do Admin — nunca a de
    outro autor."""
    consulta = sessao_bd.query(SugestaoOuProposta).filter_by(autor_id=contexto.persona_id)

    if parametros.cursor:
        posicao = decodificar_cursor(parametros.cursor)
        try:
            registrada_em_cursor = datetime.fromisoformat(posicao["registrado_em"])
            id_cursor = uuid.UUID(posicao["id"])
        except (KeyError, ValueError) as exc:
            raise ErroDeValidacao(mensagem="Cursor de paginação inválido.", campo="cursor") from exc
        consulta = consulta.filter(
            tuple_(SugestaoOuProposta.registrado_em, SugestaoOuProposta.id)
            > (registrada_em_cursor, id_cursor)
        )

    consulta = consulta.order_by(SugestaoOuProposta.registrado_em, SugestaoOuProposta.id)
    registros = consulta.limit(parametros.tamanho + 1).all()

    proximo_cursor = None
    if len(registros) > parametros.tamanho:
        registros = registros[: parametros.tamanho]
        ultimo = registros[-1]
        proximo_cursor = codificar_cursor(
            {"registrado_em": ultimo.registrado_em.isoformat(), "id": str(ultimo.id)}
        )

    return PaginaDeResultado(
        itens=[_saida_da_sugestao_do_autor(registro) for registro in registros],
        proximo_cursor=proximo_cursor,
    )
