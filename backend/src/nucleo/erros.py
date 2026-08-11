from pydantic import BaseModel


class CorpoDeErro(BaseModel):
    codigo: str
    mensagem: str
    campo: str | None = None


class ErroDeAplicacao(Exception):
    """Erro que os manipuladores convertem no corpo único de `CorpoDeErro`."""

    status_code: int
    codigo: str
    mensagem: str

    def __init__(self, mensagem: str | None = None, *, campo: str | None = None) -> None:
        self.mensagem = mensagem or self.mensagem
        self.campo = campo
        super().__init__(self.mensagem)


class ChaveInvalida(ErroDeAplicacao):
    status_code = 401
    codigo = "chave_invalida"
    mensagem = "Chave de aplicação ausente, inválida ou revogada."


class SessaoAusente(ErroDeAplicacao):
    status_code = 401
    codigo = "sessao_ausente"
    mensagem = "Esta rota exige uma sessão de persona autenticada."


class NaoEncontrado(ErroDeAplicacao):
    status_code = 404
    codigo = "nao_encontrado"
    mensagem = "Recurso não encontrado."


class ParametroInvalido(ErroDeAplicacao):
    status_code = 422
    codigo = "parametro_invalido"
    mensagem = "Parâmetro inválido."


class ParametroDesconhecido(ErroDeAplicacao):
    status_code = 422
    codigo = "parametro_desconhecido"
    mensagem = "Parâmetro não reconhecido por esta rota."


class TamanhoDePaginaAcimaDoTeto(ErroDeAplicacao):
    status_code = 422
    codigo = "tamanho_de_pagina_acima_do_teto"
    mensagem = "Tamanho de página acima do teto permitido."


class ErroDeValidacao(ErroDeAplicacao):
    status_code = 422
    codigo = "erro_de_validacao"
    mensagem = "Campo inválido ou em falta."


class ErroInterno(ErroDeAplicacao):
    status_code = 500
    codigo = "erro_interno"
    mensagem = "Ocorreu um erro inesperado. Tente novamente em instantes."
