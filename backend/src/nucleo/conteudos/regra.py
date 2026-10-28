import enum
import uuid
from dataclasses import dataclass

from sqlalchemy import func
from sqlalchemy.orm import Session

from ..armazenamento.porta import PortaDeArmazenamento
from ..erros import ArquivoAcimaDoTeto, ErroDeValidacao, NaoEncontrado, PermissaoNegada
from ..personas.modelo import Persona
from ..trilhas.modelo import InscricaoNaTrilha, Missao, Trilha
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


def _proxima_ordem(sessao: Session, missao_id: uuid.UUID) -> int:
    """A ordem do conteúdo novo é posterior à de todos os que a missão já
    tem. É o núcleo que a atribui, não o cliente: enquanto o cliente
    declarava o número, ele declarava sempre 1, e os conteúdos da missão
    empatavam — a sequência que o Guerreiro(a) lê ficava indefinida
    (`RF-09-126`, design — decisão 2)."""
    maior = sessao.query(func.max(ConteudoDaMissao.ordem)).filter_by(missao_id=missao_id).scalar()
    return (maior or 0) + 1


def _conferir_coerencia_do_tipo(
    tipo: TipoDeConteudo, *, corpo: str | None, endereco: str | None
) -> None:
    """Cada tipo exige só o que lhe cabe — valem na correção as mesmas
    recusas da criação, senão corrigir seria a porta de entrada do estado
    que a criação recusa (`RF-09-14`, `RF-09-15`, `RF-09-123`)."""
    if tipo == TipoDeConteudo.texto and (corpo is None or not corpo.strip()):
        raise ErroDeValidacao(mensagem="Conteúdo de texto exige o corpo.", campo="corpo")
    if tipo == TipoDeConteudo.link_externo and (endereco is None or not endereco.strip()):
        raise ErroDeValidacao(
            mensagem="Conteúdo de link externo exige o endereço.", campo="endereco"
        )


def _autoria_conferida(autoria: str | None, *, fonte: str | None) -> AutoriaDoConteudo:
    """Terceiro exige fonte; próprio nunca a exige (`RF-09-24`)."""
    try:
        autoria_valida = AutoriaDoConteudo(autoria)
    except ValueError as exc:
        raise ErroDeValidacao(
            mensagem="Autoria fora dos valores previstos.", campo="autoria"
        ) from exc
    if autoria_valida == AutoriaDoConteudo.terceiro and (fonte is None or not fonte.strip()):
        raise ErroDeValidacao(mensagem="Conteúdo de terceiro exige a fonte.", campo="fonte")
    return autoria_valida


def criar_conteudo(
    sessao: Session,
    *,
    operador: Persona,
    missao: Missao | None,
    tipo: str | None,
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

    _conferir_coerencia_do_tipo(tipo_valido, corpo=corpo, endereco=endereco)
    autoria_valida = _autoria_conferida(autoria, fonte=fonte)

    conteudo = ConteudoDaMissao(
        missao_id=missao.id,
        ordem=_proxima_ordem(sessao, missao.id),
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


def corrigir_conteudo(
    sessao: Session,
    conteudo: ConteudoDaMissao | None,
    *,
    operador: Persona,
    tipo: str | None,
    corpo: str | None,
    endereco: str | None,
    autoria: str | None,
    fonte: str | None,
) -> ConteudoDaMissao:
    """O Mestre autor redeclara os campos **mutáveis** do conteúdo já
    gravado — corpo, endereço, autoria e fonte —, pelas mesmas recusas da
    criação, no molde de `personas.regra.editar_artefato_do_mestre`: a
    correção substitui o conjunto, não remenda campo a campo. A autoria
    estrita é a mesma da criação, e vale em qualquer situação da trilha,
    publicada inclusive — nada que Guerreiros e Guerreiras gravaram é
    tocado (`RF-09-123`, `RN-09-16`, decisão do fundador de 2026-10-27).

    `tipo` entra só para ser **recusado com motivo**: trocá-lo é remover o
    conteúdo e cadastrar outro, porque o tipo governa que campos existem e
    que bytes o conteúdo serve (`RN-09-45`).
    """
    if conteudo is None:
        raise NaoEncontrado(mensagem="Conteúdo não encontrado.")
    missao = sessao.get(Missao, conteudo.missao_id)
    conferir_autoria_estrita_da_trilha(_trilha_da_missao(sessao, missao), operador)

    if tipo is not None and tipo != conteudo.tipo.value:
        raise ErroDeValidacao(
            mensagem=(
                "O tipo do conteúdo não se altera. Para trocá-lo, remova este conteúdo e "
                "cadastre outro."
            ),
            campo="tipo",
        )

    _conferir_coerencia_do_tipo(conteudo.tipo, corpo=corpo, endereco=endereco)
    autoria_valida = _autoria_conferida(autoria, fonte=fonte)

    conteudo.corpo = corpo if conteudo.tipo == TipoDeConteudo.texto else None
    conteudo.endereco = endereco if conteudo.tipo == TipoDeConteudo.link_externo else None
    conteudo.autoria = autoria_valida
    conteudo.fonte = fonte if autoria_valida == AutoriaDoConteudo.terceiro else None
    sessao.flush()
    return conteudo


def remover_conteudo(
    sessao: Session,
    conteudo: ConteudoDaMissao | None,
    *,
    operador: Persona,
    armazenamento: PortaDeArmazenamento,
) -> None:
    """Apaga o conteúdo **de verdade** — nenhuma outra tabela o aponta — e,
    havendo arquivo confirmado, remove os bytes **antes** da linha: falhando
    o armazenamento, nada é apagado e a falha sobe como erro de camada, não
    como recusa do domínio (invariante 25 do documento 99, design — decisão
    6). Vale em qualquer situação da trilha, publicada inclusive. Nenhum
    lançamento entra no livro-razão: o armazenamento não é medido por ato
    (`RF-09-124`, `RF-09-20`, `RN-09-07`).
    """
    if conteudo is None:
        raise NaoEncontrado(mensagem="Conteúdo não encontrado.")
    missao = sessao.get(Missao, conteudo.missao_id)
    conferir_autoria_estrita_da_trilha(_trilha_da_missao(sessao, missao), operador)

    if conteudo.referencia is not None:
        armazenamento.remover(referencia=conteudo.referencia)
    sessao.delete(conteudo)
    sessao.flush()


class DirecaoDoMovimento(enum.StrEnum):
    """Para onde o conteúdo vai na ordem da missão. Não é coluna: o Mestre
    move, e o que se grava é a ordem resultante (`RF-09-126`)."""

    cima = "cima"
    baixo = "baixo"


def mover_conteudo(
    sessao: Session,
    conteudo: ConteudoDaMissao | None,
    *,
    operador: Persona,
    direcao: str | None,
) -> ConteudoDaMissao:
    """Troca a ordem do conteúdo com a do **vizinho** no sentido pedido. Só
    as duas linhas envolvidas mudam: a ordem é sequência, não índice, e
    renumerar o que o ato não pediu para mudar é o que
    `trilhas.regra.remover_pergunta_do_desbloqueio` já evita. Mover o
    primeiro para cima, ou o último para baixo, é recusado sem alterar nada
    (`RF-09-126`, design — decisão 3).
    """
    if conteudo is None:
        raise NaoEncontrado(mensagem="Conteúdo não encontrado.")
    missao = sessao.get(Missao, conteudo.missao_id)
    conferir_autoria_estrita_da_trilha(_trilha_da_missao(sessao, missao), operador)

    try:
        sentido = DirecaoDoMovimento(direcao)
    except ValueError as exc:
        raise ErroDeValidacao(
            mensagem="A direção do movimento é 'cima' ou 'baixo'.", campo="direcao"
        ) from exc

    irmaos = consultar_conteudos_da_missao(sessao, conteudo.missao_id)
    posicao = next(i for i, irmao in enumerate(irmaos) if irmao.id == conteudo.id)
    vizinha = posicao - 1 if sentido == DirecaoDoMovimento.cima else posicao + 1
    if vizinha < 0 or vizinha >= len(irmaos):
        raise ErroDeValidacao(
            mensagem=(
                "Este conteúdo já é o primeiro da missão."
                if sentido == DirecaoDoMovimento.cima
                else "Este conteúdo já é o último da missão."
            ),
            campo="direcao",
        )

    vizinho = irmaos[vizinha]
    conteudo.ordem, vizinho.ordem = vizinho.ordem, conteudo.ordem
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
    origem: str | None = None,
) -> str:
    """Confere autoria, formato e teto **antes** de abrir a sessão — a
    recusa de formato e de tamanho acontece sem nenhum byte enviado
    (`RF-09-16`, `RF-09-17`, `RF-09-115`, `RN-09-06`, design — decisão 1).
    `origem` é repassada ao armazenamento, que decide se aceita o envio
    vindo dela (`RF-09-19`, design — decisão 3)."""
    if conteudo is None:
        raise ErroDeValidacao(mensagem="Conteúdo não encontrado.", campo="conteudo_id")
    missao = sessao.get(Missao, conteudo.missao_id)
    conferir_autoria_estrita_da_trilha(_trilha_da_missao(sessao, missao), operador)

    # Sem esta guarda o arquivo é trocável pela porta dos fundos: a
    # referência deriva do id do conteúdo, e um segundo envio sobrescreveria
    # os bytes do primeiro (`RN-09-45`, design — decisão 5).
    if conteudo.referencia is not None:
        raise ErroDeValidacao(
            mensagem=(
                "Este conteúdo já tem arquivo enviado, e o arquivo não se troca. Para trocá-lo, "
                "remova este conteúdo e cadastre outro."
            ),
            campo="arquivo",
        )

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
        origem=origem,
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
    # O tipo vem do armazenamento, como o tamanho: o recebido pode desmentir
    # o declarado na abertura da sessão, e é este que serve os bytes de volta
    # (`RF-09-16`, `RF-09-17`, `RF-09-115`, design — decisão 2).
    conteudo.tipo_do_arquivo = envio.tipo_mime
    sessao.flush()
    return conteudo


@dataclass
class ArquivoDoConteudo:
    """Os bytes e o tipo com que eles saem — `application/octet-stream` para
    conteúdo gravado antes de o tipo passar a ser apurado (design — decisão
    2)."""

    bytes_do_arquivo: bytes
    tipo_mime: str


def ler_arquivo_do_conteudo(
    sessao: Session,
    conteudo: ConteudoDaMissao | None,
    *,
    operador: Persona,
    armazenamento: PortaDeArmazenamento,
) -> ArquivoDoConteudo:
    """A segunda saída de bytes do núcleo, no molde da primeira: serve ao
    **Mestre autor** da trilha e ao **Guerreiro(a) inscrito** nela — os
    mesmos que já leem a missão —, e a ninguém mais (`RF-05-11`,
    `RF-09-25`, design — decisão 3). Sem ela, a referência do armazenamento
    chegava à tela no lugar do conteúdo. O que a arquitetura mantém fora do
    núcleo é o **envio**, não a saída (`RN-01-28`).
    """
    if conteudo is None:
        raise NaoEncontrado(mensagem="Conteúdo não encontrado.")
    missao = sessao.get(Missao, conteudo.missao_id)
    trilha = _trilha_da_missao(sessao, missao)
    if trilha.autor_id != operador.id:
        inscrito = (
            sessao.query(InscricaoNaTrilha)
            .filter_by(guerreiro_id=operador.id, trilha_id=trilha.id)
            .first()
            is not None
        )
        if not inscrito:
            raise PermissaoNegada(
                mensagem="O arquivo do conteúdo é servido ao Mestre autor e a quem está "
                "inscrito na trilha."
            )

    if conteudo.referencia is None:
        raise NaoEncontrado(mensagem="Este conteúdo não tem arquivo.")
    return ArquivoDoConteudo(
        bytes_do_arquivo=armazenamento.ler(referencia=conteudo.referencia),
        tipo_mime=conteudo.tipo_do_arquivo or "application/octet-stream",
    )


def consultar_conteudos_da_missao(sessao: Session, missao_id: uuid.UUID) -> list[ConteudoDaMissao]:
    return (
        sessao.query(ConteudoDaMissao)
        .filter_by(missao_id=missao_id)
        .order_by(ConteudoDaMissao.ordem)
        .all()
    )
