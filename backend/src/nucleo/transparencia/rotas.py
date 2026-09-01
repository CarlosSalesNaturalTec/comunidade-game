import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..autenticacao import ContextoDaSessao
from ..banco import obter_sessao
from ..permissoes import Operacao, exigir_permissao
from ..responsaveis.regra import exigir_vinculo_do_responsavel
from .regra import consultar_catalogo_de_dados

roteador = APIRouter()


class ItemDoCatalogoSaida(BaseModel):
    dado: str
    finalidade: str
    prazo: str
    restrito_a_gestao: bool
    guardado: bool


@roteador.get("/eu/guerreiros/{id}/dados", response_model=list[ItemDoCatalogoSaida])
def consultar_dados_do_vinculado_rota(
    id: uuid.UUID,
    contexto: Annotated[
        ContextoDaSessao,
        Depends(exigir_permissao(Operacao.guerreiros_sob_sua_responsabilidade, "le")),
    ],
    sessao_bd: Annotated[Session, Depends(obter_sessao)],
) -> list[ItemDoCatalogoSaida]:
    """Restrita ao responsável vinculado — 403 sem vínculo, sem revelar
    dado algum (`RN-13-04`) —, com o catálogo declarado, cada item com a
    marca do que está guardado hoje, sem conteúdo (`RF-13-29`, `RN-13-20`)."""
    exigir_vinculo_do_responsavel(
        sessao_bd, papel=contexto.papel, responsavel_id=contexto.persona_id, guerreiro_id=id
    )
    catalogo = consultar_catalogo_de_dados(sessao_bd, guerreiro_id=id)
    return [
        ItemDoCatalogoSaida(
            dado=item.dado,
            finalidade=item.finalidade,
            prazo=item.prazo,
            restrito_a_gestao=item.restrito_a_gestao,
            guardado=item.guardado,
        )
        for item in catalogo
    ]
