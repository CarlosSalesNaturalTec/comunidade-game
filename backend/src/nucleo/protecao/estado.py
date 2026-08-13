from collections.abc import Callable

from starlette.requests import Request


def obter_ou_criar[T](request: Request, atributo: str, fabrica: Callable[[], T]) -> T:
    """Singleton por processo, guardado em `app.state` — nasce na primeira
    chamada e vive enquanto o contêiner viver, sem gravação em disco
    (`RN-01-45`). Um `app` novo (como o de cada teste) começa sempre vazio.
    """
    if not hasattr(request.app.state, atributo):
        setattr(request.app.state, atributo, fabrica())
    return getattr(request.app.state, atributo)
