import uuid
from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import Subquery, tuple_
from sqlalchemy.orm import Session, aliased

from ..coletas.modelo import DesafioDeColeta
from ..comunidades.regra import resolver_vinculo_na_data
from ..erros import ErroDeValidacao, NaoEncontrado, PermissaoNegada
from ..paginacao import PaginaDeResultado, codificar_cursor, decodificar_cursor
from ..personas.modelo import Papel, Persona
from ..tempo import agora
from ..trilhas.modelo import Missao, Trilha
from ..trilhas.regra import conferir_posse_da_trilha
from .modelo import (
    ORDEM_DOS_NIVEIS,
    Local,
    NivelDoLocal,
    SituacaoDaSolicitacaoDeLocal,
    SolicitacaoDeLocal,
)


class LocalSaida(BaseModel):
    id: uuid.UUID
    comunidade_virtual_id: uuid.UUID
    nivel: str
    rotulo: str
    local_pai_id: uuid.UUID | None


class SolicitacaoDeLocalSaida(BaseModel):
    id: uuid.UUID
    solicitante_id: uuid.UUID
    comunidade_virtual_id: uuid.UUID
    desafio_de_coleta_id: uuid.UUID
    nivel_pretendido: str
    rotulo: str
    justificativa: str
    situacao: str
    avaliador_id: uuid.UUID | None
    motivo_da_recusa: str | None
    local_criado_id: uuid.UUID | None
    avaliado_em: datetime | None
    registrado_em: datetime


def cadastrar_local(
    sessao: Session,
    *,
    operador: Persona,
    comunidade_id: uuid.UUID | None,
    nivel: str | None,
    rotulo: str | None,
    local_pai_id: uuid.UUID | None,
) -> Local:
    """Só Admin cadastra local diretamente — a segunda origem é a
    aprovação de solicitação, por `_criar_local_validado` (`RF-08-04`,
    `RN-08-18`)."""
    if operador.papel != Papel.admin:
        raise PermissaoNegada(mensagem="Só o Admin cadastra local.")
    return _criar_local_validado(
        sessao,
        comunidade_id=comunidade_id,
        nivel=nivel,
        rotulo=rotulo,
        local_pai_id=local_pai_id,
    )


def _criar_local_validado(
    sessao: Session,
    *,
    comunidade_id: uuid.UUID | None,
    nivel: str | None,
    rotulo: str | None,
    local_pai_id: uuid.UUID | None,
) -> Local:
    """Núcleo de validação da hierarquia, sem opinião sobre quem chama — o
    portão de autorização é de cada origem (`cadastrar_local` e a
    aprovação de `SolicitacaoDeLocal`), nunca daqui (design — Decisions).
    O pai precisa ser do nível imediatamente acima e da mesma comunidade;
    só o nível `comunidade` dispensa pai.
    """
    if comunidade_id is None:
        raise ErroDeValidacao(mensagem="Local exige uma comunidade.", campo="comunidade_id")
    if not rotulo or not rotulo.strip():
        raise ErroDeValidacao(mensagem="Local exige rótulo.", campo="rotulo")

    try:
        nivel_valido = NivelDoLocal(nivel)
    except ValueError as exc:
        raise ErroDeValidacao(mensagem="Nível fora dos valores previstos.", campo="nivel") from exc

    indice = ORDEM_DOS_NIVEIS.index(nivel_valido)
    if nivel_valido == NivelDoLocal.comunidade:
        if local_pai_id is not None:
            raise ErroDeValidacao(
                mensagem="O nível 'comunidade' não tem local pai.", campo="local_pai_id"
            )
    else:
        if local_pai_id is None:
            raise ErroDeValidacao(mensagem="Local exige o local pai.", campo="local_pai_id")

        pai = sessao.get(Local, local_pai_id)
        if pai is None:
            raise ErroDeValidacao(mensagem="Local pai não encontrado.", campo="local_pai_id")
        if pai.comunidade_virtual_id != comunidade_id:
            raise ErroDeValidacao(
                mensagem="Local pai precisa ser da mesma comunidade.", campo="local_pai_id"
            )
        nivel_esperado_do_pai = ORDEM_DOS_NIVEIS[indice - 1]
        if pai.nivel != nivel_esperado_do_pai:
            raise ErroDeValidacao(
                mensagem=f"O nível imediatamente acima de '{nivel_valido.value}' é "
                f"'{nivel_esperado_do_pai.value}'.",
                campo="local_pai_id",
            )

    local = Local(
        comunidade_virtual_id=comunidade_id,
        nivel=nivel_valido,
        rotulo=rotulo,
        local_pai_id=local_pai_id,
    )
    sessao.add(local)
    sessao.flush()
    return local


def paginar_locais(
    sessao: Session,
    *,
    comunidade_id: uuid.UUID,
    cursor: str | None,
    tamanho: int,
) -> PaginaDeResultado[LocalSaida]:
    """Listagem paginada, sempre filtrada por comunidade (`RF-01-18`,
    `RF-01-28`) — nenhum local de outra comunidade entra na página."""
    consulta = sessao.query(Local).filter(Local.comunidade_virtual_id == comunidade_id)

    if cursor:
        posicao = decodificar_cursor(cursor)
        try:
            criado_em_cursor = datetime.fromisoformat(posicao["criado_em"])
            id_cursor = uuid.UUID(posicao["id"])
        except (KeyError, ValueError) as exc:
            raise ErroDeValidacao(mensagem="Cursor de paginação inválido.", campo="cursor") from exc
        consulta = consulta.filter(
            tuple_(Local.criado_em, Local.id) > (criado_em_cursor, id_cursor)
        )

    consulta = consulta.order_by(Local.criado_em, Local.id).limit(tamanho + 1)
    locais = consulta.all()

    proximo_cursor = None
    if len(locais) > tamanho:
        locais = locais[:tamanho]
        ultimo = locais[-1]
        proximo_cursor = codificar_cursor(
            {"criado_em": ultimo.criado_em.isoformat(), "id": str(ultimo.id)}
        )

    itens = [
        LocalSaida(
            id=local.id,
            comunidade_virtual_id=local.comunidade_virtual_id,
            nivel=local.nivel.value,
            rotulo=local.rotulo,
            local_pai_id=local.local_pai_id,
        )
        for local in locais
    ]
    return PaginaDeResultado(itens=itens, proximo_cursor=proximo_cursor)


def resolver_locais_publicados(sessao: Session, *, comunidade_id: uuid.UUID) -> Subquery:
    """Subconsulta que mapeia cada local da comunidade ao seu **local
    publicado** — o ancestral de nível bairro, ou a própria comunidade
    quando o local já está nela (`RN-08-13`, design — Decisions).

    CTE recursiva sobre `local_pai_id`, podada pela comunidade: a recursão
    para assim que alcança bairro ou comunidade, de modo que cada local
    produz exatamente uma linha de saída — nunca duas, nunca nenhuma
    (design — Decisions, Riscos).
    """
    ancestrais = (
        sessao.query(
            Local.id.label("local_id"),
            Local.id.label("ancestral_id"),
            Local.nivel.label("ancestral_nivel"),
            Local.local_pai_id.label("proximo_pai_id"),
        )
        .filter(Local.comunidade_virtual_id == comunidade_id)
        .cte(name="ancestrais_do_local", recursive=True)
    )

    proximo = aliased(Local)
    passo_recursivo = (
        sessao.query(
            ancestrais.c.local_id,
            proximo.id.label("ancestral_id"),
            proximo.nivel.label("ancestral_nivel"),
            proximo.local_pai_id.label("proximo_pai_id"),
        )
        .join(proximo, proximo.id == ancestrais.c.proximo_pai_id)
        .filter(
            ancestrais.c.ancestral_nivel != NivelDoLocal.bairro.value,
            ancestrais.c.ancestral_nivel != NivelDoLocal.comunidade.value,
        )
    )
    cte = ancestrais.union_all(passo_recursivo)

    return (
        sessao.query(
            cte.c.local_id.label("local_id"),
            cte.c.ancestral_id.label("local_publicado_id"),
        )
        .filter(
            cte.c.ancestral_nivel.in_([NivelDoLocal.bairro.value, NivelDoLocal.comunidade.value])
        )
        .subquery()
    )


def _trilha_do_desafio(sessao: Session, desafio: DesafioDeColeta) -> Trilha:
    """A trilha nunca é declarada pelo solicitante nem pelo avaliador: é
    alcançada por `missao_id` → `trilha_id`, o mesmo caminho que a emissão
    da credencial de dispositivo já percorre (design — Context)."""
    missao = sessao.get(Missao, desafio.missao_id)
    return sessao.get(Trilha, missao.trilha_id)


def solicitar_local(
    sessao: Session,
    *,
    operador: Persona,
    desafio: DesafioDeColeta | None,
    comunidade_id: uuid.UUID | None,
    nivel: str | None,
    rotulo: str | None,
    justificativa: str | None,
) -> SolicitacaoDeLocal:
    """Ato do Guerreiro(a): a comunidade da solicitação é sempre a vigente
    do solicitante, e apontar outra é recusado com 403, não silenciosamente
    substituída (`RF-08-22`, `RN-08-02`). O pedido em si NEVER cria local
    (`RN-08-18`)."""
    if operador.papel != Papel.guerreiro:
        raise PermissaoNegada(mensagem="Só o Guerreiro(a) solicita novo local.")
    if desafio is None:
        raise ErroDeValidacao(
            mensagem="Solicitação de local exige um desafio de coleta.",
            campo="desafio_de_coleta_id",
        )

    vinculo = resolver_vinculo_na_data(sessao, guerreiro_id=operador.id, data=agora())
    if vinculo is None or comunidade_id != vinculo.comunidade_virtual_id:
        raise PermissaoNegada(
            mensagem="A solicitação só pode apontar a comunidade vigente do solicitante."
        )

    if not rotulo or not rotulo.strip():
        raise ErroDeValidacao(mensagem="Solicitação de local exige rótulo.", campo="rotulo")
    if not justificativa or not justificativa.strip():
        raise ErroDeValidacao(
            mensagem="Solicitação de local exige justificativa.", campo="justificativa"
        )
    try:
        nivel_valido = NivelDoLocal(nivel)
    except ValueError as exc:
        raise ErroDeValidacao(mensagem="Nível fora dos valores previstos.", campo="nivel") from exc

    solicitacao = SolicitacaoDeLocal(
        solicitante_id=operador.id,
        comunidade_virtual_id=vinculo.comunidade_virtual_id,
        desafio_de_coleta_id=desafio.id,
        nivel_pretendido=nivel_valido,
        rotulo=rotulo,
        justificativa=justificativa,
        situacao=SituacaoDaSolicitacaoDeLocal.recebida,
    )
    sessao.add(solicitacao)
    sessao.flush()
    return solicitacao


def avaliar_solicitacao_de_local(
    sessao: Session,
    solicitacao: SolicitacaoDeLocal | None,
    *,
    operador: Persona,
    situacao: SituacaoDaSolicitacaoDeLocal | None,
    local_pai_id: uuid.UUID | None = None,
    motivo: str | None = None,
) -> SolicitacaoDeLocal:
    """Avalia o Admin ou o Mestre autor da trilha do desafio de origem —
    `conferir_posse_da_trilha` recusa qualquer outro com 403, inclusive o
    próprio Guerreiro(a) solicitante (`RF-08-23`). A hierarquia é validada
    por `_criar_local_validado`, o mesmo núcleo do cadastro direto, antes de
    qualquer escrita do desfecho: pai inválido recusa com 422 e deixa a
    solicitação em aberto, sem avaliador nem data gravados (`RF-08-04`,
    design — Decisions). Solicitação já aprovada ou recusada não se
    reavalia.
    """
    if solicitacao is None:
        raise NaoEncontrado(mensagem="Solicitação de local não encontrada.")

    desafio = sessao.get(DesafioDeColeta, solicitacao.desafio_de_coleta_id)
    trilha = _trilha_do_desafio(sessao, desafio)
    conferir_posse_da_trilha(trilha, operador)

    if solicitacao.situacao != SituacaoDaSolicitacaoDeLocal.recebida:
        raise ErroDeValidacao(mensagem="Esta solicitação já foi avaliada.", campo="situacao")
    if situacao not in (
        SituacaoDaSolicitacaoDeLocal.aprovada,
        SituacaoDaSolicitacaoDeLocal.recusada,
    ):
        raise ErroDeValidacao(
            mensagem="Desfecho precisa ser aprovada ou recusada.", campo="situacao"
        )

    if situacao == SituacaoDaSolicitacaoDeLocal.aprovada:
        local = _criar_local_validado(
            sessao,
            comunidade_id=solicitacao.comunidade_virtual_id,
            nivel=solicitacao.nivel_pretendido.value,
            rotulo=solicitacao.rotulo,
            local_pai_id=local_pai_id,
        )
        solicitacao.local_criado_id = local.id
    else:
        if not motivo or not motivo.strip():
            raise ErroDeValidacao(mensagem="A recusa exige motivo.", campo="motivo")
        solicitacao.motivo_da_recusa = motivo

    solicitacao.situacao = situacao
    solicitacao.avaliador_id = operador.id
    solicitacao.avaliado_em = agora()
    sessao.flush()
    return solicitacao


def listar_solicitacoes_de_local_abertas(
    sessao: Session,
    *,
    operador: Persona,
    comunidade_id: uuid.UUID,
    cursor: str | None,
    tamanho: int,
) -> PaginaDeResultado[SolicitacaoDeLocalSaida]:
    """O Admin vê todas as solicitações em aberto da comunidade filtrada; o
    Mestre, só as dos desafios das suas trilhas — um caminho só, com um
    predicado a mais para o Mestre, pela mesma junção desafio → missão →
    trilha da avaliação (`RF-08-24`, `RF-01-18`, design — Decisions).
    Solicitação já avaliada NEVER aparece aqui.
    """
    if operador.papel not in (Papel.admin, Papel.mestre):
        raise PermissaoNegada(
            mensagem="Só Admin ou Mestre veem as solicitações de local em aberto."
        )

    consulta = sessao.query(SolicitacaoDeLocal).filter(
        SolicitacaoDeLocal.comunidade_virtual_id == comunidade_id,
        SolicitacaoDeLocal.situacao == SituacaoDaSolicitacaoDeLocal.recebida,
    )
    if operador.papel == Papel.mestre:
        consulta = (
            consulta.join(
                DesafioDeColeta, DesafioDeColeta.id == SolicitacaoDeLocal.desafio_de_coleta_id
            )
            .join(Missao, Missao.id == DesafioDeColeta.missao_id)
            .join(Trilha, Trilha.id == Missao.trilha_id)
            .filter(Trilha.autor_id == operador.id)
        )

    if cursor:
        posicao = decodificar_cursor(cursor)
        try:
            registrado_em_cursor = datetime.fromisoformat(posicao["registrado_em"])
            id_cursor = uuid.UUID(posicao["id"])
        except (KeyError, ValueError) as exc:
            raise ErroDeValidacao(mensagem="Cursor de paginação inválido.", campo="cursor") from exc
        consulta = consulta.filter(
            tuple_(SolicitacaoDeLocal.registrado_em, SolicitacaoDeLocal.id)
            > (registrado_em_cursor, id_cursor)
        )

    consulta = consulta.order_by(SolicitacaoDeLocal.registrado_em, SolicitacaoDeLocal.id).limit(
        tamanho + 1
    )
    solicitacoes = consulta.all()

    proximo_cursor = None
    if len(solicitacoes) > tamanho:
        solicitacoes = solicitacoes[:tamanho]
        ultima = solicitacoes[-1]
        proximo_cursor = codificar_cursor(
            {"registrado_em": ultima.registrado_em.isoformat(), "id": str(ultima.id)}
        )

    itens = [
        SolicitacaoDeLocalSaida(
            id=solicitacao.id,
            solicitante_id=solicitacao.solicitante_id,
            comunidade_virtual_id=solicitacao.comunidade_virtual_id,
            desafio_de_coleta_id=solicitacao.desafio_de_coleta_id,
            nivel_pretendido=solicitacao.nivel_pretendido.value,
            rotulo=solicitacao.rotulo,
            justificativa=solicitacao.justificativa,
            situacao=solicitacao.situacao.value,
            avaliador_id=solicitacao.avaliador_id,
            motivo_da_recusa=solicitacao.motivo_da_recusa,
            local_criado_id=solicitacao.local_criado_id,
            avaliado_em=solicitacao.avaliado_em,
            registrado_em=solicitacao.registrado_em,
        )
        for solicitacao in solicitacoes
    ]
    return PaginaDeResultado(itens=itens, proximo_cursor=proximo_cursor)
