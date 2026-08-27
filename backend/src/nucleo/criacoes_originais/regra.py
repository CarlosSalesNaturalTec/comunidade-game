import uuid
from datetime import UTC, datetime

from sqlalchemy import or_
from sqlalchemy.orm import Session

from ..armazenamento.porta import PortaDeArmazenamento
from ..culminancias.modelo import Culminancia, ModalidadeDaCulminancia
from ..equipes.modelo import Equipe, IntegranteDaEquipe
from ..erros import (
    ArquivoAcimaDoTeto,
    CriacaoOriginalJaValidada,
    ErroDeValidacao,
    NaoEncontrado,
    PermissaoNegada,
    TrilhaSemCulminanciaDeclarada,
)
from ..personas.modelo import Papel, Persona
from ..pontuacao.regra import creditar_pontuacao_da_criacao_original
from ..trilhas.modelo import Trilha
from ..trilhas.regra import conferir_posse_da_trilha
from .modelo import CriacaoOriginal, SituacaoDaCriacaoOriginal, TipoDeProducaoDaCriacaoOriginal

# O mesmo teto e a mesma lista de formatos que `conteudos.regra` já usa: a
# criação original espelha a sessão retomável de envio, sem régua própria
# (design — decisão 4).
_FORMATOS_DE_ENVIO_ACEITOS = frozenset(
    {
        "video/mp4",
        "video/webm",
        "image/jpeg",
        "image/png",
        "image/webp",
        "audio/mpeg",
        "application/pdf",
    }
)
_TAMANHO_TETO_VIDEO = 200 * 1024 * 1024
_TAMANHO_TETO_ARQUIVO = 20 * 1024 * 1024

_TIPOS_DE_TEXTO_LIVRE = frozenset(
    {TipoDeProducaoDaCriacaoOriginal.texto, TipoDeProducaoDaCriacaoOriginal.link_externo}
)
_TIPOS_DE_MIDIA = frozenset(
    {
        TipoDeProducaoDaCriacaoOriginal.imagem,
        TipoDeProducaoDaCriacaoOriginal.video,
        TipoDeProducaoDaCriacaoOriginal.arquivo,
    }
)


def _formatar_mb(tamanho_em_bytes: int) -> str:
    return f"{tamanho_em_bytes / (1024 * 1024):.0f} MB"


def _teto_do_tipo(tipo: TipoDeProducaoDaCriacaoOriginal) -> int:
    return (
        _TAMANHO_TETO_VIDEO
        if tipo == TipoDeProducaoDaCriacaoOriginal.video
        else _TAMANHO_TETO_ARQUIVO
    )


def _referencia_do_arquivo(criacao: CriacaoOriginal) -> str:
    return f"criacoes-originais/{criacao.id}/arquivo"


def _validar_tipo_e_producao(
    tipo: str | None, producao: str | None
) -> TipoDeProducaoDaCriacaoOriginal:
    try:
        tipo_valido = TipoDeProducaoDaCriacaoOriginal(tipo)
    except (ValueError, TypeError) as exc:
        raise ErroDeValidacao(
            mensagem="Tipo de produção fora dos valores previstos.", campo="tipo"
        ) from exc

    if tipo_valido == TipoDeProducaoDaCriacaoOriginal.texto and (
        producao is None or not producao.strip()
    ):
        raise ErroDeValidacao(mensagem="Criação original de texto exige o corpo.", campo="producao")
    if tipo_valido == TipoDeProducaoDaCriacaoOriginal.link_externo and (
        producao is None or not producao.strip()
    ):
        raise ErroDeValidacao(
            mensagem="Criação original de link externo exige o endereço.", campo="producao"
        )
    return tipo_valido


def entregar_criacao_original(
    sessao: Session,
    *,
    guerreiro: Persona | None,
    trilha: Trilha | None,
    equipe: Equipe | None,
    tipo: str | None,
    producao: str | None,
) -> CriacaoOriginal:
    """Segue a modalidade declarada na culminância da trilha (`RF-09-30`):
    um integrante entrega pela equipe, na em equipe, ou o próprio
    Guerreiro(a), na individual. A nova entrega, antes da validação,
    substitui a produção existente; depois de validada, é recusada
    (`RF-05-40`, `RF-05-42`, design — decisões 1, 2, 3, 4).
    """
    if trilha is None:
        raise NaoEncontrado(mensagem="Trilha não encontrada.")
    if guerreiro is None:
        raise ErroDeValidacao(
            mensagem="Criação original exige o Guerreiro(a) autor.", campo="guerreiro_id"
        )

    culminancia = sessao.query(Culminancia).filter_by(trilha_id=trilha.id).first()
    if culminancia is None:
        raise TrilhaSemCulminanciaDeclarada()

    tipo_valido = _validar_tipo_e_producao(tipo, producao)
    producao_gravada = producao if tipo_valido in _TIPOS_DE_TEXTO_LIVRE else None

    if culminancia.modalidade == ModalidadeDaCulminancia.individual:
        if equipe is not None:
            raise ErroDeValidacao(
                mensagem="Esta culminância é individual; a entrega é do próprio Guerreiro(a).",
                campo="equipe_id",
            )
        existente = (
            sessao.query(CriacaoOriginal)
            .filter_by(guerreiro_id=guerreiro.id, trilha_id=trilha.id)
            .first()
        )
        equipe_id = None
        guerreiro_id = guerreiro.id
    else:
        if equipe is None or equipe.trilha_id != trilha.id:
            raise ErroDeValidacao(
                mensagem="Criação original exige a equipe da trilha.", campo="equipe_id"
            )
        e_integrante = (
            sessao.query(IntegranteDaEquipe)
            .filter_by(equipe_id=equipe.id, persona_id=guerreiro.id)
            .first()
        )
        if e_integrante is None:
            raise PermissaoNegada(
                mensagem="Só um integrante da equipe entrega a criação original dela."
            )
        existente = sessao.query(CriacaoOriginal).filter_by(equipe_id=equipe.id).first()
        equipe_id = equipe.id
        guerreiro_id = None

    if existente is not None:
        if existente.situacao == SituacaoDaCriacaoOriginal.validada:
            raise CriacaoOriginalJaValidada()
        existente.tipo = tipo_valido
        existente.producao = producao_gravada
        existente.referencia = None
        existente.tamanho = None
        existente.situacao = SituacaoDaCriacaoOriginal.entregue
        existente.autor_id = guerreiro.id
        existente.papel_do_autor = guerreiro.papel.value
        sessao.flush()
        return existente

    criacao = CriacaoOriginal(
        trilha_id=trilha.id,
        equipe_id=equipe_id,
        guerreiro_id=guerreiro_id,
        tipo=tipo_valido,
        producao=producao_gravada,
        situacao=SituacaoDaCriacaoOriginal.entregue,
        autor_id=guerreiro.id,
        papel_do_autor=guerreiro.papel.value,
    )
    sessao.add(criacao)
    sessao.flush()
    return criacao


def _conferir_autoria_do_envio(criacao: CriacaoOriginal, operador: Persona) -> None:
    """Só quem entregou envia o arquivo da própria criação — o mesmo autor
    que `ComAutoria.autor_id` grava, na equipe ou na individual."""
    if criacao.autor_id != operador.id:
        raise PermissaoNegada(mensagem="Só quem entregou a criação original envia o arquivo.")
    if criacao.tipo not in _TIPOS_DE_MIDIA:
        raise ErroDeValidacao(
            mensagem="Esta criação original não é de um tipo que recebe arquivo.", campo="tipo"
        )


def abrir_envio_da_criacao(
    sessao: Session,
    criacao: CriacaoOriginal | None,
    *,
    operador: Persona,
    tipo_mime: str | None,
    tamanho_declarado: int | None,
    armazenamento: PortaDeArmazenamento,
) -> str:
    """Espelha `conteudos.regra.abrir_envio`: confere autoria, formato e
    teto antes de abrir a sessão (design — decisão 4)."""
    if criacao is None:
        raise NaoEncontrado(mensagem="Criação original não encontrada.")
    _conferir_autoria_do_envio(criacao, operador)

    if tipo_mime not in _FORMATOS_DE_ENVIO_ACEITOS:
        raise ErroDeValidacao(
            mensagem=(
                f"Formato '{tipo_mime}' não aceito. A lista aceita é MP4, WebM, JPG, PNG, "
                "WebP, MP3 e PDF."
            ),
            campo="tipo_mime",
        )
    if tamanho_declarado is None or tamanho_declarado <= 0:
        raise ErroDeValidacao(
            mensagem="Envio exige o tamanho declarado do arquivo.", campo="tamanho_declarado"
        )

    teto = _teto_do_tipo(criacao.tipo)
    if tamanho_declarado > teto:
        raise ArquivoAcimaDoTeto(
            mensagem=(
                f"O arquivo tem {_formatar_mb(tamanho_declarado)} e o limite para este tipo "
                f"de produção é {_formatar_mb(teto)}."
            )
        )

    return armazenamento.abrir_sessao(
        referencia=_referencia_do_arquivo(criacao),
        tipo_mime=tipo_mime,
        tamanho_declarado=tamanho_declarado,
    )


def confirmar_envio_da_criacao(
    sessao: Session,
    criacao: CriacaoOriginal | None,
    *,
    operador: Persona,
    armazenamento: PortaDeArmazenamento,
) -> CriacaoOriginal:
    """Espelha `conteudos.regra.confirmar_envio`: só grava a referência
    depois de o armazenamento confirmar o tamanho real (design —
    decisão 4)."""
    if criacao is None:
        raise NaoEncontrado(mensagem="Criação original não encontrada.")
    _conferir_autoria_do_envio(criacao, operador)

    envio = armazenamento.consultar_envio(referencia=_referencia_do_arquivo(criacao))
    if envio is None:
        raise ErroDeValidacao(mensagem="O envio ainda não foi concluído.", campo="arquivo")

    teto = _teto_do_tipo(criacao.tipo)
    if envio.tamanho > teto:
        raise ArquivoAcimaDoTeto(
            mensagem=(
                f"O arquivo enviado tem {_formatar_mb(envio.tamanho)} e o limite para este "
                f"tipo de produção é {_formatar_mb(teto)}."
            )
        )

    criacao.referencia = _referencia_do_arquivo(criacao)
    criacao.tamanho = envio.tamanho
    sessao.flush()
    return criacao


def _conferir_transicao(criacao: CriacaoOriginal, trilha: Trilha, operador: Persona) -> None:
    """Comum a validar e devolver: só o Mestre autor da trilha ou o Admin
    decidem (`RF-01-16`), e só uma entrega "entregue" aceita transição —
    o que também impede crédito duplo por chamada repetida (design —
    decisões).
    """
    conferir_posse_da_trilha(trilha, operador)
    if criacao.situacao != SituacaoDaCriacaoOriginal.entregue:
        raise ErroDeValidacao(
            mensagem="Só uma criação original entregue pode ser validada ou devolvida.",
            campo="situacao",
        )


def validar_criacao_original(
    sessao: Session, *, operador: Persona, criacao: CriacaoOriginal
) -> CriacaoOriginal:
    """Credita, na mesma transação da mudança de situação, os 50 pontos
    regulares, o nível 5 e o badge de autoria — ao autor individual ou a
    cada integrante da equipe, conforme a modalidade (`RF-01-26`,
    `RF-01-21`, `RF-09-31`, 11 §§5-7).
    """
    trilha = sessao.get(Trilha, criacao.trilha_id)
    _conferir_transicao(criacao, trilha, operador)

    criacao.situacao = SituacaoDaCriacaoOriginal.validada
    criacao.validado_por_id = operador.id
    criacao.validado_em = datetime.now(UTC)
    sessao.flush()

    creditar_pontuacao_da_criacao_original(sessao, criacao_original=criacao, trilha=trilha)
    return criacao


def devolver_criacao_original(
    sessao: Session, *, operador: Persona, criacao: CriacaoOriginal, motivo: str | None
) -> CriacaoOriginal:
    """Devolve para ajuste sem creditar nada, registrando o motivo em
    linguagem simples; a autoria original permanece (`RN-01-13`,
    `RN-05-13`, `RN-09-04`, `RF-05-42`, `RF-09-34`)."""
    if not motivo or not motivo.strip():
        raise ErroDeValidacao(mensagem="Devolução exige o motivo.", campo="motivo")

    trilha = sessao.get(Trilha, criacao.trilha_id)
    _conferir_transicao(criacao, trilha, operador)

    criacao.situacao = SituacaoDaCriacaoOriginal.devolvida
    criacao.motivo_da_devolucao = motivo
    criacao.validado_por_id = operador.id
    criacao.validado_em = datetime.now(UTC)
    sessao.flush()
    return criacao


def consultar_criacao_original_do_guerreiro_na_trilha(
    sessao: Session, *, guerreiro_id: uuid.UUID, trilha_id: uuid.UUID
) -> CriacaoOriginal | None:
    """A própria entrega do Guerreiro(a) naquela trilha, em qualquer
    situação — é o que a tela de entrega e a de devolução precisam para
    saber se já existe entrega, e com que motivo, ao reabrir a aplicação
    (`RF-05-40`, `RF-05-42`)."""
    equipes_do_guerreiro = sessao.query(IntegranteDaEquipe.equipe_id).filter_by(
        persona_id=guerreiro_id
    )
    return (
        sessao.query(CriacaoOriginal)
        .filter(CriacaoOriginal.trilha_id == trilha_id)
        .filter(
            or_(
                CriacaoOriginal.guerreiro_id == guerreiro_id,
                CriacaoOriginal.equipe_id.in_(equipes_do_guerreiro),
            )
        )
        .first()
    )


def consultar_portfolio_do_guerreiro(
    sessao: Session, *, guerreiro_id: uuid.UUID
) -> list[CriacaoOriginal]:
    """As criações validadas de que o Guerreiro(a) é creditado, pela
    equipe ou individualmente (`RF-05-43`, `RF-05-44`, `RN-05-21`)."""
    equipes_do_guerreiro = sessao.query(IntegranteDaEquipe.equipe_id).filter_by(
        persona_id=guerreiro_id
    )
    return (
        sessao.query(CriacaoOriginal)
        .filter(CriacaoOriginal.situacao == SituacaoDaCriacaoOriginal.validada)
        .filter(
            or_(
                CriacaoOriginal.guerreiro_id == guerreiro_id,
                CriacaoOriginal.equipe_id.in_(equipes_do_guerreiro),
            )
        )
        .all()
    )


def consultar_fila_do_mestre_autor(sessao: Session, *, operador: Persona) -> list[CriacaoOriginal]:
    """As criações entregues das trilhas de que o operador é autor; Admin
    lê a fila inteira, pela matriz de posse já vigente (`RF-09-31`,
    `RF-09-32`, `RF-01-16`)."""
    consulta = (
        sessao.query(CriacaoOriginal)
        .join(Trilha, Trilha.id == CriacaoOriginal.trilha_id)
        .filter(CriacaoOriginal.situacao == SituacaoDaCriacaoOriginal.entregue)
    )
    if operador.papel != Papel.admin:
        consulta = consulta.filter(Trilha.autor_id == operador.id)
    return consulta.all()
