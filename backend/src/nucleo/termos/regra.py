from dataclasses import dataclass
from datetime import datetime

from sqlalchemy.orm import Session

from ..consentimentos.modelo import TipoDeConsentimento
from ..erros import NaoEncontrado
from ..personas.modelo import Persona
from ..tempo import agora
from .modelo import LeituraDeTermo, Termo


@dataclass(frozen=True)
class VersaoDoTermo:
    versao: str
    texto: str
    vigente_desde: datetime


@dataclass(frozen=True)
class CatalogoDeTermo:
    tipo: TipoDeConsentimento
    vigente: VersaoDoTermo
    historico: list[VersaoDoTermo]


def consultar_catalogo_de_termos(
    sessao: Session, *, em: datetime | None = None
) -> list[CatalogoDeTermo]:
    """`RF-13-32`, `RF-13-33`: a versão vigente de cada tipo — a mais
    recente cujo `vigente_desde` já passou —, e as anteriores, cada uma
    com o texto e a data em que passou a valer, para que "o que valia
    naquela data" se responda sem reconstituição (design — decisão 1)."""
    momento = em or agora()
    tipos = sessao.query(Termo.tipo).distinct().all()

    catalogo: list[CatalogoDeTermo] = []
    for (tipo,) in tipos:
        versoes = (
            sessao.query(Termo)
            .filter(Termo.tipo == tipo, Termo.vigente_desde <= momento)
            .order_by(Termo.vigente_desde.desc())
            .all()
        )
        if not versoes:
            continue
        vigente, *anteriores = versoes
        catalogo.append(
            CatalogoDeTermo(
                tipo=tipo,
                vigente=VersaoDoTermo(
                    versao=vigente.versao, texto=vigente.texto, vigente_desde=vigente.vigente_desde
                ),
                historico=[
                    VersaoDoTermo(versao=v.versao, texto=v.texto, vigente_desde=v.vigente_desde)
                    for v in anteriores
                ],
            )
        )
    return catalogo


def registrar_leitura_de_termo(
    sessao: Session, *, responsavel: Persona, versao: str
) -> LeituraDeTermo:
    """`RF-13-32`: um registro por (responsável, versão) — reler a mesma
    versão devolve o registro existente em vez de criar o segundo, e a
    data do primeiro permanece (design — decisão 3). Versão fora do
    catálogo é recusada com 404."""
    existe_a_versao = sessao.query(Termo).filter_by(versao=versao).first() is not None
    if not existe_a_versao:
        raise NaoEncontrado(mensagem="Versão de termo não encontrada.", campo="versao")

    existente = (
        sessao.query(LeituraDeTermo).filter_by(responsavel_id=responsavel.id, versao=versao).first()
    )
    if existente is not None:
        return existente

    leitura = LeituraDeTermo(responsavel_id=responsavel.id, versao=versao)
    sessao.add(leitura)
    sessao.flush()
    return leitura
