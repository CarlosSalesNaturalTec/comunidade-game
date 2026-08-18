import pytest
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError

from nucleo.auditoria.modelo import Auditoria
from nucleo.erros import AuditoriaImutavel
from nucleo.personas.modelo import Papel


def test_registro_guarda_o_que_foi_gravado(sessao, criar_persona, criar_registro_de_auditoria):
    admin = criar_persona(Papel.admin)
    registro = criar_registro_de_auditoria(
        admin, acao="POST cadastrar_responsavel_rota", entidade_afetada="cadastrar_responsavel_rota"
    )

    assert registro.autor_id == admin.id
    assert registro.papel_do_autor == Papel.admin.value
    assert registro.acao == "POST cadastrar_responsavel_rota"
    assert registro.entidade_afetada == "cadastrar_responsavel_rota"
    assert registro.momento is not None
    assert registro.origem == "app-06-vitrine"


def test_registro_de_auditoria_nao_e_editado_nem_apagado_no_orm(
    sessao, criar_persona, criar_registro_de_auditoria
):
    """Imutabilidade (PRD-01 §8): corrigir um engano exige um registro novo,
    nunca a edição do anterior — o mesmo princípio de `Consentimento`."""
    admin = criar_persona(Papel.admin)
    registro = criar_registro_de_auditoria(admin)

    registro.acao = "PUT outra_acao"
    with pytest.raises(AuditoriaImutavel):
        sessao.commit()
    sessao.rollback()

    registro_intacto = sessao.get(Auditoria, registro.id)
    assert registro_intacto.acao != "PUT outra_acao"

    sessao.delete(registro_intacto)
    with pytest.raises(AuditoriaImutavel):
        sessao.commit()
    sessao.rollback()

    assert sessao.get(Auditoria, registro.id) is not None


def test_update_e_delete_em_auditoria_sao_recusados_direto_no_banco(
    conexao, sessao, criar_persona, criar_registro_de_auditoria
):
    """Fora do ORM — direto no banco — o gatilho da migração recusa também,
    como já vale para `consentimento` e `acesso_ao_template`."""
    admin = criar_persona(Papel.admin)
    registro = criar_registro_de_auditoria(admin)

    with pytest.raises(DBAPIError), conexao.begin_nested():
        conexao.execute(
            text("UPDATE auditoria SET acao = 'PUT outra_acao' WHERE id = :id"),
            {"id": str(registro.id)},
        )

    with pytest.raises(DBAPIError), conexao.begin_nested():
        conexao.execute(text("DELETE FROM auditoria WHERE id = :id"), {"id": str(registro.id)})

    ainda_existe = sessao.get(Auditoria, registro.id)
    assert ainda_existe is not None
    assert ainda_existe.acao != "PUT outra_acao"
