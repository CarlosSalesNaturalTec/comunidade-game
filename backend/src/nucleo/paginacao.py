import base64
import json
from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends, Request
from pydantic import BaseModel

from .configuracao import Configuracao, obter_configuracao
from .erros import ErroDeValidacao, ParametroDesconhecido, TamanhoDePaginaAcimaDoTeto

# Filtros universais a toda listagem de dado de comunidade (RF-01-28). Uma rota
# soma a isso os filtros próprios do domínio que ela declarar.
FILTROS_UNIVERSAIS = frozenset({"comunidade", "periodo_inicio", "periodo_fim", "persona"})
PARAMETROS_DE_PAGINACAO = frozenset({"cursor", "tamanho"})


@dataclass(frozen=True)
class ParametrosDeListagem:
    cursor: str | None
    tamanho: int
    filtros: dict[str, str]


def contrato_de_listagem(filtros_do_dominio: frozenset[str] = frozenset()):
    """Fábrica de dependência de listagem: cada rota declara os filtros próprios
    do seu domínio, além dos universais de comunidade, período e persona.
    Parâmetro fora dessa lista é recusado com 422 (RF-01-28), nunca ignorado.
    """
    permitidos = PARAMETROS_DE_PAGINACAO | FILTROS_UNIVERSAIS | filtros_do_dominio

    def dependencia(
        request: Request,
        configuracao: Annotated[Configuracao, Depends(obter_configuracao)],
    ) -> ParametrosDeListagem:
        bruto = dict(request.query_params)

        desconhecido = next((chave for chave in bruto if chave not in permitidos), None)
        if desconhecido is not None:
            raise ParametroDesconhecido(
                mensagem=f"O parâmetro '{desconhecido}' não é aceito por esta rota.",
                campo=desconhecido,
            )

        tamanho_str = bruto.pop("tamanho", None)
        tamanho = configuracao.paginacao_tamanho_padrao
        if tamanho_str is not None:
            try:
                tamanho = int(tamanho_str)
            except ValueError as exc:
                raise ErroDeValidacao(
                    mensagem="Tamanho de página precisa ser um número inteiro.", campo="tamanho"
                ) from exc
            if tamanho < 1:
                raise ErroDeValidacao(
                    mensagem="Tamanho de página precisa ser maior que zero.", campo="tamanho"
                )
            if tamanho > configuracao.paginacao_tamanho_teto:
                raise TamanhoDePaginaAcimaDoTeto(
                    mensagem=(
                        f"Tamanho de página acima do teto de {configuracao.paginacao_tamanho_teto}."
                    ),
                    campo="tamanho",
                )

        cursor = bruto.pop("cursor", None)

        return ParametrosDeListagem(cursor=cursor, tamanho=tamanho, filtros=bruto)

    return dependencia


def codificar_cursor(valores: dict) -> str:
    bruto = json.dumps(valores, sort_keys=True, default=str).encode("utf-8")
    return base64.urlsafe_b64encode(bruto).decode("ascii")


def decodificar_cursor(cursor: str) -> dict:
    try:
        bruto = base64.urlsafe_b64decode(cursor.encode("ascii"))
        return json.loads(bruto)
    except Exception as exc:
        raise ErroDeValidacao(mensagem="Cursor de paginação inválido.", campo="cursor") from exc


class PaginaDeResultado[T](BaseModel):
    itens: list[T]
    proximo_cursor: str | None = None
