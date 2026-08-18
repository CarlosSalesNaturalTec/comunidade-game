import uuid

import pytest
from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Mapped, mapped_column

from nucleo.autoria import ComAutoria
from nucleo.banco import Base


class _RegistroDeExemplo(Base, ComAutoria):
    """Modelo só de teste, para exercitar o mixin sem inventar entidade de
    domínio (mesmo padrão de `test_convencoes.py` para `ComMomentoDoFato`)."""

    __tablename__ = "registro_de_exemplo_autoria"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


def test_escrita_grava_autor_papel_e_data_e_hora(conexao, criar_persona):
    persona = criar_persona()
    with conexao.begin_nested():
        conexao.execute(
            insert(_RegistroDeExemplo.__table__).values(
                autor_id=persona.id, papel_do_autor=persona.papel.value
            )
        )
        linha = conexao.execute(select(_RegistroDeExemplo.__table__)).one()

    assert linha.autor_id == persona.id
    assert linha.papel_do_autor == persona.papel.value
    assert linha.registrado_em is not None


def test_registro_exige_autor(conexao):
    with pytest.raises(IntegrityError), conexao.begin_nested():
        conexao.execute(insert(_RegistroDeExemplo.__table__).values(papel_do_autor="admin"))


def test_autor_id_e_um_uuid_valido(conexao, criar_persona):
    persona = criar_persona()
    with conexao.begin_nested():
        conexao.execute(
            insert(_RegistroDeExemplo.__table__).values(
                autor_id=persona.id, papel_do_autor=persona.papel.value
            )
        )
        linha = conexao.execute(select(_RegistroDeExemplo.__table__)).one()
    assert isinstance(linha.autor_id, uuid.UUID)
