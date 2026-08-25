import uuid

from sqlalchemy.orm import Session

from ..armazenamento.porta import PortaDeArmazenamento
from ..erros import ArquivoAcimaDoTeto, ErroDeValidacao
from ..personas.modelo import Persona
from ..trilhas.modelo import Missao, Trilha
from ..trilhas.regra import conferir_autoria_estrita_da_trilha
from .modelo import AutoriaDoConteudo, ConteudoDaMissao, TipoDeConteudo

# A lista fechada do `RF-09-115`, em MIME — a mesma moeda que
# `aportes.regra._FORMATOS_DE_COMPROVANTE_ACEITOS` já usa para o
# comprovante.
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

# Teto por tipo, nunca por missão — a missão admite mais de um vídeo e mais
# de um arquivo, cada um dentro do próprio teto (`RF-09-16` a `RF-09-18`,
# `RN-09-06`, decisão do fundador de 2026-08-25).
_TAMANHO_TETO_VIDEO = 200 * 1024 * 1024
_TAMANHO_TETO_ARQUIVO = 20 * 1024 * 1024


def _formatar_mb(tamanho_em_bytes: int) -> str:
    return f"{tamanho_em_bytes / (1024 * 1024):.0f} MB"


def _teto_do_tipo(tipo: TipoDeConteudo) -> int:
    return _TAMANHO_TETO_VIDEO if tipo == TipoDeConteudo.video else _TAMANHO_TETO_ARQUIVO


def _referencia_do_arquivo(conteudo: ConteudoDaMissao) -> str:
    return f"conteudos/{conteudo.id}/arquivo"


def _trilha_da_missao(sessao: Session, missao: Missao) -> Trilha:
    return sessao.get(Trilha, missao.trilha_id)


def criar_conteudo(
    sessao: Session,
    *,
    operador: Persona,
    missao: Missao | None,
    tipo: str | None,
    ordem: int,
    corpo: str | None,
    endereco: str | None,
    autoria: str | None,
    fonte: str | None,
) -> ConteudoDaMissao:
    """Autoria estrita do Mestre autor da trilha, o mesmo 403 que a
    publicação já usa — outro Mestre e o Admin são recusados (`RF-09-14`,
    `RF-09-15`, `RN-09-16`). Cada tipo exige só o que lhe cabe: texto pede
    corpo, link externo pede endereço; imagem, vídeo e arquivo nascem sem
    bytes (design — decisão 4). Terceiro exige fonte; próprio nunca a exige
    (`RF-09-24`).
    """
    if missao is None:
        raise ErroDeValidacao(mensagem="Conteúdo exige uma missão.", campo="missao_id")
    conferir_autoria_estrita_da_trilha(_trilha_da_missao(sessao, missao), operador)

    try:
        tipo_valido = TipoDeConteudo(tipo)
    except ValueError as exc:
        raise ErroDeValidacao(
            mensagem="Tipo de conteúdo fora dos valores previstos.", campo="tipo"
        ) from exc

    if tipo_valido == TipoDeConteudo.texto and (corpo is None or not corpo.strip()):
        raise ErroDeValidacao(mensagem="Conteúdo de texto exige o corpo.", campo="corpo")
    if tipo_valido == TipoDeConteudo.link_externo and (endereco is None or not endereco.strip()):
        raise ErroDeValidacao(
            mensagem="Conteúdo de link externo exige o endereço.", campo="endereco"
        )

    try:
        autoria_valida = AutoriaDoConteudo(autoria)
    except ValueError as exc:
        raise ErroDeValidacao(
            mensagem="Autoria fora dos valores previstos.", campo="autoria"
        ) from exc
    if autoria_valida == AutoriaDoConteudo.terceiro and (fonte is None or not fonte.strip()):
        raise ErroDeValidacao(mensagem="Conteúdo de terceiro exige a fonte.", campo="fonte")

    conteudo = ConteudoDaMissao(
        missao_id=missao.id,
        ordem=ordem,
        tipo=tipo_valido,
        corpo=corpo if tipo_valido == TipoDeConteudo.texto else None,
        endereco=endereco if tipo_valido == TipoDeConteudo.link_externo else None,
        autoria=autoria_valida,
        fonte=fonte if autoria_valida == AutoriaDoConteudo.terceiro else None,
        autor_id=operador.id,
        papel_do_autor=operador.papel.value,
    )
    sessao.add(conteudo)
    sessao.flush()
    return conteudo


def abrir_envio(
    sessao: Session,
    conteudo: ConteudoDaMissao | None,
    *,
    operador: Persona,
    tipo_mime: str | None,
    tamanho_declarado: int | None,
    armazenamento: PortaDeArmazenamento,
) -> str:
    """Confere autoria, formato e teto **antes** de abrir a sessão — a
    recusa de formato e de tamanho acontece sem nenhum byte enviado
    (`RF-09-16`, `RF-09-17`, `RF-09-115`, `RN-09-06`, design — decisão 1)."""
    if conteudo is None:
        raise ErroDeValidacao(mensagem="Conteúdo não encontrado.", campo="conteudo_id")
    missao = sessao.get(Missao, conteudo.missao_id)
    conferir_autoria_estrita_da_trilha(_trilha_da_missao(sessao, missao), operador)

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

    teto = _teto_do_tipo(conteudo.tipo)
    if tamanho_declarado > teto:
        raise ArquivoAcimaDoTeto(
            mensagem=(
                f"O arquivo tem {_formatar_mb(tamanho_declarado)} e o limite para este tipo "
                f"de conteúdo é {_formatar_mb(teto)}."
            )
        )

    return armazenamento.abrir_sessao(
        referencia=_referencia_do_arquivo(conteudo),
        tipo_mime=tipo_mime,
        tamanho_declarado=tamanho_declarado,
    )


def confirmar_envio(
    sessao: Session,
    conteudo: ConteudoDaMissao | None,
    *,
    operador: Persona,
    armazenamento: PortaDeArmazenamento,
) -> ConteudoDaMissao:
    """Só grava a referência depois de consultar o armazenamento pelo
    tamanho **real** — o teto vale de novo aqui, porque o recebido pode
    divergir do declarado na abertura (`RF-09-16`, `RF-09-17`, design —
    decisão 1)."""
    if conteudo is None:
        raise ErroDeValidacao(mensagem="Conteúdo não encontrado.", campo="conteudo_id")
    missao = sessao.get(Missao, conteudo.missao_id)
    conferir_autoria_estrita_da_trilha(_trilha_da_missao(sessao, missao), operador)

    envio = armazenamento.consultar_envio(referencia=_referencia_do_arquivo(conteudo))
    if envio is None:
        raise ErroDeValidacao(mensagem="O envio ainda não foi concluído.", campo="arquivo")

    teto = _teto_do_tipo(conteudo.tipo)
    if envio.tamanho > teto:
        raise ArquivoAcimaDoTeto(
            mensagem=(
                f"O arquivo enviado tem {_formatar_mb(envio.tamanho)} e o limite para este "
                f"tipo de conteúdo é {_formatar_mb(teto)}."
            )
        )

    conteudo.referencia = _referencia_do_arquivo(conteudo)
    conteudo.tamanho = envio.tamanho
    sessao.flush()
    return conteudo


def consultar_conteudos_da_missao(sessao: Session, missao_id: uuid.UUID) -> list[ConteudoDaMissao]:
    return (
        sessao.query(ConteudoDaMissao)
        .filter_by(missao_id=missao_id)
        .order_by(ConteudoDaMissao.ordem)
        .all()
    )
