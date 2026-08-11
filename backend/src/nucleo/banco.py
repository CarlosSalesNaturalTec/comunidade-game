from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from .configuracao import obter_configuracao


class Base(DeclarativeBase):
    pass


_engine = None
_fabrica_de_sessao: sessionmaker[Session] | None = None


def obter_fabrica_de_sessao() -> sessionmaker[Session]:
    global _engine, _fabrica_de_sessao
    if _fabrica_de_sessao is None:
        _engine = create_engine(obter_configuracao().dsn_banco, pool_pre_ping=True)
        _fabrica_de_sessao = sessionmaker(bind=_engine, expire_on_commit=False)
    return _fabrica_de_sessao


def obter_sessao() -> Iterator[Session]:
    fabrica = obter_fabrica_de_sessao()
    sessao = fabrica()
    try:
        yield sessao
    finally:
        sessao.close()
