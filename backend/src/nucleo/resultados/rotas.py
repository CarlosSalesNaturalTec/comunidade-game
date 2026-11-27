import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from ..armazenamento.fabrica import dependencia_de_armazenamento
from ..armazenamento.porta import PortaDeArmazenamento
from ..aulas.modelo import Aula
from ..autenticacao import ContextoDaSessao
from ..banco import obter_sessao
from ..permissoes import Operacao, exigir_permissao
from ..personas.modelo import Nick, Persona
from ..tempo import DataHoraComFuso
from ..trilhas.modelo import Atividade
from .modelo import Resultado
from .regra import (
    ComprovanteDeclarado,
    JulgamentoDeclarado,
    ResultadoDaEquipe,
    ResultadoDeclarado,
    abrir_envio_do_comprovante,
    lancar_resultados_da_atividade,
    ler_arquivo_do_comprovante,
    listar_resultados_da_aula,
)

roteador = APIRouter()


class ComprovanteCorpo(BaseModel):
    """O comprovante do participante (`RF-09-149`): texto e link no corpo;
    imagem, áudio, vídeo e arquivo pelo `envio_id` do envio já concluído
    (design — decisão 2)."""

    model_config = ConfigDict(extra="forbid")

    tipo: str
    texto: str | None = None
    envio_id: uuid.UUID | None = None


class JulgamentoDoPraticoCorpo(BaseModel):
    """Os dois vereditos e o motivo do prático da missão, no mesmo envio do
    lançamento (`RF-09-150`, `RF-09-133`, `RF-09-134`)."""

    model_config = ConfigDict(extra="forbid")

    cumpriu: bool
    publicavel: bool = False
    motivo: str | None = None


class ParticipanteDoLancamentoCorpo(BaseModel):
    model_config = ConfigDict(extra="forbid")

    guerreiro_id: uuid.UUID
    momento_do_fato: DataHoraComFuso
    # A produção em texto segue aceita — é a App 03 —, e vale como comprovante
    # em texto; a App 09 manda `comprovante` (design — decisão 3).
    producao: str | None = None
    comprovante: ComprovanteCorpo | None = None
    julgamento_do_pratico: JulgamentoDoPraticoCorpo | None = None
    desfecho: str


class EquipeDoLancamentoCorpo(BaseModel):
    """O lançamento **da equipe da aula**: um desfecho e uma produção só,
    que valem igualmente a cada integrante presente (`RF-02-112`,
    `RN-02-32`)."""

    model_config = ConfigDict(extra="forbid")

    equipe_id: uuid.UUID
    momento_do_fato: DataHoraComFuso
    producao: str = Field(min_length=1)
    desfecho: str


class LancarResultadosDaAtividadeEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    aula_id: uuid.UUID
    participantes: list[ParticipanteDoLancamentoCorpo] = Field(default_factory=list)
    equipe: EquipeDoLancamentoCorpo | None = None
    """A equipe é alternativa à lista de participantes, nunca companhia
    dela — a recusa das duas e a de nenhuma são da regra (`RN-02-33`)."""


class ResultadoSaida(BaseModel):
    id: uuid.UUID
    guerreiro_id: uuid.UUID
    atividade_id: uuid.UUID
    aula_id: uuid.UUID
    momento_do_fato: DataHoraComFuso
    producao: str | None
    comprovante_tipo: str
    desfecho: str


class LancamentoDaAtividadeSaida(BaseModel):
    """Os Resultados gravados e quem ficou de fora por não ter presença na
    aula — é por essa lista que a tela diz quem não recebeu (`RF-02-112`,
    `RN-02-32`)."""

    resultados: list[ResultadoSaida]
    fora_por_falta_de_presenca: list[uuid.UUID]


def _saida(resultado: Resultado) -> ResultadoSaida:
    return ResultadoSaida(
        id=resultado.id,
        guerreiro_id=resultado.guerreiro_id,
        atividade_id=resultado.atividade_id,
        aula_id=resultado.aula_id,
        momento_do_fato=resultado.momento_do_fato,
        producao=resultado.producao,
        comprovante_tipo=resultado.comprovante_tipo.value,
        desfecho=resultado.desfecho.value,
    )


@roteador.post("/atividades/{id_da_atividade}/lancamentos", status_code=201)
def lancar_resultados_da_atividade_rota(
    id_da_atividade: uuid.UUID,
    entrada: LancarResultadosDaAtividadeEntrada,
    contexto: Annotated[
        ContextoDaSessao,
        Depends(
            exigir_permissao(
                Operacao.lancamentos_e_pontuacao_negativa_das_suas_atividades, "escreve"
            )
        ),
    ],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    armazenamento: Annotated[PortaDeArmazenamento, Depends(dependencia_de_armazenamento)],
) -> LancamentoDaAtividadeSaida:
    """Mestre autor da trilha da atividade, ou Admin: lança o Resultado de
    todos os participantes numa operação só, sem consumir reserva nem
    alterar a situação da aula — distinto do lançamento por aula, do Admin
    (`RF-09-43`, `RF-09-44`, `RF-09-49`, `RF-09-74`).

    É também o caminho da **atividade avulsa**, do Admin, por participante
    ou pela equipe da aula (`RF-02-112`)."""
    operador = sessao_bd.get(Persona, contexto.persona_id)
    aula = sessao_bd.get(Aula, entrada.aula_id)
    atividade = sessao_bd.get(Atividade, id_da_atividade)

    resultados_declarados = [
        ResultadoDeclarado(
            guerreiro_id=item.guerreiro_id,
            atividade=atividade,
            momento_do_fato=item.momento_do_fato,
            producao=item.producao,
            desfecho=item.desfecho,
            comprovante=ComprovanteDeclarado(
                tipo=item.comprovante.tipo,
                texto=item.comprovante.texto,
                envio_id=item.comprovante.envio_id,
            )
            if item.comprovante is not None
            else None,
            julgamento=JulgamentoDeclarado(
                cumpriu=item.julgamento_do_pratico.cumpriu,
                publicavel=item.julgamento_do_pratico.publicavel,
                motivo=item.julgamento_do_pratico.motivo,
            )
            if item.julgamento_do_pratico is not None
            else None,
        )
        for item in entrada.participantes
    ]

    equipe = (
        ResultadoDaEquipe(
            equipe_id=entrada.equipe.equipe_id,
            momento_do_fato=entrada.equipe.momento_do_fato,
            producao=entrada.equipe.producao,
            desfecho=entrada.equipe.desfecho,
        )
        if entrada.equipe is not None
        else None
    )

    gravados, fora = lancar_resultados_da_atividade(
        sessao_bd,
        operador=operador,
        aula=aula,
        atividade=atividade,
        resultados=resultados_declarados,
        equipe=equipe,
        armazenamento=armazenamento,
    )
    sessao_bd.commit()
    return LancamentoDaAtividadeSaida(
        resultados=[_saida(resultado) for resultado in gravados],
        fora_por_falta_de_presenca=fora,
    )


class AbrirEnvioDoComprovanteEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tipo: str
    tipo_mime: str
    tamanho_declarado: int


class AbrirEnvioDoComprovanteSaida(BaseModel):
    envio_id: uuid.UUID
    endereco_da_sessao: str


@roteador.post("/atividades/{id_da_atividade}/lancamentos/comprovantes", status_code=201)
def abrir_envio_do_comprovante_rota(
    id_da_atividade: uuid.UUID,
    entrada: AbrirEnvioDoComprovanteEntrada,
    requisicao: Request,
    contexto: Annotated[
        ContextoDaSessao,
        Depends(
            exigir_permissao(
                Operacao.lancamentos_e_pontuacao_negativa_das_suas_atividades, "escreve"
            )
        ),
    ],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    armazenamento: Annotated[PortaDeArmazenamento, Depends(dependencia_de_armazenamento)],
) -> AbrirEnvioDoComprovanteSaida:
    """`RF-09-149`: abre, antes do lançamento, o envio retomável do comprovante
    em mídia. Quem envia, a lista e o teto são de `abrir_envio_do_comprovante`;
    os bytes nunca passam por aqui."""
    envio_id, endereco = abrir_envio_do_comprovante(
        sessao_bd,
        operador=sessao_bd.get(Persona, contexto.persona_id),
        atividade=sessao_bd.get(Atividade, id_da_atividade),
        tipo=entrada.tipo,
        tipo_mime=entrada.tipo_mime,
        tamanho_declarado=entrada.tamanho_declarado,
        armazenamento=armazenamento,
        origem=requisicao.headers.get("Origin"),
    )
    return AbrirEnvioDoComprovanteSaida(envio_id=envio_id, endereco_da_sessao=endereco)


class ResultadoDaAulaSaida(BaseModel):
    """O Resultado lido na tela da aula: o Guerreiro(a) por **nick**, nunca
    pelo nome civil (`RN-09-18`), e o comprovante — o texto ou o endereço, e
    se há arquivo, cujos bytes vão pela rota própria (`RF-09-151`)."""

    id: uuid.UUID
    guerreiro_id: uuid.UUID
    nick: str | None
    atividade_id: uuid.UUID
    atividade_titulo: str
    momento_do_fato: DataHoraComFuso
    desfecho: str
    comprovante_tipo: str
    comprovante_texto: str | None
    tem_arquivo: bool


@roteador.get("/aulas/{id_da_aula}/resultados")
def listar_resultados_da_aula_rota(
    id_da_aula: uuid.UUID,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_permissao(Operacao.suas_turmas, "le"))],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> list[ResultadoDaAulaSaida]:
    """`RF-09-151`: os Resultados lançados na aula — o Admin vê todos, o Mestre
    os das atividades de que é autor. Sem paginação: o encontro é do tamanho da
    sala, como as presenças."""
    linhas = listar_resultados_da_aula(
        sessao_bd,
        operador=sessao_bd.get(Persona, contexto.persona_id),
        aula=sessao_bd.get(Aula, id_da_aula),
    )
    ids = {resultado.guerreiro_id for resultado, _ in linhas}
    nicks = (
        dict(sessao_bd.query(Nick.persona_id, Nick.valor).filter(Nick.persona_id.in_(ids)).all())
        if ids
        else {}
    )
    return [
        ResultadoDaAulaSaida(
            id=resultado.id,
            guerreiro_id=resultado.guerreiro_id,
            nick=nicks.get(resultado.guerreiro_id),
            atividade_id=atividade.id,
            atividade_titulo=atividade.titulo,
            momento_do_fato=resultado.momento_do_fato,
            desfecho=resultado.desfecho.value,
            comprovante_tipo=resultado.comprovante_tipo.value,
            comprovante_texto=resultado.producao,
            tem_arquivo=resultado.comprovante_referencia is not None,
        )
        for resultado, atividade in linhas
    ]


@roteador.get("/resultados/{id_do_resultado}/comprovante")
def ler_comprovante_do_resultado_rota(
    id_do_resultado: uuid.UUID,
    contexto: Annotated[ContextoDaSessao, Depends(exigir_permissao(Operacao.suas_turmas, "le"))],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
    armazenamento: Annotated[PortaDeArmazenamento, Depends(dependencia_de_armazenamento)],
) -> Response:
    """`RF-09-151`: os bytes do comprovante em mídia, ao Mestre autor da
    atividade e ao Admin."""
    arquivo = ler_arquivo_do_comprovante(
        sessao_bd,
        operador=sessao_bd.get(Persona, contexto.persona_id),
        resultado=sessao_bd.get(Resultado, id_do_resultado),
        armazenamento=armazenamento,
    )
    return Response(content=arquivo.bytes_do_arquivo, media_type=arquivo.tipo_mime)
