import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Response
from pydantic import BaseModel
from sqlalchemy import tuple_
from sqlalchemy.orm import Session

from ..armazenamento.fabrica import dependencia_de_armazenamento
from ..armazenamento.porta import PortaDeArmazenamento
from ..banco import obter_sessao
from ..comunidades.modelo import ComunidadeVirtual
from ..configuracao import Configuracao, obter_configuracao
from ..criacoes_originais.modelo import (
    CriacaoOriginal,
)
from ..cuidado_do_bem.modelo import RegistroDeCustomizacao
from ..erros import ErroDeValidacao, NaoEncontrado
from ..ods.regra import cobertura_por_comunidade, comunidades_com_cobertura
from ..paginacao import (
    PaginaDeResultado,
    ParametrosDeListagem,
    codificar_cursor,
    contrato_de_listagem,
    decodificar_cursor,
)
from ..personas.modelo import Papel
from ..poderes.modelo import Poder
from ..pontuacao.regra import consulta_de_ranking
from ..protecao.freio import exigir_freio_por_origem
from ..trilhas.modelo import DesbloqueioDaMissao, SituacaoDaTrilha, Trilha
from .publico import (
    AvatarENickSaida,
    CartaPublicaDeApoiadorSaida,
    CartaPublicaDeGuerreiroSaida,
    CartaPublicaDeMestreSaida,
    CriacaoPublicaSaida,
    MestreResponsavelSaida,
    buscar_adulto_publico,
    buscar_persona_guerreiro_publica_por_nick,
    condicoes_de_comprovacao_publica,
    condicoes_de_criacao_publica,
    condicoes_de_customizacao_publica,
    mestres_responsaveis_por_poder,
    montar_cartas_de_apoiador,
    montar_cartas_de_mestre,
    montar_cartas_publicas,
    montar_itens_do_acervo,
    paginar_apoiadores_publicos,
    paginar_cartas_publicas,
    paginar_mestres_publicos,
)

roteador = APIRouter()


def _analisar_comunidade(valor: str | None) -> uuid.UUID | None:
    if not valor:
        return None
    try:
        return uuid.UUID(valor)
    except ValueError as exc:
        raise ErroDeValidacao(
            mensagem="Filtro 'comunidade' precisa ser um identificador válido.",
            campo="comunidade",
        ) from exc


@roteador.get("/vitrine/guerreiros", response_model=PaginaDeResultado[CartaPublicaDeGuerreiroSaida])
def listar_guerreiros_publicos(
    parametros: Annotated[ParametrosDeListagem, Depends(contrato_de_listagem())],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> PaginaDeResultado[CartaPublicaDeGuerreiroSaida]:
    """Cards de quem tem autorização vigente, cada um com a **carta inteira**
    do documento 11 §8.2, paginado e filtrável por comunidade (`RF-01-02`,
    `RF-01-28`, `RF-03-02`, `RF-03-04`, `RF-03-05`, `RN-01-10`, `RN-01-11`).
    A composição sai na própria listagem: montá-la com uma consulta por nick
    para cada card cairia no freio por origem (`RF-01-65`)."""
    comunidade_id = _analisar_comunidade(parametros.filtros.get("comunidade"))
    return paginar_cartas_publicas(
        sessao_bd,
        comunidade_id=comunidade_id,
        cursor=parametros.cursor,
        tamanho=parametros.tamanho,
    )


@roteador.get(
    "/vitrine/guerreiros/{nick}",
    response_model=CartaPublicaDeGuerreiroSaida,
    dependencies=[Depends(exigir_freio_por_origem("consulta_por_nick"))],
)
def perfil_publico_de_guerreiro(
    nick: str,
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> CartaPublicaDeGuerreiroSaida:
    """Perfil por nick exato, na **mesma** composição do card (`RF-03-03`,
    `RF-03-05`); nick inexistente e nick sem autorização devolvem o mesmo
    404, resolvidos na mesma consulta (`RF-01-33`, `RF-01-34`, `RN-01-22`,
    `RF-01-65`)."""
    persona = buscar_persona_guerreiro_publica_por_nick(sessao_bd, nick)
    if persona is None:
        raise NaoEncontrado(mensagem="Guerreiro(a) não encontrado(a).")

    return montar_cartas_publicas(sessao_bd, [(persona, nick)])[0]


class ItemDeRankingSaida(AvatarENickSaida):
    pontos_regulares: int
    posicao: int


@roteador.get("/vitrine/rankings", response_model=PaginaDeResultado[ItemDeRankingSaida])
def ranking_publico(
    parametros: Annotated[ParametrosDeListagem, Depends(contrato_de_listagem())],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> PaginaDeResultado[ItemDeRankingSaida]:
    """Ordena por ponto regular; a posição é calculada sobre o conjunto já
    filtrado pelo portão da divulgação, de modo que quem não autorizou não
    abre buraco na numeração (`RF-01-21`, `RF-01-28`, `RN-01-10`). A
    derivação é a mesma que `pontuacao.regra.consulta_de_ranking` usa para o
    ranking logado da turma — este ranking sempre exige o portão da
    divulgação (design — Decisions)."""
    comunidade_id = _analisar_comunidade(parametros.filtros.get("comunidade"))

    base = consulta_de_ranking(sessao_bd, exigir_divulgacao=True, comunidade_id=comunidade_id)

    subquery = base.subquery()
    consulta = sessao_bd.query(*subquery.c).order_by(subquery.c.posicao)

    if parametros.cursor:
        posicao_do_cursor = decodificar_cursor(parametros.cursor)
        try:
            ultima_posicao = int(posicao_do_cursor["posicao"])
        except (KeyError, ValueError) as exc:
            raise ErroDeValidacao(mensagem="Cursor de paginação inválido.", campo="cursor") from exc
        consulta = consulta.filter(subquery.c.posicao > ultima_posicao)

    linhas = consulta.limit(parametros.tamanho + 1).all()

    proximo_cursor = None
    if len(linhas) > parametros.tamanho:
        linhas = linhas[: parametros.tamanho]
        proximo_cursor = codificar_cursor({"posicao": linhas[-1].posicao})

    itens = [
        ItemDeRankingSaida(
            avatar=linha.avatar,
            nick=linha.nick,
            pontos_regulares=linha.total,
            posicao=linha.posicao,
        )
        for linha in linhas
    ]
    return PaginaDeResultado(itens=itens, proximo_cursor=proximo_cursor)


class TrilhaPublicaSaida(BaseModel):
    id: uuid.UUID
    nome: str


class PoderPublicoSaida(BaseModel):
    id: uuid.UUID
    nome: str
    descricao: str
    trilhas: list[TrilhaPublicaSaida]
    # Os Mestres responsáveis do documento 11 §8.2, que a fatia 2 deixou de
    # fora por não haver rota de Mestre. Poder sem trilha publicada sai com a
    # lista **vazia**, nunca omitida (`RF-03-02`).
    mestres_responsaveis: list[MestreResponsavelSaida]


@roteador.get("/vitrine/poderes", response_model=list[PoderPublicoSaida])
def listar_poderes_publicos(
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> list[PoderPublicoSaida]:
    """Poderes ativos com as trilhas publicadas vinculadas a cada um; a
    trilha nunca é filtrada por comunidade, bem comum da plataforma
    (`RF-01-62`, `RN-01-42`)."""
    poderes = sessao_bd.query(Poder).filter_by(ativo=True).order_by(Poder.nome).all()
    mestres = mestres_responsaveis_por_poder(sessao_bd, [poder.id for poder in poderes])
    saida: list[PoderPublicoSaida] = []
    for poder in poderes:
        trilhas = (
            sessao_bd.query(Trilha)
            .filter_by(poder_id=poder.id, situacao=SituacaoDaTrilha.publicada)
            .order_by(Trilha.nome)
            .all()
        )
        saida.append(
            PoderPublicoSaida(
                id=poder.id,
                nome=poder.nome,
                descricao=poder.descricao,
                trilhas=[TrilhaPublicaSaida(id=trilha.id, nome=trilha.nome) for trilha in trilhas],
                mestres_responsaveis=mestres.get(poder.id, []),
            )
        )
    return saida


@roteador.get("/vitrine/mestres", response_model=PaginaDeResultado[CartaPublicaDeMestreSaida])
def listar_mestres_publicos(
    parametros: Annotated[ParametrosDeListagem, Depends(contrato_de_listagem())],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> PaginaDeResultado[CartaPublicaDeMestreSaida]:
    """Cards de Mestre, cada um com a **carta inteira** do documento 11 §8.2,
    para que a página individual não custe uma consulta por card (`RF-03-02`,
    `RF-03-07`). Sem token de sessão e sem freio por origem próprio: a cota
    por faixa da chave é o que cobre a navegação por card — o freio é da
    superfície de busca (`RF-01-02`, `RN-03-01`)."""
    return paginar_mestres_publicos(sessao_bd, cursor=parametros.cursor, tamanho=parametros.tamanho)


@roteador.get("/vitrine/mestres/{mestre_id}", response_model=CartaPublicaDeMestreSaida)
def pagina_publica_de_mestre(
    mestre_id: uuid.UUID,
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> CartaPublicaDeMestreSaida:
    """A página individual, na **mesma** composição do card (`RF-03-03`). Por
    identificador, e não por nick: o nick é opcional para adulto, e por nick
    ficaria sem página quem ainda não o definiu. Persona de outro papel e
    identificador inexistente recebem o mesmo 404 (`RN-03-01`)."""
    persona = buscar_adulto_publico(
        sessao_bd, persona_id=mestre_id, papel=Papel.mestre, apenas_com_aporte=False
    )
    if persona is None:
        raise NaoEncontrado(mensagem="Mestre não encontrado.")
    return montar_cartas_de_mestre(sessao_bd, [persona])[0]


@roteador.get("/vitrine/apoiadores", response_model=PaginaDeResultado[CartaPublicaDeApoiadorSaida])
def listar_apoiadores_publicos(
    parametros: Annotated[ParametrosDeListagem, Depends(contrato_de_listagem())],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> PaginaDeResultado[CartaPublicaDeApoiadorSaida]:
    """Cards de Apoiador. Só entra quem tem **aporte homologado**
    (`RF-03-57`), o total sai em moedas (`RF-03-10`, `RN-03-18`) e a ordem é
    a estável do cursor — **nunca** por valor aportado, que pódio de apoiador
    é proibido (`RN-14-38`)."""
    return paginar_apoiadores_publicos(
        sessao_bd, cursor=parametros.cursor, tamanho=parametros.tamanho
    )


@roteador.get("/vitrine/apoiadores/{apoiador_id}", response_model=CartaPublicaDeApoiadorSaida)
def pagina_publica_de_apoiador(
    apoiador_id: uuid.UUID,
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> CartaPublicaDeApoiadorSaida:
    """A página individual, na mesma composição do card (`RF-03-03`).
    Apoiador sem aporte homologado, persona de outro papel e identificador
    inexistente recebem **o mesmo 404** (`RF-03-57`, `RN-03-01`)."""
    persona = buscar_adulto_publico(
        sessao_bd, persona_id=apoiador_id, papel=Papel.apoiador, apenas_com_aporte=True
    )
    if persona is None:
        raise NaoEncontrado(mensagem="Apoiador não encontrado.")
    return montar_cartas_de_apoiador(sessao_bd, [persona])[0]


@roteador.get("/vitrine/criacoes/{id_da_criacao}/arquivo")
def ler_arquivo_publico_da_criacao(
    id_da_criacao: uuid.UUID,
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    armazenamento: Annotated[PortaDeArmazenamento, Depends(dependencia_de_armazenamento)],
) -> Response:
    """Os bytes da mídia da criação pública, sob o **mesmo** portão da
    listagem — `condicoes_de_criacao_publica`, e não uma segunda cópia da
    regra que possa divergir dela (`RF-01-81`, `RN-01-63`).

    Até aqui o portão protegia **quem aparece na lista**, não quem serve o
    arquivo. A recusa é **404 em todos os casos** — criação inexistente,
    ainda não validada ou com creditado sem autorização —, para a rota não
    virar oráculo sobre quais crianças têm divulgação autorizada
    (`RN-01-22`). Sem freio, como a listagem irmã."""
    criacao = (
        sessao_bd.query(CriacaoOriginal)
        .filter(CriacaoOriginal.id == id_da_criacao)
        .filter(*condicoes_de_criacao_publica(sessao_bd))
        .first()
    )
    if criacao is None or criacao.referencia is None:
        raise NaoEncontrado(mensagem="Criação original não encontrada.")
    return Response(
        content=armazenamento.ler(referencia=criacao.referencia),
        media_type=criacao.tipo_do_arquivo or "application/octet-stream",
    )


@roteador.get("/vitrine/comprovacoes/{id_da_comprovacao}/arquivo")
def ler_arquivo_publico_da_comprovacao(
    id_da_comprovacao: uuid.UUID,
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    armazenamento: Annotated[PortaDeArmazenamento, Depends(dependencia_de_armazenamento)],
) -> Response:
    """Os bytes da comprovação do desafio prático em público, sob o **mesmo**
    portão da listagem — `condicoes_de_comprovacao_publica`, e não uma segunda
    cópia da regra que possa divergir dela (`RF-03-85`, `RN-03-41`,
    `RN-01-63`, design — decisão 5).

    A recusa é **404 em todos os casos** — comprovação inexistente, não
    julgada, julgada não cumprida, julgada não publicável ou de Guerreiro(a)
    sem autorização vigente —, para a rota não virar oráculo sobre quais
    crianças têm divulgação autorizada (`RN-01-22`). Sem freio, como a
    listagem irmã.
    """
    comprovacao = (
        sessao_bd.query(DesbloqueioDaMissao)
        .filter(DesbloqueioDaMissao.id == id_da_comprovacao)
        .filter(*condicoes_de_comprovacao_publica(sessao_bd))
        .first()
    )
    if comprovacao is None or comprovacao.comprovacao_referencia is None:
        raise NaoEncontrado(mensagem="Comprovação não encontrada.")
    return Response(
        content=armazenamento.ler(referencia=comprovacao.comprovacao_referencia),
        media_type=comprovacao.comprovacao_tipo_do_arquivo or "application/octet-stream",
    )


@roteador.get("/vitrine/customizacoes/{id_do_registro}/arquivo")
def ler_arquivo_publico_da_customizacao(
    id_do_registro: uuid.UUID,
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    armazenamento: Annotated[PortaDeArmazenamento, Depends(dependencia_de_armazenamento)],
) -> Response:
    """Os bytes da customização do kit em público, sob o **mesmo** portão da
    listagem — `condicoes_de_customizacao_publica` —, e 404 em toda recusa,
    como a comprovação irmã (`RF-03-88`, `RN-03-41`)."""
    registro = (
        sessao_bd.query(RegistroDeCustomizacao)
        .filter(RegistroDeCustomizacao.id == id_do_registro)
        .filter(*condicoes_de_customizacao_publica(sessao_bd))
        .first()
    )
    if registro is None or registro.midia_referencia is None:
        raise NaoEncontrado(mensagem="Customização não encontrada.")
    return Response(
        content=armazenamento.ler(referencia=registro.midia_referencia),
        media_type=registro.midia_tipo_do_arquivo or "application/octet-stream",
    )


def _posicao_do_acervo(cursor: str) -> tuple[datetime, uuid.UUID]:
    """A posição do keyset do acervo, `(data de aprovação, id)` descendente.

    A chave é `aprovado_em`, porque a data vem de duas fontes — a validação da
    criação e o julgamento da comprovação. A chave antiga, `validado_em`,
    **continua aceita**: o cursor é opaco, e quem estivesse no meio da
    paginação na implantação receberia 422 numa seção pública (design —
    decisão 2).

    O cursor **não** marca a fonte: o `id` é UUID, único entre as duas
    tabelas, e a tupla já ordena (design — decisão 1).
    """
    posicao = decodificar_cursor(cursor)
    try:
        bruto = posicao.get("aprovado_em") or posicao["validado_em"]
        return datetime.fromisoformat(bruto), uuid.UUID(posicao["id"])
    except (KeyError, ValueError) as exc:
        raise ErroDeValidacao(mensagem="Cursor de paginação inválido.", campo="cursor") from exc


@roteador.get("/vitrine/criacoes", response_model=PaginaDeResultado[CriacaoPublicaSaida])
def listar_criacoes_publicas(
    parametros: Annotated[ParametrosDeListagem, Depends(contrato_de_listagem())],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> PaginaDeResultado[CriacaoPublicaSaida]:
    """O **acervo** público: a criação da culminância validada e a comprovação
    do desafio prático julgada cumprida e publicável, nas duas sob o portão de
    autorização de divulgação (`RF-01-26`, `RN-01-13`, `RN-01-10`,
    `RF-03-84`, `RN-03-41`).

    A ordem é **decrescente** pela data em que o Mestre aprovou o item, do
    mais recente para o mais antigo, e o keyset acompanha: o cursor desce
    (`RF-03-83`, decisão do fundador, 2026-10-11).

    Cada fonte roda a consulta dela com o **mesmo** recorte de cursor e
    `tamanho + 1` itens; a junção é em memória, por `(data, id)`. É correto
    porque item além do `tamanho + 1`-ésimo de uma fonte nunca cabe entre os
    `tamanho` primeiros da união (design — decisão 1).
    """
    posicao = _posicao_do_acervo(parametros.cursor) if parametros.cursor else None
    teto = parametros.tamanho + 1

    criacoes_bd = sessao_bd.query(CriacaoOriginal).filter(*condicoes_de_criacao_publica(sessao_bd))
    if posicao is not None:
        criacoes_bd = criacoes_bd.filter(
            tuple_(CriacaoOriginal.validado_em, CriacaoOriginal.id) < posicao
        )
    criacoes = (
        criacoes_bd.order_by(CriacaoOriginal.validado_em.desc(), CriacaoOriginal.id.desc())
        .limit(teto)
        .all()
    )

    comprovacoes_bd = sessao_bd.query(DesbloqueioDaMissao).filter(
        *condicoes_de_comprovacao_publica(sessao_bd)
    )
    if posicao is not None:
        comprovacoes_bd = comprovacoes_bd.filter(
            tuple_(DesbloqueioDaMissao.julgado_em, DesbloqueioDaMissao.id) < posicao
        )
    comprovacoes = (
        comprovacoes_bd.order_by(
            DesbloqueioDaMissao.julgado_em.desc(), DesbloqueioDaMissao.id.desc()
        )
        .limit(teto)
        .all()
    )

    customizacoes_bd = sessao_bd.query(RegistroDeCustomizacao).filter(
        *condicoes_de_customizacao_publica(sessao_bd)
    )
    if posicao is not None:
        customizacoes_bd = customizacoes_bd.filter(
            tuple_(RegistroDeCustomizacao.julgado_em, RegistroDeCustomizacao.id) < posicao
        )
    customizacoes = (
        customizacoes_bd.order_by(
            RegistroDeCustomizacao.julgado_em.desc(), RegistroDeCustomizacao.id.desc()
        )
        .limit(teto)
        .all()
    )

    acervo = [
        (item.validada_em, item.id, item)
        for item, _ in montar_itens_do_acervo(sessao_bd, criacoes, comprovacoes, customizacoes)
    ]

    proximo_cursor = None
    if len(acervo) > parametros.tamanho:
        acervo = acervo[: parametros.tamanho]
        aprovado_em, id_do_item, _ = acervo[-1]
        proximo_cursor = codificar_cursor(
            {"aprovado_em": aprovado_em.isoformat(), "id": str(id_do_item)}
        )

    return PaginaDeResultado(itens=[item for _, _, item in acervo], proximo_cursor=proximo_cursor)


class CoberturaPublicaSaida(BaseModel):
    comunidade_id: uuid.UUID
    comunidade_nome: str
    objetivos: list[int]
    ciclo: str


@roteador.get("/vitrine/ods/cobertura", response_model=list[CoberturaPublicaSaida])
def cobertura_publica_de_ods(
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    configuracao: Annotated[Configuracao, Depends(obter_configuracao)],
) -> list[CoberturaPublicaSaida]:
    """Cobertura agregada por comunidade e ciclo; nenhum recorte por
    Guerreiro(a) existe nesta rota (`RF-01-43`, `RN-01-24`)."""
    saida: list[CoberturaPublicaSaida] = []
    for comunidade_id in comunidades_com_cobertura(sessao_bd):
        comunidade = sessao_bd.get(ComunidadeVirtual, comunidade_id)
        objetivos = cobertura_por_comunidade(sessao_bd, comunidade_id)
        saida.append(
            CoberturaPublicaSaida(
                comunidade_id=comunidade_id,
                comunidade_nome=comunidade.nome,
                objetivos=sorted(objetivos),
                ciclo=configuracao.ciclo_rotulo,
            )
        )
    return saida
