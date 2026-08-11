from fastapi import Request

from .erros import SessaoAusente

NOME_DO_CABECALHO_DE_SESSAO = "Authorization"


def exigir_persona(request: Request) -> None:
    """Mecanismo que distingue rota autenticada de rota pública: exige a
    credencial de persona, sem validar a sessão em si — isso é RF-01-03 a
    RF-01-19, de fatia futura. A recusa aqui nunca é a mesma da chave ausente
    (`ChaveInvalida`): são credenciais independentes (RN-01-34).
    """
    if not request.headers.get(NOME_DO_CABECALHO_DE_SESSAO):
        raise SessaoAusente()
