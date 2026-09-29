import uuid
from datetime import datetime
from urllib.parse import urlsplit

from sqlalchemy.orm import Session

from ..erros import ErroDeValidacao
from ..tempo import agora
from .modelo import ConteudoInstitucional, SecaoInstitucional

TAMANHO_MAXIMO_DO_LINK = 2048


def ler_conteudo_institucional(sessao: Session) -> list[ConteudoInstitucional]:
    """As três seções, na ordem fixa do enum, publicadas ou não. A ausente
    volta sem texto, e nenhum texto de exemplo ocupa o lugar (`RF-03-45`)."""
    existentes = {linha.secao: linha for linha in sessao.query(ConteudoInstitucional).all()}
    return [
        existentes.get(secao) or ConteudoInstitucional(secao=secao) for secao in SecaoInstitucional
    ]


def _validar_link_do_video(secao: SecaoInstitucional, video_url: str | None) -> str | None:
    if video_url is None:
        return None
    if secao is not SecaoInstitucional.quem_somos:
        raise ErroDeValidacao('O vídeo de apresentação só vai em "Quem somos".', campo="video_url")
    partes = urlsplit(video_url)
    if partes.scheme != "https" or not partes.netloc or len(video_url) > TAMANHO_MAXIMO_DO_LINK:
        raise ErroDeValidacao("O link do vídeo precisa ser um endereço https.", campo="video_url")
    return video_url


def publicar_secao(
    sessao: Session,
    secao: SecaoInstitucional,
    *,
    texto: str,
    video_url: str | None,
    autor_id: uuid.UUID | None,
    publicado_em: datetime | None = None,
) -> ConteudoInstitucional:
    """Publica a seção substituindo a versão vigente. Publicar sem o link
    retira o anterior (`RF-02-80`, `RF-03-49`)."""
    if not texto or not texto.strip():
        raise ErroDeValidacao("O texto da seção é obrigatório.", campo="texto")
    link = _validar_link_do_video(secao, video_url)

    linha = sessao.get(ConteudoInstitucional, secao)
    if linha is None:
        linha = ConteudoInstitucional(secao=secao)
        sessao.add(linha)
    linha.texto = texto
    linha.video_url = link
    linha.autor_id = autor_id
    linha.publicado_em = publicado_em or agora()
    sessao.flush()
    return linha
