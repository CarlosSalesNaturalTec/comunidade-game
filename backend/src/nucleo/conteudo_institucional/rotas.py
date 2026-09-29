import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from ..autenticacao import ContextoDaSessao
from ..banco import obter_sessao
from ..permissoes import Operacao, exigir_permissao
from ..tempo import DataHoraComFuso
from .modelo import SecaoInstitucional
from .regra import ler_conteudo_institucional, publicar_secao

roteador = APIRouter()


class SecaoPublicaSaida(BaseModel):
    """Só o que o visitante vê: nunca o autor da publicação (`RF-03-45`)."""

    secao: SecaoInstitucional
    texto: str | None
    video_url: str | None


class PublicarSecaoEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    texto: str
    video_url: str | None = None


class SecaoPublicadaSaida(SecaoPublicaSaida):
    autor_id: uuid.UUID | None
    publicado_em: DataHoraComFuso | None


@roteador.get("/vitrine/conteudo-institucional", response_model=list[SecaoPublicaSaida])
def ler_conteudo_institucional_rota(
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> list[SecaoPublicaSaida]:
    """Pública, sem credencial de persona e sob chave de aplicação, como
    toda leitura do prefixo `/vitrine`: "Quem somos", "Contatos" e "Como
    apoiar", nessa ordem, publicadas ou não (`RF-03-45`, `RF-03-49`,
    `RF-01-02`)."""
    return [
        SecaoPublicaSaida(secao=linha.secao, texto=linha.texto, video_url=linha.video_url)
        for linha in ler_conteudo_institucional(sessao_bd)
    ]


@roteador.put("/conteudo-institucional/{secao}")
def publicar_secao_rota(
    secao: SecaoInstitucional,
    entrada: PublicarSecaoEntrada,
    contexto: Annotated[
        ContextoDaSessao, Depends(exigir_permissao(Operacao.conteudo_institucional, "escreve"))
    ],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> SecaoPublicadaSaida:
    """Restrita a Admin — nenhuma outra persona tem `conteudo_institucional`
    na matriz. Devolve autor e data para a tela de edição (`RF-02-80`); a
    auditoria vem do `MiddlewareDeAuditoria`."""
    linha = publicar_secao(
        sessao_bd,
        secao,
        texto=entrada.texto,
        video_url=entrada.video_url,
        autor_id=contexto.persona_id,
    )
    sessao_bd.commit()
    return SecaoPublicadaSaida(
        secao=linha.secao,
        texto=linha.texto,
        video_url=linha.video_url,
        autor_id=linha.autor_id,
        publicado_em=linha.publicado_em,
    )
