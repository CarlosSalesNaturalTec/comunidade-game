"""Lista de formatos e tetos de tamanho do envio de mídia do Guerreiro(a).

A criação original e a comprovação do desafio prático são a **mesma** mídia de
criança, entregue pelo mesmo aparelho ao mesmo armazenamento, e por isso leem a
lista e os tetos daqui em vez de cada uma manter a sua (design — decisão 4).
Os valores são os que a criação original já praticava; nada muda de
comportamento ao sair de lá.

O teto é **por tipo**, nunca por entrega. O conteúdo da missão, que é do Mestre
e tem o enum `TipoDeConteudo` dele, segue com a cópia própria: é outro papel,
outro requisito e outro enum, e unificá-lo não é desta fatia.
"""

from ..criacoes_originais.modelo import TipoDeProducaoDaCriacaoOriginal

FORMATOS_DE_ENVIO_ACEITOS = frozenset(
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

TAMANHO_TETO_VIDEO = 200 * 1024 * 1024
TAMANHO_TETO_ARQUIVO = 20 * 1024 * 1024

FORMATOS_ACEITOS_EM_TEXTO = "MP4, WebM, JPG, PNG, WebP, MP3 e PDF"


def formatar_mb(tamanho_em_bytes: int) -> str:
    return f"{tamanho_em_bytes / (1024 * 1024):.0f} MB"


def teto_do_tipo_de_producao(tipo: TipoDeProducaoDaCriacaoOriginal) -> int:
    return (
        TAMANHO_TETO_VIDEO
        if tipo == TipoDeProducaoDaCriacaoOriginal.video
        else TAMANHO_TETO_ARQUIVO
    )
